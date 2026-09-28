# Critérios de Aceite

Cada arquivo nesta pasta documenta **uma história de usuário** e as **regras de negócio** por trás dos cenários automatizados, escritas em formato Dado/Quando/Então (BDD). É um nível de documentação diferente do `docs/test-cases.md`: a matriz de test cases responde "o que está automatizado e onde", enquanto estes arquivos respondem "por que o cenário existe e qual regra ele protege".

Um arquivo aqui não substitui o `.feature` correspondente — o `.feature` é a fonte executável da verdade, e roda no CI a cada push. Se um critério aqui e o `.feature` divergirem, o `.feature` está certo e este arquivo precisa ser atualizado.

| Arquivo                                        | Feature                     | Test cases                       |
| ----------------------------------------------- | ---------------------------- | --------------------------------- |
| [login.md](login.md)                             | `features/login.feature`     | TC-001, TC-002, TC-003, TC-011, TC-022 |
| [produtos-carrinho.md](produtos-carrinho.md)     | `features/products.feature`  | TC-004, TC-005, TC-006            |
| [checkout.md](checkout.md)                       | `features/checkout.feature`  | TC-007, TC-008, TC-023            |
| [contato-newsletter.md](contato-newsletter.md)   | `features/contact.feature`   | TC-009, TC-010                    |
| [seguranca.md](seguranca.md)                     | `features/security.feature`  | TC-012 a TC-015                   |
| [acessibilidade.md](acessibilidade.md)           | `features/accessibility.feature` | TC-016, TC-017                 |
| [api.md](api.md)                                 | `features/api.feature`       | TC-018 a TC-021, TC-024 a TC-027  |
