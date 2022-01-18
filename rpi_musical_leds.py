"""
This project will play songs in realtime using a tonal (passive) buzzer and will show the song notes lighting up through an LED bar!

This script includes ten common songs to play. You can add your own below as long as you follow the structuring. To assist in creating a song, you can use this python script to help make them:

https://github.com/hexadeci-male/dumptruck/blob/main/python/musical_timing_recorder.py

Required parts:
- RPI 40-pin GPIO
- Breadboard
- LED bar (10 LEDs)
- Passive Buzzer
- Wires and resistors
"""

from gpiozero import LEDBarGraph,TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
import os

DEBUG = False
LEDCOUNT = 10
ledbar = LEDBarGraph(19, 13, 25, 22, 27, 24, 23, 18, 17, 12)
buzzer = TonalBuzzer(26,octaves=4)

# Songs
# Song structure:
# >Notes
# >Duration of a note
# >Pause time after note
doeraemee = [
    [
        "C4","D4","E4","F4","G4","A4","B4","C5",
    ],
    [
        0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,
    ],
    [
        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
    ]
]

birthday = [
    [
        "D4","D4","E4","D4","G4","F#4",
        "D4","D4","E4","D4","A4","G4",
        "D4","D4","D5","B4","G4","F#4","E4",
        "C5","C5","B4","G4","A4","G4",

    ],
    [
        0.200,0.100,0.339,0.223,0.239,0.511,
        0.200,0.100,0.339,0.223,0.239,0.511,
        0.142,0.079,0.495,0.367,0.399,0.399,0.511,
        0.200,0.100,0.339,0.223,0.239,0.511,
    ],
    [
        0.100,0.112,0.269,0.320,0.320,0.591,
        0.100,0.112,0.269,0.320,0.320,0.591,
        0.239,0.112,0.176,0.224,0.144,0.176,0.511,
        0.100,0.112,0.269,0.320,0.320,0.591,
    ]
]

twinkle = [
    [
        "G4","G4","D5","D5","E5","E5","D5",
        "C5","C5","B4","B4","A4","A4","G4",
        "D5","D5","C5","C5","B4","B4","A4",
        "D5","D5","C5","C5","B4","B4","A4",
        "G4","G4","D5","D5","E5","E5","D5",
        "C5","C5","B4","B4","A4","A4","G4",
    ],
    [
        0.261,0.342,0.382,0.328,0.289,0.241,0.542,
        0.322,0.281,0.321,0.261,0.321,0.221,0.441,
        0.241,0.261,0.241,0.201,0.241,0.201,0.441,
        0.241,0.261,0.241,0.201,0.241,0.201,0.441,
        0.261,0.342,0.382,0.328,0.289,0.241,0.542,
        0.322,0.281,0.321,0.261,0.321,0.221,0.441,
    ],
    [
        0.150,0.161,0.121,0.147,0.161,0.201,0.423,
        0.181,0.171,0.161,0.160,0.180,0.201,0.604,
        0.221,0.151,0.181,0.181,0.211,0.181,0.304,
        0.221,0.151,0.181,0.181,0.211,0.181,0.304,
        0.150,0.161,0.121,0.147,0.161,0.201,0.423,
        0.181,0.171,0.161,0.160,0.180,0.201,0.604,
    ]
]

yankee = [
    [
        "C5","C5","D5","E5","C5","E5","D5","G4",
        "C5","C5","D5","E5","C5","B4",
        "C5","C5","D5","E5","F5","E5","D5","C5","B4","G4","A4","B4","C5","C5",
        "A4","B4","A4","G4","A4","B4","C5",
        "G4","A4","G4","F4","E4","G4",
        "A4","B4","A4","G4","A4","B4","C5","A4","G4","C5","B4","D5","C5","C5",
    ],
    [
        0.141,0.181,0.161,0.161,0.161,0.120,0.116,0.201,
        0.120,0.140,0.161,0.140,0.402,0.301,
        0.140,0.141,0.161,0.181,0.241,0.163,0.185,0.184,0.201,0.181,0.161,0.161,0.382,0.405,
        0.201,0.101,0.261,0.221,0.181,0.181,0.281,
        0.381,0.121,0.201,0.161,0.342,0.341,
        0.281,0.120,0.201,0.241,0.161,0.161,0.181,0.201,0.181,0.239,0.201,0.147,0.376,0.342,
    ],
    [
        0.161,0.120,0.141,0.120,0.161,0.178,0.197,0.141,
        0.181,0.161,0.161,0.141,0.202,0.362,
        0.161,0.161,0.161,0.100,0.136,0.154,0.132,0.160,0.120,0.120,0.140,0.141,0.127,0.341,
        0.221,0.120,0.100,0.121,0.141,0.140,0.221,
        0.181,0.120,0.140,0.161,0.181,0.341,
        0.221,0.100,0.120,0.140,0.201,0.141,0.181,0.161,0.100,0.100,0.142,0.138,0.201,0.000,
    ]
]

