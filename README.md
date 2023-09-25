# Art refs API

Projeto criado como componente B do MVP da disciplina de Back-end avançado do curso de pós-graduação em Desenvolvimento Full Stack da PUC-Rio. 

## O que é?
Implementação da API do chatGPT para buscar referencias de Artes Visuais em séries de tv.

[GraphiQL Playground](http://127.0.0.1:5000/graphiql)

## API's utilizadas 
[Trakt API](https://trakt.docs.apiary.io/#introduction/verbs)
API pública e gratuita utilizada neste projeto para recuperar informações de séries e filmes.
É necessário se cadastrar no site oficial e criar um "Trakt API app" para gerar uma API Key necessária para consumir os dados (que deve ser acrescentada no .env como descrito aqui). 
A API possui uma [documentação detalhada aqui](https://trakt.docs.apiary.io/#introduction/verbs) de como se cadastrar, gerar a API Key e fazer os requests. 

Endpoints utilizados:

| Endpoint                               | Descrição                               |
| -------------------------------------- | --------------------------------------- |
| https://api.trakt.tv/search/show       | Retorna informações sobre séries.       |
| https://api.trakt.tv/search/movie      | Retorna informações sobre filmes.       |


[TMDB API](https://developer.themoviedb.org/reference/intro/getting-started)
API pública e gratuita utilizada neste projeto para recuperar o endereço da imagem que será usada como poster para cada filme ou série exibidos na [Home do front-end](https://github.com/amandagpearce/got-that-ref#home).
Na response das requisições do Trakt é fornecida a id do filme/série no TMDB, com essa id, o endereço da imagem do poster é retornado.  

É necessário se cadastrar no site oficial para gerar uma API Key (que deve ser acrescentada no .env como descrito aqui). 
A API possui uma [documentação detalhada aqui](https://developer.themoviedb.org/reference/intro/getting-started) de como se cadastrar, gerar a API Key e fazer os requests.

Endpoints utilizados:

| Endpoint                                   | Descrição                                |
| ------------------------------------------ | ---------------------------------------- |
| https://api.themoviedb.org/3/tv/<id>       | Retorna a url do poster da referida id.  |
| https://api.themoviedb.org/3/movie/<id>    | Retorna a url do poster da referida id.  |


[Google Image Service](https://github.com/amandagpearce/google-image-service)
API Rest criada também para este trabalho, utiliza a Google's Programmable Search Engine para buscar uma imagem da obra de arte referenciada pelo filme ou série, de acordo com o cadastro realizado no [front-end](https://github.com/amandagpearce/got-that-ref#send-a-reference). 

Informações mais detalhadas sobre licensas e utilização estão no [repositório do projeto](https://github.com/amandagpearce/google-image-service). 

Endpoints utilizados:

| Endpoint                                   | Descrição                                |
| ------------------------------------------ | ---------------------------------------- |
| http://127.0.0.1:9000/get_image_url        | Retorna a url da imagem da obra de arte. |


## Arquivo .env
É necessário a criação de um arquivo .env tanto para rodar o projeto com Docker quanto sem. Após ter as API keys do Trakt e do TBMD como descrito acima, crie um arquivo chamado `.env` com o seguinte conteúdo:

```bash
TRAKT_API_KEY=keystringaqui
TBDB_API_KEY=keystringaqui
```
Substitua "keystringaqui" pelas suas keys. 

## Instalação com Docker
1. Clone o projeto
2. Crie o arquivo .env como descrito acima e cole na raiz do projeto 
3. Na raiz do projeto, crie a imagem:
```bash
  docker build -t art-refs-api .
```

3. Rode a imagem criada:
```bash
  docker run -p 4000:4000 art-refs-api
```

## Instalação sem Docker
1. Clone o projeto
2. Crie o arquivo .env como descrito acima e cole na raiz do projeto 
3. Na raiz do projeto, rode o comando:
```bash
  flask run --host 0.0.0.0 --port 4000
```

