import ast

app_code = '''import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import json

# ---------------------------------------------------------
# 1. KHỞI TẠO CƠ SỞ DỮ LIỆU SQLITE
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect("dogemnet.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            income REAL,
            age INTEGER,
            gender TEXT,
            marital_status TEXT,
            housing_status TEXT,
            dependents INTEGER,
            monthly_debt REAL,
            current_savings REAL,
            risk_appetite TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS savings_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            target REAL,
            current REAL,
            target_date TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS debts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL,
            interest_rate REAL,
            min_pay REAL
        )
    """)
    
    # Kiểm tra nếu chưa có hồ sơ thì tạo mặc định
    c.execute("SELECT COUNT(*) FROM profile")
    if c.fetchone()[0] == 0:
        c.execute("""
            INSERT INTO profile (id, income, age, gender, marital_status, housing_status, dependents, monthly_debt, current_savings, risk_appetite)
            VALUES (1, 20000000, 26, 'Nam', 'Độc thân', 'Đang ở trọ / Đi thuê', 0, 0, 30000000, 'Cân bằng')
        """)
    
    # Thêm dữ liệu mẫu nếu bảng thu chi trống
    c.execute("SELECT COUNT(*) FROM expenses")
    if c.fetchone()[0] == 0:
        sample_expenses = [
            ("17/10/2026", "Thiết yếu (Needs)", "Tiền thuê nhà & dịch vụ", 4500000),
            ("17/10/2026", "Thiết yếu (Needs)", "Đi siêu thị thực phẩm", 2800000),
            ("16/10/2026", "Sở thích (Wants)", "Cà phê & Đi xem phim", 450000),
            ("15/10/2026", "Tích lũy & Đầu tư (Savings)", "Gửi tiết kiệm tích lũy", 3000000)
        ]
        c.executemany("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)", sample_expenses)
        
    # Thêm dữ liệu mẫu hũ tiết kiệm nếu trống
    c.execute("SELECT COUNT(*) FROM savings_goals")
    if c.fetchone()[0] == 0:
        sample_goals = [
            ("Mua iPhone mới 📱", 30000000, 12000000, "2026-12-31"),
            ("Quỹ Du Lịch Nhật Bản 🌸", 40000000, 25000000, "2027-04-30"),
            ("Mua Xe Máy Mới 🛵", 50000000, 15000000, "2027-08-31")
        ]
        c.executemany("INSERT INTO savings_goals (name, target, current, target_date) VALUES (?, ?, ?, ?)", sample_goals)

    conn.commit()
    conn.close()

init_db()

# Các hàm thao tác DB
def load_profile():
    conn = sqlite3.connect("dogemnet.db")
    df = pd.read_sql("SELECT * FROM profile WHERE id=1", conn)
    conn.close()
    return df.iloc[0].to_dict()

def save_profile(data):
    conn = sqlite3.connect("dogemnet.db")
    c = conn.cursor()
    c.execute("""
        UPDATE profile SET income=?, age=?, gender=?, marital_status=?, housing_status=?, 
        dependents=?, monthly_debt=?, current_savings=?, risk_appetite=? WHERE id=1
    """, (data['income'], data['age'], data['gender'], data['marital_status'], data['housing_status'],
          data['dependents'], data['monthly_debt'], data['current_savings'], data['risk_appetite']))
    conn.commit()
    conn.close()

def load_expenses():
    conn = sqlite3.connect("dogemnet.db")
    df = pd.read_sql("SELECT * FROM expenses ORDER BY id DESC", conn)
    conn.close()
    return df

def add_expense(date, category, description, amount):
    conn = sqlite3.connect("dogemnet.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)", (date, category, description, amount))
    conn.commit()
    conn.close()

def load_goals():
    conn = sqlite3.connect("dogemnet.db")
    df = pd.read_sql("SELECT * FROM savings_goals", conn)
    conn.close()
    return df

def add_goal(name, target, current, target_date):
    conn = sqlite3.connect("dogemnet.db")
    c = conn.cursor()
    c.execute("INSERT INTO savings_goals (name, target, current, target_date) VALUES (?, ?, ?, ?)", (name, target, current, target_date))
    conn.commit()
    conn.close()

def update_goal_savings(goal_id, add_amount):
    conn = sqlite3.connect("dogemnet.db")
    c = conn.cursor()
    c.execute("UPDATE savings_goals SET current = current + ? WHERE id = ?", (add_amount, goal_id))
    conn.commit()
    conn.close()

def load_debts():
    conn = sqlite3.connect("dogemnet.db")
    df = pd.read_sql("SELECT * FROM debts", conn)
    conn.close()
    return df

def add_debt(name, amount, rate, min_pay):
    conn = sqlite3.connect("dogemnet.db")
    c = conn.cursor()
    c.execute("INSERT INTO debts (name, amount, interest_rate, min_pay) VALUES (?, ?, ?, ?)", (name, amount, rate, min_pay))
    conn.commit()
    conn.close()

def delete_debt(debt_id):
    conn = sqlite3.connect("dogemnet.db")
    c = conn.cursor()
    c.execute("DELETE FROM debts WHERE id = ?", (debt_id,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# 2. CẤU HÌNH TRANG & GIAO DIỆN SẮC MÀU VIBRANT DOGE 🐶
# ---------------------------------------------------------
st.set_page_config(
    page_title="DOGEMNET Super App 🐶 - Quản Lý Tài Chính Cá Nhân",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS siêu sặc sỡ, trẻ trung & sinh động
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #FFFBEB 0%, #F8FAFC 100%);
    }

    /* BANNER SIÊU SẮC MÀU DOGEMNET */
    .doge-hero-banner {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 30%, #F59E0B 70%, #8B5CF6 100%);
        border-radius: 24px;
        padding: 35px 30px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.25);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 3px solid #FFFFFF;
    }
    
    .doge-hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 8px;
        text-shadow: 2px 3px 8px rgba(0,0,0,0.25);
    }
    
    .doge-hero-banner p {
        color: #FEF3C7;
        font-size: 1.15rem;
        margin: 0;
        font-weight: 600;
    }

    /* CARD KHUNG VIỀN MÀU SẮC */
    .card-vibrant-amber {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border-top: 6px solid #F59E0B;
        margin-bottom: 20px;
    }

    .card-vibrant-purple {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border-top: 6px solid #8B5CF6;
        margin-bottom: 20px;
    }

    .card-vibrant-emerald {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border-top: 6px solid #10B981;
        margin-bottom: 20px;
    }

    .card-vibrant-rose {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border-top: 6px solid #F43F5E;
        margin-bottom: 20px;
    }

    /* WIDGET TRẠNG THÁI THÚ CỦA DOGE (PET STATUS) */
    .doge-pet-status {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border: 2px dashed #F59E0B;
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* CHAT BOT CONTAINER */
    .chat-bubble-user {
        background: #D97706;
        color: white;
        border-radius: 18px 18px 0px 18px;
        padding: 12px 18px;
        margin: 8px 0;
        max-width: 80%;
        float: right;
        clear: both;
        font-weight: 500;
    }

    .chat-bubble-doge {
        background: #FFFFFF;
        color: #1E293B;
        border-radius: 18px 18px 18px 0px;
        padding: 14px 20px;
        margin: 8px 0;
        max-width: 85%;
        float: left;
        clear: both;
        border: 2px solid #FDE68A;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SIDEBAR: TỰ ĐỘNG ĐỒNG BỘ DỮ LIỆU TỪ SQLITE
# ---------------------------------------------------------
user_prof = load_profile()

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #D97706; margin-bottom:0;'>🐶 DOGEMNET</h1>", unsafe_allow_html=True)
    st.caption("<p style='text-align:center;'>🚀 Quản Lý Tài Chính AI & Game Hóa Số 1</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("⚙️ Hồ Sơ Người Dùng (Tự Động Lưu)")
    income = st.number_input("💵 Thu nhập hàng tháng (VNĐ):", min_value=1000000, value=int(user_prof['income']), step=1000000, format="%d")
    age = st.slider("🎂 Độ tuổi:", min_value=18, max_value=70, value=int(user_prof['age']))
    gender = st.selectbox("🚻 Giới tính:", ["Nam", "Nữ", "Khác"], index=["Nam", "Nữ", "Khác"].index(user_prof['gender']))
    marital_status = st.selectbox("💍 Tình trạng hôn nhân:", ["Độc thân", "Đã kết hôn (Chưa có con)", "Đã kết hôn (Có con nhỏ)", "Đã kết hôn (Con đã lớn)"], index=["Độc thân", "Đã kết hôn (Chưa có con)", "Đã kết hôn (Có con nhỏ)", "Đã kết hôn (Con đã lớn)"].index(user_prof['marital_status']))
    housing_status = st.selectbox("🏠 Tình trạng nhà ở:", ["Đang ở trọ / Đi thuê", "Ở cùng bố mẹ", "Đang trả góp mua nhà", "Sở hữu nhà riêng"], index=["Đang ở trọ / Đi thuê", "Ở cùng bố mẹ", "Đang trả góp mua nhà", "Sở hữu nhà riêng"].index(user_prof['housing_status']))
    dependents = st.number_input("👨‍👩‍👧‍👦 Số người phụ thuộc:", min_value=0, max_value=10, value=int(user_prof['dependents']))
    monthly_debt = st.number_input("💳 Khoản nợ/trả góp tháng (VNĐ):", min_value=0, value=int(user_prof['monthly_debt']), step=500000, format="%d")
    current_savings = st.number_input("🏦 Tiết kiệm hiện có (VNĐ):", min_value=0, value=int(user_prof['current_savings']), step=5000000, format="%d")
    risk_appetite = st.select_slider("🎯 Khẩu vị rủi ro:", options=["Rất an toàn", "An toàn", "Cân bằng", "Tăng trưởng", "Rất mạo hiểm"], value=user_prof['risk_appetite'])
    
    # Cập nhật DB khi người dùng thay đổi dữ liệu sidebar
    updated_data = {
        'income': income, 'age': age, 'gender': gender, 'marital_status': marital_status,
        'housing_status': housing_status, 'dependents': dependents, 'monthly_debt': monthly_debt,
        'current_savings': current_savings, 'risk_appetite': risk_appetite
    }
    save_profile(updated_data)

    st.markdown("---")
    selected_menu = st.radio(
        "📌 Menu Chức Năng:",
        [
            "📊 Phân Bổ Ngân Sách (50/30/20 & 6 Hũ)",
            "🏺 Hũ Tiết Kiệm Mục Tiêu (Goal Savings)",
            "💳 Mô Phỏng Xóa Nợ (Snowball vs Avalanche)",
            "🤖 AI Doge & Chatbot 'Hỏi Sếp Doge'",
            "📈 Dự Phòng & Tự Do Tài Chính (FIRE)",
            "📝 Sổ Thu Chi & SQLite Báo Cáo"
        ]
    )

# ---------------------------------------------------------
# 4. BANNER HERO VIBRANT & WIDGET "NUÔI DOGE TỐT SỐ"
# ---------------------------------------------------------
st.markdown("""
    <div class="doge-hero-banner">
        <h1>🐶 DOGEMNET SUPER FINANCIAL APP 🚀</h1>
        <p>"Làm Chủ Dòng Tiền - Nuôi Doge Tốt Số - Tự Do Tài Chính Vững Chắc"</p>
    </div>
""", unsafe_allow_html=True)

# TÍNH TOÁN TRẠNG THÁI "NUÔI DOGE TỐT SỐ" (GAMIFICATION)
df_exp_all = load_expenses()
total_spent_now = df_exp_all["amount"].sum() if not df_exp_all.empty else 0
spent_ratio = total_spent_now / income if income > 0 else 0

if spent_ratio <= 0.50:
    pet_avatar = "🐶🕶️"
    pet_status_title = "Sếp Doge Đại Gia - Rất Hài Lòng!"
    pet_msg = "Tuyệt vời! Bạn đang kiểm soát chi tiêu siêu đỉnh. Doge đang được ăn bò steak cao cấp 🥩!"
    pet_bg = "#D1FAE5"
    pet_border = "#10B981"
elif spent_ratio <= 0.85:
    pet_avatar = "🐶🍖"
    pet_status_title = "Sếp Doge Vui Vẻ - Đúng Kế Hoạch!"
    pet_msg = "Mọi thứ vẫn nằm trong tầm kiểm soát. Hãy tiếp tục duy trì thói quen tích lũy này nhé 🦴!"
    pet_bg = "#FEF3C7"
    pet_border = "#F59E0B"
else:
    pet_avatar = "🐶😭"
    pet_status_title = "Sếp Doge Cầu Cứu - Nguy Cơ Vỡ Quỹ!"
    pet_msg = f"Cảnh báo! Bạn đã tiêu hết **{spent_ratio*100:.1f}%** thu nhập tháng này. Cắt giảm các khoản 'Sở thích' ngay 🚨!"
    pet_bg = "#FFE4E6"
    pet_border = "#F43F5E"

st.markdown(f"""
    <div class="doge-pet-status" style="background-color: {pet_bg}; border-color: {pet_border};">
        <div style="font-size: 2.8rem; margin-bottom: 5px;">{pet_avatar}</div>
        <h3 style="margin: 0; color: #1E293B;">{pet_status_title}</h3>
        <p style="margin: 5px 0 0 0; color: #475569; font-weight: 600;">{pet_msg}</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. XỬ LÝ NỘI DUNG TỪNG MENU
# ---------------------------------------------------------

# =========================================================
# CHỨC NĂNG 1: PHÂN BỔ NGÂN SÁCH (50/30/20 & 6 HŨ)
# =========================================================
if selected_menu == "📊 Phân Bổ Ngân Sách (50/30/20 & 6 Hũ)":
    st.subheader("📊 Tự Động Phân Bổ Ngân Sách Dựa Trên Hoàn Cảnh Cá Nhân")

    needs_pct, wants_pct, savings_pct = 50, 30, 20
    adjustment_reasons = []

    if housing_status in ["Đang ở trọ / Đi thuê", "Đang trả góp mua nhà"]:
        needs_pct += 5
        wants_pct -= 5
        adjustment_reasons.append("Tăng 5% Nhu cầu thiết yếu do chi phí nhà ở/trả góp")
    
    if dependents > 0:
        add_n = min(10, dependents * 5)
        needs_pct += add_n
        wants_pct -= add_n
        adjustment_reasons.append(f"Tăng {add_n}% Nhu cầu thiết yếu do nuôi người phụ thuộc")

    total_p = needs_pct + wants_pct + savings_pct
    needs_pct = round((needs_pct / total_p) * 100)
    wants_pct = round((wants_pct / total_p) * 100)
    savings_pct = 100 - needs_pct - wants_pct

    needs_val = income * (needs_pct / 100)
    wants_val = income * (wants_pct / 100)
    savings_val = income * (savings_pct / 100)

    st.markdown("<div class='card-vibrant-amber'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Tỷ Lệ Ngân Sách 50/30/20 Khuyên Dùng")
    if adjustment_reasons:
        st.info("💡 **Hệ thống cá nhân hóa:** " + " | ".join(adjustment_reasons))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(f"🏠 Thiết Yếu ({needs_pct}%)", f"{needs_val:,.0f} VNĐ")
    with c2:
        st.metric(f"🎉 Sở Thích ({wants_pct}%)", f"{wants_val:,.0f} VNĐ")
    with c3:
        st.metric(f"🚀 Tích Lũy ({savings_pct}%)", f"{savings_val:,.0f} VNĐ")
    
    df_chart_50 = pd.DataFrame({
        "Hạng mục": ["Thiết yếu (Needs)", "Sở thích (Wants)", "Tích lũy & Đầu tư (Savings)"],
        "Số tiền": [needs_val, wants_val, savings_val]
    })
    st.bar_chart(df_chart_50, x="Hạng mục", y="Số tiền", color="#F59E0B")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card-vibrant-purple'>", unsafe_allow_html=True)
    st.markdown("### 🏺 Quy Tắc 6 Hũ Tài Chính (Six Jars Method)")
    jars = {
        "📦 1. Thiết Yếu (NEC - 55%)": (0.55, "Thức ăn, hóa đơn, nhà ở, y tế"),
        "📈 2. Tự Do Tài Chính (FFA - 10%)": (0.10, "Đầu tư sinh lời, chứng khoán, cổ tức"),
        "🏥 3. Tiết Kiệm Dài Hạn (LTSS - 10%)": (0.10, "Mua nhà, mua xe, dự phòng khẩn cấp"),
        "🎓 4. Học Tập Phát Triển (EDU - 10%)": (0.10, "Sách, khóa học, nâng cao tay nghề"),
        "🍷 5. Hưởng Thụ (PLAY - 10%)": (0.10, "Thư giãn, du lịch, giải trí"),
        "❤️ 6. Cho Đi (GIVE - 5%)": (0.05, "Mừng cưới, từ thiện, giúp gia đình")
    }
    j_cols = st.columns(3)
    for idx, (j_title, (j_rate, j_desc)) in enumerate(jars.items()):
        with j_cols[idx % 3]:
            st.write(f"**{j_title}**")
            st.markdown(f"<h3 style='color:#8B5CF6; margin:0;'>{income * j_rate:,.0f} VNĐ</h3>", unsafe_allow_html=True)
            st.caption(j_desc)
            st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CHỨC NĂNG 2: HŨ TIẾT KIỆM MỤC TIÊU (GOAL SAVINGS)
# =========================================================
elif selected_menu == "🏺 Hũ Tiết Kiệm Mục Tiêu (Goal Savings)":
    st.subheader("🏺 Quản Lý Hũ Tiết Kiệm Cho Từng Mục Tiêu Cụ Thể")

    col_g1, col_g2 = st.columns([1, 1.3])

    with col_g1:
        st.markdown("<div class='card-vibrant-emerald'>", unsafe_allow_html=True)
        st.markdown("### ➕ Tạo Hũ Tiết Kiệm Mới")
        g_name = st.text_input("Tên mục tiêu:", placeholder="Ví dụ: Mua laptop mới, Đi du lịch...")
        g_target = st.number_input("Số tiền mục tiêu (VNĐ):", min_value=1000000, value=20000000, step=1000000, format="%d")
        g_current = st.number_input("Số tiền đã có ban đầu (VNĐ):", min_value=0, value=2000000, step=500000, format="%d")
        g_date = st.date_input("Hạn hoàn thành:", datetime.now())

        if st.button("🚀 Khởi Tạo Hũ Tiết Kiệm", type="primary", use_container_width=True):
            if g_name:
                add_goal(g_name, g_target, g_current, g_date.strftime("%Y-%m-%d"))
                st.toast(f"Đã tạo hũ '{g_name}' thành công! 🏺", icon="🎉")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_g2:
        st.markdown("### 📜 Danh Sách Hũ Tiết Kiệm Hiện Có")
        df_goals = load_goals()

        if df_goals.empty:
            st.info("Chưa có hũ tiết kiệm nào được tạo.")
        else:
            for idx, row in df_goals.iterrows():
                st.markdown("<div class='card-vibrant-amber'>", unsafe_allow_html=True)
                g_id = row['id']
                pct = min(1.0, row['current'] / row['target']) if row['target'] > 0 else 1.0
                
                c_head1, c_head2 = st.columns([2, 1])
                with c_head1:
                    st.markdown(f"#### {row['name']}")
                    st.caption(f"🎯 Mục tiêu: **{row['target']:,.0f} VNĐ** | Hạn: **{row['target_date']}**")
                with c_head2:
                    st.markdown(f"<h3 style='color:#10B981; text-align:right;'>{row['current']:,.0f}đ</h3>", unsafe_allow_html=True)

                st.progress(pct)
                st.write(f"Đã hoàn thành **{pct*100:.1f}%**")

                c_dep1, c_dep2 = st.columns([2, 1])
                with c_dep1:
                    dep_amount = st.number_input(f"Thêm tiền vào hũ (VNĐ):", min_value=50000, value=500000, step=100000, key=f"dep_val_{g_id}", format="%d")
                with c_dep2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("💵 Tích Lũy", key=f"btn_dep_{g_id}"):
                        update_goal_savings(g_id, dep_amount)
                        st.toast(f"Đã nạp +{dep_amount:,.0f}đ vào hũ {row['name']}!", icon="✅")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CHỨC NĂNG 3: MÔ PHỎNG XÓA NỢ (SNOWBALL VS AVALANCHE)
# =========================================================
elif selected_menu == "💳 Mô Phỏng Xóa NỢ (Snowball vs Avalanche)":
    st.subheader("💳 Công Cụ Lập Kế Hoạch Xóa Nợ Thông Minh")

    col_d1, col_d2 = st.columns([1, 1.4])

    with col_d1:
        st.markdown("<div class='card-vibrant-rose'>", unsafe_allow_html=True)
        st.markdown("### ➕ Nhập Khoản Nợ Mới")
        d_name = st.text_input("Tên khoản nợ / Ngân hàng:", placeholder="Ví dụ: Thẻ tín dụng, Trả góp xe...")
        d_amount = st.number_input("Dư nợ gốc còn lại (VNĐ):", min_value=500000, value=15000000, step=1000000, format="%d")
        d_rate = st.number_input("Lãi suất năm (%):", min_value=0.0, value=18.0, step=0.5)
        d_min_pay = st.number_input("Tiền trả tối thiểu/tháng (VNĐ):", min_value=100000, value=1000000, step=100000, format="%d")

        if st.button("📌 Thêm Khoản Nợ", type="primary", use_container_width=True):
            if d_name:
                add_debt(d_name, d_amount, d_rate, d_min_pay)
                st.toast("Đã ghi nhận khoản nợ thành công!", icon="💳")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_d2:
        st.markdown("### 📜 Danh Sách Khoản Nợ Cần Thanh Toán")
        df_debts = load_debts()

        if df_debts.empty:
            st.success("🎉 Bạn hiện tại không có khoản nợ nào! Hãy tiếp tục duy trì trạng thái tự do này nhé!")
        else:
            st.dataframe(df_debts[["id", "name", "amount", "interest_rate", "min_pay"]], use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("### ⚔️ So Sánh Chiến Lược Trả Nợ Tối Ưu")

            col_snow, col_aval = st.columns(2)
            with col_snow:
                st.markdown("<div class='card-vibrant-amber'>", unsafe_allow_html=True)
                st.markdown("#### 🏔️ Tuyết Lăn (Snowball)")
                st.caption("Ưu tiên trả khoản nợ **NHỎ NHẤT** trước để giải phóng tinh thần.")
                df_snow = df_debts.sort_values(by="amount", ascending=True)
                for i, r in df_snow.iterrows():
                    st.write(f"1️⃣ **{r['name']}**: {r['amount']:,.0f}đ (Lãi {r['interest_rate']}%)")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_aval:
                st.markdown("<div class='card-vibrant-purple'>", unsafe_allow_html=True)
                st.markdown("#### 🌋 Cơn Lốc (Avalanche)")
                st.caption("Ưu tiên trả khoản nợ **LÃI SUẤT CAO NHẤT** trước để tiết kiệm tiền lãi.")
                df_aval = df_debts.sort_values(by="interest_rate", ascending=False)
                for i, r in df_aval.iterrows():
                    st.write(f"🔥 **{r['name']}**: Lãi {r['interest_rate']}% (Gốc: {r['amount']:,.0f}đ)")
                st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CHỨC NĂNG 4: AI DOGE & CHATBOT "HỎI SẾP DOGE"
# =========================================================
elif selected_menu == "🤖 AI Doge & Chatbot 'Hỏi Sếp Doge'":
    st.subheader("🤖 Trợ Lý Tương Tác Trực Tiếp - 'Hỏi Sếp Doge'")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "doge", "msg": f"Gâu gâu! Chào bạn ({age} tuổi). Doge đã xem hồ sơ thu nhập {income:,.0f} VNĐ của bạn rồi! Bạn muốn hỏi Doge gì về chi tiêu, mua sắm hay đầu tư nào?"}
        ]

    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"<div class='chat-bubble-user'>👤 {chat['msg']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-doge'>🐶 <b>Sếp Doge:</b> {chat['msg']}</div>", unsafe_allow_html=True)

    st.markdown("<br style='clear:both;'>", unsafe_allow_html=True)
    st.markdown("---")

    user_query = st.text_input("💬 Nhập câu hỏi tư vấn tài chính cho Sếp Doge:", placeholder="Ví dụ: Có nên mua iPhone 30 triệu trả góp không?, Làm sao để tích lũy mua nhà?...")

    if st.button("📩 Gửi Câu Hỏi Cho Doge", type="primary"):
        if user_query:
            st.session_state.chat_history.append({"role": "user", "msg": user_query})
            
            # Logic AI Doge Phản Hồi Tự Động Dí Dỏm & Thông Minh
            q_lower = user_query.lower()
            if "iphone" in q_lower or "mua đồ" in q_lower or "trả góp" in q_lower:
                max_phone = income * 0.8
                if income < 15000000:
                    reply = f"Gâu gâu! Lương {income:,.0f}đ mà đòi mua tiêu sản đắt tiền? Doge khuyên bạn NÊN DỪNG LẠI! Trả góp sẽ bòn rút {income*0.15:,.0f}đ mỗi tháng của bạn đấy!"
                else:
                    reply = f"Gâu! Thu nhập {income:,.0f}đ của bạn khá ổn, nhưng chỉ nên mua nếu khoản trả góp/giá trị món đồ < {max_phone:,.0f}đ và bạn đã có Quỹ dự phòng ít nhất 3 tháng!"
            elif "đầu tư" in q_lower or "chứng khoán" in q_lower or "crypto" in q_lower:
                reply = f"Gâu gâu! Ở độ tuổi {age} với khẩu vị '{risk_appetite}', Doge khuyên bạn trích {income*0.2:,.0f}đ/tháng chia làm 2 phần: 70% Quỹ mở/VN30 an toàn, 30% thử sức mạo hiểm!"
            elif "nhà" in q_lower or "bất động sản" in q_lower:
                reply = f"Gâu! Mua nhà cần chuẩn bị tối thiểu 30% tiền mặt vốn có. Với thu nhập hiện tại, hãy tích lũy Hũ Tiết Kiệm Dài Hạn ít nhất 3-5 năm trước khi nghĩ tới chuyện trả góp ngân hàng nhé!"
            else:
                reply = f"Gâu gâu! Lời khuyên vàng của Doge cho bạn: Hãy luôn trích ngay **20% thu nhập ({income*0.2:,.0f}đ)** vào Hũ Tích Lũy ngay khi nhận lương, rồi mới tính chuyện tiêu phần còn lại!"

            st.session_state.chat_history.append({"role": "doge", "msg": reply})
            st.rerun()

# =========================================================
# CHỨC NĂNG 5: DỰ PHÒNG & TỰ DO TÀI CHÍNH (FIRE)
# =========================================================
elif selected_menu == "📈 Dự Phòng & Tự Do Tài Chính (FIRE)":
    st.subheader("📈 Dự Phóng Quỹ Khẩn Cấp & Lộ Trình Nghỉ Hưu Tự Do (FIRE)")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("<div class='card-vibrant-amber'>", unsafe_allow_html=True)
        st.markdown("### 🛡️ Quỹ Dự Phòng Khẩn Cấp")
        monthly_essential = income * 0.50
        req_months = 6 if (housing_status == "Đang ở trọ / Đi thuê" or dependents > 0) else 3
        req_emergency = monthly_essential * req_months

        st.write(f"• Chi phí thiết yếu ước tính / tháng: **{monthly_essential:,.0f} VNĐ**")
        st.write(f"• Mức dự phòng khuyên dùng: **{req_months} tháng** sinh hoạt.")
        st.markdown(f"#### 💰 Mục tiêu quỹ: <span style='color:#D97706;'>{req_emergency:,.0f} VNĐ</span>", unsafe_allow_html=True)

        prog_em = min(1.0, current_savings / req_emergency) if req_emergency > 0 else 1.0
        st.progress(prog_em)
        st.write(f"Đã đạt **{prog_em*100:.1f}%** (Hiện có: {current_savings:,.0f}đ)")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_f2:
        st.markdown("<div class='card-vibrant-purple'>", unsafe_allow_html=True)
        st.markdown("### 🎯 Con Số Tự Do Tài Chính (FIRE)")
        annual_exp = (income * 0.75) * 12
        fire_num = annual_exp * 25

        st.write(f"• Chi tiêu năm ước tính: **{annual_exp:,.0f} VNĐ**")
        st.markdown(f"#### 🏆 Con số FIRE cần tích lũy: <span style='color:#8B5CF6;'>{fire_num:,.0f} VNĐ</span>", unsafe_allow_html=True)

        m_save = income * 0.20
        if m_save > 0:
            r = 0.08 / 12
            months = 0
            acc = current_savings
            while acc < fire_num and months < 600:
                acc = acc * (1 + r) + m_save
                months += 1
            years = months / 12
            st.success(f"🚀 Tích lũy {m_save:,.0f}đ/tháng với lãi suất 8%/năm, bạn sẽ đạt FIRE sau **{years:.1f} năm** (ở tuổi **{age + int(years)}**).")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CHỨC NĂNG 6: SỔ THU CHI & SQLITE BÁO CÁO
# =========================================================
else:
    st.subheader("📝 Sổ Ghi Chép Thu Chi Real-Time (Đồng Bộ SQLite)")

    col_e1, col_e2 = st.columns([1, 1.4])

    with col_e1:
        st.markdown("<div class='card-vibrant-amber'>", unsafe_allow_html=True)
        st.markdown("### ➕ Nhập Chi Tiêu Mới")
        e_date = st.date_input("Ngày giao dịch:", datetime.now())
        e_cat = st.selectbox("Danh mục:", ["Thiết yếu (Needs)", "Sở thích (Wants)", "Tích lũy & Đầu tư (Savings)"])
        e_desc = st.text_input("Ghi chú / Mô tả:", placeholder="Ví dụ: Tiền điện nước, Mua quần áo...")
        e_amt = st.number_input("Số tiền (VNĐ):", min_value=1000, value=100000, step=50000, format="%d")

        if st.button("💾 Lưu Vào CSDL SQLite", type="primary", use_container_width=True):
            add_expense(e_date.strftime("%d/%m/%Y"), e_cat, e_desc if e_desc else "Chi tiêu", e_amt)
            st.toast("Đã lưu chi tiêu vào CSDL SQLite vĩnh viễn! 🐶", icon="✅")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_e2:
        st.markdown("### 📜 Lịch Sử Chi Tiêu & Xuất Báo Cáo")
        df_expenses_list = load_expenses()
        st.dataframe(df_expenses_list[["id", "date", "category", "description", "amount"]], use_container_width=True, hide_index=True)

        if not df_expenses_list.empty:
            tot_exp = df_expenses_list["amount"].sum()
            st.metric("💸 Tổng chi tiêu thực tế đã ghi nhận", f"{tot_exp:,.0f} VNĐ")

            # Xuất dữ liệu ra file CSV
            csv_exp = df_expenses_list.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải Báo Cáo Tài Chính CSV (Excel)",
                data=csv_exp,
                file_name=f"DOGEMNET_Financial_Report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                type="primary"
            )
'''

ast.parse(app_code)
print("DOGEMNET Super App code AST verified successfully!")
