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

| Comando | Descrição                        |
| ------- | -------------------------------- |
| `ping`  | Retorna `Pong` + latência do bot |
| `ban`   | Bane um membro do servidor       |
| `unban` | Remove o banimento de um membro  |
| `clear` | Apaga mensagens de um canal      |

> ⚠️ Comandos de moderação exigem permissões apropriadas.

---

## 🧱 Estrutura do Projeto

```
TheOnlyOne/
│
├── src/
│   └── theonlyone/
│       ├── app.py                # Inicialização do bot
│       └── commands/
│           └── commands.py       # Comandos de moderação
│
├── requeriments.txt
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
pip install -r requeriments.txt
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

---

## 🧩 Arquitetura

O projeto utiliza o sistema de **Cogs do discord.py**, permitindo:

* Separação de responsabilidades
* Fácil adição de novos comandos
* Melhor manutenção do código

---

## 📈 Roadmap

* [ ] Sistema de logs
* [ ] Comandos de moderação avançados (mute, warn)
* [ ] Sistema de permissões customizado
* [ ] Slash commands (`/`)

---

## 🤝 Contribuição

Contribuições são bem-vindas.

1. Fork do projeto
2. Crie uma branch (`feature/minha-feature`)
3. Commit (`git commit -m 'feat: nova feature'`)
4. Push
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

## 💡 Observação

Este projeto está em desenvolvimento ativo. Mudanças podem ocorrer com frequência.

---
