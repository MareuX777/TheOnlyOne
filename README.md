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

| Comando                | Descrição                       |
| ---------------------- | ------------------------------- |
| `ping` / `/ping`       | Retorna latência do bot         |
| `ban` / `/ban`         | Bane um membro do servidor      |
| `unban`                | Remove o banimento de um membro |
| `clear`                | Apaga mensagens de um canal     |
| `timeout` / `/timeout` | Aplica timeout em um membro     |

> ⚠️ Comandos de moderação exigem permissões apropriadas.

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
│       │   └── logger.py        # Sistema de logging
│       └── commands/
│           ├── cmd.py           # Comandos prefixados
│           └── slash.py         # Slash commands
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos

* Python **3.10+**
* `discord.py`
* `python-dotenv`

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

Além disso, o projeto conta com:

* Sistema de logging estruturado
* Separação entre comandos prefixados e slash commands
* Tratamento global de erros

---

## 📈 Roadmap

* [x] Sistema de logs
* [x] Slash commands (`/`)
* [ ] Comandos de moderação avançados (mute, warn)
* [ ] Sistema de permissões customizado
* [ ] Histórico de punições

---

## 🤝 Contribuição

Contribuições são bem-vindas!

1. Fork do projeto
2. Crie uma branch (`feature/minha-feature`)
3. Commit (`git commit -m 'feat: nova feature'`)
4. Push
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo `LICENSE` para mais detalhes.

---

## 💡 Observação

Este projeto está em desenvolvimento ativo. Mudanças podem ocorrer com frequência.
