# Contato e Newsletter

Cenários executáveis: `features/contact.feature`.

## História de Usuário — Formulário de contato

- **Como** visitante do site
- **Quero** enviar uma mensagem pelo formulário de contato
- **Para** relatar uma dúvida ou problema à equipe do site

### Critério 1 – Enviar formulário de contato com sucesso (TC-009)

- **Dado** que estou na página de contato
- **Quando** preencho nome, e-mail, assunto e mensagem, e envio o formulário
- **Então** devo ver a confirmação "Success! Your details have been submitted successfully."

> Nota de implementação: o site exibe um `window.confirm()` nativo do navegador antes de enviar; o teste aceita esse diálogo automaticamente (`page.once("dialog", ...)`).

---

## História de Usuário — Newsletter

- **Como** visitante do site
- **Quero** me inscrever na newsletter informando meu e-mail
- **Para** receber atualizações do site

### Critério 2 – Inscrever e-mail na newsletter com sucesso (TC-010)

- **Dado** que estou na página inicial
- **Quando** informo um e-mail e confirmo a inscrição
- **Então** devo ver a mensagem "You have been successfully subscribed!"
