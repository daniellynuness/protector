from src.services.sistema_gerenciador import SistemaGerenciadorSenhas
from src.interface.menu_handler import MenuHandler

def main():
    sistema = SistemaGerenciadorSenhas()
    menu = MenuHandler(sistema)
    menu.menu_inicial()

if __name__ == "__main__":
    main()