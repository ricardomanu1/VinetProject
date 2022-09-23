import os
import json
import typing
import importlib
import datetime as dt
import xml.etree.cElementTree as ET
import numpy as np

from emotions_manager import emotions_manager
from belief_manager import belief_manager
from desires_manager import desires_manager
from intents_manager import intents_manager 

from os import listdir
from typing import Any, Text, Dict, List

from rasa_sdk import events
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, BotUttered, UserUttered, EventType

from rasa.shared.nlu.training_data.loading import load_data

if typing.TYPE_CHECKING:
    from rasa_sdk.trackers import DialogueStateTracker
    from rasa_sdk.dispatcher import Dispatcher
    from rasa_sdk.domain import Domain

# Variables globales
user_intent = ''
count = 0
Bi = ''
Be = ''
lang = 'es-ES'

# Gestor EBDI
Emotions = emotions_manager()
Beliefs = belief_manager()
Desires = desires_manager()        
Intents = intents_manager()
context = Intents.get_context()

# Memoria del Bot
slot_people = 0
slot_hito = 0
slot_emotion = ''
slot_posXY = [0,0]
slot_name = ''
slot_daytime = ''

# Methods
def __init__(self):
    self.agent_id = 'actions'

def contador():
    # Numero de respuestas que se van a generar
    global count
    count = count + 1
    return []

def get_latest_event(events):
    # Toma el ultimo evento que se ha generado para captar la respuesta que ha seleccionado el bot del Domain
    latest_actions = []
    for e in events:
        if e['event'] == 'bot':
            latest_actions.append(e)
    return latest_actions

def part_of_day(x):
    # Proporciona una respuesta de 'Saludar' basandose en la hora del día
    if (x > 4) and (x <= 12 ):
        return 'morning'
    elif (x > 12) and (x <= 16):
        return'afternoon'
    elif (x > 16) and (x <= 24) :
        return 'evening'
    elif (x > 24) and (x <= 4):
        return'none'

def the_day(x):
    # Saber el día en castelano
    if x == "Monday":
        return 'lunes'
    if x == "Tuesday":
        return 'martes'
    if x == "Wednesday":
        return 'miercoles'
    if x == "Thursday":
        return 'jueves'
    if x == "Friday":
        return 'viernes'
    if x == "Saturday":
        return 'sabado'
    if x == "Sunday":
        return 'domingo'

## Estructura BOT
class ChatBot(Action):

    def name(self) -> Text:
        return "chatbot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        # Acceso a variables globales
        global Bi
        global Be
        global lang
        global slot_people
        global slot_hito
        global slot_emotion
        global slot_name
        global slot_daytime
        global slot_posXY
        ## Valores de entrada, si es un texto
        intent = tracker.latest_message['intent']
        text = tracker.latest_message['text']
        entities = tracker.latest_message['entities']
        ## Slots
        slot_name = tracker.get_slot('name')       
        slot_place = tracker.get_slot('place')       
        slot_year = tracker.get_slot('year')       
        slot_milestone = tracker.get_slot('milestone')           

        Bi = intent['name']
        
        slot_daytime = part_of_day(int(f"{dt.datetime.now().strftime('%H')}"))

        id_event = tracker.latest_message['metadata']['event']

        for e in entities:
            print("entidad: {} = {}".format(e['entity'],e['value']))
       
        ## Entradas de Voz       
        if (id_event == 'say'):
            Be = tracker.latest_message['metadata']['sentiment']
            if (tracker.latest_message['metadata']['language']!=None):
                lang = tracker.latest_message['metadata']['language']
            user_event = [id_event,Bi,Be,text,slot_name,entities,lang] 
            print('----->EVENT: ' + str(user_event)) 
            if Bi in context:
                EBDI.run(self, dispatcher, tracker, domain, user_event)
            else:
                print('No se contestar a esto.')    
                
        ## Entradas de conocimiento
        elif (id_event == 'know'):
            for key, value in tracker.latest_message['metadata'].items():
                print(key, value)
            print(key)
            if (tracker.latest_message['metadata'][key]!=None):
                if key == 'people':
                    slot_people = tracker.latest_message['metadata']['people']
                elif key == 'chapter':
                    slot_hito = tracker.latest_message['metadata']['chapter'] 
                elif key == 'emotion':
                    slot_emotion = tracker.latest_message['metadata']['emotion']  
                elif key == 'posXY':
                    slot_posXY = tracker.latest_message['metadata']['posXY']  
            user_event = [id_event,text,'',''] 
            print('EVENT: ' + str(user_event)) 
            if text in context:
                EBDI.run(self, dispatcher, tracker, domain, user_event)
            else:
                print('No se que hacer con este conocimiento.')
                
        ## Entrada de acciones a realizar
        elif (id_event == 'do'):
            print('Ahora lo hago')
        else:
            print('Comando no conocido')            

        print(slot_posXY)
        ## comprobacion del diccionario de sinonimos de entidades
        synonyms_dict = Dictionary.get_synonym_mapper()
        for value, synonyms in synonyms_dict.items():
            ## print("Value:", value)
            ## print("Synonyms:", str(synonyms))
            Ricardo_synonyms = synonyms      
        
        return [SlotSet("daytime", slot_daytime)]

