📘 LOCAL VOICE ASSISTANT — User Guide
🎯 What This App Does

This application lets you talk to an AI assistant entirely offline.
It listens to your voice, converts speech to text (STT), sends it to a local language model (LLM), then speaks the AI’s answer back to you using text-to-speech (TTS).

No internet connection is required.
All processing happens on your laptop.

🖥️ System Requirements

Windows 11

Intel i7 (or equivalent)

16 GB RAM minimum (40 GB recommended)

Working microphone & speakers

Python (installed automatically in the setup script)

⚙️ Installation

Download or copy the two provided files:

install_environment.ps1

local_voice_assistant.py

Right-click install_environment.ps1 → Run with PowerShell
(You may need to allow the script in the Windows prompt.)

Wait until the installation finishes.
The script automatically:

creates a Python environment,

installs all required libraries,

downloads the LLM and STT models.

When it says “Done!”, installation is complete.

▶️ How to Run the Voice Assistant

Open PowerShell

Activate the environment:

conda activate local_llm


Start the assistant:

python local_voice_assistant.py


After a few seconds, you will see:

“Ready. Speak any time…”

Now you can talk naturally.

🎤 Using the Assistant
Talking

Just speak normally.
Pause briefly after your sentence — the app automatically detects your speech and processes it.

Responding

The AI will think for a moment

Then it will speak its answer aloud

You don’t need to press anything

You can speak again as soon as it finishes

💡 What You Can Ask

Try prompts like:

"Explain a science concept to me."

"Tell me a short story about space explorers."

"Summarize the causes of World War I."

"Help me understand algebra."

"Describe how photosynthesis works in simple terms."

The model works best with:

educational questions

general knowledge

creative tasks

step-by-step explanations

📦 What Happens Internally

For showcasing or explaining the system to others:

Audio Capture
The microphone continuously records small chunks of sound.

Speech-to-Text (STT)
Audio is converted to text using the Whisper model (running locally).

Local LLM Processing
The transcribed text is sent to a quantized Mistral-7B model via llama.cpp.

Text-to-Speech (TTS)
The AI response is turned into speech using Coqui TTS.

Playback
The synthesized voice is played through your speakers.

This entire workflow runs offline with no cloud connection.

🛠️ Troubleshooting
No sound or no microphone?

Check Windows audio settings

Ensure the microphone is enabled and selected

Try plugging in a USB mic or headset

The LLM is too slow?

Close other apps

Use shorter prompts

Ask to switch to a smaller model (e.g., 3B)

Distorted TTS audio?

Lower speaker volume

Try a different TTS model (I can provide options)

🎓 Showcase Tips

When demonstrating the app:

✔ Start with simple conversational questions
✔ Point out that everything runs offline
✔ Show the folder where the models live
✔ Open Task Manager to show CPU usage in real time
✔ Emphasize the privacy benefits (no data leaves the device)

A great opening question:

“What’s a fun science fact?”

It’s short, changes often, and sounds good when spoken aloud.
