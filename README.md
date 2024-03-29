[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


# BzBCodec

# Description

This program is implementation of custom codec applied for images, videos and audio files.
It allows usage of LZW, LZ77, Huffman and Deflate algorithms of compression and player for
playing these files

# Installation

 - For proper usage of mp3 you need to install ffmpeg. Tips on installation:

    * MacOS:
    Run in terminal
    ```
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null
    ```
    ```
    brew install ffmpeg
    ```

    * Unix:
    ```
    $ sudo apt-get install ffmpeg
    ```
 - To install all the necessary libraries for proper work do the following:
    ```
    pip install -r requirements.txt
    ```
# Usage
Note: Current version of the programm supports only png, jpg, mp3, mp4 and mov extensions of the files

To compress your files you should do the following in the terminal:
```
python3 PathToConvert.py PathToFile algorithm
```
 * Algorithm pararameter is optional. Default algorithm is lz77
 * Supported algorithms:
   - lz77
   - lzw
   - deflate
   - huffman

To play your files and show them in our player you should do the following:
```
python3 PathToPlayer.py PathToFile
```
 * File to be played must have one of the following extensions of pur codec:
   - bzbi for image
   - bzbv for video
   - bzba for audio

# Contributing

We are working on expanding our codec to every possible file extension.
Pull requests are welcome. \
For major changes, please open an issue first to discuss what you would like to change.

To create a pull request:

* Fork this repository on GitHub 
* Clone the project to your computer 
* Create a new branch 
* Commit changes to your own branch
* Push your work back up to your forked repository
* Create a pull request so that we can review your changes

# License
[MIT License](https://choosealicense.com/licenses/mit/)


## Credits

* [firstgenius](https://github.com/firstgenius)
* [shevdan](https://github.com/shevdan)
* [bohdanhlovatskyi](https://github.com/bohdanhlovatskyi)
* [michael-2956](https://github.com/michael-2956)
* [bmykhaylivvv](https://github.com/bmykhaylivvv)





[contributors-shield]: https://img.shields.io/github/contributors/UCUBezB/BzBCodec.svg?style=for-the-badge
[contributors-url]: https://github.com/UCUBezB/BzBCodec/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/UCUBezB/BzBCodec.svg?style=for-the-badge
[forks-url]: https://github.com/UCUBezB/BzBCodec/network/members
[stars-shield]: https://img.shields.io/github/stars/UCUBezB/BzBCodec.svg?style=for-the-badge
[stars-url]: https://github.com/UCUBezB/BzBCodec/stargazers
[issues-shield]: https://img.shields.io/github/issues/UCUBezB/BzBCodec.svg?style=for-the-badge
[issues-url]: https://github.com/UCUBezB/BzBCodec/issues
[license-shield]: https://img.shields.io/github/license/UCUBezB/BzBCodec.svg?style=for-the-badge
[license-url]: https://github.com/UCUBezB/BzBCodec/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/yaroslav-brovchenko-247477205/
