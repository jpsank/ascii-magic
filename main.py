import scipy.ndimage
import re
import argparse

# A;B;C;D
# A is 38
# B is 5
# C is a number 1-255
# D: 0=white, 1=bright, 2=dark, 3=normal, 4=underline, 5=blinking 6=normal 7=highlight 8=invisible

ANSI_COLORS = {
  "black": "0",
  "maroon": "1",
  "green": "2",
  "olive": "3",
  "navy": "4",
  "purple": "5",
  "teal": "6",
  "silver": "7",
  "grey": "8",
  "red": "9",
  "lime": "10",
  "yellow": "11",
  "blue": "12",
  "fuchsia": "13",
  "aqua": "14",
  "white": "15",
  "grey0": "16",
  "navyblue": "17",
  "darkblue": "18",
  "blue3": "20",
  "blue1": "21",
  "darkgreen": "22",
  "deepskyblue4": "25",
  "dodgerblue3": "26",
  "dodgerblue2": "27",
  "green4": "28",
  "springgreen4": "29",
  "turquoise4": "30",
  "deepskyblue3": "32",
  "dodgerblue1": "33",
  "green3": "40",
  "springgreen3": "41",
  "darkcyan": "36",
  "lightseagreen": "37",
  "deepskyblue2": "38",
  "deepskyblue1": "39",
  "springgreen2": "47",
  "cyan3": "43",
  "darkturquoise": "44",
  "turquoise2": "45",
  "green1": "46",
  "springgreen1": "48",
  "mediumspringgreen": "49",
  "cyan2": "50",
  "cyan1": "51",
  "darkred": "88",
  "deeppink4": "125",
  "purple4": "55",
  "purple3": "56",
  "blueviolet": "57",
  "orange4": "94",
  "grey37": "59",
  "mediumpurple4": "60",
  "slateblue3": "62",
  "royalblue1": "63",
  "chartreuse4": "64",
  "darkseagreen4": "71",
  "paleturquoise4": "66",
  "steelblue": "67",
  "steelblue3": "68",
  "cornflowerblue": "69",
  "chartreuse3": "76",
  "cadetblue": "73",
  "skyblue3": "74",
  "steelblue1": "81",
  "palegreen3": "114",
  "seagreen3": "78",
  "aquamarine3": "79",
  "mediumturquoise": "80",
  "chartreuse2": "112",
  "seagreen2": "83",
  "seagreen1": "85",
  "aquamarine1": "122",
  "darkslategray2": "87",
  "darkmagenta": "91",
  "darkviolet": "128",
  "purple2": "129",
  "lightpink4": "95",
  "plum4": "96",
  "mediumpurple3": "98",
  "slateblue1": "99",
  "yellow4": "106",
  "wheat4": "101",
  "grey53": "102",
  "lightslategrey": "103",
  "mediumpurple": "104",
  "lightslateblue": "105",
  "darkolivegreen3": "149",
  "darkseagreen": "108",
  "lightskyblue3": "110",
  "skyblue2": "111",
  "darkseagreen3": "150",
  "darkslategray3": "116",
  "skyblue1": "117",
  "chartreuse1": "118",
  "lightgreen": "120",
  "palegreen1": "156",
  "darkslategray1": "123",
  "red3": "160",
  "mediumvioletred": "126",
  "magenta3": "164",
  "darkorange3": "166",
  "indianred": "167",
  "hotpink3": "168",
  "mediumorchid3": "133",
  "mediumorchid": "134",
  "mediumpurple2": "140",
  "darkgoldenrod": "136",
  "lightsalmon3": "173",
  "rosybrown": "138",
  "grey63": "139",
  "mediumpurple1": "141",
  "gold3": "178",
  "darkkhaki": "143",
  "navajowhite3": "144",
  "grey69": "145",
  "lightsteelblue3": "146",
  "lightsteelblue": "147",
  "yellow3": "184",
  "darkseagreen2": "157",
  "lightcyan3": "152",
  "lightskyblue1": "153",
  "greenyellow": "154",
  "darkolivegreen2": "155",
  "darkseagreen1": "193",
  "paleturquoise1": "159",
  "deeppink3": "162",
  "magenta2": "200",
  "hotpink2": "169",
  "orchid": "170",
  "mediumorchid1": "207",
  "orange3": "172",
  "lightpink3": "174",
  "pink3": "175",
  "plum3": "176",
  "violet": "177",
  "lightgoldenrod3": "179",
  "tan": "180",
  "mistyrose3": "181",
  "thistle3": "182",
  "plum2": "183",
  "khaki3": "185",
  "lightgoldenrod2": "222",
  "lightyellow3": "187",
  "grey84": "188",
  "lightsteelblue1": "189",
  "yellow2": "190",
  "darkolivegreen1": "192",
  "honeydew2": "194",
  "lightcyan1": "195",
  "red1": "196",
  "deeppink2": "197",
  "deeppink1": "199",
  "magenta1": "201",
  "orangered1": "202",
  "indianred1": "204",
  "hotpink": "206",
  "darkorange": "208",
  "salmon1": "209",
  "lightcoral": "210",
  "palevioletred1": "211",
  "orchid2": "212",
  "orchid1": "213",
  "orange": "214",
  "sandybrown": "215",
  "lightsalmon1": "216",
  "lightpink1": "217",
  "pink1": "218",
  "plum1": "219",
  "gold1": "220",
  "navajowhite1": "223",
  "mistyrose1": "224",
  "thistle1": "225",
  "yellow1": "226",
  "lightgoldenrod1": "227",
  "khaki1": "228",
  "wheat1": "229",
  "cornsilk1": "230",
  "grey100": "231",
  "grey3": "232",
  "grey7": "233",
  "grey11": "234",
  "grey15": "235",
  "grey19": "236",
  "grey23": "237",
  "grey27": "238",
  "grey30": "239",
  "grey35": "240",
  "grey39": "241",
  "grey42": "242",
  "grey46": "243",
  "grey50": "244",
  "grey54": "245",
  "grey58": "246",
  "grey62": "247",
  "grey66": "248",
  "grey70": "249",
  "grey74": "250",
  "grey78": "251",
  "grey82": "252",
  "grey85": "253",
  "grey89": "254",
  "grey93": "255"
}
prefix = "38;5;"
ANSI_COLORS = {c: prefix + ANSI_COLORS[c] for c in ANSI_COLORS}

