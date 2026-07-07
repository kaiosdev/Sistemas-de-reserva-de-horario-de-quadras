<div align="center">
  <h1>🏆 ATHLETIX</h1>
  <h3>Sistema de Gestão de Espaços Esportivos</h3>
  <p><i>Projeto Interdisciplinar: Sistemas de Banco de Dados I & Programação Orientada a Objetos</i></p>
  <p><b>ICET - Universidade Federal do Amazonas (UFAM)</b></p>
</div>

<hr>

<h2>📍 Sobre o Projeto</h2>
<p>O <strong>Athletix</strong> foi desenvolvido para solucionar problemas comuns na administração de complexos esportivos, como o choque de horários (double-booking) e a falta de controle financeiro. O sistema utiliza uma arquitetura robusta orientada a objetos em Python integrada a um banco de dados relacional PostgreSQL, garantindo integridade de dados e aplicação de regras de negócio consistentes.</p>

<p>O projeto possui <strong>duas interfaces</strong> conectadas ao mesmo backend/banco:</p>
<ul>
  <li>🖥️ <strong>Interface Web moderna</strong> (HTML/CSS/JS + API Flask) — visual <em>top de linha</em> com tema dark, glassmorphism e dashboard.</li>
  <li>🖥️ <strong>Interface Desktop</strong> (CustomTkinter) — versão redesenhada do app original em Tkinter.</li>
</ul>

<p>O <strong>fluxo de gerenciamento</strong> segue o encadeamento das entidades (inspirado no diagrama de classes):</p>
<p align="center"><code>Modalidade → Espaço → Cliente → Agendamento → Pagamento</code></p>

<hr>

<h2>🧰 Tecnologias Utilizadas</h2>
<ul>
  <li><strong>Linguagem:</strong> Python 3</li>
  <li><strong>Backend Web (API REST):</strong> Flask + Flask-CORS</li>
  <li><strong>Interface Web:</strong> HTML5, CSS3 e JavaScript (vanilla, sem build)</li>
  <li><strong>Interface Desktop:</strong> CustomTkinter (tema dark moderno)</li>
  <li><strong>Banco de Dados:</strong> PostgreSQL</li>
  <li><strong>Dependências:</strong> <code>flask</code>, <code>flask-cors</code>, <code>customtkinter</code>, <code>psycopg2</code>, <code>python-dotenv</code></li>
</ul>

<hr>

<h2>🏗️ Arquitetura do Sistema</h2>
<pre>
Athletix/
├── database/            # Scripts SQL (Tabelas e Trigger) e conexão (PostgreSQL)
├── models/              # Classes de domínio (Abstração, Encapsulamento, Herança e Polimorfismo)
├── repositories/        # Persistência de dados e CRUD
├── services/            # Regras de negócio e validações
├── ui/                  # Interface Desktop (CustomTkinter)
├── backend/             # API REST (Flask) — serve o frontend web
│   ├── app.py
│   └── routes/          # Blueprints: modalidade, espaco, cliente, agendamento, pagamento, dashboard
├── frontend/            # Interface Web moderna (SPA vanilla)
│   ├── index.html
│   ├── css/style.css
│   └── js/              # api.js, app.js e views/*.js
├── main.py              # Ponto de entrada da aplicação Desktop
├── requirements.txt     # Dependências Python
├── .env.example         # Modelo para variáveis de ambiente
└── .gitignore
</pre>

<hr>

<h2>🚀 Como Executar o Projeto</h2>

<h3>1. Preparação do Ambiente</h3>
<p>Clone o repositório para a sua máquina local e acesse a pasta:</p>
<pre><code>git clone https://github.com/kaiosdev/Sistemas-de-reserva-de-horario-de-quadras
cd Athletix</code></pre>

<p>Crie e ative um ambiente virtual:</p>
<pre><code># No Windows:
python -m venv .venv
.venv\Scripts\activate

# No Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate</code></pre>

