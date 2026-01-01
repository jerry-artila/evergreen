#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Git 仓库中的文件扩展名从大写改为小写
适用于 Windows 系统（文件系统不区分大小写）
"""

import subprocess
import re
import sys
import io

# 设置输出编码为 UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_git_files():
    """获取 Git 中跟踪的文件列表（使用 -z 参数避免编码问题）"""
    result = subprocess.run(
        ['git', 'ls-files', '-z', 'lifeimages25/'],
        capture_output=True
    )
    
    files = []
    for filename_bytes in result.stdout.split(b'\x00'):
        if filename_bytes:
            try:
                filename = filename_bytes.decode('utf-8')
                files.append(filename)
            except:
                pass
    return files

def needs_rename(filename):
    """检查文件是否需要重命名（扩展名是否为大写）"""
    # 匹配大写扩展名
    match = re.search(r'\.(JPG|JPEG|PNG|GIF|MP4|MOV)$', filename)
    if match:
        ext = match.group(0)
        new_file = filename.replace(ext, ext.lower())
        return True, new_file
    return False, None

def main():
    print("Checking files in Git repository...")
    files = get_git_files()
    
    if not files:
        print("No files found.")
        return
    
    print(f"Found {len(files)} files.")
    
    renames = []
    for file in files:
        if not file:
            continue
        needs, new_file = needs_rename(file)
        if needs:
            renames.append((file, new_file))
    
    if not renames:
        print("\nAll file extensions are already lowercase. No renaming needed.")
        return
    
    print(f"\nFound {len(renames)} files that need renaming:")
    for old_file, new_file in renames[:5]:
        print(f"  {old_file} -> {new_file}")
    if len(renames) > 5:
        print(f"  ... and {len(renames) - 5} more files")
    
    print(f"\nStarting to rename {len(renames)} files...")
    print("(Using two-step renaming for Windows file system)\n")
    
    success_count = 0
    error_count = 0
    
    # 两步重命名：先重命名为临时名称，再重命名为目标名称
    for old_file, new_file in renames:
        temp_name = old_file + ".temp_rename"
        
        try:
            # 第一步：重命名为临时名称
            result1 = subprocess.run(
                ['git', 'mv', '-f', old_file, temp_name],
                capture_output=True,
                text=True
            )
            
            if result1.returncode != 0:
                print(f"Error: Cannot rename {old_file} to temp file")
                print(f"  {result1.stderr}")
                error_count += 1
                continue
            
            # 第二步：重命名为最终名称
            result2 = subprocess.run(
                ['git', 'mv', '-f', temp_name, new_file],
                capture_output=True,
                text=True
            )
            
            if result2.returncode != 0:
                print(f"Error: Cannot rename temp file to {new_file}")
                print(f"  {result2.stderr}")
                error_count += 1
                # 尝试恢复
                subprocess.run(['git', 'mv', '-f', temp_name, old_file], capture_output=True)
                continue
            
            success_count += 1
            if success_count % 10 == 0:
                print(f"  Processed {success_count}/{len(renames)} files...")
                
        except Exception as e:
            print(f"Error: Exception while processing {old_file}: {e}")
            error_count += 1
    
    print(f"\nDone!")
    print(f"  Success: {success_count} files")
    print(f"  Failed: {error_count} files")
    
    if success_count > 0:
        print(f"\nUse the following commands to review and commit changes:")
        print(f"  git status")
        print(f"\nTo commit:")
        print(f"  git commit -m \"Convert file extensions to lowercase\"")
        print(f"  git push origin main")

if __name__ == '__main__':
    main()
