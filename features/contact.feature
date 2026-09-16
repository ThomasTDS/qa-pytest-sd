Feature: Contato e newsletter no Automation Exercise

  @TC-009
  Scenario: Enviar formulário de contato com sucesso
    Given que o usuário está na página de contato
    When ele envia o formulário de contato com "QA Pytest SD", "qa-pytest-sd@mailinator.com", "Teste automatizado" e "Mensagem de teste automatizado."
    Then ele deve ver a confirmação de envio do formulário

  @TC-010
  Scenario: Inscrever e-mail na newsletter com sucesso
    Given que o usuário está na página inicial
    When ele se inscreve na newsletter com o e-mail "qa-pytest-sd@mailinator.com"
    Then ele deve ver a confirmação da inscrição
