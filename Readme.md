# 🚛 Sistema de Agendamento de Carros para Descarrego

Este projeto é um sistema web desenvolvido com **Django** que permite o **agendamento, controle e gestão de veículos** que chegam para descarregar mercadorias. 
O sistema possui dois níveis de acesso: **usuário comum** e **gerente**, cada um com permissões específicas.

## 🔧 Funcionalidades

### 👤 Área do Usuário
- Login e autenticação.
- Cadastro de agendamentos (respeitando regras de disponibilidade).
- Acesso somente ao seu formulário de agendamento.
- **Filtros por período, status e galpão** na visualização dos próprios agendamentos.

### 🛠 Área do Gerente
- Acesso restrito com permissão de gerente.
- Visualização de todos os agendamentos com filtros por período, status e galpão.
- Visualização detalhada de produtos de cada agendamento via modal.
- **Totais gerais de quantidade e cubagem** apresentados ao final da tabela.
- Alteração do status dos agendamentos por meio de botões (Confirmar, Finalizar, Editar, Cancelar)
- Cadastro e exclusão de usuários.
- Paginação da listagem de agendamentos.

### 📊 Dashboard Gerencial
- Indicadores de:
  - Agendamentos do dia.
  - Quantidade de agendamentos por status (pendente, confirmado, cancelado, finalizado).
- **Filtro por período**.
- Gráfico de agendamentos por dia (via Chart.js).
- Exportação dos dados filtrados para CSV.

---

## ⚙️ Tecnologias Utilizadas

- Django (backend e autenticação)
- Postgresql (banco de dados em produção, configurado via `.env`)
- Bootstrap 5 (interface e responsividade)
- Chart.js (visualização gráfica dos dados)

---

## ✅ Validações de Agendamento

- ❌ **Não é permitido agendar em feriados**:  
  O sistema realiza uma validação automática para impedir agendamentos em datas consideradas feriados nacionais. 
  Essa verificação é feita no momento do cadastro e impede a conclusão do agendamento.  
  Os feriados atualmente considerados são fixos e definidos diretamente no código

- 🏭 **Limite de docas por galpão**:  
  Cada galpão possui um número máximo de agendamentos simultâneos (docas). O sistema verifica se há docas disponíveis antes de permitir um novo agendamento.
  Este limite é configurável por galpão diretamente no modelo do sistema.

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

### 4. Execute as migrações e rode o servidor

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
