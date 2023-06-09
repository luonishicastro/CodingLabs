# Primeira Parte - SQL
 Tendo em conta um modelo de ecomeerce que trabalhamos, temos alguma entidades básicas que queremos representar: *Customer, Order, Item y Category*
 
 * **Customer:** é a entidade onde se encontram todos os nossos usuários, sejam eles Buyers ou Sellers do site. Os principais atributos são e-mail, nome, sobrenome, sexo, endereço, data de nascimento e outros mais.
 * **Item:** é a entidade onde se encontram os produtos publicados no nosso marketplace. O volume é muito grande, pois temos todos os produtos que foram publicados, independente de estarem ativos ou não. Para identificar o estado de um produto temos que fazer uma consulta pelo estado do item ou pelo campo de baixa (end_date).
 * **Category:** é a entidade onde tempos a descrição de cada categoria com seu respectivo path. Cada item tem uma categoria associada a ele.
 * **Order:** a tabela order é a entidade que reflete as transações geradas dentro do site (cada compra é uma order). Nesse caso não vamos levar em conta o fluxo do carrinho de compras, porém para cada item que for vendido será refletido em uma order independente da quantidade que for comprada.

**Fluxo de Compras:** um usuário no site do Mercado Livre para comprar dois celulares idênticos. Realiza uma busca na categoria Tecnologia > Celulares e Telefones > Celulares e Smartphones e, por fim, encontra o produto que deseja comprar. Segue com a compra, selecionando duas unidades iguais e com isso será gerado uma ordem de compra.
 
 Com base no caso de uso descrito acima, criar uma DER que responda ao modelo de Negócio. Em paralelo, resolver os desafios utilizando a linguagem SQL.

# Segunda Parte - APIs
