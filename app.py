"""
app.py
后端入口：计算 + 计算历史 REST API。
"""
from flask import Flask, request, jsonify
from flask_cors import CORS

from calculator import calculate, CalcError
import database as db

app = Flask(__name__)
CORS(app)

# 启动时初始化数据库
db.init_db()


# ============ 通用响应工具 ============

def ok(data, status=200):
    return jsonify({"success": True, **data}), status


def fail(message, status=400):
    return jsonify({"success": False, "message": message}), status


# ============ 计算接口 ============

@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json(silent=True)
    if not data or "expression" not in data:
        return fail("请求体缺少 expression 字段", 400)

    expression = data["expression"]

    try:
        result = calculate(expression)
    except CalcError as e:
        return fail(str(e), 400)
    except Exception:
        return fail("计算失败，请检查表达式", 500)

    # 成功计算后写入历史
    try:
        record = db.insert_history(expression, result)
    except Exception:
        # 历史写入失败不阻断计算
        record = None

    return ok({
        "expression": expression,
        "result": result,
        "record": record,
    }, 200)


# ============ 历史接口 ============

@app.route("/api/history", methods=["GET"])
def api_history_list():
    records = db.query_history(limit=100)
    return ok({"history": records}, 200)


@app.route("/api/history/<int:record_id>", methods=["DELETE"])
def api_history_delete(record_id):
    deleted = db.delete_history(record_id)
    if not deleted:
        return fail("记录不存在", 404)
    return ok({"deleted_id": record_id}, 200)


@app.route("/api/history", methods=["DELETE"])
def api_history_clear():
    count = db.clear_history()
    return ok({"deleted_count": count}, 200)


# ============ 健康检查 ============

@app.route("/")
def index():
    return jsonify({"message": "Calculator backend is running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)