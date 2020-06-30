import collections
import math
import numpy as np

############################################################
# Problem 3a

def findAlphabeticallyLastWord(text):
    """
    Given a string |text|, return the word in |text| that comes last
    alphabetically (that is, the word that would appear last in a dictionary).
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    words = text.split()
    words.sort()
    return words[len(words) - 1]
    # END_YOUR_CODE

############################################################
# Problem 3b

def euclideanDistance(loc1, loc2):
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    a = np.array(loc1)
    b = np.array(loc2)
    return np.linalg.norm(a-b)
    # END_YOUR_CODE

############################################################
# Problem 3c

def mutateSentences(sentence):
    """
    Given a sentence (sequence of words), return a list of all "similar"
    sentences.
    We define a sentence to be similar to the original sentence if
      - it as the same number of words, and
      - each pair of adjacent words in the new sentence also occurs in the original sentence
        (the words within each pair should appear in the same order in the output sentence
         as they did in the orignal sentence.)
    Notes:
      - The order of the sentences you output doesn't matter.
      - You must not output duplicates.
      - Your generated sentence can use a word in the original sentence more than
        once.
    Example:
      - Input: 'the cat and the mouse'
      - Output: ['and the cat and the', 'the cat and the mouse', 'the cat and the cat', 'cat and the cat and']
                (reordered versions of this list are allowed)
    """
    # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
    words = sentence.split()
    sentences = []
    #Create pairs with key a word in sentence and value following adjacent word in sentence
    pairs = []
    pairDict = dict()
    print words
    # pairDict.get(key, [])
    # for k, v in pairDict.items():
    #     k, v
    for i in xrange(len(words) - 1):
        if i == len(words) - 1:
            pairDict.setdefault(words[len(words) - 1], []).append(words[i])
        else:
            pairDict.setdefault(words[i], []).append(words[i+1])
    print pairDict
    prevValue = ''
    for key, value in pairDict.iteritems():
        newSentence = ''
        if len(value) == 1:
            prevValue = value[0]
            nextValue = value
            if newSentence == '':
                newSentence += key + ' ' + nextValue[0]
            else:
                newSentence += ' ' + nextValue[0]
            nextValue = pairDict.get(prevValue)

        else:
            for string in value:
                prevValue = string
                if newSentence == '':
                    newSentence += key + ' ' + string
                else:
                    newSentence += ' ' + string
        print newSentence
        sentences.append(newSentence)
    # for i in xrange(len(words)-1):
    #     pairDict = {words[i] : words[i+1]}
    #     pairs.append(pairDict)
    # print pairs
    # for i, pair in enumerate(pairs): #Iterate through all pairs, changing starting pair
    #     newSentence = ''
    #     j = i #Copy starting position
    #     howLong = 0 #Track number of pairs laid down in newSentence
    #     while howLong < len(pairs):
    #         curDict = pairs[j]
    #         for key in curDict:
    #             if newSentence == '': 
    #                 newSentence += key + ' ' + curDict.get(key)
    #             else: 
    #                 newSentence += ' ' + curDict.get(key)    
    #         if j + 1 == len(pairs):
    #             j = 0
    #         else:
    #             j += 1
    #         howLong+=1
    #     sentences.append(newSentence)
    #     print "Appended: " + newSentence
    print sentences
    return sentences
    # END_YOUR_CODE

############################################################
# Problem 3d

def sparseVectorDotProduct(v1, v2):
    """
    Given two sparse vectors |v1| and |v2|, each represented as collections.defaultdict(float), return
    their dot product.
    You might find it useful to use sum() and a list comprehension.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    dotProd = 0
    larger = v1
    smaller = v2
    if len(v2) > len(v1):
        larger = v2
        smaller = v1
    for key, value in larger.iteritems():
        if smaller.get(key) != None:
            dotProd += smaller.get(key) * value
    return dotProd
    # END_YOUR_CODE

############################################################
# Problem 3e

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    for key, value in v1.iteritems():
        if v2.get(key) != None:
            v1[key] = value + scale * v2.get(key)
    for key, value in v2.iteritems():
        if v1.get(key) == None:
            newVal = scale * value
            v1.update({key: newVal})
    return v1
    # END_YOUR_CODE

############################################################
# Problem 3f

def findSingletonWords(text):
    """
    Splits the string |text| by whitespace and returns the set of words that
    occur exactly once.
    You might find it useful to use collections.defaultdict(int).
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    words = text.split()
    singletons = set()
    for word in words:
        if words.count(word) == 1:
            singletons.add(word)
    return singletons
    # END_YOUR_CODE

############################################################
# Problem 3g

def computeLongestPalindromeLength(text):
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.
    """
    # BEGIN_YOUR_CODE (our solution is 19 lines of code, but don't worry if you deviate from this)
    cache = {}
    def recurse(m, n):
    #Compute longest palindrome from text[m:n+1]
        if (m, n) in cache:
            return cache[(m, n)] 
        elif m > n:
            return 0
        elif m == n:
            return 1
        elif text[m] == text[n]:
            result = 2 + recurse(m+1, n-1)
        else:
            excludeM = recurse(m+1, n)
            excludeN = recurse(m, n-1)
            result = max(excludeM, excludeN)
        cache[(m, n)] = result
        return result
    return recurse(0, len(text)-1)
    # END_YOUR_CODE