## Estructura EBDI
class EBDI(Action):

    def name(self) -> Text:
        return "ebdi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            user_event) -> List[Dict[Text, Any]]:          
        ## Conjunto E B D I
        global Emotions
        global Beliefs
        global Desires
        global Intents 

        # Establecen las nuevas creencias a partir del evento
        newBelief = Beliefs.new_belief(user_event)     
        
        Beliefs.del_belief(Emotions.estado)
        for e in Beliefs.emotionalBeliefs:
            Beliefs.del_belief(e)
        # Primera gestion del estado emocional
        E1 = Emotions.euf1(Intents,newBelief)
        print('PRIMARY EMOTION: ' + E1) 
        newBelief.append(['know',E1,True])        

        # BDI actualizacion        
        BDI.bdi(self,newBelief)             

        # Segunda gestion del estado emocional
        E2 = Emotions.euf2(Intents,Beliefs)
        print('SECONDARY EMOTION: ' + E2) 

        #if (inTime and E1 != E2):
        #   BDI.bdi(self,Beliefs.agent_beliefs)

        p = Plan.plan(self, Intents.agent_intents)  
        if Intents.agent_intents:
            del Intents.agent_intents[0]
            
        for i in p:
            print('--->' + i)
            exec(i) 

        return []

# actualizacion Beliefs Desires Intents
class BDI:

    def bdi(self,newBelief):     
        ## Conjunto E B D I
        global Emotions
        global Beliefs
        global Desires
        global Intents 

        #B = brf_in(E,I,Bm) # se actualizan las creencias
        Beliefs.brf_in(Emotions,Intents,newBelief)
        print('BELIEFS:')
        for belief in Beliefs.agent_beliefs:
            print(" -", belief[0], belief[1], belief[2])

        #D = options(B,I) # se crean los deseos
        Desires.options(Beliefs,Intents)
        print('DESIRES:')
        for desire in Desires.agent_desires:
            print(" -", desire[0], desire[1], desire[2])     

        #I = filterI(E,B,D,I)
        Intents.filterI(Emotions,Beliefs,Desires.agent_desires)
        print('INTENTS:')
        for intent in Intents.agent_intents:
            print(" -", intent)

        # se estan manteniendo deseos, asi que esta linea los elimina, pero... ¿se pueden mantener deseos?
        Desires.agent_desires = [] 

        return []

class Plan:

    def plan(self, Intents):
        p = []    
        for intent in Intents:
            for idx, val in enumerate(intent):    
                # Seleccionamos la primera intencion y las acciones correspondientes        
                if val == 'acc_say':  
                    resp = intent[idx+1]
                    s = "Say.run(self, dispatcher, tracker, domain,'{0}')".format(str(resp))
                    p.append((s))

                if val == 'acc_new_belief':
                    user_event = ['say',intent[idx+1],'none','','','','']   
                    s = "EBDI.run(self, dispatcher, tracker, domain,{0})".format(user_event)
                    p.append((s))

                if val == 'acc_del_belief':
                    s = "Beliefs.del_belief('{0}')".format(str(intent[idx+1]))
                    p.append(s)

                if val == 'acc_fulfill':
                    s = "Beliefs.fulfill_belief('{0}')".format(str(intent[idx+1]))
                    p.append(s)
        return p

## Acciones ##
class Say(Action):

    def name(self) -> Text:
        return "say"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            resp) -> List[Dict[Text, Any]]:
        print('la respuesta es: ' + resp)

        hours = str(f"{dt.datetime.now().strftime('%H:%M')}")
        day = the_day(str(f"{dt.datetime.now().strftime('%A')}"))

        dispatcher.utter_message(
            response = resp,           
            hours = hours,
            day = day,
            daytime = slot_daytime,
            name = slot_name,
            people = slot_people,
            hito = slot_hito,
            emotion = slot_emotion)

        contador()
        print("dispatcher: " + str(count))          
        print("daytime: " + str(tracker.get_slot('daytime')))  

        return []

