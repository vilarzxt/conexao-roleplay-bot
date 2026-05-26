# 📊 FLUXO COMPLETO DO SISTEMA DE TICKETS — V1.3.2

## 🧠 Arquitetura geral

UI → Router → Permissions → Ticket Manager → Auto Close → Transcript → Logs → Rating

---

# 🎫 1. ABERTURA DO TICKET

Arquivos:
- systems/views.py
- systems/dropdowns.py

Fluxo:
Usuário abre painel → seleciona categoria → dropdown envia seleção

---

# 🧭 2. ROUTER

Arquivo:
- systems/router.py

Fluxo:
Categoria → define tipo de ticket → define setor → define permissões

---

# 🔐 3. PERMISSÕES

Arquivo:
- systems/permissions.py

Regras:
- Abrir: todos
- Responder: equipe compatível
- Fechar: staff autorizado
- Financeiro: Coordenador Geral+
- Denúncia staff: Coordenador+

---

# 🎫 4. TICKET MANAGER

Arquivo:
- systems/ticket_manager.py

Fluxo:
router aprova → canal criado → permissões aplicadas → auto-close inicia

---

# ⏰ 5. AUTO CLOSE

Arquivos:
- systems/auto_close.py
- systems/events/ticket_events.py

Fluxo:
ticket ativo → timer inicia → atividade reseta timer

Timeout:
- 50% aviso 1
- 75% aviso 2
- 100% fechamento

---

# 📩 6. ATIVIDADE EM TEMPO REAL

Arquivo:
- systems/events/ticket_events.py

Fluxo:
mensagem detectada → reset timer

---

# 🔒 7. FECHAMENTO MANUAL

Arquivo:
- systems/ticket_manager.py

Fluxo:
staff fecha → valida permissão → envia DM → fecha canal

---

# 📜 8. TRANSCRIPT

Arquivo:
- systems/transcripts.py

Fluxo:
mensagens coletadas → TXT + HTML → enviado para logs + usuário

---

# ⭐ 9. AVALIAÇÃO

Fluxo:
ticket fechado → nota 1–5 estrelas → comentário opcional → log

---

# 📊 10. LOG FINAL

Canal:
logs-tickets

Conteúdo:
fechamento + motivo + nota + feedback + timestamp

---

# 🧠 FLUXO FINAL

Usuário → UI → Router → Permissions → Manager → AutoClose → Events → Close → Transcript → Rating → Logs
