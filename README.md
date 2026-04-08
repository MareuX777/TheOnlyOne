# ⚡ TheOnlyOne

> Bot de moderação para Discord focado em simplicidade, controle e extensibilidade.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📌 Visão Geral

**TheOnlyOne** é um bot para Discord desenvolvido em Python com foco em comandos essenciais de moderação e utilidades básicas.

O projeto foi projetado para ser:

* Simples de usar
* Seguro em permissões
* Fácil de expandir (arquitetura modular com Cogs)

Ideal tanto para aprendizado quanto para uso real em servidores.

---

## 🚀 Funcionalidades

### 🛡️ Moderação

| Comando                  | Descrição                                                    |
| ------------------------ | ------------------------------------------------------------ |
| `ban` / `/ban`           | Bane um membro do servidor                                   |
| `unban`                  | Remove o banimento de um membro                              |
| `kick` / `/kick`         | Expulsa um membro do servidor                                |
| `clear` / `/clear`       | Apaga mensagens de um canal                                  |
| `timeout` / `/timeout`   | Aplica timeout em um membro                                  |
| `warn` / `/warn`         | Dá aviso a um membro                                         |
| `warnings` / `/warnings` | Mostra avisos de um membro (com histórico quando disponível) |
| `mute` / `/mute`         | Silencia um membro                                           |
| `unmute` / `/unmute`     | Dessilencia um membro                                        |

### 🎭 Sistemas Automáticos

| Comando                        | Descrição                            |
| ------------------------------ | ------------------------------------ |
| `reaction_role_setup`          | Cria painel de reaction roles        |
| `reaction_role_add`            | Adiciona emoji e role ao painel      |
| `ticket_panel`                 | Cria painel para abertura de tickets |
| `ticket_add` / `ticket_remove` | Gerencia acesso ao ticket            |
| `ticket_close`                 | Fecha ticket                         |

### 📊 Utilitários

| Comando                      | Descrição               |
| ---------------------------- | ----------------------- |
| `ping` / `/ping`             | Retorna latência do bot |
| `userinfo` / `/userinfo`     | Info de um usuário      |
| `serverinfo` / `/serverinfo` | Info do servidor        |
| `help` / `/help`             | Lista de comandos       |

> Comandos de moderação exigem permissões apropriadas.

---

## 🎮 Tipos de Comandos

O bot suporta dois tipos de comandos:

* **Prefixados**: `!ban`, `$clear`
* **Slash Commands**: `/ban`, `/timeout`

Os slash commands oferecem melhor experiência com:

* Autocomplete
* Validação automática
* Interface nativa do Discord

---

## 🧱 Estrutura do Projeto

```
TheOnlyOne/
│
├── src/
│   └── theonlyone/
│       ├── app.py
│       ├── utils/
│       │   ├── logger.py          # Sistema de logging
│       │   └── database.py        # Camada de banco (MySQL opcional)
│       └── commands/
│           ├── commands.py        # Comandos prefixados
│           ├── slash_commands.py  # Slash commands
│           ├── reaction_roles.py  # Sistema de reaction roles
│           └── tickets.py         # Sistema de tickets
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos

* Python **3.10+**
* `discord.py`
* `python-dotenv`
* `mysql-connector-python` (opcional)

---

## 📦 Instalação

```bash
git clone <URL-do-repositório>
cd TheOnlyOne
pip install -r requirements.txt
```

---

## 🔐 Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
TOKEN=seu_token_aqui

# Opcional (MySQL)
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=senha
DB_NAME=theonlyone
```

---

## ▶️ Execução

```bash
python src/theonlyone/app.py
```

---

## 🛡️ Permissões Necessárias

O bot precisa das seguintes permissões no servidor:

* Banir membros
* Desbanir membros
* Gerenciar mensagens
* Moderar membros (timeout)

---

## 🧩 Arquitetura

O projeto utiliza o sistema de **Cogs do discord.py**, permitindo:

* Separação de responsabilidades
* Fácil adição de novos comandos
* Melhor manutenção do código

Além disso:

* Sistema de logging estruturado
* Separação entre comandos prefixados e slash commands
* Tratamento global de erros
* Camada de banco desacoplada

---

## 💾 Banco de Dados

O bot utiliza **MySQL** para persistência de dados.

### Importante

* O banco é **opcional**
* O bot funciona normalmente **sem banco**
* Quando indisponível, os sistemas utilizam fallback em memória (sem persistência)
* Falhas de conexão não derrubam o bot

### Tabelas

* **warns**
* **guild_config**
* **reaction_roles**
* **tickets**
* **users**

### Uso

```python
from theonlyone.utils.database import db

db.add_warn(guild_id=123, user_id=456, moderator_id=789, reason="Spam")
warns = db.get_warns(guild_id=123, user_id=456)

db.add_xp(guild_id=123, user_id=456, xp=10)
leaderboard = db.get_leaderboard(guild_id=123)
```

---

## 📈 Roadmap

* [x] Sistema de logs
* [x] Slash commands
* [x] Estrutura de banco (MySQL)
* [ ] Integração completa com banco
* [ ] Sistema de permissões customizado
* [ ] Histórico avançado de punições

---

## 🤝 Contribuição

1. Fork do projeto
2. Crie uma branch (`feature/minha-feature`)
3. Commit (`git commit -m 'feat: nova feature'`)
4. Push
5. Abra um Pull Request

---

## 📄 Licença

Licença MIT.

---

## 💡 Observação

Projeto em desenvolvimento ativo.
