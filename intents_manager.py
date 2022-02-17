import numpy as np

class intents_manager(object):

    def __init__(self):
        self.agent_id = 'intents_manager'

        # Estado inicial de las intenciones, en este caso vacio
        self.agent_intents = []
        self.intents = []
        self.intentsData()

# Biblioteca de planes
    def intentsData(self):
        #acc_fulfill suceso que ha ocurrido y se mantiene
        #acc_del_belief suceso/creencia que ha ocurrido y se elimina tras cumplirse
        self.intents.append(('say','utter_presentacion', ['presentacion'], 'acc_fulfill','presentacion', 'acc_say', 'utter_presentacion'))   

        self.intents.append(('say','utter_saludar', ['saludar','happy'], 'acc_say', 'utter_saludar', 'acc_fulfill','saludar', 'acc_new_belief','muestro_interes', 'acc_new_belief','espero_respuesta'))        
        self.intents.append(('say','utter_saludar', ['saludar','sad'], 'acc_say', 'utter_saludar','acc_fulfill','saludar'))

        self.intents.append(('say','utter_estar_bien', ['empatizar','happy'], 'acc_say', 'utter_estar_bien','acc_fulfill','empatizar'))
        self.intents.append(('say','utter_estar_mal', ['empatizar','sad'], 'acc_say', 'utter_estar_mal','acc_fulfill','empatizar'))
        self.intents.append(('say','utter_estar_enfadado', ['empatizar','anger'], 'acc_say', 'utter_estar_enfadado','acc_fulfill','empatizar'))
        self.intents.append(('say','utter_estar_miedo', ['empatizar','fear'], 'acc_say', 'utter_estar_miedo','acc_fulfill','empatizar'))
        self.intents.append(('say','utter_estar_nervioso', ['empatizar','anxious'], 'acc_say', 'utter_estar_nervioso','acc_fulfill','empatizar'))
        self.intents.append(('say','utter_estar_aburrido', ['empatizar','bored'], 'acc_say', 'utter_estar_aburrido','acc_fulfill','empatizar'))
        self.intents.append(('say','utter_estar_emocionado', ['empatizar','excited'], 'acc_say', 'utter_estar_emocionado','acc_fulfill','empatizar'))
        self.intents.append(('say','utter_estar_soledad', ['empatizar','lonely'], 'acc_say', 'utter_estar_soledad','acc_fulfill','empatizar'))
        self.intents.append(('say','utter_estar_cansado', ['empatizar','tired'], 'acc_say', 'utter_estar_cansado','acc_fulfill','empatizar'))

        self.intents.append(('say','utter_interes', ['muestro_interes'], 'acc_say', 'utter_interes','acc_fulfill','muestro_interes'))
   
        self.intents.append(('say','utter_empatizar_bien', ['espero_respuesta','estado_bien'],'acc_del_belief','espero_respuesta', 'acc_say', 'utter_empatizar_bien', 'acc_new_belief','utter_preguntar'))
        self.intents.append(('say','utter_empatizar_mal', ['espero_respuesta','estado_mal'],'acc_del_belief','espero_respuesta', 'acc_say', 'utter_empatizar_mal', 'acc_new_belief','utter_animar'))        
        self.intents.append(('say','utter_empatizar_aburrimiento', ['espero_respuesta','estado_aburrimiento'],'acc_del_belief','espero_respuesta', 'acc_say', 'utter_empatizar_aburrimiento', 'acc_new_belief','dar_hitos_opciones')) 
              
        self.intents.append(('say','utter_hitos_opciones', ['dar_hitos_opciones'],'acc_del_belief','dar_hitos_opciones','acc_say', 'utter_hitos_opciones'))
        
        self.intents.append(('say','utter_animar', ['utter_animar'],'acc_del_belief','utter_animar','acc_say', 'utter_animar', 'acc_new_belief','he_preguntado_si_no'))

        self.intents.append(('say','utter_preguntar', ['utter_preguntar'], 'acc_say', 'utter_preguntar','acc_fulfill','utter_preguntar','acc_new_belief','he_preguntado')) 

        self.intents.append(('say','utter_solicitar', ['he_preguntado_si_no', 'afirmar'],'acc_del_belief','he_preguntado_si_no', 'acc_del_belief','afirmar','acc_say', 'utter_solicitar','acc_new_belief','he_solicitado')) 
        self.intents.append(('say','utter_empatizar_mal', ['he_preguntado_si_no', 'negar'],'acc_del_belief','he_preguntado_si_no', 'acc_del_belief','negar','acc_say', 'utter_empatizar_mal')) 
        
        self.intents.append(('say','utter_especificar', ['he_preguntado','afirmar'],'acc_del_belief','he_preguntado', 'acc_say', 'utter_especificar', 'acc_del_belief','afirmar','acc_new_belief','debes_especificar','acc_del_belief','utter_preguntar'))  # llama a la accion action_service_options 
        self.intents.append(('say','utter_no_solicitar', ['he_preguntado','negar'],'acc_del_belief','he_preguntado', 'acc_say', 'utter_no_solicitar', 'acc_del_belief','negar','acc_new_belief','no_solicita','acc_del_belief','utter_preguntar'))  # llama a la accion action_service_options 
        self.intents.append(('say','utter_no_solicitar', ['he_preguntado','no_solicitar'],'acc_del_belief','he_preguntado', 'acc_say', 'utter_no_solicitar', 'acc_del_belief','no_solicitar','acc_new_belief','no_solicita','acc_del_belief','utter_preguntar'))  # llama a la accion action_service_options 
        self.intents.append(('say','utter_solicitar', ['he_preguntado','solicitar'],'acc_del_belief','he_preguntado','acc_say', 'utter_solicitar', 'acc_del_belief','solicitar','acc_del_belief','utter_preguntar','acc_new_belief','he_solicitado'))  # llama a la accion buscar lo solicitado
        
        self.intents.append(('say','utter_hito', ['debes_especificar','solicitar_especifica_hito'],'acc_del_belief','debes_especificar','acc_del_belief','solicitar_especifica_hito', 'acc_say', 'utter_hito'))
        self.intents.append(('say','utter_solicitar', ['debes_especificar','solicitar'],'acc_del_belief','debes_especificar','acc_del_belief','solicitar', 'acc_say', 'utter_solicitar','acc_new_belief','he_solicitado'))
        self.intents.append(('say','utter_hito1', ['debes_especificar','hito1'],'acc_del_belief','debes_especificar','acc_del_belief','hito1', 'acc_say', 'utter_hito1'))
        self.intents.append(('say','utter_hito2', ['debes_especificar','hito2'],'acc_del_belief','debes_especificar','acc_del_belief','hito2', 'acc_say', 'utter_hito2'))
                
        self.intents.append(('say','utter_pronombre_interrogativo', ['he_solicitado','afirmar'],'acc_del_belief','he_solicitado','acc_say', 'utter_pronombre_interrogativo', 'acc_del_belief','afirmar'))  # llama a la accion buscar lo solicitado
        self.intents.append(('say','utter_dar_opciones', ['he_solicitado','negar'],'acc_del_belief','he_solicitado','acc_say', 'utter_dar_opciones', 'acc_del_belief','negar','acc_say','utter_hitos_opciones'))  # llama a la accion buscar lo solicitado
                
        self.intents.append(('say','utter_hito', ['solicitar_especifica_hito'],'acc_del_belief','solicitar_especifica_hito', 'acc_say', 'utter_hito'))
        self.intents.append(('say','utter_hito1', ['hito1'], 'acc_del_belief','hito1', 'acc_say', 'utter_hito1'))
        self.intents.append(('say','utter_hito2', ['hito2'],'acc_del_belief','hito2', 'acc_say', 'utter_hito2'))
       
        self.intents.append(('say','utter_despedir', ['despedir'], 'acc_say', 'utter_despedir','acc_fulfill','despedir'))
        self.intents.append(('say','utter_responder_hora', ['pregunta_hora'], 'acc_say', 'utter_responder_hora','acc_del_belief','pregunta_hora'))

        #self.intents.append(('say', 'utter_estar_bien', ['empatizar','happy'], 'acc_say', 'utter_estar_bien','acc_fulfill', 'empatizar'))
        #self.intents.append(('say', 'utter_estar_mal', ['empatizar','sad'], 'acc_say', 'utter_estar_mal','acc_fulfill', 'empatizar'))

        #self.intents.append(('say', 'utter_agradecer', ['agradecer'], 'acc_say', 'utter_preguntar','acc_fulfill', 'agradecer')) 
        
        #self.intents.append(('say', 'utter_hito1', ['utter_dar_opciones','hito1'], 'acc_say', 'utter_hito1','acc_del_belief', 'utter_dar_opciones')) 
        #self.intents.append(('say', 'utter_hito2', ['utter_dar_opciones','hito2'], 'acc_say', 'utter_hito2','acc_del_belief', 'utter_dar_opciones')) 



    def filterI(self, Emotions, Beliefs, Desires):
        desires_fulfill = []
        intents_selected = [i for i in self.intents if i[1] in [d[1] for d in Desires]]
        # print('todas las intenciones coincidentes')
        #print(intents_selected)
        #print('---------------')
        for intent in intents_selected:
            if intents_manager.check(self, intent[2], Beliefs, Emotions):
                self.agent_intents.append(intent) 
                desires_fulfill.append(intent[1])
        for idx,ele in enumerate(Desires):
            if ele[1] in desires_fulfill:
                del Desires[idx]               
        #print("el conj de intenciones es:" +  str(len(self.agent_intents)) + " con creencia " + Beliefs)

        #if(len(self.agent_intents)==0):
        #    print("la creencia sin nada es:" + Beliefs.belief_event)
        #    Beliefs.del_belief(Beliefs.belief_event)

        # dentro de las intenciones tomar el subconjunto que cumpla [1]
        # comprobar que se cumplen las condiciones
        # enviar las acciones

    def check(self, terms, Beliefs, Emotions):
        beliefs = [b[0] for b in Beliefs.agent_beliefs]
        Belief_check = Beliefs.agent_beliefs
        for i in terms:
           if i not in beliefs:
                return False
           elif Belief_check[beliefs.index(i)][1] == False:
                return False
        return True
           
    def get_context(self):
        context_intents = [x[2] for x in self.intents]        
        context = set(np.concatenate(context_intents))
        return context

#intents
#i_tuple = ('','',[,],''...)

# REGLAS
# say saludar: saludo happy -> utter_saludar say interes
# say interes: true -> utter_interes
# say empatizar_bien: interes estado_bien -> utter_empatizar_bien new_belief preguntar
# say empatizar_mal: interes estado_mal -> utter_empatizar_mal new_belief preguntar
# say preguntar: true -> utter_preguntar



# say empatizar empatizado happy utter_empatizar_bien
# say empatizar empatizado sad utter_empatizar_mal
# 

