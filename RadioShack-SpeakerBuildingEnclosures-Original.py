#!/usr/bin/env python3
"""
LOUDSPEAKER DESIGN PROGRAMS
Written by Robert L. Caudle (TRS-80 BASIC)
Based on the equations of D.B. Keele and Richard Small

Python port of the BASIC listing in "Fig. D-3" (Radio Shack, Speaker Building
and Enclosures).  Original BASIC line numbers are noted in comments.

Differences from the TRS-80 original:
  * LPRINT output is appended to a text file (PRINTER_FILE) instead of a printer.
  * The SET() pixel graph is drawn as an ASCII plot in the terminal.
  * Answers of "y" or "Y" are both accepted.
"""

import math
import os

PRINTER_FILE = "speaker_printout.txt"

FREQS = list(range(20, 201, 5))          # FOR F=20 TO 200 STEP 5
TICK_FREQS = [30, 40, 50, 60, 70, 80, 90, 100, 200]          # DATA line 2110
PRINT_FREQS = [20, 30, 40, 45, 50, 60, 80, 100, 120, 140, 160, 200]  # DATA 2115


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def cls():
    os.system("cls" if os.name == "nt" else "clear")


def title(col, text):
    """PRINT TAB(col)"text":PRINT:PRINT"""
    print(" " * col + text)
    print()
    print()


def num(x):
    """Format a number roughly the way BASIC prints it."""
    return f"{x:.6g}"


def ask_float(prompt):
    while True:
        try:
            return float(input(prompt + " ").strip())
        except ValueError:
            print("?REDO FROM START")


def ask_yes(prompt):
    return input(prompt + " ").strip().upper() == "Y"


def lprint(text=""):
    with open(PRINTER_FILE, "a") as fh:
        fh.write(text + "\n")


def tabline(items):
    """Build a line from (column, text) pairs, like LPRINT TAB(n)"text"..."""
    s = ""
    for col, text in items:
        s = s.ljust(col) + text
    return s


def log10(x):
    return math.log(x) / math.log(10)


# --------------------------------------------------------------------------
# Response graph (BASIC subroutine at line 1900)
# --------------------------------------------------------------------------
def draw_graph(m):
    """Show the response graph. m is a dict {freq: dB}."""
    cls()
    top_db, bottom_db, db_per_row = 10.0, -25.0, 2.5
    rows = int(round((top_db - bottom_db) / db_per_row)) + 1
    width = 61
    grid = [[" "] * width for _ in range(rows)]

    # Frequency tick marks along the bottom axis (lines 2030-2060)
    axis = ["-"] * width
    for j in TICK_FREQS:
        axis[int(round(log10(j / 20) * (width - 1)))] = "+"
    axis[0] = "+"

    # Plot the response (lines 2070-2100); values below -25 dB are clamped
    for f in FREQS:
        if m[f] < -25:
            m[f] = -25
        db = min(m[f], top_db)
        r = int(round((top_db - db) / db_per_row))
        c = int(round(log10(f / 20) * (width - 1)))
        grid[r][c] = "*"

    print("RESPONSE GRAPH      (5 DB PER DIV)")
    print()
    for i, row in enumerate(grid):
        db = top_db - i * db_per_row
        label = f"{db:+5.0f} DB" if db % 5 == 0 else "       "
        print(f"{label} |{''.join(row)}")
    print("       +" + "".join(axis))
    print(" " * 8 + "20" + " " * 26 + "HZ" + " " * 29 + "200")
    print()

    if ask_yes("LINE PRINT (Y) "):                    # line 2120
        # Printer plot (lines 2150-2250)
        lprint(tabline([(9, "-40"), (19, "-30"), (29, "-20"),
                        (39, "-10"), (50, "0"), (59, "+10")]))
        lprint(tabline([(10, "+"), (20, "+"), (30, "+"),
                        (40, "+"), (50, "+"), (60, "+")]))
        for f in PRINT_FREQS:
            line = tabline([(0, str(f)), (9, "I")])
            if m[f] < -39:
                lprint(line)
            else:
                lprint(tabline([(0, line), (int(round(50 + m[f])), "*")]))
        input("PRESS ENTER TO CONTINUE ")


