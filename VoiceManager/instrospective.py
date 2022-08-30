import time
from interaction_manager import interaction_manager

Interaction = interaction_manager()

while True:    
    print("instrospectiva")
    #['isHappy','isSad','isFear','isAnger','isSurprise','isBored','isAnxious','isLonely','isTired']
    Interaction.know('sentiment','emotion','isSad')   
    time.sleep(2)