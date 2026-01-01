#!/usr/bin/env python3
"""
视频压缩脚本
将超过 100MB 的视频文件压缩到更小的尺寸
"""

import os
import subprocess
import sys
from pathlib import Path

def check_ffmpeg():
    """检查 ffmpeg 是否可用"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_file_size_mb(filepath):
    """获取文件大小（MB）"""
    return os.path.getsize(filepath) / (1024 * 1024)

def compress_video(input_path, output_path, target_size_mb=50, quality='medium'):
    """
    压缩视频文件
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        target_size_mb: 目标文件大小（MB），默认 50MB
        quality: 质量设置 ('low', 'medium', 'high')
    """
    # 根据质量设置不同的 CRF 值（Constant Rate Factor）
    # CRF 范围：0-51，值越小质量越高，文件越大
    quality_settings = {
        'low': {'crf': 28, 'preset': 'fast'},
        'medium': {'crf': 23, 'preset': 'medium'},
        'high': {'crf': 18, 'preset': 'slow'}
    }
    
    settings = quality_settings.get(quality, quality_settings['medium'])
    
    # 创建临时输出文件
    temp_output = output_path.with_suffix('.tmp' + output_path.suffix)
    
    # 构建 ffmpeg 命令
    # 使用 H.264 编码，调整 CRF 来控制文件大小
    # 降低分辨率到 1920x1080 以减小文件大小
    cmd = [
        'ffmpeg',
        '-i', str(input_path),
        '-c:v', 'libx264',
        '-crf', str(settings['crf']),
        '-preset', settings['preset'],
        '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease',  # 降低分辨率
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',  # 优化网络播放
        '-y',  # 覆盖输出文件
        str(temp_output)
    ]
    
    print(f"Compressing: {input_path.name}")
    print(f"Target size: ~{target_size_mb}MB")
    print(f"Quality: {quality} (CRF={settings['crf']})")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0:
            original_size = get_file_size_mb(input_path)
            new_size = get_file_size_mb(temp_output)
            compression_ratio = (1 - new_size / original_size) * 100
            print(f"Success!")
            print(f"  Original size: {original_size:.2f} MB")
            print(f"  Compressed size: {new_size:.2f} MB")
            print(f"  Compression ratio: {compression_ratio:.1f}%")
            
            # 替换原文件
            import shutil
            if output_path.exists():
                output_path.unlink()
            shutil.move(temp_output, output_path)
            return True
        else:
            print(f"Failed:")
            print(result.stderr)
            # 清理临时文件
            if temp_output.exists():
                temp_output.unlink()
            return False
    except Exception as e:
        print(f"Error: {e}")
        # 清理临时文件
        if temp_output.exists():
            temp_output.unlink()
        return False

def main():
    # 设置输出编码
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 检查 ffmpeg
    if not check_ffmpeg():
        print("Error: ffmpeg not found")
        print("\nPlease install ffmpeg first:")
        print("1. Windows: Download from https://ffmpeg.org/download.html")
        print("   Or use Chocolatey: choco install ffmpeg")
        print("   Or use Scoop: scoop install ffmpeg")
        print("2. Make sure ffmpeg is in your system PATH")
        sys.exit(1)
    
    # 需要压缩的文件（超过 100MB 的视频）
    video_dir = Path("lifeimages25")
    large_videos = [
        "0914陽明山竹子湖相調.mp4",  # 198.77 MB
        "0914陽明山竹子湖相調2.mp4",  # 203.23 MB
    ]
    
    print("=" * 60)
    print("Video Compression Tool")
    print("=" * 60)
    print()
    
    for video_file in large_videos:
        input_path = video_dir / video_file
        if not input_path.exists():
            print(f"Warning: File not found: {input_path}")
            continue
        
        file_size = get_file_size_mb(input_path)
        if file_size < 100:
            print(f"Skipping {video_file} (Size: {file_size:.2f} MB < 100 MB)")
            continue
        
        # 创建备份
        backup_path = input_path.with_suffix('.backup' + input_path.suffix)
        if not backup_path.exists():
            print(f"Creating backup: {backup_path.name}")
            import shutil
            shutil.copy2(input_path, backup_path)
        
        # 压缩视频（目标 50MB，使用中等质量）
        success = compress_video(input_path, input_path, target_size_mb=50, quality='medium')
        
        if success:
            new_size = get_file_size_mb(input_path)
            if new_size > 100:
                print(f"Warning: Compressed file still exceeds 100MB ({new_size:.2f} MB)")
                print("   Consider using lower quality or further compression")
            print()
        else:
            # 如果压缩失败，恢复备份
            if backup_path.exists():
                print(f"Restoring backup...")
                import shutil
                shutil.copy2(backup_path, input_path)
            print()
    
    print("=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()

