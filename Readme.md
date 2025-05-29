# 🚛 Sistema de Agendamento de Carros para Descarrego

Este projeto é um sistema web desenvolvido com **Django** que permite o **agendamento, controle e gestão de veículos** que chegam para descarregar mercadorias.
O sistema possui dois níveis de acesso: **usuário comum** e **gerente**, cada um com permissões específicas.

## 🔧 Funcionalidades

### 👤 Área do Usuário

* Login e autenticação.
* Cadastro de agendamentos (respeitando regras de disponibilidade).
* Acesso somente ao seu próprio formulário de agendamento.
* **Filtros** por período, status e galpão na visualização dos próprios agendamentos.

### 🛠 Área do Gerente

* Acesso restrito com permissão de gerente.
* Visualização de todos os agendamentos, com **filtros** por período, status e galpão.
* Visualização detalhada dos produtos de cada agendamento via modal.
* **Totais gerais de quantidade e cubagem** apresentados ao final da tabela.
* Alteração do status dos agendamentos por meio de botões (Confirmar, Finalizar, Editar, Cancelar).
* Cadastro e exclusão de usuários.
* Paginação da listagem de agendamentos.

### 📊 Dashboard Gerencial

* Indicadores de:

  * Agendamentos do dia.
  * Quantidade de agendamentos por status (pendente, confirmado, cancelado, finalizado).
* **Filtro por período**.
* Gráfico de agendamentos por dia (via Chart.js).
* Exportação dos dados filtrados para CSV.

---

## ⚙️ Tecnologias Utilizadas

* **Django** (backend e autenticação)
* **PostgreSQL** (banco de dados em produção, configurado via `.env`)
* **Bootstrap 5** (interface e responsividade)
* **Chart.js** (visualização gráfica dos dados)

---

## ✅ Validações de Agendamento

* ❌ **Agendamentos não são permitidos em feriados:**
  O sistema impede agendamentos em feriados nacionais, definidos no código.

* 🏭 **Limite diário de agendamentos por galpão:**
  Cada galpão tem um limite de agendamentos diários. Se o limite for atingido, o sistema sugere as datas mais próximas (anteriores ou posteriores) com disponibilidade.

---

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/devthayron/agendamento.git
cd agendamento
```

### 2. Crie o arquivo `.env`

Antes de rodar o projeto, crie um arquivo `.env` na raiz do projeto com as configurações para desenvolvimento:

```env
SECRET_KEY='SENHA_SEGURA_DEV'
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=
```

⚠️ **Não versionar o `.env`!** Esse arquivo contém informações sensíveis. O projeto já inclui uma entrada no `.gitignore` para que ele não seja enviado ao GitHub.

### 3. Instale as dependências

Crie um ambiente virtual e instale os pacotes:

```bash
python -m venv venv
venv\Scripts\activate  # no Windows
pip install -r requirements.txt
```

### 4. Execute as migrações e inicie o servidor

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```