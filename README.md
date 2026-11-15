# MINDSPACE | StarMasters - JIM

### NASA Space Apps Challenge 2026

**Equipe:** StarMasters - JIM

**Integrantes:**
- Ana Beatriz
- Alice
- João
- Amanda

---

## 1. Sobre o projeto

O **MINDSPACE** é uma aplicação web desenvolvida pela equipe **StarMasters - JIM** durante o NASA Space Apps Challenge 2026.

O projeto tem como proposta desenvolver uma plataforma de monitoramento e visualização de informações relacionadas à saúde de astronautas em missões espaciais.

A aplicação utiliza dados científicos de pesquisas espaciais para organizar resultados laboratoriais, permitindo visualizar informações por participante, estudo e período de coleta.

A interface foi concebida com uma identidade visual inspirada em sistemas de monitoramento utilizados em missões espaciais, incluindo um painel de controle e uma interface HUD (*Heads-Up Display*).

## 2. O desafio do Hackathon

**Create Health Monitoring Software for Astronauts on Space Missions**

O desafio proposto pela NASA aborda a necessidade de desenvolver softwares capazes de auxiliar no monitoramento da saúde de astronautas durante missões espaciais.

Missões de longa duração expõem os astronautas a condições extremas, como:

- Radiação espacial;
- Isolamento e confinamento;
- Alterações na gravidade;
- Ambientes fechados e hostis;
- Alterações no sistema imunológico;
- Perda de massa óssea;
- Riscos cardiovasculares;
- Problemas relacionados à saúde comportamental e mental.

Em missões prolongadas, os astronautas também precisam participar ativamente da identificação de possíveis alterações em sua própria saúde.

Diante desse cenário, o desafio consiste em desenvolver um software que reúna indicadores de saúde e permita que os astronautas acompanhem suas condições, identifiquem possíveis alterações e tenham informações que auxiliem na tomada de decisões.

### Nossa proposta

O MINDSPACE busca contribuir com esse desafio por meio de uma plataforma centralizada de visualização de dados de saúde.

A proposta contempla:

- Organização de informações por participante científico;
- Visualização de resultados de exames laboratoriais;
- Separação dos dados por estudos científicos;
- Consulta aos diferentes períodos de coleta;
- Apresentação de indicadores em uma interface de monitoramento;
- Interface visual inspirada em sistemas de controle de missões espaciais.

O objetivo é transformar conjuntos de dados científicos em informações organizadas e de fácil consulta.

## 3. Funcionalidades desenvolvidas

### 3.1. Cadastro e identificação dos participantes

A aplicação possui uma área de visualização dos participantes da missão Inspiration4.

Os participantes científicos são identificados pelos códigos:

- C001
- C002
- C003
- C004

A aplicação também possui informações cadastrais dos astronautas, incluindo nome, agência, nacionalidade, ocupação, biografia e fotografia.

**Importante:** os códigos dos participantes científicos não devem ser associados aos nomes dos astronautas sem documentação que comprove essa correspondência.

### 3.2. Dashboard de saúde

O dashboard apresenta informações laboratoriais organizadas por participante.

Entre os indicadores disponíveis estão:

- Quantidade de registros laboratoriais;
- Quantidade de exames CBC;
- Quantidade de exames CMP;
- Quantidade de parâmetros analisados;
- Quantidade de períodos de coleta;
- Resultados fora dos intervalos de referência informados pelo laboratório.

A plataforma também permite consultar os resultados de acordo com os estudos científicos disponíveis.

### 3.3. Mission HUD

A interface HUD (*Heads-Up Display*) apresenta uma experiência visual inspirada nos sistemas de monitoramento de missões espaciais.

Entre os elementos implementados estão:

- Identificação da missão Inspiration4;
- Identificação do participante científico;
- Relógio da interface;
- Indicadores de conexão com o banco de dados;
- Painel de monitoramento;
- Indicadores visuais de fadiga mental;
- Linha do tempo dos períodos de coleta;
- Painéis de visualização dos estudos laboratoriais.

### 3.4. Indicador de fadiga mental

A interface apresenta um indicador visual semafórico com três estados:

| Estado | Identificação | Descrição |
|---|---|---|
| Verde | COOL | LOW FATIGUE |
| Amarelo | ALERT | MODERATE FATIGUE |
| Vermelho | STRESSED | HIGH FATIGUE |

O estado é selecionado aleatoriamente para demonstrar o funcionamento visual do componente.

**Esse indicador é ilustrativo e não representa uma avaliação clínica ou uma medição científica real da fadiga dos astronautas.**

## 4. Dados científicos utilizados

O projeto utiliza dados públicos relacionados à missão **Inspiration4**, disponibilizados pelo NASA Open Science Data Repository (OSDR).

Foram trabalhados dois conjuntos de dados laboratoriais:

### OSD-569 — Complete Blood Count (CBC)

Estudo relacionado ao hemograma completo.

O conjunto contempla parâmetros hematológicos, permitindo consultar resultados como hemoglobina, leucócitos, plaquetas e hematócrito, entre outros.

- Registros importados: 553
- Parâmetros: 23
- Participantes científicos: 4
- Períodos de coleta: 7

### OSD-575 — Comprehensive Metabolic Panel (CMP)

Estudo relacionado ao painel metabólico completo.

O conjunto contempla parâmetros bioquímicos utilizados na avaliação de diferentes aspectos metabólicos e da função orgânica.

- Registros importados: 509
- Parâmetros: 19
- Participantes científicos: 4
- Períodos de coleta: 7

