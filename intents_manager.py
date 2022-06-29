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

        ### PLANS ###
        ## Usuario se presenta
        self.intents.append(('say','utter_presentacion', ['presentacion'], 'acc_del_belief','presentacion', 'acc_say', 'utter_presentacion'))   
        ## Usuario me saluda
        self.intents.append(('say','utter_saludar', ['saludar','happy'],'acc_say','utter_saludar','acc_fulfill','saludar','acc_new_belief','muestro_interes', 'acc_new_belief','espero_respuesta'))        
        self.intents.append(('say','utter_saludar', ['saludar','neutral'], 'acc_say', 'utter_saludar','acc_fulfill','saludar'))    
        ## Usuario se interesa por mi estado de animo
        self.intents.append(('say','utter_estar_bien', ['empatizar','happy'], 'acc_say', 'utter_estar_bien','acc_del_belief','empatizar'))
        self.intents.append(('say','utter_estar_mal', ['empatizar','sad'], 'acc_say', 'utter_estar_mal','acc_del_belief','empatizar'))
        self.intents.append(('say','utter_estar_enfadado', ['empatizar','anger'], 'acc_say', 'utter_estar_enfadado','acc_del_belief','empatizar'))
        self.intents.append(('say','utter_estar_miedo', ['empatizar','fear'], 'acc_say', 'utter_estar_miedo','acc_del_belief','empatizar'))
        self.intents.append(('say','utter_estar_nervioso', ['empatizar','anxious'], 'acc_say', 'utter_estar_nervioso','acc_del_belief','empatizar'))
        self.intents.append(('say','utter_estar_aburrido', ['empatizar','bored'], 'acc_say', 'utter_estar_aburrido','acc_del_belief','empatizar'))
        self.intents.append(('say','utter_estar_emocionado', ['empatizar','excited'], 'acc_say', 'utter_estar_emocionado','acc_del_belief','empatizar'))
        self.intents.append(('say','utter_estar_soledad', ['empatizar','lonely'], 'acc_say', 'utter_estar_soledad','acc_del_belief','empatizar'))
        self.intents.append(('say','utter_estar_cansado', ['empatizar','tired'], 'acc_say', 'utter_estar_cansado','acc_del_belief','empatizar'))        
        ## Usuario empatiza conmigo
        self.intents.append(('say','utter_afirmar', ['empatizar_bien','happy'], 'acc_say', 'utter_afirmar','acc_del_belief','empatizar_bien'))
        self.intents.append(('say','utter_negar', ['empatizar_bien','sad'], 'acc_say', 'utter_negar','acc_del_belief','empatizar_bien'))
        ## Usuario me hace preguntas basicas
        self.intents.append(('say','utter_responder_hora', ['pregunta_hora'], 'acc_say', 'utter_responder_hora','acc_del_belief','pregunta_hora'))
        self.intents.append(('say','utter_ubicarme', ['ubicarme'], 'acc_say', 'utter_ubicarme','acc_del_belief','ubicarme'))
        ## Usuario se despide
        self.intents.append(('say','utter_despedir', ['despedir'], 'acc_say', 'utter_despedir','acc_fulfill','despedir','acc_del_belief','saludar'))
        self.intents.append(('say','utter_identidad', ['identidad'], 'acc_say', 'utter_identidad','acc_fulfill','identidad'))        
        self.intents.append(('say','utter_agradecer', ['agradecer'], 'acc_say', 'utter_agradecer','acc_fulfill','agradecer'))                
        self.intents.append(('say','utter_empatizar_bien', ['estado_bien'], 'acc_say', 'utter_empatizar_bien','acc_del_belief','estado_bien'))
                        
        ## YO muestro interes por el usuario
        self.intents.append(('say','utter_interes', ['muestro_interes'], 'acc_say', 'utter_interes','acc_del_belief','muestro_interes'))
        ## YO voy a empatizar con el estado de animo del usuario  
        self.intents.append(('say','utter_empatizar_bien', ['espero_respuesta','estado_bien'],'acc_del_belief','espero_respuesta','acc_del_belief','estado_bien', 'acc_say', 'utter_empatizar_bien', 'acc_new_belief','le_pregunto'))
        self.intents.append(('say','utter_empatizar_mal', ['espero_respuesta','estado_mal'],'acc_del_belief','espero_respuesta', 'acc_say', 'utter_empatizar_mal', 'acc_new_belief','le_animo'))        
        self.intents.append(('say','utter_empatizar_aburrimiento', ['espero_respuesta','estado_aburrimiento'],'acc_del_belief','espero_respuesta', 'acc_say', 'utter_empatizar_aburrimiento', 'acc_new_belief','dar_hitos_opciones')) 
        ## YO intervengo en el estado de animo del usuario
        self.intents.append(('say','utter_animar', ['le_animo'],'acc_del_belief','le_animo','acc_say', 'utter_animar', 'acc_new_belief','he_preguntado_si_no', 'acc_new_belief','utter_animar'))
        ## YO pregunto al usuario 
        self.intents.append(('say','utter_preguntar', ['le_pregunto'], 'acc_say', 'utter_preguntar','acc_fulfill','le_pregunto','acc_new_belief','he_preguntado')) 
        self.intents.append(('say','utter_solicitar', ['utter_animar','he_preguntado_si_no', 'afirmar'],'acc_del_belief','he_preguntado_si_no','acc_del_belief','utter_animar', 'acc_del_belief','afirmar','acc_say', 'utter_solicitar','acc_new_belief','he_solicitado')) 
        self.intents.append(('say','utter_solicitar', ['he_preguntado','solicitar'],'acc_del_belief','he_preguntado','acc_say', 'utter_solicitar', 'acc_del_belief','solicitar','acc_del_belief','le_pregunto','acc_new_belief','he_solicitado'))  # llama a la accion buscar lo solicitado
        self.intents.append(('say','utter_solicitar', ['debes_especificar','solicitar'],'acc_del_belief','debes_especificar','acc_del_belief','solicitar', 'acc_say', 'utter_solicitar','acc_new_belief','he_solicitado'))
        self.intents.append(('say','utter_empatizar_mal', ['utter_animar','he_preguntado_si_no', 'negar'],'acc_del_belief','he_preguntado_si_no','acc_del_belief','utter_animar', 'acc_del_belief','negar','acc_say', 'utter_empatizar_mal')) 
        self.intents.append(('say','utter_pronombre_interrogativo', ['he_solicitado','afirmar'],'acc_del_belief','he_solicitado','acc_say', 'utter_pronombre_interrogativo', 'acc_del_belief','afirmar'))  # llama a la accion buscar lo solicitado
        ## YO propongo temas
        self.intents.append(('say','utter_dar_opciones', ['he_solicitado','negar'],'acc_del_belief','he_solicitado','acc_say', 'utter_dar_opciones', 'acc_del_belief','negar','acc_say','utter_hitos_opciones'))  # llama a la accion buscar lo solicitado
        ## YO necesito mas informacion                
        self.intents.append(('say','utter_especificar', ['he_preguntado','afirmar'],'acc_del_belief','he_preguntado', 'acc_say', 'utter_especificar', 'acc_del_belief','afirmar','acc_new_belief','debes_especificar','acc_del_belief','le_pregunto'))  # llama a la accion action_service_options 
        ## YO no continuo la conversacion
        self.intents.append(('say','utter_no_solicitar', ['he_preguntado','negar'],'acc_del_belief','he_preguntado', 'acc_say', 'utter_no_solicitar', 'acc_del_belief','negar','acc_new_belief','no_solicita','acc_del_belief','le_pregunto'))  # llama a la accion action_service_options 
        self.intents.append(('say','utter_no_solicitar', ['he_preguntado','no_solicitar'],'acc_del_belief','he_preguntado', 'acc_say', 'utter_no_solicitar', 'acc_del_belief','no_solicitar','acc_new_belief','no_solicita','acc_del_belief','le_pregunto'))  # llama a la accion action_service_options 

        ## Contexto VINET
        self.intents.append(('say','utter_hito1', ['hito1'], 'acc_say', 'utter_hito1', 'acc_del_belief','hito1'))
        self.intents.append(('say','utter_hito2', ['hito2'], 'acc_say', 'utter_hito2','acc_del_belief','hito2'))
        self.intents.append(('say','utter_hitos_opciones', ['dar_hitos_opciones'],'acc_del_belief','dar_hitos_opciones','acc_say', 'utter_hitos_opciones'))
        self.intents.append(('say','utter_hito', ['debes_especificar','solicitar_especifica_hito'],'acc_del_belief','debes_especificar','acc_del_belief','solicitar_especifica_hito', 'acc_say', 'utter_hito'))
        self.intents.append(('say','utter_hito1', ['debes_especificar','hito1'],'acc_del_belief','debes_especificar','acc_del_belief','hito1', 'acc_say', 'utter_hito1'))
        self.intents.append(('say','utter_hito2', ['debes_especificar','hito2'],'acc_del_belief','debes_especificar','acc_del_belief','hito2', 'acc_say', 'utter_hito2'))                
        self.intents.append(('say','utter_hito', ['solicitar_especifica_hito'],'acc_del_belief','solicitar_especifica_hito', 'acc_say', 'utter_hito'))
             
        self.intents.append(('say','utter_vinet', ['vinet'], 'acc_say', 'utter_vinet', 'acc_del_belief','vinet'))

        ## Conocimiento del entorno
        self.intents.append(('know', 'utter_conocer_personas', ['utter_conocer_personas'],'acc_del_belief','utter_conocer_personas','acc_say', 'utter_conocer_personas')) 
       
        self.intents.append(('say', 'utter_h1', ['vinet_cuenco'],'acc_del_belief','vinet_cuenco','acc_say', 'utter_h1','acc_say', 'utter_h2','acc_say', 'utter_h3',
                            'acc_say', 'utter_h4','acc_say', 'utter_h5','acc_say', 'utter_h6','acc_say', 'utter_h7', 'acc_new_belief','he_preguntado_si_no', 'acc_new_belief','utter_h7')) 
        self.intents.append(('say','utter_h8', ['utter_h7','he_preguntado_si_no','afirmar'],'acc_del_belief','he_preguntado_si_no', 'acc_del_belief','utter_h7',
                            'acc_say', 'utter_h8', 'acc_say', 'utter_h9', 'acc_new_belief','utter_h10'))
        self.intents.append(('say', 'utter_h10', ['utter_h7','he_preguntado_si_no','negar'],'acc_del_belief','he_preguntado_si_no','acc_del_belief','utter_h7', 'acc_new_belief','utter_h10'))
        self.intents.append(('say', 'utter_h10', ['utter_h10'],'acc_del_belief','utter_h10','acc_say', 'utter_h10','acc_say', 'utter_h11','acc_say', 'utter_h12'
                             ,'acc_say', 'utter_mostrar','acc_say', 'utter_h13','acc_say', 'utter_h14','acc_say', 'utter_mostrar','acc_say', 'utter_h15',
                             'acc_say', 'utter_h16','acc_say', 'utter_mostrar'))

    def filterI(self, Emotions, Beliefs, Desires):
        desires_fulfill = []
        intents_selected = [i for i in self.intents if i[1] in [d[1] for d in Desires]]
        #print('todas las intenciones coincidentes')
        #print(intents_selected)
        #print('---------------')
        for intent in intents_selected:
            if intents_manager.check(self, intent[2], Beliefs, Emotions):
                self.agent_intents.append(intent) 
                desires_fulfill.append(intent[1])
        for idx,ele in enumerate(Desires):
            if ele[1] in desires_fulfill:
                del Desires[idx]     
                
        print("el conj de intenciones es: " +  str(len(self.agent_intents)))
        # en el caso de varias intenciones hay que tomar la prioritaria
        if len(self.agent_intents) > 1:
            aux = 1
            for i in self.agent_intents:            
                if len(i[2])>=aux:
                    aux = len(i[2])
                    aux_intent = i
            self.agent_intents = []
            self.agent_intents.append(aux_intent)
                    
        #if(len(self.agent_intents)==0):
        #    print("la creencia sin nada es:" + Beliefs.belief_event)
        #    Beliefs.del_belief(Beliefs.belief_event)

        # dentro de las intenciones tomar el subconjunto que cumpla [1]
        # comprobar que se cumplen las condiciones
        # enviar las acciones

    def check(self, terms, Beliefs, Emotions):
        beliefs = [b[1] for b in Beliefs.agent_beliefs]
        #print('aqui')
        #print(terms)
        Belief_check = Beliefs.agent_beliefs
        for i in terms:
           if i not in beliefs:
                return False
           elif Belief_check[beliefs.index(i)][2] == False:
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

