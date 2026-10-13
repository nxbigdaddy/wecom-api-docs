#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信API文档批量抓取脚本 - 使用Playwright绕过反爬虫
优化版本：可视化模式、验证码处理、重试机制
"""

import re
import sys
import asyncio
import random
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "https://developer.work.weixin.qq.com/document/path/"
OUTPUT_DIR = Path(__file__).parent / "apis"
DELAY = 2.0  # 请求间隔（秒）
HEADLESS = False  # False=可视化模式，可以看到浏览器
SLOW_MO = 50  # 操作慢放毫秒数

APIS = [
    ("22-微盘/概述", "93654", "概述"),
    ("22-微盘/管理空间", "93655", "新建空间"),
    ("22-微盘/管理空间", "97856", "重命名空间"),
    ("22-微盘/管理空间", "97857", "解散空间"),
    ("22-微盘/管理空间", "97858", "获取空间信息"),
    ("22-微盘/管理空间权限", "93656", "添加成员部门"),
    ("22-微盘/管理空间权限", "97875", "移除成员部门"),
    ("22-微盘/管理空间权限", "97876", "安全设置"),
    ("22-微盘/管理空间权限", "97877", "获取邀请链接"),
    ("22-微盘/管理空间权限", "97878", "获取空间信息"),
    ("22-微盘/管理文件", "93657", "获取文件列表"),
    ("22-微盘/管理文件", "97880", "上传文件"),
    ("22-微盘/管理文件", "98004", "文件分块上传"),
    ("22-微盘/管理文件", "97881", "下载文件"),
    ("22-微盘/管理文件", "97882", "新建文件夹文档"),
    ("22-微盘/管理文件", "97883", "重命名文件"),
    ("22-微盘/管理文件", "97884", "移动文件"),
    ("22-微盘/管理文件", "97885", "删除文件"),
    ("22-微盘/管理文件", "97886", "获取文件信息"),
    ("22-微盘/管理文件权限", "93658", "新增成员"),
    ("22-微盘/管理文件权限", "97888", "删除成员"),
    ("22-微盘/管理文件权限", "97889", "分享设置"),
    ("22-微盘/管理文件权限", "97890", "获取分享链接"),
    ("22-微盘/管理文件权限", "97891", "获取文件权限信息"),
    ("22-微盘/管理文件权限", "97892", "修改文件安全设置"),
    ("22-微盘/回调通知", "97482", "概述"),
    ("22-微盘/回调通知", "97898", "微盘容量不足事件"),
    ("22-微盘/回调通知", "97899", "空间变更事件"),
    ("22-微盘/回调通知", "97900", "文件变更事件"),
    ("22-微盘/回调通知", "97901", "解散空间"),
    ("22-微盘/回调通知", "97902", "修改空间成员"),
    ("22-微盘/回调通知", "97903", "修改空间安全设置"),
    ("22-微盘/高级功能账号管理", "99512", "分配高级功能账号"),
    ("22-微盘/高级功能账号管理", "99513", "取消高级功能账号"),
    ("22-微盘/高级功能账号管理", "99514", "获取高级功能账号列表"),
    ("22-微盘/高级功能账号管理", "95856", "版本和容量管理"),
    ("23-直播", "93633", "概述"),
    ("23-直播", "93637", "创建预约直播"),
    ("23-直播", "93640", "修改预约直播"),
    ("23-直播", "93638", "取消预约直播"),
    ("23-直播", "93874", "删除直播回放"),
    ("23-直播", "93641", "在微信中观看直播或直播回放"),
    ("23-直播", "93634", "获取成员直播ID列表"),
    ("23-直播", "93635", "获取直播详情"),
    ("23-直播", "93636", "获取直播观看明细"),
    ("23-直播", "94145", "直播回调事件"),
    ("23-直播", "94442", "获取跳转小程序商城的直播观众信息"),
    ("24-公费电话", "93662", "获取公费电话拨打记录"),
    ("25-打卡", "93384", "获取企业所有打卡规则"),
    ("25-打卡", "90263", "获取员工打卡规则"),
    ("25-打卡", "90262", "获取打卡记录数据"),
    ("25-打卡", "93374", "获取打卡日报数据"),
    ("25-打卡", "93387", "获取打卡月报数据"),
    ("25-打卡", "93380", "获取打卡人员排班信息"),
    ("25-打卡", "93385", "为打卡人员排班"),
    ("25-打卡", "95803", "为打卡人员补卡"),
    ("25-打卡", "99647", "添加打卡记录"),
    ("25-打卡", "93378", "录入打卡人员人脸信息"),
    ("25-打卡", "94126", "获取设备打卡数据"),
    ("25-打卡", "98041", "管理打卡规则"),
    ("26-审批", "91854", "概述"),
    ("26-审批", "91982", "获取审批模板详情"),
    ("26-审批", "91853", "提交审批申请"),
    ("26-审批", "91815", "审批申请状态变化回调通知"),
    ("26-审批", "91816", "批量获取审批单号"),
    ("26-审批", "91983", "获取审批申请详情"),
    ("26-审批", "93375", "获取企业假期管理配置"),
    ("26-审批", "93376", "获取成员假期余额"),
    ("26-审批", "93377", "修改成员假期余额"),
    ("26-审批", "90269", "审批流程引擎"),
    ("26-审批", "97437", "创建审批模板"),
    ("26-审批", "97438", "更新审批模板"),
    ("27-汇报", "93496", "概述"),
    ("27-汇报", "93393", "批量获取汇报记录单号"),
    ("27-汇报", "93394", "获取汇报记录详情"),
    ("27-汇报", "93395", "获取汇报统计数据"),
    ("27-汇报", "98021", "下载微盘文件"),
    ("28-人事助手", "99130", "概述"),
    ("28-人事助手", "99131", "获取员工字段配置"),
    ("28-人事助手", "99132", "获取员工花名册信息"),
    ("28-人事助手", "99133", "更新员工花名册信息"),
    ("29-会议室", "93618", "概述"),
    ("29-会议室", "93619", "会议室管理"),
    ("29-会议室", "93620", "会议室预定管理"),
    ("29-会议室", "95333", "回调事件"),
    ("30-高级功能", "99860", "概述"),
    ("30-高级功能", "99876", "成员申请的提交回调"),
    ("30-高级功能", "99877", "成员申请的终止回调"),
    ("30-高级功能", "99880", "设置审批单审批信息"),
    ("30-高级功能", "99883", "批量获取申请单ID"),
    ("30-高级功能", "99885", "获取申请单详细信息"),
    ("31-紧急通知应用", "91623", "概述"),
    ("31-紧急通知应用", "91627", "发起语音电话"),
    ("31-紧急通知应用", "91628", "获取接听状态"),
]

def sanitize(name):
    return re.sub(r'[\\/:*?"<>|]', '_', re.sub(r'\s+', '_', name))[:100]

async def fetch_with_playwright(page, api_dir, path_id, name):
    url = f"{BASE_URL}{path_id}"
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            print(f"[尝试 {attempt+1}/{max_retries}] {name}...")
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            
            # 等待文章内容加载，最多等15秒
            try:
                await page.wait_for_selector('article', timeout=15000)
            except:
                # 检查是否有验证码
                captcha = await page.query_selector('#captcha, .captcha, .verify')
                if captcha:
                    print(f"[验证码] {name}: 请手动完成验证码...")
                    # 等待用户手动完成验证码，最多60秒
                    try:
                        await page.wait_for_selector('article', timeout=60000)
                    except:
                        print(f"[超时] {name}: 验证码超时，跳过")
                        return False
            
            # 额外等待确保内容渲染完成
            await asyncio.sleep(1)
            
            # 获取标题
            title = await page.evaluate("""() => {
                const titleEl = document.querySelector('title');
                if (titleEl) {
                    return titleEl.textContent.split(' - ')[0].trim();
                }
                return null;
            }""")
            if not title or '验证码' in title:
                title = name
            
            # 获取文章内容
            content = await page.evaluate("""() => {
                const article = document.querySelector('article');
                if (article) {
                    // 移除脚本和样式标签
                    const scripts = article.querySelectorAll('script, style');
                    scripts.forEach(s => s.remove());
                    return article.innerText.trim();
                }
                return null;
            }""")
            
            if not content or len(content) < 50:
                if attempt < max_retries - 1:
                    print(f"[内容短] {name}: 等待重试...")
                    await asyncio.sleep(3)
                    continue
                content = "内容提取失败，请手动访问查看"
            
            md = f"# {title}\n\n> 来源: [{url}]({url})\n\n{content}"
            
            out_dir = OUTPUT_DIR / api_dir
            out_dir.mkdir(parents=True, exist_ok=True)
            fname = f"{sanitize(name)}.md"
            (out_dir / fname).write_text(md, encoding='utf-8')
            print(f"[OK] {api_dir}/{fname}")
            return True
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"[ERR] {name}: {str(e)[:60]} - 重试中...")
                await asyncio.sleep(3)
            else:
                print(f"[ERR] {name}: {str(e)[:80]}")
                return False
    
    return False

async def main():
    print(f"开始使用Playwright抓取 {len(APIS)} 个API接口...")
    print(f"模式: {'无头模式' if HEADLESS else '可视化模式（可以看到浏览器）'}")
    print("提示: 如果遇到验证码，请在浏览器中手动完成\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )
        
        page = await context.new_page()
        
        # 先访问首页建立Cookie
        print("正在初始化浏览器...")
        await page.goto('https://developer.work.weixin.qq.com/', wait_until='domcontentloaded', timeout=30000)
        await asyncio.sleep(2)
        
        ok = 0
        total = len(APIS)
        
        for i, (api_dir, path_id, name) in enumerate(APIS):
            print(f"\n[{i+1}/{total}] ", end='')
            result = await fetch_with_playwright(page, api_dir, path_id, name)
            if result:
                ok += 1
            
            # 随机延迟，模拟人类行为
            import random
            await asyncio.sleep(DELAY + random.uniform(0.5, 2.0))
        
        await browser.close()
    
    print(f"\n{'='*50}")
    print(f"抓取完成! 成功: {ok}/{total}")
    print(f"文件保存在: {OUTPUT_DIR}")
    print(f"{'='*50}")

if __name__ == "__main__":
    asyncio.run(main())
