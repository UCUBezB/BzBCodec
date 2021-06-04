from concurrent.futures import ProcessPoolExecutor
from lz77 import decompress as lz77_decompress
from Huffman_algo import HuffmanCode
from lzw import lzw_decompress
from time import sleep, time
from deflate import Deflate
from mido import MidiFile
import sounddevice as sd
from cv2 import cv2
import numpy as np
import functools
import asyncio

def extract_wave_from_midi(filename='toccata.mid'):
    """
    extracts wave from midi (testing purposes)
    """
    bach = MidiFile(filename)
    sample_rate = 44100

    midi_dicts_list = []
    for msg in bach.tracks[2]:
        if msg.type in ['note_on', 'note_off']:
            midi_dicts_list.append(msg.dict())

    # change time values from delta to relative time.
    cur_time = 0
    notes_on = [-1 for _ in range(128)]
    notes = []
    for msg in midi_dicts_list:
        msg['time'] += cur_time
        cur_time = msg['time']

        if msg['type'] == 'note_on' and msg['velocity'] == 0:
            msg['type'] = 'note_off'

        if msg['type'] == 'note_on':
            notes_on[msg['note']] = int(msg['time'] / bach.ticks_per_beat * sample_rate)
        if msg['type'] == 'note_off':
            if notes_on[msg['note']] != -1:
                notes.append((
                    notes_on[msg['note']],
                    int(msg['time'] / bach.ticks_per_beat * sample_rate),
                    int(2 ** ((msg['note'] - 69) / 12) * 440)
                ))
                notes_on[msg['note']] = -1

    wave = np.zeros(notes[-1][1] + 1, dtype='float64')

    for begin, end, freq in notes:
        freqs = [freq]
        second_part = np.arange(end - begin, dtype='float64') / sample_rate * 2 * np.pi
        note_wave = np.sin(second_part * freqs[0])
        for freq_p in freqs[1:]:
            note_wave += np.sin(second_part * freq_p)
        note_wave /= len(freqs)
        wave[begin:end] += note_wave

    return wave

def play_audio(path, debug=True):
    """
    plays and decompresses audio concurrently
    """
    audio_file = np.load(path, allow_pickle=True)['info']
    audio_cur_ind = 0
    def callback(outdata, frames, *_):
        nonlocal audio_cur_ind, ready_audio
        if debug:
            print(f'ready {len(ready_audio) - 1} / playing {audio_cur_ind}', flush=True, end='     \r')
        if audio_cur_ind >= len(ready_audio):
            outdata[:] = np.zeros((frames, audio_file[1][1]), dtype='float32')
            return
        frame_num = len(ready_audio[audio_cur_ind])
        if frame_num < frames:
            outdata[:frame_num] = ready_audio[audio_cur_ind]
            outdata[frame_num:] = np.zeros(frames - frame_num, dtype='float32')
        else:
            outdata[:] = ready_audio[audio_cur_ind]
        ready_audio[audio_cur_ind] = None
        audio_cur_ind += 1
    transform = lambda buffer: (lz77_decompress(buffer) / audio_file[1][0]).reshape((audio_file[1][3], audio_file[1][1]))
    ready_audio = [transform(audio_file[0][0])]
    with sd.OutputStream(
            callback=callback,
            channels=audio_file[1][1],
            samplerate=audio_file[1][2],
            blocksize=audio_file[1][3]
        ):
        time_began = time()
        ind = 0
        for buffer in audio_file[0][1:]:
            ind += 1
            ready_audio.append(transform(buffer))
            if debug:
                print(f'ready {len(ready_audio) - 1} / playing {audio_cur_ind}', flush=True, end='     \r')
        sleep(audio_file[1][4] - (time() - time_began))

def show_image(path):
    """
    decompress and show image
    """
    image_file = np.load(path, allow_pickle=True)['info']
    if len(image_file) > 2:
        if image_file[2].lower() == 'lzw':
            decompressed = lzw_decompress(image_file[0])
        elif image_file[2].lower() == 'deflate':
            decompressed = Deflate().decode(*image_file[0])
        elif image_file[2].lower() == 'huffman':
            decompressed = HuffmanCode(image_file[0][0]).decode(image_file[0][1])
        else:
            decompressed = lz77_decompress(image_file[0])
    else:
        decompressed = lz77_decompress(image_file[0])
    image = np.reshape(decompressed, image_file[1])
    print("Press any key to exit...")
    cv2.imshow('image', image)
    cv2.waitKey(0)

def cv2_create_window(winname):
    """
    create a named video (in the main thread separate process)
    """
    cv2.namedWindow(winname)

def cv2_rgb_image_show(winname, img_rgb, wait_time):
    """
    update image in named window (in the main thread separate process)
    """
    cv2.imshow(winname, cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
    cv2.waitKey(wait_time)

def decompress_frame(frame, metadata):
    """
    decompress frames (in the main thread separate process)
    """
    ret = lz77_decompress(frame).reshape(metadata[1:])
    return ret

def play_video(path, debug=True):
    """
    plays and decompresses video concurrently (omg thread-safe)
    """
    video_file = np.load(path, allow_pickle=True)['info']
    metadata = video_file[1].astype(int)
    frame_rate = metadata[0]
    
    frames_num = len(video_file[0])

    ready_frames = [decompress_frame(video_file[0][0], metadata)]  # preload 1 frame
    ready_frames_lock = asyncio.Lock()

    main_thread_cv2_executor = ProcessPoolExecutor(1)
    main_thread_decompress_executor = ProcessPoolExecutor(2)
    loop = asyncio.get_event_loop()

    async def play_video_in_main_thread(loop):
        current_frame_index = 0
        wait_time = 1 / frame_rate

        await loop.run_in_executor(main_thread_cv2_executor, functools.partial(cv2_create_window, winname="video"))

        image = np.zeros(metadata[1:]).astype('uint8')

        while current_frame_index < frames_num:
            if debug and current_frame_index % 10 == 0:
                print(f'ready {len(ready_frames)} / playing {current_frame_index}', flush=True, end='     \r')
            async with ready_frames_lock:
                if current_frame_index < len(ready_frames):
                    image = ready_frames[current_frame_index]
                    current_frame_index += 1
            await loop.run_in_executor(
                main_thread_cv2_executor,
                functools.partial(
                    cv2_rgb_image_show, winname='video',
                    img_rgb=image, wait_time=int(max(wait_time, 0.001) * 1000)
                )
            )

    async def prepare_frames(loop):
        for frame in video_file[0][1:]:
            result = await loop.run_in_executor(
                main_thread_decompress_executor, functools.partial(decompress_frame, frame=frame, metadata=metadata)
            )
            async with ready_frames_lock:
                ready_frames.append(result)

    async def run_loop(loop):
        await asyncio.gather(
            asyncio.create_task(play_video_in_main_thread(loop)),
            asyncio.create_task(prepare_frames(loop))
        )

    loop.run_until_complete(run_loop(loop))

def play(path):
    """
    play the specified file
    """
    res_dict = {
        "bzbv": play_video,
        "bzbi": show_image,
        "bzba": play_audio
    }
    res_dict[path.split('.')[-1]](path)

if __name__ == '__main__':
    play('examples/mouse.bzbv')
