<div align="center">
  <h1>ATHLETIX</h1>
  <h3>Sistema de Gestão de Espaços Esportivos</h3>
  <p><i>Projeto Final da Disciplina de Programação Orientada a Objetos (POO)</i></p>
  <p><b>ICET - Universidade Federal do Amazonas (UFAM)</b></p>
</div>

<hr>

<h2>Sobre o Projeto</h2>
<p>O <strong>Athletix</strong> foi desenvolvido para solucionar problemas comuns na administração de complexos esportivos. Este projeto foi estruturado com forte ênfase no paradigma de <strong>Programação Orientada a Objetos</strong>, aplicando na prática os conceitos de <strong>Abstração, Encapsulamento, Herança e Polimorfismo.</strong> A arquitetura é dividida em camadas (Models, Repositories, Services e UI), garantindo separação de responsabilidades, alta coesão, reaproveitamento de código e baixo acoplamento.</p>

<h2>Tecnologias Utilizadas</h2>
<ul>
  <li><strong>Linguagem:</strong> Python 3</li>
  <li><strong>Interface Gráfica:</strong> Tkinter (com biblioteca Ttk para estilização moderna)</li>
  <li><strong>Persistência:</strong> PostgreSQL (Acesso via camadas encapsuladas)</li>
  <li><strong>Dependências Externas:</strong> <code>psycopg2</code>, <code>python-dotenv</code>, <code>tkcalendar</code></li>
</ul>

<h2>Arquitetura Orientada a Objetos</h2>
<pre>
Athletix/
├── models/           # Classes de domínio (Herança, Polimorfismo e Construtores)
├── services/         # Regras de negócio, orquestração e validação de objetos
├── repositories/     # Camada de persistência (Data Access Objects isolados)
├── ui/               # Interface gráfica instanciando e consumindo os serviços
├── database/         # Conexão abstraída e scripts do SGBD
├── main.py           # Ponto de entrada (App instantiation)
└── .env.example      # Modelo para variáveis de ambiente
</pre>

<hr>

<h2>Como Executar o Projeto</h2>

<h3>1. Preparação do Ambiente</h3>
<p>Clone o repositório para a sua máquina local e acesse a pasta do projeto:</p>
<pre><code>git clone https://github.com/kaiosdev/Sistemas-de-reserva-de-horario-de-quadras.git
cd Sistemas-de-reserva-de-horario-de-quadras</code></pre>

<p>Crie e ative um ambiente virtual para isolar as dependências:</p>
<pre><code># No Windows:
python -m venv .venv
.venv\Scripts\activate

# No Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate</code></pre>

<p>Instale as bibliotecas exigidas para o funcionamento da interface e do banco de dados:</p>
<pre><code>pip install psycopg2 python-dotenv tkcalendar</code></pre>
<p><i>Nota: Se ocorrer erro de compilação no Windows ao instalar a biblioteca do banco, utilize o comando auxiliar <code>pip install psycopg2-binary</code>.</i></p>

<h3>2. Configuração do Banco de Dados</h3>
<p><i>(Necessário para a persistência correta dos objetos do sistema)</i></p>
<ul>
  <li>Abra o gerenciador do PostgreSQL (pgAdmin 4 ou DBeaver).</li>
  <li>Crie um novo banco de dados em branco chamado <code>athletix_db</code>.</li>
  <li>Abra a ferramenta de execução de SQL (Query Tool) conectada ao banco recém-criado.</li>
  <li>Copie todo o conteúdo do arquivo <code>database/schema.sql</code>, cole na ferramenta e execute para gerar a estrutura relacional necessária.</li>
</ul>

<h3>3. Configuração de Credenciais</h3>
<p>Crie um arquivo chamado <code>.env</code> na raiz do projeto (mesmo nível do <code>main.py</code>) e preencha com as suas credenciais locais:</p>
<pre><code>DB_HOST=localhost
DB_NAME=athletix_db
DB_USER=postgres
DB_PASSWORD=sua_senha_do_pgadmin</code></pre>

<h3>4. Inicialização do Sistema</h3>
<p>Com as bibliotecas instaladas e o ambiente ativado, inicie a interface gráfica executando:</p>
<pre><code>python main.py</code></pre>

<hr>

<h2>Equipe de Desenvolvimento</h2>
<ul>
  <li><strong>Kaio Sobral Moreira</strong></li>
  <li><strong>Kevily Da SilvaOliveira</strong></li>
  <li><strong>Ricky Brendon da Silva Almeida</strong></li>
  <li><strong>Jean Carlos dos Santos Baraúna</strong></li>
</ul>

<h2>Professor</h2>
<ul>
  <li><strong>Prof. Alternei Brito</strong> (Disciplina de Programação Orientada a Objetos)</li>
</ul>
