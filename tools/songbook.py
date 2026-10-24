"""The Feedback Loop songbook: hand-written songs in scale degrees (0 = tonic, 7 = octave up).

Each song has its own style: tempo, groove (how the songbook page plays the drums and bass; in the game
the drums are the player's), swing, and per section a harmonic rhythm (hr 1 = a chord a bar, hr 2 = two).
Each section has a progression (4 chords, or 8 at hr 2) and a 4-bar melody: three bars, then the 4th bar
twice (open = phrase ends mid-song, closed = it resolves). Notes are [start, degree, length] in 16ths, 4/4. Run this file to check every melody against its chords and write tools/songbook.json,
which the game embeds (see SONGBOOK in index.html).

Check rules (the same as the game's melody writer): a strong note (on a beat, or 4+ sixteenths long)
must be a chord tone; no note may sit a semitone above a chord tone (the b9 rub). Chromatic chord
tones are reached the game's way: a scale tone a semitone away bends onto them (G -> G# over E7).
"""
import json, re, sys
SC = {'major': [0, 2, 4, 5, 7, 9, 11], 'minor': [0, 2, 3, 5, 7, 8, 10]}
RN = {'I': 0, 'II': 2, 'III': 4, 'IV': 5, 'V': 7, 'VI': 9, 'VII': 11}

def chord(sym):
    m = re.match(r'^(b|#)?(VII|VI|IV|V|III|II|I|vii|vi|iv|v|iii|ii|i)(°|maj7|7|sus4|sus2|add9)?$', sym)
    up = m[2] == m[2].upper(); q = m[3] or ''
    iv = [0, 3, 6] if q == '°' else [0, 5, 7] if q == 'sus4' else [0, 2, 7] if q == 'sus2' else [0, 4, 7] if up else [0, 3, 7]
    if q == '7': iv = iv + [10]
    if q == 'maj7': iv = iv + [11]
    if q == 'add9': iv = iv + [14]
    pc = (RN[m[2].upper()] + (-1 if m[1] == 'b' else 1 if m[1] == '#' else 0)) % 12
    return [(pc + i) % 12 for i in iv]

