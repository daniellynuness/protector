import re
import hashlib
import requests

def classificar_senha(senha):
    """
    Classifica a força da senha com base em critérios de segurança.
    """
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

def verificar_senha_vazada(senha):
    """
    Verifica se a senha foi vazada usando a API do Have I Been Pwned.
    Retorna o número de vezes que a senha foi vazada, ou 0 se não foi encontrada.
    Retorna -1 em caso de erro na verificação (ex: sem internet).
    """
    try:
        # 1. Gera o hash SHA-1 da senha, conforme exigido pela API
        sha1_senha = hashlib.sha1(senha.encode('utf-8')).hexdigest().upper()
        
        # 2. Divide o hash para k-Anonymity (envia apenas os 5 primeiros caracteres)
        prefixo, sufixo = sha1_senha[:5], sha1_senha[5:]
        
        # 3. Faz a requisição para a API
        url = f'https://api.pwnedpasswords.com/range/{prefixo}'
        response = requests.get(url, timeout=5) # Timeout de 5 segundos
        response.raise_for_status() # Lança exceção para status de erro (4xx ou 5xx)

        # 4. Procura o sufixo do nosso hash na resposta da API
        hashes_vazados = (line.split(':') for line in response.text.splitlines())
        for hash_sufixo, count in hashes_vazados:
            if hash_sufixo == sufixo:
                return int(count) # Encontrou, retorna a contagem de vazamentos
        
        return 0 # Senha não encontrada na lista de vazamentos
    except requests.RequestException:
        print("\n[Aviso] Não foi possível verificar se a senha já foi vazada. Verifique sua conexão com a internet.")
        return -1