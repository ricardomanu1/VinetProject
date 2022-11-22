
class desires_manager(object):

    def __init__(self):
        self.agent_id = 'desires_manager'

        # Estado inicial de las intenciones, en este caso vacio
        self.agent_desires = []

    def options(self, Beliefs, Intents):
        # tiene en cuenta las intenciones activas
        # tiene en cuenta las creencias         
        b = [i[2] for i in Intents.intents]    
        for belief in Beliefs.agent_beliefs: 
            # si ya existe esa intencion no se genera el deseo    
            if belief[2] == True: 
                if belief[1] not in Beliefs.emotionalBeliefs:
                    #print(belief) ## las emociones del usuario se tienen en cuenta como creencia? o solo emociones
                #else:
                    desires = [[item[0],item[1]] for item in Intents.intents if belief[1] in item[2]]
                    #desires = list(dict.fromkeys(desires))
                    for d in desires:
                        if (belief[0]==d[0]):                            
                            desire_tupla = (d[0], d[1], belief[1], self.agent_id)
                            self.agent_desires.append(desire_tupla)

                    #if not self.check_desire(belief, Intents.agent_intents):
                    #    desire_tupla = ('say', belief[0], belief[2], self.agent_id)
                    #    self.agent_desires.append(desire_tupla)
                    #    belief[1] = False

    def check_desire(self, belief, Intents):
        if not Intents:
            return False
        for intent in Intents:
            if belief[0] == intent[1]:
                return True
        return False

