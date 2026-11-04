# Filing Evidence Ledger

[繁體中文](README.zh-Hant.md) · [Website](https://filings.vesperai.space/en/)

Organize user-supplied public-disclosure quotations and reported numbers into a local Markdown ledger and a JSON field-completeness checklist.

## Run

Requires Python 3.10+. Clone this repository, then work from its root:

```sh
git clone https://github.com/Vesper2026/filing-evidence-ledger.git
cd filing-evidence-ledger
# No runtime dependencies; Python 3.10+ is sufficient.
python filing_evidence.py examples/sample.json --output examples/output
```

Optional project installation: create a local venv and install `.` there to expose the console entry point. Direct script execution needs no installation.

## Input and actual example output

```text
{"evidence":[{"id":"E01","question":"Revenue?","title":"Synthetic","source_url":"https://github.com/Vesper2026/filing-evidence-ledger/blob/main/examples/sample.json","location":"synthetic p12","quote":"Revenue was USD 12 million for FY2025.","value":"12.00","currency":"USD","unit":"million","period":"FY2025"}]}
```

The bundled fixture, not just the abbreviated illustration above, produces:

```text
3 evidence rows; 2 need field review. Sources not verified.
```

The bundled synthetic fixture has three rows. E01 preserves `12.00`; E02 produces `missing:period`; E03 produces `missing:quote`. Outputs: `ledger.json` and `ledger.md`. Values should be JSON strings. Required fields: id, question, title, source_url, location, quote. Nonempty values additionally require unit and period. Currency and disclosed_on are preserved, not inferred. Duplicate IDs remain separate rows and are flagged. `status` defaults to `unreviewed`; `reviewed` records your own status, not program approval.

## Tests

```sh
python -m unittest discover -p "test_*.py"
```

Six tests cover precision, missing fields, duplicate IDs, separate user status, escaping and input shape.

## Limits and privacy

No source fetching, URL availability checks, quotation verification, financial calculations or investment advice. A clean field checklist does not prove a fact. Source URLs in the synthetic fixture point to that fixture, not issuer disclosures. The tool reads inputs and writes reports locally; it does not upload documents. Markdown special characters and HTML are escaped; treat report content as untrusted user material when integrating it elsewhere.

## Build this repository's independent bilingual site

```sh
python site/build.py
python -m http.server 8090 --directory docs
```

Open http://localhost:8090/en/ or /zh-Hant/. The source lives in `site/`, output in `docs/`, and examples are copied to `docs/downloads/`. The site has two original articles per language, its own hostname/canonical/sitemap/robots/CNAME, and no analytics or upload form. 

## Useful tools

[Eqvero](https://eqvero.com/) can be used alongside this tool. KolmoPDF's cloud service uploads documents; these open-source local CLIs do not replace its proprietary parser.

## License

MIT for this code, authored fixtures, documentation and static-site sources; see LICENSE. Third-party dependencies keep their own licenses.
