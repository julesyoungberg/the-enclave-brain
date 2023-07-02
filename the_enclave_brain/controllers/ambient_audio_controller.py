import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import os
import random
import time
from pathlib import Path
# import ... we expect custom SoundPlayer.py in same folder as this file

# Global variables
audio_data = {} # these should all be in one structure
samplerates = {}
volumes = {}
audio_idx = {}
audio_len = {} # Used for ending sounds pre-emptively
file_active = {} # If sounds are fading out, this is 0, else 1
streams = {}
exit_flag = False

FADE_TIME_s = 1.5  # Fade duration in seconds
AUDIO_CHUNK_SZ = 1024

audio_paths = {}
# Use this path when running as a standalone test script
where_we_at_path = str(Path.cwd().resolve())
# Use this path when running as part of enclave
# where_we_at_path = str(Path.cwd().resolve().parent.parent)
AUDIO_FOLDER = "/audio"

SCENE_FILE_COUNTS = {
    "healthy_forest": 1,
    "burning_forest": 1,
    "dead_forest": 1,
    "growing_forest": 1,
    "storm": 1,
    "rain": 1,
    "deforestation": 2,
    # "climate_change": 1,
}

# Missing audio files in your filepath? Download them from Jules' gdrive
def initialize_filepaths():
    audio_paths["healthy_forest"] = (where_we_at_path + AUDIO_FOLDER + "/HEALTHY") # Looks like "path/audio/HEALTHY"
    audio_paths["burning_forest"] = (where_we_at_path + AUDIO_FOLDER + "/BURN")
    audio_paths["dead_forest"] = (where_we_at_path + AUDIO_FOLDER + "/BURNT")
    audio_paths["growing_forest"] = (where_we_at_path + AUDIO_FOLDER + "/GROWING")
    audio_paths["storm"] = (where_we_at_path + AUDIO_FOLDER + "/STORM")
    audio_paths["rain"] = (where_we_at_path + AUDIO_FOLDER + "/RAIN")
    audio_paths["deforestation"] = (where_we_at_path + AUDIO_FOLDER + "/HUMAN")
    # No sound design for this one??
    # audio_paths["climate_change"] = (where_we_at_path + AUDIO_FOLDER + "/CLIMATE_CHANGE")

# Scene param are from SCENES dict in scenes.py
def set_scene(new_scene):
    for filename in audio_data:
        stop_audio(filename)

    if new_scene not in audio_paths:
        return
    
    subfolder_path = audio_paths[new_scene]
    filenames = os.listdir(subfolder_path)
    files_to_play = random.sample(filenames, SCENE_FILE_COUNTS[new_scene])

    for filename in files_to_play:
        load_audio(filename, subfolder_path + "/" + filename)
        play_audio(filename)

# Scene param are from SCENES dict in scenes.py
# Call this every 100ms or so. Longer intervals will leave more of a gap on sound fadeout/fadein
def update(scene):
    remaining_times = get_audio_time_remaining()
    for filename in remaining_times:
        if remaining_times[filename] < FADE_TIME_s and file_active[filename] is 1:

            # Mark the audio file that's finishing
            file_active[filename] = 0

            # Get list of all possible files for scene
            subfolder_path = audio_paths[scene]
            filenames = os.listdir(subfolder_path)

            # Find which files area playing right now
            dictKeys = list(audio_data.keys())

            # Point to existing item to enter the loop
            newFile = dictKeys[0] 

            # Pick a file that isn't playing
            loops = 0 
            while newFile in audio_data.keys():
                newFile = random.sample(filenames, 1)
                newFile = newFile[0] # Convert to string from list

                # Don't loop forever if all available files already playing
                loops += 1
                if(loops > 70):
                    print("we're looping forever, quik escape ambient")
                    break 

            load_audio(newFile, subfolder_path + "/" + newFile)
            play_audio(newFile)


# -----------  Private  -------------

