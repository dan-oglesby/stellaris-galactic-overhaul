# Galactic Overhaul — fitting the vanilla user experience

Audit, 2026-10-10, against Stellaris 4.5.2 "Cygnus" vanilla files and Dan's current 25-mod playset.
Goal (Dan): "make sure the things we do blend in pretty well." Every finding below cites what vanilla
does and what GO does now, so each one can be checked.

## Where GO touches the player

8 policies · 2 decisions (debug toggle, open bank) · 1 edict (open bank) · 1 Galactic Community
resolution (+ re-host) · 1 resource (Banked Credits) · the Galactic Bank window · the Dividend
Reinvestment card on Galactic Stock Market's regulation page. No notifications, no glossary
concepts, no Databank entries, no custom art.

## Findings

### 1. Banked Credits has no icon (bug, visible)
`error.log`, every launch: *Did not find an icon for resource: go_banked_credits* (and greyscale), plus
9 *Missing modifier icon* lines (`mod_resource_go_banked_credits_mult.dds`, `…_upkeep_add.dds`, …).
For resources the engine loads the **file** `gfx/interface/icons/resources/<key>.dds` (and `_grey`,
`_large`) directly. Our `.gfx` sprite (`GFX_resource_go_banked_credits` → `trade.dds`) is not what it
reads. Vanilla ships all three for every resource, plus an icon per resource modifier.
Even if the reuse had worked, Banked Credits would look identical to Trade.

### 2. Banked Credits is always visible
Vanilla resources gate the top bar with `visibility_prerequisite` (e.g. `sr_zro`: `{ always = yes }` with
a tech prerequisite). Ours has none, so it can appear before the bank is chartered.

### 3. Text voice and shape differ from vanilla
Measured across 168 vanilla policy descriptions vs GO's 48:

| | vanilla | GO |
|---|---|---|
| addresses the player as "you / your" | **0%** | 66% |
| median length | 142 chars | 166 (max 758) |
| uses colour codes (§E effects, §H highlights) | 49% | 10% |
| shares an effects block via `$…$` | 23% | 0% |
| ASCII " - " | 0% | 18% |

Vanilla's shape is one in-universe sentence in the empire's voice ("We will…", "Trade is an important
source of prosperity for our empire", gestalts "The Mind…"), then `\n\n`, then the mechanics in
`§E…§!`. Ours reads like a manual, written to the player.

### 4. Automation is silent
Vanilla has 418 notification types, and players can toggle each one in the game's notification settings
(`message_setting_key`). GO's desks, branch offices, colony and science automation, and bank interest
report only to `game.log`. Galactic Stock Market shows the pattern: one `message_type` (`category = economy`,
`default_toast = yes`) plus `create_message` calls.

### 5. No glossary or Databank presence
Vanilla links terms in tooltips (`['concept_…']`, in **2,441** vanilla strings). Concepts in
`common/game_concepts/` can carry a **Databank** entry with an icon and picture. GO links nothing and
defines nothing. Vanilla concepts we could link today include `concept_branch_office`, `concept_market`,
`concept_trade`, `concept_crime`, `concept_influence`, `concept_galactic_community`, `concept_edicts`,
`concept_colony_ship`, `concept_construction_ship`, `concept_science_ship`, `concept_starbase` and
`concept_market_view`.

### 6. The bank window doesn't use the economy windows' kit
Vanilla's Market and Edicts windows use `GFX_tiled_window_transparent` (frame), `GFX_tiles_dark_area_cut_8`
(cut-corner panels, which is vanilla's own version of the "card" look), `GFX_hex_bg`, `GFX_tab_1_active`
tabs, `GFX_line`, and the fonts `malgun_goth_24` / `cg_16b`. The bank uses `GFX_plain_bg_tile` +
`GFX_dark_area_window_bg` in a 480×360 box, so it reads as a different game. No custom art is needed to
fix this.

### 7. The bank has two improvised doors
A one-day edict (`go_open_bank_edict`, `length = 1`, timer icon) sits in the Edicts list as if it were a
policy lever, and there is also a planet decision. Vanilla opens screens from the HUD and screen
buttons, never through edicts.
**No mod in Dan's playset overrides `market_view.gui`**, so a "Galactic Bank" button in the vanilla
Market screen would be conflict-free. It would be a generated override, re-synced after patches, as
`tools/gen_gsm_regulation.py` already does. The bottom bar is taken by Galactic Stock Market (see the
launcher discussion).

### 8. Developer tools are visible to players
The "Toggle Galactic Bank Debug Log" decision is offered to every human player, and debug logging is on
by default. That was ~1,900 `GALACTIC_OVERHAUL_TRADE` lines in one session's `game.log`.

### 9. Policy option icons borrow diplomatic-stance art
GO options use `GFX_diplomatic_stance_*`. Only 24 of 224 vanilla policy options set an icon at all.

### 10. One permanent error-log line
*Object with key: choose_galactic_market_host already exists* — the intentional override of vanilla's
market-host effect. It's harmless, but it's the only GO entry in the log besides the icons.

## Recommended plan

| # | Change | Effort | Risk |
|---|---|---|---|
| A | Banked Credits icon set (resource normal/grey/large + 9 modifier icons) as original art in vanilla's resource style; `visibility_prerequisite` once chartered | small | none |
| B | Hide the debug decision behind a global flag (console-settable); debug logging **off** by default | small | none |
| C | Text pass: every description in vanilla voice and shape (in-universe sentence, `\n\n`, `§E` mechanics), `£trade£`-style inline icons, concept links | medium | none |
| D | Notifications: one GO `message_type` (economy); concise digests for desk trades, offices opened, bank interest, stock desk; toggleable in settings | medium | low |
| E | Concepts + Databank entries for Treasury Reserve, Banked Credits, Treasury Automation, Branch Office Automation, Dividend Reinvestment | medium | none |
| F | Bank window restyled with vanilla's economy kit (frame, cut panels, tabs), sized like the Market window | medium | low |
| G | Bank entry point moved to a button in the Market screen (generated override); retire the edict and decision | larger | medium (vanilla patches; generator re-sync) |
| H | Policy option icons: drop the borrowed stance icons, or draw matching ones | small | none |

Suggested order: A, B, then C/E together (shared vocabulary), then D, F, G. Choices that need Dan:
debug-off default (B), notification defaults and frequency (D), whether G replaces or supplements the
current doors.