<p>Instale as bibliotecas exigidas:</p>
<pre><code>pip install -r requirements.txt</code></pre>
<p><i>Nota: se ocorrer erro de compilação no Windows ao instalar o <code>psycopg2</code>, o <code>requirements.txt</code> já usa <code>psycopg2-binary</code>.</i></p>

<h3>2. Configuração do Banco de Dados</h3>
<ul>
  <li>Abra o gerenciador do PostgreSQL (pgAdmin 4 ou DBeaver).</li>
  <li>Crie um novo banco de dados em branco chamado <code>athletix_db</code>.</li>
  <li>Abra a ferramenta de execução de SQL (Query Tool) no banco criado.</li>
  <li>Copie todo o conteúdo do arquivo <code>database/schema.sql</code>, cole na ferramenta e execute para gerar as tabelas e a Trigger de validação de choque de horário.</li>
</ul>

<h3>3. Configuração de Credenciais</h3>
<p>Crie um arquivo chamado <code>.env</code> na raiz do projeto e preencha com os dados do seu PostgreSQL local:</p>
<pre><code>DB_HOST=localhost
DB_NAME=athletix_db
DB_USER=postgres
DB_PASSWORD=sua_senha_do_pgadmin</code></pre>

<hr>

<h2>🖥️ Executando a Interface Web (Recomendada)</h2>
<p>A interface web moderna requer o backend Flask em execução.</p>

<p><strong>Passo 1:</strong> Inicie a API Flask:</p>
<pre><code>python backend/app.py</code></pre>
<p>Você verá a mensagem <code>ATHLETIX API rodando em http://127.0.0.1:5000</code>.</p>

<p><strong>Passo 2:</strong> Abra o arquivo <code>frontend/index.html</code> no navegador (duplo clique ou via servidor estático).</p>

<p>O frontend se comunicará automaticamente com a API em <code>http://127.0.0.1:5000/api</code>.</p>

<hr>

<h2>🖱️ Executando a Interface Desktop</h2>
<pre><code>python main.py</code></pre>
<p>Abre a aplicação CustomTkinter com tema dark moderno. Esta versão acessa os repositories diretamente (sem passar pela API Flask).</p>

<hr>

<h2>🔌 Endpoints da API REST</h2>
<table>
  <thead>
    <tr><th>Método</th><th>Endpoint</th><th>Descrição</th></tr>
  </thead>
  <tbody>
    <tr><td>GET</td><td><code>/api/dashboard/stats</code></td><td>Estatísticas agregadas (cards)</td></tr>
    <tr><td>GET</td><td><code>/api/modalidades</code></td><td>Lista modalidades esportivas</td></tr>
    <tr><td>GET / POST</td><td><code>/api/espacos</code></td><td>Lista / Cadastra quadras</td></tr>
    <tr><td>GET / POST</td><td><code>/api/clientes</code></td><td>Lista / Cadastra clientes</td></tr>
    <tr><td>GET / POST</td><td><code>/api/agendamentos</code></td><td>Lista / Cria reservas</td></tr>
    <tr><td>GET / POST</td><td><code>/api/pagamentos</code></td><td>Lista / Processa pagamentos</td></tr>
  </tbody>
</table>

<hr>

<h2>👥 Equipe de Desenvolvimento</h2>
<ul>
  <li><strong>Kaio Sobral Moreira</strong></li>
  <li><strong>Kevily Oliveira</strong></li>
  <li><strong>Ricky Brendon da Silva Almeida</strong></li>
  <li><strong>Jean Carlos dos Santos Baraúna</strong></li>
</ul>

<h2>👨‍🏫 Professores Orientadores</h2>
<ul>
  <li><strong>Prof. Edson de Araújo Silva</strong> (Sistemas de Banco de Dados I)</li>
  <li><strong>Prof. Alternei Brito</strong> (Programação Orientada a Objetos)</li>
</ul>
