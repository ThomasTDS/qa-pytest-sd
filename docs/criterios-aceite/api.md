# API Pública

Cenários executáveis: `features/api.feature`.

Diferente dos demais critérios, estes não simulam um usuário navegando pela UI — validam diretamente o contrato da API pública do automationexercise.com (documentada em `automationexercise.com/api_list`), via `page.request`. É uma camada de teste mais rápida e menos frágil para verificar regras de negócio que também valem no back-end.

## História de Usuário — Consulta de catálogo via API

- **Como** integrador de terceiros consumindo a API do site
- **Quero** consultar produtos e marcas
- **Para** exibir o catálogo em outro sistema sem depender da UI

### Critério 1 – Lista de produtos contém um produto conhecido (TC-018)

- **Quando** consulto `GET /api/productsList`
- **Então** a resposta deve ter `responseCode: 200`
- **E** a lista de produtos deve conter um produto com nome "Blue Top"

### Critério 2 – Lista de marcas não está vazia (TC-019)

- **Quando** consulto `GET /api/brandsList`
- **Então** a resposta deve ter `responseCode: 200`
- **E** a lista de marcas deve ter pelo menos um item

### Critério 3 – Busca de produtos retorna resultados esperados (TC-020)

- **Quando** consulto `POST /api/searchProduct` com o termo "top"
- **Então** a resposta deve ter `responseCode: 200`
- **E** a lista de produtos retornada deve conter "Blue Top"

### Critério 4 – Método HTTP não suportado é rejeitado (TC-021)

- **Quando** consulto `POST /api/productsList` (o endpoint só aceita `GET`)
- **Então** a API deve responder com `responseCode: 405` no corpo

> Nota de implementação: `automationexercise.com` sempre responde HTTP 200 na camada de transporte — o status semântico real (sucesso, erro de validação, método não suportado) vem no campo `responseCode` do corpo da resposta, não no status code HTTP. Confirmado manualmente contra a API real antes de escrever as asserções.

---

## História de Usuário — Verificação de conta via API

- **Como** integrador de terceiros
- **Quero** verificar credenciais, criar/remover contas e consultar dados de usuário via API
- **Para** automatizar fluxos de conta sem depender de formulários HTML

### Critério 5 – Login válido é confirmado (TC-024)

- **Quando** consulto `POST /api/verifyLogin` com e-mail e senha da conta de teste
- **Então** a resposta deve ter `responseCode: 200` e mensagem "User exists!"

### Critério 6 – Login inválido é rejeitado (TC-025)

- **Quando** consulto `POST /api/verifyLogin` com credenciais que não correspondem a nenhuma conta
- **Então** a resposta deve ter `responseCode: 404` e mensagem "User not found!"

### Critério 7 – Criação e remoção de conta (TC-026)

- **Quando** crio uma conta via `POST /api/createAccount` com um e-mail novo
- **Então** a resposta deve ter `responseCode: 201`
- **E** ao remover essa conta via `DELETE /api/deleteAccount`, a resposta deve ter `responseCode: 200`

> Nota de implementação: o e-mail é gerado com `uuid4` a cada execução, e a conta é sempre removida ao final do teste, para não acumular contas descartáveis na aplicação de terceiros. Os demais dados do cadastro (nome, empresa, endereço, telefone) vêm do [Faker](https://faker.readthedocs.io/) (locale `pt_BR`) — a senha continua fixa, já que é reaproveitada na remoção da mesma conta.

### Critério 8 – Consulta de usuário por e-mail (TC-027)

- **Quando** consulto `GET /api/getUserDetailByEmail` com o e-mail da conta de teste
- **Então** a resposta deve ter `responseCode: 200`
- **E** o e-mail no perfil retornado deve corresponder ao e-mail consultado