### Períodos de coleta

Os dados estão organizados de acordo com os seguintes períodos relativos à missão:

- L-92
- L-44
- L-3
- R+1
- R+45
- R+82
- R+194

Essas identificações representam os períodos de coleta em relação à missão, e não uma transmissão contínua de sinais vitais.

### Resumo da base de dados

| Informação | Quantidade |
|---|---:|
| Estudos científicos | 2 |
| Participantes científicos | 4 |
| Registros CBC | 553 |
| Registros CMP | 509 |
| Total de registros | 1.062 |
| Parâmetros distintos | 42 |

Os intervalos de referência apresentados nos exames correspondem aos valores informados nos dados laboratoriais e não representam, isoladamente, um diagnóstico médico.

## 5. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal do projeto |
| Django 5.0 | Framework para desenvolvimento web |
| SQLite | Banco de dados |
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização das interfaces |
| Bootstrap | Componentes e recursos visuais |
| JavaScript | Interatividade da interface |
| NASA OSDR | Fonte dos dados científicos |

## 6. Como executar o projeto

### 6.1. Pré-requisitos

Antes de iniciar, é necessário possuir:

- Python instalado (o projeto foi desenvolvido com Python 3.13.3);
- Git, caso queira clonar o repositório;
- Editor de código, preferencialmente Visual Studio Code ou PyCharm;
- Terminal PowerShell ou equivalente.

### 6.2. Clonar o repositório

Abra o terminal e execute:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd NOME_DO_REPOSITORIO
```

### 6.3. Acessar a pasta Django

O projeto Django está organizado dentro da pasta `saudenoespaco`.

```bash
cd saudenoespaco
```

É nessa pasta que se encontra o arquivo `manage.py`.

### 6.4. Criar o ambiente virtual

No terminal, execute:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso esteja utilizando o Prompt de Comando:

```cmd
.venv\Scripts\activate
```

### 6.5. Instalar as dependências

Caso o repositório possua um arquivo `requirements.txt`, execute:

```bash
pip install -r requirements.txt
```

Caso ainda não exista esse arquivo, instale a versão do Django utilizada no desenvolvimento:

```bash
pip install Django==5.0.14
```

### 6.6. Configurar o banco de dados

O projeto utiliza SQLite.

Após instalar as dependências, execute as migrações:

```bash
python manage.py makemigrations
```

Em seguida:

```bash
python manage.py migrate
```

Esses comandos criam e atualizam a estrutura do banco de dados de acordo com os models da aplicação.

### 6.7. Criar um usuário administrador

Para acessar o painel administrativo do Django, execute:

```bash
python manage.py createsuperuser
```

Informe o nome de usuário, e-mail e senha solicitados pelo terminal.

### 6.8. Executar o servidor

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Após a inicialização, acesse:

**Aplicação:**

http://127.0.0.1:8000/

**Painel administrativo:**

http://127.0.0.1:8000/admin/

O servidor poderá ser encerrado pressionando `CTRL + C` no terminal.

## 7. Estrutura do projeto

O projeto está organizado em aplicações Django, separando as responsabilidades de cada módulo.

```text
saudenoespaco/
│
├── accounts/
│
├── analytics/
│
├── astronaut/
│
├── core/
│
├── interventions/
│
├── medical/
│
├── monitoring/
│
├── physiology/
│
├── data/
│   └── raw/
│       └── inspiration4/
│           ├── OSD-569/
│           └── OSD-575/
│
├── static/
│   ├── css/
│   ├── img/
│   └── js/
│
├── templates/
│
├── manage.py
│
└── db.sqlite3
```

A estrutura representa a organização geral da aplicação. Arquivos adicionais, como configurações, templates específicos e comandos de importação, podem estar distribuídos dentro das respectivas aplicações.

## 8. Fontes e referências

### NASA Space Apps Challenge

Página oficial do evento:

https://www.spaceappschallenge.org/

Página do desafio:

https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/

### Recursos da NASA

**Five Hazards of Human Spaceflight**

https://www.nasa.gov/hrp/hazards/

Informações sobre os principais perigos relacionados à saúde humana durante missões espaciais.

**Human Spaceflight Risks**

https://www.nasa.gov/hrp/risks/

Informações sobre os riscos enfrentados por astronautas durante missões espaciais.

**Ongoing Human Research Program Research**

https://www.nasa.gov/hrp/ongoing-hrp-research/

Pesquisas em andamento relacionadas à saúde humana no espaço.

### Recursos da Agência Espacial Canadense (CSA)

**Monitoring radiation for astronaut health**

https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp

Informações sobre o monitoramento da exposição à radiação espacial e seus efeitos sobre a saúde dos astronautas.

**Why do we conduct science experiments in space?**

https://www.asc-csa.gc.ca/eng/iss/science/why-do-we-conduct-science-experiments-in-space.asp

Explicações sobre a importância dos experimentos científicos realizados no ambiente espacial.

### NASA Open Science Data Repository (OSDR)

https://osdr.nasa.gov/

Repositório utilizado como fonte dos conjuntos de dados científicos trabalhados no projeto.

## 9. Equipe

**StarMasters - JIM**

Projeto desenvolvido durante o NASA Space Apps Challenge 2026.

Integrantes:

- Ana Beatriz
- Alice
- João
- Amanda

---

**MINDSPACE — Space Health Intelligence**

*Transformando dados científicos em informações para apoiar o monitoramento da saúde humana no espaço.*