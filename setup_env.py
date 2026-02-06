import os
import subprocess
import sys

# Nombre del entorno virtual
VENV_DIR = "RAG"
REQUIREMENTS_FILE = "requirements.txt"

def run_command(command, check=True):
    """Ejecuta un comando de shell."""
    result = subprocess.run(command, shell=True, check=check)
    return result

def create_venv():
    print(f"Creando entorno virtual en '{VENV_DIR}'...")
    run_command(f"{sys.executable} -m venv {VENV_DIR}")
    print("Entorno virtual creado.")

def install_requirements(python_executable):
    if os.path.exists(REQUIREMENTS_FILE):
        print(f"Instalando paquetes desde {REQUIREMENTS_FILE}...")
        run_command(f"{python_executable} -m pip install --upgrade pip")
        run_command(f"{python_executable} -m pip install -r {REQUIREMENTS_FILE}")
        print("Paquetes instalados.")
    else:
        print(f"No se encontró {REQUIREMENTS_FILE}. Saltando instalación de paquetes.")

def get_venv_python():
    """Devuelve la ruta al ejecutable de Python dentro del venv."""
    if os.name == "nt":  # Windows
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:  # Mac/Linux
        return os.path.join(VENV_DIR, "bin", "python")

def main():
    if os.path.exists(VENV_DIR):
        print(f"El entorno '{VENV_DIR}' ya existe.")
        python_executable = get_venv_python()
        print(f"Usando Python del entorno: {python_executable}")
    else:
        create_venv()
        python_executable = get_venv_python()
        install_requirements(python_executable)
    
    print("¡Listo! Puedes usar el entorno virtual ejecutando:")
    if os.name == "nt":
        print(f"{VENV_DIR}\\Scripts\\activate")
    else:
        print(f"source {VENV_DIR}/bin/activate")

if __name__ == "__main__":
    main()
