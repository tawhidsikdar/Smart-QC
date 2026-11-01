# SmartQC

Automated fabric inspection machine (IUT IPE capstone). Python inspection engine,
Streamlit dashboard and ESP32 firmware.

## New computer setup (Windows, about 30 minutes)

Use **Anaconda Prompt** (cmd), not PowerShell. Commands below assume that.

### 0. Install the tools (skip any you already have)
- Git: https://git-scm.com
- Anaconda or Miniconda: https://www.anaconda.com
- VS Code: https://code.visualstudio.com (then install the **Python** extension by Microsoft)

### 1. Get the code
Go to the folder where you keep code projects (example: `D:\code`):
```
cd /d D:\code
git clone https://github.com/tawhidsikdar/Smart-QC.git
cd Smart-QC
```

### 2. Create the environment
```
conda env create -f environment.yml
conda activate smartqc
```
The prompt should now start with `(smartqc)`.

### 3. Install PyTorch (different for GPU and CPU computers)
Run `nvidia-smi`.

**A. NVIDIA GPU, and "CUDA UMD Version" (or "CUDA Version") is 13.4 or higher:**
```
python -m pip install torch==2.15.0 torchvision==0.29.2 --index-url https://download.pytorch.org/whl/cu134
```

**B. No NVIDIA GPU (or `nvidia-smi` not found):**
```
python -m pip install torch==2.15.0 torchvision==0.29.2 --index-url https://download.pytorch.org/whl/cpu
```

**C. NVIDIA GPU but CUDA version below 13.4:** update the NVIDIA driver first, or ask Ratul.

Check:
```
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```
GPU computer: `2.15.0+cu134 True`. CPU computer: `2.15.0+cpu False`.

### 4. Install Ultralytics (always AFTER PyTorch)
```
python -m pip install ultralytics==8.4.197
```

### 5. Make your local config
```
copy config.example.yaml config.local.yaml
code config.local.yaml
```
Edit the values for this computer. On a computer without an NVIDIA GPU, set `device: cpu`.
Never commit `config.local.yaml` (Git ignores it automatically).

### 6. Run the setup check
```
python check_setup.py
```
You need `ALL GOOD`. `WARN` lines (camera, ESP32 port, model) are fine until that hardware or model is ready.

### 7. Connect VS Code
```
code .
```
- `Ctrl+Shift+P` → **Python: Select Interpreter** → choose the one with `envs\smartqc`.
- `Ctrl+Shift+P` → **Terminal: Select Default Profile** → **Command Prompt**.
- Open a new terminal: it should start with `(smartqc)`.

## Every session
```
cd /d <your path>\Smart-QC
conda activate smartqc
git pull
```
`git pull` before you start, `git push` when you finish. Keep `main` always working.

## Where things live
| What | Where |
| --- | --- |
| Code, `environment.yml`, `config.example.yaml` | This GitHub repo |
| Photos, labels, trained models | Google Drive (`models.md` says which model is current) |
| This computer's settings | `config.local.yaml` (not in Git) |