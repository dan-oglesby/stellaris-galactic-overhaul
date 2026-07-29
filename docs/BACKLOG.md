# Galactic Overhaul — Backlog

Running list of *maybe-build* items: things we've decided are worth considering but
haven't committed to. Feasibility notes come from `docs/MODDING_SURFACE.md`.

**Design principle:** this is a toggleable **quality-of-life automation** mod, not a
cheat mod. Automation does what the player would have done by hand, at the same cost,
under the same rules. Anything that grants resources from nothing, skips prerequisites,
or manipulates other empires' decisions in our favour is out of scope.

---

## Queued — agreed, just not built yet

| Item | Notes |
|---|---|
| **Embassy notification** | *On the backburner (user, 2026-07-29).* A toggleable alert when empires become eligible for an embassy. Purely informational, so it fits the QoL rule. `create_message` is confirmed; the work is mirroring `action_embassy`'s eligibility conditions (comms established, not at war, no embassy yet, neither side fanatic purifier / devouring swarm / terminator). **Open question:** one-off toast when new candidates appear, or a persistent badge while any exist? Leaning toast — a permanent badge for something you may deliberately ignore becomes nagging. |

## Strong candidates — cheap, high value

| Item | Why | Effort |
|---|---|---|
| **`country_container` + `economic_categories`** | Makes bank interest, tax and trade-desk income appear as **named lines in the topbar tooltip** instead of unexplained deltas. Directly addresses the recurring "I can't see what this is doing" problem. Vanilla's own file exists precisely to solve this. | Small |
| **Situations as a native dashboard** | Could replace much of the hand-built `custom_gui` panel with data files that survive Paradox UI patches: staged progress bar, player-selectable Approaches (a built-in settings UI), scriptable alerts, `permanent = yes`. | Medium |
| **`deficit_situation`** | Confirmed in `common/strategic_resources`. The engine starts a situation **the instant** a country enters deficit — an event-driven replacement for polling 8 resources every month for every empire. Biggest performance win available. | Medium |

## Bigger ideas — real value, real cost

| Item | Why | Risk |
|---|---|---|
| **Rebuild Smart Build on `scripted_actions`** | The *supported* fleet-order system: real pathing, `required_progress`, cooldown, cost, `on_completed` hook, `ai_minister`, and an `automation = { }` block that adds a checkbox to the **vanilla fleet-automation menu**. Replaces our fragile `queue_actions` choreography. | Large rewrite of a working feature |
| **`tradable_actions` custom treaties** | Define our own bilateral treaty that appears in the vanilla trade-deal UI with genuine AI acceptance (`ai_weight`), lasting 10+ years. Interesting in its own right — **not** a substitute for vanilla pacts or embassies. | Medium; new subsystem |
| **`resource_converters`** | Engine-level per-country exchange rates (`can_be_paid_with`), `bottomless` spending, market-access override. Could replace the simulated trade desk entirely. | Conflicts with any other mod calling `set_resource_converter` |

## Open design questions — need a decision, not code

- **Bank interest is newly minted.** `add_resource = { go_banked_credits = 1 mult = go_interest }` creates credits from nothing. Defensible as a bank simulation with stated rates and real loss risk, but it *is* free resources and it compounds. Where's the line?
- **Opportunistic desk profitability.** Now that the fee spread is inside the trading band, it should accumulate trade. If it becomes a money printer in play, that's a balance dial (`@go_opp_buy_mult` / `@go_opp_sell_mult` / the fee mults), not a bug.
- **AI megacorp suppression** (`change_government` on AI empires at game start) reaches into other empires rather than automating our clicks. Requested deliberately and civic-gated, but it's the one existing feature that sits outside the QoL principle. Keep, make optional, or drop?
- **Research weighting** — now a first-class rotation slot (v0.25.0). Revisit if it still feels under-built.

## Known limitations — accepted, documented, not scheduled

- **Multiplayer:** the bank panel uses a bare `save_global_event_target_as = go_bank_player`, which is a single **global** slot. Fine in single-player (the panel is `is_ai = no` gated); with two human megacorps they'd overwrite each other. A `<key>@<scope>` form exists. Not fixed because the panel is fragile and working.
- **Branch offices:** criminal/legit ladder selection branches on `is_criminal_syndicate`, not on whether the office was *legalised* on that specific planet. Vanilla's `is_legit_or_legal_criminal` can't be called from our effect (it references `root.owner`, and our root is the megacorp).
- **Workshop release prep** (if we ever publish): needs a `thumbnail.png`, a store description, DLC-requirement notes (Federations / MegaCorp), a compatibility warning for the `choose_galactic_market_host` override, and a "new game recommended" note. See `docs/MODDING_SURFACE.md`.

## Ruled out — do not revisit

- **Auto-sending any diplomatic proposal** (embassies, the 5 mutual-consent pacts). No effect proposes or initiates a diplomatic offer or trade deal; the only proposal effects in the API are `propose_resolution` / `pass_resolution` for the Galactic Community. Firm engine wall.
- **Pumping `add_trust` / `add_opinion_modifier` so the AI can't refuse**, and overriding `action_embassy`'s `auto_accepted`. Both would buy outcomes rather than automate actions — rejected on design grounds.
- **Driving the built-in monthly-trade tool.** Zero effects for `monthly_trade` / `market_order` / `buy_resource` / `sell_resource`; the only three market effects are `set_market_leader`, `enable_on_market`, `enable_galactic_market`. `monthly_trades` is a data category plus UI, not an action.
- **Envoy assignment**, **sector focus** (vanilla focus bodies are empty in 4.4).
