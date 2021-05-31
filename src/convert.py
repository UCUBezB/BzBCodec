'''
Module for converting files into custom codec using compression algos
'''

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
        if 'deflate' in compression_type.lower():
            return HuffmanCode().encode
        raise ValueError('Unsupported compression. One of the following are supported:\
 lz77, lzw, huffman, deflate')

    def _convert_img(self, image) -> tuple:
        '''
        Private method for converting image into numpy array
        '''
        arr = np.array(image)
        shape = np.array(arr.shape, dtype='uint8')
        flat_arr = self.compress(arr.ravel())

        # flat_arr = np.array(flat_arr, dtype=[('offset', 'uint8'), ('length', 'uint16'), ('pixel', 'uint8')])
        # print(flat_arr)

        return flat_arr, shape

    def save_img(self):
        '''
        compresses the image and creates encoded file
        '''
        img = Image.open(self.path).convert('RGB')
        arr, shape = self._convert_img(img)
        img_info = np.array([arr, shape])


        # with open(f'{self.path[:-3]}bzbi', 'wb') as file:
        np.savez_compressed(f'{self.path[:-3]}bzbi', img_info)

    def save_vid(self):
        '''
        compresses the video and creates encoded file
        '''
        clip = VideoFileClip(self.path)
        rate = clip.fps
        print(rate)
        size = clip.size[::-1]
        vid_info = np.array([rate, *size, 3.], dtype = np.int)

        #convert frames of the video into numpy
        frames = []
        for frame in clip.iter_frames():
            frame = np.array(frame, dtype='uint8')
            #insert compression here
            frame_arr = self.compress(frame.ravel())

            frames.append(frame_arr)

        frames = np.array(frames)

        frames = np.array([frames, vid_info])

        # with open(f'{self.path[:-3]}bzbv', 'wb') as file:
        np.savez_compressed(f'{self.path[:-3]}bzbv', frames)

    def save_audio(self):
        '''
        compresses the audio and creates encoded file
        '''
        sound = AudioSegment.from_file(self.path, format='mp3')
        peak_amplitude = sound.max
        loudness = sound.dBFS
        channels_cnt = sound.channels
        raw = np.array(sound.get_array_of_samples())

        frame_r = sound.frame_rate
        audio_info = np.array([peak_amplitude, channels_cnt, sound.frame_rate, 
                    sound.frame_rate, sound.frame_count()/ sound.frame_rate], dtype=object)

        package = []
        for cnt in range(round(sound.frame_count()/ sound.frame_rate)):

            compressed_package = np.array(raw[(cnt * sound.frame_rate) : ((cnt + 1)*sound.frame_rate)], dtype='uint16')
            #insert compression here
            compressed_package = self.compress(compressed_package)

            package.append(compressed_package)
        
        package = np.array(package)
        audio = np.array([package, audio_info])

        np.savez_compressed(f'{self.path[:-3]}bzba', audio)

    
    def save(self):
        '''
        compresses any given file or raises the error if it is unsupported
        '''
        if self.path.endswith('.jpg') or self.path.endswith('.png') or self.path.endswith('.jpeg'):
            self.save_img()
        elif self.path.endswith('mp4') or self.path.endswith('mov'):
            self.save_vid()
        elif self.path.endswith('mp3'):
            self.save_audio()
        else:
            raise ValueError('Currently unsupported file.')

if __name__ == '__main__':
    path = './examples/test_audio.mp3'
    
    conv = Convert(path)
    conv.save()