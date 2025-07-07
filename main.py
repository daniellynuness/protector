from src.servicos.sistema_gerenciador import SistemaGerenciadorSenhas
from src.menu.menus import Menus

def main():
    sistema = SistemaGerenciadorSenhas()
    menu = Menus(sistema)
    try:
        menu.menu_inicial()
    finally:
        sistema.salvar_dados()

if __name__ == "__main__":
    main()