def play_audio(filename, isMusic=False):
    # Fade in
    fade_in_samples = int(FADE_TIME_s * samplerates[filename])
    fade_in_curve = np.linspace(0, volumes[filename], fade_in_samples)
    audio_data[filename][:fade_in_samples] *= fade_in_curve[:, np.newaxis]

    # Fade out
    fade_out_samples = int(FADE_TIME_s * samplerates[filename])
    fade_out_curve = np.linspace(volumes[filename], 0, fade_out_samples)
    audio_data[filename][-fade_out_samples:] *= fade_out_curve[:, np.newaxis]

    stream = sd.OutputStream(channels=audio_data[filename].shape[1])
    stream.start()
    streams[filename] = stream

    def write_audio():
        current_index = 0
        while current_index < audio_len[filename]:
            chunk = audio_data[filename][current_index:current_index+AUDIO_CHUNK_SZ]
            chunk *= volumes[filename]
            if len(chunk) < AUDIO_CHUNK_SZ:
                # NOTE: this line produces a dtype mismatch TypeError
                # resolving this error by setting the correct dtype on np.zeros produces a pop
                chunk = np.append(chunk, np.zeros([AUDIO_CHUNK_SZ - len(chunk), 2]), axis=0)

            stream.write(chunk)        
            audio_idx[filename] += AUDIO_CHUNK_SZ # TODO combine audio_idx[filename] & current_index
            current_index += AUDIO_CHUNK_SZ

        stream.stop()
        stream.close()
        del streams[filename]
        del audio_data[filename]
        del samplerates[filename]
        del volumes[filename]
        del audio_idx[filename]
        del audio_len[filename]
        del file_active[filename]

    t = threading.Thread(target=write_audio)
    t.start()


# Triggers the audio to start fading out. Thread is killed after FADE_TIME_s
def stop_audio(filename):
    if filename in streams:

        file_active[filename] = 0
        
        fade_out_samples = int(FADE_TIME_s * samplerates[filename])
        playhead_idx = audio_idx[filename]

        # Don't double-fade audio if we are already near the end
        fade_time = samplerates[filename] * 1.5 # 1s is samplerate of samples
        if(audio_len[filename] - playhead_idx > fade_out_samples + fade_time):
            
            # Changing the length will make play_audio() stop @ appropriate time & handle cleanup
            audio_len[filename] = playhead_idx + fade_out_samples

            # Create fade
            fade_out_curve = np.linspace(volumes[filename], 0, fade_out_samples)
            for i in range(0, fade_out_samples):
                audio_data[filename][playhead_idx+i] *= fade_out_curve[i]

            # Add zeroes to the end to cover cases where we don't end on a frame boundary
            for i in range(0, AUDIO_CHUNK_SZ):
                audio_data[filename][playhead_idx+fade_out_samples+i] = 0
            

def load_audio(filename, filepath):
    audio, samplerate = sf.read(filepath)
    audio_data[filename] = audio.astype(np.float32)
    audio_len[filename] = len(audio)
    audio_idx[filename] = 0
    samplerates[filename] = samplerate
    volumes[filename] = 1.0
    file_active[filename] = 1


# Calling this every 100ms on all playing files should give us time to select the next sound
def get_audio_time_remaining():
    remaining_times_s = {}
    for filename in audio_data:
        remaining_samples = audio_len[filename] - audio_idx[filename]
        remaining_times_s[filename] = remaining_samples / samplerates[filename]

    return remaining_times_s

# For testing
def main():
    
    global exit_flag
    print("Audio Playback Application")
    print("Press 'q' to quit")

    # Load audio files
    audio_files = {
        # "ZOOM0263.wav" : "ZOOM0263.wav",
        # "shakir.wav" : "shakir.wav",
        # "thunderstorm.wav" : "thunderstorm.wav",
        # Add more audio files as needed
    }

    # Initialize audio data and volumes
    for filename, filepath in audio_files.items():
        load_audio(filename, filepath)

    # Start initial audio playback threads
    for file in audio_files:
        play_audio(file)

    # Main application loop
    while not exit_flag:
        initialize_filepaths()

        test_scene = "healthy_forest"
        set_scene(test_scene)

        while(1):
            update(test_scene)
            time.sleep(0.1)

    # Stop audio playback and join playback threads
    for stream in streams.values():
        stream.stop()
        stream.close()
    for t in threading.enumerate():
        if t != threading.current_thread():
            t.join()

    print("Application exited successfully.")


if __name__ == "__main__":
    main()
