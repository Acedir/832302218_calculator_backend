"""
database.py
SQLite 数据库操作：初始化、插入、查询、删除计算历史。
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "calculator.db")


def get_conn():
    """获取数据库连接（每次调用都新建，线程安全）"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # 让查询结果能像字典一样访问
    return conn


def init_db():
    """初始化表结构；如果表已存在则不动"""
    conn = get_conn()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS calculation_history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                expression  TEXT    NOT NULL,
                result      TEXT    NOT NULL,
                created_at  TEXT    NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def insert_history(expression: str, result) -> dict:
    """插入一条历史记录，返回新记录（含 id）"""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO calculation_history (expression, result, created_at) "
            "VALUES (?, ?, ?)",
            (expression, str(result), created_at),
        )
        conn.commit()
        new_id = cur.lastrowid
        return {
            "id": new_id,
            "expression": expression,
            "result": result,
            "created_at": created_at,
        }
    finally:
        conn.close()


def query_history(limit: int = 100) -> list:
    """按时间倒序查询历史记录"""
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT id, expression, result, created_at "
            "FROM calculation_history "
            "ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_history(record_id: int) -> bool:
    """删除指定 id 的记录；返回是否真的删掉了"""
    conn = get_conn()
    try:
        cur = conn.execute(
            "DELETE FROM calculation_history WHERE id = ?",
            (record_id,),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def clear_history() -> int:
    """清空所有历史；返回删除条数"""
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM calculation_history")
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()