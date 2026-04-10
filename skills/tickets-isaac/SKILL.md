---
name: tickets-isaac
description: "Alias corto para mostrar los tickets asignados al agente Isaac en Freshservice"
user-invocable: true
---

# tickets-isaac

Este skill es solo un alias corto.

Cuando se invoque `/tickets-isaac`, actúa exactamente como si el usuario hubiera pedido:

- mostrar los tickets del agente Isaac en Freshservice
- agente objetivo: `isaac@easytek.cr`
- usar la lógica y scripts del skill `freshservice`

## Instrucciones

1. Ejecuta:

```bash
python3 /Users/isaacmora/.openclaw/workspace/skills/freshservice/scripts/freshservice.py list-tickets-for-agent --agent-name Isaac --per-page 100
```

2. Resume los tickets en español, breve y claro.
3. Incluye por ticket:
   - ID
   - asunto
   - estado
   - prioridad
   - última actualización
4. No dupliques lógica fuera de Freshservice. Este skill existe solo como alias de entrada.
