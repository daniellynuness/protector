import re

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