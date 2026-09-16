Feature: Login e cadastro no Automation Exercise

  @TC-001
  Scenario: Login com credenciais válidas
    Given que o usuário está na página de login
    When ele faz login com a conta de teste
    Then ele deve ver que está logado

  @TC-002
  Scenario: Login com credenciais inválidas
    Given que o usuário está na página de login
    When ele insere o e-mail "usuario-invalido@mailinator.com" e a senha "senhaerrada"
    Then ele deve ver a mensagem de erro "Your email or password is incorrect!"

  @TC-003
  Scenario: Cadastro de um novo usuário
    Given que o usuário está na página de login
    When ele se cadastra com um e-mail novo
    Then ele deve ver a mensagem "ACCOUNT CREATED!"
    And a conta criada deve poder ser removida

  @TC-011
  Scenario: Logout
    Given que o usuário está na página de login
    When ele faz login com a conta de teste
    And ele faz logout
    Then ele deve ver que está deslogado
