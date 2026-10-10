#!/usr/bin/env python3
"""gen_gsm_regulation - add Galactic Overhaul's Dividend Reinvestment card to Galactic Stock
Market's regulation page.

    python tools/gen_gsm_regulation.py           # (re)write interface/zz_go_gsm_regulation.gui
    python tools/gen_gsm_regulation.py --check   # exit 1 if GSM changed and the file is stale

WHY A GENERATOR. GSM (Workshop 3813910097, a third-party mod) draws its regulation page as one
fixed window, `gsm_win_regulation`, in its generated interface/gsm_gen_terminal.gui. Stellaris
keeps the LAST definition of a window name, so the only way to add a card is to redefine that
window in a file that loads after GSM's (the zz_ prefix - the same mechanism GSM itself uses for
the bottom bar). A hand-made copy would freeze GSM's layout and silently mask its next update, so
this script rebuilds the copy from whatever GSM version is installed, and refuses when GSM's
layout no longer matches what the card was designed against. The generated file is git-ignored:
GSM's markup is theirs and stays out of this public repo.

The card's buttons call Galactic Overhaul's own button effects
(common/button_effects/galactic_overhaul_gsm_reg_button_effects.txt), not GSM's event options, so
GSM's event gsm_ui.5 is untouched.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GSM = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3813910097")
OUT = REPO / "interface" / "zz_go_gsm_regulation.gui"
WINDOW = "gsm_win_regulation"

# Designed against GSM 1.0.0: bottom-row cards at y = 461, 245 x 337, columns 257 apart; the
# fourth bottom-row column (x = 789) is empty. Option buttons 213 x 38 from y = 599, 43 apart.
CARD_X, CARD_Y, CARD_W, CARD_H = 789, 461, 245, 337
BTN_Y0, BTN_DY = 599, 43
ANCHOR = ('buttonType = { name = "gsm_p30" quadTextureSprite = "GFX_gsm_panel" '
          'position = { x = 532 y = 461 } size = { x = 245 y = 337 } alwaysTransparent = yes }')
OPTIONS = ["off", "on", "index", "desk"]


def extract_window(text, name):
    i = text.find('name = "%s"' % name)
    if i < 0:
        raise SystemExit("GSM no longer defines %s - the card cannot be placed" % name)
    s = text.rfind("containerWindowType", 0, i)
    depth = 0
    for j in range(s, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[s:j + 1]
    raise SystemExit("unbalanced braces in %s" % name)


def check_layout(block):
    """Refuse unless GSM's layout is the one the card was designed against."""
    problems = []
    if ANCHOR not in block:
        problems.append("the third bottom-row card (gsm_p30) moved or changed size")
    if "size = { width = 1440 height = 810 }" not in block:
        problems.append("the window is no longer 1440 x 810")
    for x, y in re.findall(r"position = \{ x = (-?\d+) y = (-?\d+) \}", block):
        if CARD_X - 10 <= int(x) < CARD_X + CARD_W and CARD_Y <= int(y) < CARD_Y + CARD_H:
            problems.append("something now occupies the free slot at x=%s y=%s" % (x, y))
    if problems:
        raise SystemExit("GSM's regulation layout changed - card not generated:\n  " + "\n  ".join(problems))


def card(indent="\t\t"):
    x, y = CARD_X, CARD_Y
    L = [
        "### Galactic Overhaul: Dividend Reinvestment card (tools/gen_gsm_regulation.py)",
        'buttonType = { name = "go_reg_p1" quadTextureSprite = "GFX_gsm_panel" position = { x = %d y = %d } '
        'size = { x = %d y = %d } alwaysTransparent = yes }' % (x, y, CARD_W, CARD_H),
        'iconType = { name = "go_reg_i1" spriteType = "GFX_gsm_section" position = { x = %d y = %d } '
        'alwaysTransparent = yes }' % (x + 16, y + 13),
        'instantTextBoxType = { name = "go_reg_t1" font = "cg_16b" text = "policy_go_dividend_reinvestment" '
        'position = { x = %d y = %d } maxWidth = 205 maxHeight = 20 fixedsize = yes format = left '
        'vertical_alignment = center text_color_code = "W" alwaysTransparent = yes }' % (x + 28, y + 12),
        'instantTextBoxType = { name = "go_reg_t2" font = "cg_16b" text = "GO_REG_DRIP_DESC" '
        'position = { x = %d y = %d } maxWidth = 213 maxHeight = 52 fixedsize = yes format = left '
        'vertical_alignment = top text_color_code = "v" alwaysTransparent = yes }' % (x + 16, y + 80),
    ]
    for n, key in enumerate(OPTIONS):
        by = BTN_Y0 + n * BTN_DY
        for state, sprite, transparent in (("cur", "GFX_gsm_btn_solid", True),
                                           ("set", "GFX_gsm_btn_ghost", False),
                                           ("no", "GFX_gsm_btn_off", True)):
            L.append(
                'effectButtonType = { name = "go_reg_%s_%s" quadTextureSprite = "%s" position = { x = %d y = %d } '
                'size = { x = 213 y = 38 } font = "cg_16b" buttonText = "GO_REG_DRIP_%s_%s" format = center '
                'effect = "go_reg_drip_%s_%s"%s }'
                % (key, state, sprite, x + 16, by, key.upper(), state.upper(), key, state,
                   " alwaysTransparent = yes" if transparent else ' clicksound = "interface"'))
    return "\n".join(indent + l for l in L) + "\n"


def build():
    src = GSM / "interface" / "gsm_gen_terminal.gui"
    if not src.exists():
        raise SystemExit("Galactic Stock Market not found at %s" % GSM)
    text = src.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    block = extract_window(text, WINDOW)
    check_layout(block)
    version = "unknown"
    desc = GSM / "descriptor.mod"
    if desc.exists():
        m = re.search(r'version="([^"]+)"', desc.read_text(encoding="utf-8", errors="replace"))
        version = m.group(1) if m else version
    sha = hashlib.sha256(block.encode("utf-8")).hexdigest()[:16]
    close = block.rstrip().rfind("}")
    merged = block[:close] + card() + block[close:]
    header = ("# GENERATED by tools/gen_gsm_regulation.py - DO NOT EDIT, NOT COMMITTED (.gitignore).\n"
              "# Source: Galactic Stock Market %s, interface/gsm_gen_terminal.gui, window %s (sha %s).\n"
              "# Redefines only that window to add Galactic Overhaul's Dividend Reinvestment card.\n"
              "# Re-run the script after Galactic Stock Market updates.\n\n" % (version, WINDOW, sha))
    return header + "guiTypes = {\n\t" + merged.replace("\n", "\n") + "\n}\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out = build()
    if a.check:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if cur != out:
            print("STALE: %s does not match the installed Galactic Stock Market - re-run without --check" % OUT)
            return 1
        print("OK: %s is current" % OUT.name)
        return 0
    OUT.write_text(out, encoding="utf-8", newline="\n")
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
