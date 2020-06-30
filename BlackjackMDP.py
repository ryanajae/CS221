import util, math, random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    # Return a value of any type capturing the start state of the MDP.
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0
        # END_YOUR_CODE

    # Return a list of strings representing actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        if state == -1:
            return [-2, 0]
        elif state == 0:
            return [-1, 1]
        elif state == 1:
            return [0, 2]
        elif state == -2:
            return [-2]
        else:
            return [2]
        # END_YOUR_CODE

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # Remember that if |state| is an end state, you should return an empty list [].
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        tuples = []
        prob = 0
        reward = 0
        if state == -1 and action == -2:
            prob = 0.25
            reward = 20
        elif state == -1 and action == 0:
            prob = 0.75
            reward = -5
        elif state == 0 and action == -1:
            prob = 0.25
            reward = -5
        elif state == 0 and action == 1:
            prob = 0.75
            reward = -5
        elif state == 1 and action == 0:
            prob = 0.25
            reward = -5
        elif state == 1 and action == 2:
            prob = 0.75
            reward = 100
        constructTuple = (action, prob, reward)
        tuples.append(constructTuple)
        return tuples
        # END_YOUR_CODE

    # Set the discount factor (float or integer) for your counterexample MDP.
    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 1
        # END_YOUR_CODE

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: list of integers (face values for each card included in the deck)
        multiplicity: single integer representing the number of cards with each face value
        threshold: maximum number of points (i.e. sum of card values in hand) before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look closely at this function to see an example of state representation for our Blackjack game.
    # Each state is a tuple with 3 elements:
    #   -- The first element of the tuple is the sum of the cards in the player's hand.
    #   -- If the player's last action was to peek, the second element is the index
    #      (not the face value) of the next card that will be drawn; otherwise, the
    #      second element is None.
    #   -- The third element is a tuple giving counts for each of the cards remaining
    #      in the deck, or None if the deck is empty or the game is over (e.g. when
    #      the user quits or goes bust).
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be placed into the succAndProbReward function below.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        def checkDeck(deck):
            returnBool = True
            for card in deck:
                if card == 0:
                    returnBool = False
                else:
                    returnBool = True
            return returnBool
        if state[2] == None:
            return []
        tuplesList = []
        if action == 'Take':
            if state[1] != None: #Peeked deterministically take
                deck = list(state[2])
                total = state[0] + self.cardValues[state[1]]
                deck[state[1]] -= 1
                if checkDeck(deck) == False or total > self.threshold:
                    deck = None
                else:
                    deck = tuple(deck)
                newState = (total, None, deck)
                appendTuple = (newState, 1, 0)
                tuplesList.append(appendTuple)
            else: #We need all possibilities
                idx = 0
                allTake = []
                if state[2] != None:
                    for card in state[2]:
                        total = state[0]
                        deck = list(state[2])
                        if card!= 0:
                            total += self.cardValues[idx]
                            deck[idx] -= 1
                            if checkDeck(deck) == False or total > self.threshold:
                                deck = None
                            else:
                                deck = tuple(deck)
                            newState = (total, None, deck)
                            allTake.append(newState)
                        idx += 1
                    prob = float(1) / float(len(allTake))
                    reward = 0
                    for newTake in allTake:
                        if newTake[2] == None:
                            reward = newTake[0]
                        if newTake[0] > self.threshold:
                            reward = 0
                        appendTuple = (newTake, prob, reward)
                        tuplesList.append(appendTuple)
                        reward = 0
                else:
                    action = 'Quit' #Deck ran out so treat as quit
        elif action == 'Peek':
            deck = state[2]
            if state[1] != None:
                return []
            else:
                idx = 0
                allPeek = []
                if deck != None:
                    for card in deck:
                        if card != 0:
                            newState = (state[0], idx, state[2])
                            allPeek.append(newState)
                        idx += 1
                    prob = float(1) / float(len(allPeek))
                    for newPeek in allPeek:
                        appendTuple = (newPeek, prob, -self.peekCost)
                        tuplesList.append(appendTuple)
                else:
                    action = 'Quit'
        elif action == 'Quit':
            quitState = (state[0], None, None)
            appendQuit = (quitState, 1, state[0])
            tuplesList.append(appendQuit)
        return tuplesList
        # END_YOUR_CODE
    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action at least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    # return BlackjackMDP(cardValues=[0, 2, 3, 4, 5, 17, 18.5, 19, 20, 21], multiplicity=2,
    #                                threshold=20, peekCost=1)
    return BlackjackMDP(cardValues=[1, 2, 3, 8, 20], multiplicity=4,
                                   threshold=20, peekCost=1)
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        stepSZ = self.getStepSize()
        vOpt = 0
        for actionN in self.actions(newState):
            curQ = self.getQ(newState, actionN)
            if curQ > vOpt: vOpt = curQ 
        newQ = (1 - stepSZ)*self.getQ(state, action) + stepSZ*(reward + self.discount*vOpt)
        f = (state, action)
        self.weights[f] = newQ
        # END_YOUR_CODE

# Return a single-element list containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

def simulate_QL_over_MDP(mdp, featureExtractor):
    # NOTE: adding more code to this function is totally optional, but it will probably be useful
    # to you as you work to answer question 4b (a written question on this assignment).  We suggest
    # that you add a few lines of code here to run value iteration, simulate Q-learning on the MDP,
    # and then print some stats comparing the policies learned by these two approaches.
    # BEGIN_YOUR_CODE
    listSmall = util.simulate(smallMDP, QLearningAlgorithm, 30000)
    print listSmall
    # END_YOUR_CODE


############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs.
# (See identityFeatureExtractor() above for a simple example.)
# Include the following features in the list you return:
# -- Indicator for the action and the current total (1 feature).
# -- Indicator for the action and the presence/absence of each face value in the deck.
#       Example: if the deck is (3, 4, 0, 2), then your indicator on the presence of each card is (1, 1, 0, 1)
#       Note: only add this feature if the deck is not None.
# -- Indicators for the action and the number of cards remaining with each face value (len(counts) features).
#       Note: only add these features if the deck is not None.
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state

    # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
    extractionList = []
    featureKeyOne = (action, total)
    featureKeyVal = 1
    if total == None or total == 0:
        featureKeyVal = 0
    featureOne = (featureKeyOne, featureKeyVal)
    extractionList.append(featureOne)
    if counts != None:
        featureKeyTwo = (action, counts)
        featureKeyThree = (action, counts)
        featureTwoValList = []
        featureThreeValList = []
        for card in counts:
            if card == 0:
                featureTwoValList.append(0)
            else:
                featureTwoValList.append(1)
            featureThreeValList.append(card)
        featureTwo = (featureKeyTwo, tuple(featureTwoValList))
        extractionList.append(featureTwo)
        newCounts = tuple(featureThreeValList)
        countI = (newCounts, 1)
        cardIndicator = 1
        if nextCard == None:
            cardIndicator = 0
        cardI = (card, cardIndicator)
        actionI = (action, 1)
        tripleVal = (cardI, countsI, actionI)
        featureThree = (featureKeyThree, tripleVal)
        extractionList.append(featureThree)
    return extractionList
    # END_YOUR_CODE
