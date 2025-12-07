@echo off
echo ========================================
echo 测试AI续写API
echo ========================================
echo.

echo 测试1: 简单的续写请求
echo.
curl -X POST http://localhost:8000/api/ai/simple-write ^
  -H "Content-Type: application/json" ^
  -d "{\"previous_content\": \"李明走进办公室，发现所有人的电脑都变成了蓝色屏幕。\", \"length_hint\": \"short\"}"

echo.
echo ========================================
echo 测试2: 测试API连接
echo.
curl -X POST http://localhost:8000/api/ai/test ^
  -H "Content-Type: application/json" ^
  -d "{}"

echo.
echo ========================================
echo 测试完成
pause