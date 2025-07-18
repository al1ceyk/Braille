from data import english_alpha, english_acr, english_abb, english_num, english_math, english_punc, english_symb, english_indic, english_curr
from test import *

if __name__ == '__main__':
    test_braille(english_alpha)
    test_braille(english_acr)
    test_braille(english_abb)
    test_braille(english_num)
    test_braille(english_math)
    test_braille(english_punc)
    test_braille(english_symb)
    test_braille(english_indic)
    test_braille(english_curr)