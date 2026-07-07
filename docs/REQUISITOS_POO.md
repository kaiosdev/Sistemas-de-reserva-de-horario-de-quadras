# Requisitos de POO e Banco de Dados — Mapeamento no código

Este documento mapeia cada requisito do trabalho ao local exato onde foi
atendido no projeto **Athletix**, facilitando a correção e justificando o uso
de cada conceito.

---

## 1. Classes de domínio (mínimo 4)

| Classe | Arquivo | Tabela correspondente |
|--------|---------|----------------------|
| `Cliente` | `models/cliente.py` | `Cliente` |
| `Espaco` | `models/espaco.py` | `Espaco` |
| `Agendamento` | `models/agendamento.py` | `Agendamento` |
| `Pagamento` (+ subclasses) | `models/pagamento.py` | `Pagamento` |
| `Modalidade` | `models/modalidade.py` | `Modalidade` |

**5 classes de domínio** (acima do mínimo exigido).

---

## 2. Atributos e métodos

Todas as classes possuem atributos de instância (`__init__`) e métodos:

- `Cliente.de_texto()` — *factory method* / named constructor
- `Cliente.__eq__()` e `__repr__()` — métodos especiais
- `Pagamento.processar()` — método abstrato implementado nas subclasses
- `Espaco.__str__()` — representação textual

A classe `Cliente` ainda tem **atributo de classe** `total_clientes`,
compartilhado por todas as instâncias.

---

## 3. Encapsulamento

Local: `models/cliente.py`

```python
class Cliente:
    def __init__(self, id_cliente, nome, cpf, endereco, telefone="Nao informado"):
        ...
        self.__cpf = cpf          # ATRIBUTO PRIVADO (name mangling)
        ...

    @property
    def cpf(self):                # ACESSO CONTROLADO via getter
        return self.__cpf
```

O CPF é **privado** (`__cpf`) e só pode ser lido pela *property* `cpf`,
impedindo acesso/alteração direta externa.

---

## 4. Herança

Local: `models/pagamento.py`

```
Pagamento (classe abstrata)
   ├── PagamentoPix
   └── PagamentoCartao
```

```python
class PagamentoPix(Pagamento):
    def __init__(self, id_pagamento, valor_total, id_agendamento, chave_pix, status="Pendente"):
        super().__init__(id_pagamento, valor_total, id_agendamento, status)
        self.chave_pix = chave_pix
```

`PagamentoPix` e `PagamentoCartao` **herdam** de `Pagamento` e usam `super()`
para reaproveitar a inicialização da superclasse.

---

## 5. Classe abstrata com ABC + @abstractmethod

Local: `models/pagamento.py`

```python
from abc import ABC, abstractmethod

class Pagamento(ABC):
    @abstractmethod
    def processar(self) -> str:
        pass
```

**Justificativa (contrato definido):**
A classe `Pagamento` é abstrata e define o contrato: **todo pagamento deve
saber se processar** e retornar o status final (`'Pago'` ou `'Cancelado'`).
Ela **não pode ser instanciada diretamente** — só suas subclasses concretas
(`PagamentoPix`, `PagamentoCartao`). Isso obriga cada forma de pagamento a
implementar sua própria lógica, garantindo consistência.

---

## 6. Polimorfismo

Local: `services/pagamento_service.py` (método `processar`)

```python
# factory instancia a subclasse correta conforme a forma
pagamento = factory_pagamento(forma_pagamento=forma, ...)

# MESMA chamada de método, COMPORTAMENTO DIFERENTE:
status_resultante = pagamento.processar()
```

- `PagamentoPix.processar()` → sempre confirma (`'Pago'`)
- `PagamentoCartao.processar()` → recusa se valor > R$ 1000 (`'Cancelado'`)

O **mesmo método** `processar()` é invocado em objetos diferentes, produzindo
comportamentos distintos — exatamente o polimorfismo exigido. O caller
(`PagamentoService`) não precisa saber qual subclasse está manipulando.

---

## 7. `__str__` em classes principais

Todas as classes principais implementam `__str__`:

- `Cliente.__str__` → `"Cliente(ID: 1 | Nome: Joao)"`
- `Espaco.__str__` → `"Espaco: Quadra Central [Futsal] (Oficial) - ..."`
- `Agendamento.__str__` → `"Reserva 5: Data 2026-07-10 das 14:00 as 16:00"`
- `Pagamento.__str__` → `"Pagamento #1 | R$ 80.00 | PagamentoPix | Pago"`
- `PagamentoPix.__str__` → inclui a chave PIX
- `PagamentoCartao.__str__` → inclui o final do cartão
- `Modalidade.__str__` → `"Modalidade(ID: 1 | Futsal)"`

---

## 8. Tratamento de Exceções

