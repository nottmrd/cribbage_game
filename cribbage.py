# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 09:35:25 2020

@author: peter
"""

import itertools
import random

#Creating the Card object
class Card(object):
    """
    suit = a string: either "Clubs", "Spades", "Diamonds"", or "Hearts"
    number = an integer representing the order of the cards, Ace being 1, King being 13.
    value = an integer representing the value of the card for addition purposes. Jack through King = 10.
    """
    def __init__(self, suit, number, value):
        self.suit = suit
        self.number = number
        self.value = value
    def getSuit(self):
        return self.suit
    def getNumber(self):
        return self.number
    def getValue(self):
        return self.value
    def __str__(self):
        if self.getNumber() == 1:
            return "<Ace of " + self.getSuit() + ">"
        elif self.getNumber() == 11:
            return "<Jack of " + self.getSuit() + ">"
        elif self.getNumber() == 12:
            return "<Queen of " + self.getSuit() + ">"     
        elif self.getNumber() == 13:
            return "<King of " + self.getSuit() + ">"     
        else:
            return "<" + str(self.getNumber()) + " of " + self.getSuit() + ">"
    def __repr__(self):
        return str(self.__str__())

#Creating a deck of 52 Cards
deck = []
for i in range(1,11):
    deck.append(Card("Diamonds",i,i))
    deck.append(Card("Clubs",i,i))
    deck.append(Card("Hearts",i,i))
    deck.append(Card("Spades",i,i))
for i in range(11,14):
    deck.append(Card("Diamonds", i, 10))
    deck.append(Card("Clubs", i, 10))
    deck.append(Card("Hearts", i, 10))
    deck.append(Card("Spades", i, 10))

#Creating the Player who can have a hand
class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
    def addScore(self, handscore):
        self.score += handscore
    def getScore(self):
        return self.score
    def addCards(self, cards):
        self.hand.append(cards)
    def removeCards(self, cards):
        self.hand.remove(cards)
    def getHand(self):
        return self.hand


#Helper function for choosing which player starts the game
def higherLower(deck):
    deck_copyforround = deck[:]
    print("Player 1 chooses a card....")
    card = random.choice(deck_copyforround)
    print("He picks: ", card)
    deck_copyforround.remove(card)
    print("Player 2 chooses a card....")
    card2 = random.choice(deck_copyforround)
    print("He picks: ", card2)
    if card.getNumber() <= card2.getNumber():
        print("Player 1's card is lower. He starts")
    else:
        print("Player 2's card is lower. He starts")
    return 1
    
    
#Creating a hand and turn-up card (non-duplicated cards)
        
    
def hand(deck, num_of_cards):
    deck_copyforround = deck[:]
    hand = []
    for i in range(num_of_cards):
        card = random.choice(deck_copyforround)
        hand.append(card)
        deck_copyforround.remove(card)
    turnup = [random.choice(deck_copyforround)]
    return hand, turnup

#Creating a function for determing a hand's score
def scoring(hand, turnup):
    """
    hand is a list of Cards
    turnup is also a list of one Card, the one that was turned up
    """
    #making it a 5 card hand with the turn-up card
    newHand = []
    for each in hand:
        newHand.append(each)
    if len(turnup) > 0:
        newHand += turnup
    #extracting the Number value out of the Card class for each Card
    newHand_Number = []
    for each in newHand:
        newHand_Number.append(each.getNumber())
    newHand_Number.sort()
    # print(newHand_Number)
    #score value to be added to and returned
    score = 0
    #pairs / triples / quadruples
    tracker = []
    quads = list(itertools.combinations(newHand_Number, 4))
    for each in quads:
        if each[0] == each[1] == each[2] == each[3]:
            score += 12
            tracker.append(each[0])
            break
    triples = list(itertools.combinations(newHand_Number, 3))
    for each in triples:
        if each[0] not in tracker:
            if each[0] == each[1] == each[2]:
                score += 6
                tracker.append(each[0])
                break
    pairs = list(itertools.combinations(newHand_Number, 2))
    for each in pairs:
        if each[0] not in tracker:
            if each[0] == each[1]:
                tracker.append(each[0])
                score += 2
    #runs
    three = list(itertools.permutations(newHand_Number, 3))
    four = list(itertools.permutations(newHand_Number, 4))
    five = list(itertools.permutations(newHand_Number, 5))
    def runs():
        for each in five:
            if each[4] == (each[3]+1) == (each[2]+2) == (each[1]+3) == (each[0]+4):
                return 5
        for each in four:
            if each[3] == (each[2]+1) == (each[1]+2) == (each[0]+3):
                return 4
        for each in three:
            if each[2] == (each[1]+1) == (each[0]+2):
                return 3
        return 0
    score += runs()
    #flush
    if hand[0].getSuit() == hand[1].getSuit() == hand[2].getSuit() == hand[3].getSuit():
        score += 4
        if len(newHand) > 4:
            if turnup[0].getSuit() == hand[0].getSuit():
                score += 1
    #jack suit
    if len(newHand) > 4:
        for each in hand:
            if each.getNumber() == 11:
                if each.getSuit() == turnup[0].getSuit():
                    score += 1
    #fifteens
    newHand_Value = []
    for each in newHand:
        newHand_Value.append(each.getValue())
    newHand_Value.sort()                
    quints = list(itertools.combinations(newHand_Value, 5))
    for each in quints:
        if sum(each) == 15:
            score += 2  
    quads = list(itertools.combinations(newHand_Value, 4))
    for each in quads:
        if sum(each) == 15:
            score += 2 
    triples = list(itertools.combinations(newHand_Value, 3))
    for each in triples:
        if sum(each) == 15:
            score += 2 
    pairs = list(itertools.combinations(newHand_Value, 2))
    for each in pairs:
        if sum(each) == 15:
            score += 2
    #DONE!            
    return score

h, t = hand(deck, 4)
print("Hand:", h)
print("Turnup:", t)
print("Hand score: ", scoring(h, t))
    
# def pegging_scoring(pile):
#     """
#     Parameters
#     ----------
#     pile : a list of Cards, but it will be an empty list
#         DESCRIPTION:
#             an

