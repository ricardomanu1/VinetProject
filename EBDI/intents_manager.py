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
            #a_fB suceso que ha ocurrido y se mantiene
            #a_dB suceso/creencia que ha ocurrido y se elimina tras cumplirse
        ### PLANS ###
        ## Usuario se presenta
        self.intents.append(('say','utter_presentacion',['presentacion'],'a_dB','presentacion','a_say','utter_presentacion'))
        ## User:'me saluda'
        self.intents.append(('say','utter_saludar',['saludar','happy'],'a_say','utter_saludar','a_dB','saludar','a_nB','muestro_interes','a_nB','espero_respuesta'))

        self.intents.append(('say','utter_saludar',['saludar','sad'],'a_say','utter_saludar','a_dB','saludar'))
        self.intents.append(('say','utter_saludar',['saludar'],'a_say','utter_saludar','a_dB','saludar'))
        ## User:'quiere saber mi estado de ánimo'
        self.intents.append(('say','utter_estar_bien',['empatizar','happy'],'a_say','utter_estar_bien','a_dB','empatizar'))
        self.intents.append(('say','utter_estar_mal',['empatizar','sad'],'a_say','utter_estar_mal','a_dB','empatizar'))
        self.intents.append(('say','utter_estar_enfadado',['empatizar','anger'],'a_say','utter_estar_enfadado','a_dB','empatizar'))
        self.intents.append(('say','utter_estar_miedo',['empatizar','fear'],'a_say','utter_estar_miedo','a_dB','empatizar'))
        self.intents.append(('say','utter_estar_nervioso',['empatizar','anxious'],'a_say','utter_estar_nervioso','a_dB','empatizar'))
        self.intents.append(('say','utter_estar_aburrido',['empatizar','bored'],'a_say','utter_estar_aburrido','a_dB','empatizar'))
        self.intents.append(('say','utter_estar_emocionado',['empatizar','surprise'],'a_say','utter_estar_emocionado','a_dB','empatizar'))
        self.intents.append(('say','utter_estar_soledad',['empatizar','lonely'],'a_say','utter_estar_soledad','a_dB','empatizar'))
        self.intents.append(('say','utter_estar_cansado',['empatizar','tired'],'a_say','utter_estar_cansado','a_dB','empatizar'))
        ## User:'como crees que me siento?'
        self.intents.append(('say','utter_estado_bien',['analizame','isHappy'],'a_say','utter_estado_bien','a_dB','analizame'))
        self.intents.append(('say','utter_estado_mal',['analizame','isSad'],'a_say','utter_estado_mal','a_dB','analizame'))
        self.intents.append(('say','utter_estado_enfado',['analizame','isAnger'],'a_say','utter_estado_enfado','a_dB','analizame'))
        self.intents.append(('say','utter_estado_miedo',['analizame','isFear'],'a_say','utter_estado_miedo','a_dB','empatizar'))
        self.intents.append(('say','utter_estado_nerviosismo',['analizame','isAnxious'],'a_say','utter_estado_nerviosismo','a_dB','analizame'))
        self.intents.append(('say','utter_estado_aburrimiento',['analizame','isBored'],'a_say','utter_estado_aburrimiento','a_dB','analizame'))
        self.intents.append(('say','utter_estado_emocion',['analizame','isSurprise'],'a_say','utter_estado_emocion','a_dB','analizame'))
        self.intents.append(('say','utter_estado_soledad',['analizame','isLonely'],'a_say','utter_estado_soledad','a_dB','analizame'))
        self.intents.append(('say','utter_estado_cansancio',['analizame','isTired'],'a_say','utter_estado_cansancio','a_dB','analizame'))
        ## User:'me pregunta si estoy bien'
        self.intents.append(('say','utter_afirmar',['empatizar_bien','happy'],'a_say','utter_afirmar','a_dB','empatizar_bien'))
        self.intents.append(('say','utter_negar',['empatizar_bien','sad'],'a_say','utter_negar','a_dB','empatizar_bien'))
        ## User:'hace preguntas básicas'
        self.intents.append(('say','utter_responder_hora',['pregunta_hora'],'a_say','utter_responder_hora','a_dB','pregunta_hora'))
        self.intents.append(('say','utter_responder_dia',['pregunta_dia'],'a_say','utter_responder_dia','a_dB','pregunta_dia'))
        self.intents.append(('say','utter_preguntar_cuando',['preguntar_cuando'],'a_say','utter_preguntar_cuando','a_dB','preguntar_cuando'))
        self.intents.append(('say','utter_preguntar_por_que',['preguntar_por_que'],'a_say','utter_preguntar_por_que','a_dB','preguntar_por_que'))
        self.intents.append(('say','utter_preguntar_quien',['preguntar_quien'],'a_say','utter_preguntar_quien','a_dB','preguntar_quien'))
        self.intents.append(('say','utter_preguntar_donde',['preguntar_donde'],'a_say','utter_preguntar_donde','a_dB','preguntar_donde'))
        self.intents.append(('say','utter_preguntar_como',['preguntar_como'],'a_say', 'utter_preguntar_como','a_dB','preguntar_como'))
        self.intents.append(('say','utter_ubicarme',['ubicarme'],'a_say','utter_ubicarme','a_dB','ubicarme'))
        self.intents.append(('say','utter_identidad',['identidad'],'a_say','utter_identidad','a_fB','identidad'))
        ## User:'se despide'
        self.intents.append(('say','utter_despedir',['despedir'],'a_dB','saludar','a_dB','despedir','a_say','utter_despedir','ki','k_reiniciar','a_rB'))   ## funcion de reinicio

        ## User:'me agradece'
        self.intents.append(('say','utter_agradecer',['agradecer'],'a_say','utter_agradecer','a_fB','agradecer'))
        ## User:'me ha dicho como se siente'
        self.intents.append(('say','utter_empatizar_bien',['estado_bien'],'a_say','utter_empatizar_bien','a_dB','estado_bien'))
        self.intents.append(('say','utter_empatizar_mal',['estado_mal'],'a_say','utter_empatizar_mal','a_dB','estado_mal'))
        self.intents.append(('say','utter_empatizar_aburrimiento',['estado_aburrimiento'],'a_say','utter_empatizar_aburrimiento','a_dB','estado_aburrimiento'))
        self.intents.append(('say','utter_empatizar_cansancio',['estado_cansancio'],'a_say','utter_empatizar_cansancio','a_dB','estado_cansancio'))
        self.intents.append(('say','utter_empatizar_enfado',['estado_enfado'],'a_say','utter_empatizar_enfado','a_dB','estado_enfado'))
        self.intents.append(('say','utter_empatizar_miedo',['estado_miedo'],'a_say','utter_empatizar_miedo','a_dB','estado_miedo'))
        self.intents.append(('say','utter_empatizar_nerviosismo',['estado_nerviosismo'],'a_say','utter_empatizar_nerviosismo','a_dB','estado_nerviosismo'))
        self.intents.append(('say','utter_empatizar_soledad',['estado_soledad'],'a_say','utter_empatizar_soledad','a_dB','estado_soledad'))
        self.intents.append(('say','utter_empatizar_emocion',['estado_emocion'],'a_say','utter_empatizar_emocion','a_dB','estado_emocion'))

        ## YO muestro interes por el usuario
        self.intents.append(('say','utter_interes',['muestro_interes'],'a_dB','muestro_interes','a_say','utter_interes'))
        ## YO voy a empatizar con el estado de animo del usuario  
        self.intents.append(('say','utter_empatizar_bien',['espero_respuesta','estado_bien'],'a_dB','espero_respuesta','a_dB','estado_bien','a_say','utter_empatizar_bien','a_nB','le_pregunto'))
        self.intents.append(('say','utter_empatizar_mal',['espero_respuesta','estado_mal'],'a_dB','espero_respuesta','a_say', 'utter_empatizar_mal','a_nB','le_animo'))
        self.intents.append(('say','utter_empatizar_aburrimiento',['espero_respuesta','estado_aburrimiento'],'a_dB','espero_respuesta','a_say','utter_empatizar_aburrimiento'))
        ## YO intervengo en el estado de animo del usuario
        self.intents.append(('say','utter_animar',['le_animo'],'a_dB','le_animo','a_say','utter_animar','a_nB','he_preguntado_si_no','a_nB','utter_animar'))
        ## YO pregunto al usuario 
        self.intents.append(('say','utter_preguntar', ['le_pregunto'], 'a_say', 'utter_preguntar','a_fB','le_pregunto','a_nB','he_preguntado')) 
        self.intents.append(('say','utter_solicitar', ['utter_animar','he_preguntado_si_no', 'afirmar'],'a_dB','he_preguntado_si_no','a_dB','utter_animar', 'a_dB','afirmar','a_say', 'utter_solicitar','a_nB','he_solicitado')) 
        self.intents.append(('say','utter_solicitar', ['he_preguntado','solicitar'],'a_dB','he_preguntado','a_say', 'utter_solicitar', 'a_dB','solicitar','a_dB','le_pregunto','a_nB','he_solicitado'))  # llama a la accion buscar lo solicitado
        self.intents.append(('say','utter_solicitar', ['debes_especificar','solicitar'],'a_dB','debes_especificar','a_dB','solicitar', 'a_say', 'utter_solicitar','a_nB','he_solicitado'))
        self.intents.append(('say','utter_empatizar_mal', ['utter_animar','he_preguntado_si_no', 'negar'],'a_dB','he_preguntado_si_no','a_dB','utter_animar', 'a_dB','negar','a_say', 'utter_empatizar_mal')) 
        self.intents.append(('say','utter_pronombre_interrogativo', ['he_solicitado','afirmar'],'a_dB','he_solicitado','a_say', 'utter_pronombre_interrogativo', 'a_dB','afirmar'))  # llama a la accion buscar lo solicitado
        ## YO propongo temas
        self.intents.append(('say','utter_dar_opciones', ['he_solicitado','negar'],'a_dB','he_solicitado','a_say', 'utter_dar_opciones', 'a_dB','negar','a_say','utter_hitos_opciones'))  # llama a la accion buscar lo solicitado
        ## YO necesito mas informacion                
        self.intents.append(('say','utter_especificar', ['he_preguntado','afirmar'],'a_dB','he_preguntado', 'a_say', 'utter_especificar', 'a_dB','afirmar','a_nB','debes_especificar','a_dB','le_pregunto'))  # llama a la accion action_service_options 
        ## YO no continuo la conversacion
        self.intents.append(('say','utter_no_solicitar', ['he_preguntado','negar'],'a_dB','he_preguntado', 'a_say', 'utter_no_solicitar', 'a_dB','negar','a_nB','no_solicita','a_dB','le_pregunto'))  # llama a la accion action_service_options 
        self.intents.append(('say','utter_no_solicitar', ['he_preguntado','no_solicitar'],'a_dB','he_preguntado', 'a_say', 'utter_no_solicitar', 'a_dB','no_solicitar','a_nB','no_solicita','a_dB','le_pregunto'))  # llama a la accion action_service_options 
        ## YO soy

        self.intents.append(('say','utter_silencio', ['solicitar_silencio'],'a_dB','solicitar_silencio', 'a_say', 'utter_silencio'))


        ## Contexto VINET
        self.intents.append(('say','utter_hitos_opciones', ['dar_hitos_opciones'],'a_dB','dar_hitos_opciones','a_say', 'utter_hitos_opciones'))
        self.intents.append(('say','utter_hito', ['debes_especificar','solicitar_especifica_hito'],'a_dB','debes_especificar','a_dB','solicitar_especifica_hito', 'a_say', 'utter_hito'))               
        self.intents.append(('say','utter_hito', ['solicitar_especifica_hito'],'a_dB','solicitar_especifica_hito', 'a_say', 'utter_hito'))
           
        ## Comandos de Voz
        self.intents.append(('say','vinet_comando_apagar', ['vinet_comando_apagar'],'a_dB','vinet_comando_apagar','a_say','utter_vinet_comando_apagar'))
        self.intents.append(('say','vinet_comando_aprendizaje', ['vinet_comando_aprendizaje'],'a_dB','vinet_comando_aprendizaje','a_say','utter_vinet_comando_aprendizaje'))

        ## Conocimiento del entorno
        self.intents.append(('know', 'numero_personas', ['numero_personas'],'a_say', 'utter_conocer_personas','a_dB','numero_personas')) 

        #self.intents.append(('know', 'escoger_capitulo', ['escoger_capitulo'],'a_say', 'utter_hito_grupo','a_dB','escoger_capitulo')) 
        self.intents.append(('know', 'escoger_capitulo', ['escoger_capitulo'],'a_say', 'utter_interes_grupo','a_dB','escoger_capitulo', 'a_nB','v_interes_objeto')) 


        ## self.intents.append(('know', 'entra_grupo', ['entra_grupo'],'a_fB','entra_grupo','a_nB','saludar'))
        ## self.intents.append(('know', 'entra_grupo', ['entra_grupo'],'a_fB','entra_grupo','a_say','utter_bienvenida','a_say','utter_mirar','ki','k_observar'))
        self.intents.append(('know', 'entra_grupo', ['entra_grupo'],'a_fB','entra_grupo','a_say','utter_bienvenida','a_say','utter_identidad','a_say','utter_agradecimiento','a_nB', 'vinet_intro'))

        # INTRODUCCION
        self.intents.append(('say','utter_intro',['vinet_intro'],'a_dB','vinet_intro','a_say','utter_intro1','a_say','utter_intro2','a_say','utter_intro3','a_nB','saber_portus'))
        self.intents.append(('say','saber_portus',['saber_portus', 'vinet_portus_acierto'],'a_dB','saber_portus','a_dB','vinet_portus_acierto','a_say','utter_portus_ok','a_nB','vinet_intro4'))
        self.intents.append(('say','saber_portus',['saber_portus', 'vinet_portus_error'],'a_dB','saber_portus','a_dB','vinet_portus_error','a_say','utter_portus_fail','a_nB','vinet_intro4'))
        self.intents.append(('say','vinet_intro4',['vinet_intro4'],'a_dB','vinet_intro4','a_say','utter_intro4','a_say','utter_intro5'))

        self.intents.append(('say','vinet_guia',['vinet_guia'],'a_dB','vinet_guia','a_say','utter_intro_guia1','a_say','utter_intro_guia2','a_say','utter_intro_guia3','a_say','utter_intro_guia4',
                             'a_say','utter_intro_guia5','a_say','utter_intro_guia6','a_say','utter_intro_guia7','a_say','utter_intro_guia8','a_say','utter_intro_guia9','a_nB','vinet_seguir_intro'))

        self.intents.append(('say','vinet_seguir_intro', ['vinet_seguir_intro','afirmar'],'a_dB','vinet_seguir_intro','a_dB','afirmar','a_say','utter_intro6','a_say','utter_intro7', 'a_nB', 'saber_portus2'))  
        self.intents.append(('say','vinet_seguir_intro', ['vinet_seguir_intro','negar'],'a_dB','vinet_seguir_intro','a_dB','negar','a_say','utter_no_solicitar','a_say','utter_mirar','ki','k_observar'))
        
        self.intents.append(('say','saber_portus',['saber_portus2', 'vinet_portus_acierto2'],'a_dB','saber_portus2','a_dB','vinet_portus_acierto2','a_say','utter_portus2_ok','a_nB','vinet_intro8'))
        self.intents.append(('say','saber_portus',['saber_portus2', 'vinet_portus_error'],'a_dB','saber_portus2','a_dB','vinet_portus_error','a_say','utter_portus2_fail','a_nB','vinet_intro8'))

        self.intents.append(('say','vinet_intro8',['vinet_intro8'],'a_dB','vinet_intro8','a_say','utter_intro8','a_say','utter_intro9','a_say','utter_intro10','a_say','utter_intro11','a_say','utter_intro12',
                             'a_say','utter_intro13','a_say','utter_intro14','a_say','utter_intro15','a_say','utter_intro16','a_say','utter_intro17','a_say','utter_mirar','ki','k_observar'))
        
        self.intents.append(('know', 'sale_grupo', ['sale_grupo'],'a_dB','sale_grupo','a_dB','entra_grupo','a_nB','despedir'))
        #self.intents.append(('know', 'sale_grupo', ['sale_grupo','entra_grupo'],'a_dB','sale_grupo','a_dB','entra_grupo','a_nB','despedir'))
        self.intents.append(('know', 'pos_ojos', ['pos_ojos'],'a_dB','pos_ojos','a_nB','pos_ojos'))


        #self.intents.append(('know', 'isBored', ['isBored'],'a_dB','isBored'))
        
        
        self.intents.append(('say','utter_interes_objeto',['v_interes_objeto'],'a_dB','v_interes_objeto','a_say','utter_interes_objeto', 'a_nB', 'objeto_interesante'))

        self.intents.append(('say','objeto_interesante', ['objeto_interesante','afirmar','obj1'],'a_dB','objeto_interesante','a_dB','afirmar','a_dB','obj1', 'a_nB', 'vinet_lucerna'))  # llama a la accion action_service_options 
        self.intents.append(('say','objeto_interesante', ['objeto_interesante','negar','obj1'],'a_dB','objeto_interesante','a_dB','negar','a_dB','obj1', 'a_say', 'utter_especificacion','a_nB','elige_opcion'))  # llama a la accion action_service_options

        self.intents.append(('say','objeto_interesante', ['objeto_interesante','afirmar','obj2'],'a_dB','objeto_interesante','a_dB','afirmar','a_dB','obj2', 'a_nB', 'vinet_lacrimario'))  # llama a la accion action_service_options 
        self.intents.append(('say','objeto_interesante', ['objeto_interesante','negar','obj2'],'a_dB','objeto_interesante','a_dB','negar','a_dB','obj2', 'a_say', 'utter_especificacion','a_nB','elige_opcion'))  # llama a la accion action_service_options 
        
        self.intents.append(('say','objeto_interesante', ['objeto_interesante','afirmar','obj3'],'a_dB','objeto_interesante','a_dB','afirmar','a_dB','obj3', 'a_nB', 'vinet_cuenco'))  # llama a la accion action_service_options 
        self.intents.append(('say','objeto_interesante', ['objeto_interesante','negar','obj3'],'a_dB','objeto_interesante','a_dB','negar','a_dB','obj3', 'a_say', 'utter_especificacion','a_nB','elige_opcion'))  # llama a la accion action_service_options 
       
        self.intents.append(('say','objeto_interesante', ['objeto_interesante','afirmar','obj4'],'a_dB','objeto_interesante','a_dB','afirmar','a_dB','obj4', 'a_nB', 'vinet_ara'))  # llama a la accion action_service_options 
        self.intents.append(('say','objeto_interesante', ['objeto_interesante','negar','obj4'],'a_dB','objeto_interesante','a_dB','negar','a_dB','obj4', 'a_say', 'utter_especificacion','a_nB','elige_opcion'))  # llama a la accion action_service_options   
        
        self.intents.append(('say','elige_opcion', ['elige_opcion','afirmar'],'a_dB','elige_opcion','a_dB','afirmar','a_say', 'utter_especifica'))  # llama a la accion action_service_options
        self.intents.append(('say','elige_opcion', ['elige_opcion','negar'],'a_dB','elige_opcion','a_dB','negar','a_say', 'utter_no_solicitar','ki','k_observar'))  # llama a la accion action_service_options
        

     ## Cuenco de ceramica Hilo     
        self.intents.append(('say', 'utter_cue1', ['vinet_cuenco'],'a_dB','vinet_cuenco','a_say', 'utter_cue1','a_say', 'utter_cue2','a_say', 'utter_cue3', 'a_say', 'utter_cue4','a_say', 'utter_cue5','a_say', 'utter_cue6','a_say', 'utter_cue7', 'a_nB','he_preguntado_si_no', 'a_nB','cuenco_7')) 
            ## pregunta_cuenco (afirmar)
        self.intents.append(('say','utter_cue8', ['cuenco_7','he_preguntado_si_no','afirmar'],'a_dB','he_preguntado_si_no', 'a_dB','afirmar', 'a_dB','cuenco_7', 
                            'a_say', 'utter_cue8', 'a_say', 'utter_cue9', 'a_nB','cuenco_10'))
            ## pregunta_cuenco (negar)
        self.intents.append(('say', 'utter_cue10', ['cuenco_7','he_preguntado_si_no','negar'],'a_dB','he_preguntado_si_no','a_dB','negar','a_dB','cuenco_7', 'a_nB','cuenco_10'))
            ## Cierra_cuenco
        self.intents.append(('say','utter_cue10', ['cuenco_10'],'a_dB','cuenco_10', 'a_say', 'utter_cue10', 'a_say', 'utter_cue11', 'a_say', 'utter_cue12', 'a_say', 'utter_cue13','a_say', 'utter_cue14','a_say', 'utter_cue15','a_say', 'utter_cue16','a_nB','prof_cue1','ki','k_observar'))
           




     ## Lacrimario
        self.intents.append(('say', 'utter_lac1', ['vinet_lacrimario'],'a_dB','vinet_lacrimario','a_say','utter_lac1','a_say','utter_img', 'ki','k_observar'))

     ## Lucerna
        self.intents.append(('say', 'utter_luc1', ['vinet_lucerna'],'a_dB','vinet_lucerna','a_say','utter_luc1','a_say','utter_luc2','a_say','utter_luc3',
                             'a_say','utter_luc4','a_say','utter_luc5','a_nB','he_preguntado_si_no','a_nB','lucerna_5'))        
            ## pregunta_lucerna (afirmar)
        self.intents.append(('say','utter_luc5_s1', ['lucerna_5','he_preguntado_si_no','afirmar'],'a_dB','he_preguntado_si_no', 'a_dB','afirmar', 'a_dB','lucerna_5', 
                            'a_say', 'utter_luc5_s1', 'a_say', 'utter_luc5_s2',  'a_say', 'utter_luc5_s3','a_say', 'utter_luc5_s4','a_nB','lucerna_6'))
            ## pregunta_lucerna (negar)
        self.intents.append(('say','utter_luc5_n1', ['lucerna_5','he_preguntado_si_no','negar'],'a_dB','he_preguntado_si_no', 'a_dB','negar', 'a_dB','lucerna_5',
                            'a_say', 'utter_luc5_n1','a_nB','lucerna_6'))
            ## Cierra_lucerna
        self.intents.append(('say','utter_luc6', ['lucerna_6'],'a_dB','lucerna_6', 'a_say', 'utter_luc6', 'a_say', 'utter_luc7', 'a_say', 'utter_luc8', 'a_say', 'utter_luc9','a_nB','prof_luc1','ki','k_observar'))
            ## Lucerna profundidad 1
        self.intents.append(('say', 'utter_luc7_a1', ['vinet_lucerna','prof_luc1'],'a_dB','vinet_lucerna','a_dB','prof_luc1','a_say','utter_luc7_a1','a_say','utter_luc7_a2','a_say','utter_luc7_a3','a_nB','prof_luc_final','ki','k_observar'))
            ## Lucerna profundidad final
        self.intents.append(('say', 'sin_informacion', ['vinet_lucerna','prof_luc_final'],'a_dB','vinet_lucerna','a_say','utter_sin_informacion','a_say','utter_reiniciar_informacion', 'a_nB','reiniciar_informacion_luc'))
        self.intents.append(('say', 'reiniciar_informacion', ['reiniciar_informacion_luc','afirmar'],'a_dB','reiniciar_informacion','a_dB','afirmar','a_dB','prof_luc_final','a_say','utter_no_solicitar','ki','k_observar'))
        self.intents.append(('say', 'reiniciar_informacion', ['reiniciar_informacion_luc','negar'],'a_dB','reiniciar_informacion','a_dB','negar','a_say','utter_no_solicitar','ki','k_observar'))
        
     ## ara
        self.intents.append(('say', 'utter_ara1', ['vinet_ara'],'a_dB','vinet_ara','a_say', 'utter_ara1','ki','k_observar'))

        ## Emoción entrante
        #self.intents.append(('know', 'isHappy', ['isHappy'],'a_dB','isHappy'))
        #self.intents.append(('know', 'isSad', ['isSad'],'a_dB','isSad'))

        ## Reglas
        self.intents.append(('say', 'out_of_scope', ['out_of_scope'],'a_dB','out_of_scope','a_say', 'utter_out_of_scope'))
        ## Reglas
        self.intents.append(('know', 'nlu_fallback', ['nlu_fallback'],'a_dB','nlu_fallback','a_say', 'utter_please_rephrase'))
        
        self.intents.append(('say', 'a_narrar', ['a_narrar'],'a_dB','a_narrar','a_say', 'utter_a_narrar'))
        self.intents.append(('say', 'a_informar', ['a_informar'],'a_dB','a_informar','a_say', 'utter_a_informar'))
        self.intents.append(('say', 'a_saludar', ['a_saludar'],'a_dB','a_saludar','a_say', 'utter_a_saludar'))
        self.intents.append(('say', 'a_preguntar', ['a_preguntar'],'a_dB','a_preguntar','a_say', 'utter_a_preguntar'))
        self.intents.append(('say', 'a_despedir', ['a_despedir'],'a_dB','a_despedir','a_say', 'utter_a_despedir'))

        self.intents.append(('say', 'k_observa', ['k_observa'],'a_dB','k_observa','Kinect', 'k_observa'))

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
                
        print("El conjunto de intenciones es: " +  str(len(self.agent_intents)))
        # en el caso de varias intenciones hay que tomar la prioritaria
        if len(self.agent_intents) > 1:
            aux = 1
            for i in self.agent_intents:            
                if len(i[2])>=aux:
                    aux = len(i[2])
                    aux_intent = i
            self.agent_intents = []
            self.agent_intents.append(aux_intent)
                    
        if(len(self.agent_intents)==0 and Beliefs.inter):
            print("la creencia sin nada es:")
            for b in Beliefs.belief_events:       
                #print(" ",b[1])
                Beliefs.del_belief(b[1])
            Beliefs.belief_events.clear()

        # dentro de las intenciones tomar el subconjunto que cumpla [1]
        # comprobar que se cumplen las condiciones
        # enviar las acciones

    def check(self, terms, Beliefs, Emotions):
        beliefs = [b[1] for b in Beliefs.agent_beliefs]
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

