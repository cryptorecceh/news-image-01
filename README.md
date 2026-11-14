# The World in One Page — Friday 13 November 2026

Entry for make.fun's **news-image-01** bounty: "Sum up 13 November's world
news in one image" ($250 in USDC).

`main.py` copies `entry.png` to `/output/entry.png`. `entry.png` is a
newspaper front page drawn programmatically by `render.py` (PIL, run at
build time — the graded program itself is standard library only and runs
with no network).

## The stories (all first reported Friday 13 November 2026)

- **Lead — NVIDIA chief summoned by Congress.** A day after Jensen Huang
  quit as chief executive, lawmakers open a probe into Nvidia's China chip
  sales, and the ex-chief must testify. (BBC / Guardian / FT)
- **FAA lifts nationwide ground stop.** Flights resume at 8:15 p.m. ET
  after a 4.5-hour halt; 8,267 departures cancelled, a third of the day's
  schedule. (AP / Airways Magazine)
- **Microsoft 365 outage drags on.** Outlook, Teams and Copilot still
  recovering after Thursday's global failure. (Guardian)
- **Türkiye–Qatar defence pact.** Erdoğan and Emir Tamim sign a mutual
  defence deal in Istanbul. (Reuters)
- **Europe joins Ukraine talks.** Dublin agrees the EU and five states will
  sit at the peace table. (BBC)
- **Taiwan details China drills.** Taipei calls Beijing's unannounced
  Pacific exercises intimidation. (Reuters)
- **IEA forecasts oil surplus.** Supply to top demand by 1.7m barrels a day
  in the fourth quarter. (Reuters / IEA)
- **Ebola cases pass 11,000.** Second-worst outbreak on record. (Reuters / UN)
- **Also:** IAEA flags an uninspected Iranian enrichment plant; Israeli
  strikes in southern Lebanon; US Treasury chief faults delays on Nvidia
  chip controls.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Produces `out/entry.png` (1024×1024 PNG, ~120 KB, byte-identical every run).

## License

MIT — see `LICENSE`.
