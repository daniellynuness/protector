import hashlib

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