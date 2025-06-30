#!/bin/bash

# 启动Appium服务器
echo "启动Appium服务器..."
appium --log appium.log --local-timezone &
APPIUM_PID=$!

# 等待Appium服务器启动
echo "等待Appium服务器启动..."
sleep 15

# 检查Appium服务器状态
if curl -f http://127.0.0.1:4723/status; then
    echo "Appium服务器启动成功"
else
    echo "Appium服务器启动失败"
    exit 1
fi

# 运行测试
echo "开始运行自动化测试..."
python run_tests.py --report

# 保存测试结果
echo "测试完成，结果保存在 reports/ 目录"

# 保持容器运行（可选）
# tail -f appium.log 