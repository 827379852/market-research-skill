# Market Research AI Platform API Client

市场调研 AI 平台 API 客户端，通过 LLM Agents 模拟真实受访者进行调研，生成专业的市场研究报告。

## 功能特点

- 🤖 AI 模拟用户人设，进行深度访谈
- 📊 自动生成专业市场研究报告
- 🔍 社交媒体数据侦察（小红书、微博、抖音）
- 📋 完整的研究流程：框架设计 → 人设生成 → 社媒侦察 → 深度访谈 → 报告生成

## 快速开始

### 第一步：注册账号并获取 API Key

1. 访问 **[市场调研 AI 平台](http://47.93.30.245:3000)** 注册账号
2. 登录后，在个人中心获取你的 API Key

### 第二步：配置 API

在运行脚本前，需要配置 API 连接信息：

**方式一：设置环境变量（推荐）**

```bash
# Linux/macOS
export MARKET_RESEARCH_API_KEY="your-api-key-here"
export MARKET_RESEARCH_API_BASE="http://47.93.30.245:8000"

# Windows PowerShell
$env:MARKET_RESEARCH_API_KEY="your-api-key-here"
$env:MARKET_RESEARCH_API_BASE="http://47.93.30.245:8000"

# Windows CMD
set MARKET_RESEARCH_API_KEY=your-api-key-here
set MARKET_RESEARCH_API_BASE=http://47.93.30.245:8000
```

**方式二：命令行参数**

```bash
python scripts/run_research.py \
  --api-key "your-api-key-here" \
  --api-base "http://47.93.30.245:8000" \
  --request "你的研究需求"
```

**方式三：Claude Code 配置文件（推荐 Claude Code 用户）**

将配置写入 Claude Code 的 settings.json 文件：

**Windows:** `C:\Users\<用户名>\.claude\settings.json`

**macOS/Linux:** `~/.claude/settings.json`

```json
{
  "env": {
    "MARKET_RESEARCH_API_KEY": "your-api-key-here",
    "MARKET_RESEARCH_API_BASE": "http://47.93.30.245:8000"
  }
}
```

配置完成后，在 Claude Code 中直接调用市场调研技能即可自动读取配置。

### 第三步：运行研究任务

```bash
# 基础用法
python scripts/run_research.py \
  --api-key "your-api-key" \
  --api-base "http://47.93.30.245:8000" \
  --request "研究职场白领对AI工具的使用情况" \
  --personas 5 \
  --output report.md

# 使用环境变量
python scripts/run_research.py \
  --request "研究职场白领对AI工具的使用情况" \
  --output report.md
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--request`, `-r` | 是* | - | 研究需求描述 |
| `--api-key`, `-k` | 否 | 环境变量 | API Key |
| `--api-base`, `-b` | 否 | `http://localhost:8000` | API 服务地址 |
| `--personas`, `-p` | 否 | 5 | AI 人设数量 (1-10) |
| `--platforms` | 否 | 小红书 微博 抖音 | 社媒侦察平台 |
| `--output`, `-o` | 否 | 标准输出 | 报告输出文件 |
| `--test` | 否 | - | 测试 API 连接 |

*`--test` 模式下不需要 `--request`

## 测试连接

```bash
python scripts/run_research.py \
  --api-key "your-api-key" \
  --api-base "http://47.93.30.245:8000" \
  --test
```

成功输出示例：
```
✅ Connection OK
API Base: http://47.93.30.245:8000/api/v1/research-flow
User: 用户名 (email@example.com)
Credits: 100
Can research: True
```

## 研究流程

```
1. 设计研究框架 (designing) → 设计访谈框架，锚定研究目标
2. 生成用户人设 (personas) → 查询/生成目标人群认知基线
3. 社媒侦察排队 (queuing) → 等待获取执行槽位
4. 社交媒体侦察 (scouting) → 使用真实浏览器池爬取小红书数据
5. 自动深度访谈 (interviewing) → 基于社媒洞察进行深度访谈
6. 生成研究报告 (completed) → 合成研究报告
```

## 研究需求最佳实践

**好的示例：**
```
我想研究职场白领对AI工具的使用情况，包括：
1. 他们使用哪些AI工具？使用频率如何？
2. 使用AI工具的主要动机是什么？
3. 在使用过程中遇到哪些痛点和挑战？
4. 对AI工具的准确性和隐私保护有什么顾虑？
5. 什么因素会影响他们选择或放弃某个AI工具？
```

**不好的示例：**
```
研究AI工具
```

## 报告结构

生成的报告包含以下章节：

1. **执行摘要** - 核心发现与建议
2. **研究方法** - 方法论与样本概述
3. **用户画像分析** - 人设画像与痛点
4. **核心发现** - 调研发现与用户原话
5. **竞品与市场洞察** - 竞品分析
6. **机会与建议** - 可执行的建议
7. **附录** - 研究统计数据

## 常见问题

### 1. 连接失败

检查 API 地址是否正确：
```bash
# 正确格式
--api-base "http://47.93.30.245:8000"
```

### 2. 认证失败 (401 Unauthorized)

检查 API Key 是否正确，确保从 [平台](http://47.93.30.245:3000) 获取的 key 完整复制。

### 3. 积分不足 (402 Payment Required)

登录 [平台](http://47.93.30.245:3000) 充值积分。

### 4. 任务超时

减少人设数量或增加等待时间：
```bash
python scripts/run_research.py --request "..." --personas 3
```

## 依赖安装

```bash
pip install requests
```

## License

MIT
