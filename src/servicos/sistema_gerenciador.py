import time
import json
import os
from src.usuario.usuario import Usuario
from src.usuario.perfil import Perfil
from src.utilitario.validadores import classificar_senha, verificar_senha_vazada
from src.utilitario.geradores import gerar_senha
from src.servicos.email import Email
from src.utilitario.limpeza import limpar_tela

class SistemaGerenciadorSenhas:
    def __init__(self):
        self.usuarios = {}
        self.email_service = Email()
        self.arquivo_dados = "dados_sistema.json"
        self.carregar_dados()

    def cadastrar_usuario(self):
        """Cadastra um novo usuário no sistema"""
        print("\n=== Cadastro ===")
        try:
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            login = input("Login: ").strip()

            while True:
                senha = input("Senha: ").strip()
                if not senha:
                    print("A senha não pode estar vazia!")
                    continue

                contagem_vazamento = verificar_senha_vazada(senha)
                if contagem_vazamento > 0:
                    print(f"\n[ALERTA DE SEGURANÇA] Esta senha foi encontrada em {contagem_vazamento} vazamentos de dados conhecidos.")
                    print("Para sua segurança, recomendamos fortemente que você escolha outra senha.")
                elif contagem_vazamento == -1:
                    print("\n[Aviso] Não foi possível verificar se a senha foi vazada. Prossiga com cautela.")
                break

            if not all([nome, email, login]):
                print("Os campos nome, email e login são obrigatórios!")
                limpar_tela()
                return self.cadastrar_usuario()

            dominios_permitidos = ["@gmail.com", "@ufrpe.br", "@coasah.com"]
            if not any(email.endswith(dominio) for dominio in dominios_permitidos):
                print("E-mail inválido! Permitidos apenas: @gmail.com e @ufrpe.br")
                limpar_tela()
                return self.cadastrar_usuario()

            if any(u.email == email or u.login == login for u in self.usuarios.values()):
                print("E-mail ou login já cadastrado!")
                limpar_tela()
                return self.login_usuario()

            self.usuarios[login] = Usuario(nome, email, login, senha)
            usuario = self.usuarios[login]
            print("Cadastro realizado com sucesso!")
            limpar_tela()
            return usuario

        except Exception as e:
            print(f"Erro no cadastro: {str(e)}")
            limpar_tela()
            return None
        
    def login_usuario(self):
        """Realiza o login do usuário"""
        print("\n=== Login ===")
        login = input("Login: ").strip()
        usuario = self.usuarios.get(login)
        if not usuario:
            print("Login não encontrado!")
            return None

        while True:
            if usuario.bloqueado_ate and time.time() < usuario.bloqueado_ate:
                tempo_restante = int((usuario.bloqueado_ate - time.time()) / 60)
                print(f"Usuário bloqueado! Tente novamente em {tempo_restante} minutos.")
                return None

            senha = input("Senha: ").strip()
            if usuario.verificar_senha(senha):
                print(f"Bem-vindo(a), {usuario.nome}!")
                usuario.tentativas = 0
                limpar_tela()
                return usuario

            usuario.tentativas += 1
            print("Senha incorreta!")

            if usuario.tentativas >= 3:
                usuario.bloqueado_ate = time.time() + (15 * 60)  # 15 minutos
                usuario.tentativas = 0  # zera tentativas após bloquear
                mensagem = "Conta bloqueada por excesso de tentativas. Tente novamente em 15 minutos."
                print(mensagem)
                self.email_service.enviar_email(usuario.email, mensagem)
                return None

    def cadastrar_senha(self, usuario):
        """Cadastra uma nova senha para o perfil ativo do usuário"""
        perfil = usuario.perfil_atual
        while True:
            print("\n=== Cadastrar Senha ===")
            titulo = input("Título da página/serviço: ").strip()
            if any(credencial['titulo'] == titulo for credencial in perfil.senhas):
                print("Este título já está cadastrado!")
                continue
            senha = input("Digite a senha: ").strip()
            perfil.senhas.append({"titulo": titulo, "senha": senha})
            print("Senha cadastrada com sucesso!")
            if input("Cadastrar outra senha? (s/n): ").lower() != 's':
                break

    def visualizar_senhas(self, usuario):
        """Exibe as senhas do perfil ativo do usuário"""
        perfil = usuario.perfil_atual
        print("\n=== Senhas Cadastradas ===")
        if not perfil.senhas:
            print("Nenhuma senha cadastrada!")
            return

        for idx, credencial in enumerate(perfil.senhas, 1):
            print(f"{idx}. {credencial['titulo']} - {credencial['senha']}")

        limpar_tela()

    def atualizar_senha(self, usuario):
        """Atualiza uma senha existente do perfil ativo"""
        perfil = usuario.perfil_atual
        while True:
            print("\n=== Atualizar Senha ===")
            if not perfil.senhas:
                print("Nenhuma senha cadastrada!")
                limpar_tela()
                return

            self.visualizar_senhas(usuario)
            try:
                idx = int(input("\nEscolha o número da senha para atualizar (0 para cancelar): ")) - 1
                if idx == -1:
                    break
                if 0 <= idx < len(perfil.senhas):
                    nova_senha = input("Nova senha: ").strip()
                    if nova_senha:
                        perfil.senhas[idx]["senha"] = nova_senha
                        print("Senha atualizada com sucesso!")
                else:
                    print("Índice inválido!")
            except ValueError:
                print("Por favor, digite um número válido!")

            if input("\nDeseja atualizar outra senha? (s/n): ").lower() != 's':
                limpar_tela()
                break

    def deletar_senha(self, usuario):
        """Remove uma senha cadastrada do perfil ativo"""
        perfil = usuario.perfil_atual
        while True:
            print("\n=== Deletar Senha ===")
            if not perfil.senhas:
                print("Nenhuma senha cadastrada!")
                limpar_tela()
                return

            self.visualizar_senhas(usuario)
            try:
                idx = int(input("\nEscolha o número da senha para deletar (0 para cancelar): ")) - 1
                if idx == -1:
                    break
                if 0 <= idx < len(perfil.senhas):
                    senha_removida = perfil.senhas.pop(idx)
                    print(f"Senha de {senha_removida['titulo']} removida com sucesso!")
                else:
                    print("Índice inválido!")
            except ValueError:
                print("Por favor, digite um número válido!")

            if input("\nDeseja deletar outra senha? (s/n): ").lower() != 's':
                limpar_tela()
                break

    def gerar_senha(self, usuario):
        """Interface para o gerador de senhas"""
        perfil = usuario.perfil_atual
        print("\n=== Gerador de Senhas ===")
        while True:
            try:
                senha_gerada = gerar_senha()
                if senha_gerada:
                    perfil.senhas_geradas.append(senha_gerada)
                    print(f"Senha gerada: {senha_gerada}")
                    if input("\nDeseja gerar outra senha? (s/n): ").lower() != 's':
                        break
                else:
                    print("Falha ao gerar senha!")
            except Exception as e:
                print(f"Erro: {str(e)}")
                break
        limpar_tela()

    def salvar_dados(self):
        dados = {}
        for login, usuario in self.usuarios.items():
            dados[login] = {
                "nome": usuario.nome,
                "email": usuario.email,
                "login": usuario.login,
                "senha_hash": usuario.senha_hash,
                "perfis": [
                    {
                        "nome": perfil.nome,
                        "senha_hash": perfil.senha_hash,
                        "senhas": perfil.senhas,
                        "senhas_geradas": perfil.senhas_geradas
                    }
                    for perfil in usuario.perfis
                ]
            }
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar_dados(self):
        if not os.path.exists(self.arquivo_dados):
            return
        with open(self.arquivo_dados, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for login, usuario_data in dados.items():
                usuario = Usuario(
                    usuario_data["nome"],
                    usuario_data["email"],
                    usuario_data["login"],
                    "dummy"  # senha não será usada, pois vamos sobrescrever o hash
                )
                usuario.senha_hash = usuario_data["senha_hash"]
                for perfil_data in usuario_data["perfis"]:
                    perfil = Perfil(
                        perfil_data["nome"],
                        "dummy"  # senha não será usada, pois vamos sobrescrever o hash
                    )
                    perfil.senha_hash = perfil_data["senha_hash"]
                    perfil.senhas = perfil_data.get("senhas", [])
                    perfil.senhas_geradas = perfil_data.get("senhas_geradas", [])
                    usuario.perfis.append(perfil)
                self.usuarios[login] = usuario