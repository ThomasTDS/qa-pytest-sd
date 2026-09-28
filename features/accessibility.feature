Feature: Acessibilidade básica no Automation Exercise

  @TC-016
  Scenario: Página de login sem violações críticas de acessibilidade
    Given que o usuário está na página de login
    Then a página não deve ter violações críticas de acessibilidade

  @TC-017
  Scenario: Página de produtos sem violações críticas de acessibilidade
    Given que o usuário está na página de produtos
    Then a página não deve ter violações críticas de acessibilidade
