import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & THEME DOGEMNET 🐶
# ---------------------------------------------------------
st.set_page_config(
    page_title="DOGEMNET - Quản Lý Tài Chính Cá Nhân AI 🐶",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện DOGEMNET mang phong cách Chó Cố Vấn Tài Chính
st.markdown("""
    <style>
    :root {
        --doge-amber: #F59E0B;
        --doge-gold: #D97706;
        --doge-dark: #1E293B;
        --doge-card-bg: #FFFFFF;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }

    /* BANNER DOGEMNET */
    .doge-banner {
        background: linear-gradient(135deg, #1E293B 0%, #334155 50%, #D97706 100%);
        border-radius: 20px;
        padding: 30px 25px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 25px;
        border: 2px solid #F59E0B;
    }
    
    .doge-banner h1 {
        color: #FBBF24 !important;
        font-family: 'Georgia', serif;
        font-size: 2.3rem;
        font-weight: 900;
        margin-bottom: 8px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    
    .doge-banner p {
        color: #E2E8F0;
        font-size: 1.1rem;
        margin: 0;
        font-style: italic;
    }

    /* CARD KHUNG TƯ VẤN AI */
    .doge-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 6px solid #F59E0B;
        margin-bottom: 20px;
    }

    .doge-ai-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FFFBEB 100%);
        border: 1.5px solid #F59E0B;
        border-radius: 14px;
        padding: 18px;
        margin: 15px 0;
    }

    /* JAR CARD */
    .jar-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. KHỞI TẠO SESSION STATE
# ---------------------------------------------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = [
        {"Ngày": "17/10/2026", "Danh mục": "Thiết yếu (Needs)", "Mô tả": "Tiền thuê nhà", "Số tiền": 4500000},
        {"Ngày": "17/10/2026", "Danh mục": "Thiết yếu (Needs)", "Mô tả": "Tiền siêu thị & Ăn uống", "Số tiền": 3200000},
        {"Ngày": "16/10/2026", "Danh mục": "Sở thích (Wants)", "Mô tả": "Cà phê & Đi xem phim", "Số tiền": 450000},
        {"Ngày": "15/10/2026", "Danh mục": "Tích lũy & Đầu tư (Savings)", "Mô tả": "Gửi tiết kiệm tích lũy", "Số tiền": 3000000}
    ]

# ---------------------------------------------------------
# 3. SIDEBAR: THÔNG TIN HỒ SƠ NGƯỜI DÙNG & MENU
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #D97706;'>🐶 DOGEMNET</h1>", unsafe_allow_html=True)
    st.caption("🤖 Trợ Lý Tài Chính Cá Nhân AI Thông Minh")
    st.markdown("---")
    
    st.subheader("👤 Hồ Sơ Tài Chính Của Bạn")
    income = st.number_input("💵 Thu nhập hàng tháng (VNĐ):", min_value=1000000, value=20000000, step=1000000, format="%d")
    age = st.slider("🎂 Độ tuổi:", min_value=18, max_value=70, value=26)
    gender = st.selectbox("🚻 Giới tính:", ["Nam", "Nữ", "Khác"])
    marital_status = st.selectbox("💍 Tình trạng hôn nhân:", ["Độc thân", "Đã kết hôn (Chưa có con)", "Đã kết hôn (Có con nhỏ)", "Đã kết hôn (Con đã lớn)"])
    housing_status = st.selectbox("🏠 Tình trạng nhà ở:", ["Đang ở trọ / Đi thuê", "Ở cùng bố mẹ", "Đang trả góp mua nhà", "Sở hữu nhà riêng"])
    dependents = st.number_input("👨‍👩‍👧‍👦 Số người phụ thuộc (con cái/cha mẹ):", min_value=0, max_value=10, value=0 if "Độc thân" in marital_status else 1)
    monthly_debt = st.number_input("💳 Khoản nợ/trả góp hàng tháng (VNĐ):", min_value=0, value=0, step=500000, format="%d")
    current_savings = st.number_input("🏦 Số tiền tiết kiệm/dự phòng hiện có (VNĐ):", min_value=0, value=30000000, step=5000000, format="%d")
    risk_appetite = st.select_slider("🎯 Khẩu vị rủi ro đầu tư:", options=["Rất an toàn", "An toàn", "Cân bằng", "Tăng trưởng", "Rất mạo hiểm"], value="Cân bằng")
    
    st.markdown("---")
    selected_menu = st.radio(
        "📌 Menu Chức Năng:",
        [
            "📊 Phân Bổ Ngân Sách (50/30/20 & 6 Hũ)",
            "🤖 AI Doge Tư Vấn Chi Tiêu & Đầu Tư",
            "📈 Dự Phòng & Tự Do Tài Chính (FIRE)",
            "📝 Sổ Thu Chi & Theo Dõi Real-Time"
        ]
    )

# ---------------------------------------------------------
# 4. BANNER TIÊU ĐỀ DOGEMNET
# ---------------------------------------------------------
st.markdown("""
    <div class="doge-banner">
        <h1>🐶 DOGEMNET PERSONAL FINANCE AI 🚀</h1>
        <p>"Làm Chủ Đồng Tiền - Tự Do Tài Chính - Quản Lý Thông Minh Theo Nguyên Tắc Chuẩn"</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. XỬ LÝ THEO CHỨC NĂNG CỦA MENU
# ---------------------------------------------------------

# =========================================================
# CHỨC NĂNG 1: PHÂN BỔ NGÂN SÁCH (50/30/20 & 6 HŨ)
# =========================================================
if selected_menu == "📊 Phân Bổ Ngân Sách (50/30/20 & 6 Hũ)":
    st.subheader("📊 Tự Động Phân Bổ Dòng Tiền Theo Nguyên Tắc Tài Chính")
    
    # Tính toán điều chỉnh tỉ lệ theo hoàn cảnh sống
    needs_pct, wants_pct, savings_pct = 50, 30, 20
    adjustment_reasons = []

    if housing_status in ["Đang ở trọ / Đi thuê", "Đang trả góp mua nhà"]:
        needs_pct += 5
        wants_pct -= 5
        adjustment_reasons.append("Tăng 5% Nhu cầu thiết yếu do chi phí ở/trả góp nhà.")
    
    if dependents > 0:
        add_needs = min(10, dependents * 5)
        needs_pct += add_needs
        wants_pct -= add_needs
        adjustment_reasons.append(f"Tăng {add_needs}% Nhu cầu thiết yếu do nuôi người phụ thuộc.")

    if monthly_debt > 0:
        debt_pct = (monthly_debt / income) * 100
        if debt_pct > 35:
            st.error(f"⚠️ Cảnh báo: Tỷ lệ trả nợ hiện tại chiếm {debt_pct:.1f}% thu nhập (Vượt ngưỡng an toàn 35%). Bạn nên ưu tiên trả nợ gốc!")

    total_pct = needs_pct + wants_pct + savings_pct
    needs_pct = round((needs_pct / total_pct) * 100)
    wants_pct = round((wants_pct / total_pct) * 100)
    savings_pct = 100 - needs_pct - wants_pct

    needs_val = income * (needs_pct / 100)
    wants_val = income * (wants_pct / 100)
    savings_val = income * (savings_pct / 100)

    st.markdown("### 1️⃣ Quy Tắc Phân Bổ 50/30/20 (Đã Tối Ưu Cho Bạn)")
    if adjustment_reasons:
        st.info("💡 **Hệ thống đã tự động điều chỉnh tỷ lệ ngân sách dựa trên hoàn cảnh cá nhân:** " + " | ".join(adjustment_reasons))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"🏠 Nhu cầu thiết yếu ({needs_pct}%)", f"{needs_val:,.0f} VNĐ", help="Thuê nhà, ăn uống, điện nước, đi lại, y tế gốc...")
    with col2:
        st.metric(f"🎉 Sở thích & Linh hoạt ({wants_pct}%)", f"{wants_val:,.0f} VNĐ", help="Mua sắm, đồ công nghệ, du lịch, giải trí...")
    with col3:
        st.metric(f"🚀 Tích lũy & Đầu tư ({savings_pct}%)", f"{savings_val:,.0f} VNĐ", help="Dự phòng khẩn cấp, trả nợ, đầu tư chứng khoán, bất động sản...")

    df_503020 = pd.DataFrame({
        "Hạng mục": ["Thiết yếu (Needs)", "Sở thích (Wants)", "Tích lũy & Đầu tư (Savings)"],
        "Số tiền (VNĐ)": [needs_val, wants_val, savings_val]
    })
    st.bar_chart(df_503020, x="Hạng mục", y="Số tiền (VNĐ)", color="#D97706")

    st.markdown("---")
    st.markdown("### 2️⃣ Quy Tắc 6 Hũ Tài Chính (Six Jars Method - T. Harv Eker)")
    st.caption("Chia nhỏ ngân sách thành 6 hũ để kiểm soát mục đích sử dụng tiền hiệu quả nhất:")

    jars = {
        "📦 Hũ 1: Nhu Cầu Thiết Yếu (NEC - 55%)": (0.55, "Thức ăn, hóa đơn, nhà ở, y tế"),
        "📈 Hũ 2: Tự Do Tài Chính (FFA - 10%)": (0.10, "Đầu tư sinh lời, chứng khoán, cổ tức"),
        "🏥 Hũ 3: Tiết Kiệm Dài Hạn (LTSS - 10%)": (0.10, "Mua nhà, mua xe, quỹ dự phòng khẩn cấp"),
        "🎓 Hũ 4: Giáo Dục & Bản Thân (EDU - 10%)": (0.10, "Sách, khóa học, nâng cao kỹ năng nghề nghiệp"),
        "🍷 Hũ 5: Hưởng Thụ (PLAY - 10%)": (0.10, "Thư giãn, du lịch, mua sắm cá nhân"),
        "❤️ Hũ 6: Cho Đi (GIVE - 5%)": (0.05, "Mừng cưới, từ thiện, giúp đỡ gia đình")
    }

    j_cols = st.columns(3)
    for idx, (j_name, (j_rate, j_desc)) in enumerate(jars.items()):
        j_amount = income * j_rate
        with j_cols[idx % 3]:
            st.markdown(f"""
                <div class="jar-card">
                    <h4 style="color:#D97706; margin-bottom:5px;">{j_name}</h4>
                    <h3 style="color:#1E293B; margin:5px 0;">{j_amount:,.0f} VNĐ</h3>
                    <p style="color:#64748B; font-size:0.85rem; margin:0;">{j_desc}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# CHỨC NĂNG 2: AI DOGE TƯ VẤN CHI TIÊU & ĐẦU TƯ
# =========================================================
elif selected_menu == "🤖 AI Doge Tư Vấn Chi Tiêu & Đầu Tư":
    st.subheader("🤖 Chú Chó Cố Vấn AI DOGE - Phân Tích & Đưa Ra Lời Khuyên")
    
    st.markdown(f"""
        <div class="doge-ai-box">
            <h3 style="color:#D97706; margin-top:0;">🐶 Giao Diện Tư Vấn Thông Minh Dựa Trên Đặc Điểm Cá Nhân</h3>
            <p style="color:#334155;">Dựa trên độ tuổi (<b>{age} tuổi</b>), tình trạng hôn nhân (<b>{marital_status}</b>), chỗ ở (<b>{housing_status}</b>), và mức thu nhập (<b>{income:,.0f} VNĐ</b>), AI Doge đã phân tích cho bạn cụ thể như sau:</p>
        </div>
    """, unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown("<div class='doge-card'>", unsafe_allow_html=True)
        st.markdown("### 💡 1. Chiến Lược Chi Tiêu & Tích Lũy")
        
        # Lời khuyên theo độ tuổi
        if age < 25:
            st.write("• **Độ tuổi phát triển sự nghiệp:** Ưu tiên trích ít nhất 10-15% thu nhập cho Hũ Giáo Dục (EDU) để học kỹ năng mới, ngoại ngữ, công nghệ. Đây là khoản đầu tư có ROI cao nhất.")
        elif 25 <= age <= 35:
            st.write("• **Độ tuổi tích lũy tài sản:** Cần xây dựng ngay Quỹ dự phòng 3-6 tháng và lập mục tiêu cho các cột mốc lớn (lập gia đình, mua nhà, sinh con).")
        else:
            st.write("• **Độ tuổi củng cố & bảo toàn:** Cần tập trung gia tăng tài sản an toàn, thu nhập thụ động và chuẩn bị quỹ hưu trí.")

        # Lời khuyên theo chỗ ở
        if housing_status == "Đang ở trọ / Đi thuê":
            st.write("• **Về nhà ở:** Chi phí thuê nhà không nên vượt quá **20-25%** tổng thu nhập. Hãy cân nhắc gom tiền thưởng/tiết kiệm gửi kỳ hạn cố định để chuẩn bị vốn mua nhà.")
        elif housing_status == "Đang trả góp mua nhà":
            st.write("• **Về khoản trả góp:** Luôn đảm bảo tổng tiền trả gốc + lãi hàng tháng không quá **30-35%** thu nhập để tránh áp lực rủi ro thanh khoản.")
        
        # Lời khuyên theo phụ thuộc
        if dependents > 0:
            st.write(f"• **Gia đình có người phụ thuộc ({dependents} người):** Bắt buộc phải có **Bảo hiểm nhân thọ/Y tế** cho người trụ cột tài chính để bảo vệ gia đình trước rủi ro.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_a2:
        st.markdown("<div class='doge-card'>", unsafe_allow_html=True)
        st.markdown("### 🚀 2. Gợi Ý Phân Bổ Đầu Tư Dữ Liệu (Asset Allocation)")
        
        # Nguyên tắc 100 - Số tuổi
        equity_pct = max(10, 100 - age)
        bond_pct = 100 - equity_pct
        
        st.write(f"• **Nguyên tắc phân bổ tài sản mạo hiểm theo độ tuổi (100 - Số tuổi):**")
        st.write(f"   - **Tài sản tăng trưởng (Chứng khoán, Quỹ mở, Crypto):** ~**{equity_pct}%**")
        st.write(f"   - **Tài sản an toàn (Tiền gửi tiết kiệm, Trái phiếu, Vàng):** ~**{bond_pct}%**")

        st.markdown(f"#### 🎯 Danh Mục Đầu Tư Gợi Ý Theo Khẩu Vị: **{risk_appetite}**")
        if risk_appetite in ["An toàn", "Rất an toàn"]:
            st.success("🔒 **Danh mục khuyến nghị:** 60% Tiết kiệm ngân hàng, 30% Trái phiếu doanh nghiệp/Quỹ trái phiếu, 10% Chứng khoán VN30.")
        elif risk_appetite == "Cân bằng":
            st.info("⚖️ **Danh mục khuyến nghị:** 40% Quỹ cổ phiếu/Chứng khoán, 30% Tiết kiệm/Trái phiếu, 20% Bất động sản/Tích lũy dài hạn, 10% Crypto/Vàng.")
        else:
            st.warning("🔥 **Danh mục khuyến nghị:** 60% Cổ phiếu tăng trưởng / Quỹ ETF, 20% Crypto / Công nghệ, 20% Tiết kiệm dự phòng.")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CHỨC NĂNG 3: DỰ PHÒNG & TỰ DO TÀI CHÍNH (FIRE)
# =========================================================
elif selected_menu == "📈 Dự Phòng & Tự Do Tài Chính (FIRE)":
    st.subheader("📈 Tính Toán Quỹ Dự Phòng & Con Đường Tự Do Tài Chính (FIRE)")

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("<div class='doge-card'>", unsafe_allow_html=True)
        st.markdown("### 🛡️ Quỹ Dự Phòng Khẩn Cấp (Emergency Fund)")
        
        monthly_essential = income * 0.50
        recommended_months = 6 if (housing_status == "Đang ở trọ / Đi thuê" or dependents > 0) else 3
        required_emergency = monthly_essential * recommended_months

        st.write(f"• Chi phí thiết yếu ước tính / tháng: **{monthly_essential:,.0f} VNĐ**")
        st.write(f"• Khuyên dùng cho hoàn cảnh của bạn: **{recommended_months} tháng** sinh hoạt.")
        st.markdown(f"#### 💰 Số tiền dự phòng mục tiêu: <span style='color:#D97706;'>{required_emergency:,.0f} VNĐ</span>", unsafe_allow_html=True)

        progress = min(1.0, current_savings / required_emergency) if required_emergency > 0 else 1.0
        st.progress(progress)
        st.write(f"Bạn đã hoàn thành **{progress*100:.1f}%** mục tiêu dự phòng (Hiện có: {current_savings:,.0f} VNĐ).")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_f2:
        st.markdown("<div class='doge-card'>", unsafe_allow_html=True)
        st.markdown("### 🎯 Công Cụ Tính FIRE (Tự Do Tài Chính)")
        st.caption("Theo Quy tắc 4% (Trinity Study), số tiền bạn cần tích lũy để nghỉ hưu tự do = **Chi tiêu hàng năm x 25**.")

        annual_expense = (income * 0.8) * 12 # Giả định chi tiêu 80% thu nhập
        fire_number = annual_expense * 25
        
        st.write(f"• Chi tiêu ước tính năm: **{annual_expense:,.0f} VNĐ**")
        st.markdown(f"#### 🏆 Con số FIRE của bạn: <span style='color:#D97706;'>{fire_number:,.0f} VNĐ</span>", unsafe_allow_html=True)

        monthly_saving = income * 0.20 # Giả định tiết kiệm 20%
        expected_return_rate = 0.08 # Lãi suất kép 8%/năm

        if monthly_saving > 0:
            r_monthly = expected_return_rate / 12
            months_to_fire = 0
            accumulated = current_savings
            while accumulated < fire_number and months_to_fire < 600:
                accumulated = accumulated * (1 + r_monthly) + monthly_saving
                months_to_fire += 1
            
            years_to_fire = months_to_fire / 12
            st.success(f"🚀 Với mức tiết kiệm {monthly_saving:,.0f} VNĐ/tháng và lãi suất đầu tư 8%/năm, bạn sẽ đạt Tự Do Tài Chính sau khoảng **{years_to_fire:.1f} năm** (ở tuổi **{age + int(years_to_fire)}**).")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CHỨC NĂNG 4: SỔ THU CHI & THEO DÕI REAL-TIME
# =========================================================
else:
    st.subheader("📝 Sổ Ghi Chép Thu Chi Real-Time DOGEMNET")

    col_e1, col_e2 = st.columns([1, 1.5])

    with col_e1:
        st.markdown("### ➕ Nhập Giao Dịch Mới")
        exp_date = st.date_input("Ngày giao dịch:", datetime.now())
        exp_cat = st.selectbox("Danh mục:", ["Thiết yếu (Needs)", "Sở thích (Wants)", "Tích lũy & Đầu tư (Savings)"])
        exp_desc = st.text_input("Ghi chú / Mô tả chi tiêu:", placeholder="Ví dụ: Tiền siêu thị, Mua áo...")
        exp_amount = st.number_input("Số tiền (VNĐ):", min_value=1000, value=100000, step=50000, format="%d")

        if st.button("💾 Lưu Giao Dịch", type="primary", use_container_width=True):
            new_exp = {
                "Ngày": exp_date.strftime("%d/%m/%Y"),
                "Danh mục": exp_cat,
                "Mô tả": exp_desc if exp_desc else "Chi tiêu",
                "Số tiền": exp_amount
            }
            st.session_state.expenses.append(new_exp)
            st.toast("Đã ghi nhận chi tiêu thành công! 🐶", icon="✅")

    with col_e2:
        st.markdown("### 📜 Lịch Sử Chi Tiêu")
        df_exp = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df_exp, use_container_width=True, hide_index=True)

        if not df_exp.empty:
            total_spent = df_exp["Số tiền"].sum()
            st.metric("💸 Tổng chi tiêu đã ghi nhận", f"{total_spent:,.0f} VNĐ")

            st.markdown("#### 📊 Tỷ Lệ Chi Tiêu Thực Tế:")
            df_cat = df_exp.groupby("Danh mục")["Số tiền"].sum().reset_index()
            st.bar_chart(df_cat, x="Danh mục", y="Số tiền", color="#F59E0B")
