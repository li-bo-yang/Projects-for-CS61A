"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    valid_list = []
    for paragraph in paragraphs:
        if select(paragraph):
            valid_list.append(paragraph)
    if k > len(valid_list):
        return ''
    else:        
        while k < len(valid_list):
            paragraph = valid_list[k]
            if select(paragraph):
                return paragraph
            else:
                k += 1 
        return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select_func(input_list):
        input_list = split(input_list)
        input_list = [lower(x) for x in input_list]
        input_list = [remove_punctuation(x) for x in input_list]
        for key in topic:
            for word in input_list:
                if key == word:
                    return True
        return False

    return select_func  
    # END PROBLEM 2

def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    count, index = 0, 0
    if len(typed_words) == 0 or len(reference_words) == 0:
        return 0.0
    elif len(typed_words) != len(reference_words) and typed_words[0] != reference_words[0]:
        return 0.0
    while index < len(reference_words):
        if len(typed_words) == len(reference_words):
            if typed_words[index] == reference_words[index]:
                count += 1
            index += 1
        elif len(typed_words) != len(reference_words):
            if index >= min(len(typed_words), len(reference_words)):
                if len(typed_words) < len(reference_words):
                    return (100 * count / len(typed_words))
                return (100 * count / len(reference_words))
            if typed_words[index] == reference_words[index]:
                count += 1
            index += 1
    return (100 * count / max(len(reference_words),len(typed_words)))
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    word = len(typed) / 5.0
    return word / (elapsed / 60.0)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than or equal to LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    accuracy_list = []
    for valid in valid_words:
        accuracy_list.append(diff_function(user_word, valid, limit)) 
    best = min(accuracy_list)
    if best > limit:
        return user_word
    else:
        return valid_words[accuracy_list.index(best)]
        
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def helper(start, goal, limit, count):
        if count > limit:
            return limit + 114514
        elif len(start) == 0 and len(goal) == 0:
            return count
        elif len(start) == 0 and len(goal) != 0:
            return max(len(start), len(goal)) + count
        elif len(start) != 0 and len(goal) == 0:
            return max(len(start), len(goal)) + count
        else:
            if start[0] == goal[0]:
                return helper(start[1:], goal[1:], limit, count)
            elif start[0] != goal[0]:
                return helper(start[1:], goal[1:], limit, count+1)

    return helper(start, goal, limit, 0)
    # END PROBLEM 6


def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    m = len(start) + 1
    n = len(goal) + 1   
    matrix = []
    for i in range(m):
        matrix.append([])
        for j in range(n):
            matrix[i].append("蛤")
   
    for i in range(m):
        matrix[i][0] = i
    for j in range(n):
        matrix[0][j] = j

    for x in range(1, m):
        for y in range(1, n):
            if start[x-1] == goal[y-1]:
                matrix[x][y] = min(matrix[x-1][y] + 1, matrix[x-1][y-1], matrix[x][y-1] + 1)
            else:
                matrix[x][y] = min(matrix[x-1][y] + 1, matrix[x-1][y-1] + 1, matrix[x][y-1] + 1)
    if matrix[m-1][n-1] > limit:
        return 114514
    else:
        return matrix[m-1][n-1]  


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    def check(typed, prompt):
        if len(typed) == 0 and len(prompt) != 0:
            return 0 
        if typed[0] != prompt[0]:
            return 0
        elif typed[0] == prompt[0]:
            return 1 + check(typed[1:], prompt[1:])
    
    ratio = check(typed, prompt) / len(prompt)
    dictionary = {'id': id, 'progress': ratio}
    send(dictionary)
    return ratio
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    #from decimal import getcontext
    #getcontext().prec = 5
    word_matrix = []
    for _ in range(n_players):      
        word_matrix.append([])
    for j in range(1, n_words+1):       
        index_list = [] 
        time_list = []
        for i in range(n_players):
            time_list.append(elapsed_time(word_times[i][j]) - elapsed_time(word_times[i][j-1]))
        min_time =min(time_list) 
        for i in range(n_players):
            time_passed = elapsed_time(word_times[i][j]) - elapsed_time(word_times[i][j-1])
            if time_passed < min_time or abs(time_passed - min_time) < margin:
                index_list.append(i)
                min_time = time_passed
        for index in index_list:    
            if word(word_times[0][j]) != 'START':
                word_matrix[index].append(word(word_times[0][j]))
    return word_matrix    
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = True  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)