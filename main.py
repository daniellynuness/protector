from src.servicos.sistema_gerenciador import SistemaGerenciadorSenhas
from src.menu.menus import Menus

def main():
    sistema = SistemaGerenciadorSenhas()
    menu = Menus(sistema)
<<<<<<< HEAD
    try:
        menu.menu_inicial()
    finally:
        sistema.salvar_dados()
=======
    menu.menu_inicial()
>>>>>>> c5bbacc84a700283a24a18c1bcf8f376e5317076

if __name__ == "__main__":
    main()