lgt = [
    [
        "E4","E4","Eb4","E4","G4",
        "G4","A4","G4",
        "E4","G4","G4","E4","G4","A4","A4","G4",
        "A4","A4","G#4","A4","C5",
        "C5","C5","D5","C5",
        "E4","G4","G4","E4","G4","A4","A4","G4",
        "G4","A4","G4","B4","D5","B4","G4","F4",
        "G4","A4","G4","B4","D5","B4","G4","F4",
        "G4","A4","C5",
        "C5","D5","C5",
    ],
    [
        0.281,0.141,0.125,0.125,0.328,
        0.109,0.187,0.391,
        0.094,0.109,0.109,0.094,0.266,0.141,0.281,0.375,
        0.172,0.141,0.109,0.109,0.422,
        0.125,0.109,0.156,0.391,
        0.125,0.078,0.094,0.094,0.266,0.125,0.250,0.359,
        0.078,0.094,0.094,0.297,0.219,0.208,0.109,0.422,
        0.094,0.109,0.094,0.297,0.203,0.234,0.094,0.469,
        0.078,0.109,0.469,
        0.094,0.297,0.300,
    ],
    [
        0.141,0.109,0.078,0.094,0.281,
        0.109,0.187,0.484,
        0.125,0.109,0.109,0.109,0.156,0.109,0.125,0.531,
        0.234,0.125,0.125,0.109,0.219,
        0.125,0.094,0.109,0.344,
        0.125,0.141,0.125,0.125,0.172,0.109,0.172,0.391,
        0.156,0.109,0.109,0.141,0.187,0.172,0.141,0.359,
        0.125,0.125,0.109,0.172,0.187,0.172,0.109,0.328,
        0.125,0.125,0.313,
        0.156,0.187,0.000,
    ]
]

daysxmas = [
    [
        "C4","C4","C4","F4","F4","F4","E4","F4","G4","A4","A#4","G4","A4",
        "C5","G4","A4","A#4","G4",
        "C5","G4","A4","A#4","G4",
        "C5","G4","A4","A#4","G4",
        "A4","A#4","C5","D5","Bb4","A4","F4","G4","F4",
    ],
    [
        0.161,0.161,0.376,0.161,0.160,0.358,0.153,0.141,0.140,0.160,0.140,0.100,0.281,
        0.370,0.141,0.140,0.141,0.160,
        0.370,0.141,0.140,0.140,0.161,
        0.370,0.140,0.121,0.161,0.161,
        0.100,0.120,0.341,0.181,0.120,0.221,0.151,0.301,0.322,
    ],
    [
        0.140,0.156,0.151,0.150,0.150,0.163,0.140,0.140,0.120,0.141,0.141,0.161,0.382,
        0.141,0.141,0.141,0.141,0.101,
        0.151,0.140,0.161,0.140,0.100,
        0.151,0.161,0.141,0.161,0.101,
        0.140,0.161,0.120,0.121,0.141,0.141,0.141,0.152,0.000,
    ]
]

