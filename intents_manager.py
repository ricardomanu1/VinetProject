
class intents_manager(object):

    def __init__(self):
        self.agent_id = 'intents_manager'

        # Estado inicial de las intenciones, en este caso vacio
        self.agent_intents = []
        self.intents = []
        self.intentsData()

# Biblioteca de planes
    def intentsData(self):
        self.intents.append(('say','utter_saludar', ['presentacion'], 'acc_fulfill','presentacion', 'acc_say', 'utter_saludar'))   

        self.intents.append(('say','utter_saludar', ['saludar','happy'], 'acc_fulfill','saludar', 'acc_say', 'utter_saludar'))        
        self.intents.append(('say','utter_saludar', ['saludar','sad'],'acc_fulfill','saludar', 'acc_say', 'utter_saludar', 'acc_new_belief','utter_interes'))

        self.intents.append(('say','utter_interes', ['utter_interes'], 'acc_say', 'utter_interes','acc_fulfill','utter_interes','acc_new_belief','estoy_interesado'))
   
        self.intents.append(('say','utter_empatizar_bien', ['estoy_interesado','estado_bien'],'acc_del_belief','estoy_interesado', 'acc_say', 'utter_empatizar_bien','acc_fulfill','utter_empatizar_mal', 'acc_new_belief','utter_preguntar'))
        self.intents.append(('say','utter_empatizar_mal', ['estoy_interesado','estado_mal'],'acc_del_belief','estoy_interesado', 'acc_say', 'utter_empatizar_mal','acc_fulfill','utter_empatizar_mal', 'acc_new_belief','utter_preguntar'))        
        
        self.intents.append(('say','utter_preguntar', ['utter_preguntar'], 'acc_say', 'utter_preguntar','acc_fulfill','utter_preguntar','acc_new_belief','he_preguntado')) 
        
        self.intents.append(('say','utter_especificar', ['he_preguntado','afirmar'],'acc_del_belief','he_preguntado', 'acc_say', 'utter_especificar', 'acc_del_belief','afirmar','acc_new_belief','utter_especificar','acc_del_belief','utter_preguntar'))  # llama a la accion action_service_options 
        self.intents.append(('say','utter_no_solicitar', ['he_preguntado','negar'],'acc_del_belief','he_preguntado', 'acc_say', 'utter_no_solicitar', 'acc_del_belief','negar','acc_new_belief','utter_no_solicitar','acc_del_belief','utter_preguntar'))  # llama a la accion action_service_options 
        self.intents.append(('say','utter_solicitar', ['he_preguntado','solicitar'],'acc_del_belief','he_preguntado','acc_say', 'utter_solicitar', 'acc_del_belief','solicitar','acc_del_belief','utter_preguntar','acc_new_belief','he_solicitado'))  # llama a la accion buscar lo solicitado
        
        self.intents.append(('say','utter_pronombre_interrogativo', ['he_solicitado','afirmar'],'acc_del_belief','he_solicitado','acc_say', 'utter_pronombre_interrogativo', 'acc_del_belief','afirmar'))  # llama a la accion buscar lo solicitado
        self.intents.append(('say','utter_dar_opciones', ['he_solicitado','negar'],'acc_del_belief','he_solicitado','acc_say', 'utter_dar_opciones', 'acc_del_belief','negar','acc_say','utter_si_no'))  # llama a la accion buscar lo solicitado
                
        self.intents.append(('say','utter_hito', ['solicitar_especifica_hito'], 'acc_say', 'utter_hito'))
       
        self.intents.append(('say','utter_despedir', ['despedir'], 'acc_say', 'utter_despedir','acc_fulfill','despedir'))

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

        # dentro de las intenciones tomar el subconjunto que cumpla [1]
        # comprobar que se cumplen las condiciones
        # enviar las acciones

    def check(self, terms, Beliefs, Emotions):
        beliefs = [b[0] for b in Beliefs]
        for i in terms:
           if i not in beliefs:
                return False
           elif Beliefs[beliefs.index(i)][1] == False:
                return False
        return True
           


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

