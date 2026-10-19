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
DB_FILE = "expense_spring_v2.db"

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
        
        c.execute("SELECT COUNT(*) FROM budgets")
        if c.fetchone()[0] == 0:
            sample_budgets = [
                ("🌸 Mua Sắm Tết & Quà Cáp", 10000000.0),
                ("🧧 Lì Xì Đầu Năm", 5000000.0),
                ("🍲 Ăn Uống & Tiệc Tùng", 7000000.0),
                ("🚗 Di Chuyển & Vé Xe/Máy Bay", 4000000.0),
                ("👗 Quần Áo & Làm Đẹp", 3000000.0),
                ("💡 Hóa Đơn & Sinh Hoạt", 5000000.0),
                ("🛍️ Mua Sắm Hàng Ngày", 4000000.0)
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
# 4. CSS TRANG TRÍ CHỦ ĐỀ TẾT SẮC XUÂN 🌸🧧
# =========================================================
css_code = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #FFF5F5 0%, #FFF0F2 50%, #FFFAFA 100%);
    }

    .spring-header {
        background: linear-gradient(135deg, #B91C1C 0%, #D97706 50%, #991B1B 100%);
        border-radius: 24px;
        padding: 30px 25px;
        color: #FFFFFF;
        box-shadow: 0 12px 30px rgba(185, 28, 28, 0.25);
        border: 2px solid #FBBF24;
        margin-bottom: 25px;
        text-align: center;
    }

    .spring-header h1 {
        font-weight: 800 !important;
        font-size: 2.3rem !important;
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

    .spring-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 22px;
        border: 1px solid #FECDD3;
        box-shadow: 0 8px 24px rgba(225, 29, 72, 0.05);
        margin-bottom: 20px;
    }

    [data-testid="stSidebar"] {
        background-color: #881337 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFE4E6 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255, 255, 255, 0.08);
        padding: 12px 16px;
        border-radius: 14px;
        margin-bottom: 6px;
        border: 1px solid rgba(251, 191, 36, 0.2);
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(251, 191, 36, 0.25);
    }

    .stButton>button {
        border-radius: 12px !important;
        font-weight: 700 !important;
    }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# Danh mục Thu / Chi
INCOME_CATEGORIES = [
    "🧧 Tiền Lì Xì / Thưởng Tết",
    "💼 Lương / Thu Nhập Chính",
    "📈 Đầu Tư / Tiết Kiệm",
    "🎁 Quà Tặng / Bán Hàng",
    "🔹 Thu Nhập Khác"
]

EXPENSE_CATEGORIES = [
    "🌸 Mua Sắm Tết & Quà Cáp",
    "🧧 Lì Xì Đầu Năm",
    "🍲 Ăn Uống & Tiệc Tùng",
    "🚗 Di Chuyển & Vé Xe/Máy Bay",
    "👗 Quần Áo & Làm Đẹp",
    "💡 Hóa Đơn & Sinh Hoạt",
    "🛍️ Mua Sắm Hàng Ngày",
    "🔻 Chi Phí Khác"
]

# Sidebar Menu
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #FEF08A; font-size: 1.8rem; font-weight:800;'>🌸 SỔ THU CHI XUÂN</h1>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center; color: #FECDD3;'>Quản Lý Tài Chính Rực Rỡ & May Mắn ✨</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "📌 Menu Chức Năng:",
        [
            "📊 Tổng Quan Thu Chi",
            "💸 Nhập Giao Dịch Nhanh",
            "📜 Sổ Nhật Ký Giao Dịch",
            "🎯 Ngân Sách Hạn Mức Tết",
            "📖 Hướng Dẫn Sử Dụng App"
        ]
    )