jingle = [
    [
        "D4","B4","A4","G4","D4",
        "D4","D4","D4","B4","A4","G4","E4",
        "E4","C5","B4","A4","F#4",
        "D5","D5","C5","A4","B4",
        "D4","B4","A4","G4","D4",
        "D4","B4","A4","G4","E4",
        "E4","E4","C5","B4","A4","D5","D5","D5","D5","E5","D5","C5","A4","G4",
        "D5",
        "B4","B4","B4","B4","B4","B4",
        "B4","D5","G4","A4","B4",
        "C5","C5","C5","C5","C5","B4","B4",
        "B4","B4","B4","A4","A4","B4","A4",
        "D5",
        "B4","B4","B4","B4","B4","B4",
        "B4","D5","G4","A4","B4",
        "C5","C5","C5","C5","C5","B4","B4",
        "B4","B4","D5","D5","C5","A4","G4",
    ],
    [
        0.201,0.141,0.181,0.181,0.482,
        0.120,0.060,0.181,0.201,0.181,0.160,0.502,
        0.100,0.120,0.181,0.161,0.482,
        0.160,0.100,0.140,0.100,0.499,
        0.121,0.090,0.141,0.100,0.463,
        0.140,0.140,0.120,0.100,0.442,
        0.120,0.151,0.120,0.121,0.171,0.140,0.161,0.130,0.120,0.106,0.141,0.141,0.120,0.421,
        0.420,
        0.118,0.130,0.381,0.161,0.070,0.362,
        0.159,0.161,0.342,0.060,0.703,
        0.118,0.120,0.382,0.050,0.161,0.167,0.201,
        0.100,0.100,0.137,0.161,0.161,0.160,0.332,
        0.561,
        0.139,0.120,0.372,0.181,0.140,0.343,
        0.139,0.121,0.381,0.120,0.624,
        0.098,0.120,0.321,0.100,0.161,0.141,0.181,
        0.098,0.060,0.623,0.905,0.723,0.723,0.783,
    ],
    [
        0.160,0.101,0.120,0.161,0.362,
        0.140,0.141,0.141,0.141,0.141,0.140,0.382,
        0.181,0.160,0.141,0.161,0.463,
        0.181,0.161,0.161,0.201,0.356,
        0.221,0.141,0.161,0.161,0.342,
        0.151,0.161,0.161,0.140,0.241,
        0.181,0.141,0.161,0.181,0.141,0.140,0.160,0.201,0.201,0.195,0.181,0.201,0.160,0.201,
        0.141,
        0.161,0.161,0.201,0.181,0.181,0.301,
        0.141,0.130,0.161,0.100,0.321,
        0.173,0.161,0.120,0.120,0.141,0.147,0.122,
        0.163,0.116,0.160,0.110,0.140,0.136,0.224,
        0.221,
        0.160,0.181,0.251,0.161,0.180,0.300,
        0.181,0.161,0.120,0.100,0.342,
        0.161,0.181,0.140,0.080,0.141,0.160,0.141,
        0.100,0.101,0.181,0.060,0.040,0.060,0.000,
    ]
]

xmastree = [
    [
        "D4","G4","G4","G4",
        "A4","B4","B4","B4",
        "B4","A4","B4","C5","Gb4","A4","G4",
        "D4","G4","G4","G4",
        "A4","B4","B4","B4",
        "B4","A4","B4","C5","Gb4","A4","G4",
        "D5","D5","B4","E5","D5","D5","C5","C5",
        "C5","C5","A4","D5","C5","C5","B4","B4",
        "D4","G4","G4","G4",
        "A4","B4","B4","B4",
        "B4","A4","B4","C5","Gb4","A4","G4",
    ],
    [
        0.623,0.482,0.121,0.663,
        0.703,0.422,0.140,0.843,
        0.228,0.251,0.301,0.522,0.623,0.542,0.683,
        0.623,0.482,0.121,0.663,
        0.703,0.422,0.140,0.843,
        0.228,0.251,0.301,0.522,0.623,0.542,0.683,
        0.259,0.281,0.301,1.104,0.341,0.623,0.281,0.743,
        0.259,0.281,0.301,1.104,0.341,0.623,0.281,0.743,
        0.623,0.482,0.121,0.663,
        0.703,0.422,0.140,0.843,
        0.228,0.251,0.301,0.522,0.623,0.542,0.683,
    ],
    [
        0.040,0.100,0.121,0.080,
        0.080,0.120,0.100,0.247,
        0.120,0.100,0.080,0.080,0.100,0.100,0.421,
        0.040,0.100,0.121,0.080,
        0.080,0.120,0.100,0.247,
        0.120,0.100,0.080,0.080,0.100,0.100,0.421,
        0.100,0.120,0.100,0.020,0.100,0.100,0.100,0.120,
        0.100,0.120,0.100,0.020,0.100,0.100,0.100,0.120,
        0.040,0.100,0.121,0.080,
        0.080,0.120,0.100,0.247,
        0.120,0.100,0.080,0.080,0.100,0.100,0.000,
    ]
]

