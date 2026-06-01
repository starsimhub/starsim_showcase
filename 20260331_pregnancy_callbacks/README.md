# Extending modules without inheritance: hooks in Starsim

**Starsim show and tell #01** — Robyn Stuart, 2026-03-31

## Overview

How we used callback hooks to let `FetalHealth` plug into `Pregnancy` — and when you might (or might not) want this pattern.

The notebook covers:

1. **The Starsim loop** — the fixed 16-step sequence and why ordering matters
2. **Two extension approaches** — inheritance vs. hooks, with worked examples
3. **Hooks in practice** — how `FetalHealth` uses `Pregnancy`'s `_conception_callbacks` and `_delivery_callbacks`
4. **Chaining** — how hooks compose across layers (Pregnancy → FetalHealth → connectors)
5. **Minimal example** — a `BirthWeightTracker` that hooks into Pregnancy, stripped to essentials

## Files

- `callbacks_showcase.ipynb` — the notebook
- `loop_order.png` — diagram of the Starsim simulation loop
- `hooks_vs_inheritance.png` — comparison of the two extension approaches
- `pregnancy_hooks.png` — diagram of hook firing points inside `Pregnancy.step()`

## Running the notebook

```bash
pip install starsim
jupyter notebook callbacks_showcase.ipynb
```
