'''
Module for converting files into custom codec using compression algos
'''

import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os



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
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise TypeError('You must provide a valid path')

        self.path = path

    def _convert_img(self, image) -> tuple:
        '''
        Private method for converting image into numpy array
        '''
        arr = np.array(image)
        shape = np.array(arr.shape)
        flat_arr = arr.ravel()
        return flat_arr, shape

    def save_img(self):
        '''
        compresses the image and creates encoded file
        '''
        img = Image.open(self.path).convert('RGB')
        arr, shape = self._convert_img(img)
        img_info = np.array([arr, shape])
        # insert compression here
        with open(f'{self.path[:-3]}bzbi', 'wb') as file:
            np.save(file, img_info)

    def save_vid(self):
        '''
        compresses the video and creates encoded file
        '''
        clip = VideoFileClip(self.path)
        rate = clip.fps
        size = clip.size[::-1]
        vid_info = np.array([rate, *size, 3.], dtype = np.int)
        print(vid_info)
        clip = clip.subclip(0, 2)

        #convert frames of the video into numpy
        frames = []
        for frame in clip.iter_frames():
            #insert compression here
            frame_arr = frame.ravel()
            frames.append(frame_arr)

        frames = np.array(frames)

        frames = np.array([frames, vid_info])

        with open(f'{self.path[:-3]}bzbv', 'wb') as file:
            np.save(file, frames)

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
            
            #insert compression here

            package.append(raw[(cnt * sound.frame_rate) : ((cnt + 1)*sound.frame_rate)])
        
        package = np.array(package)
        audio = np.array([package, audio_info])

        with open(f'{self.path[:-3]}bzba', 'wb') as file:
            np.save(file, audio)

    
    def save(self):
        '''
        compresses any given file or raises the error if it is unsupported
        '''
        if self.path.endswith('.jpg') or self.path.endswith('.png'):
            self.save_img()
        elif self.path.endswith('mp4'):
            self.save_vid()
        elif self.path.endswith('mp3'):
            self.save_audio()
        else:
            raise ValueError('Currently unsupported file.')
