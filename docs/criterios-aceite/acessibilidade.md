# Acessibilidade Básica

Cenários executáveis: `features/accessibility.feature`.

Estes critérios rodam o motor [axe-core](https://github.com/dequelabs/axe-core) (via [axe-playwright-python](https://pypi.org/project/axe-playwright-python/)) contra páginas-chave do automationexercise.com e avaliam apenas violações de impacto `critical` ou `serious` — os demais níveis (`moderate`, `minor`) são ruído demais para uma aplicação de terceiros que não controlamos.

O teste é **QA passivo**: se o axe-core encontrar violações relevantes, elas são anexadas como nota ao relatório HTML para visibilidade, mas o cenário não falha. A aplicação é de terceiros — o objetivo aqui é documentar o estado de acessibilidade observado, não bloquear o pipeline por um problema que não podemos corrigir.

## História de Usuário — Acessibilidade das páginas principais

- **Como** usuário de tecnologia assistiva (ex.: leitor de tela)
- **Quero** navegar pelas páginas principais do site sem barreiras críticas de acessibilidade
- **Para** conseguir fazer login e comprar produtos como qualquer outro usuário

### Critério 1 – Página de login sem violações críticas (TC-016)

- **Dado** que estou na página de login
- **Então** a página não deve ter violações de acessibilidade com impacto `critical` ou `serious`
- **E**, se houver, elas devem aparecer como nota no relatório, sem falhar o teste

### Critério 2 – Página de produtos sem violações críticas (TC-017)

- **Dado** que estou na página de produtos
- **Então** a página não deve ter violações de acessibilidade com impacto `critical` ou `serious`
- **E**, se houver, elas devem aparecer como nota no relatório, sem falhar o teste
