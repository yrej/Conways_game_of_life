# overlay.py
import pygame as pg

class HelpOverlay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.visible = True
        self._build()

    def _build(self):
        self.font_title = pg.font.SysFont("Arial", 28, bold=True)
        self.font_text  = pg.font.SysFont("Arial", 18)

        self.lines = [
            ("Conway's Game of Life",           self.font_title, (255, 255, 255)),
            ("",                                self.font_text,  (200, 200, 200)),
            ("Left click    – place / remove cell",  self.font_text,  (200, 200, 200)),
            ("Space        – pause / resume",        self.font_text,  (200, 200, 200)),
            ("↑ / ↓           – speed up / slow down",  self.font_text,  (200, 200, 200)),
            ("C               – clear the grid",        self.font_text,  (200, 200, 200)),
            ("Press any key or click to start", self.font_text,  (255, 220, 50)),
        ]

        # pre-render surfaces so draw() is fast
        self.rendered = [
            (font.render(text, True, color), font.get_height())
            for text, font, color in self.lines
        ]
    
    def draw(self, screen):
        if not self.visible:
            return

        # dim the background
        overlay = pg.Surface((self.width, self.height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # centered box
        box_w, box_h = 620, 420
        box_x = (self.width  - box_w) // 2
        box_y = (self.height - box_h) // 2

        box = pg.Surface((box_w, box_h), pg.SRCALPHA)
        box.fill((30, 30, 30, 220))
        screen.blit(box, (box_x, box_y))

        # draw text lines
        y = box_y + 30
        for surf, line_height in self.rendered:
            screen.blit(surf, (box_x + 30, y))
            y += line_height + 8