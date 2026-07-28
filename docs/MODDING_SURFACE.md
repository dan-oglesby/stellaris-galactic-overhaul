# Stellaris 4.4 "Pegasus" — Modding Surface Reference

A survey of what is moddable in Stellaris 4.4, grounded in this install
(`C:\Program Files (x86)\Steam\steamapps\common\Stellaris`) and the generated script
documentation in `Documents\Paradox Interactive\Stellaris\logs\script_documentation\`.

Written for **Galactic Overhaul**, so it is biased toward economy/automation work and
flags what this mod does *not* yet use.

**Scale of the surface**

| Surface | Size | Used by this mod |
|---|---|---|
| `common/` data folders | **169** | 15 (~9%) |
| Effects | **1,056** | ~40 |
| Triggers | **1,084** | ~25 |
| Scopes | **99** | 5 (country/planet/colony/ship/fleet) |
| `interface/` `.gui` files | **169** (+116 `.gfx`) | 1 custom window |
| Modifiers | `modifiers.log` is **4.2 MB** | a handful |

**Verification status.** Every claim marked ✅ was confirmed by direct file read. Claims
that failed verification are listed in [Corrections](#corrections--unverified) rather than
quietly dropped. The presentation/limits chunk was partly cut short by a session limit;
what is here was verified by hand, and the gaps are marked *(not yet surveyed)*.

---

## 1. The four systems that route around "impossible"

These are the headline finds. Each one bypasses a wall previously recorded as a hard limit.

### 1.1 `common/tradable_actions/` — custom bilateral treaties ✅
**Bypasses:** "mutual-consent pacts (embassy, commercial, NAP, defensive, research,
migration) cannot be created from script."

That remains true of *vanilla's* pacts. But you can define **your own** treaty that runs
through real diplomacy. From the vanilla schema in `00_tradable_actions.txt`:

| Field | Meaning |
|---|---|
| `fire_and_forget = no` | the deal becomes **"a treaty that lasts for at least 10 years"** |
| `potential` | whether it appears in the **vanilla trade-deal UI**. SCOPE = giving country, FROM = receiving |
| `active` | re-checked **daily**; the treaty cancels if it returns false |
| `on_traded_effect` | fires **when the deal is accepted** |
| `on_deal_ended_sender_effect` / `_recipient_effect` | fire on termination, on each side |
| `ai_weight` | **how much the AI values it** when deciding |

Vanilla's own example grants `set_galactic_custodian`, and 8 real treaties ship
(`trade_action_pledge_loyalty`, `share_empire_data`, `bulwark_prefabs`, …), so this is a
working system rather than a documented intention. A custom "Trade Concordat" can be
offered, genuinely accepted or refused by the AI, persist a decade, and run arbitrary
effects on both empires — without touching a vanilla file.

⚠️ **Scope of the bypass — do not overstate it.** This does *not* let you create, send or
accept a vanilla **embassy** or any vanilla pact: `effects.log` contains **zero** embassy
entries, so `has_embassy` stays false and the diplomacy screen shows nothing. It also does
**not** automate anything — there is **no effect that proposes or initiates a trade deal**
(the only proposal effects in the API are for Galactic Community resolutions:
`propose_resolution` / `pass_resolution`). The player still opens every deal by hand, one
empire at a time. What you get is a *parallel, custom* agreement with real AI acceptance —
useful, but a lookalike, not the vanilla relationship.

### 1.2 `common/scripted_actions/` — real custom fleet orders ✅
**Bypasses:** "construction ships cannot be given a real build order" (the reason Smart
Build uses fragile `queue_actions` choreography).

Ships a **19 KB README** (`99_README_SCRIPTED_ACTIONS.txt`) and real users
(`03_arkships.txt`, 49 KB). Verified fields: `required_progress`, `cooldown`, `cost`,
`on_completed` (raises a named on_action), `ai_minister`, and an **`automation = { }` block
that adds a real checkbox row to the vanilla fleet-automation menu** with nestable
sub-options. The fleet genuinely **paths to its target** before executing.

Attach via `scripted_action = { ... }` on a ship size — documented at
`common/ship_sizes/00_ship_sizes.txt:93` — or on a component template.

This is the *supported* version of what Smart Build hand-rolls.

### 1.3 `common/resource_converters/` + `set_resource_converter` ✅
**Bypasses (partly):** "no effect places a real market order."

`set_resource_converter = <key/none>` (country scope, `effects.log:3104`) swaps a country
onto a scripted economy rule-set the engine applies every tick:

- `can_be_paid_with = { minerals = 2.4 }` — automatic substitution at **scripted exchange
  rates** when a resource runs short
- `bottomless = yes` — spending always succeeds (basis for a credit/overdraft system)
- `override_trade_restriction` — bypasses market-access gating
- `affected_situation` — wires resource income directly into a Situation's progress bar

A functioning internal exchange with **no event scripting**. Vanilla ships ~one (Nomads).
Caveat: set per-country and replaces wholesale — conflicts with any other mod calling it.

### 1.4 `game_rules` `should_colony_automate` ✅
**Bypasses (from the other side):** "planet automation cannot be toggled from script."

It is a bare `always = yes` at `common/game_rules/00_rules.txt:2909`, colony scope.
Rewrite it to key off a planet flag and you get script-level control over whether
automation acts on a planet. Related script_value rules:
`building_automation_unemployment_threshold`, `building_automation_civilians_threshold`.

⚠️ Game rules still **cannot be invoked from script** (zero `game_rule` hits across
effects/triggers/scopes logs). All logic must live *inside* the rule body, keyed off flags
and variables the mod sets elsewhere.

---

## 2. Data surface — `common/` (169 folders)

Grouped by what they govern. ✅ = this mod already uses it.

**Scripting spine** — ✅ `scripted_effects`, `scripted_triggers`, `scripted_variables`,
`script_values`, `scripted_loc`, `on_actions`, `button_effects`.

**Empire & governance** — ✅ `policies`, `edicts`, `decisions`, `governments` (civics),
`resolutions`, `resolution_categories`. Untapped: `traditions`, `ascension_perks`,
`origins`, `ethics`, `agendas`, `authorities`.

**Economy & pops** — ✅ `strategic_resources`, `defines` (NEconomy market block).
Untapped and high-value:
- `resource_converters` — see §1.3
- `economic_plans` — **explicitly additive** (like `on_actions`), so safe to extend AI
  economic goals without conflict
- `economic_categories` — required companion for `country_container` (see §4)
- `pop_jobs` — the **only** way to influence job choice (weight/`possible` blocks, which
  *can* read country flags)
- `pop_categories` — `change_job_threshold`, `job_reshuffle_interval` per stratum
- `buildings`, `districts`, `deposits`, `planet_classes`

**Automation & AI** — all untapped:
- `ai_budget` (19 files, documented schema; needs `use_for_ai_budget = yes` on the
  economic category — only 29 qualify)
- `colony_automation` (18 files, 168 building entries; declarative, with trigger-gated
  `available` blocks) + `colony_automation_categories` + `colony_automation_exceptions`
  (supports `job_changes = { job = X amount = N }` with `emergency = yes` to bypass build
  gates — conditional, engine-ticked job assignment; only 2 vanilla users)
- `game_rules` — 217 named hooks in 4,734 lines
- `sector_focuses` — **dead end**, all six focus bodies are empty in 4.4

**Diplomacy** — `diplomatic_actions` (~6.5 K lines; UI/AI-driven), `diplo_phrases`,
`tradable_actions` (§1.1), `agreement_presets`, `federation` types.

**Galaxy & space** — `megastructures`, `starbase_*`, `solar_system_initializers`,
`planet_modifiers`, `map_modes`.

**Ships/military** — `ship_sizes` (hosts `scripted_action`), `component_templates`,
`ship_behaviors`, `armies`.

**Missions** — `common/missions/` **does ship data** (cosmic storms, nomads, contracts).

**Present but empty in this install:** `country_focus`, `country_limits`, `situation_log`,
`technology_ages`. Note `unchecked_defines/` sits at the **root**, beside `common/`.

### Override semantics (important)
Most keyed databases are replaced **by filename** — a mod file named the same as a vanilla
file replaces it wholesale. **Always ship new numbered filenames**, especially against the
monsters: `game_rules/00_rules.txt` (99 KB), `message_types` (112 KB),
`diplomatic_actions` (~6.5 K lines). Exceptions that **merge additively**: `on_actions`
and `economic_plans`.

---

## 3. Scripting API — untapped capability

**Situations = a free native dashboard.** A persistent player-visible panel with a staged
progress bar, player-selectable **Approaches** each carrying their own
`resources = { category cost upkeep produces }` table and modifiers, `monthly_progress` as
a script_value weight block, scriptable blocked-state alerts, `permanent = yes`, and its
own `on_monthly` on_action that runs *only while the situation exists*. Most of a custom
GUI can be replaced by data files that survive Paradox UI patches.

**`deficit_situation` — polling replaced by an engine trigger** ✅ Confirmed in
`common/strategic_resources`: `deficit_situation = situation_energy_deficit` (also
minerals, food, consumer goods). The engine starts a situation **the instant** a country
enters deficit. Directly relevant: this mod polls 8 resources every month for every empire.

**Messaging without custom GUI** ✅ `create_message` (`effects.log:1589`) with
`type` / `localization` / `days` / `target` / `variable`, plus `add_notification_modifier`
(persistent government-screen badge), `add_timeline_event`, and the `*_list_tooltip` family.

**Data structures.** There are **no variable arrays** — variables are strictly scalar. But
flags and event targets accept a `<key>@<scope>` suffix
(`set_agreement_flag = my_flag@from`), giving a savegame-persistent associative map keyed
by game object.

**Pops.** Can be created, moved between planets, killed, and re-ethicised by script;
`check_planet_employment` forces immediate re-employment. There is **no effect to
prioritise or forbid a specific job** — that is `common/pop_jobs` weight triggers only.

**Scopes.** 99 scope links across 39 object types; this mod uses 5. Untouched object types
with their own flags/variables/iterators/event dispatchers: `agreement`, `situation`,
`mission`, `sector`, `job`, `design`, `deposit`, `spy_network`, `espionage_operation`,
`debris`, `exhibit`. Most require iterators from country scope (`every_agreement`,
`every_situation`, `every_owned_sector`, `every_owned_design`), which is why they get
overlooked.

**Hooks.** ~300 on_actions exist; the vast majority are **event-driven and free**. The
costly ones are `on_monthly_pulse_country` (per country per month — where this mod's ~9
events live) and `on_colony_monthly_pulse` (per planet per month; vanilla keeps it to 3).
`on_building_queued` / `on_district_queued` are **empty in vanilla** and fire at *order*
time, before resources are spent. Per-database `on_*` hooks exist on buildings, decisions,
megastructures, deposits, policies and traditions — behaviour attached to one entity at
zero global cost. 19 typed event dispatchers, all accepting `scopes = { from = fromfrom }`.
`is_triggered_only` + `hide_window` + `pre_triggers` is the correct performance shape;
avoid `mean_time_to_happen` (137 vanilla uses vs 9,499 `is_triggered_only`).

---

## 4. Presentation layer

**`interface/`** — 169 `.gui` + 116 `.gfx`. Element types available (usage counts):
`containerWindowType` 3130, `iconType` 2623, `instantTextBoxType` 2328, `buttonType` 1808,
`gridBoxType` 235, `guiButtonType` 164, `smoothListboxType` 131,
`OverlappingElementsBoxType` 131, `checkboxType` 72, `editBoxType` 70, `spinnerType` 37.
This mod uses only a handful — `checkboxType`, `editBoxType`, `spinnerType` and
`gridBoxType` are unexploited.

⚠️ **You cannot add a row to a vanilla window.** Same-filename override replaces the whole
file, so extending e.g. `topbar.gui` or `market_view.gui` means shipping a full copy —
a maintenance and compatibility landmine.

**`common/country_container/` — the cheap topbar win** ✅ Verified. Its own header explains
it exists "to solve the problem of where resource income bonuses come from in the tooltips
in the topbar" — without it, a `*_produces_add` modifier silently changes "Base: X" with no
explanation. Define an entry plus a matching `common/economic_categories` entry and your
income becomes a **named line in the topbar tooltip**. Directly applicable: this mod's
interest, tax and trade income currently appear as unexplained deltas.

**`common/map_modes/`** — supports `color`, `icon`, `shortcut`; a custom map mode colouring
empires by a scripted value is feasible.

**`common/notification_modifiers/`**, **`common/message_types/`** (114 KB) — status badges
and message definitions.

**Localisation** — `§Y…§!` colour codes, `£resource£` icon tokens, `[Scope.GetX]` tokens,
`scripted_loc` `defined_text` (incl. `value = value:<script_value>` for numbers), custom
tooltips, the concept/keyword system. Files require a **UTF-8 BOM**, and a literal newline
inside a quoted value kills **every key after it in that file**.

*(gfx/portraits/models/shaders, music/sound, flags, fonts: not yet surveyed.)*

---

## 5. Hard limits

Evidence-backed. Each is "zero hits across effects/triggers/scopes logs" unless noted.

| Limit | Workaround |
|---|---|
| No effect assigns an **envoy** to a task | None. Do the envoy's job directly (e.g. `finish_first_contact_effect`) |
| No effect creates/sends/accepts an **embassy** or the 5 mutual-consent pacts | Nothing restores the vanilla relationship. `tradable_actions` (§1.1) gives a *custom lookalike* treaty; `add_trust` / `add_opinion_modifier` raise AI acceptance of a manually-sent proposal |
| No effect **proposes or initiates a diplomatic offer / trade deal** (only `propose_resolution` for GalCom) — so no diplomacy can ever be automated | None. Reduce refusals with `add_trust` / `add_opinion_modifier`; the click stays manual |
| No **real market order** | Simulate via `add_resource` at `market_resource_price`, or `resource_converters` (§1.3) |
| **Planet automation** cannot be toggled | `should_colony_automate` game rule (§1.4) |
| No **sector focus** effect | Dead end — vanilla focus bodies are empty in 4.4 |
| No real **construction order** | `scripted_actions` (§1.2) |
| **Game rules** cannot be invoked from script | Put the logic in the rule body, keyed off flags/variables |
| **Defines** cannot be read back from script | No `define:` accessor exists; duplicate the value as a `@constant` |
| Cannot add to a **vanilla GUI window** | Whole-file replace, or use Situations / `create_message` / `country_container` |

**Diplomacy's underlying rule:** anything requiring another empire's *consent* is
unscriptable; anything **unilateral or imposed** is scriptable — `declare_war`,
`set_truce`, `set_subject_of`, `guarantee_country`, `set_closed_borders`,
`establish_communications`. A second pattern: **removal is exposed, creation is not**
(`dissolve_federation`, `remove_from_federation`, `end_rivalry` exist; no create/join/make).

**Checksum/ironman:** overriding defines or any file changes the checksum, disabling
achievements and requiring all MP players to run the mod.

---

## 6. Corrections & unverified

Kept deliberately, so nothing gets laundered into fact.

- ❌ **`issue_contract` is not a bilateral empire agreement.** `effects.log:3048` says it
  "adds the specified contract to a **target system**" — it is the Nomads/cosmic-storms
  mission system. An agent overstated it as a diplomacy bypass.
- ❌ **`common/missions/` is not empty** — a second agent claimed it ships no data; it does.
- ⚠️ **`owned_planet` deprecation: unverified.** Claimed deprecated in favour of
  `owned_colony`; grepping `scopes.log` for "deprecated" returns **zero hits**. Not acted on.
- ⚠️ **`save_global_event_target_as` is genuinely global** (`effects.log:699`, "accessible
  globally until cleared"). This mod's `go_bank_player` is a single global slot. Harmless in
  single-player (the panel is `is_ai = no` gated) but in **multiplayer** two human megacorps
  would overwrite each other's target. A `<key>@<scope>` form exists. Known limitation, not
  yet fixed — the panel is fragile and working.

---

## 7. Prioritised opportunities for Galactic Overhaul

1. **`country_container` + `economic_categories`** — small change; makes bank interest, tax
   and trade income appear as *named lines* in the topbar tooltip instead of unexplained
   deltas. Directly addresses the recurring "I can't see what this is doing" problem.
2. **Situations** — replace parts of the fragile custom GUI with a native, patch-proof
   dashboard, with Approaches as a built-in settings UI.
3. **`deficit_situation`** — stop polling 8 resources monthly; let the engine tell us.
4. **`scripted_actions`** — rebuild Smart Build on the supported order system, with a real
   checkbox in the vanilla fleet-automation menu.
5. **`tradable_actions`** — the actual answer to the embassy/pact request.
6. **`resource_converters`** — an engine-level exchange, if the simulated desk is ever to
   be replaced.

---

*Survey run 2026-07-26 against Stellaris 4.4.6 (mod compat 4.4). Chunks 1–2 completed;
chunk 3 partly hand-verified after a session limit cut the agents short.*
