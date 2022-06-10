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
from inner_speech import inner_speech

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
Emotions = emotions_manager()
Beliefs = belief_manager()
Desires = desires_manager()        
Intents = intents_manager()
#InnerSpeech = inner_speech()
context = Intents.get_context()


def __init__(self):
    self.agent_id = 'actions'

def contador():
    global count
    count = count + 1
    return []

def get_latest_event(events):
    latest_actions = []
    for e in events:
        if e['event'] == 'bot':
            latest_actions.append(e)
    return latest_actions

def part_of_day(x):
    if (x > 4) and (x <= 12 ):
        return 'morning'
    elif (x > 12) and (x <= 16):
        return'afternoon'
    elif (x > 16) and (x <= 24) :
        return 'evening'
    elif (x > 24) and (x <= 4):
        return'none'

## Estructura BOT
class ChatBot(Action):

    def name(self) -> Text:
        return "chatbot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        global Bi
        global Be

        ## Valores de entrada, si es un texto
        intent = tracker.latest_message['intent']
        text = tracker.latest_message['text']
        entities = tracker.latest_message['entities']            
        ## Slots
        slot_name = tracker.get_slot('name')       
        slot_place = tracker.get_slot('place')       
        slot_year = tracker.get_slot('year')       
        slot_milestone = tracker.get_slot('milestone')   
        slot_daytime = tracker.get_slot("daytime")
        slot_people = tracker.get_slot("people")

        slot_daytime = part_of_day(int(f"{dt.datetime.now().strftime('%H')}"))
        Bi = intent['name']

        id_event = tracker.latest_message['metadata']['event']
       
        ## Entradas de Voz       
        if (id_event == 'say'):
            Be = tracker.latest_message['metadata']['sentiment']
            user_event = [id_event,Bi,Be,text,slot_name,entities] 
            print('EVENT: ' + str(user_event)) 
            if Bi in context:
                print('Se reaccionar ante esta situación')
                EBDI.run(self, dispatcher, tracker, domain, user_event)
            else:
                print('No se actuar ante esta situación')        
        ## Entradas de conocimiento
        elif (id_event == 'know'):
            print('ahora lo se')
            if (tracker.latest_message['metadata']['people']!=None):
                slot_people = tracker.latest_message['metadata']['people']
            user_event = [id_event,text,'',''] 
            print('EVENT: ' + str(user_event)) 
            if text in context:
                print('sabemos reaccionar ante esta situación')
                EBDI.run(self, dispatcher, tracker, domain, user_event)
            else:
                print('NO se actuar ante esta situación')
        ## Entrada de acciones a realizar
        elif (id_event == 'do'):
            print('ahora lo hago')
        else:
            print('comando no conocido')            

        ## comprobacion del diccionario de sinonimos de entidades
        synonyms_dict = Dictionary.get_synonym_mapper()
        for value, synonyms in synonyms_dict.items():
            ## print("Value:", value)
            ## print("Synonyms:", str(synonyms))
            Ricardo_synonyms = synonyms      

        return [SlotSet("daytime", slot_daytime),SlotSet("people", slot_people)]

