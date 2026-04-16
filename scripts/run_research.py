#!/usr/bin/env python3
"""
Market Research API Client Script
==================================
Execute market research tasks via the Market Research AI Platform API.

Usage:
    python run_research.py --request "研究需求" --api-key KEY [--api-base URL] [--personas N] [--output FILE]

Environment variables:
    MARKET_RESEARCH_API_KEY - API key for authentication
    MARKET_RESEARCH_API_BASE - API base URL (optional)

API Flow:
    1. Submit task → designing (研究框架设计)
    2. Generating personas → personas (生成用户人设)
    3. Queue for scout → queuing (社媒侦察排队)
    4. Social media scout → scouting (真实社媒爬取)
    5. Auto interview → interviewing (自动深度访谈)
    6. Generate report → completed (生成研究报告)
"""

import argparse
import json
import os
import sys
import time
import requests
from typing import Optional


# 默认API base URL
DEFAULT_API_BASE = "http://localhost:8000/api/v1/research-flow"

# 阶段消息映射
PHASE_MESSAGES = {
    "designing": "📋 正在设计研究框架...",
    "post-design": "✅ 研究框架设计完成",
    "personas": "👤 正在生成用户人设...",
    "queuing": "⏳ 社媒侦察排队中...",
    "scouting": "🔍 正在进行社交媒体侦察...",
    "interviewing": "💬 正在进行深度访谈...",
    "completed": "✅ 研究已完成",
}


def get_phase_message(phase: str) -> str:
    """获取阶段对应的友好消息"""
    return PHASE_MESSAGES.get(phase, f"📌 当前阶段: {phase}")


def get_api_key() -> Optional[str]:
    """Get API key from environment or argument."""
    return os.environ.get("MARKET_RESEARCH_API_KEY")


def normalize_api_base(api_base: str) -> str:
    """
    规范化API base URL，确保路径正确

    支持的输入格式：
    - http://localhost:8000
    - http://localhost:8000/
    - http://localhost:8000/api/v1/research-flow
    - http://localhost:8000/api/v1/research-flow/

    输出格式：
    - http://localhost:8000/api/v1/research-flow
    """
    api_base = api_base.rstrip("/")

    # 如果已经包含完整路径，直接返回
    if api_base.endswith("/api/v1/research-flow"):
        return api_base

    # 如果只是域名，添加完整路径
    return f"{api_base}/api/v1/research-flow"


def test_connection(api_base: str, api_key: str) -> dict:
    """Test API connection and return user info."""
    headers = {"Content-Type": "application/json", "X-API-Key": api_key}
    api_base = normalize_api_base(api_base)
    response = requests.get(f"{api_base}/auto-research/test", headers=headers, timeout=10)
    result = response.json()
    if result.get("code") != 0:
        raise Exception(f"API test failed: {result}")
    return result.get("data", {})


def submit_task(api_base: str, api_key: str, user_request: str, persona_count: int = 5, platforms: list = None) -> dict:
    """Submit a research task and return task info including queue status."""
    if platforms is None:
        platforms = ["小红书", "微博", "抖音"]

    headers = {"Content-Type": "application/json", "X-API-Key": api_key}
    api_base = normalize_api_base(api_base)

    payload = {
        "user_request": user_request,
        "persona_count": persona_count,
        "platforms": platforms
    }

    response = requests.post(
        f"{api_base}/auto-research/submit",
        headers=headers,
        json=payload,
        timeout=30
    )
    result = response.json()

    if result.get("code") != 0:
        raise Exception(f"Task submission failed: {result}")

    return result["data"]


def poll_status(api_base: str, api_key: str, task_id: str, interval: int = 5, max_wait: int = 900) -> dict:
    """Poll task status until completion or failure."""
    headers = {"Content-Type": "application/json", "X-API-Key": api_key}
    api_base = normalize_api_base(api_base)
    waited = 0
    last_phase = None
    last_queue_pos = None

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"📊 研究进度追踪", file=sys.stderr)
    print(f"{'='*50}\n", file=sys.stderr)

    while waited < max_wait:
        response = requests.get(
            f"{api_base}/auto-research/status/{task_id}",
            headers=headers
        )
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"Status check failed: {result}")

        data = result.get("data", {})
        status = data.get("status")
        current_phase = data.get("current_phase", "unknown")

        # 显示阶段变化
        if current_phase != last_phase:
            print(f"{get_phase_message(current_phase)}", file=sys.stderr)
            last_phase = current_phase

        if status == "completed":
            print(f"\n{'='*50}", file=sys.stderr)
            print(f"✅ 研究任务完成!", file=sys.stderr)
            print(f"{'='*50}\n", file=sys.stderr)
            return {
                "status": "completed",
                "title": data.get("title"),
                "report": data.get("report"),
                "personas_count": data.get("personas_count", 0),
                "personas": data.get("personas", []),
            }
        elif status == "failed":
            raise Exception(f"Task failed: {data.get('error')}")
        elif status == "queued":
            # 显示排队位置
            queue_pos = data.get("queue_position", "?")
            queue_info = data.get("queue_info", {})
            if queue_pos != last_queue_pos:
                print(f"  ⏳ 排队中... 位置: 第 {queue_pos} 位 (当前运行: {queue_info.get('running', 0)}/{queue_info.get('max_concurrent', 4)})", file=sys.stderr)
                last_queue_pos = queue_pos
        elif status == "in_progress":
            # 显示进度
            elapsed = f"[{waited}s]"
            if current_phase == "scouting":
                print(f"  {elapsed} 🔍 正在爬取小红书真实数据...", file=sys.stderr)
            elif current_phase == "interviewing":
                print(f"  {elapsed} 💬 正在进行AI深度访谈...", file=sys.stderr)

        time.sleep(interval)
        waited += interval

    raise TimeoutError(f"Task timed out after {max_wait} seconds")


def main():
    parser = argparse.ArgumentParser(description="Market Research API Client")
    parser.add_argument("--request", "-r", help="Research request/topic (required unless --test)")
    parser.add_argument("--api-key", "-k", help="API key (or set MARKET_RESEARCH_API_KEY env)")
    parser.add_argument("--api-base", "-b", default=DEFAULT_API_BASE,
                        help=f"API base URL (default: {DEFAULT_API_BASE})")
    parser.add_argument("--personas", "-p", type=int, default=5, help="Number of personas (1-10)")
    parser.add_argument("--output", "-o", help="Output file for report (default: stdout)")
    parser.add_argument("--platforms", nargs="+", default=["小红书", "微博", "抖音"],
                        help="Social media platforms")
    parser.add_argument("--test", action="store_true", help="Test connection only")

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or get_api_key()
    if not api_key:
        print("Error: API key required. Set MARKET_RESEARCH_API_KEY or use --api-key", file=sys.stderr)
        sys.exit(1)

    # Test connection
    if args.test:
        info = test_connection(args.api_base, api_key)
        print(f"✅ Connection OK")
        print(f"API Base: {normalize_api_base(args.api_base)}")
        print(f"User: {info['user']['name']} ({info['user']['email']})")
        print(f"Credits: {info['user']['credits']}")
        print(f"Can research: {info['can_research']}")
        sys.exit(0)

    # 研究模式下需要 --request
    if not args.request:
        print("Error: --request/-r is required for research mode", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Submit task
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"🚀 提交市场研究任务", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    print(f"📝 研究需求: {args.request}", file=sys.stderr)
    print(f"👤 人设数量: {args.personas}", file=sys.stderr)
    print(f"📱 社媒平台: {', '.join(args.platforms)}", file=sys.stderr)

    task_info = submit_task(
        args.api_base,
        api_key,
        args.request,
        args.personas,
        args.platforms
    )
    task_id = task_info.get("task_id")
    print(f"\n📋 Task ID: {task_id}", file=sys.stderr)

    if task_info.get("credits_deducted"):
        print(f"💰 积分已扣除: {task_info.get('credits_cost', 10)}", file=sys.stderr)

    # Poll for results
    result = poll_status(args.api_base, api_key, task_id)

    # Output report
    report = result["report"]
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"📄 报告已保存至: {args.output}", file=sys.stderr)
    else:
        print("\n" + "="*50)
        print("📄 市场研究报告")
        print("="*50 + "\n")
        print(report)

    # 输出统计信息
    if result.get("personas_count"):
        print(f"\n📊 研究统计:", file=sys.stderr)
        print(f"   - 人设数量: {result['personas_count']}", file=sys.stderr)


if __name__ == "__main__":
    main()