#     Returns
#     -------
#     None.

#     """
#     score = 0
#     #switch for counting runs, e.g. so i don't count a 5 card run... and then also a 4 card run
#     run = False
#     if len(pile) == 0 or len(pile) == 1:
#         return score
#     if len(pile) == 2:
#         if pile[-1].getValue() + pile[-2].getValue() == 15:
#             score += 2
#         if pile[-1].getNumber() == pile[-2].getNumber():
#             score += 2
#         return score
#     if len(pile) == 3:
#         if pile[-1].getValue() + pile[-2].getValue() + pile[-3].getValue() == 15:
#             score += 2
#         if pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber():
#             score += 6
#         elif pile[-1].getNumber() == pile[-2].getNumber():
#             score += 2
#         three = list(itertools.permutations(pile, 3))
#         for each in three:
#             if each[2] == (each[1]+1) == (each[0]+2):
#                 score += 3
#         return score
#     if len(pile) == 4:
#         #15
#         if pile[-1].getValue() + pile[-2].getValue() + pile[-3].getValue() + pile[-4].getValue() == 15:
#             score += 2
#         #4 of a kind
#         if pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber() == pile[-4].getNumber():
#             score += 12
#         #3 of a kind
#         elif pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber():
#             score += 6
#         #2 of a kind
#         elif pile[-1].getNumber() == pile[-2].getNumber():
#             score += 2
#         #run of four
#         four = list(itertools.permutations(pile, 4))
#         for each in four:
#             if each[3] == (each[2]+1) == (each[1]+2) == (each[0]+3):
#                 score += 4
#                 run = True
#         #run of three
#         if run == False:
#             three = list(itertools.permutations(pile[1:4], 3))
#             for each in three:
#                 if each[2] == (each[1]+1) == (each[0]+2):
#                     score += 3
#         return score
#     if len(pile) == 5:
#         #15
#         if pile[-1].getValue() + pile[-2].getValue() + pile[-3].getValue() + pile[-4].getValue() + pile[-5].getValue() == 15:
#             score += 2
#         #4 of a kind
#         if pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber() == pile[-4].getNumber():
#             score += 12
#         #3 of a kind
#         elif pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber():
#             score += 6
#         #2 of a kind
#         elif pile[-1].getNumber() == pile[-2].getNumber():
#             score += 2
#         #run of five
#         five = list(itertools.permutations(pile, 5))     
#         for each in five:
#             if each[4] == (each[3]+1) == (each[2]+2) == (each[1]+3) == (each[0]+4):
#                 score += 5
#                 run = True
#         #run of four
#         if run == False:
#             four = list(itertools.permutations(pile[1:5], 4))
#             for each in four:
#                 if each[3] == (each[2]+1) == (each[1]+2) == (each[0]+3):
#                     score += 4
#                     run = True
#         #run of three
#         if run == False:
#             three = list(itertools.permutations(pile[2:5], 3))
#             for each in three:
#                 if each[2] == (each[1]+1) == (each[0]+2):
#                     score += 3
#             return score
#     if len(pile) == 6:
#         #15
#         if pile[-1].getValue() + pile[-2].getValue() + pile[-3].getValue() + pile[-4].getValue() + pile[-5].getValue() + pile[-6].getValue() == 15:
#             score += 2
#         #4 of a kind
#         if pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber() == pile[-4].getNumber():
#             score += 12
#         #3 of a kind
#         elif pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber():
#             score += 6
#         #2 of a kind
#         elif pile[-1].getNumber() == pile[-2].getNumber():
#             score += 2
#         #run of six
#         six = list(itertools.permutations(pile, 6))
#         for each in six:
#             if each[5] == (each[4]+1) == (each[3]+2) == (each[2]+3) == (each[1]+4) == (each[0]+5):
#                 score += 5
#                 run = True  
#         #run of five
#         if run == False:
#             five = list(itertools.permutations(pile, 5))     
#             for each in five:
#                 if each[4] == (each[3]+1) == (each[2]+2) == (each[1]+3) == (each[0]+4):
#                     score += 5
#                     run = True
#         #run of four
#         if run == False:
#             four = list(itertools.permutations(pile[1:5], 4))
#             for each in four:
#                 if each[3] == (each[2]+1) == (each[1]+2) == (each[0]+3):
#                     score += 4
#                     run = True
#         #run of three
#         if run == False:
#             three = list(itertools.permutations(pile[2:5], 3))
#             for each in three:
#                 if each[2] == (each[1]+1) == (each[0]+2):
#                     score += 3
#             return score


