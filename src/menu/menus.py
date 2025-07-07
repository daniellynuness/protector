class Menus:
    def __init__(self, sistema):
        self.sistema = sistema

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
                    self.menu_perfil(usuario)
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

    def menu_perfil(self, usuario):
        while True:
            print("\n=== Perfis do Usuário ===")
            if usuario.perfis:
                nomes = [perfil.nome for perfil in usuario.perfis]
                print("Perfis existentes: " + ", ".join(nomes))
            else:
                print("Nenhum perfil cadastrado.")

            print("1. Selecionar perfil")
            print("2. Criar novo perfil")
            print("0. Sair")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                if not usuario.perfis:
                    print("Nenhum perfil cadastrado.")
                    continue
                nome = input("Nome do perfil: ").strip()
                senha = input("Senha do perfil: ").strip()
                if usuario.selecionar_perfil(nome, senha):
                    print(f"Perfil '{nome}' selecionado!")
                    self.menu_principal(usuario)
                    break
                else:
                    print("Perfil ou senha incorretos!")
            elif opcao == "2":
                nome = input("Nome do novo perfil: ").strip()
                senha = input("Crie uma senha para este perfil: ").strip()
                from src.usuario.perfil import Perfil
                novo_perfil = Perfil(nome, senha)
                usuario.adicionar_perfil(novo_perfil)
                print(f"Perfil '{nome}' criado!")
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")

    def menu_principal(self, usuario):
        perfil = usuario.perfil_atual
        while True:
            print(f"\n=== Menu Principal | Perfil: {perfil.nome} ===")
            print("1. Cadastrar senhas")
            print("2. Visualizar senhas")
            print("3. Atualizar senhas")
            print("4. Deletar senhas")
            print("5. Gerar senhas")
            print("0. Sair do perfil")
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
                self.sistema.gerar_senha(usuario)
            elif opcao == "0":
                usuario.perfil_atual = None
                break
            else:
                print("Opção inválida!")