def semi(d, mode): s = SC[mode]; return s[d % 7] + 12 * (d // 7)

def bend(sm, cps, mode):
    pc = sm % 12; s = SC[mode]
    if pc in cps: return sm
    for ct in cps:
        if ct not in s:
            if (pc + 1) % 12 == ct: return sm + 1
            if (pc + 11) % 12 == ct: return sm - 1
    return sm

def R(rhythm, degs):
    assert len(rhythm) == len(degs), (rhythm, degs)
    return [[s, d, l] for (s, l), d in zip(rhythm, degs)]

S = []
def song(name, mode, bpm, groove, sections, big=False, swing=0):
    for sec in sections.values(): sec.setdefault('hr', 1)
    S.append({'name': name, 'mode': mode, 'bpm': bpm, 'groove': groove, 'swing': swing, 'big': big, 'sec': sections})
LONG = [[0, 6], [6, 2], [8, 8]]
Q = [[0, 4], [4, 4], [8, 4], [12, 4]]
L1 = [[0, 16]]
H2 = [[0, 8], [8, 8]]
QQH = [[0, 4], [4, 4], [8, 8]]
E8 = [[i * 2, 2] for i in range(8)]

# 1. motorik synth: long notes and leaps over a pulsing bass
song('NIGHT BUS', 'minor', 104, 'motorik', {
  'verse': {'prog': 'i bVI bIII bVII', 'mel': [R([[0, 8], [8, 6], [14, 2]], [4, 7, 6]), R([[0, 8], [8, 6], [14, 2]], [5, 9, 7]), R([[0, 8], [8, 6], [14, 2]], [4, 6, 4]),
            R([[0, 4], [4, 4], [8, 8]], [3, 1, 1]), R(L1, [3])]},
  'pre': {'prog': 'bVI bVII bVI bVII', 'mel': [R(E8, [7, 9, 12, 9, 7, 9, 12, 9]), R(E8, [8, 10, 13, 10, 8, 10, 13, 10]), R(E8, [9, 12, 14, 12, 9, 12, 14, 12]), R(H2, [13, 10]), R(H2, [13, 10])]},
  'chorus': {'prog': 'i bVII bVI bVII', 'mel': [R([[0, 3], [3, 3], [6, 2], [8, 8]], [7, 11, 9, 11]), R([[0, 3], [3, 3], [6, 2], [8, 8]], [8, 10, 8, 13]), R([[0, 3], [3, 3], [6, 2], [8, 8]], [7, 12, 9, 14]),
             R(QQH, [13, 10, 8]), R(QQH, [13, 10, 13])]},
  'bridge': {'prog': 'iv iv bVI bVI', 'mel': [R(L1, [10]), R(H2, [12, 10]), R(L1, [9]), R(H2, [7, 9]), R(H2, [7, 9])]},
}, big=True)

# 2. disco: repeated-note syncopation, octave pre, two chords a bar in the chorus
SYNC = [[0, 1], [2, 1], [3, 2], [6, 2], [8, 1], [10, 1], [11, 2], [14, 2]]
HK = [[0, 3], [3, 3], [6, 2], [8, 3], [11, 3], [14, 2]]
song('NEON STATIC', 'major', 122, 'disco', {
  'verse': {'prog': 'I vi ii V', 'mel': [R(SYNC, [4, 4, 4, 2, 4, 4, 4, 5]), R(SYNC, [5, 5, 5, 4, 5, 5, 5, 7]), R(SYNC, [5, 5, 5, 3, 5, 5, 5, 8]),
            R([[0, 1], [2, 1], [3, 2], [6, 2], [8, 8]], [4, 4, 4, 6, 4]), R([[0, 1], [2, 1], [3, 2], [6, 2], [8, 8]], [6, 6, 6, 8, 8])]},
  'pre': {'prog': 'IV V iii vi', 'mel': [R(E8, [3, 10, 3, 10, 5, 12, 5, 12]), R(E8, [4, 11, 4, 11, 6, 13, 6, 13]), R(E8, [2, 9, 2, 9, 4, 11, 4, 11]), R(QQH, [5, 9, 12]), R(QQH, [5, 9, 12])]},
  'chorus': {'prog': 'IV V iii vi ii V I I', 'hr': 2, 'mel': [R(HK, [12, 12, 10, 11, 11, 8]), R(HK, [11, 11, 9, 12, 12, 9]), R(HK, [12, 12, 10, 11, 11, 8]),
             R([[0, 6], [6, 2], [8, 8]], [9, 8, 7]), R([[0, 6], [6, 2], [8, 8]], [11, 9, 7])]},
  'bridge': {'prog': 'vi IV vi IV', 'mel': [R([[0, 12], [12, 4]], [9, 7]), R([[0, 12], [12, 4]], [10, 12]), R([[0, 12], [12, 4]], [12, 9]), R(L1, [10]), R(H2, [12, 10])]},
})

# 3. slow ballad: long, singing lines
song('PAPER WALLS', 'major', 72, 'ballad', {
  'verse': {'prog': 'I IV I V', 'mel': [R([[0, 6], [6, 2], [8, 4], [12, 4]], [4, 5, 4, 2]), R([[0, 6], [6, 2], [8, 4], [12, 4]], [5, 7, 5, 3]), R([[0, 6], [6, 2], [8, 4], [12, 4]], [4, 2, 0, 2]),
            R(H2, [1, 4]), R([[0, 6], [6, 2], [8, 8]], [6, 5, 4])]},
  'pre': {'prog': 'vi iii IV V', 'mel': [R([[0, 2], [2, 2], [4, 4], [8, 4], [12, 4]], [5, 7, 9, 7, 5]), R([[0, 2], [2, 2], [4, 4], [8, 4], [12, 4]], [4, 6, 9, 6, 4]),
          R([[0, 2], [2, 2], [4, 4], [8, 4], [12, 4]], [5, 7, 10, 7, 5]), R(H2, [8, 11]), R(H2, [6, 8])]},
  'chorus': {'prog': 'IV V vi I', 'mel': [R([[0, 8], [8, 2], [10, 2], [12, 4]], [12, 10, 9, 10]), R([[0, 8], [8, 2], [10, 2], [12, 4]], [11, 13, 12, 11]),
             R([[0, 8], [8, 2], [10, 2], [12, 4]], [12, 14, 12, 9]), R(L1, [11]), R(H2, [9, 7])]},
  'bridge': {'prog': 'ii V iii vi', 'mel': [R(QQH, [8, 5, 3]), R(QQH, [8, 6, 4]), R(QQH, [9, 6, 4]), R(L1, [7]), R(QQH, [5, 7, 9])]},
})

# 4. punk: shouted short phrases with rests, a chant chorus
song('SIGNAL BLEED', 'minor', 156, 'punk', {
  'verse': {'prog': 'i i bVI bVII', 'mel': [R([[0, 2], [2, 2], [4, 4]], [4, 4, 2]), R([[8, 2], [10, 2], [12, 4]], [4, 4, 7]), R([[0, 2], [2, 2], [4, 4]], [5, 5, 7]),
            R([[8, 2], [10, 2], [12, 4]], [6, 6, 3]), R([[8, 2], [10, 2], [12, 4]], [8, 8, 6])]},
  'pre': {'prog': 'iv iv bVI bVII', 'mel': [R(Q, [7, 7, 10, 10]), R(Q, [10, 10, 12, 12]), R(Q, [12, 12, 14, 14]), R(H2, [13, 13]), R(H2, [13, 13])]},
  'chorus': {'prog': 'i bVII bVI bVII', 'mel': [R([[0, 3], [3, 3], [6, 6], [12, 4]], [11, 11, 9, 7]), R([[0, 3], [3, 3], [6, 6], [12, 4]], [10, 10, 8, 6]),
             R([[0, 3], [3, 3], [6, 6], [12, 4]], [9, 9, 7, 5]), R([[0, 3], [3, 3], [6, 10]], [10, 10, 8]), R([[0, 3], [3, 3], [6, 10]], [10, 10, 13])]},
  'bridge': {'prog': 'bVI bVI bVII bVII', 'mel': [R(L1, [9]), R(H2, [7, 9]), R(L1, [8]), R(H2, [10, 8]), R(H2, [10, 8])]},
})

# 5. half-time anthem: wide range, an octave-leap hook
song('HOUSE LIGHTS', 'major', 76, 'anthem', {
  'verse': {'prog': 'I V vi IV', 'mel': [R(QQH, [2, 4, 7]), R(QQH, [1, 4, 6]), R(QQH, [0, 2, 5]), R(QQH, [0, 3, 5]), R(QQH, [3, 5, 7])]},
  'pre': {'prog': 'IV V IV V', 'mel': [R([[0, 6], [6, 2], [8, 6], [14, 2]], [7, 8, 10, 9]), R([[0, 6], [6, 2], [8, 6], [14, 2]], [8, 9, 11, 10]),
          R([[0, 6], [6, 2], [8, 6], [14, 2]], [10, 11, 12, 11]), R(L1, [11]), R(L1, [11])]},
  'chorus': {'prog': 'I V vi IV', 'mel': [R([[0, 2], [2, 2], [4, 12]], [7, 7, 14]), R([[0, 2], [2, 2], [4, 12]], [8, 8, 13]), R([[0, 2], [2, 2], [4, 12]], [9, 9, 14]),
             R([[0, 2], [2, 2], [4, 4], [8, 8]], [10, 10, 12, 10]), R([[0, 2], [2, 2], [4, 4], [8, 8]], [10, 9, 10, 7])]},
  'bridge': {'prog': 'vi IV I V', 'mel': [R([[0, 8], [8, 4], [12, 4]], [12, 9, 7]), R([[0, 8], [8, 4], [12, 4]], [12, 10, 7]), R([[0, 8], [8, 4], [12, 4]], [11, 9, 7]), R(H2, [11, 8]), R(L1, [13])]},
}, big=True)

# 6. dorian funk: 16th syncopation over i and a major IV
FK = [[0, 1], [1, 1], [3, 1], [6, 2], [10, 1], [11, 3], [14, 2]]
FC = [[0, 2], [2, 1], [3, 3], [6, 2], [8, 2], [10, 1], [11, 3], [14, 2]]
song('GROUND LOOP', 'minor', 100, 'funk', {
  'verse': {'prog': 'i IV i IV', 'mel': [R(FK, [4, 4, 2, 4, 6, 4, 2]), R(FK, [5, 5, 3, 5, 7, 5, 3]), R(FK, [4, 4, 2, 4, 6, 4, 2]),
            R([[0, 1], [1, 1], [3, 1], [6, 2], [8, 8]], [5, 5, 3, 5, 7]), R([[0, 1], [1, 1], [3, 1], [6, 2], [8, 8]], [3, 3, 0, 3, 3])]},
  'pre': {'prog': 'bVII bVII IV IV', 'mel': [R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 4], [12, 4]], [8, 8, 10, 8, 13, 10]), R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 4], [12, 4]], [10, 10, 8, 10, 13, 13]),
          R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 4], [12, 4]], [10, 10, 12, 10, 14, 12]), R(QQH, [12, 10, 7]), R(QQH, [12, 10, 7])]},
  'chorus': {'prog': 'i bVII i IV', 'mel': [R(FC, [11, 11, 9, 7, 9, 9, 7, 4]), R(FC, [10, 10, 8, 6, 8, 8, 6, 3]), R(FC, [11, 11, 9, 7, 9, 9, 11, 14]),
             R([[0, 2], [2, 1], [3, 3], [6, 2], [8, 8]], [12, 12, 10, 7, 7]), R([[0, 2], [2, 1], [3, 3], [6, 2], [8, 8]], [12, 12, 10, 7, 10])]},
  'bridge': {'prog': 'iv bVII iv bVII', 'mel': [R(H2, [10, 7]), R(H2, [10, 8]), R(H2, [12, 10]), R(L1, [13]), R(L1, [13])]},
})

