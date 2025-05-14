Aqui está o trecho atualizado do seu `README.md`, com a explicação sobre o uso do arquivo `.env` e como configurar o banco de dados de forma segura:

````md
# 🚛 Sistema de Agendamento de Carros para Descarrego

Este projeto é um sistema web desenvolvido com **Django** que permite o **agendamento, controle e gestão de veículos** que chegam para descarregar mercadorias. O sistema possui dois níveis de acesso: **usuário comum** e **gerente**, cada um com permissões específicas.

## 🔧 Funcionalidades

### 👤 Área do Usuário
- Login e autenticação.
- Cadastro de agendamentos.
- Acesso somente ao seu formulário de agendamento.
  
### 🛠 Área do Gerente
- Acesso restrito com permissão de gerente.
- Visualização de todos os agendamentos.
- Cancelamento, confirmação e finalização de agendamentos.
- Cadastro e exclusão de usuários.
- Filtros por status.
- Paginação da listagem de agendamentos.

### 📊 Dashboard Gerencial
- Indicadores de:
  - Agendamentos do dia.
  - Quantidade de agendamentos por status (pendente, confirmado, cancelado, finalizado).
- Filtro por período.
- Gráfico de agendamentos por dia (via Chart.js).
- Exportação dos dados filtrados para CSV.

---

## ⚙️ Tecnologias Utilizadas

- [Django](https://www.djangoproject.com/) (backend e autenticação)
- MySQL (banco de dados em produção, configurado via `.env`)
- Bootstrap 5 (interface e responsividade)
- Chart.js (visualização gráfica dos dados)

---

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/devthayron/agendamento.git
cd agendamento
````

### 2. Crie o arquivo `.env`

Antes de rodar o projeto, crie um arquivo `.env` na raiz do projeto com as configurações do banco de dados:

```env
DB_NAME=seu_banco_de_dados
DB_USER=seu_usuario
DB_PASSWORD="sua_senha_segura"
DB_HOST=localhost
DB_PORT=3306
```

⚠️ **Não versionar o `.env`!** Esse arquivo contém informações sensíveis. O projeto já inclui uma entrada no `.gitignore` para que ele não seja enviado ao GitHub.

### 3. Instale as dependências

Crie um ambiente virtual e instale os pacotes:

```bash
python -m venv venv
venv\Scripts\activate  # no Windows
pip install -r requirements.txt
```

### 4. Execute as migrações e rode o servidor

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
