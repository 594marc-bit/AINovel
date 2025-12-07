@echo off
echo ========================================
echo 启动AI续写测试服务器
echo ========================================
echo.

echo [1/2] 检查后端服务器是否运行...
ping -n 1 localhost > nul
findstr /C:"TTL=" > nul
if errorlevel 1 (
    echo 警告: 后端服务器可能未运行
    echo 请确保先运行: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    echo.
    pause
)

echo [2/2] 启动测试代理服务器 (端口 8080)...
echo 测试页面将在: http://localhost:8080/test_ai_write_frontend.html
echo.
echo 按Ctrl+C停止服务器
echo.

python test_server.py