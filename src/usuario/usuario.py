import hashlib
from .perfil import Perfil

class Usuario:
    """
    Representa um usuário no sistema de gerenciamento de senhas.
    """
    def __init__(self, nome, email, login, senha):
        self.nome = nome
        self.email = email
        self.login = login
        self.senha_hash = self._hash_senha(senha)
        self.tentativas = 0
        self.bloqueado_ate = None
        self.perfis = []
        self.perfil_atual = None

    @staticmethod
    def _hash_senha(senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha):
        return self.senha_hash == self._hash_senha(senha)

    def adicionar_perfil(self, perfil):
        self.perfis.append(perfil)

    def selecionar_perfil(self, nome_perfil, senha_perfil):
        for perfil in self.perfis:
            if perfil.nome == nome_perfil and perfil.verificar_senha(senha_perfil):
                self.perfil_atual = perfil
                return True
        return False