# Art refs API

Projeto criado como componente B do MVP da disciplina de Back-end avançado do curso de pós-graduação em Desenvolvimento Full Stack da PUC-Rio. 

## O que é?
API Graphql que utiliza as APIs públicas do `Trakt` e `TMDB` mais a aplicação própria `Google Image Service` e executa queries e mutations em um banco de dados sqlite.

## API's utilizadas 
1. [Trakt API](https://trakt.docs.apiary.io/#introduction/verbs)
API pública e gratuita utilizada neste projeto para recuperar informações de séries e filmes.
É necessário se cadastrar no site oficial e criar um "Trakt API app" para gerar uma API Key necessária para consumir os dados (que deve ser acrescentada no .env como descrito [aqui](https://github.com/amandagpearce/art-refs-api#arquivo-env)). 
A API possui uma [documentação detalhada aqui](https://trakt.docs.apiary.io/#introduction/verbs) de como se cadastrar, gerar a API Key e fazer os requests. 

Endpoints utilizados:

| Endpoint                               | Descrição                               |
| -------------------------------------- | --------------------------------------- |
| https://api.trakt.tv/search/show       | Retorna informações sobre séries.       |
| https://api.trakt.tv/search/movie      | Retorna informações sobre filmes.       |



2. [TMDB API](https://developer.themoviedb.org/reference/intro/getting-started)
API pública e gratuita utilizada neste projeto para recuperar o endereço da imagem que será usada como poster para cada filme ou série exibidos na [Home do front-end](https://github.com/amandagpearce/got-that-ref#home).
Na response das requisições do Trakt é fornecida a id do filme/série no TMDB, com essa id, o endereço da imagem do poster é retornado.  

É necessário se cadastrar no site oficial para gerar uma API Key (que deve ser acrescentada no .env como descrito [aqui](https://github.com/amandagpearce/art-refs-api#arquivo-env)). 
A API possui uma [documentação detalhada aqui](https://developer.themoviedb.org/reference/intro/getting-started) de como se cadastrar, gerar a API Key e fazer os requests.

Endpoints utilizados:

| Endpoint                                   | Descrição                                |
| ------------------------------------------ | ---------------------------------------- |
| https://api.themoviedb.org/3/tv/<id>       | Retorna a url do poster da referida id.  |
| https://api.themoviedb.org/3/movie/<id>    | Retorna a url do poster da referida id.  |



3. [Google Image Service](https://github.com/amandagpearce/google-image-service)
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
Substitua `keystringaqui` pelas suas keys. 

## Instalação com Docker
1. Clone o projeto
2. Crie o arquivo .env como descrito acima e cole na raiz do projeto 
3. Na raiz do projeto, crie a imagem:
```bash
  docker build -t art-refs-api .
```

4. Rode a imagem criada:
```bash
  docker run -p 4000:4000 art-refs-api
```
5. Acesse a documentação GraphiQL no endereço http://127.0.0.1:4000/graphiql


## Instalação sem Docker
1. Clone o projeto
2. Crie o arquivo .env como descrito acima e cole na raiz do projeto 
3. Na raiz do projeto, rode o comando:
```bash
  flask run --host 0.0.0.0 --port 4000
```
4. Acesse a documentação GraphiQL no endereço http://127.0.0.1:4000/graphiql


## Banco de dados 
A aplicação utiliza um banco de dados sqlite cujas tabelas e campos são:

### Artworks Table

| Field Name       | Data Type  | Description                    |
|------------------|------------|--------------------------------|
| id               | Integer    | Primary Key                     |
| artworkTitle     | String     | Título da Obra de Arte         |
| year             | Integer    | Ano de Criação da Obra         |
| artist           | String     | Nome do Artista                |
| size             | String     | Tamanho da Obra                |
| description      | String     | Descrição da Obra              |
| currentLocation  | String     | Localização Atual              |
| imageUrl         | String     | URL da Imagem da Obra          |

**Relacionamentos:**
- One-to-Many with SeriesScene (series_scenes)
- One-to-Many with MovieScene (movie_scenes)

### Movies Table

| Field Name       | Data Type  | Description                    |
|------------------|------------|--------------------------------|
| id               | Integer    | Primary Key                     |
| productionTitle  | String     | Título da Produção Cinematográfica |
| year             | Integer    | Ano de Produção                |
| imageUrl         | String     | URL da Imagem da Produção      |

### Movie Scenes Table

| Field Name       | Data Type  | Description                    |
|------------------|------------|--------------------------------|
| id               | Integer    | Primary Key                     |
| artworkId        | Integer    | Chave Estrangeira para Artwork  |
| sceneDescription | String     | Descrição da Cena              |
| sceneImgUrl      | String     | URL da Imagem da Cena          |
| movieId          | Integer    | Chave Estrangeira para Movies  |

**Relacionamentos:**
- Many-to-One with Artwork (artwork)
- Many-to-One with Movies (movie)

### Series Table

| Field Name       | Data Type  | Description                    |
|------------------|------------|--------------------------------|
| id               | Integer    | Primary Key                     |
| productionTitle  | String     | Título da Série                |
| year             | Integer    | Ano de Produção da Série       |
| imageUrl         | String     | URL da Imagem da Série         |

### Series Scenes Table

| Field Name       | Data Type  | Description                    |
|------------------|------------|--------------------------------|
| id               | Integer    | Primary Key                     |
| seriesId         | Integer    | Chave Estrangeira para Series   |
| artworkId        | Integer    | Chave Estrangeira para Artwork  |
| sceneDescription | String     | Descrição da Cena              |
| season           | Integer    | Temporada                       |
| episode          | Integer    | Episódio                        |
| sceneImgUrl      | String     | URL da Imagem da Cena          |

**Relacionamentos:**
- Many-to-One with Artwork (artwork)

### References to approve Table

| Field Name       | Data Type  | Description                    |
|------------------|------------|--------------------------------|
| id               | Integer    | Primary Key                     |
| productionType   | String     | Tipo de Produção                |
| productionTitle  | String     | Título da Produção              |
| productionYear   | Integer    | Ano de Produção da Produção    |
| season           | Integer    | Temporada                       |
| episode          | Integer    | Episódio                        |
| artist           | String     | Nome do Artista                |
| artworkTitle     | String     | Título da Obra de Arte         |
| artworkDescription | String   | Descrição da Obra de Arte      |
| artworkYear      | Integer    | Ano da Obra de Arte            |
| size             | String     | Tamanho da Obra de Arte        |
| currentLocation  | String     | Localização Atual da Obra      |
| sceneDescription | String     | Descrição da Cena              |
| sceneImgUrl      | String     | URL da Imagem da Cena          |
