# Teste Dev 

Olá, bem-vindo(a) ao teste para pessoa desenvolvedora! 🖖

## A quest pelo sistema de fretes: 🚚

Esse é um sistema de cálculo de fretes, o usuário entra com a distância a ser percorrida, peso da encomenda e a opção do frete. A partir daí o sistema calcula o valor do frete.
Porém há um problema, alguns testes não estão passando. Precisamos de você para fazê-los passar!
Além disso, precisamos que o sistema seja transformado numa API REST para futuras integrações.
Também temos que implementar as seguintes histórias de usuário:

- "Como usuário gostaria de poder me cadastrar no sistema."
- "Como usuário quero inserir o CEP de partida e o de entrega da minha encomenda, peso e tipo do frete e espero que o sistema me retorne o valor do frete."
- "Como usuário quero poder confirmar o envio de minha encomenda para então pagá-la utilizando cartão de débito, crédito ou pix."
- "Como usuário gostaria de ter acesso ao meu histórico de encomendas, espero que o sistema me retorne origem, destino, valor do frete, peso, tipo e forma de pagamento."
- "Como usuário gostaria de atualizar meus dados."
- "Como gerente gostaria de poder verificar a quantidade de encomendas realizadas no atual dia."
- "Como gerente preciso bater meu ponto de entrada e saída."
- "Como entregador gostaria de verificar o cep de origem e destino de certa encomenda bem como o nome e telefone do remetente."
- "Como entregador preciso bater meu ponto de entrada e saída."
- "Como entregador, gerente e funcionário preciso fazer login no sistema."

Nossas pesquisas nos mostraram que há muitas APIs públicas que retornam os dados de CEP porém preferimos seguir com a [Brasil API](https://brasilapi.com.br/).
Agora para calcular a distância entre os dois CEPs seguimos com a API do [Project OSRM](https://project-osrm.org).
Como banco de dados preferimos seguir com o Postgres.
O usuário precisará informar os seguintes dados para cadastro: Nome, Telefone, Email e Senha.
Precisamos guardar os seguintes dados de gerentes e entregadores: Cargo, Nome, Número de registro e Senha.
Não se preocupe com a implementação dos pagamentos, apenas uma mensagem de sucesso é suficiente.

    
### Como instalar as dependências? 📦

Para isso você pode tanto utilizar o requirements.txt ou instalar o [Pipenv](https://pipenv.pypa.io/en/latest/) e rodar os seguintes comandos:

- requirements:
  `pip install -r requirements.txt`
- pipenv:
  `pipenv install`

### Como executar os testes? ⚙️

Esse teste utiliza do pytest para executar testes automatizados, para rodar a suíte de testes, basta chamar o pytest com o seguinte comando no seu terminal: `pytest`.
Se você estiver usando o pipenv, será importante acessar o ambiente virtual dele antes de rodar os testes, para isso, basta utilizar o comando `pipenv shell`

Qualquer dúvidas deixe-nos saber! :)
