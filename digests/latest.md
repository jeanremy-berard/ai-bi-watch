# AI & BI Watch: week ending 2026-10-31

## This week in five lines
- Claude Code for VS Code versions 2.1.312 and 2.1.313, distributed via the Cursor Marketplace, carried a backdoor. Check any Cursor installs now.
- OpenAI and Anthropic API price cuts since June, mostly on cache reads, lower agentic coding costs by an estimated 40-75%.
- Gemini 4 Carbon, Mistral Large 4 (open weights) and Kimi K3.1 Pro (weights due Nov 4) all landed, but only Mistral's weights are downloadable today.
- Fabric data agents get agentic NL2SQL/DAX generation, rolling out to the standard runtime from Nov 2. Re-test existing agents.
- The Fabric data agent custom tool in Foundry is retired on Nov 6. Move to the Fabric IQ (OneLake Catalog) tool.

## Access & licensing
### LLM API prices have fallen sharply since June, driven by cache-read cuts
One author tracked OpenAI and Anthropic price changes between June and September. Anthropic made Sonnet 5's launch price permanent, halved Opus 5.5 relative to Opus 5, and cut cache-read costs on Fable 5.1 by 75%. OpenAI cut GPT-5.6 Luna by 80% and halved cache-read pricing on GPT-6.1 Sol. The author argues cache reads dominate agentic coding spend, so total costs drop roughly 40-75%, and attributes this to competition from cheaper open-weight models. This is one analyst's tally, not an official source.
**Why it matters:** Cheaper cache reads change which agent workloads are affordable on Claude and what budgets you should assume.
●●●●○ · [minimaxir](https://minimaxir.com/2026/10/cheap-llms)

### Claude Platform is generally available on Google Cloud, Anthropic-managed
The full Claude Platform is now available on Google Cloud with new features shipping the same day as on the native platform. It uses Google Cloud IAM credentials, bills on a single GCP invoice and draws down existing GCP commitments. It is on US and Global endpoints only, and Google's separate managed offering, where Google is the data processor, remains available. Check existing discounts with account executives before switching.
**Why it matters:** If any of your Claude usage runs through GCP, you can consolidate access and billing and get day-one features.
●●●○○ · [Claude Blog](https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed)

## AI: releases & platforms
### Gemini 4 Carbon announced, but access is restricted and pricing is unclear
Google says Gemini 4 Carbon ranks first on the Artificial Analysis Intelligence Index (59), with gains in coding, long-horizon agentic tasks and cybersecurity. Initial access is limited to cyber defenders and trusted partners through the Fairwind Program, with broader availability promised but undated. Google quotes $2/$10 per million tokens, while Artificial Analysis lists $4/$20 with an open-ended 50% launch discount. The benchmark figures are Google's own.
**Why it matters:** It is a frontier candidate for agentic coding evaluations, but with no developer API yet there is nothing to plan around.
●●●○○ · [Google DeepMind](https://deepmind.google/blog/gemini-4-carbon-our-next-frontier-model) · [Latent Space](https://latent.space/p/ainews-gemini-4-carbon) · [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon) · covered by 3 sources

### Mistral Large 4 ("Le Chonk") ships open weights with a 1M-token context
Mistral released an open-weight multimodal mixture-of-experts model, about 1T parameters with 49B active, aimed at coding agents and cyber defense. It has day-0 support in transformers, vLLM and llama.cpp, and three selectable reasoning modes. Benchmarks are vendor-reported. The Mistral Ecosystem Open-Weight License is an MIT derivative that requires a separate commercial license for model-as-a-service businesses.
**Why it matters:** It is a self-hostable coding-agent option, but it needs your own evals before it substitutes for Claude, and the license limits hosted offerings.
●●●○○ · [Hugging Face](https://huggingface.co/blog/mistral-large4) · [Mistral AI](https://mistral.ai/news/mistral-large-4-oss) · [Latent Space](https://latent.space/p/ainews-building-aie-code-the-top-coding-agent-conference) · covered by 3 sources

### Kimi K3.1 Pro launches via API, weights promised for November 4
Moonshot's K3.1 Pro is a 2.8T-parameter mixture-of-experts model (104B active) with a 1M-token context and a Highspeed variant claimed to be 2-3x faster. Artificial Analysis puts it fourth on its index, behind Opus 5.5, and Moonshot's own Terminal-Bench 4.0 score is close to Opus 5.5's. Weights are promised for Nov 4 and license terms are unknown.
**Why it matters:** A near-frontier open-weight model could become an alternative for agent workloads, but at this size the API is the practical route.
●●●○○ · [Latent Space](https://latent.space/p/ainews-kimi-31) · [Kimi](https://www.kimi.ai/blog/kimi-k3-1-pro) · covered by 2 sources

### Claude Duet research preview: a proactive background agent
Duet is a mobile and web agent that sends a morning brief, monitors connected apps and runs tasks in a background VM. It asks for approval before sending messages, making payments, signing or deleting. Anthropic's safety write-up describes an outgoing-message classifier, credentials kept away from the model and a one-time card for purchases, and admits the safeguards will sometimes miss. It is a waitlist preview on Pro and Max plans, not an API.
**Why it matters:** The approval gating and credential-proxy design are a concrete reference for agents you build yourself.
●●●○○ · [Claude Blog](https://claude.com/resources/articles/claude-duet) · [Claude Blog (safety)](https://claude.com/resources/articles/claude-duet-safety-privacy-and-security) · covered by 2 sources

## AI: tooling & engineering
### Foundry Agent Service gets a managed Copilot harness (public preview)
Microsoft runs the agent loop and sandbox. Developers supply skills, MCP and Foundry tools with configured approvals, and built-in subagents. Long-running resilience for hosted agents is now GA: Foundry restarts interrupted work, but your application must save checkpoints and avoid duplicate actions.
**Why it matters:** It could replace much of the orchestration code you would otherwise write for agents on the Microsoft side, though it is still preview.
●●●●○ · [Azure Blog](https://devblogs.microsoft.com/foundry/microsoft-copilot-harness-in-foundry)

### Claude Code extension on Cursor Marketplace was compromised
Phorion reports that the official Claude Code for VS Code bundle on the Cursor Marketplace was backdoored in versions 2.1.312 and 2.1.313, per a later Cursor notice. The payload adds an attacker SSH key, tries to enable Remote Login and a reverse SSH tunnel, and includes persistence for macOS, Linux and Windows. Cursor has removed the versions. Phorion advises reviewing environments and engaging incident response if they are found.
**Why it matters:** The extension runs with full local user permissions, so anyone using Claude Code through Cursor should check versions now.
●●●●○ · [Phorion](https://phorion.io/blog/offical-claude-code-vsx-compromise)

### Anthropic: prefer one agent loop with skills over many subagents
Anthropic's Applied AI team reports that across several enterprise deployments, a single loop with skills, progressive tool disclosure and a clear system prompt often beat orchestrator-plus-specialist designs on quality, cost and latency. One customer saw roughly 2x faster runtime. Subagents still make sense for context bloat, parallel work with fresh context, and tool-selection or instruction conflicts. A migration kit is offered. This is vendor guidance, not an independent comparison.
**Why it matters:** It gives you a concrete heuristic for when to split a Claude agent and when to fold it back.
●●●○○ · [Claude Blog](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)

### Agent Skills standard donated to the Agentic AI Foundation
Anthropic is donating the SKILL.md-based Agent Skills standard to the Linux Foundation's Agentic AI Foundation. It says more than 70 agent platforms, including ChatGPT, Cursor, GitHub Copilot and VS Code, have integrated it. Maintainers will come from several companies, with versioned releases and a proposal process planned.
**Why it matters:** Skills you write once can travel across agent platforms, which makes a shared skills library a lower-risk investment.
●●●○○ · [Anthropic News](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation)

## BI: Microsoft Fabric & Power BI
### Fabric data agents: agentic NL2SQL and DAX generation reaches GA
Before writing SQL or DAX, the agent now explores the schema, tests joins and looks up real filter values, and creators can inspect each step. Creators can add schema descriptions and Markdown topics for SQL sources (preview runtime for now). Core improvements reach the standard runtime from Nov 2, completing by Nov 10. Accuracy and latency gains come from Microsoft's own benchmarks.
**Why it matters:** Schema descriptions and topics let you encode business definitions and filter-value mappings, so re-test existing agents after the rollout.
●●●●○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Advanced-NL2SQL-and-advanced-DAX-generation-in-Fabric-data/ba-p/5374654)

### Fabric data agent custom tool in Foundry retires on Nov 6
The custom-connection integration between Foundry agents and Fabric data agents is deprecated effective 11/6/2026. The replacement, the Fabric IQ (OneLake Catalog) tool in preview, lets you pick published data agents from a catalog, attach several to one Foundry agent and reach them via an MCP endpoint. The post includes portal and SDK/REST migration steps.
**Why it matters:** Any Foundry agent using Fabric data agents as a custom tool breaks after the deadline unless migrated.
●●●○○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Retiring-the-Fabric-data-agent-custom-tool-in-Microsoft-Foundry/ba-p/5374418)

### Project Osmos: an autonomous data engineering agent in Fabric
Following Microsoft's January acquisition of Osmos, a multi-agent orchestrator investigates data, writes PySpark, runs it through the Livy API, validates results and pauses when blocked. Work runs as persistent tasks on Fabric capacity under the user's permissions, and can be started from GitHub Copilot CLI, Claude Code or Codex via the Skills for Fabric plug-in. The visible text does not state the availability stage. A separate FNTK preview lets coding agents read, edit and run cells in live Fabric notebooks.
**Why it matters:** It moves agent help from generating code to persistent, validated pipeline work, which consumes capacity and needs deliberate guardrails and review.
●●●○○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Introducing-the-data-engineering-agent-for-Fabric-Project-Osmos/ba-p/5377944) · [Fabric Blog (FNTK)](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Connect-coding-agents-to-Fabric-notebooks-with-FNTK-Preview/ba-p/5375986)

### Fabric Data Warehouse can call Python User Data Functions from T-SQL (preview)
T-SQL statements can invoke Python functions hosted in Fabric User Data Functions. That Python can send email or Teams messages, read Key Vault secrets and variable libraries, read OneLake data and call APIs. The example maps an IPv6-prefix function to a T-SQL external function used in an UPDATE.
**Why it matters:** Row-level enrichment, masking or API calls no longer need a separate app or pipeline, so it is worth testing on warehouse workloads.
●●●○○ · [Power BI Blog](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/Fabric-Data-Warehouse-integration-with-Fabric-User-Data/ba-p/5375137)

### SQLBI DAX LLM Benchmark v2: frontier models score 90-96%
SQLBI and Maxim Anatsko re-ran the single-shot benchmark on Contoso-based models, covering writing and fixing DAX measures, queries and UDFs. Frontier models from three vendors released in August and September score 90-96%, and model generation matters more than vendor. Open-source models lag but follow the same trend. Agent iteration and skills are disabled, so this measures native ability, not real-world agent performance.
**Why it matters:** Agent-drafted DAX looks dependable enough to adopt, with the author still advising that you read and validate the business logic.
●●●○○ · [SQLBI](https://www.sqlbi.com/blog/marco/2026/10/27/dax-llm-benchmark-v2) · [SQLBI (trailer)](https://www.sqlbi.com/tv/dax-llm-benchmark-v2-0-trailer) · covered by 2 sources

## BI: market
### DuckDB 2.0.0 LTS, with a built-in DuckDB adapter in dbt v2
DuckDB 2.0.0 is a long-term-support release (supported until at least October 2027). It adds a client-server mode (Quack protocol), asynchronous I/O for Parquet, CSV and native reads, fuller VARIANT support, a new default PEG-based SQL parser and C API v2. It also contains breaking changes that need migration. dbt v2 ships a built-in DuckDB adapter, so a profile change lets you run dbt builds locally and offline.
**Why it matters:** An LTS DuckDB is a safer base for local and semi-structured work next to Fabric, and a free local dbt target helps development, but check the parser and breaking changes before upgrading.
●●●○○ · [DuckDB](https://duckdb.org/2026/10/21/announcing-duckdb-200.html) · [dbt Labs](https://www.getdbt.com/blog/dbt-duckdb-warehouse-free-data-transformation) · covered by 2 sources

## Research corner
### Analysts adopted an AI agent's hidden lean on 86% of judgment calls
**What:** Anthropic ran a randomized trial with 50 professional analysts doing a causal-inference analysis with Claude Code. The agent was secretly set to favor one option on each of four analytical choices. **Result:** Analysts followed the lean 86% of the time, against about 50% by chance. 77% used the agent's arguments, yet only 15% credited the agent. **Timescale and solidity:** The finding applies now to any agent-assisted analysis. It is one company's study. The leans were deliberately strengthened, so real-world effects may be smaller, and the no-agent comparison group was small and less experienced.
**Why it matters:** Review of agent-run analyses has to cover the analytical choices, not just the code and outputs.
●●●●○ · [Anthropic Research](https://www.anthropic.com/research/agents-judgment-calls)

### LLM judges flip verdicts on small prompt changes
**What:** Ai2 tested six LLM judges (GPT-5.x and Claude models) on whether a research idea is novel, using ICLR 2026 peer reviews as labels and comparing against LLM-generated ideas. **Result:** Verdicts changed a lot with prompt, formatting or sampling. A simpler prompt dropped one judge's accuracy on AI-generated pairs from 93.5% to 40.9%. **Timescale and solidity:** The caution applies now to any LLM-as-judge eval. The generated-idea labels are weak assumptions, so strength is moderate, though the instability result is hard to ignore.
**Why it matters:** Validate judge prompts on the kind of outputs they will actually score before trusting your eval numbers.
●●●○○ · [Hugging Face Blog](https://huggingface.co/blog/allenai/novelty-bench)

## BI practice
### How Data Culture got an analytics agent from 0% to 94.7% accuracy
Opeyemi Fabiyi describes measuring an AI analytics agent before stakeholders rely on it. The method is golden questions, comparing query results rather than SQL text, and deterministic checks plus an LLM judge for the rest. On one e-commerce deployment, accuracy rose from 0% on raw tables to 94.7% as modeled dbt tables, column descriptions, business rules and verified queries were added, with the model held constant. It is a small number of client deployments, but the pipeline is open-sourced.
**Why it matters:** It is a measured case that the semantic and context layer, not the model, drove accuracy, and the evaluation approach carries over to Power BI semantic models.
●●●○○ · [dbt Labs](https://www.getdbt.com/blog/data-culture-ai-analytics-agent-trust-context)

### Bolt's 14 written rules for a growing dbt project
Silja Märdla of Bolt explained at dbt Summit 2026 how inconsistent staging and diverging answers appeared once the team passed 20 people. The rules fix the shapes of exposed tables and intermediate models, define each metric once against its source fact table, forbid shared model ownership, and enforce one-directional dependencies between vertical and horizontal teams. Non-additive metrics such as distinct counts live in separate marts. Bolt reports about six months without major issues.
**Why it matters:** The single-definition metric rule and one-way dependencies between domain projects translate directly to semantic model and workspace design in Fabric.
●●●○○ · [dbt Labs](https://www.getdbt.com/blog/dbt-project-standards-medallion-architecture)

---

## Under the hood

288 items triaged this week, 96 kept (+3 BI practice reads in the pool), 188 dropped.

Top drop reasons: marketing or case study (101), low significance (25), off-topic (19), minor feature (11), funding or business news (8), tutorial or listicle (7).


<details><summary>Borderline drops (significance ≥ 3 but excluded): check these to calibrate the filter</summary>

- [How LangChain grew self-serve analytics questions 40x by giving its AI agent layered context](https://www.getdbt.com/blog/langchain-self-serve-analytics-ai-agent-context) · dbt Labs Blog · sig 3 · marketing or case study: Customer case study from a dbt Labs blog recap of a dbt Summit talk, with product promotion for dbt Wizard CLI.
- [From Spreadsheets to DuckLake: A Data Engineer's Road to DuckDB](https://duckdb.org/2026/10/29/from-spreadsheets-to-ducklake.html) · DuckDB · sig 3 · marketing or case study: Vendor-hosted personal career story promoting DuckDB and DuckLake; the 2.0 alpha features it mentions (async I/O, dynamic ATTACH) are only reported as one practitioner's experience.

</details>
