import hashlib # para gerar hashes seguros das senhas
import secrets # para gerar senhas aleatórias seguras
import string # para manipular caracteres
import time # para manipular o tempo
import os  # para limpar a tela 
import re #para usar regex

class Usuario:
    """
    Representa um usuário no sistema de gerenciamento de senhas.
    """
    def __init__(self, nome, email, login, senha):
        self.nome = nome
        self.email = email
        self.login = login
        self.senha_hash = self._hash_senha(senha)
        self.senhas = []  # Lista para armazenar as senhas do usuário
        self.tentativas = 0  # Contador de tentativas de login
        self.bloqueado_ate = None  # Timestamp para bloqueio de login

    @staticmethod
    def _hash_senha(senha):
        """
        Gera o hash seguro da senha.
        """
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha):
        """
        Verifica se a senha = hash armazenado.
        """
        return self.senha_hash == self._hash_senha(senha)


class SistemaGerenciadorSenhas:
    """
    Classe que gerencia o sistema de usuários e senhas.
    """

    def __init__(self):
        self.usuarios = {}  # armazenar usuários no formato {login: Usuario}

    def limpar_tela(self):
        """
        Limpa a tela do terminal.
        """
        time.sleep(3)  # 3 segundos para limpar a tela
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception: # tratamento de erros
            print("Não foi possivel limpar  tela. Continuando...")

    def enviar_email(self, destinatario, mensagem):
        """
        Simula o envio de um e-mail para o destinatário, informando que após
        3 tentativas (sem sucesso) de login ele ficará bloqueado do sistema por 15 minutos.
        """
        print("\n=== Simulação de Envio de E-mail ===")
        print(f"Para: {destinatario}")
        print(f"Assunto: Tentativas de Login Bloqueadas")
        print(f"Mensagem: {mensagem}")

    def menu_inicial(self):
        """
        Exibe o menu inicial do sistema e permite ao usuário escolher entre
        cadastro, login ou sair.
        """
        while True:
            print("\n=== Menu Inicial ===")
            print("1. Cadastro")
            print("2. Login")
            print("0. Sair")
            opcao = input("Escolha uma opção: ").stripe()

            if opcao == "1":
                self.cadastrar_usuario()
            elif opcao == "2":
                usuario = self.login_usuario()
                if usuario:
                    self.menu_principal(usuario)
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

    def cadastrar_usuario(self):
        """
        Permite ao usuário cadastrar um novo login no sistema.
        Valida e-mails e verifica duplicidade de login ou e-mail.
        """
        print("\n=== Cadastro ===")
        nome = input("Nome: ")
        email = input("Email: ")
        login = input("Login: ")
        senha = input("Senha: ")

        # validar e-mail
        dominios_permitidos = ["@gmail.com", "@ufrpe.br", "@uorak.com"] #o dominio @uorak.com é de um email temporario, usado para fins de teste
        email = email.strip() # remove espaços em branco
        if not any(email.endswith(dominio) for dominio in dominios_permitidos):
            print("E-mail inválido! Permitidos apenas: @gmail.com, @ufrpe.br, @uorak.com.")
            self.limpar_tela()
            self.cadastrar_usuario()
            return

        # verifica se usuario ou e-mail já está cadastrado
        if any(u.email == email or u.login == login for u in self.usuarios.values()):
            print("E-mail ou login já cadastrado! Redirecionando para o login...")
            self.limpar_tela()
            self.login_usuario()
            return

        # cria o usuário
        self.usuarios[login] = Usuario(nome, email, login, senha)
        print("Cadastro realizado com sucesso!")
        self.limpar_tela()
        self.menu_inicial()

    def login_usuario(self):
        """
        Gerencia o login do usuário, permitindo até 3 tentativas de acesso.
        Redireciona para cadastro caso o login não exista.
        """
        print("\n=== Login ===")
        for _ in range(3):
            login = input("Login: ")
            senha = input("Senha: ")

            usuario = self.usuarios.get(login)
            if usuario:
                # verifica se o usuário está bloqueado
                if usuario.bloqueado_ate and time.time() < usuario.bloqueado_ate:
                    tempo_restante = int((usuario.bloqueado_ate - time.time()) / 60)
                    print(f"Usuário bloqueado! Tente novamente em {tempo_restante} minutos.")
                    return None

                if usuario.verificar_senha(senha):
                    print(f"Bem-vindo(a), {usuario.nome}!")
                    self.limpar_tela()
                    return usuario
                else:
                    print("Senha incorreta!")
            else:
                print("Login não encontrado! Redirecionando para o cadastro...")
                self.limpar_tela()
                self.cadastrar_usuario()
                return None

            usuario.tentativas += 1 

        # bloqueia o usuário após 3 tentativas
        if usuario and usuario.tentativas >= 3:
            usuario.bloqueado_ate = time.time() + 15 * 60  # bloqueio por 15 minutos
            mensagem = "Você foi bloqueado por falhar 3 vezes no login. Tente novamente após 15 minutos."
            print(mensagem)
            self.enviar_email(usuario.email, mensagem)  # simula o envio de e-mail
        else:
            print("Login não encontrado! Verifique seus dados.")
        return None

    def menu_principal(self, usuario):
        """
        Exibe o menu principal do sistema após o login.
        Permite ao usuário gerenciar senhas ou gerar novas.
        """
        while True:
            print("\n=== Menu Principal ===")
            print("1. Cadastrar senhas")
            print("2. Visualizar senhas")
            print("3. Atualizar senhas")
            print("4. Deletar senhas")
            print("5. Gerar senhas")
            print("0. Sair")
            opcao = input("Escolha uma opção: ").stripe()

            if opcao == "1":
                self.cadastrar_senha(usuario)
            elif opcao == "2":
                self.visualizar_senhas(usuario)
            elif opcao == "3":
                self.atualizar_senha(usuario)
            elif opcao == "4":
                self.deletar_senha(usuario)
            elif opcao == "5":
                self.gerar_senha()
            elif opcao == "0":
                print("Deslogando...")
                break
            else:
                print("Opção inválida!")

    def cadastrar_senha(self, usuario):
        """
        Permite ao usuário cadastrar senhas associadas à sua conta.
        Avalia a força da senha e oferece feedback.
        """
        while True:
            print("\n=== Cadastrar Senha ===")
            titulo = input("Título da página/serviço: ")
            # garantir que os titulos das paginas não se repitam
            if any (credencial['titulo'] == titulo for credencial in usuario.senhas):
                print("Este título já está cadastrado. Escolha outro título.")
                selfie.cadastrar_senha()
                return
            senha = input("Senha: ")

            # avalia a força da senha
            classificacao = self.classificar_senha(senha)
            print("Senha cadastrada com sucesso!")
            print(f"\nA sua senha cadastrada foi classificada como: {classificacao}")

            # feedback sobre as senhas
            if classificacao == "Fraca":
                print(f"\nMotivo: A senha é curta e/ou possui baixa diversidade de caracteres.")
                print(f"\nSugestão: Gere uma senha forte utilizando o gerador de senhas.")
            elif classificacao == "Média":
                print(f"\nMotivo: A senha tem comprimento moderado, mas pode melhorar na diversidade de caracteres.")
                print(f"\nSugestão: Considere gerar uma senha mais forte.")
            else:
                print(f"\nA senha cadastrada é considerada forte. Bom trabalho!")

            # armazena a senha no usuário
            usuario.senhas.append({"titulo": titulo, "senha": senha})

            # pergunta se quer cadastrar outra senha
            cadastrar_outra = input("Deseja cadastrar outra senha? (s/n): ").lower()
            if cadastrar_outra != 's':
                self.limpar_tela()
                break
    
    def visualizar_senhas(self, usuario):
        """
        Permite ao usuário visualizar as senhas cadastradas.
        """
        print("\n=== Visualizar Senhas ===")
        if not usuario.senhas:
            print("Nenhuma senha cadastrada. Redirecionando para o cadastro de senhas...")
            self.limpar_tela()
            self.cadastrar_senha(usuario)
            return

        try: # tratameno de erros
            for idx, credencial in enumerate(usuario.senhas, 1):
                print(f"{idx}. {credencial['titulo']} - {credencial['senha']}")
        except Exception as e:
            print(f"Ocorreu um erro ao listar as senhas: {e}")

    @staticmethod
    def gerar_senha():
        """
        Gera uma senha com comprimento definido pelo usuário.
        O tamanho deve estar entre 8 e 20 caracteres.
        """
        while True:
            try:
                tamanho = int(input("Digite o tamanho da senha a ser gerada (entre 8 e 20 caracteres): "))
                if tamanho < 8:
                    print("O tamanho da senha deve ser no mínimo 8 caracteres.")
                    continue
                elif tamanho > 20:
                    print("O tamanho da senha deve ser no máximo 20 caracteres.")
                    continue

                # geração da senha
                caracteres = string.ascii_letters + string.digits + string.punctuation
                senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
                print(f"Senha gerada: {senha}")

                # perguntar se o usuário deseja gerar outra senha
                gerar_novamente = input("Deseja gerar outra senha? (s/n): ").lower()
                if gerar_novamente != 's':
                    break
            except ValueError:
                print("Por favor, insira um número válido.")

    def atualizar_senha(self, usuario):
        """
        Permite ao usuário atualizar as senhas cadastradas.
        """
        while True:
            print("\n=== Atualizar Senha ===")
            if not usuario.senhas:
                print("Nenhuma senha cadastrada. Retornando ao menu principal...")
                self.limpar_tela()
                return

            # exibe a lista de senhas 
            for idx, credencial in enumerate(usuario.senhas, 1):
                print(f"{idx}. {credencial['titulo']} - {credencial['senha']}")

            try:
                indice = int(input("Escolha o número da senha para atualizar: ")) - 1
                if 0 <= indice < len(usuario.senhas):
                    nova_senha = input("Digite a nova senha: ")
                    usuario.senhas[indice]["senha"] = nova_senha
                    print("Senha atualizada com sucesso!")
                else:
                    print("Índice inválido! Tente novamente.")
                    self.limpar_tela()
                    continue
            except ValueError:
                print("Entrada inválida! Digite um número válido.")
                self.limpar_tela()
                continue

            # pergunta se quer atualizar outra senha
            atualizar_outra = input("Deseja atualizar outra senha? (s/n): ").lower()
            if atualizar_outra != 's':
                self.limpar_tela()
                break

    def deletar_senha(self, usuario):
        while True:
            print("\n=== Deletar Senha ===")
            if not usuario.senhas:
                print("Nenhuma senha cadastrada. Retornando ao menu principal...")
                self.limpar_tela()
                return

            # exibe a lista de senhas 
            for idx, credencial in enumerate(usuario.senhas, 1):
                print(f"{idx}. {credencial['titulo']} - {credencial['senha']}")

            try:
                indice = int(input("Escolha o número da senha para deletar: ")) - 1
                if 0 <= indice < len(usuario.senhas):
                    usuario.senhas.pop(indice)
                    print("Senha deletada com sucesso!")
                else:
                    print("Índice inválido! Tente novamente.")
                    self.limpar_tela()
                    continue
            except ValueError:
                print("Entrada inválida! Digite um número válido.")
                self.limpar_tela()
                continue

            # pergunta se quer deletar outra senha
            deletar_outra = input("Deseja deletar outra senha? (s/n): ").lower()
            if deletar_outra != 's':
                self.limpar_tela()
                break
              
    @staticmethod
    def classificar_senha(senha):
        # verifica comprimento
        comprimento = len(senha)

        # define padrões para tipos de caracteres
        tem_maiuscula = bool(re.search(r'[A-Z]', senha))
        tem_minuscula = bool(re.search(r'[a-z]', senha))
        tem_numero = bool(re.search(r'\d', senha))
        tem_especial = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', senha))

        # conta os grupos de caracteres
        diversidade = sum([tem_maiuscula, tem_minuscula, tem_numero, tem_especial])

        # classifica a senha com base nos critérios
        if comprimento < 8 or diversidade < 2:
            return "Fraca"
        elif 8 <= comprimento <= 10 and diversidade >= 2:
            return "Média"
        elif comprimento > 10 and diversidade >= 3:
            return "Forte"
        else:
            return "Fraca"


# Inicia o programa
if __name__ == "__main__":
    sistema = SistemaGerenciadorSenhas()
    sistema.menu_inicial()