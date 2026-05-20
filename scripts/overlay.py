from pygame import font, Surface, SRCALPHA
from scripts.constants import WIDTH, HEIGHT

class HelpOverlay:
    """Poloprůhledný overlay zobrazený přes celou obrazovku.

    Překryje celou obrazovku tmavým poloprůhledným pozadím a uprostřed
    zobrazí panel s předaným textem. Overlay zmizí po kliknutí myší
    nebo stisku libovolné klávesy.

    Textové povrchy jsou předvykresleny při inicializaci v metodě
    ``_build()``, aby bylo vykreslování v metodě ``draw()`` co nejrychlejší.

    Args:
        lines: Seznam trojic ``(text, styl, barva)`` definující obsah panelu.
               Styl může být ``"title"`` nebo ``"text"``.
        width: Šířka obrazovky v pixelech.
        height: Výška obrazovky v pixelech.
        visible: ``True`` pokud má být overlay zobrazen.
        rendered: Seznam předvykreslených textových povrchů a jejich výšek.
    """
    def __init__(self,lines: list[tuple[str, str, tuple[int, int, int]]],visibility : bool) -> None:
        """Inicializuje overlay a předvykreslí textové povrchy.
        Args:
            lines: Seznam trojic ``(text, styl, barva)``, kde styl je
                   ``"title"`` (tučný, 28 px) nebo ``"text"`` (18 px)
                   a barva je RGB trojice, např. ``(255, 255, 255)``.
            visibility: bool zda má být overlay při inicializaci
        """
        self.width = WIDTH
        self.height = HEIGHT
        self.lines = lines
        self.visible = visibility
        self._build()

    def _build(self) -> None:
        """Připraví fonty a předvykreslí všechny textové řádky.

        Vytvoří interní fonty ``_font_title`` a ``_font_text`` a předvykreslí
        každý řádek z ``self.lines`` do Surface, aby metoda ``draw()``
        nemusela renderovat text při každém snímku.

        Výsledek je uložen do ``self.rendered`` jako seznam dvojic
        ``(Surface, výška_řádku)``.

        Returns:
            None
        """
        self._font_title = font.SysFont("Arial", 28, bold=True)
        self._font_text  = font.SysFont("Arial", 18)

        # pre-render surfaces so draw() is fast
        self.rendered = [
            ( (self._font_title if style == "title" else self._font_text)
                .render(text, True, color),
                (self._font_title if style == "title" else self._font_text)
                .get_height(), )
            for text, style, color in self.lines
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