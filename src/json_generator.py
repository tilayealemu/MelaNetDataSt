from __future__ import absolute_import, division, print_function

import argparse
import json
import os
import wave
import sys


"""
trans_file should be csv file where each line is of the form: transcription,file_name
"""
def generate_json(trans_file, wav_base_dir, output_file):
    labels = []
    durations = []
    keys = []
    for line in open(trans_file):
        split = line.strip().split(",")
        label = split[0]
        file_id = split[1]
        audio_file = os.path.join(wav_base_dir, file_id)
        audio = wave.open(audio_file)
        duration = float(audio.getnframes()) / audio.getframerate()
        audio.close()
        keys.append(audio_file)
        durations.append(duration)
        labels.append(label)
    with open(output_file, 'w') as out_file:
        for i in range(len(keys)):
            line = json.dumps({'key': keys[i], 'duration': durations[i],
                              'text': labels[i]}, ensure_ascii=False)
            out_file.write(line + '\n')
