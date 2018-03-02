import scipy.ndimage


def asciiify(image,text,threshold=150,repeat=True,mode="normal",color=None):
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
    array = [[1 if all(rgb <= threshold for rgb in c) else 0 for c in row] for row in list(scipy.ndimage.imread(image))]
    mode = mode.split()
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
        i = 0
        cr = len(array)/2
        cc = len(array[0])/2
        if len(mode) > 1:
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
    if color is not None:
        if isinstance(color,dict):
            for char in color:
                string = string.replace(char,"\x1b[{}m{}\x1b[0m".format(color[char],char))
        elif isinstance(color,list):
            table = {}
            i = 0
            for ch in text:
                table[ord(ch)] = "\x1b[{}m{}\x1b[0m".format(color[i],ch)
                i += 1
                if i == len(color): i = 0
            string = string.translate(table)
    return string


color = {
    "R":"0;31;40",
    "A":"0;33;40",
    "I":"0;33;40",
    "N":"0;32;40",
    "B":"0;34;40",
    "O":"0;35;40",
    "W":"0;35;40"
}
# color = ["0;31;40","0;33;40","0;32;40","0;34;40","0;35;40"]
ascii = asciiify("octocat.jpg", "RAINBOW", mode="swirl tl", color=color)

print(ascii)
