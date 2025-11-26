# ================================
# INSTALL SCRIPT FOR LOCAL LLM + STT + TTS
# WINDOWS 11 (CPU ONLY)
# ================================

Write-Host "Creating Conda environment..."

# Create environment
conda create -n local_llm python=3.10 -y
conda activate local_llm

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel

Write-Host "Installing core Python packages..."
pip install sounddevice numpy scipy pydub playsound soundfile

Write-Host "Installing faster-whisper (STT)..."
pip install faster-whisper

Write-Host "Installing llama-cpp-python (LLM backend)..."
pip install llama-cpp-python

Write-Host "Installing Coqui TTS..."
pip install TTS

# ================================
# CREATE MODEL FOLDER
# ================================
$ModelDir = "C:\local_llm_models"
if (!(Test-Path $ModelDir)) {
    New-Item -ItemType Directory -Force -Path $ModelDir
}

Write-Host "Downloading LLM (Mistral 7B GGUF Q4_K_M)..."

# -------- LLM (GGUF) --------
Invoke-WebRequest `
    -Uri "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf" `
    -OutFile "$ModelDir\mistral-7b.Q4_K_M.gguf"

Write-Host "Downloading Whisper STT model (small)..."

# -------- Whisper STT --------
Invoke-WebRequest `
    -Uri "https://huggingface.co/capslock/faster-whisper-small/resolve/main/model.bin" `
    -OutFile "$ModelDir\whisper-small.bin"

Write-Host "Coqui TTS will auto-download its model on first run."
Write-Host "Done!"
