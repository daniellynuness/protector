from src.utilitario.limpeza import limpar_tela

class Menus:
    """    Classe responsável por gerenciar os menus do sistema.
    Ela permite que o usuário cadastre-se, faça login, crie perfis e acesse funcionalidades do sistema.
    """
    def __init__(self, sistema):
        """
        Inicializa a classe Menus.
        """
        self.sistema = sistema

    def menu_inicial(self):
        """
        Exibe o menu inicial e gerencia as opções do usuário.
        """
        while True:
            print("\n=== Menu Inicial ===")
            print("1. Cadastro")
            print("2. Login")
            
            opcao = input("Escolha uma opção (ou pressione Enter para sair): ").strip()

            if opcao == "1":
                usuario_cadastrado = self.sistema.cadastrar_usuario()
                if usuario_cadastrado:
                    # Pergunta se deseja cadastrar outro usuário
                    if input("\nDeseja cadastrar outro usuário? (s/n): ").lower() != 's':
                        # Se não, faz o login automático com o usuário recém-criado
                        self.menu_perfil(usuario_cadastrado)
            elif opcao == "2":
                usuario = self.sistema.login_usuario()
                if usuario:
                    self.menu_perfil(usuario)
            elif not opcao: # Opção "Sair"
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

    def menu_perfil(self, usuario):
        """
        Exibe o menu de perfis do usuário e permite selecionar ou criar perfis.
        """
        while True:
            print(f"\n=== Conta do(a) {usuario.nome} ===")
            if usuario.perfis:
                nomes = [perfil.nome for perfil in usuario.perfis]
                print("Perfis existentes: " + ", ".join(nomes))
            else:
                print("Nenhum perfil cadastrado.")

            print("1. Selecionar perfil")
            print("2. Criar novo perfil")
            print("3. Excluir perfil")
            
            opcao = input("Escolha uma opção (ou pressione Enter para sair): ").strip()

            if opcao == "1":
                if not usuario.perfis:
                    print("Nenhum perfil cadastrado.")
                    continue
                nome = input("Nome do perfil para selecionar: ").strip()
                senha = input("Senha do perfil: ").strip()
                if usuario.selecionar_perfil(nome, senha):
                    print(f"Perfil '{nome}' selecionado!")
                    self.menu_principal(usuario)
                    break
                else:
                    print("Perfil ou senha incorretos!")
            elif opcao == "2":
                from src.usuario.perfil import Perfil
                while True:
                    nome = input("Nome do novo perfil: ").strip()
                    if not nome:
                        print("O nome do perfil não pode ser vazio.")
                        continue

                    if any(p.nome.lower() == nome.lower() for p in usuario.perfis):
                        print("Já existe um perfil com este nome. Tente outro.")
                        continue

                    senha = input("Crie uma senha para este perfil: ").strip()
                    if not senha:
                        print("A senha do perfil não pode ser vazia.")
                        continue

                    novo_perfil = Perfil(nome, senha)
                    usuario.adicionar_perfil(novo_perfil)
                    print(f"Perfil '{nome}' criado com sucesso!")
                    self.sistema.salvar_dados()

                    if input("\nDeseja criar outro perfil? (s/n): ").lower() != 's':
                        # Auto-login com o perfil recém-criado
                        usuario.perfil_atual = novo_perfil
                        print(f"\nPerfil '{novo_perfil.nome}' selecionado automaticamente.")
                        limpar_tela()
                        self.menu_principal(usuario)
                        # Após sair do menu principal, o loop de criação de perfil é encerrado
                        # e o usuário volta para a tela de seleção de perfis.
                        break
            elif opcao == "3":
                if not usuario.perfis:
                    print("Nenhum perfil para excluir.")
                    continue

                nome_perfil = input("Digite o nome do perfil a ser excluído: ").strip()
                perfil_a_excluir = next((p for p in usuario.perfis if p.nome.lower() == nome_perfil.lower()), None)

                if not perfil_a_excluir:
                    print("Perfil não encontrado.")
                    continue

                confirmacao = 's'
                if perfil_a_excluir.senhas:
                    confirmacao = input(f"O perfil '{perfil_a_excluir.nome}' contém senhas salvas. Deseja realmente excluí-lo? (s/n): ").lower()

                if confirmacao == 's':
                    if usuario.remover_perfil(perfil_a_excluir.nome):
                        print(f"Perfil '{perfil_a_excluir.nome}' excluído com sucesso!")
                        self.sistema.salvar_dados()
                else:
                    print("Exclusão cancelada.")
            elif not opcao: # Opção "Sair"
                break
            else:
                print("Opção inválida!")

    def menu_gerenciar_senhas(self, usuario):
        """
        Exibe as senhas e oferece opções para gerenciá-las (Atualizar, Deletar).
        """
        while True:
            limpar_tela()
            print(f"\n=== Gerenciar Senhas | Perfil: {usuario.perfil_atual.nome} ===")

            # visualizar_senhas retorna False se não houver senhas
            if not self.sistema.visualizar_senhas(usuario):
                input("\nPressione Enter para voltar...")
                break

            print("\nOpções de Gerenciamento:")
            print("1. Atualizar uma senha")
            print("2. Deletar uma senha")
            
            opcao = input("Escolha uma opção (ou pressione Enter para voltar): ").strip()

            if opcao == "1":
                # Inicia uma sessão de atualização de senhas
                while True:
                    # A lista de senhas já está visível. A função abaixo pede o índice e a nova senha.
                    self.sistema.atualizar_senha(usuario)

                    if input("\nDeseja atualizar outra senha? (s/n): ").lower() != 's':
                        break  # Encerra a sessão de atualização
                    else:
                        # Se for continuar, limpa a tela e mostra a lista atualizada
                        limpar_tela()
                        print(f"\n=== Gerenciar Senhas | Perfil: {usuario.perfil_atual.nome} ===")
                        self.sistema.visualizar_senhas(usuario)
                
                # Ao sair da sessão de atualização, limpa a tela e volta para o menu principal
                limpar_tela()
                break
            elif opcao == "2":
                self.sistema.deletar_senha(usuario)
                input("\nPressione Enter para continuar...")
            elif not opcao: # Opção "Voltar"
                break
            else:
                print("Opção inválida!")
                input("\nPressione Enter para continuar...")

    def menu_principal(self, usuario):
        """
        Exibe o menu principal do perfil do usuário e permite acessar funcionalidades do sistema.
        """
        perfil = usuario.perfil_atual
        while True:
            limpar_tela()
            print(f"\n=== Menu Principal | Perfil: {perfil.nome} ===")
            print("1. Cadastrar nova senha")
            print("2. Gerenciar senhas salvas")
            print("3. Gerar nova senha")
            
            opcao = input("Escolha uma opção (ou pressione Enter para voltar): ").strip()

            if opcao == "1":
                self.sistema.cadastrar_senha(usuario)
            elif opcao == "2":
                self.menu_gerenciar_senhas(usuario)
            elif opcao == "3":
                self.sistema.gerar_senha(usuario)
            elif not opcao: # Opção "Voltar"
                usuario.perfil_atual = None
                break
            else:
                print("Opção inválida!")