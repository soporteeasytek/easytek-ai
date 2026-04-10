# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Govee
API Key: guardado en 1Password → Personal → "Govee API" (item ID: y2hdbtl4g5ypzxwtyyqlx4ovia)
Base URL: https://developer-api.govee.com/v1

| Device | Model | Device ID |
|--------|-------|-----------|
| Kitchen | H6160 | 80:12:A4:C1:38:FB:0E:E5 |
| Outdoor lights | H6160 | B1:C1:A4:C1:38:70:37:A1 |
| Wall - Bed | H6109 | 05:C3:A4:C1:38:F8:7C:83 |
| Gym | H6109 | 4B:60:A4:C1:38:2B:E9:E6 |
| Floor Lamp Basic | H6076 | B5:71:D1:C7:C0:C6:60:1F |

## Tuya SmartLife (Central Europe)
Access ID: guardado en 1Password → Personal → "Tuya SmartLife API (EU)"
Access Secret: guardado en 1Password → Personal → "Tuya SmartLife API (EU)"
Base URL: https://openapi.tuyaeu.com
Status: pendiente vincular cuenta SmartLife con QR

## 1Password
- **Cuenta:** isaacmb@gmail.com (User ID: 6CCXSQ5VEBDD7IFSZHQQDETL4Q)
- **Vault por defecto:** Personal (qdv6kniznl7dbl3ng4z3juuaku)
- Siempre guardar credenciales aquí salvo que Isaac indique otro vault

## Sensibo
API Key: guardado en 1Password → Personal → "Sensibo API" (1Password item ID: gfx2lryaou7hqqc7dbupq33joy)
Para usar: `op item get gfx2lryaou7hqqc7dbupq33joy --fields credential --reveal --account 6CCXSQ5VEBDD7IFSZHQQDETL4Q`

| Room | Device ID |
|------|-----------|
| Office | kgDm9uPz |
| Kitchen | hCbp45qK |

## NetHome Plus / msmart-ng (OMEGA - Room)
- **IP:** 192.168.110.231
- **Port:** 6444
- **Device ID:** 151732606810840
- **Key:** 7833229f67a74f15864928243cd975a575cf2c5c596845db94a7351831a2d162
- **Token:** 30ccae402e287fd0e1f5998d83f0bf0e623ccd64fcb685855af5065805ae32892ed403d5ce4884682cdb2e5400962afb8ff1c671de798b573294908bab9c1b7b
- **CLI:** `/Users/isaacmora/Library/Python/3.9/bin/msmart-ng`

---

Add whatever helps you do your job. This is your cheat sheet.
