<div align="center">
  <h1>ATHLETIX</h1>
  <h3>Sistema de Gestão de Espaços Esportivos</h3>
  <p><i>Projeto Interdisciplinar: Sistemas de Banco de Dados I & Programação Orientada a Objetos</i></p>
  <p><b>ICET - Universidade Federal do Amazonas (UFAM)</b></p>
</div>

<hr>

<h2>Sobre o Projeto</h2>
<p>O <strong>Athletix</strong> foi desenvolvido para solucionar problemas comuns na administração de complexos esportivos, como o choque de horários (double-booking) e a falta de controle financeiro. O sistema utiliza uma arquitetura robusta orientada a objetos em Python integrada a um banco de dados relacional PostgreSQL, garantindo integridade de dados e aplicação de regras de negócio consistentes.</p>

<h2>Tecnologias Utilizadas</h2>
<ul>
  <li><strong>Linguagem:</strong> Python 3</li>
  <li><strong>Interface Gráfica:</strong> Tkinter (Nativa do Python)</li>
  <li><strong>Banco de Dados:</strong> PostgreSQL</li>
  <li><strong>Dependências:</strong> <code>psycopg2</code>, <code>python-dotenv</code></li>
</ul>

<h2>Arquitetura do Sistema</h2>
<pre>
Athletix/
├── database/         # Scripts SQL (Tabelas e Trigger) e conexão (PostgreSQL)
├── models/           # Classes de domínio (Abstração, Encapsulamento, Herança e Polimorfismo)
├── repositories/     # Persistência de dados e CRUD
├── services/         # Regras de negócio e validações via interface
├── ui/               # Componentes da interface gráfica
├── main.py           # Ponto de entrada da aplicação
├── .env.example      # Modelo para variáveis de ambiente
└── .gitignore        # Arquivos ignorados pelo repositório
</pre>

<hr>

<h2>Como Executar o Projeto</h2>

<h3>1. Preparação do Ambiente</h3>
<p>Clone o repositório para a sua máquina local e acesse a pasta:</p>
<pre><code>git clone [https://github.com/kaiosdev/Sistemas-de-reserva-de-horario-de-quadras]
cd Athletix</code></pre>

<p>Crie e ative um ambiente virtual:</p>
<pre><code># No Windows:
python -m venv .venv
.venv\Scripts\activate

# No Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate</code></pre>

<p>Instale as bibliotecas exigidas:</p>
<pre><code>pip install psycopg2 python-dotenv</code></pre>
<p><i>Nota: Se ocorrer erro de compilação no Windows ao instalar a biblioteca do banco, utilize o comando <code>pip install psycopg2-binary</code>.</i></p>

<h3>2. Configuração do Banco de Dados</h3>
<ul>
  <li>Abra o gerenciador do PostgreSQL (pgAdmin 4 ou DBeaver).</li>
  <li>Crie um novo banco de dados em branco chamado <code>athletix_db</code>.</li>
  <li>Abra a ferramenta de execução de SQL (Query Tool) no banco criado.</li>
  <li>Copie todo o conteúdo do arquivo <code>database/schema.sql</code>, cole na ferramenta e execute para gerar as tabelas e a Trigger de validação.</li>
</ul>

<h3>3. Configuração de Credenciais</h3>
<p>Crie um arquivo chamado <code>.env</code> na raiz do projeto e preencha com a senha que você configurou no seu PostgreSQL local:</p>
<pre><code>DB_HOST=localhost
DB_NAME=athletix_db
DB_USER=postgres
DB_PASSWORD=sua_senha_do_pgadmin</code></pre>

<h3>4. Inicialização</h3>
<p>Com tudo configurado, inicie a interface gráfica do sistema executando o comando:</p>
<pre><code>python main.py</code></pre>

<hr>

<h2>Equipe de Desenvolvimento</h2>
<ul>
  <li><strong>Kaio Sobral Moreira</strong></li>
  <li><strong>Kevily Oliveira</strong></li>
  <li><strong>Ricky Brendon da Silva Almeida</strong></li>
  <li><strong>Jean Carlos dos Santos Baraúna</strong></li>
</ul>

<h2>Professores Orientadores</h2>
<ul>
  <li><strong>Prof. Edson de Araújo Silva</strong> (Sistemas de Banco de Dados I)</li>
  <li><strong>Prof. Alternei Brito</strong> (Engenharia de Software e Sistemas de Informação)</li>
</ul>
