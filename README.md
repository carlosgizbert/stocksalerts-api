### StocksAlerts

### objetivo da aplicação
Cadastrar, alterar e excluir ativos e rastrealos com base no valor minimo e máximo por tempo determinado pelo usuário para verificação dos preços de cada ativo

### desenvolvido
* ✔️ cadastro usuário
* ✔️ autenticação do usuário via jwt
* ✔️ cadastro/edição/exclusão de ativos
* ✔️ historico de preços dos ativos em tempo real
* ✔️ notificações por email

### principais tecnologias
* <a href="https://www.djangoproject.com/" about="_blank">Django + Rest framework (DRF)</a> (Django SimpleJWT para autenticação)
* <a href="https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html" about="_blank">Celery + Redis</a> (Gestão de funções assíncronas)
* <a href="https://www.postgresql.org/" about="_blank">PostgreSQL</a>

### resultado
#### <a href="https://stocksalerts-web.vercel.app/" target="_blank">`www.stocksalerts-web.vercel.app`</a>

# como rodar ?

Postman Collection: https://www.postman.com/science-operator-37788421/workspace/stocksalerts/collection/35578097-470d9583-b0ec-4f0e-b230-36b4691a4d39?action=share&creator=35578097

Premissas: Esteja no ambiente linux.

Após clonar o projeto, criar VENV do Python e acessá-la,
Através do terminal, entre na pasta do projeto e rode os comandos abaixo ...

Instale o homebrew
1. /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. brew --version
3. brew install redis

Caso possua zsh, e ele nao reconheça o brew:
1. (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /home/carlos/.zshrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
2. source ~/.zshrc

Verifique ostatus do redis
1. brew services info redis

Verifique se o servidor do redis pode ser usado
1. redis-server

Iniei o serviço do Redis
1. brew services start redis

Garanta que o redis rodou com o CLI
1. redis-cli (escrever ping e apertar ENTER, deverá retornar PONG)

Rode os comandos abaixo:
1. python manage.py runserver
2. celery -A prostocks worker -l info
3. celery -A prostocks beat -l info
