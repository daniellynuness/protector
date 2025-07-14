import hashlib
import os
from .perfil import Perfil

class Usuario:
    """
    Representa um usuário no sistema de gerenciamento de senhas.
    """
    def __init__(self, nome, email, login, senha):
        self.nome = nome
        self.email = email
        self.login = login
        # Gerar um salt e armazenar o hash
        self.salt = os.urandom(16).hex()
        self.senha_hash = self._hash_senha(senha, self.salt)
        self.tentativas = 0
        self.bloqueado_ate = None
        self.perfis = []
        self.perfil_atual = None

    @staticmethod
    def _hash_senha(senha, salt):
        """        
        Gera um hash SHA-256 "salgado" da senha fornecida.
        """
        senha_salted = salt.encode() + senha.encode()
        return hashlib.sha256(senha_salted).hexdigest()

    def verificar_senha(self, senha):
        """
        Verifica se a senha fornecida corresponde à senha armazenada do usuário.
        """
        return self.senha_hash == self._hash_senha(senha, self.salt)

    def adicionar_perfil(self, perfil):
        """Adiciona um novo perfil à lista de perfis do usuário."""
        self.perfis.append(perfil)

    def remover_perfil(self, nome_perfil):
        """Remove um perfil da lista de perfis do usuário pelo nome."""
        perfil_a_remover = next((p for p in self.perfis if p.nome.lower() == nome_perfil.lower()), None)
        if perfil_a_remover:
            self.perfis.remove(perfil_a_remover)
            return True
        return False

    def selecionar_perfil(self, nome_perfil, senha_perfil):
        """        
        Seleciona um perfil ativo do usuário com base no nome e senha fornecidos.
        """
        for perfil in self.perfis:
            if perfil.nome.lower() == nome_perfil.lower() and perfil.verificar_senha(senha_perfil):
                self.perfil_atual = perfil
                return True
        return False
