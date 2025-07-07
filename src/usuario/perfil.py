import hashlib

class Perfil:
    """
    Representa um perfil de acesso do usuário.
    """
    PERMISSOES_PADRAO = [
        "Cadastrar Senhas",
        "Visualizar Senhas",
        "Atualizar Senhas",
        "Deletar Senhas",
        "Gerar Senhas"
    ]

    def __init__(self, nome, senha, permissoes=None):
        self.nome = nome
        self.senha_hash = self._hash_senha(senha)
        self.permissoes = self.PERMISSOES_PADRAO.copy()
        self.senhas = []
        self.senhas_geradas = []

    @staticmethod
    def _hash_senha(senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha):
        return self.senha_hash == self._hash_senha(senha)