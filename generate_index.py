#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成企业微信API索引汇总文件
"""

import re
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

APIS_DIR = Path("<workspace>/weixin-api/apis")
OUTPUT_FILE = Path("<workspace>/weixin-api/企业微信API索引汇总.md")

def extract_url_from_file(filepath):
    """从md文件中提取来源URL"""
    try:
        content = filepath.read_text(encoding='utf-8')
        # 匹配 "> 来源: [xxx](url)" 格式
        match = re.search(r'>\s*来源:\s*\[.*?\]\((.*?)\)', content)
        if match:
            return match.group(1)
    except:
        pass
    return None

def main():
    print("正在扫描API文件...")
    
    apis = []
    for md_file in sorted(APIS_DIR.rglob("*.md")):
        rel_path = md_file.relative_to(APIS_DIR)
        parts = rel_path.parts
        
        # 模块名称（第一级目录）
        module = parts[0] if len(parts) > 1 else "根目录"
        
        # 子分类（第二级目录，如果有）
        subcategory = parts[1] if len(parts) > 2 else ""
        
        # API名称（文件名去掉.md）
        api_name = md_file.stem
        
        # 提取URL
        url = extract_url_from_file(md_file)
        if not url:
            # 如果提取失败，跳过
            continue
        
        apis.append({
            'module': module,
            'subcategory': subcategory,
            'name': api_name,
            'url': url
        })
    
    print(f"共找到 {len(apis)} 个API接口")
    
    # 按模块和子分类分组
    grouped = {}
    for api in apis:
        key = (api['module'], api['subcategory'])
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(api)
    
    # 生成Markdown
    md_lines = [
        "# 企业微信 API 接口索引汇总",
        "",
        f"> 共收录 **{len(apis)}** 个API接口",
        ">",
        "> 生成时间: 2026-04-16",
        "",
        "---",
        ""
    ]
    
    current_module = None
    for (module, subcategory), api_list in sorted(grouped.items()):
        # 模块标题
        if module != current_module:
            current_module = module
            md_lines.append(f"\n## {module}\n")
        
        # 子分类标题
        if subcategory:
            md_lines.append(f"\n### {subcategory}\n")
        
        # API列表
        for api in api_list:
            md_lines.append(f"- [{api['name']}]({api['url']})")
    
    md_lines.append("\n---\n")
    md_lines.append("\n> 本文档由企业微信API抓取脚本自动生成\n")
    
    # 写入文件
    OUTPUT_FILE.write_text('\n'.join(md_lines), encoding='utf-8')
    print(f"\n索引文件已生成: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
