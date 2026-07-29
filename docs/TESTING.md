# Testing Galactic Overhaul without burning hours

Playtesting this mod is expensive when a feature is gated behind slow in-game
progress (the Galactic Bank charter needs a Galactic Community vote, which can take
hours) and when mod updates force a new game. Most of that is avoidable.

---

## 1. Console shortcuts

Open the console with `` ~ ``. Achievements are already disabled by any mod, so
these cost nothing.

| Goal | Command |
|---|---|
| **Unlock Galactic Banking now** (skip the Community vote) | `effect set_global_flag = galactic_overhaul_chartered` |
| …then name a bank host | `effect galactic_overhaul_select_host = yes` |
| Undo it | `effect remove_global_flag = galactic_overhaul_chartered` |
| Fire the interest tick immediately | `event galactic_overhaul.1` |
| Fire the trade desk immediately | `event galactic_overhaul.2` |
| Fire the bank auto-sweep immediately | `event galactic_overhaul.4` |
| Fire the branch-office sweep | `event go_branch.1` |
| Open the Reserve panel | `event go_bank.1` |
| Turn the mod's debug logging off | enact the **Toggle Galactic Overhaul Debug Log** decision on your capital |

The banking policy's only gate is `has_global_flag = galactic_overhaul_chartered`
(`common/policies/galactic_overhaul_policies.txt`), which is why the first command is
enough — no resolution, no host, no waiting.

Useful vanilla ones for setting up a test state: `cash`, `minerals`, `influence`,
`research_all_technologies`, `instant_build`, `skipsurvey`.

---

## 2. When do you actually need a new game?

Most changes are **save-safe** — update the mod, reload the save, carry on.

### Save-safe (keep playing)
- Tuning any `@constant` (all the balance dials)
- Logic changes **inside** an existing scripted_effect / scripted_trigger / event
- Adding or changing an event `trigger` block
- Localisation edits
- New scripted_effects, scripted_triggers or script_values
- Reordering entries in an `on_action`
- Adding a new event to an existing `on_action`

### Needs a new game
- **Removing or renaming a policy**, or any of its **options** — the save stores the
  selected option key, and a dead key breaks that policy (this is what bit the
  `gb_*` → `go_*` rename at v0.12.0)
- **Removing a civic** an empire actually has (v0.26.0)
- **Removing or renaming a strategic resource**
- **Renaming event IDs** referenced by in-flight `queue_actions` (Smart Build and
  Auto-Colonization drivers hold queued action IDs across saves)
- **Adding a brand-new policy** — Stellaris does not reliably retrofit one into an
  existing save's `active_policies`

### Cheaper than a new game
- Toggling a policy **off and back on** re-enrols ships and rebuilds queued actions —
  enough to pick up most Smart Build / Colonization changes without restarting.

---

## 3. Reading the logs

Everything is under `Documents\Paradox Interactive\Stellaris\logs\`.

```bash
grep -c "GALACTIC_OVERHAUL" game.log            # did anything run at all?
grep -ohE "GALACTIC_OVERHAUL[A-Z_]*" game.log | sort | uniq -c | sort -rn
```

Tags: `GALACTIC_OVERHAUL` (host/charter), `_BANK`, `_TRADE`, `_TAX`, `_SMARTBUILD`,
`_COLONY`, `_SCIENCE`, `_BRANCH`.

The trade desk logs one line per resource per month:

```
<empire> alloys act=2 amt=25.9 stock=3516 cap=35000 inc=-14.0 price=4
```

`act` — `0` idle · `1` sold surplus · `2` restocked · `3` opportunistic buy ·
`4` opportunistic sell.

For `error.log`, the mod's own problems are the lines naming a `galactic_overhaul`
or `go_*` file. These are known-benign and can be ignored:
- `Missing modifier icon .../mod_resource_go_banked_credits_*` — auto-generated per
  custom resource
- `Did not find a greyscale icon for resource: go_banked_credits`
- `Object with key: choose_galactic_market_host already exists` — expected for a
  deliberate vanilla override; it naming *our* file means the override is active

---

## 4. Getting a feature into a testable state fast

- **Treasury Reserve** — charter via the console command above, set the Galactic
  Banking policy to any tier, then `cash` yourself trade so the sweep has something
  to deposit. Watch `GALACTIC_OVERHAUL_BANK`.
- **Treasury Automation** — set the policy, then drain a resource (or just watch
  alloys) and confirm `act=2` restock lines appear.
- **Branch offices** — needs a Corporate authority, the MegaCorp DLC, and a
  commercial pact / federation / subject relationship with someone (or a criminal
  syndicate, which needs no pact). Watch `GALACTIC_OVERHAUL_BRANCH`.
- **Smart Build / Auto-Colonization** — need construction/colony ships and spare
  influence and alloys.
