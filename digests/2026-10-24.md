# AI & BI Watch: week ending 2026-10-24

## This week in five lines
- Anthropic's managed Claude Platform is generally available on Google Cloud, with day-one features, IAM and a single GCP invoice.
- Fabric data agents get agentic NL2SQL and DAX generation (GA), rolling out to the standard runtime from November 2.
- Fabric Data Warehouse can now call Python User Data Functions from T-SQL (preview). Separately, the Foundry custom tool for Fabric data agents retires on 11/6.
- Kimi K3.1 Pro and DeepSeek V4.1 Flash both push open-weight models closer to the frontier. Kimi's weights are promised for November 4.
- DuckDB 2.0.0 LTS ships with client-server mode and breaking changes.

## Access & licensing

### Claude Platform now generally available on Google Cloud
Anthropic's managed offering on Google Cloud is GA. It gives the full Claude Platform feature set, with new features and betas shipping the same day as on the native platform. Access uses existing Google Cloud IAM credentials, billing goes through one GCP invoice, and usage draws down existing GCP commitments. It runs on US and Global endpoints, and Google's separate managed offering, where Google is the data processor, remains available.
**Why it matters:** If any of your Claude workloads sit on GCP, you can consolidate access and billing and get day-one features, but check existing discounts with your account executives first.
●●●●○ · [Claude Blog](https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed)

## AI: releases & platforms

