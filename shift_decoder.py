"""
filename: shift_decoder.py
language: Python3
author:   Scott Furman, saf5151@rit.edu

'shift_decoder' is used to decode texts that have been encoded using a Caesarian shift, without
having any knowledge of its key. The ciphertext can either be manually inputted, or sourced in a file.
It uses letter frequency analysis to determine the most likely shift key. Because of this, larger
sections of text with a more representative frequency will be more likely to work with the first
recommended key.
However, There is also an interactive console that allows users to shift by any key they wish,
and to change the ciphertext to a different string
"""
import sys  # for accepting command-line args
import re   # for regex pattern matching user input


def eval_ciphertext( ciphertext ):
    """
    This is the primary function for the general evaluation of a ciphertext. This includes:
     - finding the frequency of each letter in the ciphertext
     - finding recommended shift keys
     - printing the ciphertext after shifting it with the most recommended key
     - printing other recommendations if the best key was wrong

    :param ciphertext: the encoded string
    """
    ciphertext = ciphertext.upper()
    text_freq = freq( ciphertext )
    shift_keys = get_shift_keys( ciphertext, text_freq )

    print("Estimated Shift-Key: ", shift_keys[0] )
    print()
    print( shift( ciphertext, shift_keys[0] ) )
    print()
    print( "If the above is still incorrect, try shifting with the following keys:", shift_keys[1], ",", shift_keys[2] )


def freq(ciphertext):
    """
    Iterates through a ciphertext and totals the occurrences of each letter

    :param ciphertext: the encoded string
    :return: a dictionary mapping English letters to their frequency in the given text
    """
    freq_dict = empty_freq_dict()
    total = 0

    # total up the frequency
    for letter in ciphertext:
        if letter.isalpha():
            freq_dict[letter] += 1
            total += 1

    # calculate percentage of use
    for letter in freq_dict:
        if freq_dict[letter] != 0:
            freq_dict[letter] = freq_dict[letter] / total * 100

    return freq_dict


def get_shift_keys(ciphertext, text_freq):
    """
    For each letter in the ciphertext, its 'closest letter' is found.  The difference between the closest
    letter and the original represents a shift key. Occurrences of shift keys are totaled, at the top 3
    are returned.

    :param ciphertext: the encoded string
    :param text_freq: a dictionary mapping the frequency of each letter in the text
    :return: a 3-tuple of ints containing the top 3 options for shift keys
    """
    # find out the most common shift using letter frequency
    shift_freq = {}

    for letter in ciphertext:
        if letter.isalpha():
            # get a similar letter from standard letter frequency
            cleartext_letter = closest_letter(text_freq[letter])
            shift_num = ord(cleartext_letter) - ord(letter)

            if shift_num not in shift_freq:
                shift_freq[shift_num] = 0

            shift_freq[shift_num] += 1

    shift_keys = sorted(shift_freq.keys(), key=lambda k: shift_freq[k], reverse=True)
    return shift_keys[0], shift_keys[1], shift_keys[2]


def shift( ciphertext, shift_key ):
    """
    Performs a Caesarian shift on a text

    :param ciphertext: the encoded string
    :param shift_key: the amount you want to shift by
    :return: a string representing the ciphertext after it has been shifted
    """
    cleartext = ""

    for letter in ciphertext:
        if letter.isalpha():
            new_letter = ord( letter ) + shift_key

            if new_letter > ord( "Z" ):
                new_letter = ord( "@" ) + new_letter - ord( "Z" )  # '@' is right before 'A', so used as buffer

            elif new_letter < ord( "A" ):
                new_letter = ord( "[" ) + new_letter - ord( "A" )  # '[' is right after 'Z', so used as buffer

            cleartext += chr( new_letter ) # FIXME doesnt wrap

        else:
            # just copies all whitespace and other symbols
            cleartext += letter

    return cleartext


def closest_letter( freq_percentage ):
    """
    Finds the 'closest letter' by comparing the percentage of use in a given text
    to the standard English frequency percentages

    :param freq_percentage: frequency percentage of a certain letter in a ciphertext
    :return: the letter that the percentage most closely corresponds to
    """
    standard_freq = english_letter_frequency()

    closest_val = min( standard_freq.values(), key=lambda val:abs( float( val ) - freq_percentage ) )

    for letter in standard_freq:
        if standard_freq[ letter ] == closest_val:
            return letter


def empty_freq_dict():
    """
    :return: a dictionary mapping English letters to their frequency in a text, initialized to 0
    """
    return {
        "A" : 0,
        "B" : 0,
        "C" : 0,
        "D" : 0,
        "E" : 0,
        "F" : 0,
        "G" : 0,
        "H" : 0,
        "I" : 0,
        "J" : 0,
        "K" : 0,
        "L" : 0,
        "M" : 0,
        "N" : 0,
        "O" : 0,
        "P" : 0,
        "Q" : 0,
        "R" : 0,
        "S" : 0,
        "T" : 0,
        "U" : 0,
        "V" : 0,
        "W" : 0,
        "X" : 0,
        "Y" : 0,
        "Z" : 0,
    }


def english_letter_frequency():
    """
    Figures taken from the Wikipedia article on Letter Frequency

    :return: dictionary mapping English letters to their frequency, given in percentages
    """
    return {
        "E" : 12.702,
        "T" : 9.056,
        "A" : 8.167,
        "O" : 7.507,
        "I" : 6.966,
        "N" : 6.749,
        "S" : 6.327,
        "H" : 6.094,
        "R" : 5.987,
        "D" : 4.253,
        "L" : 4.025,
        "C" : 2.782,
        "U" : 2.758,
        "M" : 2.406,
        "W" : 2.36,
        "F" : 2.228,
        "G" : 2.015,
        "Y" : 1.974,
        "P" : 1.929,
        "B" : 1.492,
        "V" : .978,
        "K" : .772,
        "J" : .153,
        "X" : .15,
        "Q" : .095,
        "Z" : .074
    }


def main():
    print( "##################################" )
    print( "#          Shift Decoder         #" )
    print( "##################################" )
    print( "Usage: python shift_decoder.py [filename]")
    print()

    ciphertext = ""

    if len( sys.argv ) == 2:
        # if a file was specified, open the file and evaluate its contents
        try:
            input_file = open( sys.argv[1], "r" )

            for line in input_file:
                ciphertext += line

            eval_ciphertext( ciphertext )
        
        except:
            print( "Error reading file." ) 

    # set regex patterns for program loop
    shift_pattern = re.compile( "shift -?\d+" )
    new_pattern = re.compile( "new \".+\"" )

    # main program loop
    cmd = ""
    while cmd.lower() != "q" and cmd.lower() != "quit":
        cmd = input( "> " )

        # quit
        if cmd.lower() == "q" or cmd.lower() == "quit":
            break

        # shift the ciphertext by a specified number
        elif shift_pattern.match( cmd.lower() ):
            shift_key = int( cmd.split( " " )[1] )
            print( shift( ciphertext, shift_key ) )

        # set the ciphertext to a new string
        elif new_pattern.match( cmd.lower() ):
            ciphertext = cmd[ 5 : -1 ].upper()
            eval_ciphertext( ciphertext )

        # print out a usage message
        else:
            print( "Commands:" )
            print( "h/help             - prints this help message" )
            print( "shift #            - prints out the given ciphertext, shifted by # places" )
            print( "new \"ciphertext\" - sets the ciphertext to be the string inside the quotes, and prints evaluation")
            print( "q/quit             - quits the program" )


main()
