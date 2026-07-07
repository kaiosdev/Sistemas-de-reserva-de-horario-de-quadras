# 🚀 Como rodar o Athletix no VSCode

## Passo 0 — Pré-requisitos

Instale estes programas (se ainda não tem):

| Programa | Para que | Download |
|----------|----------|----------|
| **Python 3.10+** | Rodar o backend | https://www.python.org/downloads/ |
| **PostgreSQL + pgAdmin** | Banco de dados | https://www.postgresql.org/download/ |
| **VSCode** | Editor de código | https://code.visualstudio.com/ |
| **Extensão Python** (VSCode) | Rodar Python no VSCode | Abra VSCode → Extensions → pesquise "Python" → Install |

> ⚠️ Ao instalar o Python, **marque a opção "Add Python to PATH"**.

---

## Passo 1 — Abrir o projeto no VSCode

1. Abra o VSCode
2. `File` → `Open Folder`
3. Navegue até a pasta do projeto:
   ```
   C:\Users\Jean\Downloads\athe\Sistemas-de-reserva-de-horario-de-quadras
   ```
4. Clique em **Selecionar Pasta**

---

## Passo 2 — Abrir o terminal no VSCode

1. No VSCode, pressione `` Ctrl + ` `` (backtick)
2. Ou: menu superior → `Terminal` → `New Terminal`
3. O terminal abre na pasta do projeto ✅

---

## Passo 3 — Criar ambiente virtual

No terminal do VSCode, digite:

```bash
python -m venv .venv
```

Ativar o ambiente virtual:

**No Windows:**
```bash
.venv\Scripts\activate
```

**No Linux/macOS:**
```bash
source .venv/bin/activate
```

> O terminal vai mudar para `(.venv)` no início da linha — isso significa que o ambiente está ativo ✅

---

## Passo 4 — Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Passo 5 — Configurar o banco de dados

### 5.1 Criar o banco
1. Abra o **pgAdmin** (início → pgAdmin 4)
2. Clique com o botão direito em **Databases** → **Create** → **Database**
3. Nome: `athe`
4. Clique **Save**

### 5.2 Executar o schema
1. No pgAdmin, clique em `athe` → **Tools** → **Query Tool**
2. Abra o arquivo `database/schema.sql` (arraste para o VSCode)
3. Copie TODO o conteúdo
4. Cole no Query Tool do pgAdmin
5. Clique em **▶ Execute** (ou F5)

### 5.3 Criar o arquivo `.env`
Na raiz do projeto, crie um arquivo chamado `.env` com:

```
DB_HOST=localhost
DB_NAME=athe
DB_USER=postgres
DB_PASSWORD=sua_senha_do_postgres
```

> Troque `sua_senha_do_postgres` pela senha que você definiu ao instalar o PostgreSQL.

---

## Passo 6 — Rodar o sistema

### Opção A: Interface Web (recomendada)

No terminal do VSCode:

```bash
python backend/app.py
```

Vai aparecer:

```
============================================================
  ATHLETIX rodando em http://127.0.0.1:5000
  Abra no navegador: http://127.0.0.1:5000
============================================================
```

Agora abra o navegador (Chrome/Edge/Firefox) e acesse:
👉 **http://127.0.0.1:5000**

### Opção B: Interface Desktop (Tkinter)

```bash
python main.py
```

A janela desktop vai abrir com tema dark moderno.

---

## 🛑 Para parar o servidor

No terminal do VSCode: `Ctrl + C`

---

## ❌ Problemas comuns

| Problema | Solução |
|----------|---------|
| `pip não é reconhecido` | Python não está no PATH. Reinstale marcando "Add to PATH" |
| `No module named 'flask'` | O `.venv` não está ativado. Execute `venv\Scripts\activate` |
| `coluna id_espaco não existe` | O banco foi criado com schema antigo. Execute o `schema.sql` novamente |
| `Não foi possível conectar à API` | O `python backend/app.py` não está rodando. Abra outro terminal e execute |
| `relation "cliente" does not exist` | O `schema.sql` não foi executado. Volte ao Passo 5 |

---

## 📁 Estrutura do projeto no VSCode

```
Athletix/
├── 📄 main.py              ← ponto de entrada (desktop)
├── 📄 requirements.txt     ← dependências
├── 📄 .env                 ← credenciais do banco (NÃO commitar)
│
├── 📁 database/            ← schema.sql + conexão PostgreSQL
├── 📁 models/              ← classes de domínio (POO)
├── 📁 repositories/        ← CRUD + busca no banco
├── 📁 services/            ← regras de negócio
├── 📁 ui/                  ← interface desktop (CustomTkinter)
│
├── 📁 backend/             ← API REST (Flask)
│   └── 📁 routes/          ← endpoints
│
├── 📁 frontend/            ← interface web (HTML/CSS/JS)
│   ├── index.html
│   ├── css/style.css
│   └── js/ (6 arquivos)
│
└── 📁 docs/                ← documentação POO
```
