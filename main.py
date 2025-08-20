import pygame
import random
import sys
from typing import List, Tuple, Dict, Set

WIDTH, HEIGHT = 900, 600
FPS = 60

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE  = (66, 135, 245)
GREEN = (56, 174, 56)
RED   = (220, 68, 68)
ORANGE= (245, 160, 66)

# 점자 표준 도트 번호 (좌열 1-2-3, 우열 4-5-6)
DOT_LABELS = [1, 2, 3, 4, 5, 6]

# -----------------------------
# English Braille dataset (letters only, from user's schema)
# Each entry: {'english': <char>, 'number': 1, 'braille': [[b1,b2,b3,b4,b5,b6]]}
# -----------------------------
english_alpha_1 = {'english' : 'a', 'number' : 1, 'braille' : [[1, 0, 0, 0, 0, 0]]}
english_alpha_2 = {'english' : 'b', 'number' : 1, 'braille' : [[1, 1, 0, 0, 0, 0]]}
english_alpha_3 = {'english' : 'c', 'number' : 1, 'braille' : [[1, 0, 0, 1, 0, 0]]}
english_alpha_4 = {'english' : 'd', 'number' : 1, 'braille' : [[1, 0, 0, 1, 1, 0]]}
english_alpha_5 = {'english' : 'e', 'number' : 1, 'braille' : [[1, 0, 0, 0, 1, 0]]}
english_alpha_6 = {'english' : 'f', 'number' : 1, 'braille' : [[1, 1, 0, 1, 0, 0]]}
english_alpha_7 = {'english' : 'g', 'number' : 1, 'braille' : [[1, 1, 0, 1, 1, 0]]}
english_alpha_8 = {'english' : 'h', 'number' : 1, 'braille' : [[1, 1, 0, 0, 1, 0]]}
english_alpha_9 = {'english' : 'i', 'number' : 1, 'braille' : [[0, 1, 0, 1, 0, 0]]}
english_alpha_10 = {'english' : 'j', 'number' : 1, 'braille' : [[0, 1, 0, 1, 1, 0]]}
english_alpha_11 = {'english' : 'k', 'number' : 1, 'braille' : [[1, 0, 1, 0, 0, 0]]}
english_alpha_12 = {'english' : 'l', 'number' : 1, 'braille' : [[1, 1, 1, 0, 0, 0]]}
english_alpha_13 = {'english' : 'm', 'number' : 1, 'braille' : [[1, 0, 1, 1, 0, 0]]}
english_alpha_14 = {'english' : 'n', 'number' : 1, 'braille' : [[1, 0, 1, 1, 1, 0]]}
english_alpha_15 = {'english' : 'o', 'number' : 1, 'braille' : [[1, 0, 1, 0, 1, 0]]}
english_alpha_16 = {'english' : 'p', 'number' : 1, 'braille' : [[1, 1, 1, 1, 0, 0]]}
english_alpha_17 = {'english' : 'q', 'number' : 1, 'braille' : [[1, 1, 1, 1, 1, 0]]}
english_alpha_18 = {'english' : 'r', 'number' : 1, 'braille' : [[1, 1, 1, 0, 1, 0]]}
english_alpha_19 = {'english' : 's', 'number' : 1, 'braille' : [[0, 1, 1, 1, 0, 0]]}
english_alpha_20 = {'english' : 't', 'number' : 1, 'braille' : [[0, 1, 1, 1, 1, 0]]}
english_alpha_21 = {'english' : 'u', 'number' : 1, 'braille' : [[1, 0, 1, 0, 0, 1]]}
english_alpha_22 = {'english' : 'v', 'number' : 1, 'braille' : [[1, 1, 1, 0, 0, 1]]}
english_alpha_23 = {'english' : 'w', 'number' : 1, 'braille' : [[0, 1, 0, 1, 1, 1]]}
english_alpha_24 = {'english' : 'x', 'number' : 1, 'braille' : [[1, 0, 1, 1, 0, 1]]}
english_alpha_25 = {'english' : 'y', 'number' : 1, 'braille' : [[1, 0, 1, 1, 1, 1]]}
english_alpha_26 = {'english' : 'z', 'number' : 1, 'braille' : [[1, 0, 1, 0, 1, 1]]}
english_alpha = [
    english_alpha_1, english_alpha_2, english_alpha_3, english_alpha_4, english_alpha_5,
    english_alpha_6, english_alpha_7, english_alpha_8, english_alpha_9, english_alpha_10,
    english_alpha_11, english_alpha_12, english_alpha_13, english_alpha_14, english_alpha_15,
    english_alpha_16, english_alpha_17, english_alpha_18, english_alpha_19, english_alpha_20,
    english_alpha_21, english_alpha_22, english_alpha_23, english_alpha_24, english_alpha_25,
    english_alpha_26]

