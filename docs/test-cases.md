# Matriz de Test Cases

Rastreabilidade dos casos de teste do projeto. Não duplica os passos dos cenários — isso já vive nos arquivos `.feature` (Gherkin). Cada linha referencia o cenário real correspondente, marcado com a tag `@TC-XXX` correspondente no próprio `.feature`.

Para a regra de negócio e a história de usuário por trás de cada test case, veja [criterios-aceite/](criterios-aceite/).

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
| TC-016 | Acessibilidade | Página de login sem violações críticas de acessibilidade      | Funcional | Média      | Automatizado | `features/accessibility.feature` |
| TC-017 | Acessibilidade | Página de produtos sem violações críticas de acessibilidade   | Funcional | Média      | Automatizado | `features/accessibility.feature` |
| TC-018 | API        | Lista de produtos via API contém um produto conhecido           | Funcional | Média      | Automatizado | `features/api.feature`      |
| TC-019 | API        | Lista de marcas via API não está vazia                          | Funcional | Baixa      | Automatizado | `features/api.feature`      |
| TC-020 | API        | Busca de produtos via API retorna resultados esperados          | Funcional | Média      | Automatizado | `features/api.feature`      |
| TC-021 | API        | API de produtos rejeita método HTTP não suportado               | Negativo  | Baixa      | Automatizado | `features/api.feature`      |
| TC-022 | Cadastro   | Tentar se cadastrar com um e-mail já existente                  | Negativo  | Média      | Automatizado | `features/login.feature`    |
| TC-023 | Checkout   | Carrinho vazio impede prosseguir para o checkout                | Negativo  | Média      | Automatizado | `features/checkout.feature` |
| TC-024 | API        | Verificação de login via API com credenciais válidas            | Funcional | Média      | Automatizado | `features/api.feature`      |
| TC-025 | API        | Verificação de login via API com credenciais inválidas          | Negativo  | Média      | Automatizado | `features/api.feature`      |
| TC-026 | API        | Criação e remoção de conta via API                              | Funcional | Média      | Automatizado | `features/api.feature`      |
| TC-027 | API        | Consulta de detalhes do usuário de teste via API                | Funcional | Baixa      | Automatizado | `features/api.feature`      |

A numeração está alinhada com o [qa-playwright-sd](https://github.com/ThomasTDS/qa-playwright-sd): mesmo TC-XXX para o mesmo cenário nos dois repositórios.

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
