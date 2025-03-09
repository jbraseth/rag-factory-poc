from speechbrain.pretrained import SpeakerDiarization

# Path to your audio file (must be WAV format)
audio_file = "/path/to/file/audio.wav"

# Initialize the diarization model
diarizer = SpeakerDiarization.from_hparams(
    source="speechbrain/spkrec-diarization",
    savedir="pretrained_models/spkrec-diarization"
)

# Perform diarization
diarization_result = diarizer.diarize_file(audio_file)

# Print out diarization segments
for segment in diarization_result:
    start = segment['start']   # start time in seconds
    end = segment['end']       # end time in seconds
    speaker = segment['speaker']
    print(f"[{start:.2f}s - {end:.2f}s] Speaker: {speaker}")
