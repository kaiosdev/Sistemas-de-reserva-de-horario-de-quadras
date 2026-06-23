# 🏟️ Athletix SI - Sistema de Gestão de Espaços e Quadras

> Projeto prático de modelagem e implementação de uma base de dados relacional para gestão de reservas de espaços desportivos.

## 👥 Equipa de Desenvolvimento
A divisão do projeto foi planeada para garantir um ambiente colaborativo e sem conflitos de versionamento, distribuindo responsabilidades na construção da base de dados:

* **Kaio Sobral Moreira** : Responsável pela infraestrutura, repositório e criação das entidades primárias independentes.
* **Ricky Brendon da Silva Almeida**: Responsável pelo Modelo Conceitual (DER), Modelo Lógico e criação das tabelas dependentes (com Chaves Estrangeiras).
* **Jean Carlos dos Santos Baraúna** : Responsável pela consolidação da documentação (PDF), implementação do módulo financeiro e codificação das regras de negócio complexas (Triggers).

---

## 🎯 O Projeto
O **Athletix SI** soluciona o problema de gestão manual de horários em complexos desportivos, evitando falhas humanas como a sobreposição de reservas (choque de horários) e a perda de registos financeiros. 

### Principais Funcionalidades:
- **Gestão de Clientes:** Registo seguro com validação de unicidade para CPF e E-mail.
- **Catálogo de Espaços:** Vinculação de quadras/salas a modalidades específicas com definição de valor por hora.
- **Agendamentos Seguros:** Sistema transacional que cruza datas e horas de início/fim.
- **Bloqueio de Choque de Horários:** Regra de negócio implementada nativamente no SGBD (via `TRIGGER`) para impedir que dois clientes reservem o mesmo espaço no mesmo momento.
- **Gestão de Pagamentos:** Geração automática do estado financeiro de cada reserva.

---

## 🗂️ Estrutura de Ficheiros (Modelo Físico)
Para garantir a integridade referencial, os scripts DDL devem ser executados **estritamente na ordem numérica abaixo**:

1. `01_Modalidade.sql`: Criação da Base de Dados (`athletix_db`) e tabela Modalidade.
2. `02_Cliente.sql`: Criação da tabela de Clientes.
3. `03_Espaco.sql`: Criação da tabela de Espaços (com FK para Modalidade).
4. `04_Agendamento.sql`: Criação da tabela de Agendamentos (com FK para Cliente e Espaço).
5. `05_Pagamento.sql`: Criação da tabela de Pagamentos (com FK para Agendamento).
6. `06_Trigger_Valida_Horario.sql`: Implementação da barreira temporal transacional.

---

## 🚀 Como Executar o Projeto

**Pré-requisitos:**
* Ter o SGBD **MySQL (8.0+)** instalado.
* Interface gráfica como **MySQL Workbench** ou DBeaver.

**Passo a passo:**
1. Clone este repositório para a sua máquina local:
   ```bash
   git clone [https://github.com/kaiosdev/Sistemas-de-reserva-de-horario-de-quadras.git](https://github.com/kaiosdev/Sistemas-de-reserva-de-horario-de-quadras.git)
