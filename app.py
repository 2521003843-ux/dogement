import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# =========================================================
# 1. CẤU HÌNH TRANG & CHỦ ĐỀ SẮC XUÂN RỰC RỠ 🌸🧧
# =========================================================
st.set_page_config(
    page_title="Quản Lý Chi Tiêu Sắc Xuân 🌸🧧",
    page_icon="🧧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. HÀM TƯƠNG THÍCH BẢO VỆ STREAMLIT
# =========================================================
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def safe_toast(msg):
    if hasattr(st, "toast"):
        st.toast(msg)
    else:
        st.success(msg)

# =========================================================
# 3. KHỞI TẠO CƠ SỞ DỮ LIỆU SQLITE
# =========================================================
DB_FILE = "expense_spring_v1.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trans_date TEXT,
                trans_type TEXT,
                category TEXT,
                amount REAL,
                note TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                limit_amount REAL
            )
        """)
        
        # Thêm ngân sách mẫu nếu chưa có
        c.execute("SELECT COUNT(*) FROM budgets")
        if c.fetchone()[0] == 0:
            sample_budgets = [
                ("🌸 Mua Sắm Tết & Quà Cáp", 10000000),
                ("🧧 Lì Xì Đầu Năm", 5000000),
                ("🍲 Ăn Uống & Tiệc Tùng", 7000000),
                ("🚗 Di Chuyển & Vé Xe/Máy Bay", 4000000),
                ("👗 Quần Áo & Làm Đẹp", 3000000),
                ("💡 Hóa Đơn & Sinh Hoạt", 5000000),
                ("🛍️ Mua Sắm Hàng Ngày", 4000000)
            ]
            c.executemany("INSERT INTO budgets (category, limit_amount) VALUES (?, ?)", sample_budgets)

        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Lỗi CSDL: {e}")

init_db()

def add_transaction(trans_date, trans_type, category, amount, note):
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        c = conn.cursor()
        c.execute("""
            INSERT INTO transactions (trans_date, trans_type, category, amount, note)
            VALUES (?, ?, ?, ?, ?)
        """, (trans_date, trans_type, category, amount, note))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Lỗi thêm giao dịch: {e}")
        return False

def delete_transaction(trans_id):
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def load_transactions():
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        df = pd.read_sql("SELECT * FROM transactions ORDER BY trans_date DESC, id DESC", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def load_budgets():
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        df = pd.read_sql("SELECT * FROM budgets", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def update_budget(category, limit_amount):
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO budgets (category, limit_amount) VALUES (?, ?)", (category, limit_amount))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

# =========================================================
# 4. CSS TRANG TRÍ CHỦ ĐỀ MÀU SẮC TẾT & MÙA XUÂN RỰC RỠ 🌸🧧
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #FFF5F5 0%, #FFF0F2 50%, #FFFAFA 100%);
    }

    /* HEADER BANNER SẮC XUÂN */
    .spring-header {
        background: linear-gradient(135deg, #B91C1C 0%, #D97706 50%, #991B1B 100%);
        border-radius: 24px;
        padding: 30px 25px;
        color: #FFFFFF;
        box-shadow: 0 12px 30px rgba(185, 28, 28, 0.25);
        border: 2px solid #FBBF24;
        margin-bottom: 25px;
        text-align: center;
        position: relative;
    }

    .spring-header h1 {
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        color: #FEF08A !important;
        margin-bottom: 6px !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .spring-header p {
        font-size: 1.1rem;
        color: #FFEDD5;
        margin: 0;
        font-weight: 500;
    }

    /* CARDS VÀ METRIC BADGES */
    .metric-box-income {
        background: #F0FDF4;
        border: 2px solid #22C55E;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(34, 197, 94, 0.08);
    }

    .metric-box-expense {
        background: #FEF2F2;
        border: 2px solid #EF4444;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.08);
    }

    .metric-box-balance {
        background: #FEFCE8;
        border: 2px solid #EAB308;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(234, 179, 8, 0.12);
    }

    /* CARD KHU VỰC THẺ BÀI */
    .spring-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 22px;
        border: 1px solid #FECDD3;
        box-shadow: 0 8px 24px rgba(225, 29, 72, 0.05);
        margin-bottom: 20px;
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #881337 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFE4E
