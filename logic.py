import librosa
import numpy as np
import matplotlib.pyplot as plt
from google.colab import drive

### 1. Import audio file
drive.mount('/content/drive/', force_remount=True)
audio = '/content/drive/MyDrive/2026_tune_detector_project/coldplay_yellow.mp3'
y, sr = librosa.load(audio)

song_length = (len(y)/sr)/60
song_min = int(song_length)
song_sec = (60*(song_length - float(song_min)))
song_sec = int(song_sec)
if song_sec >= 10:
  print("duration: " + str(song_min) + ":" + str(song_sec))
else:
  print("duration: " + str(song_min) + ":0" + str(song_sec))

### 2. Convert time to frequency

chroma = librosa.feature.chroma_stft(y=y, sr=sr)

### 3. Compare frequencies to notes. List all 12 notes

chroma_mean = chroma.mean(axis=1)
#print(chroma_mean); print()

# CHROMA BIN    0    1     2    3     4    5    6     7    8     9    10    11
notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
notes_flat  = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
# SHARP/FLAT    ?     b    #     b    #    b     #    #     b    #     b    #

camelot     = [8, 3, 10, 5, 12, 7, 2, 9, 4, 11, 6, 1]

### 4. Establish major and minor key patterns that start at each note

  # Major: 0   2   4   5   7   9  11
  #  Diff: 0   2   2   1   2   2   2

  # Minor keys are the same but a few indices back % 12

key_scores = []

#print()

for index, note in enumerate(chroma_mean):

  #print(str(notes_sharp[index]) + " Major")

  notes = []
  note_names = []
  notes.append(float(chroma_mean[index]))
  note_names.append(notes_sharp[index])

  prev = index

  for i in range(2):
    next = prev + 2
    if next > 11:
      next = next % 12
    else:
      next = next
    prev = next
    notes.append(float(chroma_mean[next]))
    note_names.append(notes_sharp[next])

  prev = index + 3
  for i in range(4):
    next = prev + 2
    if next > 11:
      next = next % 12
    else:
      next = next
    prev = next
    notes.append(float(chroma_mean[next]))
    note_names.append(notes_sharp[next])

  score = float (sum(notes) / len(notes))
  '''print(notes)
  print(note_names)
  print("TOTAL SCORE: " + str(score)); print()'''
  key_scores.append(score);

 ## Based off I, V, vi chords

  low = 0
  middle = 0
  high = 0


  major_scores = []
  minor_scores = []

  # MAJOR CHORDS

for index, note in enumerate(chroma_mean):
  low = index
  #print(str(notes_sharp[low]) + " Major")


  middle = index + 4
  if low > 7:
    middle = middle % 12
  else:
    middle = middle


  high = middle + 3
  if low > 4:
    high = high % 12
  else:
    high = high


  score = float((chroma_mean[low]+chroma_mean[middle]+chroma_mean[high])/3)
  #print(str(notes_sharp[low]) + ", " + notes_sharp[middle] + ", "  + notes_sharp[high])
  #print(score); print()
  major_scores.append(score);

  # MINOR CHORDS

#print(); print()

for index, note in enumerate(chroma_mean):
  low = index
  #print(str(notes_sharp[low]) + " Minor")

  middle = index + 3
  if low > 8:
    middle = middle % 12
  else:
    middle = middle


  high = middle + 4
  if low > 4:
    high = high % 12
  else:
    high = high


  score = float((chroma_mean[low]+chroma_mean[middle]+chroma_mean[high])/3)
  #print(str(notes_sharp[low]) + ", " + notes_sharp[middle] + ", "  + notes_sharp[high])
  #print(score); print()
  minor_scores.append(score);

#print(major_scores)
#print(minor_scores)

### 5. Determine which major/minor key fits the notes best through iteration

#print("Major key relevance (by notes):")
#print(key_scores)

max_value = max(key_scores)
max_index = key_scores.index(max_value)

chord_scores = []

for index, score in enumerate(major_scores):
  ii_key_index  = (index - 10) % 12
  iii_key_index = (index -  8) % 12
  IV_key_index  = (index -  7) % 12
  V_key_index   = (index -  5) % 12
  vi_key_index  = (index -  3) % 12
  '''
  print()
  print(index)
  print("  I: " + str(major_scores[index]))
  #print(" ii: " + str(minor_scores[ii_key_index]))
  #print("iii: " + str(minor_scores[iii_key_index]))
  print(" IV: " + str(major_scores[IV_key_index]))
  #print("  V: " + str(major_scores[V_key_index]))
  print(" vi: " + str(minor_scores[vi_key_index]))
  '''

  total_score = (major_scores[index] + major_scores[V_key_index] + minor_scores[vi_key_index])/3
  #total_score = (major_scores[index]*5.31 + minor_scores[ii_key_index]*3.74 + minor_scores[iii_key_index]*4.15 + major_scores[IV_key_index]*4.70 + major_scores[V_key_index]*3.85 + minor_scores[vi_key_index]*4.80)/26.55

  #print("TOTAL SCORE: " + str(total_score))
  chord_scores.append(total_score)

chord_max_value = max(chord_scores)
chord_max_index = chord_scores.index(chord_max_value)

### 6. Print / output the key

'''
print(key_scores)
print(chord_scores)
print()
'''

combined_scores = [(key_scores[i] + chord_scores[i])/2 for i in range(len(key_scores))]
#print(combined_scores)

overall_max_value = max(combined_scores)
overall_max_index = combined_scores.index(overall_max_value)

print()
print("BASED OFF NOTES")

if camelot[max_index] >= 3 and camelot[max_index] < 8:
  print("Key: " + notes_flat[max_index] + " major / " + notes_flat[(max_index - 3) % 12] + " minor")
else:
  print("Key: " + notes_sharp[max_index] + " major / " + notes_sharp[(max_index - 3) % 12] + " minor")

print("Camelot: " + str(camelot[max_index]) + "A/" + str(camelot[max_index]) + "B")

print()
print("BASED OFF I-V-vi CHORDS")

if camelot[chord_max_index] >= 3 and camelot[chord_max_index] < 8:
  print("Key: " + notes_flat[chord_max_index] + " major / " + notes_flat[(chord_max_index - 3) % 12] + " minor")
else:
  print("Key: " + notes_sharp[chord_max_index] + " major / " + notes_sharp[(chord_max_index - 3) % 12] + " minor")

print("Camelot: " + str(camelot[chord_max_index]) + "A/" + str(camelot[chord_max_index]) + "B")

print()
print("OVERALL")

if camelot[overall_max_index] >= 3 and camelot[overall_max_index] < 8:
  print("Key: " + notes_flat[overall_max_index] + " major / " + notes_flat[(overall_max_index - 3) % 12] + " minor")
else:
  print("Key: " + notes_sharp[overall_max_index] + " major / " + notes_sharp[(overall_max_index - 3) % 12] + " minor")

print("Camelot: " + str(camelot[overall_max_index]) + "A/" + str(camelot[overall_max_index]) + "B")
