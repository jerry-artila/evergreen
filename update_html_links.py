#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 HTML 文件中的文件链接，使用重命名后的文件名
"""

import json
import re
from pathlib import Path

def update_html_file(html_file, rename_map):
    """
    更新 HTML 文件中的文件链接
    """
    html_file = Path(html_file)
    if not html_file.exists():
        print(f"错误：文件 {html_file} 不存在")
        return False
    
    # 读取 HTML 文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    updated_count = 0
    
    # 更新所有文件链接
    for old_name, new_name in rename_map.items():
        # 转义特殊字符用于正则表达式
        old_name_escaped = re.escape(old_name)
        
        # 匹配 src="lifeimages25/文件名" 或 src='lifeimages25/文件名'
        patterns = [
            (rf'src="lifeimages25/{old_name_escaped}"', f'src="lifeimages25/{new_name}"'),
            (rf"src='lifeimages25/{old_name_escaped}'", f"src='lifeimages25/{new_name}'"),
            (rf'<source src="lifeimages25/{old_name_escaped}"', f'<source src="lifeimages25/{new_name}"'),
            (rf"<source src='lifeimages25/{old_name_escaped}'", f"<source src='lifeimages25/{new_name}'"),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                updated_count += 1
                print(f"  ✓ 更新: {old_name} → {new_name}")
    
    # 如果内容有变化，写回文件
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ 已更新 {html_file} ({updated_count} 处)")
        return True
    else:
        print(f"\n- {html_file} 无需更新")
        return False

def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 读取重命名映射
    map_file = Path("rename_map.json")
    if not map_file.exists():
        print(f"错误：找不到映射文件 {map_file}")
        print("请先运行 rename_lifeimages.py")
        return
    
    with open(map_file, 'r', encoding='utf-8') as f:
        rename_map = json.load(f)
    
    print("=" * 60)
    print("更新 HTML 文件链接")
    print("=" * 60)
    print(f"加载了 {len(rename_map)} 个重命名映射")
    print()
    
    # 更新 HTML 文件
    html_file = Path("召會生活相簿.html")
    if html_file.exists():
        update_html_file(html_file, rename_map)
    else:
        print(f"警告：找不到 {html_file}")
    
    print()
    print("=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()

