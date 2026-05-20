# 🧬 Conwayova hra života – Real-time simulace v Pygame
 
Implementace [Conwayovy hry života](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) jako real-time grafické simulace v Pythonu s využitím knihovny **Pygame**. Simulace běží na zdánlivě nekonečné dynamické mřížce, kterou uživatel může volně prozkoumávat a upravovat.
 
---
 
## 📋 Obsah
 
- [O projektu](#o-projektu)
- [Pravidla hry](#pravidla-hry)
- [Funkce](#funkce)
- [Požadavky](#požadavky)
- [Instalace](#instalace)
- [Ovládání](#ovládání)
- [Předdefinované vzory](#předdefinované-vzory)
- [Technické detaily](#technické-detaily)
---
 
## O projektu
 
Conwayova hra života je buněčný automat, ve kterém se na dvourozměrné mřížce vyvíjí populace buněk podle předem daných pravidel. Každá buňka může být **živá** (černá) nebo **mrtvá** (bílá) a její stav v dalším kroku závisí na počtu živých sousedů.
 
Tento projekt implementuje plnohodnotnou grafickou simulaci s:
- dynamicky generovanou (zdánlivě nekonečnou) mřížkou,
- interaktivním zadáváním počátečního stavu myší,
- real-time animací generací,
- možností pausy, změny rychlosti a načítání vzorů.
---
 
## Pravidla hry
 
| Stav buňky | Počet živých sousedů | Výsledek |
|---|---|---|
| Živá | 2 nebo 3 | Přežije |
| Mrtvá | právě 3 | Oživí se |
| Živá | < 2 nebo > 3 | Zemře |
| Mrtvá | ≠ 3 | Zůstane mrtvá |
 
---
 
## Funkce
 
- **Nekonečná mřížka** – zobrazena je vždy jen část plochy; při posunu se automaticky generují nové buňky. Ukládán je pouze stav buněk, které byly vytvořeny nebo změněny.
- **Pohyb po ploše** – posun pomocí klávesnice nebo tažením myší s dynamickým načítáním dalších částí mřížky.
- **Interaktivní editace** – kliknutím myší přepínáte stav jednotlivých buněk (živá / mrtvá); možnost vymazání celé plochy.
- **Real-time animace** – simulace běží automaticky, generace se mění a zobrazují plynule v okně.
- **Pauza a spuštění** – simulaci lze kdykoliv pozastavit a znovu spustit.
- **Nastavení rychlosti** – rychlost simulace lze měnit za běhu.
- **Předdefinované vzory** – glider, blinker, block.
---
 
## Požadavky
 
- Python 3.8+
- Pygame
```
pygame>=2.0.0
```
 
---
 
## Instalace
 
1. Naklonujte repozitář:
```bash
git clone https://github.com/vase-uzivatelske-jmeno/conways-game-of-life.git
cd conways-game-of-life
```
 
2. (Volitelně) Vytvořte virtuální prostředí:
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```
 
3. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```
 
4. Spusťte simulaci:
```bash
python main.py
```
 
---
 
## Ovládání
 
### Myš
 
| Akce | Popis |
|---|---|
| **Levé tlačítko** | Přepne stav buňky (živá / mrtvá) |
| **Tažení pravým tlačítkem** | Posun po ploše |
 
### Klávesnice
 
| Klávesa | Akce |
|---|---|
| `Space` | Pauza / Spuštění simulace |
| `↑` / `↓` | Zvýšení / snížení rychlosti |
| `R` | Resetování plochy |
| `M` | Změna mezi světlým a tmavým módem |
| `I` | Vypíše nápovědu na obrazovku |
| `1` | Vykreslí glider směrující doprava |
| `2` | Vykreslí glider směrující doleva  |
| `3` | Vykreslí block |
| `4` | Vykreslí blinker |
|`Esc` | Ukončení aplikace |
 
---
 
## Předdefinované vzory
 
### Glider
Pohybující se vzor, který se opakuje každé 4 generace a přitom se posouvá o jedno pole diagonálně.
 
```
. X .
. . X
X X X
```
 
### Blinker
Oscilující vzor s periodou 2 – tři buňky v řadě se střídavě mění na sloupec a zpět.
 
```
X X X
```
 
### Block
Statický vzor (still life) – čtverec 2×2, který se nemění.
 
```
X X
X X
```
 
---
 
## Technické detaily
 
- **Reprezentace mřížky** – mřížka je uložena jako množina (`set`) souřadnic živých buněk. Díky tomu je paměťová náročnost úměrná pouze počtu živých buněk, nikoli celkové ploše.
- **Algoritmus generace** – pro každou generaci se procházejí živé buňky a jejich sousedé, a dle pravidel se vypočítá nový stav.
- **Vykreslování** – vykresluje se pouze viditelná část mřížky; bílá = mrtvá buňka, černá = živá buňka.
- **Viewport** – offset zobrazení se mění při pohybu, čímž vzniká iluze nekonečné plochy.
---