# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 20:46:13 2018

@author: Alan Jerry Pan, CPA, CSC
@affiliation: Shanghai Jiaotong University

Program used for experimental study of information asymmetry in decision making (business), risk-taking behavior, and cognition.

Suggested citation as computer software for reference:
Pan, Alan J. (2018). Linear Dungeon [Computer software]. Github repository <https://github.com/alanjpan/Linear-Dungeon>

Futher expansions may include character development, equipment packs, and others, particularly financial literacy (finance) and purchasing decisions (marketing).

Note this software's license is GNU GPLv3.
"""

import random
import math
import sys

secure_random = random.SystemRandom()

low = [2, 3, 4, 5, 6, 7]
med = [4, 5, 6, 7, 8, 9, 10, 11]
high = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
boss = [10, 12, 13, 15, 17, 18, 19, 20, 22, 24, 25]

monster = ['skeleton', 'goblin', 'imp', 'donald', 'dog', 'cat', 'wizard', 'zombie', 'slime']
mattacks = ['claws', 'bites', 'tackles', 'punches', 'hits', 'mauls']
die = [1,2,3,4,5,6]
spellmulti = [.25, .5, 1, 1.5, 2]

plays = 0
dungeon = 25
steps = 0
collapse = 10

playerhp = 100
playerst = 15
playerma = 15
boots = 3
holywater = 2
gold = 10

def magic(spmulti, mag):
    return math.ceil(spmulti * mag)

#battle encounter
def battle(monster):
    global playerhp
    global playerst
    global playerma
    global gold
    
    while monster[2] > 0:
        #monster initiative
        monstermove = secure_random.choice(die)
        if monstermove <= 4:
            print('The monster ' + secure_random.choice(mattacks) + ' you!')
            playerhp -= monster[0]
        else:
            print('The monster casts a spell!')
            print('...')
            spmulti = secure_random.choice(spellmulti)
            sphit = magic(spmulti, monster[1])
            if spmulti == .25:
                print('You feel a jolt of pain.')
            if spmulti == 2:
                print('You are knocked back from the spell!')
            else:
                print('You are hit by the spell.')
            playerhp -= sphit

        if playerhp <= 0:
            gameover()
        
        #player turn
        print('You ready your sword and magic! What do you do? (attack, spell)')
        command = input()
        if command.lower().startswith('at'):
            print('You attack the monster.')
            monster[2] = monster[2] - playerst
        elif command.lower().startswith('sp'):
            spmulti = secure_random.choice(spellmulti)
            sphit = magic(spmulti, playerma)
            if spmulti == .25:
                print('Your spell shocks the monster.')
            elif spmulti == 2:
                print('You cast an inferno of spells.')
            else:
                print('You cast firebolt at the monster.')
            monster[2] = monster[2] - sphit
        else:
            print('A falling rock hits ye head!')

    print('The monster is slain! You pick up three gold pieces from its corpse.')
    gold += 3

#treasure encounter
def opentreasure():
    global boots
    global playerst
    global playerma
    global playerhp
    global gold
    
    roll = secure_random.choice(die) + secure_random.choice(die)
    if roll == 12:
        print('Your shoes get slimed!')
        boots += 1
    elif 9 <= roll <= 11:
        print('Your sword is sharpened!')
        playerst += 2
    elif 7 <= roll <= 9:
        print('You acquire a magical trinket!')
        playerma += 2
    elif roll == 6:
        print('You pick up 10 gold pieces!')
        gold += 10
    elif 2 <= roll <= 5:
        print('You pick up 5 gold pieces!')
        gold += 5
    elif roll == 1:
        print('The treasure chest was a trap! You feel sick.')
        playerhp -= 10
        
#monster encounter
def makeminion(st, ma, hp):
    global dungeon
    deepness = math.ceil(25 - dungeon)
    minion = [deepness + secure_random.choice(st), deepness + secure_random.choice(ma), deepness + secure_random.choice(hp) + (2 * plays)]
    return minion

#monster roll
def monsterroll(st, ma, hp):
    monster = makeminion(st, ma, hp)
    battle(monster)

#branch encounter
def encounter():
    global holywater
    
    roll = secure_random.choice(die)
    
    if roll == 1:
        print('You encounter a boss ' + secure_random.choice(monster) + '!!!')
        if holywater > 0:
            print('Do you throw holy water on it? (yes/no)')
            if input().lower().startswith('ye'):
                print('The boss monster dissolves into a puddle of water.')
                holywater -= 1
            else:
                monsterroll(high, med, boss)
        else:
            monsterroll(high, med, boss)
    elif roll == 2 or roll == 3:
        print('A ' + secure_random.choice(monster) + ' blocks your path!')
        if holywater > 0:
            print('Do you throw holy water on it? (yes/no)')
            if input().lower().startswith('ye'):
                print('The monster dissolves into a puddle of water.')
                holywater -= 1
            else:
                monsterroll(low, med, high)
        else:
            monsterroll(low, med, high)
    elif roll == 4:
        print('A ' + secure_random.choice(monster) + ' lands on top of you!')
        monsterroll(low, low, med)
    elif roll == 5:
        print('You find a treasure chest! Open? (yes/no)')
        if input().lower().startswith('ye'):
            opentreasure()
    elif roll == 6:
        print('You peacefully advance the dungeon.')

def ADVANCETHEDUNGEON():
    global dungeon
    global boots
    global steps
    global collapse
    
    while (collapse > 0) and (playerhp >= 0):
        if dungeon <= 0:
            escape()    
    
        print('\n~~~~~YOU HAVE ' + str(collapse) + ' TURNS REMAINING~~~~~\n')
        print('How many spaces dare ye advance? (0-' + str(boots) + ')?')
    
        ADVANCE = int(input())
        steps += ADVANCE
        
        if 0 <= ADVANCE <= boots:
            dungeon = dungeon - ADVANCE
            encounter()
        else:
            print('A falling rock hits ye head!')    
        collapse -= 1
    gameover()

def gameover():
    global gold
    
    print('\n_____YOU HAVE DIED_____\n')
    print('You amassed ' + str(gold) + ' gold pieces this session.')
    print('You have rushed ' + str(steps) + ' steps in the dungeon.')
    sys.exit

def escape():
    global plays
    
    print('\n\nvvvvv-YOU HAVE ESCAPED THE DUNGEON!-vvvvv\n')
    print('YOU ARE ' + str(gold) + ' GOLD PIECES RICH!\n')
    print('You have rushed ' + str(steps) + ' steps in the dungeon.')
    print('Re-enter the well? (yes/no)')
    if input().lower().startswith('ye'):
        plays += 1
        ENTERTHEDUNGEON()
    else:
        gameover()

def ENTERTHEDUNGEON():
    global playerhp
    global dungeon
    global collapse

    playerhp = 50

    dungeon = 25    
    collapse = 10

    ADVANCETHEDUNGEON()
    
print('\n\n|||~~~~~<LINEAR DUNGEON>~~~~~|||\n')
print('You, a misunfortunate adventurer, have fell into a well.\nYou see a tunnel but do not know where it leads.\nYou must escape before the well collapses.\nDare ye escape? (ye/no)')
if input().lower().startswith('ye'):
    ENTERTHEDUNGEON()
else:
    gameover()
    

