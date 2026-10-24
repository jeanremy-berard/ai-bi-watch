# ai-bi-watch

Personal AI & BI news monitor. Curated feeds in, one weekly digest out.

```
config/sources.yaml ──► daily ingest (Haiku: keep/drop, category, significance, summary)
                              │
                              ▼
                      data/items/YYYY-MM.csv  (everything triaged, kept and dropped)
                              │
                              ▼  Saturday 06:41 Paris
                      weekly digest (Sonnet: cluster stories, edit, rank)
                              │
                              ▼
                      digests/YYYY-MM-DD.md + digests/latest.md
```

## Setup (once)

1. **API key**: create one at [platform.claude.com](https://platform.claude.com), ideally in a
   dedicated workspace with a monthly spend limit (e.g. $10). Expected cost is about $3/month.
2. **Secret**: repo *Settings → Secrets and variables → Actions → New repository secret*,
   name `ANTHROPIC_API_KEY`.
3. **Check feeds**: it runs automatically when `config/sources.yaml` changes (no key needed);
   results land in [`data/feed_status.md`](data/feed_status.md).
4. **First run**: *Actions → Daily ingest → Run workflow*. The first run looks back 7 days,
   later runs 3 days.
5. **First digest**: *Actions → Weekly digest → Run workflow* whenever you want one before Saturday.
6. **Site**: *Settings → Pages → Build and deployment → Source: GitHub Actions*, then
   *Actions → Publish site → Run workflow* once.

## Reading

- **Site**: https://jeanremy-berard.github.io/ai-bi-watch/ with two views: the weekly digest,
  and an explorer to filter every triaged item by period, significance, category, source and
  kept/dropped. Rebuilt after every pipeline run. Ratings (useful / not useful) stay in your browser
  and can be exported as JSON.
- [`digests/latest.md`](digests/latest.md), or the run's job summary in the Actions tab.
- Better: a Claude project with this repo connected through the GitHub connector, so you can
  ask questions about the digest and the underlying items.

## Tuning

| Want to change | Edit |
|---|---|
| What counts as relevant / significant | `config/profile.md` (read by both models) |
| Sources | `config/sources.yaml` (an `include:` regex list prefilters noisy feeds for free) |
| Models, windows, caps | `settings:` in `config/sources.yaml` |

The digest ends with an *Under the hood* section: drop reasons and borderline drops.
That is the calibration loop: if good items keep landing in borderline drops, loosen
the profile; if noise gets through, tighten it.

## Local runs

```bash
pip install -r requirements.txt
python -m watch.feedcheck            # no key needed
python -m watch.ingest --dry-run     # no API calls, keeps everything
python -m watch.digest --dry-run     # writes the model input instead of a digest
python -m watch.site && python -m http.server -d _site   # explorer on localhost:8000
```
