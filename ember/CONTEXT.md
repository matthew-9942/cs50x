# Ember — Project Context

## What is Ember?
A "Tinder for studying" app. Students swipe on each other based on shared subjects, location, and study style. Mutual like = match = can meet in person to study together.

Built as a CS50 Final Project targeting an English-speaking audience.

---

## Tech Stack
- **Frontend + Backend**: SvelteKit + TypeScript
- **Database**: SQLite via `better-sqlite3` (no ORM)
- **Editor**: Zed
- **Deploy**: Vercel (planned)

---

## Design System

### Fonts
- **Display**: Cormorant Garamond (headings, logo, hero text)
- **UI**: Baloo 2 (everything else — buttons, labels, body, chips)

### Color Palette (CSS Variables)
```css
:root {
  --bg:          #0C0B09;
  --bg2:         #131210;
  --surface:     #1C1A16;
  --surface2:    #242119;
  --border:      #2F2C26;
  --border2:     #3D3930;
  --text:        #F2EDE4;
  --text2:       #B8B0A4;
  --muted:       #6B6660;
  --ember:       #E07A2F;
  --ember-dim:   #9E5520;
  --ember-glow:  rgba(224, 122, 47, 0.15);
  --skip:        #C4503E;
  --skip-glow:   rgba(196, 80, 62, 0.15);
  --match:       #5A8C6E;
  --match-glow:  rgba(90, 140, 110, 0.15);
  --gold:        #D4A853;

  --font-display: 'Cormorant Garamond', serif;
  --font-body:    'Baloo 2', sans-serif;

  --radius-sm: 6px;
  --radius:    12px;
  --radius-lg: 20px;
  --radius-xl: 28px;
}
```

### Aesthetic
Dark academic. Warm near-black background, amber accent, cream text. Grain overlay on body. Background glow effects with radial gradients.

---

## Project Structure
```
ember/
├── src/
│   ├── app.css
│   ├── lib/
│   │   ├── db.ts                      ← better-sqlite3 connection (TODO)
│   │   └── schema.sql                 ← DB schema (TODO)
│   └── routes/
│       ├── +layout.svelte
│       ├── +page.svelte               ← landing
│       ├── register/+page.svelte
│       ├── login/+page.svelte
│       ├── onboarding/+page.svelte    ← 4-step onboarding
│       └── app/
│           ├── +page.svelte           ← swipe / discover
│           ├── matches/+page.svelte   ← TODO
│           └── profile/+page.svelte
├── database.db                        ← gitignored
└── package.json
```

---

## Database Schema

```sql
users
  id, email, password_hash, name, avatar, created_at

user_profiles
  user_id, bio, city, level, study_style
  subjects  -- JSON array as TEXT

swipes
  swiper_id, swiped_id, direction ('like'|'skip'), created_at

matches
  user_a_id, user_b_id, matched_at

messages
  match_id, sender_id, content, sent_at
```

---

## Pages Status

| Route | Status |
|---|---|
| `/` | ✅ Done |
| `/register` | ✅ Done |
| `/login` | ✅ Done |
| `/onboarding` | ✅ Done |
| `/app` | ✅ Done (swipe + match modal) |
| `/app/profile` | ✅ Done |
| `/app/matches` | ❌ TODO |

---

## API Routes Status

| Endpoint | Method | Status |
|---|---|---|
| `/api/auth/register` | POST | ❌ TODO |
| `/api/auth/login` | POST | ❌ TODO |
| `/api/auth/logout` | POST | ❌ TODO |
| `/api/onboarding` | POST | ❌ TODO |
| `/api/users/feed` | GET | ❌ TODO |
| `/api/swipe` | POST | ❌ TODO |
| `/api/matches` | GET | ❌ TODO |
| `/api/profile` | GET / PATCH | ❌ TODO |

---

## Matching Logic
1. User A swipes right → saved in `swipes`
2. Check if User B already liked User A
3. Mutual → create `matches` row → return `{ matched: true }`

Feed: same city + shared subjects + not yet swiped.

---

## Auth
Cookie-based sessions. Store `user_id` in signed cookie via SvelteKit hooks. No JWT.

---

## Key Decisions
- English-only UI (Baloo 2 has no Cyrillic)
- In-person matching, location-based
- No WebSocket for MVP — simple fetch polling
- Raw `better-sqlite3`, no Prisma
- Single SQLite file — perfect for CS50 demo
