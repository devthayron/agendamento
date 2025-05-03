# 🚛 Sistema de Agendamento de Carros para Descarrego

Este projeto é um sistema web desenvolvido com **Django** que permite o **agendamento, controle e gestão de veículos** que chegam para descarregar mercadorias. O sistema possui dois níveis de acesso: **usuário comum** e **gerente**, cada um com permissões específicas.

## 🔧 Funcionalidades

### 👤 Área do Usuário
- Login e autenticação.
- Acesso ao formulário de agendamento.
- Cadastro de agendamentos com:
  - Data e hora.
  - CNPJ.
  - Fornecedor.
  - Quantidade de mercadoria.
  - Tipo de carga.

### 🛠 Área do Gerente
- Acesso restrito com permissão de gerente.
- Visualização de todos os agendamentos.
- Cancelamento, confirmação e finalização de agendamentos.
- Cadastro e exclusão de usuários.
- Filtros por data, CNPJ, fornecedor e tipo de carga.
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
- SQLite (banco de dados local)
- Bootstrap 5 (interface e responsividade)
- Chart.js (visualização gráfica dos dados)

---

## 🚀 Instalação e Execução

### 1. Clone o repositório
```bash
git clone https://github.com/devthayron/agendamento.git
cd agendamento-carros
