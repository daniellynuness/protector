import time
import os
from src.utilitario.validadores import classificar_senha
from src.utilitario.geradores import gerar_senha

class MenuHandler:
    def __init__(self, sistema):
        self.sistema = sistema

    def limpar_tela(self):
        """
        Limpa a tela do terminal.
        """
        time.sleep(3)
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception:
            print("Não foi possivel limpar tela. Continuando...")

    def menu_inicial(self):
        while True:
            print("\n=== Menu Inicial ===")
            print("1. Cadastro")
            print("2. Login")
            print("0. Sair")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.sistema.cadastrar_usuario()
            elif opcao == "2":
                usuario = self.sistema.login_usuario()
                if usuario:
                    self.menu_principal(usuario)
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

    def menu_principal(self, usuario):
        while True:
            print("\n=== Menu Principal ===")
            print("1. Cadastrar senhas")
            print("2. Visualizar senhas")
            print("3. Atualizar senhas")
            print("4. Deletar senhas")
            print("5. Gerar senhas")
            print("0. Sair")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.sistema.cadastrar_senha(usuario)
            elif opcao == "2":
                self.sistema.visualizar_senhas(usuario)
            elif opcao == "3":
                self.sistema.atualizar_senha(usuario)
            elif opcao == "4":
                self.sistema.deletar_senha(usuario)
            elif opcao == "5":
                self.sistema.gerar_senha()
            elif opcao == "0":
                print("Deslogando...")
                break
            else:
                print("Opção inválida!")