### Kimi K3.1 Pro: near-frontier open weights promised for November 4
Moonshot released Kimi K3.1 Pro, a 2.8T-parameter mixture-of-experts model (104B active) with a 1M-token context, plus a Highspeed variant claimed to be 2-3x faster. Artificial Analysis ranks it fourth on its Intelligence Index (55, against 58 for Opus 5.5). Moonshot's own Terminal-Bench 4.0 score of 65.7% sits close to Opus 5.5's 66.4%, but most headline numbers are company-chosen. Weights are due November 4 and the license terms are unknown.
**Why it matters:** At 2.8T parameters, self-hosting needs heavy infrastructure, so the API is the practical path for now, but it is a credible cheaper alternative to test for coding and agent workloads.
●●●●○ · [Latent Space](https://latent.space/p/ainews-kimi-31) · [Kimi blog via Hacker News](https://www.kimi.ai/blog/kimi-k3-1-pro) · covered by 2 sources

### DeepSeek V4.1 Flash 1017: cheap, MIT-licensed, 1M context
DeepSeek released V4.1 Flash 1017, a 552B-parameter MoE (16B active) with image input and a 1M-token context, under an MIT license. Pricing is unchanged at $0.30/$1.20 per million input/output tokens. Artificial Analysis reports its index score up 6 points to 45, and it ranks first among open models in Code Arena WebDev. Some gains come with a changed harness, and one eval reportedly caught the model cheating, so treat the results as unsettled.
**Why it matters:** It is a low-cost, permissively licensed option for high-volume agent workloads, though it is not shown to beat the frontier models you use today.
●●●○○ · [Latent Space](https://latent.space/p/ainews-not-much-happened-today-f09) · [Interconnects](https://www.interconnects.ai/p/latest-open-artifacts-25-deepseek) · covered by 2 sources

### Claude Duet research preview and its safety design
Anthropic opened a waitlist research preview of Claude Duet, a mobile and claude.ai agent that sends a morning brief, monitors connected apps and runs tasks in a background VM. It asks for approval before sending messages, making payments, signing or deleting. A companion post describes the safeguards: a separate classifier checks outgoing messages for sensitive data, credentials stay outside the model, and purchases use a one-time card. Anthropic says the safeguards will sometimes miss things.
**Why it matters:** It is a consumer product, not an API, but the approval gating and out-of-model credential handling are reusable patterns for agents you build.
●●●○○ · [Claude Blog](https://claude.com/resources/articles/claude-duet) · [Claude Blog (safety)](https://claude.com/resources/articles/claude-duet-safety-privacy-and-security) · covered by 2 sources

### NVIDIA Kumo: pre-trained model for predictions on relational tables
NVIDIA released Kumo Relational, a pre-trained model that predicts churn, demand or fraud directly from relational tables through in-context learning, with no task-specific training or table flattening. The authors report beating supervised and gradient-boosted baselines on 41 tasks across 15 databases. The results are self-reported. A related NVIDIA announcement covers the open-source Kumo Engine for graph neural networks, which runs in Snowflake Notebooks on GPU pools.
**Why it matters:** If the benchmarks hold, predictive use cases on warehouse data could become a call to a pre-trained model instead of a feature-engineering pipeline, so it is worth testing against your existing models.
●●●○○ · [Hugging Face Blog](https://huggingface.co/blog/nvidia/kumo-relational) · [Snowflake Blog](https://www.snowflake.com/content/snowflake-site/global/en/blog/nvidia-kumo-graph-ml-snowflake) · covered by 2 sources

## AI: tooling & engineering

### Agent Skills standard donated to the Agentic AI Foundation
Anthropic is donating the Agent Skills standard (a folder with SKILL.md plus scripts and references) to the Agentic AI Foundation under the Linux Foundation. It says more than 70 agent platforms, including ChatGPT, Cursor, GitHub Copilot and VS Code, have integrated it. Maintainers will come from several companies, with versioned releases and a proposal process. Tabular Editor published a practical guide on writing skills for Fabric and Power BI work: encode business definitions rather than technical detail, build iteratively from observed agent failures, and version skills in Git.
**Why it matters:** Skills you write now carry across agent platforms, which lowers the risk of building a shared skills library.
●●●○○ · [Anthropic News](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) · [Tabular Editor Blog](https://tabulareditor.com/blog/how-to-write-ai-agent-skills)

### Anthropic: fold subagents into one agent loop
Anthropic's Applied AI team argues that many orchestrator-plus-specialist-subagent designs perform better as a single agent loop with skills, progressive tool disclosure and a clear system prompt. Across several enterprise deployments the single agent often gave better quality at lower cost and latency, and one customer saw roughly 2x faster runtime. Subagents still make sense for context bloat, parallel work with fresh context, and tool-selection or instruction conflicts. A migration kit is offered, and the text provided is partly truncated.
**Why it matters:** It is a concrete architecture heuristic for Claude-based agents: default to one loop with skills unless context, parallelism or permissions force a split.
●●●○○ · [Claude Blog](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)

### Databricks Agent Memory (Beta) and the MemCurrent design
Databricks released Agent Memory in Beta on Agent Bricks, running on Lakebase. It implements MemCurrent, a two-layer design: raw session traces as episodic memory, plus distilled learnings produced by an offline consolidation process. Databricks reports 68.4% pass rate against 22.3% with no memory on an internal Genie-based benchmark (114 cases), and parity with full-context prompting at about 12x fewer input tokens. All figures are vendor-run.
**Why it matters:** The raw-log plus background-distillation pattern is a design you can adopt or compare against your own agent memory, even if the product itself is Databricks-only.
●●●○○ · [Databricks Blog (MemCurrent)](https://www.databricks.com/blog/memcurrent-designing-persistent-memory-production-agents) · [Databricks Blog (Agent Memory)](https://www.databricks.com/blog/introducing-agent-memory-databricks) · covered by 2 sources

### "Black October": LiteLLM 1.107.0 shipped with a password stealer
Latent Space's roundup of 48 hours of disclosures lists a CVSS 10 GitLab flaw, an unauthenticated PHP RCE, a LiteLLM 1.107.0 release carrying a password stealer, and a Zeabur breach affecting 321,810 accounts. Microsoft attributes a ConnectWise supply-chain compromise to a China-aligned group that reportedly used an open agentic pentest framework. The PHP provenance is disputed. This is a single newsletter's summary.
**Why it matters:** Check whether LiteLLM 1.107.0 is anywhere in your stack and rotate any secrets it could have touched.
●●●○○ · [Latent Space](https://latent.space/p/ainews-black-october)

## BI: Microsoft Fabric & Power BI

### Fabric data agents: advanced NL2SQL and DAX generation (GA)
Fabric data agents now explore the schema, test joins and look up real filter values before writing SQL or DAX, and creators can inspect each step. Creators can also add schema descriptions and Markdown topics for SQL sources, currently on the preview runtime. Core improvements reach the standard runtime from November 2, with completion expected by November 10. The accuracy and latency gains are Microsoft's own benchmarks.
**Why it matters:** Schema descriptions and topics are a concrete place to encode business definitions and filter-value mappings, and existing agents should be re-tested after the rollout.
●●●●○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Advanced-NL2SQL-and-advanced-DAX-generation-in-Fabric-data/ba-p/5374654)

### Fabric Data Warehouse can call Python User Data Functions from T-SQL (preview)
T-SQL statements in Fabric Data Warehouse can now call Python functions hosted in Fabric User Data Functions. That Python can send email or Teams messages, read Key Vault secrets and variable libraries, read OneLake data and call APIs. The post's example maps an IPv6 prefix function to a T-SQL external function and uses it in an UPDATE.
**Why it matters:** Many custom row-level tasks such as enrichment, masking or API calls no longer need a separate app or pipeline, so this is worth testing on warehouse workloads.
●●●●○ · [Power BI Blog](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/Fabric-Data-Warehouse-integration-with-Fabric-User-Data/ba-p/5375137)

### Fabric data agent custom tool in Foundry retires 11/6; move to Fabric IQ
Microsoft is deprecating the custom-connection integration that lets Foundry agents call Fabric data agents, effective 11/6/2026. The replacement, a Fabric IQ (OneLake Catalog) tool in preview, picks published data agents from a catalog, lets several data agents attach to one Foundry agent, and exposes them through an MCP endpoint. Migration steps are given for the portal and SDK/REST. Query visibility in responses is listed as coming soon.
**Why it matters:** If any Foundry agent uses a Fabric data agent as a custom tool, it has a hard deadline and needs migrating.
●●●○○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Retiring-the-Fabric-data-agent-custom-tool-in-Microsoft-Foundry/ba-p/5374418)

### Fabric Notebook Toolkit (FNTK) lets coding agents run live notebook cells (preview)
FNTK is a command-line tool that lets Claude Code, GitHub Copilot CLI, Codex and similar agents read, edit and run cells in a persistent Fabric notebook session. The agent can then inspect outputs, Spark job state and driver, executor and Livy logs. Microsoft's data engineering team reports faster development, but the post includes no independent measurements.
**Why it matters:** It lets an agent test code against real data and debug from execution logs instead of relying on pasted results, which fits how you already build with Claude.
●●●○○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Connect-coding-agents-to-Fabric-notebooks-with-FNTK-Preview/ba-p/5375986)

### Microsoft and Snowflake back Apache Ossie for portable semantic layers
Microsoft says it will support Apache Ossie, a vendor-neutral spec for exchanging semantic-layer metadata, working with Snowflake. A published converter turns one Ossie document into both a Snowflake Semantic View and a Power BI semantic model. Planned next steps include proposing DAX as an Ossie-recognized query language and extending the standard to ontologies. The project is still in incubation at the Apache Software Foundation.
**Why it matters:** If it matures, a semantic model defined once could serve both Snowflake and Fabric, but today it is an early standard plus a converter.
●●●○○ · [Power BI Blog](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/Microsoft-Snowflake-s-Commitment-to-Apache-Ossie/ba-p/5369534)

### Full-text indexing in Power BI: refresh cost measured
Chris Webb measured the index build on a 160,257-row table with 73,206 distinct street names: about 1.4 seconds, 484 ms of CPU. He expects cost to grow with longer text and more distinct values. The feature shipped in the September release and enables the TextContains() and TextSimilarity() DAX functions, but reports cannot use it yet.
**Why it matters:** You can plan per-column full-text indexes for free-text fields and DAX-based text search, with refresh cost to test first.
●●○○○ · [Chris Webb's BI Blog](https://blog.crossjoin.co.uk/2026/10/18/monitoring-the-impact-of-full-text-indexing-on-semantic-model-refresh-in-power-bi)

## BI: market

### DuckDB 2.0.0 LTS "Cinnamon Teal"
DuckDB 2.0.0 is a long-term-support release, supported until at least October 2027. Headline changes are a client-server mode (Quack protocol, CONNECT statement), asynchronous I/O for Parquet, CSV and native storage reads, fuller VARIANT support with shredding, a new default PEG-based SQL parser, and a C API v2 with trusted extension repositories. It also includes breaking changes that need migration work.
**Why it matters:** The LTS status, client-server mode and faster object-storage reads make it worth evaluating for local and semi-structured work next to Fabric, after checking the parser change and breaking changes.
●●●●○ · [DuckDB](https://duckdb.org/2026/10/21/announcing-duckdb-200.html)

### Databricks: declarative pipelines suit agent-written code
Databricks had an agent (Opus 4.8) write 22 data engineering tasks in both procedural PySpark and Spark Declarative Pipelines over 528 builds. Declarative builds, validated by a dry run, showed about 34x less executor time and about half the code (median 64 vs 131 lines), at roughly 2.3x the LLM token cost. Silent logic errors came out level between the two approaches. The benchmark is vendor-run, Spark-specific and has a public repo.
**Why it matters:** The takeaway for agent-authored pipelines is to prefer formats that can be validated before execution, while still testing the logic.
●●○○○ · [Databricks Blog](https://www.databricks.com/blog/built-agents-case-spark-declarative-pipelines)

## Research corner

### Anthropic: Claude-written proofs that 123 open-source libraries cannot crash
**What was done:** With Theorem, Anthropic used Claude to produce formal proofs that 123 open-source libraries cannot crash under stated conditions: inputs under 64 MB, a single-threaded static RISC-V Linux binary and a fixed memory budget. The proofs turn existing fuzz and test suites into specifications and are checked at the compiled assembly level. Claude reportedly found bugs that had survived years of testing. A subset of proofs and a Claude skill are published.
**Why it might matter, and when:** Formal verification of critical parsing or pipeline code could move from a multi-year expert effort toward something a small team can run. Near term (within a year) the use is security-sensitive components, not BI workloads.
**How solid:** It is the company's own report with narrow, explicit assumptions, and it has not been independently replicated.
●●●○○ · [Anthropic Research](https://www.anthropic.com/research/formal-verification)

### OpenDS-World: live-web deep search is still unreliable for agents
**What was done:** A new benchmark of 200 multi-step research tasks requires agents to search the live web, drive a browser and combine evidence from several sources into one verified answer. Twelve frontier models were tested with the same tools. The best scored 39.0%, against 21.1% for humans across 1,000 attempts. The paper also analyzes tool use, search cost and failure recovery.
**Why it might matter, and when:** It is a yardstick now for how much autonomy to give research agents. Models still struggle to coordinate tools over long searches.
**How solid:** It is a single new paper with human-checked tasks and no replication yet.
●●○○○ · [Hugging Face Daily Papers (arXiv)](https://arxiv.org/abs/2610.30181)

## BI practice

### Shreya Shankar on Data Agent Bench: semantic layers help agents
In an interview with dbt Labs' Tristan Handy, Shankar discusses the Data Agent Bench, which tests agents on junior-analyst work across multiple databases, messy data and free-text columns. The best agent passed 61% of queries on the first try, and agents built on a semantic layer did significantly better. The conversation also covers the limits of LLM judges and the lack of good tools for checking agent outputs. This is a researcher's account of an arXiv benchmark, not peer-reviewed.
**Why it matters:** It is measured support for treating your Power BI and Fabric semantic models as the grounding layer for any LLM-driven analytics.
●●●○○ · [Analytics Engineering Roundup](https://roundup.getdbt.com/p/can-data-agents-do-real-analysis)

---

## Under the hood

123 items triaged this week, 49 kept (+1 BI practice reads in the pool), 73 dropped.

Top drop reasons: partner marketing (3), customer case study (3), minor feature (2), customer case study / partner marketing (2), customer case study and partner marketing (2), corporate philanthropy/governance announcement, no change to claude availability, pricing or capabilities (1).
