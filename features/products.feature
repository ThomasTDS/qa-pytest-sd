Feature: Busca de produtos e carrinho no Automation Exercise

  @TC-004
  Scenario: Buscar produtos e visualizar resultados
    Given que o usuário está na página de produtos
    When ele busca por "Top"
    Then ele deve ver resultados da busca

  @TC-005
  Scenario: Adicionar múltiplos produtos ao carrinho
    Given que o usuário está na página de produtos
    When ele adiciona os produtos "Blue Top" e "Men Tshirt" ao carrinho
    And ele acessa o carrinho
    Then ele deve ver os produtos "Blue Top" e "Men Tshirt" no carrinho

  @TC-006
  Scenario: Remover um produto do carrinho
    Given que o usuário está na página de produtos
    When ele adiciona os produtos "Blue Top" e "Men Tshirt" ao carrinho
    And ele acessa o carrinho
    And ele remove o produto "Blue Top" do carrinho
    Then ele não deve ver o produto "Blue Top" no carrinho
    And ele deve ver o produto "Men Tshirt" no carrinho