from typing import Any

def dataset_to_map_alpha(dataset: List[Dict[str, Any]]) -> Dict[str, Tuple[int, ...]]:
    """Convert user's english_alpha schema to { 'char': (dots...) } mapping."""
    mapping: Dict[str, Tuple[int, ...]] = {}
    for row in dataset:
        ch = row['english']
        bits = row['braille'][0]  # first cell only (letters are single cell)
        dots = tuple(i + 1 for i, b in enumerate(bits) if b)
        mapping[ch] = dots
    return mapping

# Build active map from letters only
ACTIVE_MAP: Dict[str, Tuple[int, ...]] = dataset_to_map_alpha(english_alpha)
LESSON: List[str] = list(ACTIVE_MAP.keys())

# -----------------------------
# UI 컴포넌트
# -----------------------------
class Button:
    def __init__(self, rect: pygame.Rect, text: str, onclick, font: pygame.font.Font,
                 bg=LIGHT_GRAY, fg=BLACK, border=GRAY):
        self.rect = rect
        self.text = text
        self.onclick = onclick
        self.font = font
        self.bg = bg
        self.fg = fg
        self.border = border

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.bg, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.border, self.rect, 2, border_radius=10)
        label = self.font.render(self.text, True, self.fg)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.onclick:
                    self.onclick()

