
class belief_manager(object):

    def __init__(self):
        self.agent_id = 'belief_manager'
        # Estado inicial de las creencias, en este caso vacio
        self.agent_beliefs = []  
        self.belief_events = []  
        self.inter = False
        # Estado inicial de las emociones        
        self.agent_beliefs.append(['know','happy',True])
        self.emotionalBeliefs = ['isHappy','isSad','isFear','isAnger','isSurprise','isBored','isAnxious','isLonely','isTired']

    def get_belief_value(self, belief_name):
        for belief in agent_beliefs:
            if belief[0] == belief_name:
                return belief[1]        
        return False
# 
    def brf_in(self, Emotions, Intents, newBelief):
        self.belief_events.clear()
        # Saludar TRUE
        for b in newBelief:
            belief_name = b[1]
            # tiene en cuenta las intenciones activas
            # tiene en cuenta las emociones generadas
            # tiene en cuenta las nuevas creencias creadas
            if belief_name in [belief[1] for belief in self.agent_beliefs]:
                # ¿si existe? comprueba si es falso, y dependiendo del contexto lo pasa a verdadero
                # si es una emocion, pasa las otras a falso
                print('X-X-X-X- ya existe esa creencia -X-X-X-X')
            else:
                self.agent_beliefs.append(b)
                #print(" new creencia:" + b[1])
                self.belief_events.append(b)

    def EmotionInput_Update(self,user_emotion):
        emotions = [b[0] for b in self.agent_beliefs]
        if user_emotion[0] in emotions:
            for b in self.agent_beliefs:
                if b[0] == user_emotion[0]:
                    b[2] = True
                elif b[0] in self.emotionalBeliefs:
                    b[2] = False
        else:
            self.agent_beliefs.append(user_emotion)

# crea nuevos creencias a partir del tipo de evento pero no las añade
    def new_belief(self, event): 
        belief = []
        if event[0] == 'say':
            # intencion
            belief.append([event[0],event[1],True,event[3],event[4],event[6]]) 
            # emocion
            if event[2] != 'none':
                belief.append(['know',event[2],True,event[7]])
        elif event[0] == 'know':
            # intencion
            belief.append([event[0],event[1],True])            
            if event[2] is not None:
                print("nueva creencia:" + event[2])
                belief.append([event[0],event[2],True])
        return belief

    def del_belief(self, belief_name): 
        names = [a[1] for a in self.agent_beliefs]
        if belief_name in names:
            del self.agent_beliefs[names.index(belief_name)]

    def fulfill_belief(self, belief_name):
        for b in self.agent_beliefs:
            if b[1] == belief_name:
                b[2] = False

    def reset_beliefs(self):
        self.agent_beliefs = []  
        self.belief_events = []  
        self.inter = False

