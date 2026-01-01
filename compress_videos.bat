@echo off
chcp 65001 >nul
echo ============================================================
echo Video Compression Tool
echo ============================================================
echo.

REM 检查 ffmpeg 是否可用
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo Error: ffmpeg not found
    echo.
    echo Please install ffmpeg first:
    echo 1. Using Chocolatey: choco install ffmpeg
    echo 2. Using Scoop: scoop install ffmpeg
    echo 3. Manual: Download from https://ffmpeg.org/download.html
    echo.
    pause
    exit /b 1
)

echo FFmpeg found. Starting compression...
echo.

REM 压缩大视频文件
set "VIDEO_DIR=lifeimages25"

REM 压缩 0914陽明山竹子湖相調.mp4
if exist "%VIDEO_DIR%\0914陽明山竹子湖相調.mp4" (
    echo Compressing: 0914陽明山竹子湖相調.mp4
    echo Creating backup...
    if not exist "%VIDEO_DIR%\0914陽明山竹子湖相調.backup.mp4" (
        copy "%VIDEO_DIR%\0914陽明山竹子湖相調.mp4" "%VIDEO_DIR%\0914陽明山竹子湖相調.backup.mp4"
    )
    echo Compressing with CRF=23 (medium quality)...
    ffmpeg -i "%VIDEO_DIR%\0914陽明山竹子湖相調.mp4" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart -y "%VIDEO_DIR%\0914陽明山竹子湖相調_compressed.mp4"
    if errorlevel 1 (
        echo Compression failed. Restoring backup...
        copy "%VIDEO_DIR%\0914陽明山竹子湖相調.backup.mp4" "%VIDEO_DIR%\0914陽明山竹子湖相調.mp4"
    ) else (
        echo Compression successful!
        move /Y "%VIDEO_DIR%\0914陽明山竹子湖相調_compressed.mp4" "%VIDEO_DIR%\0914陽明山竹子湖相調.mp4"
    )
    echo.
)

REM 压缩 0914陽明山竹子湖相調2.mp4
if exist "%VIDEO_DIR%\0914陽明山竹子湖相調2.mp4" (
    echo Compressing: 0914陽明山竹子湖相調2.mp4
    echo Creating backup...
    if not exist "%VIDEO_DIR%\0914陽明山竹子湖相調2.backup.mp4" (
        copy "%VIDEO_DIR%\0914陽明山竹子湖相調2.mp4" "%VIDEO_DIR%\0914陽明山竹子湖相調2.backup.mp4"
    )
    echo Compressing with CRF=23 (medium quality)...
    ffmpeg -i "%VIDEO_DIR%\0914陽明山竹子湖相調2.mp4" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart -y "%VIDEO_DIR%\0914陽明山竹子湖相調2_compressed.mp4"
    if errorlevel 1 (
        echo Compression failed. Restoring backup...
        copy "%VIDEO_DIR%\0914陽明山竹子湖相調2.backup.mp4" "%VIDEO_DIR%\0914陽明山竹子湖相調2.mp4"
    ) else (
        echo Compression successful!
        move /Y "%VIDEO_DIR%\0914陽明山竹子湖相調2_compressed.mp4" "%VIDEO_DIR%\0914陽明山竹子湖相調2.mp4"
    )
    echo.
)

echo ============================================================
echo Done!
echo ============================================================
pause