# 7. slow blues shuffle (swung 8ths), lazy phrases with rests
song('LAST CALL', 'minor', 76, 'shuffle', {
  'verse': {'prog': 'i iv i V7', 'mel': [R([[0, 2], [2, 2], [4, 6], [12, 4]], [7, 6, 4, 2]), R([[0, 2], [2, 2], [4, 6], [12, 4]], [5, 6, 7, 5]), R(QQH, [4, 2, 0]),
            R([[0, 2], [2, 2], [4, 6], [12, 4]], [3, 4, 6, 4]), R(QQH, [8, 6, 4])]},
  'pre': {'prog': 'bVI bVI V7 V7', 'mel': [R([[0, 6], [6, 2], [8, 6], [14, 2]], [9, 7, 5, 7]), R([[0, 6], [6, 2], [8, 6], [14, 2]], [12, 9, 7, 9]),
          R([[0, 6], [6, 2], [8, 6], [14, 2]], [11, 10, 8, 10]), R(H2, [13, 11]), R(H2, [13, 11])]},
  'chorus': {'prog': 'iv i bVI V7', 'mel': [R([[0, 3], [3, 3], [6, 2], [8, 8]], [12, 10, 7, 10]), R([[0, 3], [3, 3], [6, 2], [8, 8]], [11, 9, 7, 9]),
             R([[0, 3], [3, 3], [6, 2], [8, 8]], [12, 9, 7, 9]), R([[0, 3], [3, 3], [6, 2], [8, 8]], [11, 10, 8, 6]), R([[0, 3], [3, 3], [6, 2], [8, 8]], [10, 8, 6, 4])]},
  'bridge': {'prog': 'bVI bVII i i', 'mel': [R(L1, [9]), R(L1, [8]), R(H2, [7, 4]), R(L1, [7]), R(L1, [7])]},
}, swing=1)