# Banner trang chủ
banner_html = """
<div class="spring-header">
    <h1>🌸 QUẢN LÝ CHI TIÊU SẮC XUÂN 🧧</h1>
    <p>Thu Chi Rõ Ràng - Cả Năm An Kang, Tấn Tài Tấn Lộc ✨</p>
</div>
"""
st.markdown(banner_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 1: TỔNG QUAN THU CHI
# ---------------------------------------------------------
if menu == "📊 Tổng Quan Thu Chi":
    st.subheader("📊 Báo Cáo Tổng Quan Tài Chính Real-time")
    
    df = load_transactions()
    
    if df.empty:
        st.info("💡 Chưa có dữ liệu giao dịch. Bạn hãy bấm vào menu '💸 Nhập Giao Dịch Nhanh' để bắt đầu ghi chép nhé!")
    else:
        df_income = df[df["trans_type"] == "Thu"]
        df_expense = df[df["trans_type"] == "Chi"]
        
        tot_income = df_income["amount"].sum() if not df_income.empty else 0.0
        tot_expense = df_expense["amount"].sum() if not df_expense.empty else 0.0
        balance = tot_income - tot_expense

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
                <div class="metric-box-income">
                    <h4 style="margin:0; color:#166534;">📈 TỔNG THU NHẬP</h4>
                    <h2 style="margin:10px 0 0 0; color:#15803D;">+{tot_income:,.0f} VNĐ</h2>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class="metric-box-expense">
                    <h4 style="margin:0; color:#991B1B;">📉 TỔNG CHI TIÊU</h4>
                    <h2 style="margin:10px 0 0 0; color:#B91C1C;">-{tot_expense:,.0f} VNĐ</h2>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            bal_color = "#D97706" if balance >= 0 else "#DC2626"
            st.markdown(f"""
                <div class="metric-box-balance">
                    <h4 style="margin:0; color:#854D0E;">💰 SỐ DƯ HIỆN TẠI</h4>
                    <h2 style="margin:10px 0 0 0; color:{bal_color};">{balance:,.0f} VNĐ</h2>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("### 📊 Phân Phối Chi Tiêu Theo Danh Mục")
            if not df_expense.empty:
                expense_by_cat = df_expense.groupby("category")["amount"].sum().reset_index()
                st.dataframe(
                    expense_by_cat.style.format({"amount": "{:,.0f} VNĐ"}),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.caption("Chưa có giao dịch chi tiêu nào.")

        with col_g2:
            st.markdown("### 📈 Biểu Đồ So Sánh Thu vs Chi")
            df_chart = pd.DataFrame({
                "Loại": ["Tổng Thu", "Tổng Chi"],
                "Số Tiền (VNĐ)": [tot_income, tot_expense]
            })
            st.bar_chart(df_chart, x="Loại", y="Số Tiền (VNĐ)")

# ---------------------------------------------------------
# MENU 2: NHẬP GIAO DỊCH NHANH
# ---------------------------------------------------------
elif menu == "💸 Nhập Giao Dịch Nhanh":
    st.subheader("💸 Nhập Giao Dịch Mới (Thu / Chi)")
    st.caption("Thiết kế tối giản giúp bạn ghi chép khoản tiền thu hoặc chi chỉ trong vài giây!")

    with st.container():
        st.markdown('<div class="spring-card">', unsafe_allow_html=True)
        
        c_type, c_date = st.columns([1, 1])
        with c_type:
            trans_type = st.radio("Chọn Loại Giao Dịch:", ["Chi (Tiêu Tiền 🔴)", "Thu (Nhận Tiền 🟢)"], horizontal=True)
        with c_date:
            trans_date = st.date_input("Ngày Giao Dịch:", datetime.now())

        is_expense = "Chi" in trans_type
        cat_options = EXPENSE_CATEGORIES if is_expense else INCOME_CATEGORIES

        c_cat, c_amt = st.columns([1, 1])
        with c_cat:
            category = st.selectbox("Danh Mục:", cat_options)
        with c_amt:
            amount = st.number_input("Số Tiền (VNĐ):", min_value=1000.0, step=10000.0, value=50000.0, format="%.0f")

        note = st.text_input("Ghi Chú Nhanh (VD: Mua bánh chưng, Tiền lì xì cháu...):", placeholder="Thêm mô tả ngắn...")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 LƯU GIAO DỊCH NGAY", type="primary", use_container_width=True):
            type_clean = "Chi" if is_expense else "Thu"
            date_str = trans_date.strftime("%Y-%m-%d")
            if add_transaction(date_str, type_clean, category, amount, note):
                safe_toast(f"🎉 Đã lưu giao dịch {type_clean}: {amount:,.0f} VNĐ!")
                safe_rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 3: SỔ NHẬT KÝ GIAO DỊCH
# ---------------------------------------------------------
elif menu == "📜 Sổ Nhật Ký Giao Dịch":
    st.subheader("📜 Nhật Ký & Lịch Sử Giao Dịch")
    
    df = load_transactions()
    if df.empty:
        st.warning("Chưa có giao dịch nào được lưu.")
    else:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_type = st.selectbox("Lọc Loại:", ["Tất Cả", "Thu", "Chi"])
        with col_f2:
            search_note = st.text_input("🔍 Tìm Kiếm Theo Ghi Chú / Danh Mục:", placeholder="Nhập từ khóa...")

        df_filtered = df.copy()
        if filter_type != "Tất Cả":
            df_filtered = df_filtered[df_filtered["trans_type"] == filter_type]
        if search_note:
            df_filtered = df_filtered[
                df_filtered["note"].str.contains(search_note, case=False, na=False) | 
                df_filtered["category"].str.contains(search_note, case=False, na=False)
            ]

        st.write(f"📌 Tìm thấy **{len(df_filtered)}** giao dịch:")
        
        st.dataframe(
            df_filtered.rename(columns={
                "id": "ID",
                "trans_date": "Ngày",
                "trans_type": "Loại",
                "category": "Danh Mục",
                "amount": "Số Tiền (VNĐ)",
                "note": "Ghi Chú"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")
        st.markdown("### ❌ Xóa Giao Dịch Nhầm")
        col_d1, col_d2 = st.columns([3, 1])
        with col_d1:
            del_id = st.number_input("Nhập ID Giao Dịch Cần Xóa:", min_value=1, step=1)
        with col_d2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Xóa Giao Dịch", type="secondary", use_container_width=True):
                if delete_transaction(del_id):
                    safe_toast(f"Đã xóa thành công giao dịch ID #{del_id}!")
                    safe_rerun()
                else:
                    st.error("Không tìm thấy ID giao dịch cần xóa!")

# ---------------------------------------------------------
# MENU 4: NGÂN SÁCH HẠN MỨC TẾT
# ---------------------------------------------------------
elif menu == "🎯 Ngân Sách Hạn Mức Tết":
    st.subheader("🎯 Quản Lý Ngân Sách & Cảnh Báo Bội Chi")
    st.caption("Đặt hạn mức cho từng khoản chi Tết để kiểm soát chi tiêu không bị vượt mức cho phép!")

    df_trans = load_transactions()
    df_budgets = load_budgets()

    df_expense = df_trans[df_trans["trans_type"] == "Chi"] if not df_trans.empty else pd.DataFrame()

    for idx, row in df_budgets.iterrows():
        cat_name = row["category"]
        limit_val = row["limit_amount"]

        spent_val = 0.0
        if not df_expense.empty:
            spent_val = float(df_expense[df_expense["category"] == cat_name]["amount"].sum())

        pct = min(1.0, spent_val / limit_val) if limit_val > 0 else 0.0

        st.markdown(f"#### {cat_name}")
        c_b1, c_b2 = st.columns([3, 1])
        with c_b1:
            st.progress(pct)
            st.write(f"Đã chi: **{spent_val:,.0f} VNĐ** / Hạn mức: **{limit_val:,.0f} VNĐ** (Đã dùng {pct*100:.1f}%)")
            if spent_val > limit_val:
                st.error(f"🚨 **CẢNH BÁO:** Bạn đã chi vượt hạn mức **{(spent_val - limit_val):,.0f} VNĐ**!")
        with c_b2:
            new_limit = st.number_input(f"Đổi hạn mức:", min_value=0.0, value=float(limit_val), step=500000.0, key=f"bud_{idx}")
            if new_limit != limit_val:
                update_budget(cat_name, new_limit)
                safe_toast(f"Đã cập nhật hạn mức {cat_name}!")
                safe_rerun()

        st.markdown("---")

# ---------------------------------------------------------
# MENU 5: HƯỚNG DẪN SỬ DỤNG APP
# ---------------------------------------------------------
else:
    st.subheader("📖 Hướng Dẫn Sử Dụng App Quản Lý Chi Tiêu Sắc Xuân 🌸")
    st.caption("Chào mừng bạn đến với ứng dụng quản lý tài chính cá nhân & mua sắm Tết thông minh!")

    tab_g1, tab_g2, tab_g3, tab_g4 = st.tabs([
        "🚀 Bắt Đầu Nhanh", 
        "💸 Cách Nhập Thu Chi", 
        "🎯 Đặt Ngân Sách Tết", 
        "💡 Mẹo Tiết Kiệm Ngày Tết"
    ])

    with tab_g1:
        st.markdown("""
        ### 🌟 3 Bước Quản Lý Tài Chính Dễ Dàng:
        1. **Bước 1 (Nhập Tiền):** Truy cập menu **`💸 Nhập Giao Dịch Nhanh`**, chọn giao dịch **Thu** (Lương, Lì xì...) hoặc **Chi** (Mua sắm, Ăn uống...).
        2. **Bước 2 (Theo Dõi):** Xem tình hình số dư real-time & biểu đồ tại **`📊 Tổng Quan Thu Chi`**.
        3. **Bước 3 (Kiểm Soát):** Cài đặt hạn mức tại **`🎯 Ngân Sách Hạn Mức Tết`** để nhận cảnh báo màu đỏ khi chi tiêu quá tay.
        """)

    with tab_g2:
        st.markdown("""
        ### 💸 Hướng Dẫn Ghi Chép Chuẩn Xác:
        * **Loại Thu:** Nhập tiền lì xì nhận được, tiền thưởng Tết, lương tháng, hoặc tiền bán hàng.
        * **Loại Chi:** Nhập tiền mua quà biếu, vé xe/máy bay, sắm đồ trang trí, tiệc tùng đầu năm.
        * **Ghi Chú:** Nên ghi chú cụ thể (Ví dụ: *Táo ngoại biếu ông bà, Vé xe về quê*) để dễ tìm kiếm lại sau này trong menu **`📜 Sổ Nhật Ký Giao Dịch`**.
        """)

    with tab_g3:
        st.markdown("""
        ### 🎯 Cách Thiết Lập Ngân Sách Tránh "Cháy Túi":
        * Truy cập **`🎯 Ngân Sách Hạn Mức Tết`**.
        * Nhập số tiền tối đa bạn dự định chi cho từng mục (Ví dụ: Lì xì tối đa `5.000.000đ`, Ăn uống `7.000.000đ`).
        * Thanh tiến trình sẽ hiển thị phần trăm đã dùng và **báo động đỏ 🚨** ngay khi bạn chi tiêu vượt hạn mức.
        """)

    with tab_g4:
        st.markdown("""
        ### 💡 Mẹo Chi Tiêu Tết Thông Minh & May Mắn:
        * 🧧 **Lên danh sách mua sắm trước:** Tránh mua ngẫu hứng các món đồ trang trí/thực phẩm không dùng đến.
        * 🛍️ **Tách riêng quỹ Lì Xì & Quỹ Mua Sắm:** Giúp bạn chủ động nguồn tiền mặt.
        * 📊 **Cập nhật giao dịch mỗi ngày:** Dành 1 phút cuối ngày nhập thu chi để sổ sách luôn chính xác 100%.
        """)