# --------------------------------------------------------------------------
# 1. Driver parameters (lines 140-520)
# --------------------------------------------------------------------------
def driver_parameters():
    while True:
        cls()
        title(23, "DRIVER PARAMETERS")
        d = input("ENTER DRIVER NAME ")
        re_ = ask_float("ENTER D.C. RESISTANCE OF VOICE COIL")
        fs = ask_float("ENTER FREE-AIR RESONANCE")
        zmax = ask_float("ENTER IMPEDANCE AT FREE-AIR RESONANCE")
        ro = zmax / re_                                   # 200
        rf = math.sqrt(ro) * re_                          # 210
        f1 = ask_float(f"ENTER FREQ. BELOW FREE-AIR = {num(rf)} OHMS")
        f2 = ask_float(f"ENTER FREQ. ABOVE FREE-AIR = {num(rf)} OHMS")
        qms = fs * math.sqrt(ro) / (f2 - f1)              # 260
        qes = qms / (ro - 1)                              # 270
        qts = qms * qes / (qms + qes)                     # 280
        tvb = ask_float("ENTER TEST BOX VOLUME")
        tfs = ask_float("ENTER DRIVER RESONANCE IN TEST BOX")
        vas = tvb * (1.149 * ((tfs / fs) ** 2 - 1))       # 310

        cls()
        title(23, "DRIVER PARAMETERS")
        print(d)
        print(f"VOICE COIL RESISTANCE(RE)= {num(re_)} OHMS")
        print(f"FREE-AIR RESONANCE(FS)= {num(fs)} HZ")
        print(f"QMS= {num(qms)}")
        print(f"QES= {num(qes)}")
        print(f"QTS= {num(qts)}")
        print(f"VAS= {num(vas)}")
        print()
        if ask_yes("LINE PRINT OUTPUT (Y) "):
            lprint(" " * 23 + "DRIVER PARAMETERS")
            lprint(); lprint(); lprint()
            lprint(d)
            lprint(f"VOICE COIL RESISTANCE (RE)= {num(re_)} OHMS")
            lprint(f"FREE-AIR RESONANCE (FS)= {num(fs)} HZ")
            lprint(f"QMS= {num(qms)}")
            lprint(f"QES= {num(qes)}")
            lprint(f"QTS= {num(qts)}")
            lprint(f"VAS= {num(vas)}")
        if not ask_yes("ANOTHER DRIVER (Y)"):
            return


# --------------------------------------------------------------------------
# 2. Vented box design (lines 530-1360)
# --------------------------------------------------------------------------
def vented_response(qts, vas, vb, fs, fb):
    """Response calculation, lines 1030-1130."""
    a = (fb ** 2) / (fs ** 2)
    b = a / qts + (fb / (7 * fs))
    c = 1 + a + (fb / (7 * fs * qts)) + (vas / vb)
    d = 1 / qts + (fb / (7 * fs))
    m = {}
    for f in FREQS:
        f9 = f / fs
        f5 = f9 ** 2
        f4 = f9 ** 4
        f3 = f9 ** 3
        f6 = (f4 - c * f5 + a) ** 2
        f7 = (b * f9 - d * f3) ** 2
        m[f] = 20 * log10(f4 / (f6 + f7) ** 0.5)
    return m


def vented_new_box(qts, vas, fs, vb):
    """Lines 700-730: new box volume -> retuned B4 numbers."""
    fb = fs * (vas / vb) ** 0.32
    fh = fs * math.sqrt(vas / vb)
    h = 20 * log10(2.6 * qts * (vas / vb) ** 0.35)
    return fb, fh, h


def custom_vented_design(d, qts, vas, fs, vb, fb):
    """Lines 940-1340 (custom vented box)."""
    while True:
        cls()
        title(20, "CUSTOM VENTED BOX DESIGN")
        if ask_yes("CHANGE VB (Y)"):
            vb = ask_float("ENTER NEW VB")
        if ask_yes("CHANGE BOX TUNING (Y)"):
            fb = ask_float("ENTER NEW FB")
        print("GRAPHICS CALCULATION IN PROGRESS")
        draw_graph(vented_response(qts, vas, vb, fs, fb))

        cls()
        title(20, "CUSTOM VENTED BOX DESIGN")
        print(d)
        print(f"VB= {num(vb)}")
        print(f"FB= {num(fb)} HZ")
        print(f"QTS= {num(qts)}")
        print(f"FS= {num(fs)} HZ")
        print(f"VAS= {num(vas)}")
        print()
        if ask_yes("CHANGE VB OR FB (Y)"):
            continue
        if ask_yes("LINE PRINT OUTPUT (Y)"):
            lprint(" " * 20 + "CUSTOM VENTED BOX DESIGN")
            lprint(); lprint()
            lprint(d)
            lprint(f"VB= {num(vb)}")
            lprint(f"FB= {num(fb)} HZ")
            lprint(f"QTS= {num(qts)}")
            lprint(f"FS= {num(fs)} HZ")
            lprint(f"VAS= {num(vas)}")
        return


