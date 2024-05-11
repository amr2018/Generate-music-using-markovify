
import mido
import os
import markovify


# get all notes from files
def get_notes(midi_folder):
    notes = []
    for file in os.listdir(midi_folder):
        for msg in mido.MidiFile(f'{midi_folder}/{file}'):
            if not msg.is_meta and msg.type == 'note_on':
                notes.append(str(msg.note))
    
    return notes


def convert_notes_to_text(notes):
    return ' '.join(notes)


notes_as_text = convert_notes_to_text(get_notes('dataset'))

def convert_text_to_notes(text):
    notes = text.split(' ')
    notes = [int(note) for note in notes]
    return notes

def generate_midi_file():
    model = markovify.Text(notes_as_text)
    generated_tokens = model.make_sentence()
    
    notes = convert_text_to_notes(generated_tokens)
    
    output_midi = mido.MidiFile()
    track = mido.MidiTrack()
    output_midi.tracks.append(track)

    for note in notes:
        # Add note_on and note_off messages for each note
        track.append(mido.Message('note_on', note=note, velocity=64, time=120))
        track.append(mido.Message('note_off', note=note, velocity=64, time=120))

    # Save the generated MIDI file
    output_midi.save('generated_music.mid')

generate_midi_file()