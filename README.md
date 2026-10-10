# Galactic Overhaul

A multi-feature **economic & automation overhaul** for **Stellaris 4.4 "Pegasus"**.

`version 0.31.0` · `supported_version 4.5.*` · tags: Economy, Gameplay

## Features

- **Treasury Reserve (Galactic Banking)** — a Galactic Community resolution charters a galaxy-wide reserve bank. Deposit trade into **Banked Credits** and earn a **flat, stated monthly interest** — no hidden formulas. Conservative / Standard / Aggressive tiers (0.3% / 0.6% / 1.2% per month); the higher tiers pay more but carry a stated monthly **chance of loss**. Surplus trade is swept into the Reserve automatically (keeping a liquid floor), and a transparent **Galactic Bank panel** — opened from the **Edicts** screen — shows your balance, rate, last month's interest and liquid trade, and lets you deposit/withdraw by hand.
- **Treasury Automation** — an auto buy/sell desk that keeps each commodity self-levelling in a reserve band: it **restocks** anything that falls below ~25% of its cap (so bursty consumers like alloys don't run dry) and sells the overflow near ~90% of cap — but only when there's a use for the proceeds (it holds rather than sell if your Trade pool is already near full). An **Opportunistic** setting adds active buy-low / sell-high trading against each commodity's recent average, for a monthly management fee.
- **Taxation Doctrine** — an automated tax stance that drifts toward a chosen target (laissez-faire ↔ heavy), with societal effects.
- **Smart Build** — construction ships automatically claim outposts, build **mining/research stations** on unserviced deposits (deficit-first), and build megastructures (hyper relays, gateways, orbital rings, habitats), paying real costs.
- **Auto-Colonization** — automatically builds and dispatches colony ships to colonizable worlds in your borders.
- **Science Automation** — keeps science ships crewed by recruiting/assigning scientists.
- **Branch Office Automation** (megacorp) — an empire-wide policy that opens branch offices on qualifying colonies (of empires you have a commercial pact / federation / subject relationship with) and builds the most beneficial holding on each: **prioritizing the holdings your civics supercharge** (which grant extra capital Trader jobs), then your empire's resource shortfalls, then trade. Pays the real influence + mineral costs, rate-limited per month. Requires Corporate authority + the MegaCorp DLC.
- **No AI megacorps** (optional rule) — AI corporate empires are converted to oligarchic at game start, so the megacorp niche is yours.
- **Dividend Reinvestment** *(compatibility with [Galactic Stock Market](https://steamcommunity.com/sharedfiles/filedetails/?id=3813910097))* — a policy for what happens to quarterly dividends: take them as trade, **reinvest** each company's dividend in that company, or build an **index portfolio**, putting all dividends into the companies furthest below their market-cap weight in the Galactic Composite Index (new money only, never sells). Purchases go through the stock market's own buy path (fee, price impact, foreign-ownership limits, affordability). Whole shares only; the remainder stays as trade. The policy only appears when Galactic Stock Market is running, and nothing of that mod is overridden.
- Custom resource (Banked Credits), a strongest-economy Galactic Market host override, and always-on debug logging.

## Deploying (local dev)

Stellaris loads local mods via a `.mod` file in `Documents\Paradox Interactive\Stellaris\mod\`. This repo is the mod **content**; the `.mod` stub points at wherever you clone it.

1. Clone this repo somewhere **outside** any cloud-synced folder (OneDrive / Proton Drive conflict-copy the files mid-edit). e.g. `C:\StellarisModDev\galactic_overhaul`.
2. Create `Documents\Paradox Interactive\Stellaris\mod\galactic_overhaul.mod`:
   ```
   name="Galactic Overhaul"
   version="0.31.0"
   tags={
       "Economy"
       "Gameplay"
   }
   supported_version="4.5.*"
   path="C:/StellarisModDev/galactic_overhaul"
   ```
   (set `path=` to your clone location, forward slashes)
3. Enable **Galactic Overhaul** in the launcher.

## Debugging

Debug logging is **on by default** — grep `GALACTIC_OVERHAUL` in `Documents\Paradox Interactive\Stellaris\logs\game.log`. Toggle it off with the **"Toggle Galactic Overhaul Debug Log"** decision.
