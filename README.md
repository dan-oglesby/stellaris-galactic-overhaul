# Galactic Overhaul

A multi-feature **economic & automation overhaul** for **Stellaris 4.4 "Pegasus"**.

`version 0.18.0` · `supported_version 4.4.*` · tags: Economy, Gameplay

## Features

- **Galactic Banking** — a Galactic Community resolution charters a galaxy-wide reserve bank. Deposit trade into **Banked Credits** for compounding monthly interest whose rate reacts to market volatility. Conservative / Standard / Aggressive tiers; the higher-yield tiers carry a monthly **risk of loss**. Automatic deposit-when-flush / withdraw-when-low.
- **Treasury Automation** — an auto buy/sell desk that sells commodities near their cap (when overflowing) and buys them when running dry. An **Opportunistic** setting also actively buys commodities when they're cheap vs their recent average and sells when dear, for a monthly management fee.
- **Galactic Stock Market** — auto-invest surplus trade into **Galactic Shares** whose value tracks a live market index. Dividends, optional **DRIP** reinvestment, with diminishing returns, a management fee, and crash risk to keep it balanced. Liquidate on demand.
- **Taxation Doctrine** — an automated tax stance that drifts toward a chosen target (laissez-faire ↔ heavy), with societal effects.
- **Smart Build** — construction ships automatically claim outposts, build **mining/research stations** on unserviced deposits (deficit-first), and build megastructures (hyper relays, gateways, orbital rings, habitats), paying real costs.
- **Auto-Colonization** — automatically builds and dispatches colony ships to colonizable worlds in your borders.
- **Science Automation** — keeps science ships crewed by recruiting/assigning scientists.
- **Megacorp founding civics** — corporate empires can instantly found the Galactic Bank or Galactic Market galaxy-wide (with a popup for every empire); an option suppresses AI megacorps.
- Custom resources (Banked Credits, Galactic Shares), a strongest-economy Galactic Market host override, and always-on debug logging.

## Deploying (local dev)

Stellaris loads local mods via a `.mod` file in `Documents\Paradox Interactive\Stellaris\mod\`. This repo is the mod **content**; the `.mod` stub points at wherever you clone it.

1. Clone this repo somewhere **outside** any cloud-synced folder (OneDrive / Proton Drive conflict-copy the files mid-edit). e.g. `C:\StellarisModDev\galactic_overhaul`.
2. Create `Documents\Paradox Interactive\Stellaris\mod\galactic_overhaul.mod`:
   ```
   name="Galactic Overhaul"
   version="0.18.0"
   tags={
       "Economy"
       "Gameplay"
   }
   supported_version="4.4.*"
   path="C:/StellarisModDev/galactic_overhaul"
   ```
   (set `path=` to your clone location, forward slashes)
3. Enable **Galactic Overhaul** in the launcher.

## Debugging

Debug logging is **on by default** — grep `GALACTIC_OVERHAUL` in `Documents\Paradox Interactive\Stellaris\logs\game.log`. Toggle it off with the **"Toggle Galactic Overhaul Debug Log"** decision.
