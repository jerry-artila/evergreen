#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查相簿目录和网页的同步情况
"""

import re
from pathlib import Path

def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    html_file = Path("召會生活相簿.html")
    image_dir = Path("lifeimages25")
    
    # 读取 HTML 文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取 HTML 中的文件
    pattern = r'src=["\']lifeimages25/([^"\']+)["\']'
    files_in_html = set(re.findall(pattern, html_content))
    
    # 获取目录中的文件
    files_in_dir = {f.name for f in image_dir.iterdir() if f.is_file()}
    
    # 找出差异
    missing = files_in_dir - files_in_html
    extra = files_in_html - files_in_dir
    
    print("=" * 60)
    print("相簿同步检查")
    print("=" * 60)
    print(f"目录中的文件数: {len(files_in_dir)}")
    print(f"HTML中的文件数: {len(files_in_html)}")
    print()
    
    if missing:
        print(f"❌ 缺失的文件 ({len(missing)} 个):")
        for f in sorted(missing):
            print(f"  - {f}")
        print()
    else:
        print("✓ 所有目录中的文件都已存在于 HTML 中")
        print()
    
    if extra:
        print(f"⚠️  HTML 中多余的文件引用 ({len(extra)} 个):")
        for f in sorted(extra):
            print(f"  - {f}")
        print()
    else:
        print("✓ HTML 中没有多余的文件引用")
        print()
    
    if not missing and not extra:
        print("=" * 60)
        print("✓ 相簿完全同步！")
        print("=" * 60)
    else:
        print("=" * 60)
        if missing:
            print(f"需要添加 {len(missing)} 个文件到网页")
        if extra:
            print(f"需要从网页移除 {len(extra)} 个文件引用")
        print("=" * 60)

if __name__ == "__main__":
    main()