## Estructura EBDI
class EBDI(Action):

    def name(self) -> Text:
        return "ebdi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
            user_event) -> List[Dict[Text, Any]]:  
        global Bi
        ## Conjunto E B D I
        global Emotions
        global Beliefs
        global Desires
        global Intents 

        # Establecen las nuevas creencias a partir del evento
        newBelief = Beliefs.new_belief(user_event)     

        # Primera gestion del estado emocional
        E1 = Emotions.euf1(Intents,newBelief)
        print('PRIMARY EMOTION: ' + E1) 

        # BDI actualizacion        
        BDI.bdi(self,newBelief)             
        #if(len(Intents.agent_intents)==0):
        #    Beliefs.del_belief(Bi)
        #    Bi = ''

        # Segunda gestion del estado emocional
        E2 = Emotions.euf2(Intents,Beliefs)
        print('SECONDARY EMOTION: ' + E2) 

        # if (inTime and E1 != E2):
        #    BDI.bdi(self,Beliefs.agent_beliefs)

       # Desires.agent_desires = [] 

        p = Plan.plan(self, Intents.agent_intents)  
        if Intents.agent_intents:
            del Intents.agent_intents[0]
            
        for i in p:
            print('---->' + i)
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
            print("--", belief[0], belief[1], belief[2])

        #D = options(B,I) # se crean los deseos
        Desires.options(Beliefs,Intents)
        print('DESIRES:')
        for desire in Desires.agent_desires:
            print("--", desire[0], desire[1], desire[2])     

        #I = filterI(E,B,D,I)
        Intents.filterI(Emotions,Beliefs,Desires.agent_desires)
        print('INTENTS:')
        for intent in Intents.agent_intents:
            print("--", intent)

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
                    user_event = ['say',intent[idx+1],'none','','','']   
                    s = "EBDI.run(self, dispatcher, tracker, domain,{0})".format(user_event)
                    p.append((s))

                if val == 'acc_del_belief':
                    s = "Beliefs.del_belief('{0}')".format(str(intent[idx+1]))
                    p.append(s)

                if val == 'acc_fulfill':
                    s = "Beliefs.fulfill_belief('{0}')".format(str(intent[idx+1]))
                    p.append(s)
                #p = acciones a realizar        
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
        # El dia actual
        print(f"{dt.datetime.now().strftime('%A')}")
        # la hora actual
        print(f"{dt.datetime.now().strftime('%H:%M:%S')}")

        #daytime = "evening"
        hours = str(f"{dt.datetime.now().strftime('%H:%M')}")
        
        name = slot_name = tracker.get_slot('name')

        #UnBuenSaludo.run(self, dispatcher, tracker, domain)
        dispatcher.utter_message(response=resp, name=name, hours = hours)
        contador()
        print("dispatcher: " + str(count))  
        print("daytime: " + str(tracker.get_slot('daytime')))  
        print("people: " + str(tracker.get_slot('people')))  

        return []

##
class action_service_options(Action):

    def name(self) -> Text:
        return "action_service_options"

    def run (self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text,Any]) -> List[Dict[Text, Any]]: 

        buttons=[
            {"payload":'/hito1{"content_type":"hito1"}',"title":"Hito 1"},
            {"payload":'/hito2{"content_type":"hito2"}',"title":"Hito 2"}
            ]

        dispatcher.utter_message(text="Hitos:", buttons=buttons)   
        return []

class To_Speech(Action):

    def name(self) -> Text:
        return "to_speech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        global msg
        global count
        
        txt_responses = ''

        if count > 0:
            msg = get_latest_event(tracker.applied_events())        
            responses = msg[-count:]  
            txt = TXT()            
            print('-----RESPONSES-----')
            for e in responses:
                print('-' + str(e['text']))
                txt_responses += str(e['text'])
                txt_responses += ' '
            #ExecuteEBDI.execute_ebdi(resp,Emotions.tag())
            TXT.name(txt,txt_responses)
        count = 0

        return []


## Salida de la respuesta emocional en XML
class ExecuteEBDI:

    def execute_ebdi(message,tag):
        xml = XML()
        XML.name(xml,message,tag)        
        return "echo"

class TXT():
    def name(self,response) -> Text:
        output = open("speech.txt","w+")
        print("VINETbot:", response)
        output.write(str(response))
        output.close()
        return "echo"


## Salida de la respuesta emocional en XML
class XML():

    def name(self,response,tag) -> Text:
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xml:lang": "en-US"})
        voice = ET.SubElement(speak, "voice", name = "en-US-AriaNeural") 
        mstts = ET.SubElement(voice, "mstts:express-as", style = tag )
        mstts.text = response
        arbol = ET.ElementTree(speak)
        arbol.write("respuesta.xml")
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

class UnBuenSaludo(Action):

    def name(self) -> Text:
        return "un_buen_saludo"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_daytime = tracker.get_slot("daytime")
        slot_people = tracker.get_slot("people")
        slot_daytime = "afternoon"
        slot_people = 9

        return [SlotSet("daytime", slot_daytime),SlotSet("people", slot_people)]

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

class GenerarXML(Action):

    def name(self) -> Text:
        return "generar_xml"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        speak = ET.Element("speak", version ="1.0", xmls = "http://www.w3.org/2001/10/synthesis", attrib={"xmlns:mstts" : "https://www.w3.org/2001/mstts","xml:lang": "en-US"})
        voice = ET.SubElement(speak, "voice", name = "en-US-AriaNeural") 
        mstts = ET.SubElement(voice, "mstts:express-as", style="cheerful" )
        mstts.text = "Mi respuesta es estar alegre."
        arbol = ET.ElementTree(speak)
        arbol.write("respuesta.xml")
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
        slot_name = tracker.get_slot('name')
        print(intent)
        print(entities)        
        print(text)
        print(tracker.latest_action_name)
        print(tracker.slots)
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