nutcracker = [
    [
        "D5","D5","D5","D5","E5","E5","F#5","D5","E5",
        "D5","D5","D5","D5","E5","E5","F#5","D5","E5",
        "E4","C5","D5","C5","B4","A4","G4","Gb4",
        "D4","B4","C5","B4","A4","G4","Gb4","E4",
        "G4","Gb4","E4","Eb4",
        "A4","G4","Gb4","E4",
        "B4","C5","B4","A4","G4","D5","D5",
        "D5","D5","D5","D5","E5","E5","F#5","D5","E5",
        "D5","D5","D5","D5","E5","E5","F#5","D5","E5",
        "E4","C5","D5","C5","B4","A4","G4","Gb4",
        "A4","D5","E5","D5","C5","B4","A4","G4",
        "B4","E5","D5","C5",
        "E5","F#5","E5","D5",
        "F#5","G5","F#5","E5",
        "F#5","G5",
    ],
    [
        0.171,0.060,0.080,0.080,0.130,0.161,0.161,0.141,0.442,
        0.141,0.060,0.080,0.060,0.147,0.163,0.141,0.110,0.441,
        0.060,0.060,0.060,0.100,0.060,0.080,0.060,0.080,
        0.060,0.069,0.060,0.080,0.080,0.100,0.080,0.047,
        0.100,0.080,0.080,0.100,
        0.060,0.080,0.080,0.080,
        0.080,0.060,0.060,0.080,0.060,0.302,0.201,
        0.098,0.098,0.080,0.080,0.100,0.100,0.121,0.100,0.402,
        0.118,0.100,0.060,0.050,0.140,0.221,0.181,0.121,0.382,
        0.098,0.120,0.080,0.080,0.056,0.085,0.038,0.116,
        0.054,0.062,0.062,0.100,0.060,0.080,0.060,0.066,
        0.038,0.100,0.066,0.069,
        0.078,0.100,0.020,0.080,
        0.059,0.080,0.060,0.080,
        0.079,0.500,
    ],
    [
        0.241,0.120,0.100,0.100,0.282,0.282,0.261,0.301,0.433,
        0.272,0.120,0.121,0.101,0.285,0.318,0.321,0.301,0.322,
        0.101,0.241,0.080,0.181,0.080,0.201,0.121,0.281,
        0.094,0.288,0.100,0.241,0.080,0.201,0.086,0.289,
        0.080,0.221,0.121,0.241,
        0.112,0.201,0.100,0.261,
        0.100,0.281,0.120,0.201,0.131,0.181,0.322,
        0.352,0.141,0.101,0.080,0.321,0.322,0.281,0.341,0.403,
        0.301,0.120,0.100,0.121,0.261,0.261,0.262,0.301,0.261,
        0.060,0.221,0.080,0.201,0.078,0.216,0.085,0.260,
        0.100,0.254,0.085,0.273,0.101,0.221,0.100,0.255,
        0.080,0.241,0.078,0.269,
        0.050,0.241,0.121,0.261,
        0.080,0.261,0.100,0.241,
        0.100,0.000,
    ]
]

