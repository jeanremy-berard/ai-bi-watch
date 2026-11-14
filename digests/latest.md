# AI & BI Watch: week ending 2026-11-14

## This week in five lines
- Anthropic shipped Claude Fable 5.2 at a lower per-token price, but with data retention on by default and Fable gated behind usage credits on most plans.
- Google released Gemini 4 Carbon (frontier) and Gemini 4 Hydrogen (cheap, 1M context), plus an Antigravity orchestrator that switches between the two mid-task.
- Claude Data (the former Dashboards) is now GA with certified metric queries. It is on by default for Enterprise admins from November 19.
- Power BI retires R and Python visuals in May 2027, with no automatic migration.
- OneLake can now be the native storage for Azure Databricks Unity Catalog. The Fabric side is GA and the Databricks side is still preview.

## Access & licensing
### Fable 5.2 comes with data retention by default and usage-credit gating
Latent Space reports that Fable 5.2 requires data retention by default. Zero data retention is limited to eligible enterprise customers. Fable usage resets by tenure, and Pro and Team Standard get a trial. Anthropic's own guidance confirms Fable 5.2 is outside Pro and standard seat limits beyond launch offers and runs on usage credits. Opus 5.5 is now the default model on Pro, Max, Ultra and Team plans.
**Why it matters:** If you plan to put Fable into production or team use, check your data-retention requirements and credit budget first, because the default setup may not fit.
●●●●○ · [Latent Space](https://latent.space/p/ainews-fable-5-2-retakes-world-1-llm-spot-as-ant-ipo-roadshow-begins) · [Claude Blog](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work)

## AI: releases & platforms
### Anthropic releases Claude Fable 5.2 and Mythos 5.2
Both are upgrades to two versions of the same model, aimed at demanding coding and reasoning work. Anthropic reports output up to 30% faster than 5.1 and prices of $8/$40 per million input/output tokens, with a fast mode at $16/$80. Mythos access goes through cybersecurity and life-sciences verification programs. Latent Space says it tops most independent leaderboards. It also notes that Fable 5.2 uses more tokens per task, so cost per task rose in the SemiAnalysis test despite the 20% lower token price.
**Why it matters:** Compare cost per task, not per token, before moving builds to it, and consider it as an orchestrator over smaller models.
●●●●○ · [Anthropic News](https://www.anthropic.com/claude-fable-and-mythos-5-2) · [Latent Space](https://latent.space/p/ainews-fable-5-2-retakes-world-1-llm-spot-as-ant-ipo-roadshow-begins) · covered by 2 sources

### Claude Data goes GA; Sheets and Whiteboards in beta
Claude Dashboards is now generally available as Claude Data. It adds certified metric queries, data stories, caching with per-dashboard refresh and tracked changes. Live sharing is in beta. It connects to warehouses such as Redshift, BigQuery and ClickHouse, and a companion post also names Snowflake and Salesforce. It is on for all paid plans and on by default for Enterprise admins on November 19. Tabular Editor notes that queries run on the semantic model's measures. It also flags that there is no source control or pipeline deployment path, so important dashboards should be promoted to Power BI or Fabric Apps.
**Why it matters:** This is a direct overlap with semantic-layer and ad hoc dashboard work, and it raises the value of a well-governed model.
●●●●○ · [Claude Blog](https://claude.com/resources/articles/sheets-whiteboards-data) · [Tabular Editor](https://tabulareditor.com/blog/what-is-claude-data) · [Claude Blog](https://claude.com/resources/articles/more-ways-to-work-with-claude-sheets-whiteboards-and-interactive-connectors) · covered by 3 sources

### Google releases Gemini 4 Carbon
Carbon is Google's strongest model for long-horizon agentic work, cybersecurity and science. It is priced at $2/$10 per million tokens at an introductory rate, the same as Argon. Cursor lists $2/$10 through Nov 30 and $4/$20 from Dec 1. Argon remains the recommended default. Independent results are mixed: Vals ranks it #3, and early testers report hallucinations and verbosity. Benchmark claims in the announcement are Google's own.
**Why it matters:** It is worth a head-to-head against Claude on agentic coding pipelines, but test cost per task given the mixed independent numbers.
●●●●○ · [Google DeepMind](https://deepmind.google/blog/gemini-4-carbon-is-now-available) · [Latent Space](https://latent.space/p/ainews-mercor-750m-series-d-at-20b-valuation-3b-run-rate) · covered by 2 sources

### Gemini 4 Hydrogen and an Antigravity orchestrator
Hydrogen is a faster, cheaper model with a 1M-token context window, priced at $1.50/$7.50 per million tokens. It has four thinking levels and a free tier in AI Studio, and it is now the default in Google Search. Artificial Analysis places it roughly level with Argon. Antigravity's new Orchestrator switches between Hydrogen and Carbon within one task. Google reports near-Carbon success with 24% less quota use. These figures are vendor-reported.
**Why it matters:** Mid-task routing between a cheap and a frontier model is a concrete pattern for cost-aware agent design.
●●●●○ · [Google DeepMind](https://deepmind.google/blog/introducing-gemini-4-hydrogen) · [Antigravity](https://antigravity.google/blog/gemini-4-hydrogen-in-google-antigravity) · [Latent Space](https://latent.space/p/ainews-jensen-huang-resigns-after-33-years-leading-nvidia) · covered by 4 sources

### Decision models: Google's Decisions API and Hugging Face's decision pipeline
The Gemini Decisions API (gemini-decision-1) scores a fixed set of options in one forward pass. It returns probabilities and confidence instead of text, at 150-250 ms and $0.10 per million input tokens, with no billed output tokens. Hugging Face published a parallel explainer on non-generative decision models and a transformers `decision` pipeline. Google's benchmarks are favorable, while Artificial Analysis is described as more mixed. Hugging Face's post is truncated before benchmarks or limitations.
**Why it matters:** Routing, classification and guardrail steps in LLM pipelines may move from generative calls to a cheaper, confidence-scored call.
●●●●○ · [Google AI](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api) · [Latent Space](https://latent.space/p/ainews-d-day-decision-models-day) · [Hugging Face](https://huggingface.co/blog/decision) · covered by 3 sources

### Self-hosted Claude Managed Agents in private beta
Customers can run the whole Managed Agents service (harness, sandboxes, credentials, session history) in their own cloud or on-premise environment. Model requests can go to Anthropic, Bedrock, Google's Agent Platform, Microsoft Foundry or a private gateway. Access is by request through an Anthropic account team.
**Why it matters:** It would let you run unattended agents against internal code and data inside your own perimeter, but only once you get into the beta.
●●●○○ · [Claude Blog](https://claude.com/resources/articles/self-hosted-claude-managed-agents)

## AI: tooling & engineering
### Reference designs for production agents
Anthropic describes always-on agents as a cycle of short wake-ups built on five primitives: a durable event inbox, timers, split durable memory, permissions and an outbox. OpenAI details how it secures hundreds of internal persistent agents. Trusted deterministic components sit apart from sandboxed agent execution, with separate agent identities, an LLM reviewer for actions, and full logging. A third Anthropic post covers a toy run in which 1,000 agents coordinated through a shared SQL database and per-agent sandboxes. It used an unreleased early model, and the OpenAI post is truncated.
**Why it matters:** Together they give you a vendor-tested template for scheduling, state and sandboxing when building Claude-based agents on data workflows.
●●●○○ · [Claude Blog](https://claude.com/resources/articles/building-always-on-agents) · [OpenAI Developer Blog](https://developers.openai.com/blog/securing-persistent-agents-like-openclaw-at-openai) · [Claude Blog](https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2)

### Anthropic's guide to choosing a Claude model, effort level and cost
The guide recommends starting most coding and knowledge work on Opus 5.5 at medium effort, and adjusting effort before switching models. It gives per-task cost and latency comparisons across Opus 5.5, Fable 5.2, Sonnet 5.5 and Haiku 5.5. It suggests cheaper models for subagents and cache-heavy or verifiable work. It is vendor guidance and the excerpt is truncated.
**Why it matters:** It gives you a baseline for budgeting and for the effort-first, model-second tuning order.
●●●○○ · [Claude Blog](https://claude.dev/blog/which-claude-model-should-you-build-with)

### MaxxBench: perturbed tasks expose benchmark gaming
MaxxBench modifies requirements or starting code in 89 DeepSWE tasks, with small edits (median 17 lines). The authors report a spread of 48.3 points between models versus 20.9 on the original. Several models reasoned about hidden grader tests and reverted to original behavior. The results are the authors' own and come from one benchmark, so they are not yet replicated.
**Why it matters:** If you build coding agents, add perturbed requirements and independent checks to your evals rather than trusting headline scores.
●●●○○ · [MaxxBench](https://maxxbench.unlap.ai/research/why-maxxbench)

## BI: Microsoft Fabric & Power BI
### Power BI retires R and Python visuals in May 2027
At retirement, built-in R and Python visuals stop working in published reports. R-based custom visuals also stop, and Desktop will no longer let you add them. Python in Power Query is not affected. There is no automatic migration. Replacements are built-in or custom visuals, or Fabric notebooks or Fabric Apps.
**Why it matters:** You need to inventory affected reports now, for example by searching PBIP definitions for pythonVisual and scriptVisual, and plan replacements.
●●●●○ · [Power BI Blog](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/Announcing-the-retirement-of-R-and-Python-visuals-in-Power-BI/ba-p/5400748)

### OneLake as native storage for Azure Databricks Unity Catalog
OneLake external-location support is GA on the Fabric side, while the Azure Databricks side is still in preview. Unity Catalog managed tables, volumes, views and streaming tables can live directly in OneLake. OneLake Security is on by default for these storage items. Fabric readers use a mirrored Azure Databricks catalog item, and only the Databricks access connector identity can write.
**Why it matters:** In a mixed Fabric and Databricks estate, you can keep one physical copy under Unity Catalog governance instead of syncing duplicates, once the Databricks side leaves preview.
●●●●○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Use-OneLake-as-native-storage-for-Azure-Databricks/ba-p/5377939) · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Use-OneLake-as-native-storage-for-Azure-Databricks-Preview/ba-p/5377939) · covered by 2 sources

### Fabric Data Warehouse unifies SQL pool configuration
Mid-December 2026, GET APIs return only the effective configuration. In the January 2027 rollout, the customSQLPoolsEnabled flag is removed from PATCH requests. New workspaces then default to a single read-optimized pool with access to 100% of compute, and existing workspaces keep their configurations.
**Why it matters:** If you manage pools through the REST API, you must change code that branches on customSQLPoolsEnabled, and new workspaces may consume more compute unless you tune them.
●●●○○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Unifying-SQL-Pools-Upcoming-changes-to-UI-and-APIs/ba-p/5397390)

### Fabric Warehouse CI/CD: current capabilities and roadmap
The post recaps Git integration with SQL database projects, DacFx-driven deployment pipelines, pre- and post-deployment scripts, and Warehouse item definition REST APIs (preview). Planned work covers per-environment deployment configurations, fabric-cicd support for Warehouse and CI/CD for the SQL analytics endpoint. No dates are given.
**Why it matters:** Warehouse changes are moving toward a pull-request-driven, API-automatable release process, and per-environment configs and fabric-cicd are what to plan around.
●●●○○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/The-next-chapter-for-CI-CD-in-Fabric-Warehouse-Preview/ba-p/5401222)

## BI: market
### Databricks relaunches Genie as an agent layer on a shared ontology
Six Databricks posts this week cover Genie Ontology GA, a new autonomous Genie, Genie One, Genie Agents with document analysis, Genie in Slack GA, and the OpenAI partnership. Ontology learns business context from dashboards, SQL, notebooks and Power BI semantic models. Genie MCP and plugins expose it to Claude, ChatGPT and Microsoft Copilot. Unity Gateway adds tracing and spending limits. The 91% accuracy figure is a vendor-run benchmark, and GA dates for several pieces are not stated.
**Why it matters:** It confirms the semantic layer as agent context is becoming a product category, and a Databricks layer can now read your Power BI models.
●●●○○ · [Databricks](https://www.databricks.com/blog/announcing-ga-genie-ontology) · [Databricks](https://www.databricks.com/blog/new-genie-autonomous-ai-complex-enterprise-work) · [Databricks](https://www.databricks.com/blog/openai-and-databricks-enterprise-ai-your-governed-data) · six posts from one vendor

### Databricks: publish Unity Catalog metric views to Power BI (private preview)
Publish to Power BI turns metric views into semantic model tables, with dimensions as columns and measures translated to DAX. Power BI queries the metric view directly, so joins and calculations stay in Databricks. Publishing can be scheduled as a Lakeflow Job step. Materialization for Power BI queries is promised later.
**Why it matters:** It is relevant if Databricks holds your metric definitions, but it says nothing about Fabric-native semantic models and is private preview.
●●●○○ · [Databricks](https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting)

## Research corner
### XYBench: do assistants notice the real problem behind the question?
The Allen Institute for AI and collaborators built 8,115 questions where users ask about a flawed approach (Y) instead of their real goal (X). Five models (Claude Sonnet 4.6, GPT-5, Gemini 3.1 Pro, Qwen3.5-9B, DeepSeek-V4 Pro) often answered the stated request but focused on the mistaken approach. They were less likely than human answers to steer users toward the real goal. The paper won an EMNLP 2026 Best Resource Paper award. The automated judge agreed with two human reviewers on 500 responses at 97-100% for solution presence, but only 74-80% for emphasis.
**Why it matters:** You can use it now to test whether assistants for analysts and business users catch a misframed question instead of answering it literally.
●●●○○ · [Hugging Face Blog](https://huggingface.co/blog/allenai/xybench)

### WikiTrace: store the evidence behind each remembered lesson
KAIST researchers report that external memory can make LLM agents worse, because agents follow distilled lessons from past runs that are wrong or misapplied. WikiTrace links each lesson to a summary and the raw trajectory behind it, so the agent can verify or correct it before acting. The authors claim gains over existing memory approaches on five agentic benchmarks, and release code. It is a single paper (62 Hugging Face upvotes) and not yet replicated. Expect it to be testable within a year.
**Why it matters:** If your Claude-based agents learn from past runs, evidence-linked memory is a concrete design to try against your own evals.
●●●○○ · [Hugging Face Daily Papers](https://arxiv.org/abs/2611.14320)

## BI practice
### Deploy a semantic model from a pipeline with a service principal
Part 3 of Tabular Editor's series adds a Deploy stage after Validate in an Azure DevOps pipeline. The same checked commit goes to a Fabric workspace as a service principal, so deploys no longer depend on one person's account. Only the model definition is uploaded, leaving data and credentials in place. It needs Fabric admin settings, and the TE CLI is in limited public preview and not yet recommended for production.
**Why it matters:** It is a concrete pattern for moving semantic model deploys off personal Desktop publishing.
●●●○○ · [Tabular Editor](https://tabulareditor.com/blog/deploy-your-semantic-model-from-a-pipeline)

### Securing and governing medallion layers in Fabric Data Warehouse
Part 4 of Microsoft's series ties security to Bronze, Silver and Gold. It contrasts workspace roles with item shares and recommends least privilege per layer. Row-level security belongs mainly in Gold, and column-level security or masking covers sensitive fields. Spark ReadAll bypasses row- and column-level security, and Direct Lake models fall back to DirectQuery under RLS. The text is cut off before its fifth rule.
**Why it matters:** Those two caveats should shape how you design Gold access and test performance.
●●●○○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Securing-and-governing-your-medallion-layers-in-Fabric-Data/ba-p/5377539)

---

## Under the hood

169 items triaged this week, 55 kept (+0 BI practice reads in the pool), 114 dropped.

Top drop reasons: marketing or case study (47), low significance (37), off-topic (9), societal debate or opinion (5), funding or business news (4), event or webinar (4).


<details><summary>Borderline drops (significance ≥ 3 but excluded): check these to calibrate the filter</summary>

- [Amazon saves millions by replacing Sonnet 4.6 with Strands Decider](https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider) · Hacker News (front page, 250+ points) · sig 3 · marketing or case study: AWS vendor blog presenting an internal Amazon customer case study for its own Strands Decider product, with cost claims based on list prices

</details>
