![logo image](https://github.com/puffyboa/ascii-magic/raw/screenshots/ascii-magic-ascii.png)


# ascii-magic
Generate ascii art filled with specified text in the shape of an image

## Usage
```
usage: main.py [-h] [-i IMAGE] [-t THRESHOLD] [--no-repeat] [-m MODE]
               [-c COLOR] [-r]
               text [text ...]

positional arguments:
  text                  text to fill the ascii art

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        image to convert to ascii
  -t THRESHOLD, --threshold THRESHOLD
                        rgb color values under this threshold will be filled
  --no-repeat           should it repeat the text
  -m MODE, --mode MODE  change how the letters are arranged
  -c COLOR, --color COLOR
                        can be a list of color palette values, or a dictionary
                        assigning letters to colors (for XTerm/ANSI-compatible
                        terminals)
  -r, --reverse         reverse the colors order
```
Here, we are making a rainbow-colored octocat ascii image, filled with "ROYGBIV" and colored appropriately:
```
python3 main.py ROYGBIV -c red,orange,yellow,green,blue,blueviolet,violet -m swirl=tl -i octocat.jpg
```
![octocat ascii](https://github.com/puffyboa/ascii-magic/raw/screenshots/octo-ascii.png)

