# Segurança Passiva

Cenários executáveis: `features/security.feature`.

Estes critérios verificam apenas o que o automationexercise.com **já expõe publicamente** (cabeçalhos HTTP, redirecionamento, flags de cookie e tipo de campo). Não há nenhuma tentativa de exploração ativa, envio de payload malicioso ou bypass de controle contra a aplicação de terceiros — ver [SECURITY.md](../../SECURITY.md) para o escopo completo desta política.

## História de Usuário — Cabeçalhos de segurança

- **Como** responsável pela aplicação
- **Quero** que o servidor responda com cabeçalhos de segurança HTTP padrão
- **Para** reduzir a superfície de ataques como clickjacking e MIME sniffing

### Critério 1 – Cabeçalhos de segurança presentes (TC-012)

- **Quando** faço uma requisição para a página inicial
- **Então** o cabeçalho `X-Frame-Options` deve ser `DENY`
- **E** o cabeçalho `X-Content-Type-Options` deve ser `nosniff`

### Critério 2 – Redirecionamento HTTP para HTTPS (TC-013)

- **Quando** acesso a aplicação via `http://` (sem TLS)
- **Então** devo ser redirecionado para a versão `https://`

---

## História de Usuário — Proteção de credenciais

- **Como** usuário do site
- **Quero** que minha senha e minha sessão sejam protegidas no navegador
- **Para** reduzir o risco de exposição acidental (ex.: shoulder surfing, roubo de cookie via script)

### Critério 3 – Campo de senha mascarado (TC-014)

- **Dado** que estou na página de login
- **Então** o campo de senha deve ser do tipo `password` (caracteres ocultos na tela)

### Critério 4 – Cookie de sessão com flag HttpOnly (TC-015)

- **Dado** que estou na página de login
- **Quando** faço login com a conta de teste
- **Então** o cookie de sessão (`sessionid`) deve ter a flag `HttpOnly` ativada, impedindo acesso a ele via JavaScript no navegador
