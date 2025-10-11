import subprocess
import sys
import threading
import time

# Función para arrancar FastAPI
def start_fastapi():
    subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.app:app", "--reload"])
    time.sleep(2)  # Esperar a que el backend se inicialice

# Función para arrancar Streamlit
def start_streamlit():
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py"])

# Ejecutar FastAPI en un hilo separado
threading.Thread(target=start_fastapi, daemon=True).start()

# Ejecutar Streamlit
start_streamlit()
