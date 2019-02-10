# -*- coding: utf-8 -*-
'''
Racko-like game
'''

# Copyright Walter Bender 2019
# GPL 3

import os
import sys
from random import randrange


class Hand:
    hand = []

    def __init__(self):
        self.hand = []

    def show_hand(self):
        for i in range(len(self.hand)):
            print('%2d: %d' % (i * 5 + 5, self.hand[i]))

    def test_hand(self):
        for i in range(len(self.hand)):
            if i == 0:
                continue
            if self.hand[i] < self.hand[i - 1]:
                return False
        return True

    def place(self, n):
        discard = n
        i = int(n / 5.5)
        if i > 9:
            i = 9
        if abs(i * 5.5 + 5.5 - n) < abs(i * 5.5 + 5.5 - self.hand[i]):
            discard = self.hand[i]
            self.hand[i] = n
        return discard

    def replace(self, n, nn):
        for i in range(len(self.hand)):
            if self.hand[i] == n:
                self.hand[i] = nn
                return n
        return nn


class Deck:
    deck = []

    def __init__(self):
        if len(self.deck) == 0:
            for i in range(60):
                self.deck.append(i + 1)
        else:
            for i in range(60):
                self.deck[i] = i + 1
        self.shuffle()

    def shuffle(self):
        for i in range(60):
            self.swap(i, randrange(60))

    def swap(self, i, j):
        k = self.deck[i]
        self.deck[i] = self.deck[j]
        self.deck[j] = k

    def deal(self, hands):
        for hand in hands:
            for i in range(10):
                hand.hand.append(self.deck.pop())

    def draw(self):
        if len(self.deck) > 0:
            return self.deck.pop()
        return None

    def empty(self):
        if len(self.deck) == 0:
            return True
        return False


deck = Deck()
hand = Hand()
robot = Hand()
deck.deal([hand, robot])
discard = None

n = 0
while (not (hand.test_hand() or robot.test_hand())):
    hand.show_hand()
    if deck.empty():
        print('Sorry, but there are no more cards')
        break

    print("It's your turn.")
    if discard is None:
        discard = deck.draw()
        print('You drew %d.' % discard)

    print('Do you want to use %d?' % discard)
    move = input()
    if move == 'y' or move == 'yes':
        old_card = discard
        while old_card == discard:
            print('What card should we replace?')
            replace = int(input())
            old_card = hand.replace(replace, discard)
            if old_card == discard:
                print('Sorry, but I could not find %d in your hand.')
        discard = old_card
    elif n > 0:
        print("Let's draw a card.")
        discard = deck.draw()
        print('You drew %d. Do you want to use it?' % discard)
        move = input()
        if move == 'y' or move == 'yes':
            old_card = discard
            while old_card == discard:
                print('What card should we replace?')
                replace = int(input())
                old_card = hand.replace(replace, discard)
                if old_card == discard:
                    print('Sorry, but I could not find %d in your hand.')
            discard = old_card

    # Robot's turn
    print("It's the robot's turn.")
    old_card = robot.place(discard)
    if old_card == discard:
        print('The robot draws a card.')
        discard = deck.draw()
        discard = robot.place(discard)
        print('The robot discards %d,' % discard)
    else:
        print('The robot picked up %d from the pile.' % discard)
        discard = old_card
        print('The robot discards %d.' % discard)
    n += 1

if hand.test_hand():
    print('And we have a winner after %d moves.' % n)
    print('Your hand:')
    hand.show_hand()
    print("The robot's hand:")
    robot.show_hand()
elif robot.test_hand():
    print('The robot wins after %d moved.' % n)
    print('Your hand:')
    hand.show_hand()
    print("The robot's hand:")
    robot.show_hand()
else:
    print('Please try again.')
    print('Your hand:')
    hand.show_hand()
    print("The robot's hand:")
    robot.show_hand()
