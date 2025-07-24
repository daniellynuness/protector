# Protector

## Sobre

Este projeto foi desenvolvido para a disciplina Projeto Interdisciplinar de Sistemas de Informação I da UFRPE (Universidade Federal Rural de Pernambuco).

## Descrição

Protector é uma aplicação Python orientada a objetos que oferece um sistema completo de gerenciamento de senhas e usuários. O projeto implementa um CRUD completo para senhas e usuários, permitindo o cadastro, leitura, atualização e exclusão dessas informações.

Principais funcionalidades:

- **CRUD de Senhas**: Permite gerenciar senhas de forma segura.
- **CRUD de Perfil de Usuário**: Cadastro, consulta, edição e exclusão de perfis.
- **Armazenamento em JSON**: As informações dos usuários são salvas em um arquivo JSON, garantindo persistência dos dados.
- **Consumo da API Have I Been Pwned**: Integração para verificar se senhas já foram comprometidas em vazamentos conhecidos.
- **Gerador de Senhas Fortes**: Gera senhas seguras automaticamente para os usuários.
- **Bloqueio de Usuário e Notificação por E-mail**: Após múltiplas tentativas de login inválidas, o usuário é bloqueado e recebe um e-mail de notificação. O envio de e-mails está totalmente funcional através de um servidor online.
- **Orientação a Objetos**: O projeto foi estruturado utilizando os conceitos de orientação a objetos para facilitar manutenção e escalabilidade.

## Demonstrações

A seguir, exemplos do funcionamento do sistema no terminal:

<img width="491" height="161" alt="Captura de tela 2025-07-15 191722" src="https://github.com/user-attachments/assets/cb00e9d0-742f-45f8-8003-504207f2a999" />

*Menu inicial do sistema: opções para cadastro de usuário e login.*

<img width="511" height="226" alt="Captura de tela 2025-07-15 191919" src="https://github.com/user-attachments/assets/d661b6d2-8bec-4ad8-80ee-5004033665b2" />

*Gerenciamento de perfis do usuário: seleção, criação e exclusão de perfis.*

<img width="686" height="236" alt="Captura de tela 2025-07-15 192120" src="https://github.com/user-attachments/assets/f144dc4c-4217-40de-bbf4-d2cf9fc94649" />

*Bloqueio de conta e envio de e-mail após múltiplas tentativas de login sem sucesso.*

<img width="846" height="231" alt="Captura de tela 2025-07-24 155208" src="https://github.com/user-attachments/assets/ee0c3e9c-2c83-467e-b35e-f3b9510ac551" />

*Alerta de segurança avisando ao usuário quantas vezes a senha que ele utilizou no cadastro já foi vazada.*

<img width="365" height="190" alt="Captura de tela 2025-07-24 155328" src="https://github.com/user-attachments/assets/2055a036-0c3a-478c-a650-e86437539439" />

*Após o usuário realizar o cadastro e login na conta, ele poderá criar seu perfil e ter acesso ao menu principal com todas as funcionalidades do sistema.*


## Tecnologias e Bibliotecas Utilizadas

- `requests`
- `hashlib`
- `re`
- `os`
- `time`
- `string`
- `secrets`
- `smtplib`
- `json`

## Instalação

### Pré-requisitos

- Python (recomenda-se a versão mais recente)

### Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalá-las, execute:

```bash
pip install -r requirements.txt
```

## Como utilizar

1. Clone o repositório:
    ```bash
    git clone https://github.com/daniellynuness/protector.git
    cd protector
    ```
2. Instale as dependências conforme instruções acima.
3. Execute o sistema.

## Estrutura do Projeto

```
protector/
├── src/      # Código-fonte principal
├── requirements.txt
└── README.md
```

## Autores

- [@daniellynuness](https://github.com/daniellynuness)
- [@lluizdevv](https://github.com/lluizdevv)

## Licença

Este projeto não possui licença específica no momento.