class BrailleCell:
    def __init__(self, center: Tuple[int, int], dot_radius: int = 22, gap_y: int = 60, gap_x: int = 75):
        self.center = center
        self.dot_radius = dot_radius
        self.gap_y = gap_y
        self.gap_x = gap_x
        self.selected: Set[int] = set()  # 1..6
        self._compute_positions()

    def _compute_positions(self):
        cx, cy = self.center
        # 왼쪽 열 x, 오른쪽 열 x
        lx, rx = cx - self.gap_x // 2, cx + self.gap_x // 2
        # 위에서부터 3칸
        y1, y2, y3 = cy - self.gap_y, cy, cy + self.gap_y
        # 도트 인덱스: 1,2,3,4,5,6
        self.dot_positions = {
            1: (lx, y1),
            2: (lx, y2),
            3: (lx, y3),
            4: (rx, y1),
            5: (rx, y2),
            6: (rx, y3),
        }

    def clear(self):
        self.selected.clear()

    def set_pattern(self, dots: Tuple[int, ...]):
        self.selected = set(dots)

    def get_pattern(self) -> Tuple[int, ...]:
        return tuple(sorted(self.selected))

    def toggle_at(self, pos: Tuple[int, int]):
        x, y = pos
        for idx, (dx, dy) in self.dot_positions.items():
            if (x - dx) ** 2 + (y - dy) ** 2 <= self.dot_radius ** 2:
                if idx in self.selected:
                    self.selected.remove(idx)
                else:
                    self.selected.add(idx)
                return True
        return False

    def draw(self, surface: pygame.Surface, font_small: pygame.font.Font):
        # 외곽 가이드
        cx, cy = self.center
        w = self.gap_x + self.dot_radius * 2
        h = self.gap_y * 2 + self.dot_radius * 2
        guide_rect = pygame.Rect(cx - w // 2 - 15, cy - h // 2 - 15, w + 30, h + 30)
        pygame.draw.rect(surface, LIGHT_GRAY, guide_rect, border_radius=14)
        pygame.draw.rect(surface, GRAY, guide_rect, 2, border_radius=14)

        # 6개 점
        for idx in DOT_LABELS:
            (dx, dy) = self.dot_positions[idx]
            filled = idx in self.selected
            pygame.draw.circle(surface, BLACK, (dx, dy), self.dot_radius, 0 if filled else 2)
            # 점 번호 라벨(작게)
            lbl = font_small.render(str(idx), True, BLUE if filled else GRAY)
            r = lbl.get_rect(center=(dx, dy))
            r.y += self.dot_radius + 12
            surface.blit(lbl, r)

# -----------------------------
# Main App
# -----------------------------
class BrailleTrainer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Braille Trainer (6-dot)")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont(None, 72)
        self.font_med = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 22)

        # 상태
        self.mode = 'quiz'  # 'study' or 'quiz'
        self.score = 0
        self.total = 0
        self.feedback = ''
        self.feedback_color = BLACK

        # 학습 목록 섞기
        self.lesson = LESSON[:]
        random.shuffle(self.lesson)
        self.idx = 0
        self.current_char = self.lesson[self.idx]

        # 점자 셀
        self.cell = BrailleCell(center=(WIDTH // 2, HEIGHT // 2 - 30))

        # 버튼
        self.buttons: List[Button] = []
        self._create_buttons()

    def _create_buttons(self):
        bx, by = 120, HEIGHT - 110
        bw, bh, pad = 140, 50, 16
        def add(text, cb):
            rect = pygame.Rect(add.x, by, bw, bh)
            self.buttons.append(Button(rect, text, cb, self.font_med))
            add.x += bw + pad
        add.x = bx

        add("Answer", self.check_answer)
        add("Hint", self.show_hint)
        add("Initialization", self.clear_cell)
        add("Next", self.next_item)
        add("Mode", self.toggle_mode)
        add("Shuffle", self.shuffle_lesson)

    # ---------- 동작 ----------
    def toggle_mode(self):
        self.mode = 'study' if self.mode == 'quiz' else 'quiz'
        self.feedback = f"Mode: {self.mode.upper()}"
        self.feedback_color = ORANGE
        self.cell.clear()

    def shuffle_lesson(self):
        random.shuffle(self.lesson)
        self.idx = 0
        self.current_char = self.lesson[self.idx]
        self.feedback = "Shuffled"
        self.feedback_color = ORANGE
        self.cell.clear()

    def next_item(self):
        self.idx = (self.idx + 1) % len(self.lesson)
        self.current_char = self.lesson[self.idx]
        self.feedback = ''
        self.cell.clear()

    def clear_cell(self):
        self.cell.clear()
        self.feedback = ''

    def show_hint(self):
        # 현재 글자의 정답 패턴을 미리 적용 (학습 모드용)
        ans = ACTIVE_MAP[self.current_char]
        self.cell.set_pattern(ans)
        self.feedback = "Hint: See the shaded pattern"
        self.feedback_color = BLUE

    def check_answer(self):
        ans = ACTIVE_MAP[self.current_char]
        pred = self.cell.get_pattern()
        self.total += 1
        if pred == ans:
            self.score += 1
            self.feedback = "Correct!"
            self.feedback_color = GREEN
        else:
            self.feedback = f"Wrong. Answer is {ans}"
            self.feedback_color = RED

    # ---------- Render ----------
    def draw_header(self):
        # 현재 문자 표시
        title = f"학습 문자: '{self.current_char}'"
        if self.mode == 'study':
            subtitle = "Study Mode: 힌트로 패턴 확인 가능"
        else:
            subtitle = "Quiz Mode: 패턴을 클릭으로 입력 후 정답확인"
        label = self.font_big.render(title, True, BLACK)
        sub = self.font_med.render(subtitle, True, GRAY)
        self.screen.blit(label, (60, 30))
        self.screen.blit(sub, (60, 100))

    def draw_footer(self):
        # Score and Feedback
        score_txt = f"Score: {self.score} / {self.total}"
        srf = self.font_med.render(score_txt, True, BLACK)
        self.screen.blit(srf, (60, HEIGHT - 60))

        if self.feedback:
            fb = self.font_med.render(self.feedback, True, self.feedback_color)
            self.screen.blit(fb, (WIDTH // 2, HEIGHT - 60))

    def draw_buttons(self):
        for b in self.buttons:
            b.draw(self.screen)

    # ---------- Event ----------
    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # 점자 토글
                if self.cell.toggle_at(event.pos):
                    self.feedback = ''
            # 버튼 처리
            for b in self.buttons:
                b.handle_event(event)
        return True

    def run(self):
        while True:
            if not self.handle_events():
                pygame.quit()
                sys.exit()

            self.screen.fill(WHITE)

            self.draw_header()
            if self.mode == 'study':
                self.cell.set_pattern(ACTIVE_MAP[self.current_char])
            self.cell.draw(self.screen, self.font_small)
            self.draw_buttons()
            self.draw_footer()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    app = BrailleTrainer()
    app.run()
