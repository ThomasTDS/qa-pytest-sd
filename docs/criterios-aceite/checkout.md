# Checkout

Cenários executáveis: `features/checkout.feature`.

## História de Usuário — Finalizar compra

- **Como** usuário logado com produtos no carrinho
- **Quero** finalizar minha compra informando dados de pagamento
- **Para** concluir o pedido

### Critério 1 – Finalizar compra com sucesso (TC-007, `@smoke`)

- **Dado** que estou logado e adicionei um produto ao carrinho
- **Quando** prossigo para o checkout, confirmo o pedido e preencho o pagamento com um cartão de teste
- **Então** devo ver a confirmação "Order Placed!"

> Este é o cenário `@smoke`: encadeia login, produtos, carrinho e checkout num único fluxo ponta-a-ponta. Rodar isolado com `pytest -m smoke`.

### Critério 2 – Checkout exige login (TC-008)

- **Dado** que adicionei um produto ao carrinho sem estar logado
- **Quando** tento prosseguir para o checkout
- **Então** devo ver a mensagem "Register / Login account to proceed on checkout."
- **E** não devo conseguir avançar para a tela de pagamento

### Critério 3 – Carrinho vazio impede o checkout (TC-023)

- **Dado** que acesso o carrinho sem ter adicionado nenhum produto
- **Então** devo ver a mensagem "Cart is empty! Click here to buy products."
- **E** a opção "Proceed To Checkout" não deve estar disponível
