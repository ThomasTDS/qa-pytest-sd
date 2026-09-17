Feature: Checkout no Automation Exercise

  @TC-007 @smoke
  Scenario: Finalizar compra com sucesso
    Given que o usuário está na página de login
    When ele faz login com a conta de teste
    And que o usuário está na página de produtos
    And ele adiciona o produto "Blue Top" ao carrinho
    And ele acessa o carrinho
    And ele prossegue para o checkout
    And ele confirma o pedido
    And ele preenche o pagamento com um cartão de teste
    Then ele deve ver a confirmação do pedido

  @TC-008
  Scenario: Tentar finalizar checkout sem estar logado
    Given que o usuário está na página de produtos
    When ele adiciona o produto "Blue Top" ao carrinho
    And ele acessa o carrinho
    And ele prossegue para o checkout
    Then ele deve ver a mensagem pedindo para fazer login

  @TC-017
  Scenario: Carrinho vazio impede prosseguir para o checkout
    When ele acessa o carrinho
    Then ele deve ver a mensagem de carrinho vazio "Cart is empty! Click here to buy products."
    And ele não deve ver a opção de prosseguir para o checkout
