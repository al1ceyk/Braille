from data import english_alpha, english_acr, english_abb

def test_braille(brailles_list):
    for braille_dict in brailles_list:
        print(braille_dict['english'])
        braille = braille_dict['braille']
        for i in range(braille_dict['number']):
            if braille[i][0] == 1:
                print('O', end=' ')
            else:
                print('X', end=' ')
            
            if braille[i][3] == 1:
                print('O', end=' ')
            else:
                print('X', end=' ')
        print()
        for i in range(braille_dict['number']):
            if braille[i][1] == 1:
                print('O', end=' ')
            else:
                print('X', end=' ')
            
            if braille[i][4] == 1:
                print('O', end=' ')
            else:
                print('X', end=' ')
        print()
        for i in range(braille_dict['number']):
            if braille[i][2] == 1:
                print('O', end=' ')
            else:
                print('X', end=' ')
            
            if braille[i][5] == 1:
                print('O', end=' ')
            else:
                print('X', end=' ')
        print()
        print('-'*10)