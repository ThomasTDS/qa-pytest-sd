Feature: Verificações de segurança passivas no Automation Exercise

  @TC-012
  Scenario: Cabeçalhos de segurança HTTP presentes
    Then a aplicação deve responder com os cabeçalhos de segurança esperados

  @TC-013
  Scenario: Redirecionamento HTTP para HTTPS
    Then o acesso via HTTP deve ser redirecionado para HTTPS

  @TC-014
  Scenario: Campo de senha deve estar mascarado
    Given que o usuário está na página de login
    Then o campo de senha deve ser do tipo password

  @TC-015
  Scenario: Cookie de sessão deve ter a flag HttpOnly
    Given que o usuário está na página de login
    When ele faz login com a conta de teste
    Then o cookie de sessão deve ter a flag HttpOnly ativada
