import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# =========================================================
# 1. CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Sổ Thu Chi Xuân 🌸",
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

def safe_toast(msg, icon="✅"):
    if hasattr(st, "toast"):
        st.toast(msg, icon=icon)
    else:
        st.success(msg)

# =========================================================
# 3. CƠ SỞ DỮ LIỆU SQLITE
# =========================================================
DB_FILE = "expense_spring_v3.db"

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trans_date TEXT, trans_type TEXT, category TEXT, amount REAL, note TEXT
        )
    """)
    c.execute("CREATE TABLE IF NOT EXISTS budgets (category TEXT PRIMARY KEY, limit_amount REAL)")
    
    c.execute("SELECT COUNT(*) FROM budgets")
    if c.fetchone()[0] == 0:
        sample_budgets = [
            ("🌸 Mua Sắm Tết", 10000000.0), ("🧧 Lì Xì Đi", 5000000.0), 
            ("🍲 Ăn Uống Tiệc", 7000000.0), ("🚗 Di Chuyển", 4000000.0)
        ]
        c.executemany("INSERT INTO budgets VALUES (?, ?)", sample_budgets)
    conn.commit()
    conn.close()

init_db()

def add_transaction(date, type_, cat, amt, note):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO transactions (trans_date, trans_type, category, amount, note) VALUES (?, ?, ?, ?, ?)", 
              (date, type_, cat, amt, note))
    conn.commit()
    conn.close()

def delete_transaction(tid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ?", (tid,))
    conn.commit()
    conn.close()

def load_data(table, order_by=""):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql(f"SELECT * FROM {table} {order_by}", conn)
    conn.close()
    return df

def update_budget(cat, amt):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO budgets VALUES (?, ?)", (cat, amt))
    conn.commit()
    conn.close()

# =========================================================
# 4. TRANG TRÍ GIAO DIỆN TỐI GIẢN & SẮC XUÂN 🌸
# =========================================================
st.markdown("""
<style>
    /* Nền tảng sạch, font chữ hiện đại */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    
    .stApp { background-color: #FFFBFB; } /* Màu nền trắng kem ấm */
    
    /* Các thẻ hiển thị chỉ số tối giản */
    .metric-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: 1px solid #FFEBEE;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .m-title { font-size: 1rem; color: #757575; font-weight: 600; margin-bottom: 5px; }
    .m-val-in { font-size: 1.8rem; color: #2E7D32; font-weight: 800; }
    .m-val-out { font-size: 1.8rem; color: #D32F2F; font-weight: 800; }
    .m-val-bal { font-size: 1.8rem; color: #F57F17; font-weight: 800; }
    
    /* Giao diện nút bấm & viền */
    .stButton>button {
        border-radius: 30px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease;
    }
    
    /* Sidebar Tết */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #D32F2F 0%, #B71C1C 100%) !important;
    }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.1);
        border-radius: 10px; padding: 10px; margin-bottom: 5px;
    }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.2); }
