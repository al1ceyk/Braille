from data import *

def test_braille():
    for english in english_alpha:
        print(english['english'])
        braille = english['braille']
        if braille[0] == 1:
            print('O', end=' ')
        else:
            print('X', end= ' ')
        
        if braille[3] == 1:
            print('O')
        else:
            print('X')
        
        if braille[1] == 1:
            print('O', end=' ')
        else:
            print('X', end= ' ')
        
        if braille[4] == 1:
            print('O')
        else:
            print('X')
        
        if braille[2] == 1:
            print('O', end=' ')
        else:
            print('X', end= ' ')
        
        if braille[5] == 1:
            print('O')
        else:
            print('X')
        print('-'*10)