# 8. reggae one-drop: phrases that start on the off-beat
song('SIDE STAGE', 'major', 74, 'reggae', {
  'verse': {'prog': 'I IV I V', 'mel': [R([[2, 2], [6, 2], [8, 4], [14, 2]], [4, 4, 2, 1]), R([[2, 2], [6, 2], [8, 4], [14, 2]], [5, 5, 3, 4]), R([[2, 2], [6, 2], [8, 4], [14, 2]], [4, 4, 2, 0]),
            R([[2, 2], [6, 2], [8, 8]], [4, 4, 1]), R([[2, 2], [6, 2], [8, 8]], [6, 6, 4])]},
  'pre': {'prog': 'vi vi IV V', 'mel': [R(Q, [5, 7, 9, 7]), R(Q, [9, 7, 5, 7]), R(Q, [5, 7, 10, 7]), R(H2, [8, 11]), R(H2, [8, 11])]},
  'chorus': {'prog': 'I V vi IV', 'mel': [R([[0, 4], [6, 2], [8, 4], [14, 2]], [9, 9, 7, 9]), R([[0, 4], [6, 2], [8, 4], [14, 2]], [8, 8, 6, 8]), R([[0, 4], [6, 2], [8, 4], [14, 2]], [9, 9, 7, 9]),
             R([[0, 4], [6, 2], [8, 8]], [10, 9, 7]), R([[0, 4], [6, 2], [8, 8]], [10, 12, 10])]},
  'bridge': {'prog': 'ii V ii V', 'mel': [R(L1, [8]), R(L1, [6]), R(H2, [8, 5]), R(L1, [4]), R(L1, [4])]},
})

