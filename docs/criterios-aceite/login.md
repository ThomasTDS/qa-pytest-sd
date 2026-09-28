# Login, Cadastro e Logout

Cenários executáveis: `features/login.feature`.

## História de Usuário — Login

- **Como** usuário já cadastrado no Automation Exercise
- **Quero** fazer login informando e-mail e senha
- **Para** acessar minha conta e concluir compras

### Critério 1 – Login com credenciais válidas (TC-001)

- **Dado** que estou na página de login
- **Quando** informo o e-mail e a senha da conta de teste
- **Então** devo ver que estou logado (o nome da conta aparece no cabeçalho)

### Critério 2 – Login com credenciais inválidas (TC-002)

- **Dado** que estou na página de login
- **Quando** informo um e-mail ou senha que não correspondem a nenhuma conta
- **Então** devo ver a mensagem "Your email or password is incorrect!"
- **E** não devo ser autenticado

---

## História de Usuário — Cadastro

- **Como** visitante do site
- **Quero** criar uma conta informando meus dados pessoais
- **Para** poder fazer login e comprar produtos

### Critério 3 – Cadastro com sucesso (TC-003)

- **Dado** que estou na página de login
- **Quando** me cadastro com um e-mail ainda não utilizado e preencho os dados obrigatórios (senha, nome, sobrenome, endereço, telefone)
- **Então** devo ver a mensagem "ACCOUNT CREATED!"
- **E** a conta criada deve poder ser removida em seguida (limpeza do dado de teste, para não acumular contas na aplicação de terceiros)

> Nota de implementação: o e-mail único é gerado com `uuid4` a cada execução, evitando colisão com contas de execuções anteriores (inclusive entre workers paralelos do `pytest-xdist`). Os demais dados (nome, empresa, endereço, telefone, senha) são gerados dinamicamente com [Faker](https://faker.readthedocs.io/) (locale `pt_BR`) a cada execução.

### Critério 4 – Cadastro com e-mail já existente (TC-022)

- **Dado** que estou na página de login
- **Quando** tento me cadastrar usando o e-mail da própria conta de teste (já existente no site)
- **Então** devo ver a mensagem "Email Address already exist!"
- **E** meu cadastro não deve ser criado (permaneço na página de signup, não avanço para "Enter Account Information")

---

## História de Usuário — Logout

- **Como** usuário logado
- **Quero** encerrar minha sessão
- **Para** garantir que ninguém acesse minha conta pelo mesmo navegador depois de mim

### Critério 5 – Logout (TC-011)

- **Dado** que estou logado
- **Quando** clico em logout
- **Então** devo ver que estou deslogado (redirecionado para a página de login)
