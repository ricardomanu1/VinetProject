
class belief_manager(object):

    def __init__(self):
        self.agent_id = 'belief_manager'
        # Estado inicial de las creencias, en este caso vacio
        self.agent_beliefs = []  
        self.emotionalBeliefs = ['happy','sad','fear','disgust','anger','surprise','neutral']

    def get_belief_value(self, belief_name):
        for belief in agent_beliefs:
            if belief[0] == belief_name:
                return belief[1]        
        return False
# 
    def brf_in(self, Emotions, Intents, belief):
        belief_name = belief[0]
        # tiene en cuenta las intenciones activas
        
        #if belief_name[0] not in b:
        #    print("la creencia: " + belief_name[0] + "de intenciones es:" + str(b))
        # tiene en cuenta las emociones generadas
        # tiene en cuenta el evento de entrada         
        if not self.check_belief(belief_name[0]):
            self.agent_beliefs.append(belief[0])
        #belief_emotion = belief[1]
        if len(belief)==2:
            self.EmotionInput_Update(belief[1])

    def EmotionInput_Update(self,user_emotion):
        emotions = [b[0] for b in self.agent_beliefs]
        if user_emotion[0] in emotions:
            for b in self.agent_beliefs:
                if b[0] == user_emotion[0]:
                    b[1] = True
                elif b[0] in self.emotionalBeliefs:
                    b[1] = False
        else:
            self.agent_beliefs.append(user_emotion)

# crea nuevos creencias a partir del tipo de evento pero no las añade
    def new_belief(self, event): 
        belief = []
        if event[0] == 'say':
            # intencions
            belief.append([event[1],True,event[3],event[4],'spanish']) 
            # emotions
            if event[2] != 'none':
                belief.append([event[2],True,event[3]])
        return belief

    def del_belief(self, belief_name):               
        names = [a[0] for a in self.agent_beliefs]
        if belief_name in names:
            del self.agent_beliefs[names.index(belief_name)]

    def fulfill_belief(self, belief_name):
        for b in self.agent_beliefs:
            if b[0] == belief_name:
                b[1] = False
# Comprueba si ya existe esa creencia
    def check_belief(self, belief):
        beliefs_name = [b[0] for b in self.agent_beliefs] 
        if belief in beliefs_name:            
            return True
        else:
            return False
