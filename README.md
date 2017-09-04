# shift_decoder
'shift_decoder' is used to decode texts that have been encoded using a Caesarian shift, without
having any knowledge of its key. The ciphertext can either be manually inputted, or sourced in a file.
It uses letter frequency analysis to determine the most likely shift key. Because of this, larger
sections of text with a more representative frequency will be more likely to work with the first
recommended key.
However, There is also an interactive console that allows users to shift by any key they wish,
and to change the ciphertext to a different string

## Functions
* **eval_ciphertext( ciphertext ):**  
  This is the primary function for the general evaluation of a ciphertext. This includes:
     * finding the frequency of each letter in the ciphertext
     * finding recommended shift keys
     * printing the ciphertext after shifting it with the most recommended key
     * printing other recommendations if the best key was wrong
   param ciphertext: the encoded string
   
* **freq( ciphertext ):**  
  Iterates through a ciphertext and totals the occurrences of each letter
  param ciphertext: the encoded string
  return: a dictionary mapping English letters to their frequency in the given text   
  
* **get_shift_keys( ciphertext, text_freq ):**  
  For each letter in the ciphertext, its 'closest letter' is found.  The difference between the closest
  letter and the original represents a shift key. Occurrences of shift keys are totaled, at the top 3
  are returned.
  param ciphertext: the encoded string
  param text_freq: a dictionary mapping the frequency of each letter in the text
  return: a 3-tuple of ints containing the top 3 options for shift keys
  
* **shift( ciphertext, shift_key ):**  
  Performs a Caesarian shift on a text
  param ciphertext: the encoded string
  param shift_key: the amount you want to shift by
  return: a string representing the ciphertext after it has been shifted
  
* **closest_letter( freq_percentage ):**  
  Finds the 'closest letter' by comparing the percentage of use in a given text
  to the standard English frequency percentages
  param freq_percentage: frequency percentage of a certain letter in a ciphertext
  return: the letter that the percentage most closely corresponds to
  
* **empty_freq_dict():**  
  return: a dictionary mapping English letters to their frequency in a text, initialized to 0
  
* **english_letter_frequency():**  
  Figures taken from the [Wikipedia article on Letter Frequency](https://en.wikipedia.org/wiki/Letter_frequency)
  return: dictionary mapping English letters to their frequency, given in percentages
  
