"""
Does this by checking the game's input buffering data and letting you know if the input is fast enough

A Note on Street Fighter 6 on PC:

WASD = Traditional movement, W is jump, S is crouch

J = Light Punch 
K = Medium Punch 
L = Heavy Punch 

U = Light Kick 
I = Mediun Kick 
O = Heavy Kick 
"""

from pynput import keyboard
import time

myInputs = []
myKeys = []

def manageLength():

    """
    Prevents memory overload - Clears the list of inputs if it is greater than 50 
    """

    global myInputs

    if len(myInputs) > 50:
        myInputs = myInputs[- 50:]

def onPress (inputKey):
    global myInputs
    global myKeys

    myInputs.append((inputKey, time.time()))
    myKeys.append(inputKey)

    print (f"Pressed: {inputKey}", end = " | ")
    print (f"{myInputs[myInputs.__len__() - 1][0]}", end = " | ")

    frames = round((myInputs[myInputs.__len__() - 1][1] - myInputs[myInputs.__len__() - 2][1]) * 60)
    print ("Frames: " + str(frames))

    """
    manageLength()
    """

def detectQuarterCircleAttack (direction1, direction2, light, medium, heavy, attackName):
    global myKeys
    global myInputs

    startIndexS = None

    for i in range(len(myInputs)):
        if str(myInputs[i][0]) == f"'{direction1}'":
            startIndexS = i
        
    startingTime = myInputs[startIndexS][1]
    remainingInputs = myInputs[startIndexS:]
    
    endingTime = None

    if len(myKeys) == 1:

        if str(myInputs[myInputs.__len__() - 3][0]) == f"'{direction1}'" and \
            str(myInputs[myInputs.__len__() - 2][0]) == f"'{direction2}'":
                
            for i in range(len(remainingInputs)):
                if str(remainingInputs[i][0]) in [f"'{light}'", f"'{medium}'", f"'{heavy}'"]:
                    endingTime = remainingInputs[i][1]
                
            if endingTime - startingTime <= 11 / 60:
                if str(myInputs[myInputs.__len__() - 1][0]) == f"'{light}'":
                    print(f"\033[30;43m Light {attackName}! \033[0m")
                
                elif str(myInputs[myInputs.__len__() - 1][0]) == f"'{medium}'":
                    print(f"\033[30;43m Medium {attackName}! \033[0m")
                
                elif str(myInputs[myInputs.__len__() - 1][0]) == f"'{heavy}'":
                    print(f"\033[30;43m Heavy {attackName}! \033[0m")


def detectZShapeAttacks(direction1, direction2, light, medium, heavy, attackName):
    global myKeys
    global myInputs

    startIndexS = None

    for i in range(len(myInputs)):
        if str(myInputs[i][0]) == f"'{direction1}'":
            startIndexS = i
        
    startingTime = myInputs[startIndexS][1]
    remainingInputs = myInputs[startIndexS:]
    
    endingTime = None

    if len(myKeys) > 1:

        """
        This section detects if you are pressing 3 or more buttons at once
        You do need to press 3 buttons at once at the end of the dragon punch command 
        The code below is failsafe - If it is a bad input, this code prevents an error from occuring
        A dragon punch is detected by the last 4 inputs 
        If you have less than that the computer might mistake it for something else 
        """

        if len(myInputs) >= 4:

            if str(myInputs[myInputs.__len__() - 4][0]) == f"'{direction1}'" and \
            str(myInputs[myInputs.__len__() - 3][0]) == f"'{direction2}'" and \
            str(myInputs[myInputs.__len__() - 2][0]) == f"'{direction1}'":
                
                for i in range(len(remainingInputs)):
                    if str(remainingInputs[i][0]) in [f"'{light}'", f"'{medium}'", f"'{heavy}'"]:
                        endingTime = remainingInputs[i][1]
                
                if endingTime - startingTime <= 11 / 60:
                    if str(myInputs[myInputs.__len__() - 1][0]) == f"'{light}'":
                        print(f"\033[30;43m Light {attackName}! \033[0m")
                
                    elif str(myInputs[myInputs.__len__() - 1][0]) == f"'{medium}'":
                        print(f"\033[30;43m Medium {attackName}! \033[0m")
                
                    elif str(myInputs[myInputs.__len__() - 1][0]) == f"'{heavy}'":
                        print(f"\033[30;43m Heavy {attackName}! \033[0m")

def onRelease (inputKey):
    global myKeys
    global myInputs

    print (f"Released: {inputKey}", end = " |")
    print (f"{myInputs[myInputs.__len__() - 1][0]}", end = " | ")

    """
    Detect input buffering for the attacks
    Input buffering for a fireball is 11 frames 
    After you press down, you have 11 frames for the rest of the attack 
    11 frames / (60 frames per second) ~ 0.183 seconds for the rest of the inputs

    Logic: 
    If you release the keys, remove them from the myKeys
    myKeys is a list of just keys, where as myInputs is a list of tuples
    Each tuple consists of an input and the time at which the input was given 

    When you release a key, the code removes the keys from myKeys
    If you only press one key at a time myKeys will continuously fill up and become empty again 
    If you press multiple keys at once, myKeys will store the SECOND key you held down 

    If the list myKeys is not empty, it looks at the last 6 inputs in myInputs to spot patterns 
    For reference, the inputs for special moves are as follows:

    Fireball: S -> S + D -> D + Punch 
    Dragon Punch: D -> S -> S + D + Punch 
    Hurricane Kick: S -> S + A -> A + Kick 

    """

    """
    This code is specifically for detecting hurricane kicks. There is 11 frames of input buffering 
    After pressing the first input, down, you have 11 frames for the rest of the inputs 
    """
    if str(inputKey) in ["'u'", "'i'", "'o'"]:

        detectQuarterCircleAttack("s", "a", "u", "i", "o", "214K")

        detectQuarterCircleAttack("s", "d", "u", "i", "o", "236K")

        detectZShapeAttacks("d", "s", "u", "i", "o", "623K")
    
    if str(inputKey) in ["'j'", "'k'", "'l'"]:

        detectQuarterCircleAttack("s", "d", "j", "k", "l", "236P")

        detectZShapeAttacks("d", "s", "j", "k", "l", "623P")

    myKeys.remove(inputKey)
    manageLength()

myListener = keyboard.Listener(on_press = onPress, on_release = onRelease)
myListener.start()
myListener.join()