# 🧪 QA Pytest + Playwright - Automation Exercise

![tests](https://github.com/ThomasTDS/qa-pytest-sd/actions/workflows/tests.yml/badge.svg)
![license](https://img.shields.io/badge/license-MIT-blue.svg)
![python](https://img.shields.io/badge/python-%3E%3D3.12-brightgreen.svg)

## Descrição

Este repositório contém testes automatizados do site **[automationexercise.com](https://automationexercise.com)** utilizando **Playwright**, **pytest-bdd (BDD/Gherkin)** e **Page Object Model (POM)**.

É a versão em **Python** do [qa-playwright-sd](https://github.com/ThomasTDS/qa-playwright-sd), que cobre os mesmos cenários e a mesma arquitetura (POM + Gherkin), originalmente escrito em TypeScript. A ideia não é um projeto novo do zero: os arquivos `.feature` (Gherkin) são praticamente idênticos entre os dois repositórios — o que muda é a linguagem e as ferramentas usadas para implementar os steps e os Page Objects.

> **Status:** migração de cenários do projeto em TypeScript concluída. Cobertura atual: login, cadastro, logout, produtos/carrinho, checkout, contato/newsletter e verificações de segurança passivas.

---

## Estrutura do Projeto

```text
qa-pytest-sd/
├── .github/
│   ├── workflows/         # Pipeline de CI (GitHub Actions)
│   └── dependabot.yml     # Atualização automática de dependências
├── features/              # Cenários em Gherkin (.feature), compartilhados com o qa-playwright-sd
├── steps/                 # Implementação dos steps (pytest-bdd)
├── pages/                 # Page Objects (LoginPage, RegisterPage, ...)
├── tests/                 # Arquivos que ligam cada feature aos seus steps
├── reports/               # Relatório HTML gerado a cada execução (não versionado)
├── conftest.py            # Fixtures do pytest (navegador, página, screenshot em falha)
├── pyproject.toml         # Configuração do pytest, ruff e mypy
├── requirements.txt       # Dependências do projeto
├── .env.example           # Modelo de variáveis de ambiente
├── LICENSE                # Licença MIT
└── README.md              # Este arquivo
```

---

### Clonar Repositório

```
git clone https://github.com/ThomasTDS/qa-pytest-sd.git

cd qa-pytest-sd
```

### Criar ambiente virtual e instalar dependências

Requer Python 3.12 ou superior.

```
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### Instalar navegadores do Playwright

```
playwright install
```

### Configuração de credenciais (.env)

Os cenários de login usam uma conta já existente no automationexercise.com, definida por variável de ambiente (nunca hardcoded no código). Copie `.env.example` para `.env` (arquivo não versionado) e preencha:

```
BASE_URL=https://automationexercise.com/
HEADLESS=false
TEST_USER_EMAIL=
TEST_USER_PASSWORD=
```

No CI, essas mesmas variáveis vêm de GitHub Secrets (`TEST_USER_EMAIL`/`TEST_USER_PASSWORD`), configurados no repositório.

### Rodar todos os testes

```
pytest
```

**NOTA:** _Por padrão, os testes rodam com o navegador visível (headless = false). Para rodar em modo headless (ex.: como no CI), use a variável de ambiente `HEADLESS`:_

```
# PowerShell
$env:HEADLESS="true"; pytest

# bash
HEADLESS=true pytest
```

### Rodar só o smoke test

O cenário `TC-007` (checkout completo) é marcado com `@smoke` e cobre login, produtos, carrinho e checkout em um único fluxo ponta-a-ponta:

```
pytest -m smoke
```

### Rodar contra outra URL

Por padrão os testes apontam para `https://automationexercise.com/`. Para rodar contra outro ambiente, defina `BASE_URL`:

```
# PowerShell
$env:BASE_URL="https://outro-ambiente.com/"; pytest

# bash
BASE_URL=https://outro-ambiente.com/ pytest
```

### Relatório HTML

```
pytest --html=reports/report.html --self-contained-html
```

Cada execução gera `reports/report.html` (não versionado) com o resultado dos cenários. Testes que falham têm automaticamente um print da tela no momento da falha anexado ao relatório, para facilitar o diagnóstico.

### Lint, formatação e checagem de tipos

O projeto usa **ruff** (lint + formatação) e **mypy** (checagem de tipos):

```
ruff check .           # verifica problemas de lint
ruff check . --fix     # corrige o que for possível automaticamente
ruff format .          # formata todos os arquivos
ruff format --check .  # só verifica, sem alterar (usado no CI)
mypy .                 # verifica erros de tipos
```

---

### Estrutura de Testes e Padrões Aplicados

- BDD / Gherkin: cenários claros e legíveis em `.feature`, compartilhados com o projeto irmão em TypeScript.
- Page Object Model (POM): separação de responsabilidades, com Pages encapsulando elementos e ações.
- Testes End-to-End (E2E): simulação de fluxos reais de usuário.

---

### CI/CD

O projeto roda automaticamente via GitHub Actions (`.github/workflows/tests.yml`) a cada push/PR para a `main` e diariamente às 06:00 UTC. Antes dos testes, o CI valida lint (`ruff check`), formatação (`ruff format --check`) e tipos (`mypy`), quebrando o build se algo estiver fora do padrão. O relatório HTML é publicado como artifact de cada execução. Cenários que falham são reexecutados automaticamente uma vez (`--reruns 1`), para absorver instabilidades pontuais de rede sem mascarar bugs reais de código.

### Segurança da pipeline

- `pip-audit` roda no CI a cada execução, quebrando o build se houver vulnerabilidade conhecida em alguma dependência.
- **Dependabot** ativo (`.github/dependabot.yml`): atualizações automáticas semanais de dependências pip e das actions do workflow.

A `main` é protegida: mudanças precisam passar por Pull Request com o check de testes verde.

### Próximos Passos

- Todos os cenários do [qa-playwright-sd](https://github.com/ThomasTDS/qa-playwright-sd) já foram portados (login, cadastro, logout, produtos/carrinho, checkout, contato/newsletter e segurança passiva).
- Itens de manutenção em aberto: extrair a data de nascimento fixa do cadastro para `AccountInfo`, trocar a geração de e-mail único (`time.time()`) por `uuid4`, e configurar `pre-commit` local para rodar ruff/mypy antes do commit.

---

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.
