##tag emocional segun XML
        #newscast-formal
        #newscast-casual
        #narration-professional
        #customerservice
        #chat
        #cheerful
        #empathetic
        ##sad
        ##calm
        ##angry
        ##fearful
        ##disgruntled
        ##serious
        ##affectionate
        ##gentle
        ##lyrical
## Bi intenciones
    #positivas
    #neutras
    #negativas

class emotions_manager(object):

    def __init__(self):
        self.agent_id = 'emotions_manager'        
        
        # Estado inicial de la emocion
        self.estado = 'happy'
        # Interes por el usuario
        self.interes = True
        self.intencionPositiva = ["saludar","agradecer","empatizar"]
        self.intencionNegativa = ["no_solicitar","atencion"]
        self.intencionNeutra = ["solicitar","ubicarme"]
       
        # personalidad basada en BigFive
        self.personality = {"openness":0.4, "conscientiousness":0.8, "extraversion":0.6, "agreeableness":0.3, "neuroticism":0.4}
        
        # estado de animo basado en PAD
        self.PAD = {"moodWord":'', "intensity":'', "pleasure":0, "arousal":0, "dominance":0}
        self.defaultMood()

        # emocion dominante basado en OCC
        self.emotions = []
        self.occEmotions()
        self.dominantEmotion = {"name":'Disliking', "value":0.46}
    
    #
    def defaultMood(self):        
        self.PAD['pleasure'] = 0.21 * self.personality['extraversion'] + 0.59 * self.personality['agreeableness'] + 0.19 * self.personality['neuroticism']
        self.PAD['arousal'] = 0.15 * self.personality['openness'] + 0.3 * self.personality['agreeableness'] - 0.57 * self.personality['neuroticism']
        self.PAD['dominance'] = 0.25 * self.personality['openness'] + 0.17 * self.personality['conscientiousness'] + 0.6 * self.personality['extraversion'] - 0.32 * self.personality['agreeableness']
        self.PAD['moodWord'] = self.moodOctans()
        self.PAD['intensity'] = 'slightly'
    
    #
    def moodOctans(self):
        if(self.PAD['pleasure']>=0):
            if(self.PAD['arousal']>=0):
                if(self.PAD['dominance']>=0):
                    return 'Exuberant'
                else:
                    return 'Dependent'
            else:
                if(self.PAD['dominance']>=0):
                    return 'Relaxed'
                else:
                    return 'Docile'
        else:
            if(self.PAD['arousal']>=0):
                if(self.PAD['dominance']>=0):
                    return 'Hostile'
                else:
                    return 'Anxious'
            else:
                if(self.PAD['dominance']>=0):
                    return 'Disdainful'
                else:
                    return 'Bored'
        return ''
    
    #
    def occEmotions(self):
        self.emotions.append(('Admiration', 0.5, 0.3, -0.2)) 
        self.emotions.append(('Anger', -0.51, 0.59, 0.25)) #
        self.emotions.append(('Disliking', -0.4, 0.2, 0.1)) 
        self.emotions.append(('Disappointment', -0.3, 0.1, -0.4)) 
        self.emotions.append(('Distress', -0.4, -0.2, -0.5)) 
        self.emotions.append(('Fear', -0.64, 0.6, -0.43)) #
        self.emotions.append(('FearsConfirmed', -0.5, -0.3, -0.7)) 
        self.emotions.append(('Gloating', 0.3, -0.3, -0.1)) 
        self.emotions.append(('Gratification', 0.6, 0.5, 0.4)) 
        self.emotions.append(('Gratitude', 0.4, 0.2, -0.3)) 
        self.emotions.append(('HappyFor', 0.4, 0.2, 0.2)) 
        self.emotions.append(('Hate', -0.6, 0.6, 0.3)) 
        self.emotions.append(('Hope', 0.2, 0.2 -0.1)) 
        self.emotions.append(('Joy', 0.4, 0.2, 0.1)) #
        self.emotions.append(('Liking', 0.4, 0.16, -0.24)) 
        self.emotions.append(('Love', 0.3, 0.1, 0.2)) 
        self.emotions.append(('Pity', -0.4, -0.2, -0.5)) #
        self.emotions.append(('Pride', 0.4, 0.3, 0.3)) 
        self.emotions.append(('Relief', 0.2, -0.3, 0.4)) 
        self.emotions.append(('Remorse', -0.3, 0.1, -0.6)) 
        self.emotions.append(('Reproach', -0.3, -0.1, 0.4))
        self.emotions.append(('Resentment', -0.2, -0.3, -0.2)) 
        self.emotions.append(('Satisfaction', 0.3, -0.2, 0.4)) 
        self.emotions.append(('Shame', -0.3, 0.1, -0.6))

# Define la emocion primaria
    def euf1(self, Intents, belief):     
        #belief[0]
        b = belief[1]
        self.estado = b[0]
        return self.estado

# Define la emocion secundaria tras pensarlo bien
    def euf2(self,Intents,Belief):
        return self.estado
    
#
    def happy():
        if (self.estado == 'happy'):
            return True
        return False

    def sad():
        if (self.estado == 'sad'):
            return True
        return False

    def fear():
        if (self.estado == 'fear'):
            return True
        return False

    def disgust():
        if (self.estado == 'disgust'):
            return True
        return False

    def anger():
        if (self.estado == 'anger'):
            return True
        return False

    def surprise():
        if (self.estado == 'surprise'):
            return True
        return False

    def neutral():
        if (self.estado == 'neutral'):
            return True
        return False

    def tag(self):
        if (self.estado == 'happy'):
            return "cheerful" 
        if (self.estado == 'empathetic'):
            return "empathetic"
        if (self.estado == 'sad'):
            return "sad"
        if (self.estado == 'neutral'):
            return "calm"
        if (self.estado == 'anger'):
            return "angry"
        if (self.estado == 'fear'):
            return "fearful"
        if (self.estado == 'disgust'):
            return "disgruntled"
        if (self.estado == 'serious'):
            return "serious"