def vented_box_design():
    while True:
        cls()
        title(23, "VENTED BOX DESIGN")
        d = input("DRIVER NAME ")
        qts = ask_float("ENTER QTS")
        vas = ask_float("ENTER VAS")
        fs = ask_float("ENTER FS")
        vb = 15 * qts ** 2.87 * vas                       # 590  (B4 alignment)
        fb = 0.42 * qts ** -0.9 * fs                      # 600
        fh = 0.26 * qts ** -1.4 * fs                      # 610
        h = 0.0

        cls()
        title(25, "B4-ALIGNMENT")
        print(f"VB= {num(vb)}")
        print(f"FB= {num(fb)} HZ")
        print(f"F3= {num(fh)} HZ")
        print()
        if ask_yes("CHANGE BOX SIZE (Y)"):
            vb = ask_float("ENTER NEW VB ")
            fb, fh, h = vented_new_box(qts, vas, fs, vb)

        while True:                                       # label 740
            cls()
            title(23, "VENTED BOX DESIGN")
            print(d)
            print(f"VB= {num(vb)}")
            print(f"FB= {num(fb)} HZ")
            print(f"F3= {num(fh)} HZ")
            print(f"PEAK OR DIP IN RESPONSE = {num(h)} DB")
            print()
            if ask_yes("CHANGE BOX SIZE (Y)"):
                vb = ask_float("ENTER NEW VB ")
                fb, fh, h = vented_new_box(qts, vas, fs, vb)
                continue
            if ask_yes("LINE PRINT OUTPUT (Y)"):
                lprint(" " * 23 + "VENTED BOX DESIGN")
                lprint(); lprint()
                lprint(d)
                lprint(f"VB= {num(vb)}")
                lprint(f"FB= {num(fb)} HZ")
                lprint(f"F3= {num(fh)} HZ")
                lprint(f"PEAK OR DIP IN RESPONSE= {num(h)} DB")
            if ask_yes("VENTED BOX RESPONSE GRAPH (Y)"):
                print("GRAPHICS CALCULATION IN PROGRESS")
                draw_graph(vented_response(qts, vas, vb, fs, fb))
                continue
            if ask_yes("CUSTOM DESIGN (Y)"):
                custom_vented_design(d, qts, vas, fs, vb, fb)
            break

        if not ask_yes("ANOTHER VENTED BOX DESIGN (Y)"):
            return


# --------------------------------------------------------------------------
# 3. Closed box design (lines 1370-1890)
# --------------------------------------------------------------------------
def closed_box_design():
    while True:
        cls()
        title(23, "CLOSED BOX DESIGN")
        d = input("DRIVER NAME ")
        qs = ask_float("ENTER QTS")
        vas = ask_float("ENTER VAS")
        fs = ask_float("ENTER FS")
        vb = ask_float("ENTER VB")

        while True:                                       # label 1440
            a = vas / vb
            fc = fs * math.sqrt(a + 1)                    # 1450
            qtc = (fc * qs) / fs                          # 1460
            k = 1 / qtc ** 2 - 2
            f3 = fc * math.sqrt((k + math.sqrt(k ** 2 + 4)) / 2)   # 1470
            cls()
            title(23, "CLOSED BOX DESIGN")
            print(d)
            print(f"F3= {num(f3)} HZ")
            print(f"QTC= {num(qtc)}")
            print(f"VB= {num(vb)}")
            print()
            if ask_yes("CHANGE BOX SIZE (Y)"):
                vb = ask_float("ENTER NEW VB ")
                continue
            break

        while True:                                       # label 1570
            cls()
            title(23, "CLOSED BOX DESIGN")
            print(d)
            print(f"QTS= {num(qs)}")
            print(f"QTC= {num(qtc)}")
            print(f"VAS= {num(vas)}")
            print(f"VB= {num(vb)}")
            print(f"FS= {num(fs)} HZ")
            print(f"ALPHA= {num(a)}")
            print(f"FC= {num(fc)} HZ")
            print(f"F3= {num(f3)} HZ")
            print()
            if ask_yes("LINE PRINT OUTPUT (Y)"):
                lprint(" " * 22 + "CLOSED BOX DESIGN")
                lprint(); lprint()
                lprint(f"QTS= {num(qs)}")
                lprint(f"QTC= {num(qtc)}")
                lprint(f"VAS= {num(vas)}")
                lprint(f"VB = {num(vb)}")
                lprint(f"FS= {num(fs)} HZ")
                lprint(f"ALPHA= {num(a)}")
                lprint(f"FC= {num(fc)} HZ")
                lprint(f"F3= {num(f3)} HZ")
            print()
            if ask_yes("CLOSED BOX RESPONSE GRAPH (Y)"):
                print("GRAPHICS CALCULATION IN PROGRESS")
                m = {}
                for f in FREQS:                           # 1810-1840
                    fh = f / fc
                    fq = fh ** 2
                    mag = fq / math.sqrt((fq - 1) ** 2 + (fh / qtc) ** 2)
                    m[f] = 20 * log10(mag)
                draw_graph(m)
                continue
            break

        if not ask_yes("ANOTHER CLOSED BOX DESIGN (Y)"):
            return


# --------------------------------------------------------------------------
# Main menu (lines 30-130)
# --------------------------------------------------------------------------
def main():
    while True:
        cls()
        title(15, "LOUDSPEAKER SYSTEM DESIGN PROGRAMS")
        print("1. DRIVER PARAMETERS")
        print("2. VENTED BOX DESIGN")
        print("3. CLOSED BOX DESIGN")
        print("4. END")
        print()
        choice = input("SELECTION (1-4) > ").strip()
        if choice == "1":
            driver_parameters()
        elif choice == "2":
            vented_box_design()
        elif choice == "3":
            closed_box_design()
        elif choice == "4":
            return


if __name__ == "__main__":
    main()
