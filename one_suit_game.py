import numpy as np
import random
import itertools

class Game:

    def __init__(self,tricks,players):

        self.tricks = tricks
        self.num_players = len(players)
        self.players = players
        self.start = 0
    
    # Shuffle and distribute cards
    def shuffle(self):

        self.deck = list(np.arange(1,self.tricks*self.num_players+1))
        random.shuffle(self.deck)
        self.deck = [self.deck[i:i + self.tricks] for i in range(0, len(self.deck), self.tricks)]
        for i,player in zip(range(self.num_players),self.players):
            player.set_hand(self.deck[i])

    def play(self,preshuffled=[]):

        # Shuffle and distribute the cards
        if preshuffled == []:
            self.shuffle()
        else:
            for i,player in zip(range(self.num_players),self.players):
                player.set_hand(preshuffled[i])

        # Set tricks eating counter
        tricks_eaten = [0] * self.num_players

        # Play rounds
        while self.tricks > 0:
            plays = []
            plays.append(self.players[self.start].play_first()) # First player plays card
            for i in range(self.num_players - 1): # Every player plays a card
                if i != self.num_players - 2: # Respond normally if not last player
                    plays.append(self.players[(i + 1 + self.start) % self.num_players].respond(max(plays)))
                else: # Respond differently if last player
                    plays.append(self.players[(i + 1 + self.start) % self.num_players].respond(max(plays),last=True))
            self.start = (self.start + plays.index(max(plays))) % self.num_players # Find loser of the round
            tricks_eaten[self.start] += 1
            self.tricks -= 1

        return tricks_eaten
        
class Player:

    def __init__(self,number,strategy='default'):

        self.number = number
        self.hand = []
        self.strategy = strategy

    def set_hand(self,hand):

        self.hand = hand

    def play_first(self):

        if (self.strategy == 'default') or (self.strategy == 'lowest'):
            return self.play_lowest()
        elif self.strategy == 'random':
            return self.play_random()
        elif self.strategy == 'highest':
            return self.play_highest()
    
    # Used by first player in a round to play the lowest card in their hand
    def play_lowest(self):

        if len(self.hand) == 0:
            return
        lowest = min(self.hand)
        self.hand.remove(min(self.hand))
        return lowest
    
    # Play highest card in hand
    def play_highest(self):

        if len(self.hand) == 0:
            return
        highest = max(self.hand)
        self.hand.remove(max(self.hand))
        return highest
    
    def play_random(self):

        choice = random.choice(self.hand)
        self.hand.remove(choice)
        return choice
    
    # Choose a response according to initialised strategy
    def respond(self,highest,last=False):

        if self.strategy == 'default':
            return self.default_response(highest,last=last)
        elif self.strategy == 'random':
            return self.play_random()
        elif self.strategy == 'lowest':
            return self.play_lowest()
        elif self.strategy == 'highest':
            return self.play_highest()

    # Used by non-first players in a round to play a card depending on the highest card played and turn order
    def default_response(self,highest,last):

        lower_responses = [x for x in self.hand if x < highest] # Generate list of numbers lower than highest card
        if (len(lower_responses) == 0) & (last == False): # Play lowest card in hand
            lowest = min(self.hand)
            self.hand.remove(min(self.hand))
            return lowest
        elif (len(lower_responses) == 0) & (last == True): # Play highest card in hand
            highest = max(self.hand)
            self.hand.remove(max(self.hand))
            return highest
        else: # Play highest card from the list we generated above
            highest_of_low = max(lower_responses)
            self.hand.remove(max(lower_responses))
            return highest_of_low

