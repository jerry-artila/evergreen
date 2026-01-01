#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重命名 lifeimages25 目录下的文件，将特殊字符替换为安全的字符
以避免 GitHub Content-Type 问题
"""

import os
import re
from pathlib import Path
import shutil

def sanitize_filename(filename):
    """
    将文件名中的特殊字符替换为安全的字符
    
    规则：
    - 空格 → `-`
    - 括号 `()` → 移除
    - 中文顿号 `、` → `-`
    - 中文逗号 `，` → `-`
    - 多个连续的 `-` → 单个 `-`
    - 移除开头和结尾的 `-`
    """
    # 获取文件扩展名
    name, ext = os.path.splitext(filename)
    
    # 替换特殊字符
    # 空格 → `-`
    name = name.replace(' ', '-')
    
    # 括号 → 移除
    name = name.replace('(', '').replace(')', '')
    
    # 中文顿号 → `-`
    name = name.replace('、', '-')
    
    # 中文逗号 → `-`
    name = name.replace('，', '-')
    
    # 多个连续的 `-` → 单个 `-`
    name = re.sub(r'-+', '-', name)
    
    # 移除开头和结尾的 `-`
    name = name.strip('-')
    
    # 组合新的文件名
    new_filename = name + ext.lower()
    
    return new_filename

def rename_files_in_directory(directory):
    """
    重命名目录中的所有文件
    返回重命名映射字典 {旧文件名: 新文件名}
    """
    directory = Path(directory)
    if not directory.exists():
        print(f"错误：目录 {directory} 不存在")
        return {}
    
    rename_map = {}
    files = list(directory.iterdir())
    
    print(f"找到 {len(files)} 个文件")
    print("=" * 60)
    
    for file_path in files:
        if file_path.is_file():
            old_name = file_path.name
            new_name = sanitize_filename(old_name)
            
            if old_name != new_name:
                new_path = file_path.parent / new_name
                
                # 如果新文件名已存在，添加数字后缀
                counter = 1
                while new_path.exists() and new_path != file_path:
                    name, ext = os.path.splitext(new_name)
                    new_name = f"{name}-{counter}{ext}"
                    new_path = file_path.parent / new_name
                    counter += 1
                
                rename_map[old_name] = new_name
                print(f"  {old_name}")
                print(f"  → {new_name}")
                print()
    
    # 执行重命名
    if rename_map:
        print("=" * 60)
        print(f"将重命名 {len(rename_map)} 个文件")
        print()
        
        for old_name, new_name in rename_map.items():
            old_path = directory / old_name
            new_path = directory / new_name
            
            if old_path.exists():
                try:
                    old_path.rename(new_path)
                    print(f"✓ {old_name} → {new_name}")
                except Exception as e:
                    print(f"✗ 重命名失败 {old_name}: {e}")
            else:
                print(f"✗ 文件不存在: {old_name}")
    else:
        print("没有需要重命名的文件")
    
    return rename_map

def main():
    # 设置输出编码
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    directory = Path("lifeimages25")
    
    print("=" * 60)
    print("lifeimages25 文件重命名工具")
    print("=" * 60)
    print()
    print("将特殊字符替换为安全字符：")
    print("  - 空格 → `-`")
    print("  - 括号 `()` → 移除")
    print("  - 中文顿号 `、` → `-`")
    print("  - 中文逗号 `，` → `-`")
    print()
    
    rename_map = rename_files_in_directory(directory)
    
    if rename_map:
        print()
        print("=" * 60)
        print("重命名完成！")
        print("=" * 60)
        print()
        print("重命名映射已保存，可用于更新 HTML 文件")
        print()
        print("重命名映射（JSON 格式）：")
        import json
        print(json.dumps(rename_map, ensure_ascii=False, indent=2))
        
        # 保存映射到文件
        map_file = Path("rename_map.json")
        with open(map_file, 'w', encoding='utf-8') as f:
            json.dump(rename_map, f, ensure_ascii=False, indent=2)
        print(f"\n映射已保存到: {map_file}")
    else:
        print("\n没有文件被重命名")

if __name__ == "__main__":
    main()

