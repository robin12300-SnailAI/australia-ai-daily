#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""澳洲AI日报 2026-11-28 双群推送（三件套）"""
import json, urllib.request

VOICE = "https://robin12300-snailai.github.io/australia-ai-daily/voices/aunews_20261128_1019.mp3"
HTML = "https://robin12300-snailai.github.io/australia-ai-daily/2026-11-28.html"
HOOKS = {
    "主群 eff50857": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=eff50857-abc2-4122-b6ad-e66572ccda9d",
    "速报群 5c17de15": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5c17de15-e8b8-4e59-9f53-37a2ec1c6e6c",
}

md = f"""## 📰 澳洲AI日报 | 2026-11-28（周六）

> 主线：**AI 责任链一周收官**——AI 越强，法律责任越不会转移给 AI。

**【悉尼头条】**
1. **《数字注意义务法案》11/25 通过**：参议院 36:23，澳洲首次可**起诉 AI 聊天机器人提供商**，最高罚全球营收 5% 或 A$1.092 亿；御准 12 个月后生效，11/27 通信部确认时间表。
2. **Kemps Creek A$49.9 亿 AI 数据中心公开展示**：Stockland×EdgeConneX，365MW/33 数据厅，2027 开工、2029 运营，意见征至 12/17。
3. **Nine 推认证 MCP 试点**：AFR/SMH 新闻进企业 AI 工作流，2027 商用；Gleam 同步上线 MCP（能抽中奖、改奖品）。
4. **UNSW 三连**：×ANDHealth 数字健康商业化（1480+ 公司 pipeline）+ iFire 2.3 AI 山火模拟器 + 视觉艺术家 AI 版权调查。

**【其他地区】** 议会 AI 终版报告 263 页/46 建议（创作者付费+数据中心许可+AI 安全所 10 倍拨款）；老年护理算法须强制人工覆盖；NRF A$1.5 亿深科技基金；78% 澳网站无 AI 爬虫规则；SailPoint 警告 40:1 智能体安全缺口；微软：AI 框架 5 分钟攻破。

**【合规倒计时】** ⚠️ **12/10 隐私自动决策披露仅剩 12 天**（健康机构无论规模在内，人工复核不豁免）；TGA 12 款 AI scribe 8 款或属医疗器械——与 Andrew 诊所类项目直接相关。

**🎯 市场机会 TOP3**
1. 用「数字注意义务+12/10 披露」双倒计时锁诊所/会计所/客服中心，一页纸诊断工具约 3 家体检。
2. 复制「MCP 可操作+权限最小化」：助手只读起步、碰钱碰客户人工批准，做成可演示原型。
3. 吃「数据驻留+PoC 到生产」缺口，抓 12/4 Xero Builder Day（FREE，Level 26/45 Clarence St）转介绍。

🎧 **语音播报**：[点击收听]({VOICE})

📄 **完整版**：[点击查看]({HTML})"""

# 发送前自检：三件套缺一不可
checks = {
    "①简要文字（头条+TOP3）": all(k in md for k in ["悉尼头条", "市场机会 TOP3", "12/10"]),
    "②🎧语音链接": "🎧" in md and f"[点击收听]({VOICE})" in md and VOICE.startswith("https://"),
    "③📄完整版链接": "📄" in md and f"[点击查看]({HTML})" in md and HTML.startswith("https://"),
}
print("=== 发送前三件套自检 ===")
for k, v in checks.items():
    print(f"  {'PASS' if v else 'FAIL'}  {k}")
if not all(checks.values()):
    print("[ABORT] 三件套不全，禁止发送")
    raise SystemExit(1)
print("三件套齐全，允许发送。\n")

payload = json.dumps({"msgtype": "markdown", "markdown": {"content": md}}).encode("utf-8")
results = {}
for name, url in HOOKS.items():
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
        results[name] = body
        print(f"[SEND] {name}: {body}")
    except Exception as e:
        # 失败重试一次
        print(f"[RETRY] {name} 首次失败: {e}")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read().decode("utf-8")
            results[name] = body
            print(f"[SEND-RETRY] {name}: {body}")
        except Exception as e2:
            results[name] = f"ERROR: {e2}"
            print(f"[FAIL] {name}: {e2}")

print("\n=== 双群结果汇总 ===")
ok = 0
for name, body in results.items():
    try:
        code = json.loads(body).get("errcode")
    except Exception:
        code = None
    if code == 0:
        ok += 1
    print(f"  {name}: {body}")
print(f"\n成功群数: {ok}/2")
if ok != 2:
    raise SystemExit(2)
print("ALL PASS")