# 9. mixolydian riff rock: a riff verse, a big chorus
RF = [[0, 2], [2, 2], [4, 2], [6, 2], [8, 2], [10, 6]]
song('SOUNDCHECK', 'major', 118, 'rock', {
  'verse': {'prog': 'I bVII IV I', 'mel': [R(RF, [0, 0, 2, 4, 2, 0]), R(RF, [1, 1, 3, 1, 3, 6]), R(RF, [0, 0, 3, 5, 3, 0]),
            R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 8]], [0, 0, 2, 4, 4]), R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 8]], [4, 4, 2, 1, 0])]},
  'pre': {'prog': 'IV IV V V', 'mel': [R(Q, [7, 7, 10, 10]), R(Q, [10, 10, 12, 12]), R(Q, [11, 11, 13, 13]), R(L1, [11]), R(L1, [11])]},
  'chorus': {'prog': 'I bVII IV I', 'mel': [R([[0, 6], [6, 2], [8, 6], [14, 2]], [11, 9, 7, 8]), R([[0, 6], [6, 2], [8, 6], [14, 2]], [10, 8, 8, 10]),
             R([[0, 6], [6, 2], [8, 6], [14, 2]], [12, 10, 7, 9]), R([[0, 6], [6, 2], [8, 8]], [11, 9, 7]), R(L1, [7])]},
  'bridge': {'prog': 'bVI bVII I I', 'mel': [R(H2, [7, 12]), R(H2, [8, 10]), R(H2, [9, 11]), R(H2, [11, 7]), R(H2, [11, 7])]},
})

# 10. dark harmonic minor, half-time: sparse, leaning on the raised 7th
song('DEAD AIR', 'minor', 86, 'halftime', {
  'verse': {'prog': 'i i bVI V7', 'mel': [R(LONG, [0, 1, 2]), R(LONG, [4, 3, 2]), R(LONG, [5, 4, 2]), R(LONG, [6, 4, 1]), R(LONG, [1, 3, 6])]},
  'pre': {'prog': 'iv iv V7 V7', 'mel': [R(Q, [5, 7, 10, 7]), R(Q, [10, 12, 10, 7]), R(Q, [8, 10, 11, 13]), R(L1, [13]), R(L1, [13])]},
  'chorus': {'prog': 'i bVII bVI V7', 'mel': [R([[0, 3], [3, 3], [6, 2], [8, 8]], [14, 11, 9, 11]), R([[0, 3], [3, 3], [6, 2], [8, 8]], [13, 10, 8, 10]),
             R([[0, 3], [3, 3], [6, 2], [8, 8]], [12, 9, 7, 9]), R([[0, 3], [3, 3], [6, 2], [8, 8]], [11, 10, 8, 6]), R([[0, 3], [3, 3], [6, 2], [8, 8]], [11, 8, 10, 11])]},
  'bridge': {'prog': 'bVI bIII iv V7', 'mel': [R(H2, [12, 9]), R(H2, [11, 9]), R(H2, [10, 7]), R(H2, [8, 6]), R(H2, [8, 6])]},
})

