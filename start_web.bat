@echo off
rem videohuman 工作台一键启动:起服务 + 自动打开 Chrome
cd /d %~dp0

rem 延迟 5 秒等服务起来,再用 Chrome 打开页面(独立窗口,不占用本控制台)
start "" /min cmd /c "timeout /t 5 /nobreak >nul && start "" chrome.exe http://127.0.0.1:8100"

echo videohuman 工作台启动中: http://127.0.0.1:8100
echo 关闭本窗口即停止服务
uv run --no-sync vh serve --port 8100
pause
