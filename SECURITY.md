# Política de Segurança

## Escopo

Este repositório é um projeto de portfólio de automação de testes (QA), sem backend próprio, banco de dados ou dados de usuários reais. O escopo desta política cobre apenas o **código e a pipeline deste repositório** (dependências, workflow de CI, scripts, manuseio de credenciais de teste) — não o site de terceiros usado como alvo dos testes ([automationexercise.com](https://automationexercise.com)).

A suíte de segurança (`features/security.feature`) já deixa isso explícito: ela só observa e valida o que a aplicação de terceiros expõe publicamente (cabeçalhos HTTP, HTTPS, flags de cookie), sem qualquer tentativa de exploração ativa contra ela. Vulnerabilidades no automationexercise.com em si estão fora do escopo deste repositório e devem ser reportadas diretamente aos mantenedores daquele site.

## Versões Suportadas

Projeto sem versionamento semântico formal. Apenas a branch `main` (código mais recente) recebe correções de segurança.

## Como Reportar uma Vulnerabilidade

Se você encontrar uma vulnerabilidade real no código deste repositório (por exemplo, uma dependência com CVE crítico não coberta pelo Dependabot, um workflow de CI que exponha secrets, ou credenciais commitadas por engano), por favor:

1. **Não abra uma issue pública.** Use a aba **Security → Report a vulnerability** deste repositório no GitHub, que cria um advisory privado visível só para o mantenedor.
2. Descreva o problema, o impacto potencial e, se possível, os passos para reproduzir.

Esse é um projeto pessoal mantido nas horas vagas, então não há SLA formal de resposta, mas relatos são levados a sério e tratados assim que possível.

## Medidas Já em Vigor

- `pip-audit` roda no CI a cada execução, quebrando o build se houver vulnerabilidade conhecida em alguma dependência.
- **Dependabot** ativo para atualizações semanais de dependências pip e das GitHub Actions do workflow.
- Credenciais de teste nunca ficam hardcoded no código — vêm de variáveis de ambiente (`.env` local, não versionado) ou GitHub Secrets no CI.
