# Produtos e Carrinho

Cenários executáveis: `features/products.feature`.

## História de Usuário — Busca de produtos

- **Como** visitante do site
- **Quero** buscar produtos por nome
- **Para** encontrar rapidamente o que procuro sem navegar por todas as categorias

### Critério 1 – Buscar produtos e visualizar resultados (TC-004)

- **Dado** que estou na página de produtos
- **Quando** busco por um termo (ex.: "Top")
- **Então** devo ver a seção "Searched Products"
- **E** pelo menos um produto deve aparecer nos resultados

---

## História de Usuário — Carrinho de compras

- **Como** visitante do site
- **Quero** adicionar e remover produtos do carrinho
- **Para** montar minha compra antes de finalizar o pedido

### Critério 2 – Adicionar múltiplos produtos ao carrinho (TC-005)

- **Dado** que estou na página de produtos
- **Quando** adiciono dois produtos diferentes ao carrinho
- **E** acesso o carrinho
- **Então** devo ver os dois produtos listados

### Critério 3 – Remover um produto do carrinho (TC-006)

- **Dado** que tenho dois produtos no carrinho
- **Quando** removo um deles
- **Então** o produto removido não deve mais aparecer no carrinho
- **E** o outro produto deve continuar lá

> A mensagem de carrinho vazio (bloqueio do checkout sem produtos) é tratada como regra de negócio do fluxo de checkout — ver [checkout.md](checkout.md), TC-023.
