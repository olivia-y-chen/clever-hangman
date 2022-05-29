"""
Created on 11/17/2021

@author: Olivia Chen
"""

import random


def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the
    corresponding number of misses allowed for the game.
    '''
    print("How many misses do you want? Hard has 8 and Easy has 12.")
    diff = input("(h)ard or (e)asy> ")
    if diff == "h":
        print("you have 8 misses to guess word")
        return 8
    else:
        print("you have 12 misses to guess word")
        return 12
    pass




def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    lettersGuessed.sort()
    alphlst = ["a", "b", "c", "d", 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for i in range(0, len(alphlst)):
        if alphlst[i] in lettersGuessed:
            alphlst[i] = " "
    letterStr = "".join(alphlst)
    wordStr = " ".join(list(hangmanWord))
    dsply = "letters not yet guessed: " + letterStr + "\nmisses remaining = " + str(missesLeft) + "\n" + wordStr
    return dsply
    pass




def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    print(displayString)
    letter = input("letter> ")
    while letter in lettersGuessed:
        print("you already guessed that")
        letter = input("letter> ")
    else:
        return letter
    pass



def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    Will ask if the user wants to debug, thus prompting a debug version of the game
    '''
    f = open(filename)
    f = [w.strip() for w in f.read().split()]
    deb = handleUserInputDebugMode()
    print(deb)
    wlst = []
    length = handleUserInputWordLength()
    miss = handleUserInputDifficulty()
    for w in f:
        if len(w) == int(length):
            wlst.append(w)
    hng = '_'* int(length)
    n = 0
    guessed = []
    rounds = 0
    while n < miss and '_' in hng:
        if deb:
            print("(word is " + wlst[0] + ")")
        m = handleUserInputLetterGuess(guessed, createDisplayString(guessed, miss - n, hng))
        guessed.append(m)
        guessed.sort()
        qn = getNewWordList(hng, m, wlst, deb)
        wlst = qn[1]
        update = processUserGuessClever(m, wlst, miss-n)
        if update[1] == False:
            print("you missed: " + m + " not in word")
            tn= getNewWordList(hng, m, wlst, deb)
            wlst = tn[1]
            n += 1
        elif update[1] == True:
            wn= getNewWordList(hng, m, wlst, deb)
            wlst = wn[1]
            hng = wn[0]
        rounds += 1
    else:
        if '_' not in hng:
            print("you guessed the word: " + hng)
        else:
            print("you're hung!!" + "\n word is " + wlst[random.randint(0, len(wlst))])
    print("you made " + str(rounds) + " guesses with " + str(n) + " misses")
    return '_' not in hng
    pass


def handleUserInputDebugMode():
    """Asks the user whether they want to play on debug mode or normal mode and returns True if they want debug mode"""
    print("Which mode do you want: ")
    diff = input("(d)ebug or (p)lay: ")
    return diff == 'd'


def handleUserInputWordLength():
    """Asks the user how long they want their word to be and returns that number"""
    num = input("How many letters in the word you'll guess: ")
    return int(num)


def createTemplate(currTemplate, letterGuess, word):
    """Converts current template if letter is guessed correctly, else returns the current template"""
    if letterGuess in word:
        new = list(currTemplate)
        charlst = list(word)
        for i in range(0, len(charlst)):
            if letterGuess == charlst[i]:
                new[i] = letterGuess
        return "".join(new)
    else:
        return currTemplate


def getNewWordList(currTemplate, letterGuess, wordList, debug):
    """Runs through all possible templates, and which ever template has the most words that match it,
    that template would be the word the game would continue on. If on debug mode, prints  possible
    number of words, each template with the number of words to it, and the number of keys that exist.
    Returns the template with the largest list, along with the list of words."""
    diction = {}
    debdict = {}
    for word in wordList:
        newtemp = createTemplate(currTemplate, letterGuess, word)
        if newtemp not in diction:
            diction[newtemp] = [word]
        elif newtemp in diction:
            diction[newtemp].append(word)
    diction = dict(sorted(diction.items(), key=lambda x:x[0].count("_"), reverse=True))
    maxkey = max(diction, key=lambda x: len(set(diction[x])))
    if debug == True:
        for k, v in diction.items():
            debdict[k] = len(v)
        print("# possible words:", len(diction[maxkey]))
        debdict = sorted(debdict.items())
        for k, v in debdict:
            print(k, ":", v)
        print("# keys =", len(debdict))
    return maxkey, diction[maxkey]


def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    w = hangmanWord[0]
    #print(count, len(hangmanWord), count==len(hangmanWord))
    if guessedLetter in w:
        return [missesLeft, True]
    else:
        missesLeft -= 1
        return[missesLeft, False]


if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    recordW = 0
    recordL = 0
    first = runGame('lowerwords.txt')
    if first == True:
        recordW += 1
    else:
        recordL += 1
    n = input("Do you want to play again? y or n> ")
    while n == "y":
        t = runGame('lowerwords.txt')
        if t == True:
            recordW += 1
        else:
            recordL += 1
        n = input("Do you want to play again? y or n> ")
    else:
        print("You won " + str(recordW) + " game(s) and lost " + str(recordL))
