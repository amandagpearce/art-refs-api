# Art refs API

Projeto criado como componente B do MVP da disciplina de Back-end avançado do curso de pós-graduação em Desenvolvimento Full Stack da PUC-Rio. 

## O que é?
Implementação da API do chatGPT para buscar referencias de Artes Visuais em séries de tv.

[GraphiQL Playground](http://127.0.0.1:5000/graphiql)

### Rodando o projeto com Docker
1. Clone o projeto
2. Na raiz do projeto, crie a imagem:
```bash
  docker build -t art-refs-api .
```

3. Rode a imagem criada:
```bash
  docker run -p 4000:4000 art-refs-api
```

