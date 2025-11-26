import os
import queue
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
from time import time, sleep

from faster_whisper import WhisperModel
from llama_cpp import Llama
from TTS.api import TTS

# ==================================================
# CONFIGURE MODEL PATHS
# ==================================================
MODEL_DIR = r"C:\local_llm_models"

LLM_PATH = MODEL_DIR + r"\mistral-7b.Q4_K_M.gguf"   # LLM model
WHISPER_PATH = MODEL_DIR                            # Whisper folder (model.bin inside)

TTS_MODEL = "tts_models/en/ljspeech/tacotron2-DDC"  # auto-download on first run

# ==================================================
# PERFORMANCE SETTINGS
# ==================================================
NUM_THREADS = max(2, os.cpu_count() - 2)
os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
os.environ["MKL_NUM_THREADS"] = str(NUM_THREADS)

# ==================================================
# MICROPHONE SETTINGS
# ==================================================
SAMPLE_RATE = 16000
CHUNK_SEC = 2.0
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_SEC)

audio_queue = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    if status:
        print("Audio warning:", status)
    audio_queue.put(indata.copy())


# ==================================================
# INITIALIZE MODELS
# ==================================================
print("Loading Whisper (STT)...")
whisper = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8_float16"
)

print("Loading LLM (llama-cpp-python)...")
llm = Llama(
    model_path=LLM_PATH,
    n_threads=NUM_THREADS,
    n_ctx=2048,
    verbose=False
)

print("Loading TTS model...")
tts = TTS(TTS_MODEL)

# ==================================================
# HELPERS
# ==================================================
def transcribe(audio):
    """
    audio = numpy array float32 [-1..1]
    """
    print("Transcribing audio...")
    segments, info = whisper.transcribe(audio, beam_size=5, vad_filter=True)
    text = " ".join([seg.text for seg in segments])
    print("STT:", text)
    return text.strip()


def llm_reply(prompt):
    """
    Calls the LLM and returns its generated text.
    """
    print("Generating reply from LLM...")
    response = llm.create(
        prompt=f"User: {prompt}\nAssistant:",
        max_tokens=200,
        temperature=0.2,
    )
    return response["choices"][0]["text"].strip()


def speak(text, filename="tts_output.wav"):
    print("Speaking:", text)
    tts.tts_to_file(text=text, file_path=filename)
    data, sr = sf.read(filename)
    sd.play(data, sr)
    sd.wait()


# ==================================================
# WORKER THREADS
# ==================================================
def mic_worker():
    print("Microphone active.")
    with sd.InputStream(
        channels=1,
        callback=audio_callback,
        samplerate=SAMPLE_RATE,
        blocksize=CHUNK_SIZE
    ):
        while True:
            sleep(0.1)


def main_loop():
    buffer = np.zeros((0,), dtype=np.float32)

    print("Ready. Speak any time...")

    while True:
        chunk = audio_queue.get()
        mono = chunk[:, 0] if chunk.ndim > 1 else chunk
        buffer = np.concatenate([buffer, mono])

        if len(buffer) >= CHUNK_SIZE:
            audio_block = buffer.copy()
            buffer = np.zeros((0,), dtype=np.float32)

            # Normalize audio
            audio_block = audio_block.astype(np.float32)

            text = transcribe(audio_block)
            if not text:
                continue

            reply = llm_reply(text)
            speak(reply)


# ==================================================
# ENTRY POINT
# ==================================================
if __name__ == "__main__":
    t = threading.Thread(target=mic_worker, daemon=True)
    t.start()

    try:
        main_loop()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
