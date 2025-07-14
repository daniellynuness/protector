import time
import json
import os
from src.usuario.usuario import Usuario
from src.usuario.perfil import Perfil
from src.utilitario.validadores import verificar_senha_vazada, classificar_senha
from src.utilitario.geradores import gerar_senha
from src.servicos.email import Email
from src.utilitario.limpeza import limpar_tela

class SistemaGerenciadorSenhas:
    """Classe responsável por gerenciar o sistema de senhas, incluindo cadastro, login, e manipulação de senhas."""
    def __init__(self):
        """Inicializa o sistema de gerenciamento de senhas"""
        self.usuarios = {}
        self.email_service = Email()
        self.arquivo_dados = "dados_sistema.json"
        self.carregar_dados()

    def cadastrar_usuario(self):
        """Cadastra um novo usuário no sistema"""
        print("\n=== Cadastro ===")
        while True:
            try:
                nome = input("Nome: ").strip()
                email = input("Email: ").strip()
                usuario = input("Usuário: ").strip()

                if not all([nome, email, usuario]):
                    print("Os campos nome, email e usuário são obrigatórios! Tente novamente.")
                    limpar_tela()
                    continue

                dominios_permitidos = ["@gmail.com", "@ufrpe.br", "@iamtile.com"]
                if not any(email.endswith(dominio) for dominio in dominios_permitidos):
                    print("E-mail inválido! Permitidos apenas: @gmail.com e @ufrpe.br. Tente novamente.")
                    limpar_tela()
                    continue

                if any(u.email == email or u.login == usuario for u in self.usuarios.values()):
                    print("E-mail ou usuário já cadastrado! Tente novamente.")
                    limpar_tela()
                    continue

                # Se todas as verificações passaram, solicita a senha
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

                self.usuarios[usuario] = Usuario(nome, email, usuario, senha)
                usuario = self.usuarios[usuario]
                print("Cadastro realizado com sucesso!")
                self.salvar_dados()
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
            limpar_tela()
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
                self.salvar_dados()
                return None

    def cadastrar_senha(self, usuario):
        """Cadastra uma nova senha para o perfil ativo do usuário, com feedback de segurança."""
        perfil = usuario.perfil_atual
        while True:
            print("\n=== Cadastrar Senha ===")
            titulo = input("Título da página/serviço: ").strip()
            if not titulo:
                print("O título não pode ser vazio.")
                continue

            # Verifica se o título já existe (ignorando maiúsculas/minúsculas)
            if any(credencial['titulo'].lower() == titulo.lower() for credencial in perfil.senhas):
                print("Este título já está cadastrado!")
                continue

            senha = input("Digite a senha: ").strip()
            if not senha:
                print("A senha não pode ser vazia.")
                continue

            # Feedback de segurança
            forca = classificar_senha(senha)
            print(f"Força da senha: {forca}")

            contagem_vazamento = verificar_senha_vazada(senha)
            if contagem_vazamento > 0:
                print(f"[ALERTA DE SEGURANÇA] Esta senha foi encontrada em {contagem_vazamento} vazamentos de dados.")
                print("Recomendamos fortemente que você use uma senha gerada pelo sistema.")
            elif contagem_vazamento == -1:
                print("[Aviso] Não foi possível verificar vazamentos. Prossiga com cautela.")

            perfil.senhas.append({"titulo": titulo, "senha": senha})
            print("Senha cadastrada com sucesso!")
            self.salvar_dados()
            if input("\nCadastrar outra senha? (s/n): ").lower() != 's':
                limpar_tela()
                break

    def visualizar_senhas(self, usuario):
        """Exibe as senhas do perfil ativo do usuário. Retorna True se houver senhas, False caso contrário."""
        perfil = usuario.perfil_atual
        print("\n=== Senhas Cadastradas ===")
        if not perfil.senhas:
            print("Nenhuma senha cadastrada!")
            return False

        for idx, credencial in enumerate(perfil.senhas, 1):
            print(f"{idx}. {credencial['titulo']} - {credencial['senha']}")
        return True

    def atualizar_senha(self, usuario):
        """Atualiza uma senha existente do perfil ativo. A visualização é feita pelo menu."""
        perfil = usuario.perfil_atual
        idx_str = input("\nEscolha o número da senha para atualizar (ou pressione Enter para cancelar): ").strip()

        if not idx_str:
            print("Operação cancelada.")
            return

        if not idx_str.isdigit():
            print("Entrada inválida. Por favor, digite um número.")
            return

        idx = int(idx_str) - 1

        if 0 <= idx < len(perfil.senhas):
            nova_senha = input(f"Nova senha para '{perfil.senhas[idx]['titulo']}': ").strip()
            if not nova_senha:
                print("A nova senha não pode ser vazia. Operação cancelada.")
                return

            # Feedback de segurança para a nova senha
            forca = classificar_senha(nova_senha)
            print(f"Força da senha: {forca}")
            contagem_vazamento = verificar_senha_vazada(nova_senha)
            if contagem_vazamento > 0:
                print(f"[ALERTA DE SEGURANÇA] Esta senha foi encontrada em {contagem_vazamento} vazamentos de dados.")
                if input("Deseja continuar mesmo assim? (s/n): ").lower() != 's':
                    print("Atualização cancelada.")
                    return
            elif contagem_vazamento == -1:
                print("[Aviso] Não foi possível verificar vazamentos. Prossiga com cautela.")

            perfil.senhas[idx]["senha"] = nova_senha
            print("Senha atualizada com sucesso!")
            self.salvar_dados()
        else:
            print("Índice inválido!")

    def deletar_senha(self, usuario):
        """Remove uma senha cadastrada do perfil ativo. A visualização é feita pelo menu."""
        perfil = usuario.perfil_atual
        idx_str = input("\nEscolha o número da senha para deletar (ou pressione Enter para cancelar): ").strip()

        if not idx_str:
            print("Operação cancelada.")
            return

        if not idx_str.isdigit():
            print("Entrada inválida. Por favor, digite um número.")
            return

        idx = int(idx_str) - 1

        if 0 <= idx < len(perfil.senhas):
            confirmacao = input(f"Tem certeza que deseja remover a senha de '{perfil.senhas[idx]['titulo']}'? (s/n): ").lower()
            if confirmacao == 's':
                senha_removida = perfil.senhas.pop(idx)
                print(f"Senha de '{senha_removida['titulo']}' removida com sucesso!")
                self.salvar_dados()
            else:
                print("Deleção cancelada.")
        else:
            print("Índice inválido!")

    def gerar_senha(self, usuario):
        """Gera uma senha aleatória e oferece opções para salvá-la ou usá-la."""
        perfil = usuario.perfil_atual
        
        while True:
            limpar_tela()
            print("\n=== Gerador de Senhas ===")
            
            senha_gerada = gerar_senha()
            if not senha_gerada:
                if input("Falha ao gerar senha. Tentar novamente? (s/n): ").lower() != 's':
                    break
                else:
                    continue

            print(f"\nSenha gerada: {senha_gerada}")
            perfil.senhas_geradas.append(senha_gerada)
            self.salvar_dados()

            print("\nO que deseja fazer com esta senha?")
            print("1. Salvar como uma nova credencial")
            print("2. Usar para atualizar uma credencial existente")
            print("3. Gerar outra senha")
            
            opcao = input("Escolha uma opção (ou pressione Enter para voltar): ").strip()

            if opcao == '1':
                # Salvar como nova
                titulo = input("Título da página/serviço: ").strip()
                if not titulo:
                    print("O título não pode ser vazio.")
                elif any(credencial['titulo'].lower() == titulo.lower() for credencial in perfil.senhas):
                    print("Este título já está cadastrado!")
                else:
                    perfil.senhas.append({"titulo": titulo, "senha": senha_gerada})
                    print("Senha salva com sucesso!")
                    self.salvar_dados()
                input("\nPressione Enter para continuar...")

            elif opcao == '2':
                # Atualizar existente
                limpar_tela()
                print("\n=== Atualizar com Senha Gerada ===")
                print(f"Senha a ser usada: {senha_gerada}")
                if not self.visualizar_senhas(usuario):
                    print("\nNenhuma senha cadastrada para atualizar.")
                else:
                    idx_str = input("\nEscolha o número da senha para atualizar (ou pressione Enter para cancelar): ").strip()
                    if not idx_str:
                        print("Operação cancelada.")
                    elif not idx_str.isdigit():
                        print("Entrada inválida.")
                    else:
                        idx = int(idx_str) - 1
                        if 0 <= idx < len(perfil.senhas):
                            perfil.senhas[idx]["senha"] = senha_gerada
                            print(f"Senha de '{perfil.senhas[idx]['titulo']}' atualizada com sucesso!")
                            self.salvar_dados()
                        else:
                            print("Índice inválido!")
                input("\nPressione Enter para continuar...")

            elif opcao == '3':
                continue # Gera outra senha

            else: # Inclui Enter (opção vazia) e qualquer outra coisa
                break # Sai do gerador
        
        limpar_tela()

    def salvar_dados(self):
        """Salva os dados dos usuários e perfis em um arquivo JSON"""
        dados = {}
        for login, usuario in self.usuarios.items():
            dados[login] = {
                "nome": usuario.nome,
                "email": usuario.email,
                "login": usuario.login,
                "senha_hash": usuario.senha_hash,
                "bloqueado_ate": usuario.bloqueado_ate,
                "tentativas": usuario.tentativas,
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
        """Carrega os dados dos usuários e perfis de um arquivo JSON"""
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
                usuario.bloqueado_ate = usuario_data.get("bloqueado_ate", None)
                usuario.tentativas = usuario_data.get("tentativas", 0)
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
