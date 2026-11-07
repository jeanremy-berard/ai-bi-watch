# AI & BI Watch: week ending 2026-11-07

## This week in five lines
- The official Claude Code VS Code extension was backdoored on the Cursor Marketplace (v2.1.312 and v2.1.313). Check your environments.
- Fabric took several agent-oriented steps: a hosted OneLake MCP server, Iceberg writes to OneLake tables, and OneLake as native storage for Azure Databricks.
- M365 Copilot's integration with Power BI semantic models is now GA, and it avoids the old side-pane Copilot cost model.
- Anthropic put message threads in public beta on the Claude Platform. They cut time to first token on long agent sessions by about 35% at the median.
- Google shipped Gemini 4 Argon as a frontier model on the Gemini API and Google Cloud, and Moonshot open-sourced Kimi K3.1 Pro.

## Access & licensing
### Claude Code VS Code extension backdoored on the Cursor Marketplace
Phorion reports that the official Claude Code extension distributed through the Cursor Marketplace was compromised. A later Cursor notice names versions 2.1.312 and 2.1.313 as affected. The payload adds an attacker SSH key, tries to enable Remote Login and a reverse SSH tunnel, and includes persistence for macOS, Linux and Windows. Cursor has removed the affected versions, and Phorion advises reviewing environments and engaging incident response if either version is found.
**Why it matters:** The extension runs with full local user permissions, so any team using Claude Code through Cursor should check for these versions now.
●●●●● · [Phorion](https://phorion.io/blog/offical-claude-code-vsx-compromise)

## AI: releases & platforms
### Gemini 4 Argon is available; Carbon is still in restricted testing
Google rolled out Gemini 4 Argon, a frontier reasoning model aimed at complex coding, financial analysis and legal workflows. It is available in Google AI Studio, the Gemini API, Google Cloud, Search and the Gemini app. Two weeks later Google announced Gemini 4 Carbon, positioned for long-horizon engineering and cybersecurity. Carbon is so far only in pre-release testing with the U.S. government and selected cyber defenders. The source is Google's own monthly roundup.
**Why it matters:** Argon is a new model option to evaluate next to Claude for LLM-based builds, while Carbon is not yet usable.
●●●●○ · [Google (The Keyword)](https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-october-2026)

### Claude Platform: message threads in public beta
With threads, agents send only the new messages and the previous response ID each turn instead of resending the whole conversation. Anthropic reports a median time-to-first-token drop of about 35% for 500k to 1M token requests in Claude Code, where the feature is on by default for most users. Token usage is unchanged because Claude still reads the full conversation, and a thread expires 5 minutes after its last request.
**Why it matters:** Long-running Claude agents can cut latency without changing prompts, but you need to handle the 5-minute expiry and the cost stays the same.
●●●●○ · [Claude Blog](https://claude.com/resources/articles/message-threads)

### Kimi K3.1 Pro open weights
Moonshot released the weights of Kimi K3.1 Pro on Hugging Face. It is an open-weight, natively multimodal agentic model in the 3T-parameter class with a 1M-token context window. It is post-trained from K3 with large-scale reinforcement learning and swaps full-attention layers for Gated DeepSeek Sparse Attention. Latent Space reports it is already hosted on Ollama Cloud and Databricks, and that it ranks first among open models on Agent Arena, one independent ranking. The other performance claims are vendor-reported.
**Why it matters:** It is a self-hostable or cheaper-hosted alternative to evaluate against Claude for agentic coding and long-context work.
●●●●○ · [Hugging Face](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) · [Latent Space](https://latent.space/p/ainews-it-s-swapping-season) · covered by 2 sources

### Mistral Large 4 and an expanded Studio platform
Mistral announced Large 4 ("Le Chonk"), an open model aimed at coding, defensive cybersecurity and document reasoning. It also expanded Studio with managed agents and apps, workflow triggers, enterprise context, observability and evaluations. Studio can run in the cloud, a customer VPC, on-premises or a mix. The performance claims are the vendor's own.
**Why it matters:** It adds a self-hostable model and a platform for running agents with tracing and evals inside your own perimeter.
●●●○○ · [Mistral AI](https://mistral.ai/news/build-with-studio)

## AI: tooling & engineering
### Do agent skills earn their context cost?
Two posts this week test this. dbt's proof-of-concept ran Claude 5.5 models on a dbt project with and without dbt skills. Across 22 runs, run-to-run variance exceeded any skills effect, and process (testing, deployment, review) separated good runs from bad ones more than dbt knowledge did. The author calls the results non-conclusive. Tabular Editor describes an ablation method: re-run the same prompt with and without the skill, or with two versions, over several runs. Their skill helped Claude Opus 5 follow the steps and surface issues it otherwise missed. They also argue skills should be hand-written, because an AI-rewritten version of theirs contained factual errors.
**Why it matters:** Skills should be tested like code, and they are worth writing mainly for team-specific process rather than generic tool docs.
●●●○○ · [dbt Developer Blog](https://docs.getdbt.com/blog/do-coding-agents-still-need-dbt-skills) · [Tabular Editor](https://tabulareditor.com/blog/how-to-test-ai-agent-skills) · covered by 2 sources

### Anthropic on the components of agent memory
Anthropic defines agent memory as notes Claude retains between sessions, excluding weight changes, in-context learning and compaction. It proposes "dreaming", where an agent reflects offline on its logs to fix mistakes and write new notes. Evaluations on CL-Bench 1.0 and Pokémon Red suggest that memory recording validated rules and strategy works better than memory recording easily re-readable state.
**Why it matters:** It gives concrete guidance on what an agent should persist and how to structure an offline consolidation step.
●●●○○ · [Anthropic](https://www.anthropic.com/research/components-of-agent-memory)

### Claude Platform traces now export natively to Databricks MLflow
Claude Platform supports native OpenTelemetry export to Databricks MLflow for the Anthropic SDKs, the Messages API and Managed Agents. Model and tool calls appear as spans in Unity Catalog tables linked to an MLflow experiment. Databricks also describes trace analysis, Issues (beta), review queues and agent evaluation built on top.
**Why it matters:** Claude agents can be debugged and evaluated with governed traces without custom instrumentation, if Databricks is in your stack.
●●●○○ · [Databricks Blog](https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow)

## BI: Microsoft Fabric & Power BI
### OneLake gets a hosted MCP server and an endpoint discovery API (preview)
Microsoft added a remotely hosted OneLake MCP server (preview), so agents can explore data without a local install. It also added MCP tools for shortcuts and OneLake security in the Fabric Core MCP server, and an endpoint discovery API (preview) that tells agents which Fabric engines an item supports. The demos use GitHub Copilot on a mirrored database, shortcuts and a Spark analysis. No GA dates are given.
**Why it matters:** This changes how I would wire agent access to Fabric data, with discovery and security handled at the platform level.
●●●●○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/OneLake-The-file-system-for-agent-first-data-engineering/ba-p/5383035)

### M365 Copilot and Power BI semantic models: integration is GA
Chris Webb, a Microsoft employee, argues that organisations with Power BI and M365 Copilot should start their chat-with-data work here. The integration replaces the side-pane approach, reuses existing semantic model work (synonyms, AI instructions) and can combine Power BI data with Work IQ context. Querying needs an M365 Business Premium licence plus capacity CUs for DAX queries, and Cowork credits may apply for complex tasks.
**Why it matters:** It is a GA path to natural-language access over existing semantic models, with a different cost model from the older Copilot setup.
●●●●○ · [Chris Webb's BI Blog](https://blog.crossjoin.co.uk/2026/11/01/microsoft-365-copilot-and-power-bi-the-easiest-way-to-chat-with-your-data)

### OneLake table APIs: Iceberg write operations and a table metadata API (preview)
The OneLake table endpoint now supports Iceberg REST Catalog write operations. Clients such as PyIceberg, Snowflake and DuckDB can create native Iceberg tables, commit snapshots and get short-lived storage credentials. Commits use optimistic concurrency checks. A new metadata API in preview reads and writes descriptions and key-value tags on tables and columns, including through shortcuts.
**Why it matters:** External engines can land results directly in OneLake as Iceberg, and tables can carry business descriptions that agents and semantic models can use.
●●●●○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/OneLake-table-APIs-Now-with-Iceberg-writes-plus-richer-table/ba-p/5391262)

### OneLake as native storage for Azure Databricks is GA
OneLake external-location support for Azure Databricks Unity Catalog is generally available, with OneLake Security on by default for Azure Databricks Storage items. Managed tables, volumes, views, materialized views and streaming tables can live directly in OneLake, while Databricks keeps compute and Unity Catalog management. Access must be configured separately on both sides.
**Why it matters:** You can keep one physical copy of Unity Catalog data in OneLake instead of syncing between platforms, but governance now spans both.
●●●●○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Use-OneLake-as-native-storage-for-Azure-Databricks-Generally/ba-p/5377939)

### IQ Share (preview): cross-tenant sharing without copies
Producers can share a whole Lakehouse, Warehouse or Mirrored item with recipients in other Fabric tenants, with no data copied. They can attach Markdown files describing definitions and usage, and they control acceptance review, revocation and expiry. Recipients get a read-only mirrored item built on shortcuts. Spark notebooks, semantic models and data agents need an intermediate Lakehouse.
**Why it matters:** It replaces export pipelines for partner or customer data sharing, though the preview limits on semantic models and Spark add an extra step.
●●●●○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Share-data-and-context-across-organizations-with-IQ-Share/ba-p/5378764)

### Admin connection APIs and data connection policies (preview)
Tenant admins can list all tenant connections, including ones they do not own, and manage Owner assignments, for example when an owner leaves. Policies in the admin portal add an authentication allowlist and a Microsoft Entra tenant allowlist for cloud connections, enforced on existing connections too. Granting Owner does not transfer OAuth credentials, and enabling an allowlist can break existing workflows.
**Why it matters:** It gives a tenant-wide connection inventory and enforceable authentication rules, but needs a review of affected connections before you switch it on.
●●●●○ · [Microsoft Fabric Blog](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Govern-Fabric-connections-with-admin-APIs-and-data-connection/ba-p/5383656)

## BI: market
### Snowflake's agent announcements: CoWork, CoCo, Business Ontology
Snowflake published several posts the same day. CoWork gets Profiles that route questions to the right agent, plus Dashboards (public preview) and scheduled Automations. CoCo gets long-running Cloud Agents and automations, with the Cortex Agent SDK stated as GA. CoCo for Excel and Google Sheets is in public preview. Business Ontology is a governance layer for business concepts and metrics that serves only approved definitions to agents, and it is announced as public preview "soon". All of it is vendor-written, and the performance figures are internal tests.
**Why it matters:** It shows where a competing platform is taking governed, agent-driven BI and shared business definitions, which is the bar Fabric and Power BI will be measured against.
●●●○○ · [Snowflake: CoWork](https://www.snowflake.com/content/snowflake-site/global/en/blog/snowflake-cowork-profiles-automations-dashboards) · [Snowflake: Business Ontology](https://www.snowflake.com/content/snowflake-site/global/en/blog/business-ontology-context) · [Snowflake: CoCo](https://www.snowflake.com/content/snowflake-site/global/en/blog/snowflake-coco-cloud-agents-automations)

### Apache Spark 4.3 adds stateful Real-Time Mode
Spark 4.3, available in Databricks Runtime 19, extends Structured Streaming's Real-Time Mode to stateful operations: aggregations, deduplication and transformWithState. Databricks reports sub-150 ms P99 latency on three tested workloads, framed as measurements rather than a guarantee. Spark also moves to quarterly feature releases.
**Why it matters:** Millisecond-scale stateful streaming within familiar APIs could remove a separate streaming engine in some designs, which is relevant when comparing options against Fabric's real-time stack.
●●●○○ · [Databricks Blog](https://www.databricks.com/blog/introducing-apache-spark-43-now-available-databricks-runtime-19)

## Research corner
### Can LLMs read, and even edit, neural network weights?
A paper by Takehi, Teoh, Zhang and Khattab reports that frontier LLMs can infer what a small reinforcement-learning game policy was trained to do by reading its raw weights as text, with no tools. Simon Willison tried it informally on Qwen 3.8 27B running locally. It identified three of four games, was vague on Pac-Man and failed Freeway, and runs took 46 minutes to over an hour. Related reports say LLMs can write or edit small networks' weights directly. Hugging Face reproduced one such result, but critics cite missing baselines and possible overfitting, and a spaCy author called the paper misleading for conflating this with tool-assisted editing. On timescale this is long term, and the evidence is early and contested.
**Why it matters:** It hints at models inspecting or patching other models, but nothing here is usable in Fabric or LLM pipelines today.
●●○○○ · [Simon Willison](https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights) · [Latent Space](https://latent.space/p/ainews-behind-latent-space-kill-my-saas-jev-ai-in-2026-aiei-shanghai) · covered by 2 sources

### StateBench: how well do models track state over long documents?
The Allen AI team built a benchmark of increasing difficulty, from simple assignments up to swaps that reassign variables by reference. Small models trained from scratch showed that recurrent and hybrid architectures (Gated DeltaNet variants) generalize to much longer sequences than transformers on the harder levels. Four frontier models did well on easy levels, but on the longest general finite problems accuracy fell to 13% or lower. This is one lab's tech report with no independent replication yet. The architecture findings are a long-term signal, while the frontier-model result is relevant now.
**Why it matters:** If a pipeline relies on an LLM following chained updates across long inputs, test it at length instead of assuming reliability.
●●●○○ · [Hugging Face Blog](https://huggingface.co/blog/allenai/statebench)

## BI practice
### What a year of building ADBC drivers taught Columnar
Matt Topol, co-founder of Columnar, described a year of production ADBC (Arrow Database Connectivity) driver work. The pain points were inconsistent type systems across databases: numeric precision limits, string and null handling, timestamp time zones, and differing Spark backend protocols. His advice is to pin driver versions and test schemas early. Spec gaps are due to be addressed in an upcoming revision.
**Why it matters:** Power BI is among the tools that have adopted ADBC, so these type-mapping divergences are the kind of surprises to check in a connector path.
●●●○○ · [dbt Labs Blog](https://www.getdbt.com/blog/columnar-adbc-drivers-zero-copy-lessons)

### dbt Charts and the case for dashboards as reviewable code
Dave Fowler, creator of dbt Charts (open source, Apache 2.0, in beta), told Tristan Handy that AI-written dashboards need a readable, reviewable spec rather than generated JavaScript or Python. He also argues that BI tools' weak handling of relational data is a main reason teams still build dimensional models, and that AI may weaken that need. The piece is partly promotional and opinion-driven.
**Why it matters:** It poses a concrete question for an LLM-assisted BI team: should dashboards be specified as reviewable code that agents write, and is the pre-joined layer still necessary?
●●●○○ · [Analytics Engineering Roundup](https://roundup.getdbt.com/p/dbt-charts-the-markdown-of-dashboards)

---

## Under the hood

167 items triaged this week, 58 kept (+2 BI practice reads in the pool), 108 dropped.

Top drop reasons: marketing or case study (36), low significance (35), off-topic (16), tutorial or listicle (5), funding or business news (4), event or webinar (3).
