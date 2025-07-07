import os
import time

def limpar_tela():
    """Limpa a tela do terminal."""
    time.sleep(4)
    os.system('cls' if os.name == 'nt' else 'clear')