# 11. power pop: driving 8ths, two chords a bar in the pre
song('HEADROOM', 'major', 140, 'powerpop', {
  'verse': {'prog': 'I V vi IV', 'mel': [R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 2], [10, 2], [12, 4]], [4, 5, 4, 2, 4, 5, 7]), R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 2], [10, 2], [12, 4]], [4, 5, 4, 1, 4, 5, 6]),
            R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 2], [10, 2], [12, 4]], [5, 7, 5, 2, 5, 7, 9]), R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 8]], [5, 7, 5, 3, 5]), R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 8]], [5, 3, 5, 7, 7])]},
  'pre': {'prog': 'ii iii IV V ii iii IV V', 'hr': 2, 'mel': [R(Q, [8, 5, 9, 6]), R(Q, [10, 7, 11, 8]), R(Q, [12, 8, 11, 9]), R(QQH, [12, 10, 11]), R(QQH, [10, 12, 13])]},
  'chorus': {'prog': 'IV I V vi', 'mel': [R([[0, 2], [2, 2], [4, 4], [8, 2], [10, 2], [12, 4]], [12, 12, 14, 12, 10, 12]), R([[0, 2], [2, 2], [4, 4], [8, 2], [10, 2], [12, 4]], [11, 11, 14, 11, 9, 11]),
             R([[0, 2], [2, 2], [4, 4], [8, 2], [10, 2], [12, 4]], [11, 11, 13, 11, 8, 11]), R([[0, 2], [2, 2], [4, 4], [8, 8]], [12, 12, 14, 12]), R([[0, 2], [2, 2], [4, 4], [8, 8]], [12, 11, 9, 7])]},
  'bridge': {'prog': 'vi IV I V', 'mel': [R(L1, [9]), R(L1, [10]), R(H2, [11, 9]), R(L1, [11]), R(L1, [13])]},
}, big=True)

# 12. epic, half-time: a soaring chorus
song('CURFEW', 'minor', 132, 'epic', {
  'verse': {'prog': 'i bVI bIII bVII', 'mel': [R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 4], [12, 4]], [4, 2, 4, 2, 0, 2]), R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 4], [12, 4]], [5, 4, 2, 0, 2, 5]),
            R([[0, 2], [2, 2], [4, 2], [6, 2], [8, 4], [12, 4]], [4, 6, 4, 2, 4, 6]), R([[0, 4], [4, 12]], [3, 1]), R(QQH, [3, 1, -1])]},
  'pre': {'prog': 'iv bVI bVII bVII', 'mel': [R(QQH, [7, 10, 12]), R(QQH, [9, 12, 14]), R(QQH, [10, 13, 10]), R(L1, [13]), R(L1, [13])]},
  'chorus': {'prog': 'bVI bVII i i', 'mel': [R([[0, 6], [6, 2], [8, 4], [12, 4]], [14, 12, 9, 12]), R([[0, 6], [6, 2], [8, 4], [12, 4]], [13, 10, 8, 10]),
             R([[0, 6], [6, 2], [8, 4], [12, 4]], [11, 9, 7, 9]), R(QQH, [9, 11, 14]), R(L1, [7])]},
  'bridge': {'prog': 'iv iv V7 V7', 'mel': [R(L1, [10]), R(H2, [12, 10]), R(L1, [11]), R(H2, [8, 13]), R(H2, [8, 13])]},
}, big=True)

def check():
    bad = 0
    for sg in S:
        for role, sec in sg['sec'].items():
            prog = sec['prog'].split(); mel = sec['mel']; hr = sec['hr']
            assert len(prog) == 4 * hr and len(mel) == 5, (sg['name'], role)
            for bi, bar in enumerate(mel):
                end = 0
                for s0, d, l in bar:
                    assert s0 >= end, (sg['name'], role, bi, 'overlap'); end = s0 + l
                    assert end <= 16, (sg['name'], role, bi, 'past bar')
                    sym = prog[min(bi, 3) * hr + (1 if hr == 2 and s0 >= 8 else 0)]; cps = chord(sym)
                    pc = bend(semi(d, sg['mode']), cps, sg['mode']) % 12
                    strong = s0 % 4 == 0 or l >= 4
                    if strong and pc not in cps:
                        print(f"{sg['name']} {role} bar {bi+1} @{s0}: degree {d} not a chord tone of {sym}"); bad += 1
                    if pc not in cps and any((pc - c) % 12 == 1 for c in cps):
                        print(f"{sg['name']} {role} bar {bi+1} @{s0}: degree {d} rubs a semitone above {sym}"); bad += 1
                    if not -2 <= d <= 14: print(f"{sg['name']} {role} bar {bi+1}: degree {d} out of range"); bad += 1
    return bad

if __name__ == '__main__':
    n = check()
    print(f'{len(S)} songs, {n} problems')
    json.dump(S, open(__file__.replace('.py', '.json'), 'w'), separators=(',', ':'))
    sys.exit(1 if n else 0)
