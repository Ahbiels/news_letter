# Tech Newsletter
Esse projeto consiste em uma pipeline automatizada de entrega de notícias sobre technologia. Ele realiza web scraping de portais de notícias, utiliza Inteligência Artificial para ranquear a relevância do conteúdo com base em prompts específicos, resume os artigos mais importantes e, por fim, entrega uma newsletter personalizada diretamente no e-mail dos usuários.

![Status](https://img.shields.io/badge/status-Done-brightgreen)
![Atualização](https://img.shields.io/badge/Last%20update-mar%202026-red)
![Stack](https://img.shields.io/badge/stack-Golang-cyan)
![Stack](https://img.shields.io/badge/stack-Python-blue)
![Ambiente](https://img.shields.io/badge/Environment-Local-orange)
![Duração](https://img.shields.io/badge/Duration-7%20days-blueviolet)


## Summary
- [Arquitetura](#arquitetura)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
  - [Pontos importantes](#pontos-importantes)
- [Permissionamento](#permissionamento)
- [Bibliotecas e Dependências](#bibliotecas-e-dependências)
  - [Golang](#golang)
  - [Python (IA & Orquestração)](#python-ia--orquestração)
    - [Criação do ambiente virtual em python](#criação-do-ambiente-virtual-em-python)
- [Estrutura de Código](#estrutura-de-código)
  - [Concorrencia em Golang](#concorrencia-em-golang)
  - [Estrutura em Python](#estrutura-em-python)


## Arquitetura
A arquitetura do projeto tira proveito do melhor de duas linguagens: Golang é utilizado para garantir alta performance e velocidade na extração de dados (Web Scraping) através de concorrência, enquanto Python atua como o orquestrador principal e integra os modelos de Inteligência Artificial via LangChain e Google Gemini.
- **Web Scraping**: o módulo em Go inicia o scraping de dados em sites de tecnologia. Utilizando Goroutines e Channels, o processo ocorre de forma simultânea (concorrente), reduzindo drasticamente o tempo de execução e permitindo adcionar diversas fontes de informações sem afetar a performance do Scraping. O Golang é disponibilizado na porta 8081 com um único endpoint: `/run`. A resposta desse endpoint são os dados de notícias coletados no formato JSON.
- **Database**: o arquivo Dockerfile cria um banco de dados em Mysql contendo os nomes e e-mails dos usuários cadastrados na newsletter, cuja aplicação usará para enviar os e-mails.
- **Seleção e resumo de conteúdo com AI**: o módulo Python, ao receber os dados vindo do Golang, inicia o processo de:
  - Ranqueamento de filtragem: 
    - O Python instancia o primeiro modelo do Gemini via LangChain.
    - A IA avalia a lista de notícias e atribui um "Score" de relevância a cada uma (de 0 a 1), além de identificar possíveis notícias repetidas com base na similaridade entre os titulos.
    - O Gemini retorna o Score e um campo "no_repeated", que são adicionados aos dados originais
  - Resumo dos dados:
    - O Python instancia o segundo modelo do Gemini via LangChain, configurado com parâmetros diferentes para ser mais criativo na escrita
    - Apenas as notícias não repetidas e com um Score maior ou igual a 0.55 são passadas para o segundo modelo.
    - As notícias aprovadas são enviadas para esse novo modelo.
    - A IA lê os títulos/conteúdos e gera um resumo conciso de cada artigo.
  - Tratamento de Dados:
    - Em cada resposta retornada pelo Gemini nas duas fases anteriores, o Python utiliza expressões **regulares (Regex)** e a biblioteca **ast** para extrair essas respostas, formatando-as perfeitamente em uma lista Python, que posteriormente é usado para criar um objeto python com as notícias
  - Distribuição: 
    - O conteúdo final resumido é formatado e enviado para os e-mails dos usuários finais (cadastrado no banco de dados) utilizando a API do SendGrid. 

## Variáveis de Ambiente
Para o correto funcionamento da aplicação, crie um arquivo .env na raiz do projeto contendo as seguintes variáveis:

| env_name | description | example |
| --- | --- | --- |
| MODEL_NAME | É o nome do modelo utilizado no Langchain | gemini-2.0-flash |
| VIEWER_PASSWORD | É a senha do usuário do banco de dados que o Python utiliza para resgatar os e-mails | "Viewer@123" |
| SENDGRID_API_KEY | É a chave de API do Sender que é configurado dentro da plataforma SendGrid (**via SMTP**) | SG... |
| FROM_EMAIL | É o e-mail cadastrado como Sender dentro da plataforma SendGrid | user@gmail.com |

### Pontos importantes:
- É possível utilizar um e-mail pessoal sem configura o SendGrid, para isso, ao invés de usar "SENDGRID_API_KEY", usaria a senha do e-mail cadastrado. Porém, isso não funciona para e-mails que possuem MFA ou quaisquer outros métodos de segurança configurado.
- E-mails com o domínio **gmail** pode ser tratado como span na maioria dos casos. A própria documentação do SendGrid recomenda não utilizar esse domínio em produção.
- Caso gere alguem erro de permissão, configure o **Allow List** dentro do SendGrid

## Permissionamento
Como foi executado localmente, a aplicação exige um arquivo credentials.json na raiz, que contém as credenciais da Service Account do Google Cloud para autenticação do modelo Gemini. Caso seja utilizado diretamente na nuvem (dentro de um Cloud Run, ou VM), não é necesário o arquivo contendo as credenciais da Service Account, basta apenas especificar a Service Account no recurso que irá executar a aplicação.

As permissões utilizadas foram para a service account foram:
- AI Platform Developer
- Vertex AI User

## Bibliotecas e Dependências

### Golang
As dependências do Go são gerenciadas pelo go.mod.
- Padrão (Built-in): fmt, sync, time (Usadas para gerenciar as Goroutines, WaitGroups e medir o tempo de execução).
- Terceiros: * github.com/gocolly/colly: O framework principal utilizado para realizar o web scraping e navegar pelo DOM das páginas de notícias.

### Python (IA & Orquestração)
Recomenda-se o uso de um ambiente virtual (venv). As dependências podem ser instaladas via pip.
- Padrão (Built-in): os, re (Regex), ast (Para converter strings literais em dicionários/listas Python de forma segura), json.
- Terceiros (Requerem instalação):
  - langchain / langchain_core: Framework principal para orquestração de prompts e modelos de LLM.
  - langchain-google-vertexai / langchain-google-genai: Dependendo do pacote específico de integração usado pelo init_chat_model.
  - google-auth: Fornece o service_account para ler o credentials.json.
  - python-dotenv: Para carregar as variáveis de ambiente do arquivo .env.

#### Criação do ambiente virtual em python
Cria o ambiente virtual chamado `env`:
```sh
python3 -m venv env
```

Executa o ambiente virtual (em MacOS e Linux):
```sh
source env/bin/activate
```

## Estrutura de Código

### Concorrencia em Golang
A função Scrapping no módulo Go foi desenhada seguindo o padrão Producer-Consumer. O uso de canais (jobs e results) junto com sync.WaitGroup garante que as notícias sejam processadas de forma segura e paralela, sem bloquear a thread principal.
```go
// Trecho destacando o padrão de concorrência com Workers
for x := 1; x < 10; x++ {
    wgWorkers.Go(func() {
        worker(jobs, results)
    })
}
```

### Estrutura em Python
A classe Model centraliza a inteligência do projeto. Ela é instanciada duas vezes com diferentes "personalidades" (temperaturas):
- **Ranqueamento (define_ranking)**: usa temperatura baixa (0.2) para ser determinístico, avaliando matematicamente se a notícia serve ou não.
- **Resumo (summary_news)**: usa temperatura mais alta (0.9) para ter mais fluidez natural e criatividade ao redigir o resumo para o leitor.

```py
# Extração dos dados do texto retornado pela IA
score_match = re.search(r'OUTPUT_SCORE\s*=\s*(\[[^\]]+\])', response.content)
repeated_match = re.search(r'OUTPUT_REPEATED\s*=\s*(\[[^\]]+\])', response.content)

# Converter texto em formato de lista em lista
score_list = ast.literal_eval(score_match.group(1))
```
