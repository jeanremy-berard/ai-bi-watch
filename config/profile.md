# Reader profile

This file is the relevance model. The classifier and the digest writer both read it.
Edit it freely: it is the main knob for tuning what gets through.

## Who reads this

Head of Data, BI & AI. Main stack: Microsoft Fabric and Power BI. Builds with LLMs
(Claude) in practice. Knows the fundamentals of data, BI and AI: never explain basics.
Reads the digest on Saturday mornings, wants signal, not volume.

## The significance test

One question decides significance: **does this change what I could build, or how I
would architect it?** Secondary: does it change what my tools cost or whether I can
use them?

| Score | Meaning |
|---|---|
| 5 | Changes the landscape: major model generation, platform-level shift, access/pricing change on a tool I depend on |
| 4 | Clearly useful capability I could adopt within months (major feature GA or public preview, important new API) |
| 3 | Worth knowing: solid incremental release, strong practitioner piece, notable paper with traction |
| 2 | Marginal: niche feature, vendor tutorial, minor version |
| 1 | Noise |

## Categories

- `ai_releases`: models, AI platforms and products (new models, major platform features)
- `ai_engineering`: building with AI: agents, MCP, frameworks, evals, tooling, practical engineering
- `ai_research`: papers and research results (to be popularized)
- `bi_microsoft`: Microsoft Fabric and Power BI
- `bi_market`: other BI/data vendors (Databricks, Snowflake, dbt, Tableau, Looker, Qlik, DuckDB...)
- `bi_practice`: tool-independent BI craft: data modeling, semantic layers, metrics, governance, performance, analytics engineering
- `access_licensing`: anything that changes whether, where or at what price I can use a tool I depend on (Claude, Microsoft Fabric/Power BI, major AI APIs): pricing and licensing changes, regional availability, export controls or regulation that is enacted or imminent and directly affects availability

## Keep

- Major releases and significant upcoming features (announced public previews, roadmaps of major features)
- Research with real traction, from major labs or widely picked up by practitioners
- Practitioner writing on BI craft, even if not new (evergreen is fine for `bi_practice`)
- Access, pricing and licensing changes on tools in my stack

## Drop

- Funding rounds, valuations, IPOs, M&A gossip, hiring/executive moves
- Minor features and UI tweaks ("dark mode is now GA", small connector updates, minor version bumps)
- Prompt listicles, "10 tricks", hype, clickbait, generic how-to tutorials for beginners
- Philosophical, political, ethical or societal debate about AI; opinion pieces about the future of work
- Regulation in general (proposals, hearings, debates), unless it is enacted or imminent AND directly affects availability or pricing of my tools
- Events, webinars, conference recaps without new information, customer case studies, partner marketing
- AI safety/alignment research unless it changes how models can be used in practice

## Judge the core news, not the framing

Many articles wrap a real release inside paragraphs about the future of work or society.
Judge the underlying news. Conversely, an article about a real product that is mostly
opinion should be judged as opinion.

## Research items

Research must be popularized: plain language, no jargon without a short gloss. Always
say what was done, why it might matter and on what timescale (now / within a year /
long term), and how solid it looks (one lab's claim vs replicated or widely adopted).
