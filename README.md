# Vamos-Jogar-Minecraft-Bot
Bot feito para ErikrafT

## 🧠 Funcionalidades Principais

### 🔧 Moderação Avançada
- Comandos via `/modpainel` com botões interativos: `Banir`, `Expulsar`, `Mutar`
- Sistema de mute real (castigo nativo do Discord)
- Logs completos com embeds detalhados
- Mensagens diretas para o usuário punido, com link de apelação personalizado

### 🛠️ Painel Interativo
- Embed com informações do usuário:
  - Menção, apelido, ID, data de criação, entrada no servidor
- Interface com botões para ações rápidas de moderação
- Tudo efêmero (só visível para quem executa)

### ✏️ Criador de Embeds
- Comando `/embed` abre um painel onde o usuário pode:
  - Definir título, descrição, cor, imagem, thumbnail
  - Visualizar o embed em tempo real antes de enviar

### 🚀 Incentivo a Boost
- Sistema automático que envia mensagens criativas incentivando o boost a cada X mensagens
- Variações armazenadas em vetor (`booster = []`)
- Canal de boost mencionado diretamente

## 📁 Estrutura do Projeto

```bash
bot/
├── cogs/
│   ├── mod.py                     # Comandos de moderação (painel, punições)
│   ├── embed_creator.py           # Criador de embeds interativos
│   ├── main.py (booster = [)    # Mensagens automáticas de incentivo ao boost
│   └── ...                        # Outros Cogs futuros
├── config.py                      # Variáveis de configuração (token, IDs, link de apelação)
├── main.py                        # Arquivo principal de inicialização do bot
├── requirements.txt               # Dependências do projeto
└── README.md                      # Você está aqui
```

## 🧩 Requisitos

* Python 3.10+
* [discord.py 2.3+](https://pypi.org/project/discord.py/)
* Permissões de administrador para testes

Instale com:

```bash
pip install -r requirements.txt
```

## 🧠 Como Usar

1. Clone o repositório e crie seu ambiente virtual
2. Preencha `config.py`
3. Rode o bot:

   ```bash
   python main.py
   ```

## 📌 Observações

* O sistema de mute usa `timeout` real do Discord, não apenas cargos
* A maioria das respostas são efêmeras para manter a interface limpa




---


### 📄 Variáveis de Configuração

```python
id_do_servidor = 1121464803941171270
```

ID do servidor principal onde o bot irá operar.

```python
CANAL_PAINEL_ID = 1309586413422907452  
```

ID do canal onde o painel de criação de tickets será exibido.

```python
id_cargo_atendente = 1138938495428214824  
```

ID do cargo dos atendentes responsáveis por gerenciar os tickets.

```python
TOKEN = "##"
```

Token de autenticação do bot (⚠️ **nunca compartilhe publicamente**).

```python
ID_CANAL_LOGS = 1161375392582619206 
```

ID do canal onde serão enviados os logs de punições (banimentos, silenciamentos, etc).

```python
ID_CANAL_MOD = 1398446601072283758
```

ID do canal interno da moderação, usado para comunicação e registro de decisões.

```python
link_apelacao = "https://form.jotform.com/242088340178054"
```

Link para o formulário de apelação, onde usuários punidos podem contestar a decisão.
