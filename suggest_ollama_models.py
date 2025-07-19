import platform
import psutil
import shutil
import os
import subprocess
import sys


def get_os_info():
    try:
        version = platform.platform()
    except:
        version = platform.system() + " " + platform.release()
    return f"{platform.system()} (Version: {version})"


def get_ram_info():
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    return ram_gb


def get_cpu_info():
    return psutil.cpu_count(logical=True)


def get_gpu_info():
    gpus = []
    try:
        if sys.platform == "win32":
            command = [
                "powershell",
                "-Command",
                "Get-WmiObject Win32_VideoController | Select-Object Name, AdapterRAM"
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')[3:]
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                name = " ".join(parts[:-1]) if len(parts) > 1 else "Unknown"
                vram_bytes = int(parts[-1]) if parts[-1].isdigit() else 0
                vram_gb = round(vram_bytes / (1024**3), 2)
                gpu_type = "Dedicated" if "NVIDIA" in name.upper(
                ) or "RADEON" in name.upper() else "Integrated"
                gpus.append((name, gpu_type, vram_gb))
        elif sys.platform == "linux":
            result = subprocess.run(
                "lspci | grep VGA", shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if not line:
                    continue
                name = line.split(":")[-1].strip()
                gpu_type = "Dedicated" if any(x in name.lower() for x in [
                                              "nvidia", "radeon", "amd"]) else "Integrated"
                gpus.append((name, gpu_type, 0.0))
        elif sys.platform == "darwin":
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType"], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for i, line in enumerate(lines):
                if "Chipset Model" in line:
                    name = line.split(":")[-1].strip()
                    gpu_type = "Integrated" if "intel" in name.lower() else "Dedicated"
                    gpus.append((name, gpu_type, 0.0))
    except Exception as e:
        gpus.append(("Not detected", "Unknown", 0.0))

    if not gpus:
        gpus.append(("Not detected", "Unknown", 0.0))
    return gpus


def detect_npu():
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["powershell", "-Command", "Get-WmiObject Win32_Processor"], capture_output=True, text=True)
            text = result.stdout.lower()
            if "npu" in text or "neural" in text or "vpu" in text:
                return "Detected"
        elif sys.platform == "linux":
            with open("/proc/cpuinfo", "r") as f:
                text = f.read().lower()
                if any(x in text for x in ["npu", "neural", "vpu"]):
                    return "Detected"
        elif sys.platform == "darwin":
            result = subprocess.run(
                ["sysctl", "machdep.cpu"], capture_output=True, text=True)
            if "neural" in result.stdout.lower():
                return "Detected"
    except:
        pass
    return "Not detected"


def get_disk_info():
    try:
        if sys.platform == "win32":
            usage = psutil.disk_usage("C:\\")
            gb_total = round(usage.total / (1024 ** 3), 1)
            try:
                # Enhanced disk detection using PowerShell
                command = [
                    "powershell",
                    "-Command",
                    "(Get-PhysicalDisk | Where-Object {$_.DeviceID -eq 0}).MediaType"
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True)
                media_type = result.stdout.strip().upper()
                if "SSD" in media_type:
                    media_type = "SSD"
                elif "HDD" in media_type:
                    media_type = "HDD"
                else:
                    media_type = "UNKNOWN"
                return media_type, gb_total, "C:\\"
            except:
                return "UNKNOWN", gb_total, "C:\\"
        else:
            total, used, free = shutil.disk_usage("/")
            gb_total = round(total / (1024 ** 3), 1)
            media_type = "SSD" if os.path.islink("/dev/disk/by-id") else "HDD"
            return media_type, gb_total, "/"
    except:
        return "UNKNOWN", 0, "/"


def suggest_models(ram_gb, gpus):
    models = []
    if ram_gb >= 8:
        models.append("llama2:7b")
        models.append("mistral")
        models.append("gemma:2b")
        models.append("codellama:7b")

    print("\nSuggested Ollama models for your system:")
    if models:
        print(f"- ✅ {', '.join(models)} [Best for {int(ram_gb)}GB RAM]")
        for model in models:
            print(f"  🔽 ollama run {model}")
    else:
        print("- ⚠️ Not enough RAM. Use very small models like `tinyllama`")

    has_dedicated = any(g[1] == "Dedicated" for g in gpus)
    if has_dedicated:
        print("💡 Dedicated GPU detected. Ollama with GPU acceleration recommended.")
    else:
        print(
            "⚠️ Only integrated GPUs detected. Use lightweight models for best performance.")

    print("\nFor more, visit: https://ollama.com/library")


# Main Execution
if __name__ == "__main__":
    print(f"Operating System: {get_os_info()}")
    print(f"Total RAM: {get_ram_info()} GB")
    print(f"CPU Cores: {get_cpu_info()}")
    gpus = get_gpu_info()
    for i, gpu in enumerate(gpus):
        print(f"GPU #{i+1}: {gpu[0]} ({gpu[1]}, VRAM: {gpu[2]} GB)")
        print(f"  Type: {gpu[1]}")
        print(f"  Volume: {gpu[2]} GB")
    disk_type, disk_size, mountpoint = get_disk_info()
    print(f"Storage: {disk_type} {disk_size} GB (Mounted at {mountpoint})")
    print(f"NPU: {detect_npu()}")
    suggest_models(get_ram_info(), gpus)