ANSI_RESET = u"\u001b[0m"


def asciiify(text,image=None,threshold=120,repeat=True,mode="normal",color=None):
    """
    return ascii of image filled with text
    :param image: image to convert to ascii
    :param text: text to fill the ascii art
    :param threshold: rgb color values under this threshold will be filled
    :param repeat: should it repeat the text
    :param mode: change how the letters are arranged
    :param color: can be a list of color palette values, or a dictionary assigning letters to colors (for XTerm/ANSI-compatible terminals)
    :return:
    """
    text = list(text)
    if color is not None:
        if isinstance(color,str):
            if color in ANSI_COLORS: color = ANSI_COLORS[color]
            text = list("\u001b[{}m".format(color)+''.join(text)+ANSI_RESET)
        elif isinstance(color,dict):
            color = {c: ANSI_COLORS[color[c]] if color[c] in ANSI_COLORS else color[c] for c in color}
            text = ["\u001b[{}m{}{}".format(color[c],c,ANSI_RESET) if c in color else c for c in text]
        elif isinstance(color,list):
            color = [ANSI_COLORS[c] if c in ANSI_COLORS else c for c in color]
            if repeat:
                orig = text[:]
                while len(text) % len(color) != 0: text += orig
            l = len(color)
            for i in range(len(text)):
                if i >= len(color): color.append(color[i-l])
                text[i] = "\u001b[{}m{}{}".format(color[i],text[i],ANSI_RESET)

    if image:
        array = [[1 if all(rgb <= threshold for rgb in c) else 0 for c in row] for row in list(scipy.ndimage.imread(image))]
    else:
        array = [[1 for _ in range(40)] for _ in range(40)]
    mode = mode.split("=")
    if mode[0] == "normal":
        i = 0
        for r,row in enumerate(array):
            for c,col in enumerate(row):
                if repeat and i >= len(text):
                    i = 0
                if i < len(text) and col == 1:
                    array[r][c] = text[i]
                    i += 1
    elif mode[0] == "diagonal":
        i = 0
        j = 0
        for r,row in enumerate(array):
            fit = text[j:j+len(array[0])]
            for c,col in enumerate(row):
                if repeat and i >= len(fit):
                    i -= len(fit)
                if i < len(fit) and col == 1:
                    array[r][c] = fit[i]
                i += 1
            j += 1
    elif mode[0] == "swirl":
        cr = len(array)/2
        cc = len(array[0])/2
        if len(mode) > 1:
            if re.match(r"\d+,\d+",mode[1]):
                cr,cc = [int(t) for t in mode[1].split(",")]
            else:
                if "t" in mode[1]:
                    cr = 0
                if "b" in mode[1]:
                    cr = len(array)-1
                if "l" in mode[1]:
                    cc = 0
                if "r" in mode[1]:
                    cc = len(array[0])-1

        for r,row in enumerate(array):
            for c,col in enumerate(row):
                if col == 1:
                    dist = int(((r-cr)**2+(c-cc)**2)**.5)
                    while dist >= len(text):
                        dist -= len(text)
                    array[r][c] = text[dist]
    string = '\n'.join([' '.join([" " if c is 0 else str(c) for c in row]) for row in array])
    return string


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("text",nargs="+",type=str,help="text to fill the ascii art")
    parser.add_argument("-i","--image",dest="image",help="image to convert to ascii")
    parser.add_argument("-t","--threshold", type=int, dest="threshold", default=120, help="rgb color values under this threshold will be filled")
    parser.add_argument("--no-repeat", action="store_false", dest="repeat", default=True, help="should it repeat the text")
    parser.add_argument("-m", "--mode", dest="mode", default="normal", help="change how the letters are arranged")
    parser.add_argument("-c", "--color", dest="color", help="can be a list of color palette values, or a dictionary assigning letters to colors (for XTerm/ANSI-compatible terminals)")
    parser.add_argument("-r", "--reverse", dest="reverse", action="store_true", default=False, help="reverse the colors order")
    args = parser.parse_args()

    color = args.color.split(",") if args.color is not None else args.color
    if args.reverse and isinstance(color,list): color = list(reversed(color))
    ascii = asciiify(' '.join(args.text), image=args.image, threshold=args.threshold, repeat=args.repeat, mode=args.mode,color=color)

    # "swirl=21,67" "red,yellow,green,blue,purple"

    print(ascii)
