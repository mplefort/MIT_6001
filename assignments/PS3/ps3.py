# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Matthew LeFort
# Collaborators : <your collaborators>
# Time spent    : 10/16 7:00 PM - 

import math
import random
import string

VOWELS = 'aeiou*'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 15

SCRABBLE_LETTER_VALUES = {
	'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
	'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
	's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"


def load_words():
	"""
	Returns a list of valid words. Words are strings of lowercase letters.
	
	Depending on the size of the word list, this function may
	take a while to finish.
	"""
	
	print("Loading word list from file...")
	# inFile: file
	inFile = open(WORDLIST_FILENAME, 'r')
	# wordlist: list of strings
	wordlist = []
	for line in inFile:
		wordlist.append(line.strip().lower())
	print("  ", len(wordlist), "words loaded.")
	return wordlist


def get_frequency_dict(sequence):
	"""
	Returns a dictionary where the keys are elements of the sequence
	and the values are integer counts, for the number of times that
	an element is repeated in the sequence.

	sequence: string or list
	return: dictionary
	"""
	
	# freqs: dictionary (element_type -> int)
	freq = {}
	for x in sequence:
		freq[x] = freq.get(x, 0) + 1
	return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
	"""
	Returns the score for a word. Assumes the word is a
	valid word.

	You may assume that the input word is always either a string of letters, 
	or the empty string "". You may not assume that the string will only contain 
	lowercase letters, so you will have to handle uppercase and mixed case strings 
	appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
			1, or
			7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
			and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

	word: string
	n: int >= 0
	returns: int >= 0
	"""

	score1 = 0
	score2 = 0

	if word is '':
		return 0
	# get sum of letters points
	for let in word:
		if let is '*':
			score1 = score1
		else:
			score1 = score1 + SCRABBLE_LETTER_VALUES.get(let.lower())

	score2 = 7 * len(word) - 3 * (n - len(word))
	if score2 < 1: score2 = 1

	score = score1 * score2
	
	return score

# print(get_word_score('weed', 7))



# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
	"""
	Displays the letters currently in the hand.

	For example:
	   display_hand({'a':1, 'x':2, 'l':3, 'e':1})
	Should print out something like:
	   a x x l l l e
	The order of the letters is unimportant.

	hand: dictionary (string -> int)
	"""
	print('Current Hand: ', end='')
	for letter in hand.keys():
		for j in range(hand[letter]):
			 print(letter, end=' ')      # print all on the same line
	print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
	"""
	Returns a random hand containing n lowercase letters.
	ceil(n/3) letters in the hand should be VOWELS (note,
	ceil(n/3) means the smallest integer not less than n/3).
	One letter shall be 

	Hands are represented as dictionaries. The keys are
	letters and the values are the number of times the
	particular letter is repeated in that hand.

	n: int >= 0
	returns: dictionary (string -> int)
	"""
	
	hand={}
	num_vowels = int(math.ceil(n / 3))

	for i in range(num_vowels):
		if i is 0:
			x = '*'
		else:
			x = random.choice(VOWELS)
		hand[x] = hand.get(x, 0) + 1
	
	for i in range(num_vowels, n):    
		x = random.choice(CONSONANTS)
		hand[x] = hand.get(x, 0) + 1
	
	return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
	"""
	Does NOT assume that hand contains every letter in word at least as
	many times as the letter appears in word. Letters in word that don't
	appear in hand should be ignored. Letters that appear in word more times
	than in hand should never result in a negative count; instead, set the
	count in the returned hand to 0 (or remove the letter from the
	dictionary, depending on how your code is structured). 

	Updates the hand: uses up the letters in the given word
	and returns the new hand, without those letters in it.

	Has no side effects: does not modify hand.

	word: string
	hand: dictionary (string -> int)    
	returns: dictionary (string -> int)
	"""
	lowerWord = word.lower()

	newhand = hand.copy()

	for let in lowerWord:
		# if let not in hand dict continue
		if newhand.get(let) is None:
			continue

		# if let in hand = 0, leave at 0
		elif newhand.get(let) is 0:
			del newhand[let]
			continue

		else:
			newhand[let] = newhand.get(let) - 1
			if newhand.get(let) is 0:
				del newhand[let]
				
	return newhand


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
	"""
	Returns True if word is in the word_list and is entirely
	composed of letters in the hand. Otherwise, returns False.
	Does not mutate hand or word_list.

	Checks for use of "*" wildcard letter.

	word: string
	hand: dictionary (string -> int)
	word_list: list of lowercase strings
	returns: boolean
	"""
	# validWord Flase until proven True
	validWord = False
	lowerWord = word.lower()

	# Confirm word is composed of letters in hand
	letsCheck = True
	wordDict = get_frequency_dict(lowerWord)
	for let, val in wordDict.items():
		if hand.get(let,0) < val:
			letsCheck = False

	# if letsCheck:
	# 	print('letters check pass')
	
	# Confirm word in word list
	realWord = False
	# if using wildcard or all real letters
	if '*' in lowerWord:
		wildIndex = lowerWord.find('*')

		for let in VOWELS:

			wildWord = list(lowerWord)
			wildWord[wildIndex] = let
			wildWord = "".join(wildWord)
			# print(wildWord)

			if wildWord in word_list:
				realWord = True
				# print('Found wild word: ' + wildWord)
				break

	# check if using all letters
	elif lowerWord in word_list:
		realWord = True

	else:
		realWord = False
	
	if letsCheck and realWord:
		validWord = True

	# if not validWord:
	# 	print('That is not a vlaid word. Please choose another word.')

	return validWord

	# str.find(sub,start,end)

# word_list = load_words()

# hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
# word = "h*ney"

# print(is_valid_word(word, hand, word_list))


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
	""" 
	Returns the length (number of letters) in the current hand.
	
	hand: dictionary (string-> int)
	returns: integer
	"""

	handLen = 0
	for let, val in hand.items():
		handLen = handLen + val
	
	return handLen


def play_hand(hand, word_list):

	"""
	Allows the user to play the given hand, as follows:

	* The hand is displayed.
	
	* The user may input a word.

	* When any word is entered (valid or invalid), it uses up letters
	  from the hand.

	* An invalid word is rejected, and a message is displayed asking
	  the user to choose another word.

	* After every valid word: the score for that word is displayed,
	  the remaining letters in the hand are displayed, and the user
	  is asked to input another word.

	* The sum of the word scores is displayed when the hand finishes.

	* The hand finishes when there are no more unused letters.
	  The user can also finish playing the hand by inputing two 
	  exclamation points (the string '!!') instead of a word.

	  hand: dictionary (string -> int)
	  word_list: list of lowercase strings
	  returns: the total score for the hand
	  
	"""
	
	# Keep track of the total score
	totalScore = 0

	# As long as there are still letters left in the hand:
	while calculate_handlen(hand) > 0:

		# Display the hand
		display_hand(hand)

		# Ask user for input
		# print('Enter word, or "!!" to indicate that you are finished: ', end='')
		word = input('Enter word, or "!!" to indicate that you are finished: ')

		# If the input is two exclamation points:
		if word == '!!':
			# End the game (break out of the loop)
			break
			
		# Otherwise (the input is not two exclamation points):
		else:
			# If the word is valid:
			if is_valid_word(word, hand, word_list):
				# Tell the user how many points the word earned,
				# and the updated total score
				wordScore =  get_word_score(word,calculate_handlen(hand))
				totalScore = totalScore + wordScore 

				print('"%s" earned %d points. Total: %d points' % (word, wordScore, totalScore))
				print()

			# Otherwise (the word is not valid):
			else:
				# Reject invalid word (print a message)
				print('That is not a valid word. Please choose another word.')	
				print()
			# update the user's hand by removing the letters of their inputted word
			hand = update_hand(hand, word)

	# Game is over (user entered '!!' or ran out of letters),
	# so tell user the total score
	print('Ran out of letters. Total score: %d' %(totalScore))
	# Return the total score as result of function
	return totalScore


#
# Problem #6: Playing a game
# 

#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
	""" 
	Allow the user to replace all copies of one letter in the hand (chosen by user)
	with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
	should be different from user's choice, and should not be any of the letters
	already in the hand.

	If user provide a letter not in the hand, the hand should be the same.

	Has no side effects: does not mutate hand.

	For example:
		substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
	might return:
		{'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
	The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
	already in the hand.
	
	hand: dictionary (string -> int)
	letter: string
	returns: dictionary (string -> int)
	"""
	
	handCopy = hand.copy()

	# if sub letter not in hand let them now and return same hand
	if letter not in hand:
		print('Letter not in hand, must select letter from hand to replace')
		return hand
	
	# else get count of letter
	letCount = handCopy.get(letter)
	
	# remove letter from hand
	del handCopy[letter]

	# select and add new letter from vowels and constantants
		# if new letter already in hand, select another until true and add letter count to hand
	newLet = list(handCopy.keys())[0]
	
	while newLet in handCopy.keys():
		vowelRand = random.choice(VOWELS)
		constantantsRand = random.choice(CONSONANTS)
		newLet = random.choice([vowelRand, constantantsRand])
	
	handCopy.update({newLet:letCount})
	return handCopy

# hand= {'k': 1, 'e': 1, 'g': 1, 'z': 1, '*': 1, 'o': 1, 'w': 1}
# handCopy = hand.copy()
# letter = 'k'

# print(hand)

# newHand = substitute_hand(hand,letter)

# print(newHand)
# print(hand)

# print(handCopy == hand)
# print(newHand)

	
def play_game(word_list):
	"""
	Allow the user to play a series of hands

	* Asks the user to input a total number of hands

	* Accumulates the score for each hand into a total score for the 
	  entire series
 
	* For each hand, before playing, ask the user if they want to substitute
	  one letter for another. If the user inputs 'yes', prompt them for their
	  desired letter. This can only be done once during the game. Once the
	  substitue option is used, the user should not be asked if they want to
	  substitute letters in the future.

	* For each hand, ask the user if they would like to replay the hand.
	  If the user inputs 'yes', they will replay the hand and keep 
	  the better of the two scores for that hand.  This can only be done once 
	  during the game. Once the replay option is used, the user should not
	  be asked if they want to replay future hands. Replaying the hand does
	  not count as one of the total number of hands the user initially
	  wanted to play.

			* Note: if you replay a hand, you do not get the option to substitute
					a letter - you must play whatever hand you just had.
	  
	* Returns the total score for the series of hands

	word_list: list of lowercase strings
	"""

	totalScoreRun = 0
	totalScoreRound1 = 0
	totalScoreRound2 = 0
	gameCount = 0
	# Get user input for total number of hands to play
	while True:
		try:
			games = int(input('Enter total number of hands: ' ))
		except ValueError:
			print("must be an number")
			continue
		else:
			break
			
	# while game is less than game count, play another hand
	while gameCount < games:
		
		# deal hand
		hand = deal_hand(HAND_SIZE)
		display_hand(hand)

		# Check if sub a letter, and if game has not used it yet
		validInput = False
		while not validInput:
			subWanted = str(input('Would you like to substitute a letter? enter Y/N: '))
			if subWanted.lower() == 'y':
				subLet = input('Which letter would you like to replace: ')
				hand = substitute_hand(hand,subLet)
				validInput = True
				break

			elif subWanted.lower() == 'n':
				validInput = True
				break

			else:
				print('Invalid input')

		print()

		# play hand
		totalScoreRound1 = play_hand(hand, word_list)
		print('-'*20)

		#If user would like to replay hand:
		while True:
			try:
				replayHand = str(input('Would you like to replay hand? Y/n '))
				if replayHand.lower() == 'y':
					totalScoreRound2 = play_hand(hand, word_list)
					break

				elif replayHand.lower() == 'n':
					totalScoreRound2 = 0
					break

				else:
					print('must be Y/n response')
					continue
			except:
				print('must be Y/n response')
				continue

	
		# replay same hand and keep better of two scores, only be used once
		if totalScoreRound2 > totalScoreRound1:
			totalScoreRun += totalScoreRound2
		else:
			totalScoreRun += totalScoreRound1

		gameCount += 1

	# game over, total score was:
	print('Total score over all hands: %d' % totalScoreRun)
	return totalScoreRun


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':

	word_list = load_words()
	# hand = deal_hand(HAND_SIZE)
	# play_hand(hand, word_list)

	#Start Game
	play_game(word_list)