- **Regra de negócio no banco**: trigger `func_valida_choque_horario`
  (`database/schema.sql`) lança exceção em choque de horário. O
  `AgendamentoService.criar()` captura e repassa.
- **Validações de domínio** em todos os services lançam `ValueError`
  (CPF inválido, valor ≤ 0, modalidade inexistente, etc.).
- **Rotas Flask** (`backend/routes/`) fazem `try/except` distinguindo
  `ValueError` (HTTP 400) de outros erros (HTTP 500).
- **Frontend** trata erros de conexão em `js/api.js` com mensagens amigáveis.

---

## 9. Banco de Dados (PostgreSQL)

### 9.1 Tabelas (5, acima do mínimo de 3)
`Modalidade`, `Cliente`, `Espaco`, `Agendamento`, `Pagamento`

### 9.2 Chave primária em cada tabela
Todas têm `SERIAL PRIMARY KEY` (`id_modalidade`, `id_cliente`, `id_espaco`,
`id_agendamento`, `id_pagamento`).

### 9.3 Relacionamentos
```
Espaco → Modalidade       (id_modalidade, FK)
Agendamento → Cliente      (id_cliente, FK)
Agendamento → Espaco       (id_espaco, FK)
Pagamento → Agendamento    (id_agendamento, FK, ON DELETE CASCADE)
```

### 9.4 Comandos SQL completos (INSERT/SELECT/UPDATE/DELETE)

| Comando | Onde está (exemplo) |
|---------|---------------------|
| INSERT | `ClienteRepository.inserir()`, `EspacoRepository.inserir()` |
| SELECT | `listar_todos()`, `buscar_por_cpf()`, `buscar_por_nome()` |
| UPDATE | `atualizar()` em todos os repositories |
| DELETE | `deletar()` em todos os repositories |

### 9.5 CRUD completo
Todas as entidades (Cliente, Espaco, Agendamento, Pagamento) têm
**CRUD completo**: criar, listar, **buscar por critério**, atualizar e excluir.

---

## 10. Busca por critério

Local: `repositories/cliente_repository.py` + `services/cliente_service.py`

```python
def buscar_por_cpf(self, cpf):        # SELECT ... WHERE cpf = %s
def buscar_por_nome(self, termo):     # SELECT ... WHERE nome ILIKE %termo%

# service
def buscar(self, criterio):           # une CPF + nome e remove duplicados
```

Endpoint: `GET /api/clientes?q=<termo>` · Frontend: campo de busca em tempo real.

---

## 11. Regras de negócio orientadas a objetos

| Regra | Onde | Como |
|-------|------|------|
| **Não permitir choque de horário** (double-booking) | `database/schema.sql` (trigger) + `AgendamentoService` | Impede 2 reservas no mesmo espaço/data/horário sobreposto |
| **CPF obrigatório e com 11 dígitos** | `services/cliente_service.py` | `len(cpf) not in (11, 14)` lança `ValueError` |
| **Valor/hora deve ser > 0** | `services/espaco_service.py` | `if valor <= 0: raise ValueError(...)` |
| **Não agendar no passado** | `services/agendamento_service.py` | `data_obj < date.today()` |
| **Pagamento de cartão > R$ 1000 é recusado** | `models/pagamento.py` (`PagamentoCartao.processar`) | Regra polimórfica |

---

## 12. Organização em pacotes

```
athletix/
├── main.py                 # ponto de entrada (interface desktop)
├── requirements.txt
├── database/               # conexão + schema + migrações
│   ├── connection.py
│   └── schema.sql
├── models/                 # classes de domínio
│   ├── cliente.py
│   ├── espaco.py
│   ├── agendamento.py
│   ├── pagamento.py        # ABC + herança + polimorfismo
│   └── modalidade.py
├── repositories/           # acesso ao banco (CRUD + busca)
├── services/               # regras de negócio
├── ui/                     # interface desktop (CustomTkinter)
├── backend/                # API REST Flask
└── frontend/               # interface web (HTML/CSS/JS)
```

**Relação objeto ↔ tabela ↔ operação** (exemplo pedido no enunciado):

| Objeto (classe) | Tabela | Operações no sistema |
|-----------------|--------|----------------------|
| `Cliente` | `Cliente` | cadastrar, listar, **buscar por CPF/nome**, editar, excluir |
| `Espaco` | `Espaco` | cadastrar, listar, editar, excluir |
| `Agendamento` | `Agendamento` | criar (valida choque), listar, editar, excluir |
| `Pagamento` | `Pagamento` | processar (polimórfico), listar, editar, excluir |
| `Modalidade` | `Modalidade` | cadastrar, listar |

Os objetos são instanciados a partir das linhas do banco e usados na lógica
de negócio (ex.: `factory_pagamento()` cria o objeto e chama `.processar()`).