## Generar los ficheros de salida
class To_Speech(Action):

    def name(self) -> Text:
        return "to_speech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        global msg
        global count   
        global Emotions

        print("Cambios tras la primera acción")

        print("daytime: " + str(tracker.get_slot('daytime')))  

        txt_responses = ''

        if count > 0:
            msg = get_latest_event(tracker.applied_events())        
            responses = msg[-count:]  
            print(Emotions.tag())
            txt = TXT()            
            print('----RESPONSES----')
            for e in responses:
                print('- ' + str(e['text']))
                txt_responses += str(e['text'])
                txt_responses += ' '            
            sentence = TXT.name(txt,txt_responses)
            #ExecuteEBDI.execute_ebdi(sentence,Emotions.tag())
        count = 0

        return []


## Salida de la respuesta emocional en txt
class TXT():
    def name(self,response) -> Text:
        output = open("speech.txt","w+")
        print("VINETbot: {} ({})".format(response,Emotions.tag()))
        #output.write(str(response))
        lines = [str(response),str(Emotions.tag()),lang]
        output.write('\n'.join(lines))
        output.close()
        return str(response)

## Salida de la respuesta emocional en XML
class ExecuteEBDI:

    def execute_ebdi(message,tag):   
        return "echo"


## Se ejecuta una sola vez al principio de una conversacion
class Dictionary:

    def get_synonym_mapper():
        result_dict = {}
        for nlu_md in os.listdir("data"):
            if nlu_md == 'nlu.md':
                path_md = "data/{0}".format(nlu_md)
                nlu_md_file = load_data(path_md)
                nlu_md_json = nlu_md_file.nlu_as_json()
                for item in json.loads(nlu_md_json)['rasa_nlu_data']['entity_synonyms']:
                    result_dict[item['value']] = item['synonyms']
        return result_dict

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Hello World")
        dispatcher.utter_message(text="Hello World!")
        return []

class You_are(Action):
    def name(self) -> Text:
        return "you_are"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:        
        entities = tracker.latest_message['entities']
        slot_name = tracker.get_slot('name')
        print(entities)

        message = "Hola, encantado de conocerte!"

        for e in entities:
            if e['entity'] == 'name':
                name = e['value']
            if name == "ricardo":
                message = "Hey " + slot_name + ", que tal?"                
            if name == "amalia":
                message = "Hola Amalia, yo soy el sargento David Robertson, encantado"
        tag = "cheerful" 
        xml = XML()
        XML.name(xml,message,tag)
        dispatcher.utter_message(text=message)
        return []

class Info_fecha(Action):

    def name(self) -> Text:
        return "info_fecha"
    def run (self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:        
        entities = tracker.latest_message['entities']
        print(entities)
        message = 'Lo siento, no he encontrado nada relacionado con esa fecha'
        for e in entities:
            if e['entity'] == 'fecha':
                fecha = e['value']
                if fecha == '1350':
                    message = "Antoine de le Puy, peregrino a santiago y alcanza a oir el sonido de una campana entre la niebla mientras desciende de la montania"
                if fecha == '1813':
                    message = "Tengo informacion sobre unos soldados que durante la guerra de independencia Española se encargaban de vigilar la frontera con Francia"
        dispatcher.utter_message(text=message)
        return []

class Buscar_informacion(Action):

    def name(self) -> Text:
        return "buscar_informacion"
    def run (self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:  
        print("Accediendo a informacion...")
        """ acceder a slot values, ahi se encuentra la fecha """
        slot_fecha = tracker.get_slot('fecha')
        print(slot_fecha)
        message = 'Error, informacion NO localizada'
        if slot_fecha == '1350':
            message = "Escuchad companieros el sonido de la campana! Roncesvalles ya esta al alcance y podremos..."
        if slot_fecha == '1813':
            message = "...A principios de octubre la nieve cayo en tal cantidad como no habia visto en Escocia. Casi perdimos..."
        dispatcher.utter_message(text=message)
        return []

class Aprendizaje(Action):

    def name(self) -> Text:
        return "aprendizaje"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:        
        entities = tracker.latest_message['entities']
        intent = tracker.latest_message['intent']
        text = tracker.latest_message['text']
        #slot_name = tracker.get_slot('name')
        print(intent)
        print(entities)        
        print(text)
        #print(tracker.latest_action_name)
        #print(tracker.slots)
        message = "Comando de aprendizaje"
        dispatcher.utter_message(text=message)
        for e in entities:
            if e['entity'] == 'name':
                name = e['value']
            if name == "ricardo":
                message = "Hola Ricardo, estoy listo para aprender"
                '''a = tracker.'''
            if name != "ricardo":
                message = "Lo siento, no estas autorizado"     
        dispatcher.utter_message(text=message)
        return []
