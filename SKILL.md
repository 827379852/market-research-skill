---
name: market-research-api
description: Call the Market Research AI Platform API to generate professional market research reports with AI-simulated user personas and interviews. Use this skill whenever the user wants to conduct market research, user research, consumer insights, survey analysis, product testing, or understand user attitudes. Triggers on requests like "research X market", "what do users think about Y", "conduct a user study", "analyze consumer behavior", "市场调研", "用户研究", "消费者洞察", or any request that involves understanding user preferences, behaviors, or market trends.
---

# Market Research AI Platform Skill

Generate professional market research reports by calling the Market Research AI Platform API, which uses LLM Agents to simulate real respondents for surveys, product testing, and user research.

## When to Use This Skill

Use this skill when the user wants to:
- Conduct market research or user research
- Understand consumer attitudes, preferences, or behaviors
- Test product concepts with simulated users
- Generate user personas and interview insights
- Analyze market trends and competitive landscape
- Get actionable business recommendations

**Trigger phrases (English):**
- "research the [product] market"
- "what do users think about [topic]"
- "conduct a user study on [topic]"
- "analyze consumer behavior for [product]"
- "generate a market research report"
- "I need insights on [market/audience]"

**Trigger phrases (Chinese):**
- "帮我调研一下..."
- "市场调研..."
- "用户研究..."
- "消费者洞察..."
- "我想了解用户对...的看法"
- "帮我分析一下...市场"

---

## Research Flow (对标网页端流程)

```
1. 设计研究框架 (designing) → 设计访谈框架，锚定研究目标
2. 生成用户人设 (personas) → 查询/生成目标人群认知基线
3. 社媒侦察排队 (queuing) → 等待获取执行槽位
4. 社交媒体侦察 (scouting) → 使用真实浏览器池爬取小红书数据
5. 自动深度访谈 (interviewing) → 基于社媒洞察进行深度访谈
6. 生成研究报告 (completed) → 合成研究报告
```

---

## Quick Start (Direct Script Execution)

This skill includes a bundled Python script. Execute it directly via Bash tool:

```bash
python <skill-path>/scripts/run_research.py \
  --request "你的研究需求" \
  --api-key "YOUR_API_KEY" \
  --api-base "http://localhost:8000/api/v1/research-flow" \
  --personas 5 \
  --output report.md
```

**Replace `<skill-path>` with the actual path to this skill directory.**

---

## Execution Steps

### Step 1: Gather Research Requirements

Ask the user for:
1. **Research topic** - What to research?
2. **Target audience** (optional) - Who to study?
3. **Key questions** (optional) - What to explore?
4. **Persona count** (default: 5) - How many simulated users?

### Step 2: Check API Configuration

Check environment variables or ask user for:
- `MARKET_RESEARCH_API_KEY` - API key
- `MARKET_RESEARCH_API_BASE` - API base URL (default: `http://localhost:8000/api/v1/research-flow`)

### Step 3: Execute the Script

Use the Bash tool to run the script:

```bash
python "<skill-dir>/scripts/run_research.py" \
  --request "详细的研究需求描述" \
  --api-key "$MARKET_RESEARCH_API_KEY" \
  --api-base "http://localhost:8000/api/v1/research-flow" \
  --personas 5 \
  --platforms "小红书" "微博" "抖音" \
  --output "research_report.md"
```

### Step 4: Present Results

After script completes:
1. Read the generated report file
2. Display key findings to user
3. Offer to save to additional formats (PDF, Word) if needed

---

## Script Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--request`, `-r` | Yes* | - | Research topic/question in natural language |
| `--api-key`, `-k` | No | env | API key (or set `MARKET_RESEARCH_API_KEY`) |
| `--api-base`, `-b` | No | `http://localhost:8000/api/v1/research-flow` | API base URL |
| `--personas`, `-p` | No | 5 | Number of AI personas (1-10) |
| `--platforms` | No | 小红书 微博 抖音 | Social media platforms to scout |
| `--output`, `-o` | No | stdout | Output file for report |
| `--test` | No | - | Test connection only (no --request needed) |

*`--request` is required for research mode, but not needed for `--test` mode.

### API Base URL Format

The script automatically normalizes the API base URL. You can use any of these formats:

```bash
# All of these work correctly:
--api-base "http://localhost:8000"
--api-base "http://localhost:8000/"
--api-base "http://localhost:8000/api/v1/research-flow"
--api-base "http://47.93.30.245:8000"
```

The script will automatically append `/api/v1/research-flow` if needed.

---

## API Response Format

### Submit Response
```json
{
  "code": 0,
  "data": {
    "task_id": "study-uuid",
    "status": "pending",
    "current_phase": "designing",
    "status_url": "/api/v1/research-flow/auto-research/status/{task_id}",
    "queue_info": {"max_concurrent": 4, "queued": 0, "running": 0},
    "credits_deducted": true,
    "credits_cost": 10
  }
}
```

### Status Response (Queued)
```json
{
  "code": 0,
  "data": {
    "status": "queued",
    "current_phase": "queuing",
    "queue_position": 2,
    "queue_info": {"max_concurrent": 4, "queued": 2, "running": 4}
  }
}
```

### Status Response (Completed)
```json
{
  "code": 0,
  "data": {
    "status": "completed",
    "title": "研究标题",
    "current_phase": "completed",
    "report": "# 市场调研报告\n...",
    "personas_count": 5,
    "personas": [...]
  }
}
```

---

## Research Request Best Practices

### Writing Effective Research Requests

**Good example:**
```
我想研究职场白领对AI工具的使用情况，包括：
1. 他们使用哪些AI工具？使用频率如何？
2. 使用AI工具的主要动机是什么？
3. 在使用过程中遇到哪些痛点和挑战？
4. 对AI工具的准确性和隐私保护有什么顾虑？
5. 什么因素会影响他们选择或放弃某个AI工具？
```

**Poor example:**
```
研究AI工具
```

### Persona Count Guidelines

| Count | Use Case | Processing Time |
|-------|----------|-----------------|
| 3 | Quick pulse check | ~3-5 min |
| 5 | Standard research | ~5-8 min |
| 8 | Comprehensive study | ~8-12 min |
| 10 | Full market analysis | ~12-15 min |

**Note:** 社媒侦察阶段使用任务队列，高峰期可能需要排队等待。

---

## Report Structure

Generated reports include:

1. **执行摘要** - Key findings and recommendations
2. **研究方法** - Methodology and sample overview
3. **用户画像分析** - Persona profiles and pain points
4. **核心发现** - Findings with user quotes
5. **竞品与市场洞察** - Competitive analysis
6. **机会与建议** - Actionable recommendations
7. **附录** - Research statistics

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 Unauthorized | Verify API key |
| 402 Payment Required | User needs more credits |
| Timeout | Reduce persona count or increase max_wait |
| Connection failed | Check API base URL |
| Task failed | Check error message in response |

---

## Notes

- Each task consumes credits (default: 10)
- Processing time includes real Xiaohongshu scraping
- Social media scout uses browser pool with queue mechanism
- Report quality depends on request specificity
- The script handles polling automatically with detailed progress display
