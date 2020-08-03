# where_url_goes
Informa se a url possui redirecionamento e para onde é este redirecionamento.

O código recebe uma URL e realiza uma requisição para saber se houve mudança na URL.
Se houve, é identificado os dominios e subdominios das URL.
URLs, dominios e subdominios são comparados através da distância de levenshtein.
Dependendo da comparação o código informa que tipo de mudança ouve na URL.