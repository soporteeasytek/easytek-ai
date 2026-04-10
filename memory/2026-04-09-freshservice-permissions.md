# Freshservice permissions plan

- Isaac wants owner/admin control for OpenClaw.
- Isaac approved limited access for coworkers: they can use existing skills, ask questions, and run allowed workflows, but cannot modify skills/config or use elevated actions.
- Admin identities currently approved:
  - Telegram `1263132569`
  - WhatsApp `+50683288460`
- Freshservice credential isolation plan:
  - Isaac API key is now identified as `FRESHSERVICE_API_KEY_ISAAC`.
  - Isaac agent id mapped as `FRESHSERVICE_AGENT_ID_ISAAC=7000999054`.
  - Future placeholders created for Steven and Jacob.
  - Goal: each sender identity maps to only their own Freshservice API key and agent id.
  - Pending only: enroll coworkers' Telegram/WhatsApp ids and add their Freshservice keys.
- Paperclip and Freshservice multi-user mapping should be enforced by identity mapping, not by asking for API keys in chat.
