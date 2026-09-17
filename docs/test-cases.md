# Matriz de Test Cases

Rastreabilidade dos casos de teste do projeto. Não duplica os passos dos cenários — isso já vive nos arquivos `.feature` (Gherkin). Cada linha referencia o cenário real correspondente, marcado com a tag `@TC-XXX` correspondente no próprio `.feature`.

| ID     | Módulo     | Título                                                       | Tipo      | Prioridade | Automação    | Cenário                     |
| ------ | ---------- | -------------------------------------------------------------- | --------- | ---------- | ------------ | --------------------------- |
| TC-001 | Login      | Login com credenciais válidas                                  | Funcional | Crítica    | Automatizado | `features/login.feature`    |
| TC-002 | Login      | Login com credenciais inválidas                                 | Negativo  | Alta       | Automatizado | `features/login.feature`    |
| TC-003 | Cadastro   | Cadastro de um novo usuário (com exclusão ao final)             | Funcional | Alta       | Automatizado | `features/login.feature`    |
| TC-004 | Produtos   | Buscar produtos e visualizar resultados                        | Funcional | Média      | Automatizado | `features/products.feature` |
| TC-005 | Carrinho   | Adicionar múltiplos produtos ao carrinho                        | Funcional | Alta       | Automatizado | `features/products.feature` |
| TC-006 | Carrinho   | Remover um produto do carrinho                                 | Funcional | Média      | Automatizado | `features/products.feature` |
| TC-007 | Checkout   | Finalizar compra com sucesso (login → carrinho → pagamento)     | Funcional | Crítica    | Automatizado | `features/checkout.feature` |
| TC-008 | Checkout   | Tentar finalizar checkout sem estar logado                     | Negativo  | Alta       | Automatizado | `features/checkout.feature` |
| TC-009 | Contato    | Enviar formulário de contato com sucesso                        | Funcional | Média      | Automatizado | `features/contact.feature`  |
| TC-010 | Newsletter | Inscrever e-mail na newsletter com sucesso                      | Funcional | Baixa      | Automatizado | `features/contact.feature`  |
| TC-011 | Sessão     | Logout                                                          | Funcional | Média      | Automatizado | `features/login.feature`    |
| TC-012 | Segurança  | Cabeçalhos de segurança HTTP presentes (X-Frame-Options, X-Content-Type-Options) | Funcional | Alta | Automatizado | `features/security.feature` |
| TC-013 | Segurança  | Redirecionamento HTTP para HTTPS                                | Funcional | Alta       | Automatizado | `features/security.feature` |
| TC-014 | Segurança  | Campo de senha deve estar mascarado                             | Funcional | Média      | Automatizado | `features/security.feature` |
| TC-015 | Segurança  | Cookie de sessão deve ter a flag HttpOnly ativada               | Funcional | Alta       | Automatizado | `features/security.feature` |
| TC-016 | Cadastro   | Tentar se cadastrar com um e-mail já existente                  | Negativo  | Média      | Automatizado | `features/login.feature`    |
| TC-017 | Checkout   | Carrinho vazio impede prosseguir para o checkout                | Negativo  | Média      | Automatizado | `features/checkout.feature` |

`TC-016` e `TC-017` são cenários negativos adicionados só neste repositório (não existem ainda no `qa-playwright-sd`).

## Smoke

`TC-007` é marcado com `@smoke` — sozinho ele encadeia login, produtos, carrinho e checkout, cobrindo o caminho crítico ponta-a-ponta. Rodar só esse subconjunto:

```
pytest -m smoke
```

## Testes unitários

Além dos cenários E2E acima, `tests/unit/` cobre a lógica dos Page Objects (leitura de `BASE_URL`, condicionais de formulário, montagem de payloads) isoladamente, com o `Page` do Playwright mockado — sem navegador, sem rede, sem os casos de teste E2E. Não são rastreados nesta matriz por não corresponderem a um cenário de negócio (`TC-XXX`), e sim à implementação. Rodar:

```
pytest -m unit
```

## Legenda

- **Tipo** — `Funcional` (caminho feliz) ou `Negativo` (validação de erro/bloqueio esperado).
- **Prioridade** — importância do caso de teste para o negócio (`Crítica`/`Alta`/`Média`/`Baixa`). Não confundir com a Prioridade (P0–P3) dos bug reports, que mede urgência de correção de um defeito, não importância de cobertura de teste.
- **Automação** — `Automatizado`, `Manual` ou `Planejado` (identificado, ainda não implementado).
