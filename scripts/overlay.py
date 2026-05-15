from pygame import font, Surface, SRCALPHA
from scripts.constants import WIDTH, HEIGHT

class HelpOverlay:
    """Poloprůhledná nápověda zobrazená při spuštění programu.

    Překryje celou obrazovku tmavým poloprůhledným pozadím a uprostřed
    zobrazí panel s ovládáním programu. Nápověda zmizí po kliknutí myší
    nebo stisku libovolné klávesy.

    Textové povrchy jsou předvykresleny při inicializaci v metodě
    ``_build()``, aby bylo vykreslování v metodě ``draw()`` co nejrychlejší.

    Args:
        width: Šířka obrazovky v pixelech.
        height: Výška obrazovky v pixelech.
        visible: ``True`` pokud má být nápověda zobrazena.
        rendered: Seznam předvykreslených textových povrchů a jejich výšek.
    """
    def __init__(self) -> None:
        """Inicializuje overlay a předvykreslí textové povrchy."""
        self.width = WIDTH
        self.height = HEIGHT
        self.visible = True
        self._build()

    def _build(self) -> None:
        """Připraví fonty a předvykreslí všechny textové řádky.

        Vytvoří seznam trojic (text, font, barva) definující obsah nápovědy
        a předvykreslí každý řádek do Surface, aby metoda ``draw()``
        nemusela renderovat text při každém snímku.

        Returns:
            None
        """
        self.font_title = font.SysFont("Arial", 28, bold=True)
        self.font_text  = font.SysFont("Arial", 18)

        self.lines = [
            ("Conway's Game of Life",           self.font_title, (255, 255, 255)),
            ("",                                self.font_text,  (200, 200, 200)),
            ("Cell can be placed or removed only when paused",self.font_text,  (200, 200, 200)),
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
    
    def draw(self, screen : Surface) -> None:
        """Vykreslí nápovědu na obrazovku.

        Pokud není nápověda viditelná (``self.visible == False``),
        metoda se okamžitě vrátí bez jakéhokoliv vykreslování.

        Vykreslení probíhá ve třech krocích:
            1. Poloprůhledné ztmavení celé obrazovky.
            2. Tmavý obdélníkový panel uprostřed obrazovky.
            3. Předvykreslené textové řádky uvnitř panelu.

        Args:
            screen: Hlavní zobrazovací povrch, na který se nápověda vykreslí.

        Returns:
            None
        """
        if not self.visible:
            return

        # dim the background
        overlay = Surface((self.width, self.height), SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # centered box
        box_w, box_h = 620, 420
        box_x = (self.width  - box_w) // 2
        box_y = (self.height - box_h) // 2

        box = Surface((box_w, box_h), SRCALPHA)
        box.fill((30, 30, 30, 220))
        screen.blit(box, (box_x, box_y))

        # draw text lines
        y = box_y + 30
        for surf, line_height in self.rendered:
            screen.blit(surf, (box_x + 30, y))
            y += line_height + 8