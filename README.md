# 🍊 Hackathon Season 2 Fcamara
###  Backend em Python 

#### Projeto realizado para fins de estudos, seguindo a problematica de um hackathon em qual fui mentor.


### 🐱‍🏍 Problemática

Com a vacinação em andamento, já podemos enxergar novas possibilidades, e aqui na FCamara não é diferente. 

Com muito cuidado e segurança estamos planejando a reabertura dos nossos escritórios. Estamos muito felizes com essa novidade, mas sabemos que não será como antes. 

Para organizar essa reabertura, precisamos criar uma aplicação web, onde o consultor deverá realizar o agendamento, com dia e horário, para poder ir ao escritório.

### ✨ Solução proposta

Tendo em vista o desafio, desenvolvi uma API para uma aplicação Web escalável, onde a empresa pode se cadastrar e cadastrar seus escritórios e funcionarios. 

Uma vez cadastrado pela empresa, o funcionario pode marcar seus agendamentos. 

A empresa consegue ter o controle dos agendamentos de seus funcionarios, e a lotação de cada escritório podendo a qualquer momento adicionar ou remover um escritório, ou até mesmo atualiza-lo em relação a quantidade de vagas e o ocupamento máx permitido por lei ou pela própria empresa. 

### DB - Diagrama ER    
<p align="center"><img src="https://github.com/Arturhen/hackathon-python/blob/master/img/db-er.png" width="500"/></p>

### Instalação

#### Requisitos:
    -Docker

Para rodar a aplicação você vai precisar fazer o download ou o clone do repositório em sua maquina 

após o donwload entre na pasta do projeto abra o terminal e rode o seguinte comando:

```ps
docker-compose up -d --build
```   

Após isso estarão rodando 2 containers em sua maquina, um com o banco de dados do postgress outro com o python rodando a aplicação

#### Rotas:

A documentação das rotas foi feita atravez do [👨🏽‍🚀Postman](https://documenter.getpostman.com/view/17572187/UUxtDq4S) e a do insomnia esta na pasta docs é só importar no programa

### 🛠 Tecnologias
- **[Docker](https://www.docker.com/)**
- **[Python](https://www.python.org/)**
- **[Flask](https://flask.palletsprojects.com/en/2.0.x/)**
- **[JWT](https://jwt.io/)**
- **[Sql Alchemy](https://www.sqlalchemy.org/)**


## 👨🏽‍🚀 Autor 
<img src="https://github.com/Arturhen.png" width="90"/>

**Artur Henrique**

[![Linkedin Badge](https://img.shields.io/badge/-github-181717?style=for-the-badge&logo=Github&logoColor=white&link=https://github.com/Arturhen/)](https://github.com/Arturhen/)

[![Linkedin Badge](https://img.shields.io/badge/-Artur_Henrique-blue?style=for-the-badge&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/artur-henrique-do-nascimento-souza/)](https://www.linkedin.com/in/artur-henrique-do-nascimento-souza/)

## 📝 Licença
Este projeto esta sobe a licença [MIT](https://github.com/Arturhen/hackathon-python/blob/master/LICENSE).
