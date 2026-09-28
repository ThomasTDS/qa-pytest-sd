Feature: Verificação da API pública do Automation Exercise

  @TC-018
  Scenario: Lista de produtos via API contém um produto conhecido
    Then a API de produtos deve conter o produto "Blue Top"

  @TC-019
  Scenario: Lista de marcas via API não está vazia
    Then a API de marcas não deve estar vazia

  @TC-020
  Scenario: Busca de produtos via API retorna resultados esperados
    Then a busca via API por "top" deve retornar o produto "Blue Top"

  @TC-021
  Scenario: API de produtos rejeita método HTTP não suportado
    Then a API de produtos deve rejeitar POST com o código 405

  @TC-024
  Scenario: Verificação de login via API com credenciais válidas
    Then a verificação de login via API com a conta de teste deve confirmar que o usuário existe

  @TC-025
  Scenario: Verificação de login via API com credenciais inválidas
    Then a verificação de login via API com o e-mail "usuario-invalido@mailinator.com" e a senha "senhaerrada" deve indicar que o usuário não foi encontrado

  @TC-026
  Scenario: Criação e remoção de conta via API
    Then a API deve permitir criar e remover uma conta

  @TC-027
  Scenario: Consulta de detalhes do usuário de teste via API
    Then a consulta de detalhes do usuário de teste via API deve retornar o seu perfil