def all_games_2p(tricks,prints=False):

    my_list = np.arange(0,2*tricks)
    combinations = list(itertools.combinations(my_list,tricks)) # Find all possible combinations
    iteration = []
    for i in combinations: # Split the combinations into two sets, one for each player
        iteration.append(([[j for j in i],list(set(my_list)-set([j for j in i]))]))

    # Initialise players
    player1 = Player(1)
    player2 = Player(2)

    # Initialise counters
    wins = 0
    losses = 0
    draws = 0

    # Iterate through each possible game, and record wins, draws and losses for Player1
    for iter in iteration:
        game = Game(tricks=tricks,players=[player1,player2])
        result = game.play(iter)

        if result[0] > result[1]:
            losses += 1
        elif result[0] < result[1]:
            wins += 1
        else:
            draws += 1

    if prints == True:
        print('Number of Cards per Player:',tricks)
        print('Total Games:',len(iteration))
        print('Wins:',wins,'('+str(round(wins/len(iteration)*100,2))+'%)')
        print('Draws:',draws,'('+str(round(draws/len(iteration)*100,2))+'%)')
        print('Losses:',losses,'('+str(round(losses/len(iteration)*100,2))+'%)')

    return wins,draws,losses,len(iteration)

def all_games_4p(tricks,prints=False):

    my_list = np.arange(0,4*tricks)
    combinations = list(itertools.combinations(my_list,tricks)) # Find all possible combinations
    iteration = []
    for i in combinations: # Split the combinations into four sets, one for each player
        my_list1 = list(set(my_list)-set([j for j in i]))
        combinations1 = list(itertools.combinations(my_list1,tricks))
        for i1 in combinations1:
            my_list2 = list(set(my_list1)-set([j for j in i1]))
            combinations2 = list(itertools.combinations(my_list2,tricks))
            for i2 in combinations2:
                iteration.append(([[j for j in i],[j for j in i1],[j for j in i2],list(set(my_list2)-set([j for j in i2]))]))

    # Initiaise players
    player1 = Player(1)
    player2 = Player(2)
    player3 = Player(3)
    player4 = Player(4)

    # Initialise counters
    player1_wins = 0
    player2_wins = 0
    player3_wins = 0
    player4_wins = 0

    # Iterate through each possible game, and record the wins per player
    for iter in iteration:
        game = Game(tricks=tricks,players=[player1,player2,player3,player4])
        result = game.play(iter)

        if result[0] == min(result):
            player1_wins += 1
        if result[1] == min(result):
            player2_wins += 1
        if result[2] == min(result):
            player3_wins += 1
        if result[3] == min(result):
            player4_wins += 1

    if prints == True:
        print('Number of Cards per Player:',tricks)
        print('Total Games:',len(iteration))
        print('Player 1 Wins:',player1_wins,'('+str(round(player1_wins/len(iteration)*100,2))+'%)')
        print('Player 2 Wins:',player2_wins,'('+str(round(player2_wins/len(iteration)*100,2))+'%)')
        print('Player 3 Wins:',player3_wins,'('+str(round(player3_wins/len(iteration)*100,2))+'%)')
        print('Player 4 Wins:',player4_wins,'('+str(round(player4_wins/len(iteration)*100,2))+'%)')

    return player1_wins,player2_wins,player3_wins,player4_wins,len(iteration)

def two_player_simulator(tricks,iterations):

    # Initialise players
    player1 = Player(1)
    player2 = Player(2)

    # Initialise counters
    wins = 0
    losses = 0
    draws = 0

    # Iterate through each possible game, and record wins, draws and losses for Player1
    for i in range(iterations):

        game = Game(tricks=tricks,players=[player1,player2])
        result = game.play()

        if result[0] > result[1]:
            losses += 1
        elif result[0] < result[1]:
            wins += 1
        else:
            draws += 1

    return wins/iterations,draws/iterations,losses/iterations

def four_player_simulator(tricks,iterations):

    # Initialise players
    player1 = Player(1)
    player2 = Player(2)
    player3 = Player(3)
    player4 = Player(4)

    # Initialise counters
    p1_wins = 0
    p2_wins = 0
    p3_wins = 0
    p4_wins = 0

    # Iterate through each possible game, and record wins, draws and losses for Player1
    for i in range(iterations):

        game = Game(tricks=tricks,players=[player1,player2,player3,player4])
        result = game.play()

        if result[0] == min(result):
            p1_wins += 1
        if result[1] == min(result):
            p2_wins += 1
        if result[2] == min(result):
            p3_wins += 1
        if result[3] == min(result):
            p4_wins += 1

    return p1_wins/iterations,p2_wins/iterations,p3_wins/iterations,p4_wins/iterations