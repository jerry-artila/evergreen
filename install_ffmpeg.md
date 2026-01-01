# 安装 FFmpeg 指南

## 方法 1: 使用 Chocolatey (推荐)

如果您已安装 Chocolatey，运行：
```powershell
choco install ffmpeg
```

## 方法 2: 使用 Scoop

如果您已安装 Scoop，运行：
```powershell
scoop install ffmpeg
```

## 方法 3: 手动安装

1. 访问 https://www.gyan.dev/ffmpeg/builds/
2. 下载 "ffmpeg-release-essentials.zip"
3. 解压到一个文件夹，例如 `C:\ffmpeg`
4. 将 `C:\ffmpeg\bin` 添加到系统 PATH 环境变量
5. 重新打开命令行窗口

## 验证安装

安装后，运行以下命令验证：
```powershell
ffmpeg -version
```

如果显示版本信息，说明安装成功。