# def cribbage():
#     print("This is a 1 player game vs the computer")
    
    
    
    
    
a = [Card("",3,3),Card("",2,2),Card("", 4,4),Card("",7,7,),Card("",8,8),Card("",5,5)]

def pegging_scoring(pile):  
    def peg_fifteen(pile):
        pileVal = []
        for each in pile:
            pileVal.append(each.getValue())
        if sum(pileVal) == 15:
            return 2
        else:
            return 0 
    def peg_ofakind(pile):
        score = 0
        try:
            if pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber() == pile[-4].getNumber():
                score += 12
        except IndexError:
            try:
                if pile[-1].getNumber() == pile[-2].getNumber() == pile[-3].getNumber():
                    score += 6
            except IndexError:
                try:
                    if pile[-1].getNumber() == pile[-2].getNumber():
                        score += 2
                except IndexError:
                    score += 0
        return score
    def peg_run(pile):
        score = 0
        pileNum = []
        for each in pile:
            pileNum.append(each.getValue())
        if len(pileNum) < 3:
            return score
        else:
            run = list(itertools.permutations(pileNum[-3:], 3))
            for each in run:
                if each[-1] == each[-2]+1 == each[-3]+2:
                    score = 3
            run = list(itertools.permutations(pileNum[-4:], 4))
            if len(run) > 0:
                for each in run:
                    if each[-1] == each[-2]+1 == each[-3]+2 == each[-4]+3:
                        score = 4
                run = list(itertools.permutations(pileNum[-5:], 5))
                if len(run) > 0:
                    for each in run:
                        if each[-1] == each[-2]+1 == each[-3]+2 == each[-4]+3 == each[-5]+4:
                            score = 5
                    run = list(itertools.permutations(pileNum[-6:], 6))
                    if len(run) > 0:
                        for each in run:
                            if each[-1] == each[-2]+1 == each[-3]+2 == each[-4]+3 == each[-5]+4 == each[-6]+5:
                                score = 6
                        run = list(itertools.permutations(pileNum[-7:], 7))
                        if len(run) > 0:
                            for each in run:
                                if each[-1] == each[-2]+1 == each[-3]+2 == each[-4]+3 == each[-5]+4 == each[-6]+5 == each[-7]+6:
                                    score = 7
                            run = list(itertools.permutations(pileNum[-8:], 8))
                            if len(run) > 0:
                                for each in run:
                                    if each[-1] == each[-2]+1 == each[-3]+2 == each[-4]+3 == each[-5]+4 == each[-6]+5 == each[-7]+6 == each[-8]+7:
                                        score = 8
                            else:
                                return score
                        else:
                            return score
                    else:
                        return score
                else:
                    return score
            else:
                return score
    return peg_fifteen(pile) + peg_ofakind(pile) + peg_run(pile)

def choosing_simplebesthand(hand):
    """hand = a list of 6 Cards, of which the best statistcal 4 will be chosen in terms of highest avg points scored
    This will return the best 4 card hand from those 6 cards. However, it does not take into account the random turnup.
    So not TRUELY the best hand."""
    combos = list(itertools.combinations(hand, 4))
    best = []
    best_score = 0
    for each in combos:
        calc_score = scoring(each, [])
        if calc_score > best_score:
            best = each
            best_score = calc_score
    return best



print("Best 4 card hand: ", choosing_simplebesthand(a))
    
print(a)
print("Pegging score:", pegging_scoring(a))
higherLower(deck)