</style>
""", unsafe_allow_html=True)

# Danh mục
INCOME_CATS = ["🧧 Tiền Lì Xì", "💼 Lương / Thưởng", "🎁 Quà Biếu", "🔹 Khác"]
EXPENSE_CATS = ["🌸 Mua Sắm Tết", "🧧 Lì Xì Đi", "🍲 Ăn Uống Tiệc", "🚗 Di Chuyển", "👗 Làm Đẹp", "🔻 Khác"]

# =========================================================
# 5. SIDEBAR & HƯỚNG DẪN ẨN TRONG ICON ℹ️
# =========================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FFD54F;'>🌸 SỔ THU CHI XUÂN</h2>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1548005391-7649d2dd962b?q=80&w=400&auto=format&fit=crop", use_container_width=True) # Ảnh lồng đèn đỏ
    
    # --- TÍNH NĂNG MỚI: Hướng dẫn gọn trong icon (Popover) ---
    with st.popover("ℹ️ Hướng Dẫn Sử Dụng App"):
        st.markdown("""
        **👋 Chào bạn, đây là sổ tay thần tài của bạn!**
        * **Nhập Thu/Chi:** Vào *Ghi Chép Giao Dịch*, chọn loại tiền, nhập số và lưu lại.
        * **Ngân Sách:** Cài giới hạn tiền tiêu cho Tết ở tab *Quản Lý Ngân Sách* để không bị lẹm vốn.
        * **Xuất File:** Bạn có thể tải toàn bộ sao kê ra Excel (CSV) ở phần *Sổ Nhật Ký*.
        * *Mẹo:* Hãy ghi chú thật rõ để sau Tết ngồi đếm lại cho vui nhé! 🧧
        """)
        
    st.markdown("---")
    menu = st.radio("📌 TÍNH NĂNG CHÍNH", ["📊 Báo Cáo Tổng Quan", "✍️ Ghi Chép Giao Dịch", "📜 Sổ Nhật Ký & Xuất File", "🎯 Quản Lý Ngân Sách"])

# =========================================================
# 6. GIAO DIỆN CHÍNH (MAIN CONTENT)
# =========================================================

if menu == "📊 Báo Cáo Tổng Quan":
    st.markdown("### 🌸 Bức Tranh Tài Chính Đầu Năm")
    df = load_data("transactions", "ORDER BY trans_date DESC")
    
    if df.empty:
        st.info("Nhập khoản tiền đầu tiên của bạn ở mục **Ghi Chép Giao Dịch** để làm đỏ sổ nhé! ✨")
    else:
        df_in = df[df["trans_type"] == "Thu"]
        df_out = df[df["trans_type"] == "Chi"]
        
        t_in = df_in["amount"].sum() if not df_in.empty else 0
        t_out = df_out["amount"].sum() if not df_out.empty else 0
        
        # --- TÍNH NĂNG MỚI: Hũ Vàng Lì Xì ---
        lixi_in = df_in[df_in["category"] == "🧧 Tiền Lì Xì"]["amount"].sum() if not df_in.empty else 0
        
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-card"><div class="m-title">Tổng Thu</div><div class="m-val-in">+{t_in/1e6:.1f}tr</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="m-title">Tổng Chi</div><div class="m-val-out">-{t_out/1e6:.1f}tr</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="m-title">Số Dư Tồn</div><div class="m-val-bal">{(t_in-t_out)/1e6:.1f}tr</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-card"><div class="m-title">🏺 Lộc Lì Xì</div><div class="m-val-in">{lixi_in/1e6:.1f}tr</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_g1, col_g2 = st.columns([1, 1])
        with col_g1:
            st.markdown("**Biểu Đồ Chi Tiêu (VNĐ)**")
            if not df_out.empty:
                st.bar_chart(df_out.groupby("category")["amount"].sum())
        with col_g2:
            st.markdown("**Dòng Tiền Thu Gần Nhất**")
            if not df_in.empty:
                st.dataframe(df_in.head(5)[["trans_date", "category", "amount"]].style.format({"amount": "{:,.0f}"}), hide_index=True, use_container_width=True)

elif menu == "✍️ Ghi Chép Giao Dịch":
    st.markdown("### ✍️ Ghi Chép Nhanh Chóng")
    
    with st.container():
        st.markdown('<div class="metric-card" style="text-align: left;">', unsafe_allow_html=True)
        
        c_type, c_date = st.columns(2)
        trans_type = c_type.selectbox("Phân Loại", ["Chi (Tiêu tiền 🔴)", "Thu (Nhận tiền 🟢)"])
        t_date = c_date.date_input("Ngày thực hiện", datetime.now())
        
        is_exp = "Chi" in trans_type
        c_cat, c_amt = st.columns(2)
        category = c_cat.selectbox("Danh Mục", EXPENSE_CATS if is_exp else INCOME_CATS)
        amount = c_amt.number_input("Số Tiền (VNĐ)", min_value=1000.0, step=10000.0, value=50000.0)
        
        note = st.text_input("Ghi Chú Nhanh", placeholder="Ví dụ: Lì xì bé Na, Mua mứt Tết...")
        
        if st.button("💾 Ghi Vào Sổ", type="primary", use_container_width=True):
            clean_type = "Chi" if is_exp else "Thu"
            add_transaction(t_date.strftime("%Y-%m-%d"), clean_type, category, amount, note)
            safe_toast(f"Ting ting! Đã ghi nhận {clean_type} {amount:,.0f}đ 💰", icon="🧧")
            safe_rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📜 Sổ Nhật Ký & Xuất File":
    st.markdown("### 📜 Lịch Sử Giao Dịch & Sao Kê")
    
    df = load_data("transactions", "ORDER BY trans_date DESC, id DESC")
    if df.empty:
        st.warning("Chưa có giao dịch.")
    else:
        # --- TÍNH NĂNG MỚI: Xuất Dữ Liệu Excel (CSV) ---
        c_search, c_export = st.columns([3, 1])
        search = c_search.text_input("🔍 Tìm kiếm theo Ghi chú / Mục")
        
        df_show = df[df["note"].str.contains(search, case=False, na=False) | df["category"].str.contains(search, case=False, na=False)] if search else df
        
        csv_data = df_show.to_csv(index=False).encode('utf-8-sig')
        c_export.markdown("<br>", unsafe_allow_html=True)
        c_export.download_button(label="📥 Tải Báo Cáo (CSV)", data=csv_data, file_name="Sao_Ke_Tet.csv", mime="text/csv", use_container_width=True)
        
        st.dataframe(df_show.rename(columns={"id":"ID", "trans_date":"Ngày", "trans_type":"Loại", "category":"Mục", "amount":"Số Tiền", "note":"Ghi Chú"}).style.format({"Số Tiền": "{:,.0f}"}), use_container_width=True, hide_index=True)

        st.markdown("---")
        with st.expander("❌ Sửa / Xóa Giao Dịch Nhầm"):
            del_id = st.number_input("Nhập ID cần xóa", min_value=1, step=1)
            if st.button("Xóa ID này"):
                delete_transaction(del_id)
                safe_toast("Đã xóa giao dịch!")
                safe_
