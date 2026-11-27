#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, urllib.request

VOICE = "https://robin12300-snailai.github.io/australia-ai-daily/voices/aunews_20261114_1022.mp3"
HTML  = "https://robin12300-snailai.github.io/australia-ai-daily/2026-11-14.html"

content = """📰 **澳洲AI日报 | 2026-11-14（周六）**

【悉尼头条】
1. UNSW 发布 RipEye：照片秒级识别离岸流，今夏救生会试点（AI 向善范本）
2. CampusQ 悉尼发布 ReportReady：AI agent 做合规证据审查（可复制为蜗牛合规助手）
3. UBS 悉尼峰会：RBA 副行长公开叫板 AI 行业"秀出生产力数字"
4. Qantas「AI washing」争议：裁 850 岗外包印度，工会批借 AI 洗白裁员
5. APRA：明年起对银行 / 养老金 / 保险做 AI 压力测试

【全国】AutoSwift 获新加坡 X Star 近 A$10M；Firmus 再融 A$500M 绿电数据中心；西澳蓝莓农场自动驾驶 + AI 采摘。

【政策倒计时】数字关怀义务法案 11/20 交报告；隐私法自动决策披露 12/10 生效；联邦 AI 标准立法年底引入。

🎯 **市场机会 TOP3**
1. 受监管行业 AI 合规自动化（APRA + Digital Duty of Care 硬推）
2. 透明化 AI ROI / 生产力度量工具（RBA 叫板 + AI washing 反向需求）
3. 垂直 agentic AI 落地模板（汽车 / 房产 / 教育三线印证）

🎧 语音播报：[点击收听](%s)
📄 完整版：[点击查看](%s)""" % (VOICE, HTML)

payload = json.dumps({"msgtype": "markdown", "markdown": {"content": content}}, ensure_ascii=False).encode("utf-8")

webhooks = {
    "总管家大群": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=eff50857-abc2-4122-b6ad-e66572ccda9d",
    "澳洲AI速报群": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5c17de15-e8b8-4e59-9f53-37a2ec1c6e6c",
}

for name, url in webhooks.items():
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            resp = r.read().decode("utf-8")
        print(f"[{name}] {resp}")
    except Exception as e:
        print(f"[{name}] ERROR {e}")
