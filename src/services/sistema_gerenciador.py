import time
import os
from src.models.usuario import Usuario
from src.utils.validadores import classificar_senha
from src.utils.geradores import gerar_senha
from src.services.email_service import EmailService

class SistemaGerenciadorSenhas:
    def __init__(self):
        self.usuarios = {}
        self.email_service = EmailService()

    def limpar_tela(self):
        """Limpa a tela do terminal"""
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

    def cadastrar_usuario(self):
        """Cadastra um novo usuário no sistema"""
        print("\n=== Cadastro ===")
        try:
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            login = input("Login: ").strip()
            senha = input("Senha: ").strip()

            if not all([nome, email, login, senha]):
                print("Todos os campos são obrigatórios!")
                self.limpar_tela()
                return self.cadastrar_usuario()

            dominios_permitidos = ["@gmail.com", "@ufrpe.br", "@uorak.com"]
            if not any(email.endswith(dominio) for dominio in dominios_permitidos):
                print("E-mail inválido! Permitidos apenas: @gmail.com, @ufrpe.br, @uorak.com")
                self.limpar_tela()
                return self.cadastrar_usuario()

            if any(u.email == email or u.login == login for u in self.usuarios.values()):
                print("E-mail ou login já cadastrado!")
                self.limpar_tela()
                return self.login_usuario()

            self.usuarios[login] = Usuario(nome, email, login, senha)
            print("Cadastro realizado com sucesso!")
            self.limpar_tela()
            return self.usuarios[login]

        except Exception as e:
            print(f"Erro no cadastro: {str(e)}")
            self.limpar_tela()
            return None

    def login_usuario(self):
        """Realiza o login do usuário"""
        print("\n=== Login ===")
        for _ in range(3):
            login = input("Login: ").strip()
            senha = input("Senha: ").strip()

            usuario = self.usuarios.get(login)
            if not usuario:
                print("Login não encontrado!")
                return None

            if usuario.bloqueado_ate and time.time() < usuario.bloqueado_ate:
                tempo_restante = int((usuario.bloqueado_ate - time.time()) / 60)
                print(f"Usuário bloqueado! Tente novamente em {tempo_restante} minutos.")
                return None

            if usuario.verificar_senha(senha):
                print(f"Bem-vindo(a), {usuario.nome}!")
                usuario.tentativas = 0
                self.limpar_tela()
                return usuario

            usuario.tentativas += 1
            print("Senha incorreta!")

            if usuario.tentativas >= 3:
                usuario.bloqueado_ate = time.time() + (15 * 60)  # 15 minutos
                mensagem = "Conta bloqueada por excesso de tentativas. Tente novamente em 15 minutos."
                print(mensagem)
                self.email_service.enviar_email(usuario.email, mensagem)
                return None

        return None

    def cadastrar_senha(self, usuario):
        """Cadastra uma nova senha para o usuário"""
        while True:
            print("\n=== Cadastrar Senha ===")
            titulo = input("Título da página/serviço: ").strip()
            
            if any(credencial['titulo'] == titulo for credencial in usuario.senhas):
                print("Este título já está cadastrado!")
                continue
                
            senha = input("Senha: ").strip()
            if not senha:
                print("A senha não pode estar vazia!")
                continue

            classificacao = classificar_senha(senha)
            usuario.senhas.append({"titulo": titulo, "senha": senha})
            
            print(f"\nSenha cadastrada! Classificação: {classificacao}")
            if classificacao != "Forte":
                print("Recomendamos usar o gerador de senhas para maior segurança.")

            if input("\nDeseja cadastrar outra senha? (s/n): ").lower() != 's':
                self.limpar_tela()
                break

    def visualizar_senhas(self, usuario):
        """Exibe as senhas do usuário"""
        print("\n=== Senhas Cadastradas ===")
        if not usuario.senhas:
            print("Nenhuma senha cadastrada!")
            return

        for idx, credencial in enumerate(usuario.senhas, 1):
            print(f"{idx}. {credencial['titulo']} - {credencial['senha']}")
        
        input("\nPressione ENTER para continuar...")
        self.limpar_tela()

    def atualizar_senha(self, usuario):
        """Atualiza uma senha existente"""
        while True:
            print("\n=== Atualizar Senha ===")
            if not usuario.senhas:
                print("Nenhuma senha cadastrada!")
                self.limpar_tela()
                return

            self.visualizar_senhas(usuario)
            try:
                idx = int(input("\nEscolha o número da senha para atualizar (0 para cancelar): ")) - 1
                if idx == -1:
                    break
                if 0 <= idx < len(usuario.senhas):
                    nova_senha = input("Nova senha: ").strip()
                    if nova_senha:
                        usuario.senhas[idx]["senha"] = nova_senha
                        print("Senha atualizada com sucesso!")
                else:
                    print("Índice inválido!")
            except ValueError:
                print("Por favor, digite um número válido!")

            if input("\nDeseja atualizar outra senha? (s/n): ").lower() != 's':
                self.limpar_tela()
                break

    def deletar_senha(self, usuario):
        """Remove uma senha cadastrada"""
        while True:
            print("\n=== Deletar Senha ===")
            if not usuario.senhas:
                print("Nenhuma senha cadastrada!")
                self.limpar_tela()
                return

            self.visualizar_senhas(usuario)
            try:
                idx = int(input("\nEscolha o número da senha para deletar (0 para cancelar): ")) - 1
                if idx == -1:
                    break
                if 0 <= idx < len(usuario.senhas):
                    senha_removida = usuario.senhas.pop(idx)
                    print(f"Senha de {senha_removida['titulo']} removida com sucesso!")
                else:
                    print("Índice inválido!")
            except ValueError:
                print("Por favor, digite um número válido!")

            if input("\nDeseja deletar outra senha? (s/n): ").lower() != 's':
                self.limpar_tela()
                break

    def gerar_senha(self):
        """Interface para o gerador de senhas"""
        print("\n=== Gerador de Senhas ===")
        while True:
            try:
                senha_gerada = gerar_senha()
                if senha_gerada:
                    if input("\nDeseja gerar outra senha? (s/n): ").lower() != 's':
                        break
                else:
                    print("Falha ao gerar senha!")
            except Exception as e:
                print(f"Erro: {str(e)}")
                break
        self.limpar_tela()