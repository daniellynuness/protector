import secrets
import string

def gerar_senha(tamanho=None):
    """
    Gera uma senha forte com comprimento definido pelo usuário.
    O tamanho deve estar entre 8 e 20 caracteres.
    A senha sempre conterá letras maiúsculas, minúsculas, números e caracteres especiais.
    """
<<<<<<< HEAD
    try:
        if tamanho is None:
            tamanho = int(input("Digite o tamanho da senha a ser gerada (entre 8 e 20 caracteres): "))
        
        if tamanho < 8:
            print("O tamanho da senha deve ser no mínimo 8 caracteres.")
            return None
        elif tamanho > 20:
            print("O tamanho da senha deve ser no máximo 20 caracteres.")
            return None

        # Define os grupos de caracteres
        maiusculas = string.ascii_uppercase
        minusculas = string.ascii_lowercase
        numeros = string.digits
        especiais = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # Garante pelo menos um caractere de cada tipo
        senha = [
            secrets.choice(maiusculas),
            secrets.choice(minusculas),
            secrets.choice(numeros),
            secrets.choice(especiais)
        ]

        # Completa o restante da senha
        caracteres_restantes = tamanho - 4
        todos_caracteres = maiusculas + minusculas + numeros + especiais
        
        senha.extend(secrets.choice(todos_caracteres) for _ in range(caracteres_restantes))
        
        # Embaralha a senha para não ter um padrão previsível
        secrets.SystemRandom().shuffle(senha)
        
        # Converte a lista em string
        senha_final = ''.join(senha)
        
        # Mostra a senha gerada
        print(f"\nSenha gerada: {senha_final}")
        return senha_final

    except ValueError:
        print("Por favor, insira um número válido.")
        return None
    except Exception as e:
        print(f"Erro ao gerar senha: {str(e)}")
        return None
=======
    while True:
        try:
            if tamanho is None:
                tamanho = int(input("Digite o tamanho da senha a ser gerada (entre 8 e 20 caracteres): "))
            
            if tamanho < 8:
                print("O tamanho da senha deve ser no mínimo 8 caracteres.")
                tamanho = None
                continue
            elif tamanho > 20:
                print("O tamanho da senha deve ser no máximo 20 caracteres.")
                tamanho = None
                continue

            # Define os grupos de caracteres
            maiusculas = string.ascii_uppercase
            minusculas = string.ascii_lowercase
            numeros = string.digits
            especiais = "!@#$%^&*()_+-=[]{}|;:,.<>?"

            # Garante pelo menos um caractere de cada tipo
            senha = [
                secrets.choice(maiusculas),  # uma maiúscula
                secrets.choice(minusculas),  # uma minúscula
                secrets.choice(numeros),     # um número
                secrets.choice(especiais)    # um caractere especial
            ]

            # Completa o restante da senha
            caracteres_restantes = tamanho - 4  # subtrai os 4 caracteres obrigatórios
            todos_caracteres = maiusculas + minusculas + numeros + especiais
            
            senha.extend(secrets.choice(todos_caracteres) for _ in range(caracteres_restantes))
            
            # Embaralha a senha para não ter um padrão previsível
            secrets.SystemRandom().shuffle(senha)
            
            # Converte a lista em string
            senha_final = ''.join(senha)
            
            # Mostra a senha gerada
            print(f"\nSenha gerada: {senha_final}")

        except ValueError:
            print("Por favor, insira um número válido.")
        except Exception as e:
            print(f"Erro ao gerar senha: {str(e)}")
            return None
>>>>>>> c5bbacc84a700283a24a18c1bcf8f376e5317076