hark = [
    [
        "A#3","D#4","D#4","D4","D#4","G4","G4","F4",
        "A#4","A#4","A#4","Ab4","G4","F4","G4",
        "Bb3","D#4","D#4","D4","D#4","G4","G4","F4",
        "A#4","F4","F4","Eb4","D4","C4","Bb3",
        "A#4","A#4","A#4","Eb4","G#4","G4","G4","F4",
        "A#4","A#4","A#4","Eb4","G#4","G4","G4","F4",
        "C5","C5","C5","Bb4","Ab4","G4","G#4",
        "F4","G4","G#4","A#4","Eb4","Eb4","F4","G4",
        "C5","C5","C5","Bb4","Ab4","G4","G#4",
        "F4","G4","G#4","A#4","Eb4","Eb4","F4","Eb4",
    ],
    [
        0.325,0.255,0.540,0.115,0.320,0.295,0.240,0.365,
        0.270,0.280,0.440,0.120,0.270,0.260,0.400,
        0.300,0.240,0.480,0.110,0.340,0.260,0.280,0.280,
        0.340,0.220,0.580,0.140,0.420,0.300,0.480,
        0.280,0.300,0.305,0.275,0.380,0.260,0.300,0.360,
        0.360,0.320,0.325,0.315,0.315,0.280,0.240,0.310,
        0.640,0.114,0.405,0.340,0.320,0.299,0.395,
        0.340,0.164,0.136,0.463,0.080,0.337,0.345,0.433,
        0.560,0.180,0.260,0.345,0.280,0.240,0.540,
        0.379,0.080,0.120,0.460,0.081,0.660,0.860,1.205,
    ],
    [
        0.160,0.200,0.240,0.080,0.140,0.180,0.210,0.160,
        0.180,0.200,0.260,0.120,0.180,0.220,0.520,
        0.200,0.220,0.240,0.140,0.140,0.180,0.180,0.240,
        0.140,0.160,0.140,0.070,0.140,0.180,0.470,
        0.220,0.195,0.180,0.155,0.160,0.160,0.140,0.160,
        0.100,0.156,0.140,0.150,0.145,0.195,0.200,0.160,
        0.075,0.075,0.120,0.100,0.116,0.184,0.560,
        0.116,0.100,0.093,0.220,0.100,0.118,0.137,0.460,
        0.120,0.100,0.135,0.120,0.180,0.220,0.340,
        0.141,0.140,0.135,0.219,0.100,0.240,0.135,0.000,
    ]
]

# Song listings
tracks = {
    "Doe Rae Mee":doeraemee,
    "Happy Birthday":birthday,
    "Twinkle Twinkle Little Star":twinkle,
    "Yankee Doodle":yankee,
    "Let's Get Together":lgt,
    "Twelve Days Of Christmas":daysxmas,
    "Jingle Bells":jingle,
    "O Christmas Tree":xmastree,
    "March (The Nutcracker)":nutcracker,
    "Hark! The Herald Angels Sing":hark,
}

# Functions
def clear_screen():
    os.system("cls" if os.name == 'nt' else "clear")

def led_note_range(song_notes,led_count=10):
    # Find lowest through highest notes in song and assign led range mapping for them
    tonal_rank = {"C":0,"D":1,"E":2,"F":3,"G":4,"A":5,"B":6}
    tone_val = lambda x: int(x[-1]) * 10 + tonal_rank[x[0]]
    notes = sorted(set(song_notes),key=tone_val)
    led_vals = []
    l = len(notes)
    for i in range(1,l+1):
        n = round(i/(l/led_count))
        led_vals.append(1 if n == 0 else n)
    return dict(zip(notes,led_vals))

def play_song(song):
    led_range = led_note_range(song[0],LEDCOUNT)
    for i in range(len(song[0])):
        buzzer.play(Tone.from_note(song[0][i]))
        ledbar.value = led_range[song[0][i]]/LEDCOUNT
        sleep(song[1][i])
        buzzer.stop()
        ledbar.value = 0
        sleep(song[2][i])
    sleep(1)

def app():
    while True:
        clear_screen()
        print("Type a number and press 'Enter' to play a song (default is 0), or type in 'Q' to quit.\n")
        song_list = dict(enumerate(tracks))
        for i,song in song_list.items():
            print(f"{i}) - {song}")
        choice = input("\n> ")
        if choice.upper() == "Q": exit()
        try:
            num = int(choice)
            if -1 < num < len(song_list): pass
            else: num = 0
        except: num = 0
        clear_screen()
        print(f"Playing song '{song_list[num]}' - press 'ctrl + c' to quit ...")
        play_song(tracks[song_list[num]])

# Execute
if __name__ == "__main__":
    if not DEBUG:
        try: app()
        # Auto-cleanup of gpio
        except Exception as e: print(e)