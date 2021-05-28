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

    Attributes
    ----------
    path: str
        path to the file that will be encoded.
        Raises TypeError if path is invalid

    Methods
    -------
    _convert_img(image)

    '''
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise TypeError('You must provide a valid path')

        self.path = path

    def _convert_img(self, image):
        arr = np.array(image)
        shape = np.array(arr.shape)
        flat_arr = arr.ravel()
        return flat_arr, shape

    def save_img(self):
        img = Image.open(self.path).convert('RGB')
        arr, shape = self._convert_img(img)
        img_info = np.array([arr, shape])
        # insert compression here
        with open(f'{self.path[:-3]}bzbi', 'wb') as file:
            np.save(file, img_info)

        print(img_info)

    def save_vid(self):
        clip = VideoFileClip(self.path)
        rate = clip.fps
        size = clip.size[::-1]
        vid_info = np.array([rate, *size, 3.], dtype = np.int)
        print(vid_info)
        clip = clip.subclip(0, 2)

        frames = []
        for frame in clip.iter_frames():
            frame_arr = frame.ravel()
            frames.append(frame_arr)
        frames = np.array(frames)

        frames = np.array([frames, vid_info])

        with open(f'{self.path[:-3]}bzbv', 'wb') as file:
            np.save(file, frames)

    def save_audio(self):
        sound = AudioSegment.from_file(self.path, format='mp3')
        peak_amplitude = sound.max
        loudness = sound.dBFS
        channels_cnt = sound.channels
        raw = np.array(sound.get_array_of_samples())

        # test = sound.get_array_of_samples()
        # print(test[:100])
        # raw = raw.ravel()
        if channels_cnt == 2:
            raw = raw.reshape(-1, 2)
        # y = np.int16(raw)
        frame_r = sound.frame_rate
        audio_info = np.array([peak_amplitude, channels_cnt, sound.frame_rate, sound.frame_rate])
        print(sound.frame_count()/ sound.frame_rate, len(sound))

        package = []
        for cnt in range(round(sound.frame_count()/ sound.frame_rate)):


            package.append(raw[(cnt * sound.frame_rate) : ((cnt + 1)*sound.frame_rate)])
        
        package = np.array(package)
        audio = np.array([package, audio_info])

        with open(f'{self.path[:-3]}bzba', 'wb') as file:
            np.save(file, audio)

        # print(len(raw), raw[1500:1700])
        # print(y[1000:1100])
        # song = AudioSegment(, frame_rate=frame_r, sample_width=2, channels=channels_cnt)
        # song.export(f'{self.path[:-5]}1.mp3', format="mp3")


        # print(raw[:100])


        # ab = np.load(raw)
        # print(signal[1000:1200])

        # print(arr[1000:1200])
        # print(ab)
        # spf = wave.open("/Users/shevdan/Documents/Programming/Python/DMProject/BzBCodec/examples/test_audi1.wav", "r")
        # # Extract Raw Audio from Wav File
        # signal = spf.readframes(-1)
        # signal = np.fromstring(signal, "Int16")
        # fs = spf.getframerate()
        # signal = signal.ravel()

        # Time = np.linspace(0, len(signal) / fs, num=len(signal))

        # plt.figure(1)
        # plt.title("Signal Wave...")
        # plt.plot(Time, signal)
        # plt.show()




        # plt.title("Signal Wave...")
        # # plt.figure(figsize=(20, 20))
        # plt.plot(arr)
        # plt.show()

    def save(self):
        if self.path.endswith('jpg') or self.path.endswith('.png'):
            self.save_img()
        elif self.path.endswith('mp4'):
            self.save_vid()
        elif self.path.endswith('mp3'):
            self.save_audio()
        else:
            raise ValueError('Currently unsupported file.')



if __name__ == '__main__':
    path = './examples/test_audio.mp3'

    # add_usr_local_bin()
    # print(os.environ['PATH'])
    # print()
    # print(os.pathsep)

    conv = Convert(path)
    conv.save()

