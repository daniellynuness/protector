# Protector - Gerenciador de Senhas Seguro

Bem-vindo ao **Protector**, um gerenciador de senhas desenvolvido como parte do projeto interdisciplinar para o curso de Sistemas de Informação I da Universidade UFRPE. Este projeto visa oferecer uma solução prática, segura e eficiente para o gerenciamento de contas e senhas, utilizando boas práticas de programação e segurança.

## 🛠️ Funcionalidades

- **Cadastro de Usuários**:
  - Armazena informações como nome, e-mail, login e senha.
  - Senhas são protegidas utilizando hashing seguro (SHA-256).

- **Login Seguro**:
  - Validação de credenciais com hash de senha.
  - Bloqueio temporário de usuários após múltiplas tentativas de login falhas (15 minutos).
  - Simulação de envio de e-mail em casos de bloqueio.

- **Gerenciamento de Senhas**:
  - Cadastro, visualização, atualização e exclusão de senhas de forma simples.
  - Classificação de senhas (Fraca, Média, Forte) com base em critérios de complexidade.

- **Geração de Senhas Seguras**:
  - Geração de senhas aleatórias com caracteres personalizados (letras, números e símbolos especiais).

- **Interface de Linha de Comando (CLI)**:
  - Menus intuitivos para navegação e interação com o sistema.

## 🔒 Segurança

- **Hashing**: Senhas são armazenadas utilizando o algoritmo SHA-256, garantindo que elas nunca sejam salvas em texto plano.
- **Proteção contra Força Bruta**: Bloqueio temporário após 3 tentativas de login incorretas.
- **Validação de E-mail**: Apenas e-mails de domínios autorizados são aceitos para cadastro (`@gmail.com`, `@ufrpe.br`).

## 🚀 Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/daniellynuness/protector.git
   cd protector
   ```

2. Execute o programa:
   ```bash
   python gerenciador.py
   ```

3. Siga as instruções exibidas no terminal para:
   - Cadastrar um novo usuário.
   - Fazer login com as credenciais cadastradas.
   - Gerenciar suas senhas.

## 📂 Estrutura do Projeto

```plaintext
protector/
├── gerenciador.py   # Código principal do gerenciador de senhas
├── README.md        # Documentação do projeto
```

## ✨ Exemplos de Uso

### Cadastro de Usuário

Ao iniciar o programa, selecione a opção **1. Cadastro** no menu inicial e forneça as informações solicitadas (nome, e-mail, login e senha).

### Login

Após cadastrar seu usuário, selecione a opção **2. Login** no menu inicial e insira suas credenciais.

### Gerenciamento de Senhas

Após realizar o login, você terá acesso ao menu principal, onde poderá:
- **Cadastrar Senhas**: Adicione novas senhas com títulos descritivos.
- **Visualizar Senhas**: Consulte suas senhas salvas.
- **Atualizar Senhas**: Altere senhas já cadastradas.
- **Deletar Senhas**: Remova senhas que não são mais necessárias.
- **Gerar Senhas**: Crie senhas seguras de forma automática.

### Bloqueio de Login

Caso insira as credenciais incorretas 3 vezes consecutivas, o sistema bloqueará o login por 15 minutos e exibirá uma mensagem informativa. Uma simulação de envio de e-mail será exibida no terminal.

## ⚙️ Tecnologias Utilizadas

- **Python 3.10+**
- Módulos padrão do Python:
  - `hashlib` para hashing de senhas.
  - `secrets` para geração de senhas seguras.
  - `string` para manipulação de caracteres.
  - `time` para gestão de bloqueios temporários.
  - `os` para manipulação do terminal.
  - `re` para validação com expressões regulares.


## 📜 Licença

Este projeto é de uso acadêmico e foi desenvolvido para a disciplina de Projeto Interdisciplinar de Sistemas de Informação I na Universidade UFRPE.

## 👩‍💻 Desenvolvedores

- **Danielly Nunes**
  - [GitHub](https://github.com/daniellynuness)
  - [LinkedIn](https://www.linkedin.com/in/danielly-nunes/)
- **Luiz Vinicius**
  - [GitHub](https://github.com/lluizdevv)
  - [LinkedIn](https://www.linkedin.com/in/luizviniciuss/)

---
**Nota**: Este projeto é uma demonstração acadêmica e não deve ser usado como uma solução de gerenciamento de senhas em produção sem melhorias adicionais de segurança.
