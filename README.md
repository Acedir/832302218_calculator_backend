# 832302218_calculator_backend

前后端分离计算器系统的**后端服务**，提供表达式计算与计算历史的 REST API。

前端仓库：https://github.com/Acedir/832302218_calculator_frontend

## 技术栈

- Python 3.10+
- Flask 3.x
- Flask-CORS
- SQLite

## 目录结构
832302218_calculator_backend/
├── app.py # 后端入口，路由定义
├── calculator.py # 安全表达式解析器（递归下降）
├── database.py # SQLite 操作
├── test_calculator.py # 解析器单元测试
├── requirements.txt # 依赖清单
├── codestyle.md # 代码规范
└── README.md

## 运行环境

- Python 3.10 或更高
- 无其他系统依赖

## 安装

```bash
# 1. 创建虚拟环境
python -m venv .venv

# 2. 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt