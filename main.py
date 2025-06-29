from src.servicos.sistema_gerenciador import SistemaGerenciadorSenhas
from src.menu.menus import Menus

def main():
    sistema = SistemaGerenciadorSenhas()
    menu = Menus(sistema)
    menu.menu_inicial()

if __name__ == "__main__":
    main()