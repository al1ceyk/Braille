import pygame
import math
import json
import os

from functools import partial

from params import *
from ui_components import *
from data import *

# -----------------------------
# Main Menu
# -----------------------------
class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Braille Trainer')
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.offset = 0
        self.content_h = HEIGHT

        self.page = 'language_select'
        self.language = 'english'
        self.braille_type = 'english'

        # --- Favorites (persistent) ---
        self.fav_path = 'favorites.json'
        self.favorites = self._load_favorites()

        # 현재 디테일 화면의 항목(즐겨찾기 토글용)
        self.current_detail_list = None   # 현재 데이터셋 (ex. english_alpha)
        self.current_detail_index = None  # 현재 인덱스
        self.current_detail_category = None  # 'alphabet' / 'punctuation' ...

        # Fonts
        # self.font_big = pygame.font.SysFont('d2coding', 60)
        # self.font_med = pygame.font.SysFont('d2coding', 50)
        # self.font_small = pygame.font.SysFont('d2coding', 30)
        # self.font_alphabet = pygame.font.SysFont('d2coding', 130)
        # self.font_alphabet_small = pygame.font.SysFont('d2coding', 60)
        
        self.font_big = pygame.font.SysFont('d2codingver13220180524', 60)
        self.font_med = pygame.font.SysFont('d2codingver13220180524', 50)
        self.font_small = pygame.font.SysFont('d2codingver13220180524', 30)
        self.font_alphabet = pygame.font.SysFont('d2codingver13220180524', 130)
        self.font_alphabet_small = pygame.font.SysFont('d2codingver13220180524', 60)

        self.language_select_menu = []
        self.create_language_select_menu()

        # Alphabet
        self.english_menu = []
        self.braille_type_menu = []

        self.review_menu = []
        
        self.alphabet_menu = []
        
        self.alphabet_detail_menu = []
        self.braille_grid_rect = None
        self.braille_grid_count = 0
        self.is_finished = False

        # Punctuation
        self.punctuation_menu = []

        # Number
        self.number_menu = []

        # symbols
        self.symbols_menu = []

        # Currency
        self.currency_menu = []

        # Indicators
        self.indicators_menu = []

        # Abbreviated form
        self.abbreviated_form_menu = []

        # Math
        self.math_menu = []
        
        # Acronym form
        self.acronym_form_menu = []

        self.consonant_menu = []
        self.final_consonant_menu = []
        self.vowel_menu = []
        self.kor_number_menu = []
        self.kor_math_menu = []
        self.kor_acronym_form_menu = []
        self.kor_abbreviated_form_menu = []
        self.kor_punctuation_menu = []

        self.back_button = self.create_back_button()
    
    # ---------- Landing page ----------
    def create_language_select_menu(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, 20 * PAD

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.language_select_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        add('English', self.english_language_function)
        add('한국어', self.korean_language_function)
        
        self.content_h = add.y + bh
        print(self.content_h)

    def create_braille_type_menu(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, 20 * PAD

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.braille_type_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        if self.language == 'english':
            add('English Braille', self.english_braille_function)
            add('Korean Braille', self.korean_braille_function)
        elif self.language == 'korean':
            add('영어 점자', self.english_braille_function)
            add('한국어 점자', self.korean_braille_function)

        self.content_h = add.y + bh
        print(self.content_h)

    # ---------- English Menu Page ----------
    # ---------- Korean Menu Page ----------
    def create_english_menu(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * (10 + 7)

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.english_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by
        if self.braille_type == 'english':
            if self.language == 'english':
                add('Review Hard Braille', self.reivew_function)
                add('Alphabet', self.alphabet_function)
                add('Punctuation', self.punctuation_function)
                add('Number', self.number_function)
                add('Symbols', self.symbols_function)
                add('Currency', self.currency_function)
                add('Indicators', self.indicators_function)
                add('Abbreviation 1', self.abbreviated_form_function)
                add('Math', self.math_function)
                add('Abbreviation 2', self.acronym_form_function)
            elif self.language == 'korean':
                add('복습', self.reivew_function)
                add('알파벳', self.alphabet_function)
                add('문장부호', self.punctuation_function)
                add('숫자', self.number_function)
                add('심볼', self.symbols_function)
                add('화폐', self.currency_function)
                add('인디케이터', self.indicators_function)
                add('축약', self.abbreviated_form_function)
                add('수학', self.math_function)
                add('약어', self.acronym_form_function)
        elif self.braille_type == 'korean':
            if self.language == 'english':
                add('Review Hard Braille', self.reivew_function)
                add('Consonant', self.consonant_function)
                add('Final consonant', self.final_consonant_function)
                add('vowel', self.vowel_function)
                add('Number', self.kor_number_function)
                add('Math', self.kor_math_function)
                add('Abbreviation 1', self.kor_abbreviated_form_function)
                add('Abbreviation 2', self.kor_acronym_form_function)
                add('Punctuation', self.kor_punctuation_function)
            elif self.language == 'korean':
                add('복습', self.reivew_function)
                add('초성', self.consonant_function)
                add('종성', self.final_consonant_function)
                add('모음', self.vowel_function)
                add('숫자', self.kor_number_function)
                add('수학', self.kor_math_function)
                add('약어', self.kor_abbreviated_form_function)
                add('약자', self.kor_acronym_form_function)
                add('문장부호', self.kor_punctuation_function)

        self.content_h = add.y + PAD

    # ---------- Review page ----------
    # def create_review_page(self):
    #     self.review_menu.clear()

    #     bw, bh = WIDTH - 2 * PAD, 75
    #     bx, by = PAD, 17 * PAD

    #     def add(text, cb):
    #         rect = pygame.Rect(bx, add.y, bw, bh)
    #         self.review_menu.append(Button(rect, text, cb, self.font_small))
    #         add.y += bh + PAD
    #     add.y = by

    #     if not self.favorites:
    #         add('No favorites yet.', None)
    #         add('Tap ☆ on a letter!', None)
    #     else:
    #         for fav in self.favorites:
    #             label = f"[{fav['category']}] {fav['english']}"
    #             cb = partial(self.open_favorite, fav['category'], fav['index'])
    #             add(label, cb)

    #     self.content_h = add.y + PAD

    def create_review_page(self):
        self.review_menu.clear()

        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, 17 * PAD

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.review_menu.append(Button(rect, text, cb, self.font_small))
            add.y += bh + PAD
        add.y = by

        current_bt = self.braille_type
        filtered = [f for f in self.favorites if f.get('braille_type') == current_bt]

        if not filtered:
            add('No favorites yet.', None)
            add('Tap ☆ on a letter!', None)
        else:
            for fav in filtered:
                label = f"[{fav['category']}] {fav['english']}"
                cb = partial(self.open_favorite, fav['category'], fav['index'])
                add(label, cb)

        self.content_h = add.y + PAD

    # ---------- Alphabet page ---------- 
    def create_alphabet_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.alphabet_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_alpha):
            cb = partial(self.alphabet_detail_function, idx, english_alpha)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD
        # print(self.content_h)
    
    # ---------- Punctuation page ----------
    def create_punctuation_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.punctuation_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_punc):
            cb = partial(self.punctuation_detail_function, idx, english_punc)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Number page ----------
    def create_number_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.number_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_num):
            cb = partial(self.number_detail_function, idx, english_num)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Symbols page ----------
    def create_symbols_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.symbols_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_symb):
            cb = partial(self.symbols_detail_function, idx, english_symb)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Currency page ----------
    def create_currency_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.currency_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_curr):
            cb = partial(self.currency_detail_function, idx, english_curr)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Indicators page ----------
    def create_indicators_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.indicators_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_indic):
            cb = partial(self.indicators_detail_function, idx, english_indic)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Abbreviated form page ----------
    def create_abbreviated_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.abbreviated_form_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_abb):
            cb = partial(self.abbreviated_form_detail_function, idx, english_abb)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Math page ----------
    def create_math_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.math_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_math):
            cb = partial(self.math_detail_function, idx, english_math)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Consonant page ----------
    def create_consonant_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.consonant_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        for idx, alphabet_dict in enumerate(korean_cons):
            cb = partial(self.consonant_detail_function, idx, korean_cons)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Final consonant page ----------
    def create_final_consonant_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.final_consonant_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        for idx, alphabet_dict in enumerate(korean_final_cons):
            cb = partial(self.final_consonant_detail_function, idx, korean_final_cons)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Vowel page ----------
    def create_vowel_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.vowel_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        for idx, alphabet_dict in enumerate(korean_vowel):
            cb = partial(self.vowel_detail_function, idx, korean_vowel)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Kor number page ----------
    def create_kor_number_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.kor_number_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        for idx, alphabet_dict in enumerate(korean_num):
            cb = partial(self.kor_number_detail_function, idx, korean_num)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Kor math page ----------
    def create_kor_math_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.kor_math_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        for idx, alphabet_dict in enumerate(korean_math):
            cb = partial(self.kor_math_detail_function, idx, korean_math)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Kor acronym form page ----------
    def create_kor_acronym_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.kor_acronym_form_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        for idx, alphabet_dict in enumerate(korean_acr):
            cb = partial(self.kor_acronym_form_detail_function, idx, korean_acr)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Kor abbreviated form page ----------
    def create_kor_abbreviated_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.kor_abbreviated_form_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        for idx, alphabet_dict in enumerate(korean_abb):
            cb = partial(self.kor_abbreviated_form_detail_function, idx, korean_abb)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Kor punctuation page ----------
    def create_kor_punctuation_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.kor_punctuation_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        for idx, alphabet_dict in enumerate(korean_punc):
            cb = partial(self.kor_punctuation_detail_function, idx, korean_punc)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    # ---------- Acronym form page ----------
    def create_acronym_page(self):
        bw, bh = WIDTH - 2 * PAD, 75
        bx, by = PAD, PAD * 17

        def add(text, cb):
            rect = pygame.Rect(bx, add.y, bw, bh)
            self.acronym_form_menu.append(Button(rect, text, cb, self.font_med))
            add.y += bh + PAD
        add.y = by

        # add('Start', self.start_function)

        for idx, alphabet_dict in enumerate(english_acr):
            cb = partial(self.acronym_form_detail_function, idx, english_acr)
            add(alphabet_dict['english'], cb)

        self.content_h = add.y + PAD

    def _draw_single_braille_grid_fixed(self, x0, y0, radius, rows=3, cols=2, idx=0):
        dot_index = [0, 3, 1, 4, 2, 5]
        dot_count = 0
        for r in range(rows):
            for c in range(cols):
                cx = x0 + radius + c * (2 * radius + CELL_GAP)
                cy = y0 + radius + r * (2 * radius + CELL_GAP)
                if self.braille_dict['braille'][idx][dot_index[dot_count]] == 1:
                    pygame.draw.circle(self.screen, BLACK, (int(cx), int(cy)), int(radius))
                else:
                    pygame.draw.circle(self.screen, WHITE, (int(cx), int(cy)), int(radius))
                dot_count += 1

    def draw_braille_grids_row_fixed(self, rect, count, rows=3, cols=2):
        if not rect or count <= 0:
            return
        
        grid_w = cols * 2 * DOT_RADIUS + (cols - 1) * CELL_GAP
        grid_h = rows * 2 * DOT_RADIUS + (rows - 1) * CELL_GAP

        per_row = max(1, (rect.width + GRID_GAP) // (grid_w + GRID_GAP))
        rows_needed = math.ceil(count / per_row)

        total_h = rows_needed * grid_h + (rows_needed - 1) * GRID_ROW_GAP
        y0 = rect.centery - total_h / 2

        remain = count
        idx = 0
        for ri in range(rows_needed):
            n_in_row = int(min(per_row, remain))
            remain -= n_in_row

            row_w = n_in_row * grid_w + (n_in_row - 1) * GRID_GAP
            x0 = rect.centerx - row_w / 2
            y = y0 + ri * (grid_h + GRID_ROW_GAP)

            for j in range(n_in_row):
                gx = x0 + j * (grid_w + GRID_GAP)
                self._draw_single_braille_grid_fixed(gx, y, DOT_RADIUS, rows=rows, cols=cols, idx=idx)
                idx += 1

    def create_alphabet_detail_page(self, idx, english_alpha):
        if idx != len(english_alpha):
            self.current_detail_list = english_alpha
            self.current_detail_index = idx
            self.current_detail_category = self._category_from_page(self.page)

            bx, by = BACK_WIDTH + PAD * 2, PAD
            rect = pygame.Rect(bx, by, BACK_WIDTH, BACK_HEIGHT)
            cb = partial(self.next_function, idx + 1, english_alpha)
            self.alphabet_detail_menu.append(Button(rect, 'NEXT', cb, self.font_small))

            star_size = BACK_HEIGHT
            sx = WIDTH - PAD - star_size
            sy = PAD
            srect = pygame.Rect(sx, sy, star_size, star_size)

            item_english = english_alpha[idx].get('english', '')
            is_fav = False
            if self.current_detail_category:
                is_fav = self._is_favorited(self.current_detail_category, item_english)

            star_text = '★' if is_fav else '☆'
            self.alphabet_detail_menu.append(Button(srect, star_text, self.toggle_favorite, self.font_big))
            
            bx, by = PAD, BACK_HEIGHT + PAD * 2
            bw, bh = WIDTH - 2 * PAD, (HEIGHT - by) // 2
            rect = pygame.Rect(bx, by, bw, bh)
            if self.page == 'indicators_detail':
                self.alphabet_detail_menu.append(Button(rect, english_alpha[idx]['english'], None, self.font_alphabet_small, BACKGROUND_COLOR, FONT_COLOR, BACKGROUND_COLOR))
            else:
                self.alphabet_detail_menu.append(Button(rect, english_alpha[idx]['english'], None, self.font_alphabet, BACKGROUND_COLOR, FONT_COLOR, BACKGROUND_COLOR))
            
            bx, by = PAD, rect.bottom
            rect = pygame.Rect(bx, by, bw, bh)
            self.braille_grid_rect = rect.inflate(-PAD * 2, -PAD * 2)
            self.braille_grid_count = english_alpha[idx]['number']
            self.braille_dict = english_alpha[idx]
        else:
            bx, by = PAD, BACK_HEIGHT + PAD * 2
            bw, bh = WIDTH - 2 * PAD, (HEIGHT - by * 2) // 2
            rect = pygame.Rect(bx, by, bw, bh)
            self.alphabet_detail_menu.append(Button(rect, 'Nice Work!', None, self.font_big, BACKGROUND_COLOR, FONT_COLOR, BLACK))

            bx, by = PAD, by + bh + PAD * 2
            # bw, bh = WIDTH - 2 * PAD, (HEIGHT - by) // 2
            rect = pygame.Rect(bx, by, bw, bh)
            self.alphabet_detail_menu.append(Button(rect, 'Next Step', self.next_step_function, self.font_big, BACKGROUND_COLOR, FONT_COLOR, BLACK))
    
    def create_back_button(self):
        bx, by = PAD, PAD

        rect = pygame.Rect(bx, by, BACK_WIDTH, BACK_HEIGHT)
        return Button(rect, 'BACK', self.back_function, self.font_small)
    
    # ---------- Language select functions ----------
    def english_language_function(self):
        print('English language function')
        self.page = 'braille_type'
        self.language_select_menu.clear()
        self.language = 'english'
        self.create_braille_type_menu()
        self.offset = 0

    def korean_language_function(self):
        print('Korean language function')
        self.page = 'braille_type'
        self.language_select_menu.clear()
        self.language = 'korean'
        self.create_braille_type_menu()
        self.offset = 0

    # ---------- Braille type functions ----------
    def english_braille_function(self):
        print('English braille function')
        self.page = 'english_menu'
        self.braille_type = 'english'
        self.braille_type_menu.clear()
        self.create_english_menu()
        self.offset = 0
    
    def korean_braille_function(self):
        print('English braille function')
        self.page = 'english_menu'
        self.braille_type = 'korean'
        self.braille_type_menu.clear()
        self.create_english_menu()
        self.offset = 0

    # ---------- English Menu's functions ----------
    def reivew_function(self):
        print('Review function')
        self.page = 'review'
        self.english_menu.clear()
        self.create_review_page()
        self.offset = 0

    def alphabet_function(self):
        print('Alphabet function')
        self.page = 'alphabet'
        self.english_menu.clear()
        self.create_alphabet_page()
        self.offset = 0

    def punctuation_function(self):
        print('Punctuation function')
        self.page = 'punctuation'
        self.english_menu.clear()
        self.create_punctuation_page()
        self.offset = 0

    def number_function(self):
        print('Number function')
        self.page = 'number'
        self.english_menu.clear()
        self.create_number_page()
        self.offset = 0

    def symbols_function(self):
        print('Symbols function')
        self.page = 'symbols'
        self.english_menu.clear()
        self.create_symbols_page()
        self.offset = 0

    def currency_function(self):
        print('Currency function')
        self.page = 'currency'
        self.english_menu.clear()
        self.create_currency_page()
        self.offset = 0

    def indicators_function(self):
        print('Indicators function')
        self.page = 'indicators'
        self.english_menu.clear()
        self.create_indicators_page()
        self.offset = 0

    def abbreviated_form_function(self):
        print('Abbreviated form function')
        self.page = 'abbreviated_form'
        self.english_menu.clear()
        self.create_abbreviated_page()
        self.offset = 0

    def math_function(self):
        print('Math function')
        self.page = 'math'
        self.english_menu.clear()
        self.create_math_page()
        self.offset = 0

    def acronym_form_function(self):
        print('Acronym form function')
        self.page = 'acronym_form'
        self.english_menu.clear()
        self.create_acronym_page()
        self.offset = 0

    # ---------- Korean Menu's functions ----------
    def consonant_function(self):
        print('Consonant function')
        self.page = 'consonant'
        self.english_menu.clear()
        self.create_consonant_page()
        self.offset = 0

    def final_consonant_function(self):
        print('Final consonant function')
        self.page = 'final_consonant'
        self.english_menu.clear()
        self.create_final_consonant_page()
        self.offset = 0

    def vowel_function(self):
        print('Vowel function')
        self.page = 'vowel'
        self.english_menu.clear()
        self.create_vowel_page()
        self.offset = 0

    def kor_number_function(self):
        print('Kor number function')
        self.page = 'kor_number'
        self.english_menu.clear()
        self.create_kor_number_page()
        self.offset = 0

    def kor_math_function(self):
        print('Kor math function')
        self.page = 'kor_math'
        self.english_menu.clear()
        self.create_kor_math_page()
        self.offset = 0

    def kor_acronym_form_function(self):
        print('Kor acronym form function')
        self.page = 'kor_acronym_form'
        self.english_menu.clear()
        self.create_kor_acronym_page()
        self.offset = 0

    def kor_abbreviated_form_function(self):
        print('Kor abbreviated form function')
        self.page = 'kor_abbreviated_form'
        self.english_menu.clear()
        self.create_kor_abbreviated_page()
        self.offset = 0

    def kor_punctuation_function(self):
        print('Kor punctuation function')
        self.page = 'kor_punctuation'
        self.english_menu.clear()
        self.create_kor_punctuation_page()
        self.offset = 0

    # ----------Unified english braille functions ----------
    def start_function(self):
        pass
    
    def alphabet_detail_function(self, idx, english_alpha):
        print('Alphabet detail page')
        self.page = 'alphabet_detail'
        self.alphabet_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def punctuation_detail_function(self, idx, english_alpha):
        print('Punctuation detail page')
        self.page = 'punctuation_detail'
        self.punctuation_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def number_detail_function(self, idx, english_alpha):
        print('Number detail page')
        self.page = 'number_detail'
        self.number_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def symbols_detail_function(self, idx, english_alpha):
        print('Symbols detail page')
        self.page = 'symbols_detail'
        self.symbols_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def currency_detail_function(self, idx, english_alpha):
        print('Alphabet detail page')
        self.page = 'currency_detail'
        self.currency_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def indicators_detail_function(self, idx, english_alpha):
        print('Indicators detail page')
        self.page = 'indicators_detail'
        self.indicators_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def abbreviated_form_detail_function(self, idx, english_alpha):
        print('Abbreviated form detail page')
        self.page = 'abbreviated_form_detail'
        self.abbreviated_form_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def math_detail_function(self, idx, english_alpha):
        print('Math detail page')
        self.page = 'math_detail'
        self.math_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def acronym_form_detail_function(self, idx, english_alpha):
        print('Acronym form detail page')
        self.page = 'acronym_form_detail'
        self.acronym_form_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0
 
    # ----------Unified korean braille functions ----------
    def consonant_detail_function(self, idx, english_alpha):
        print('Consonant detail page')
        self.page = 'consonant_detail'
        self.consonant_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0
    
    def final_consonant_detail_function(self, idx, english_alpha):
        print('Final consonant detail page')
        self.page = 'final_consonant_detail'
        self.final_consonant_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def vowel_detail_function(self, idx, english_alpha):
        print('Vowel detail page')
        self.page = 'vowel_detail'
        self.vowel_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0
    
    def kor_number_detail_function(self, idx, english_alpha):
        print('Number detail page')
        self.page = 'kor_number_detail'
        self.kor_number_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0
    
    def kor_math_detail_function(self, idx, english_alpha):
        print('Math detail page')
        self.page = 'kor_math_detail'
        self.kor_math_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0
    
    def kor_acronym_form_detail_function(self, idx, english_alpha):
        print('Acronym form detail page')
        self.page = 'kor_acronym_form_detail'
        self.kor_acronym_form_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def kor_abbreviated_form_detail_function(self, idx, english_alpha):
        print('Abbreviated form detail page')
        self.page = 'kor_abbreviated_form_detail'
        self.kor_abbreviated_form_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    def kor_punctuation_detail_function(self, idx, english_alpha):
        print('Punctuation detail page')
        self.page = 'kor_punctuation_detail'
        self.kor_punctuation_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0

    # ---------- Alphabet detail functions ----------
    def next_function(self, idx, english_alpha):
        print('Next function')
        self.alphabet_detail_menu.clear()
        self.create_alphabet_detail_page(idx, english_alpha)
        self.offset = 0
        if idx == len(english_alpha):
            self.is_finished = True
    
    # ---------- Favorites helpers ----------
    def _infer_braille_type_from_category(self, category):
        if category in KOREAN_CATEGORIES:
            return 'korean'
        return 'english'

    # def _load_favorites(self):
    #     if os.path.exists(self.fav_path):
    #         try:
    #             with open(self.fav_path, 'r', encoding='utf-8') as f:
    #                 data = json.load(f)
    #                 if isinstance(data, list):
    #                     return data
    #         except Exception:
    #             pass
    #     return []

    def _load_favorites(self):
        if os.path.exists(self.fav_path):
            try:
                with open(self.fav_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        changed = False
                        for fav in data:
                            if 'braille_type' not in fav:
                                fav['braille_type'] = self._infer_braille_type_from_category(fav.get('category'))
                                changed = True
                        if changed:
                            with open(self.fav_path, 'w', encoding='utf-8') as wf:
                                json.dump(data, wf, ensure_ascii=False, indent=2)
                        return data
            except Exception:
                pass
        return []

    def _save_favorites(self):
        try:
            with open(self.fav_path, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _category_from_page(self, page):
        if page.endswith('_detail'):
            return page[:-7]  # remove "_detail"
        return None

    # def _dataset_for_category(self, category):
    #     mapping = {
    #         'alphabet':          english_alpha,
    #         'punctuation':       english_punc,
    #         'number':            english_num,
    #         'symbols':           english_symb,
    #         'currency':          english_curr,
    #         'indicators':        english_indic,
    #         'abbreviated_form':  english_abb,
    #         'math':              english_math,
    #         'acronym_form':      english_acr,
    #     }
    #     return mapping.get(category)

    def _dataset_for_category(self, category):
        mapping = {
            'alphabet':          english_alpha,
            'punctuation':       english_punc,
            'number':            english_num,
            'symbols':           english_symb,
            'currency':          english_curr,
            'indicators':        english_indic,
            'abbreviated_form':  english_abb,
            'math':              english_math,
            'acronym_form':      english_acr,
            'consonant':             korean_cons,
            'final_consonant':       korean_final_cons,
            'vowel':                 korean_vowel,
            'kor_number':            korean_num,
            'kor_math':              korean_math,
            'kor_acronym_form':      korean_acr,
            'kor_abbreviated_form':  korean_abb,
            'kor_punctuation':       korean_punc,
        }
        return mapping.get(category)

    def _detail_page_for_category(self, category):
        return f'{category}_detail'

    def _is_favorited(self, category, english_text):
        return any(f['category'] == category and f['english'] == english_text for f in self.favorites)

    # def toggle_favorite(self):
    #     cat = self._category_from_page(self.page)
    #     if cat is None or self.current_detail_list is None or self.current_detail_index is None:
    #         return
    #     item = self.current_detail_list[self.current_detail_index]
    #     english_text = item.get('english', str(item))

    #     idx = next((i for i, f in enumerate(self.favorites)
    #                 if f['category'] == cat and f['english'] == english_text), -1)

    #     if idx >= 0:
    #         del self.favorites[idx]
    #     else:
    #         self.favorites.append({
    #             'category': cat,
    #             'index': self.current_detail_index,
    #             'english': english_text,
    #         })

    #     self._save_favorites()

    #     self.alphabet_detail_menu.clear()
    #     self.create_alphabet_detail_page(self.current_detail_index, self.current_detail_list)
    #     self.offset = 0

    def toggle_favorite(self):
        cat = self._category_from_page(self.page)
        if cat is None or self.current_detail_list is None or self.current_detail_index is None:
            return
        item = self.current_detail_list[self.current_detail_index]
        english_text = item.get('english', str(item))
        bt = self.braille_type

        idx = next((i for i, f in enumerate(self.favorites)
                    if f.get('category') == cat and f.get('english') == english_text and f.get('braille_type') == bt), -1)

        if idx >= 0:
            del self.favorites[idx]
        else:
            self.favorites.append({
                'category': cat,
                'index': self.current_detail_index,
                'english': english_text,
                'braille_type': bt,     
            })

        self._save_favorites()

        self.alphabet_detail_menu.clear()
        self.create_alphabet_detail_page(self.current_detail_index, self.current_detail_list)
        self.offset = 0

    def open_favorite(self, category, index):
        dataset = self._dataset_for_category(category)
        if not dataset:
            return
        self.page = self._detail_page_for_category(category)
        self.alphabet_detail_menu.clear()
        self.create_alphabet_detail_page(index, dataset)
        self.offset = 0

    def next_step_function(self):
        print('Next Stage Function')

        chain = {
            'alphabet_detail':              ('punctuation_detail',           english_punc),
            'punctuation_detail':           ('number_detail',                english_num),
            'number_detail':                ('symbols_detail',               english_symb),
            'symbols_detail':               ('currency_detail',              english_curr),
            'currency_detail':              ('indicators_detail',            english_indic),
            'indicators_detail':            ('abbreviated_form_detail',      english_abb),
            'abbreviated_form_detail':      ('math_detail',                  english_math),
            'math_detail':                  ('acronym_form_detail',          english_acr),
            'acronym_form_detail':          ('english_menu',                 None),
            'consonant_detail':             ('final_consonant_detail',       korean_final_cons),
            'final_consonant_detail':       ('vowel_detail',                 korean_vowel),
            'vowel_detail':                 ('kor_number_detail',            korean_num),
            'kor_number_detail':            ('kor_math_detail',              korean_math),
            'kor_math_detail':              ('kor_acronym_form_detail',      korean_acr),
            'kor_acronym_form_detail':      ('kor_abbreviated_form_detail',  korean_abb),
            'kor_abbreviated_form_detail':  ('kor_punctuation_detail',       korean_punc),
            'kor_punctuation_detail':       ('english_menu',                 None),
        }

        next_page, dataset = chain.get(self.page, ('english_menu', None))

        self.alphabet_detail_menu.clear()
        self.is_finished = False
        self.offset = 0

        if dataset is None:
            self.page = next_page
            self.english_menu.clear()
            self.create_english_menu()
            return

        self.page = next_page
        self.create_alphabet_detail_page(0, dataset)

    # ---------- BACK functions ----------
    def back_function(self):
        print('Back function')
        if self.page == 'braille_type':
            self.page = 'language_select'
            self.braille_type_menu.clear()
            self.create_language_select_menu()
        elif self.page == 'english_menu' or self.page == 'korean_menu':
            self.create_braille_type_menu()
            self.english_menu.clear()
            self.page = 'braille_type'

        elif self.page == 'review':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page == 'alphabet':
            self.page = 'english_menu'
            self.create_english_menu()
        
        elif self.page =='alphabet_detail':
            self.page = 'alphabet'
            self.alphabet_detail_menu.clear()
            self.create_alphabet_page()
            self.is_finished = False

        elif self.page == 'punctuation':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='punctuation_detail':
            self.page = 'punctuation'
            self.alphabet_detail_menu.clear()
            self.create_punctuation_page()
            self.is_finished = False

        elif self.page == 'number':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='number_detail':
            self.page = 'number'
            self.alphabet_detail_menu.clear()
            self.create_number_page()
            self.is_finished = False

        elif self.page == 'symbols':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='symbols_detail':
            self.page = 'symbols'
            self.alphabet_detail_menu.clear()
            self.create_symbols_page()
            self.is_finished = False

        elif self.page == 'currency':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='currency_detail':
            self.page = 'currency'
            self.alphabet_detail_menu.clear()
            self.create_currency_page()
            self.is_finished = False

        elif self.page == 'indicators':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='indicators_detail':
            self.page = 'indicators'
            self.alphabet_detail_menu.clear()
            self.create_indicators_page()
            self.is_finished = False

        elif self.page == 'abbreviated_form':
            self.page = 'english_menu'
            self.create_english_menu()
        
        elif self.page =='abbreviated_form_detail':
            self.page = 'abbreviated_form'
            self.alphabet_detail_menu.clear()
            self.create_abbreviated_page()
            self.is_finished = False

        elif self.page == 'math':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='math_detail':
            self.page = 'math'
            self.alphabet_detail_menu.clear()
            self.create_math_page()
            self.is_finished = False

        elif self.page == 'acronym_form':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='acronym_form_detail':
            self.page = 'acronym_form'
            self.alphabet_detail_menu.clear()
            self.create_acronym_page()
            self.is_finished = False
        
        elif self.page == 'consonant':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='consonant_detail':
            self.page = 'consonant'
            self.alphabet_detail_menu.clear()
            self.create_consonant_page()
            self.is_finished = False

        elif self.page == 'final_consonant':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='final_consonant_detail':
            self.page = 'final_consonant'
            self.alphabet_detail_menu.clear()
            self.create_final_consonant_page()
            self.is_finished = False

        elif self.page == 'vowel':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='vowel_detail':
            self.page = 'vowel'
            self.alphabet_detail_menu.clear()
            self.create_vowel_page()
            self.is_finished = False

        elif self.page == 'kor_number':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='kor_number_detail':
            self.page = 'kor_number'
            self.alphabet_detail_menu.clear()
            self.create_kor_number_page()
            self.is_finished = False

        elif self.page == 'kor_math':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='kor_math_detail':
            self.page = 'kor_math'
            self.alphabet_detail_menu.clear()
            self.create_kor_math_page()
            self.is_finished = False

        elif self.page == 'kor_acronym_form':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='kor_acronym_form_detail':
            self.page = 'kor_acronym_form'
            self.alphabet_detail_menu.clear()
            self.create_kor_acronym_page()
            self.is_finished = False

        elif self.page == 'kor_abbreviated_form':
            self.page = 'english_menu'
            self.create_english_menu()

        elif self.page =='kor_abbreviated_form_detail':
            self.page = 'kor_abbreviated_form'
            self.alphabet_detail_menu.clear()
            self.create_kor_abbreviated_page()
            self.is_finished = False

        elif self.page == 'kor_punctuation':
            self.page = 'english_menu'
            self.create_english_menu()
        
        elif self.page =='kor_punctuation_detail':
            self.page = 'kor_punctuation'
            self.alphabet_detail_menu.clear()
            self.create_kor_punctuation_page()
            self.is_finished = False
        self.offset = 0
        
    # ---------- Mouse wheel event ----------
    def max_offset(self):
        return max(0, self.content_h - HEIGHT)
    
    def handle_wheel(self, event):
        mo = self.max_offset()
        if mo == 0:
            return 

        dy = 0
        if event.type == pygame.MOUSEWHEEL:
            dy = -event.y * SCROLL_SPEED
        
        if dy != 0:
            self.offset = max(0, min(self.offset + dy, mo))

    def _dispatch_buttons_with_offset(self, buttons, event):
        if hasattr(event, 'pos') and not SCROLL_RECT.collidepoint(event.pos):
            return
        if hasattr(event, 'pos'):
            ed = event.dict.copy()
            ed['pos'] = (event.pos[0], event.pos[1] + self.offset)
            adj_event = pygame.event.Event(event.type, ed)
        else:
            adj_event = event
        
        for b in buttons:
            b.handle_event(adj_event)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Mouse wheel
            if event.type == pygame.MOUSEWHEEL:
                if self.page in (
                    'english_menu', 
                    'alphabet', 
                    'punctuation', 
                    'number', 
                    'symbols', 
                    'currency', 
                    'indicators', 
                    'abbreviated_form', 
                    'math', 
                    'acronym_form',
                    'consonant',
                    'final_consonant',
                    'vowel',
                    'kor_number',
                    'kor_math',
                    'kor_acronym_form',
                    'kor_abbreviated_form',
                    'kor_punctuation') and SCROLL_RECT.collidepoint(pygame.mouse.get_pos()):
                    self.handle_wheel(event)

            # Handle back button
            self.back_button.handle_event(event)

            # Language select menu
            if self.page == 'language_select':
                for m in self.language_select_menu:
                    m.handle_event(event)

            # Braille type menu
            elif self.page == 'braille_type':
                for m in self.braille_type_menu:
                    m.handle_event(event)

            # Handle menu
            elif self.page == 'english_menu':
                self._dispatch_buttons_with_offset(self.english_menu, event)

            # Review menu
            elif self.page == 'review':
                for m in self.review_menu:
                    m.handle_event(event)
            
            # Alphabet menu
            elif self.page == 'alphabet':
                self._dispatch_buttons_with_offset(self.alphabet_menu, event)

            # Alphabet detail menu
            elif self.page == 'alphabet_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            # Punctuation menu
            elif self.page == 'punctuation':
                self._dispatch_buttons_with_offset(self.punctuation_menu, event)

            elif self.page == 'punctuation_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            # Number menu
            elif self.page == 'number':
                self._dispatch_buttons_with_offset(self.number_menu, event)

            elif self.page == 'number_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            # Symbols menu
            elif self.page == 'symbols':
                self._dispatch_buttons_with_offset(self.symbols_menu, event)

            elif self.page == 'symbols_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            # Currency menu
            elif self.page == 'currency':
                self._dispatch_buttons_with_offset(self.currency_menu, event)

            elif self.page == 'currency_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            # Indicators menu
            elif self.page == 'indicators':
                self._dispatch_buttons_with_offset(self.indicators_menu, event)

            elif self.page == 'indicators_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            # Abbreviated form menu
            elif self.page == 'abbreviated_form':
                self._dispatch_buttons_with_offset(self.abbreviated_form_menu, event)

            elif self.page == 'abbreviated_form_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            # Math menu
            elif self.page == 'math':
                self._dispatch_buttons_with_offset(self.math_menu, event)

            elif self.page == 'math_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            # Acronym form menu
            elif self.page == 'acronym_form':
                self._dispatch_buttons_with_offset(self.acronym_form_menu, event)

            elif self.page == 'acronym_form_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            elif self.page == 'consonant':
                self._dispatch_buttons_with_offset(self.consonant_menu, event)
            
            elif self.page == 'consonant_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            elif self.page == 'final_consonant':
                self._dispatch_buttons_with_offset(self.final_consonant_menu, event)
            
            elif self.page == 'final_consonant_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            elif self.page == 'vowel':
                self._dispatch_buttons_with_offset(self.vowel_menu, event)
            
            elif self.page == 'vowel_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            elif self.page == 'kor_number':
                self._dispatch_buttons_with_offset(self.kor_number_menu, event)
            
            elif self.page == 'kor_number_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            elif self.page == 'kor_math':
                self._dispatch_buttons_with_offset(self.kor_math_menu, event)
            
            elif self.page == 'kor_math_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            elif self.page == 'kor_acronym_form':
                self._dispatch_buttons_with_offset(self.kor_acronym_form_menu, event)
            
            elif self.page == 'kor_acronym_form_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            elif self.page == 'kor_abbreviated_form':
                self._dispatch_buttons_with_offset(self.kor_abbreviated_form_menu, event)
            
            elif self.page == 'kor_abbreviated_form_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

            elif self.page == 'kor_punctuation':
                self._dispatch_buttons_with_offset(self.kor_punctuation_menu, event)

            elif self.page == 'kor_punctuation_detail':
                for m in self.alphabet_detail_menu:
                    m.handle_event(event)

        return True
    
    # ---------- Render ----------
    def draw_language_select_menu(self):
        text = self.font_big.render('Basic Braille', True, 'black', None)
        rect = text.get_rect(center=(WIDTH//2, PAD*9))
        self.screen.blit(text, rect)

        text = self.font_big.render('Language Selection', True, 'black', None)
        rect = text.get_rect(center=(WIDTH//2, PAD*15))
        self.screen.blit(text, rect)

        for m in self.language_select_menu:
            m.draw(self.screen)

    def draw_braille_type_menu(self):
        text = self.font_big.render('Basic Braille', True, 'black', None)
        rect = text.get_rect(center=(WIDTH//2, PAD*9))
        self.screen.blit(text, rect)
        for m in self.braille_type_menu:
            m.draw(self.screen)

    def draw_english_menu(self):
        if self.language == 'english':
            text = self.font_big.render('Basic Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_big.render('기본 점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.english_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_review(self):
        if self.language == 'english':
            text = self.font_big.render('Review', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_big.render('복습', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

        for m in self.review_menu:
            m.draw(self.screen)

    def draw_braille(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Alphabet', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('알파벳', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.alphabet_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)
    
    def draw_alphabet_detail(self):
        for m in self.alphabet_detail_menu:
            m.draw(self.screen)
        
        if self.braille_grid_rect and not self.is_finished:
            self.draw_braille_grids_row_fixed(self.braille_grid_rect, count=self.braille_grid_count, rows=3, cols=2)

    def draw_punctuation(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Punctuation', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('문장부호', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.punctuation_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_number(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Number', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('숫자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.number_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_symbols(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Symbols', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('심볼', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.symbols_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_currency(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Currency', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('화폐', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.currency_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_indicators(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Indicators', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('인디케이터', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.indicators_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_abbreviated_form(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Abbreviation 1', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('축약', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.abbreviated_form_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_math(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Math', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('수학', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.math_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_acronym_form(self):
        if self.language == 'english':
            text = self.font_med.render('Unified English Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Abbreviation 2', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준영어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('약어', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.acronym_form_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_consonant(self):
        if self.language == 'english':
            text = self.font_med.render('Unified Korean Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Consonant', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준한국어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('초성', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.consonant_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_final_consonant(self):
        if self.language == 'english':
            text = self.font_med.render('Unified Korean Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Final Consonant', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준한국어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('종성', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.final_consonant_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_vowel(self):
        if self.language == 'english':
            text = self.font_med.render('Unified Korean Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Vowel', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준한국어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('모음', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.vowel_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_kor_number(self):
        if self.language == 'english':
            text = self.font_med.render('Unified Korean Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Number', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준한국어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('숫자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.kor_number_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_kor_math(self):
        if self.language == 'english':
            text = self.font_med.render('Unified Korean Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Math', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준한국어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('수학', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.kor_math_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_kor_acronym_form(self):
        if self.language == 'english':
            text = self.font_med.render('Unified Korean Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Abbreviation 2', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준한국어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('약자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.kor_acronym_form_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_kor_abbreviated_form(self):
        if self.language == 'english':
            text = self.font_med.render('Unified Korean Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Abbreviation 1', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준한국어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('약어', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.kor_abbreviated_form_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_kor_punctuation(self):
        if self.language == 'english':
            text = self.font_med.render('Unified Korean Braille', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('Punctuation', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)
        elif self.language == 'korean':
            text = self.font_med.render('표준한국어점자', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*9))
            self.screen.blit(text, rect)

            text = self.font_med.render('문장부호', True, 'black', None)
            rect = text.get_rect(center=(WIDTH//2, PAD*13))
            self.screen.blit(text, rect)

        self.screen.set_clip(SCROLL_RECT)

        for m in self.kor_punctuation_menu:
            orig = m.rect.copy()
            m.rect.y = orig.y - self.offset
            if m.rect.colliderect(SCROLL_RECT):
                m.draw(self.screen)
            m.rect = orig
        
        self.screen.set_clip(None)

    def draw_back_button(self):
        self.back_button.draw(self.screen)

    def run(self):
        while True:
            if not self.handle_events():
                pygame.quit()
            
            self.screen.fill(BACKGROUND_COLOR)

            if self.page != 'language_select':
                self.draw_back_button()
            
            if self.page == 'language_select':
                self.draw_language_select_menu()
            elif self.page == 'braille_type':
                self.draw_braille_type_menu()
            elif self.page == 'english_menu':
                self.draw_english_menu()
            elif self.page == 'review':
                self.draw_review()

            elif self.page == 'alphabet':
                self.draw_braille()
            elif self.page == 'alphabet_detail':
                self.draw_alphabet_detail()

            elif self.page == 'punctuation':
                self.draw_punctuation()
            elif self.page == 'punctuation_detail':
                self.draw_alphabet_detail()

            elif self.page == 'number':
                self.draw_number()
            elif self.page == 'number_detail':
                self.draw_alphabet_detail()

            elif self.page == 'symbols':
                self.draw_symbols()
            elif self.page == 'symbols_detail':
                self.draw_alphabet_detail()

            elif self.page == 'currency':
                self.draw_currency()
            elif self.page == 'currency_detail':
                self.draw_alphabet_detail()

            elif self.page == 'indicators':
                self.draw_indicators()
            elif self.page == 'indicators_detail':
                self.draw_alphabet_detail()

            elif self.page == 'abbreviated_form':
                self.draw_abbreviated_form()
            elif self.page == 'abbreviated_form_detail':
                self.draw_alphabet_detail()

            elif self.page == 'math':
                self.draw_math()
            elif self.page == 'math_detail':
                self.draw_alphabet_detail()

            elif self.page == 'acronym_form':
                self.draw_acronym_form()
            elif self.page == 'acronym_form_detail':
                self.draw_alphabet_detail()

            elif self.page == 'consonant':
                self.draw_consonant()
            elif self.page == 'consonant_detail':
                self.draw_alphabet_detail()

            elif self.page == 'final_consonant':
                self.draw_final_consonant()
            elif self.page == 'final_consonant_detail':
                self.draw_alphabet_detail()

            elif self.page == 'vowel':
                self.draw_vowel()
            elif self.page == 'vowel_detail':
                self.draw_alphabet_detail()

            elif self.page == 'kor_number':
                self.draw_kor_number()
            elif self.page == 'kor_number_detail':
                self.draw_alphabet_detail()

            elif self.page == 'kor_math':
                self.draw_kor_math()
            elif self.page == 'kor_math_detail':
                self.draw_alphabet_detail()

            elif self.page == 'kor_acronym_form':
                self.draw_kor_acronym_form()
            elif self.page == 'kor_acronym_form_detail':
                self.draw_alphabet_detail()

            elif self.page == 'kor_abbreviated_form':
                self.draw_kor_abbreviated_form()
            elif self.page == 'kor_abbreviated_form_detail':
                self.draw_alphabet_detail()

            elif self.page == 'kor_punctuation':
                self.draw_kor_punctuation()
            elif self.page == 'kor_punctuation_detail':
                self.draw_alphabet_detail()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    print(pygame.font.get_fonts())
    app = MainMenu()
    app.run()

    ###########################################################
    #################################################