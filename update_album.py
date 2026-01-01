#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新相簿网页，添加新的图片和视频文件
"""

import re
from pathlib import Path
from datetime import datetime

def extract_date_from_filename(filename):
    """从文件名提取日期"""
    # 匹配格式：MMDD... 或 YYYY-MMDD...
    match = re.match(r'(\d{4}-)?(\d{2})(\d{2})', filename)
    if match:
        year = match.group(1) or '2025'
        year = year.rstrip('-')
        month = match.group(2)
        day = match.group(3)
        return f"{year}-{month}-{day}"
    return None

def get_file_type(filename):
    """判断文件类型"""
    ext = Path(filename).suffix.lower()
    if ext in ['.jpg', '.jpeg', '.png', '.gif']:
        return 'image'
    elif ext in ['.mp4', '.webm', '.mov']:
        return 'video'
    return None

def generate_alt_text(filename):
    """从文件名生成 alt 文本"""
    # 移除日期前缀和扩展名
    name = Path(filename).stem
    # 移除日期部分（MMDD 或 YYYY-MMDD）
    name = re.sub(r'^(\d{4}-)?\d{4}', '', name)
    return name

def generate_title(filename):
    """从文件名生成标题"""
    # 移除日期前缀和扩展名
    name = Path(filename).stem
    # 移除日期部分（MMDD 或 YYYY-MMDD）
    name = re.sub(r'^(\d{4}-)?\d{4}', '', name)
    date = extract_date_from_filename(filename)
    if date:
        return f"{name} {date}"
    return name

def create_image_card(filename):
    """创建图片卡片 HTML"""
    alt_text = generate_alt_text(filename)
    title = generate_title(filename)
    return f'''        <div class="bg-white rounded-xl shadow-md overflow-hidden transition-all duration-300 ease-in-out flex flex-col hover:-translate-y-1 hover:shadow-xl">
            <img src="lifeimages25/{filename}" alt="{alt_text}" class="w-full h-[250px] object-contain block">
            <div class="px-3 md:px-6 pt-1 pb-1 md:pb-2 bg-white">
                <p class="m-0 text-gray-700 text-base md:text-lg text-center font-medium leading-tight">{title}</p>
            </div>
        </div>'''

def create_video_card(filename):
    """创建视频卡片 HTML"""
    alt_text = generate_alt_text(filename)
    title = generate_title(filename)
    ext = Path(filename).suffix.lower()
    return f'''        <div class="bg-white rounded-xl shadow-md overflow-hidden transition-all duration-300 ease-in-out flex flex-col hover:-translate-y-1 hover:shadow-xl">
            <video controls preload="metadata" class="w-full h-[250px] object-contain block bg-black">
                <source src="lifeimages25/{filename}" type="video/{ext[1:]}">
                您的瀏覽器不支援影片播放。
            </video>
            <div class="px-3 md:px-6 pt-1 pb-1 md:pb-2 bg-white">
                <p class="m-0 text-gray-700 text-base md:text-lg text-center font-medium leading-tight">{title}</p>
            </div>
        </div>'''

def get_existing_files(html_file):
    """从 HTML 文件中提取已存在的文件列表"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有文件路径
    pattern = r'src=["\']lifeimages25/([^"\']+)["\']'
    matches = re.findall(pattern, content)
    return set(matches)

def get_all_files(directory):
    """获取目录中的所有文件"""
    directory = Path(directory)
    files = []
    for file_path in directory.iterdir():
        if file_path.is_file():
            files.append(file_path.name)
    return sorted(files)

def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    html_file = Path("召會生活相簿.html")
    image_dir = Path("lifeimages25")
    
    if not html_file.exists():
        print(f"错误：找不到 {html_file}")
        return
    
    if not image_dir.exists():
        print(f"错误：找不到 {image_dir}")
        return
    
    # 获取所有文件和已存在的文件
    all_files = get_all_files(image_dir)
    existing_files = get_existing_files(html_file)
    
    # 找出缺失的文件
    missing_files = [f for f in all_files if f not in existing_files]
    
    if not missing_files:
        print("✓ 所有文件都已存在于网页中")
        return
    
    print(f"发现 {len(missing_files)} 个新文件需要添加：")
    for f in missing_files:
        print(f"  - {f}")
    
    # 读取 HTML 文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到插入位置（在 </div> 之前，但在 </body> 之前）
    # 查找最后一个卡片 div 的结束位置
    pattern = r'(        </div>\s*</div>\s*</div>)'
    matches = list(re.finditer(pattern, content))
    
    if not matches:
        print("错误：无法找到插入位置")
        return
    
    # 在最后一个卡片后插入新卡片
    insert_pos = matches[-1].end()
    
    # 生成新卡片的 HTML
    new_cards = []
    for filename in sorted(missing_files):
        file_type = get_file_type(filename)
        if file_type == 'image':
            new_cards.append(create_image_card(filename))
        elif file_type == 'video':
            new_cards.append(create_video_card(filename))
    
    # 插入新卡片
    new_content = content[:insert_pos] + '\n' + '\n'.join(new_cards) + '\n' + content[insert_pos:]
    
    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n✓ 已更新 {html_file}，添加了 {len(missing_files)} 个新文件")

if __name__ == "__main__":
    main()

