**The below are the notes from the Sonnet 5.5 OCR of the photos from the source book that apply to the .BAS file:**

The listing is in page order (pages 181 to 187, lines 10 to 2260) and includes Robert Caudle’s TRS-80 Keele/Small loudspeaker design program.

I made a few transcription choices:

Exponents: the book prints the TRS-80 up-arrow as [ (e.g. QTS[2.87). I wrote these as ^ so the code reads and runs in standard BASIC dialects.
Typos kept as printed: the book’s typos are all preserved, including “DESION” in lines 1270 and 1700, “PEAK OF DIP” in line 890, and the unbalanced parenthesis in line 2200 (IF M(F)<-39) THEN 2230). Line 2200 will need fixing before it runs. This is also why I kept it as an “Original” listing.
Line 1910: the final string is smudged in the photo and looks like 'DIV", so I wrote it as "DIV".
Missing page: the page 183 content (between lines 560 and 570) appears in your photos as continuous, so nothing seems to be missing, but it’s worth a quick check against the book.

**The below are the notes from the Sonnet 5.5 conversion of the original BASIC program to Python**

I converted the program to Python as RadioShack-SpeakerBuildingEnclosures-Original.py. It has the same four-option menu and covers driver parameters, vented box design (including the B4 alignment and custom design) and closed box design. I ran the vented and closed box paths with sample input and they work. I didn’t exercise the driver parameters path.

The conversion keeps the original equations and prompts, and comments mark the BASIC line numbers each section came from. It differs from the BASIC in these ways:

Control flow: the GOTO/GOSUB logic became functions and loops, but the screens appear in the same order.
Printer output: LPRINT now appends to speaker_printout.txt in the folder you run it from, instead of going to a printer.
Graph: the TRS-80 SET() pixel plot is now an ASCII plot in the terminal. It uses the same log frequency axis from 20 to 200 Hz and 5 dB per division, and the printout graph keeps the original layout.
Input: both y and Y are accepted. The original only reliably accepted capitals, and line 970 even compared against lowercase.
Closed-box test case: a driver with QTS 0.4, VAS 50 and FS 30 in a 40-unit box gives FC 45 Hz and F3 54.4 Hz.

The Python is not a bug-for-bug port: the unbalanced parenthesis in BASIC line 2200 has no counterpart, and the typos in the printed text are corrected (for example “DESION” is now “DESIGN”). If you want the repo to have both files, upload the .bas and .py together.
