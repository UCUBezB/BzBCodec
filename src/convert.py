'''
Module for converting files into custom codec using compression algos
'''

import sys
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
from lzw import lzw_compress, lzw_decompress
from Huffman_algo import HuffmanCode
from lz77 import compress
from deflate import Deflate


class Convert:
    '''
    Class for converting files into customly encoded files.
    Currently supports mp3, mp4, png and jpg files

    Attributes
    ----------
    path: str
        path to the file that will be encoded.
        Raises TypeError if path is invalid

    Methods
    -------
    _convert_img(image)
        private method necessary for converting image into numpy array
    save_img()
        compresses the image and creates encoded file
    save_vid()
        compresses the video and creates encoded file
    save_audio()
        compresses the audio and creates encoded file
    save()
        compresses any given file or raises the error if it is unsupported
    '''
    def __init__(self, path: str, compression_type='lz77'):
        if not os.path.exists(path):
            raise TypeError('You must provide a valid path')

        self.path = path
        self.compress = self.compresssion(compression_type)

    def compresssion(self, compression_type):
        if compression_type.lower() == 'lz77':
            return compress
        if compression_type.lower() == 'lzw':
            return lzw_compress
        if compression_type.lower() == 'deflate':
            return Deflate().encode
        if 'huffman' in compression_type.lower():
            return HuffmanCode
        raise ValueError('Unsupported compression. One of the following is supported:\
 lz77, lzw, huffman, deflate')

    def _convert_img(self, image) -> tuple:
        '''
        Private method for converting image into numpy array
        '''
        arr = np.array(image, dtype='uint8')
        shape = np.array(arr.shape, dtype='uint16')

        if self.compress == HuffmanCode:
            flat_arr = self.compress(arr.ravel()).encode()[0]
        else:

            flat_arr = self.compress(arr.ravel())

        return flat_arr, shape

    def save_img(self):
        '''
        compresses the image and creates encoded file
        '''
        img = Image.open(self.path).convert('RGB')
        
        arr, shape = self._convert_img(img)
        img_info = np.array([arr, shape])

        np.savez_compressed(f'{self.path[:-3]}bzbi', info=img_info)
        self.bzb_extension('img')

    def save_vid(self):
        '''
        compresses the video and creates encoded file
        '''
        clip = VideoFileClip(self.path)
        rate = clip.fps
        print(f"Frames num: {clip.reader.nframes}")
        size = clip.size[::-1]
        vid_info = np.array([rate, *size, 3.], dtype = np.int)

        #convert frames of the video into numpy
        frames = []
        cnt_frame = 0
        for frame in clip.iter_frames():
            print(f'Current frame: {cnt_frame}', end= ' \r')
            frame_arr = np.array(frame, dtype='uint8')
            # #insert compression here
            if self.compress == HuffmanCode:
                frame_arr = self.compress(frame.ravel()).encode()[0]
            else:
                frame_arr = self.compress(frame.ravel())

            frames.append(frame_arr)
            cnt_frame += 1

        frames = np.array(frames)

        frames = np.array([frames, vid_info])

        np.savez_compressed(f'{self.path[:-3]}bzbv', info=frames)
        self.bzb_extension('vid')

    def save_audio(self):
        '''
        compresses the audio and creates encoded file
        '''
        sound = AudioSegment.from_file(self.path, format='mp3')
        peak_amplitude = sound.max
        loudness = sound.dBFS
        channels_cnt = sound.channels
        raw = np.array(sound.get_array_of_samples())
        pckg_size = int(sound.frame_rate / (2 * channels_cnt))

        frame_r = sound.frame_rate
        audio_info = np.array([peak_amplitude, channels_cnt, sound.frame_rate, 
                    pckg_size, sound.frame_count()/ sound.frame_rate], dtype=object)


        package = []
        size = pckg_size * channels_cnt
        cnt = 0

        while (cnt + 1) * size < len(raw):

            compressed_package = np.array(raw[(cnt * size) : ((cnt + 1)*size)], dtype='int16')

            compressed_package = self.compress(compressed_package)

            package.append(compressed_package)
            cnt += 1


        
        package = np.array(package)
        audio = np.array([package, audio_info])

        np.savez_compressed(f'{self.path[:-3]}bzba', info=audio)
        self.bzb_extension('audio')


    def bzb_extension(self, type):
        if type == 'img':
            ext = 'bzbi'
        elif type == 'vid':
            ext = 'bzbv'
        else:
            ext = 'bzba'
        os.rename(f'{self.path[:-4]}.{ext}.npz', f'{self.path[:-4]}.{ext}')

    
    def save(self):
        '''
        compresses any given file or raises the error if it is unsupported
        '''
        if self.path.endswith('.jpg') or self.path.endswith('.png'):
            self.save_img()
        elif self.path.endswith('mp4') or self.path.endswith('mov'):
            self.save_vid()
        elif self.path.endswith('mp3'):
            if self.compress != compress:
                raise ValueError('lz77 is the only compression algo that supports audio')
            self.save_audio()
        else:
            raise ValueError('Currently unsupported file.')

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} file")
    else:
        path = sys.argv[1]  # './examples/mouse.mov'
        conv = Convert(path)
        conv.save()
