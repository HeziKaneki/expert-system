"""
Streamlit Web Interface cho Hệ Chuyên Gia Chuẩn Đoán Bệnh
Cải thiện: Professional UI/UX, Medical Color Scheme, Better Layout
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

from knowledge_base import KnowledgeBase
from fuzzy_system import FuzzyLogic
from inference_engine import InferenceEngine, PatientFact

# ============================================================================
# PAGE CONFIGURATION & STYLING
# ============================================================================

st.set_page_config(
    page_title="🏥 Hệ Chuyên Gia Chuẩn Đoán Bệnh",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Medical Expert System v2.0 - Fuzzy Logic Based Diagnosis"}
)

# ============================================================================
# CUSTOM CSS - PROFESSIONAL MEDICAL THEME
# ============================================================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #0066cc;      /* Medical Blue */
        --secondary-color: #00cc66;    /* Medical Green */
        --danger-color: #ff4444;       /* Alert Red */
        --warning-color: #ffaa00;      /* Warning Orange */
        --info-color: #00aaff;         /* Info Cyan */
        --success-color: #44cc44;      /* Success Green */
        --light-gray: #f5f7fa;
        --dark-gray: #2d3436;
        --border-radius: 12px;
        --shadow: 0 4px 15px rgba(0, 102, 204, 0.1);
    }
    
    /* Main container */
    .main {
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #0066cc 0%, #00aaff 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0, 102, 204, 0.2);
    }
    
    .header-title {
        font-size: 2.5em;
        font-weight: 700;
        margin: 0;
        color: white;
    }
    
    .header-subtitle {
        font-size: 1.1em;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Cards */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
        border-left: 4px solid #0066cc;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 8px 25px rgba(0, 102, 204, 0.15);
        transform: translateY(-2px);
    }
    
    .card-success {
        border-left-color: #44cc44;
    }
    
    .card-warning {
        border-left-color: #ffaa00;
    }
    
    .card-danger {
        border-left-color: #ff4444;
    }
    
    /* Metric boxes */
    .metric-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(0, 102, 204, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        border-color: rgba(0, 102, 204, 0.3);
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.1);
    }
    
    .metric-value {
        font-size: 2.2em;
        font-weight: 700;
        color: #0066cc;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #666;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 0.3rem;
    }
    
    .badge-mild {
        background-color: #e3f2fd;
        color: #0066cc;
    }
    
    .badge-moderate {
        background-color: #fff3e0;
        color: #ff8f00;
    }
    
    .badge-severe {
        background-color: #ffebee;
        color: #d32f2f;
    }
    
    .badge-critical {
        background-color: #ff1744;
        color: white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.2);
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 25px rgba(0, 102, 204, 0.35);
        transform: translateY(-2px);
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0066cc 0%, #0052a3 100%);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #f5f7fa;
        border-radius: 8px;
        border-left: 3px solid #0066cc;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #e8ecf1;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8em;
        font-weight: 700;
        color: #0066cc;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0066cc;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #0066cc, transparent);
        margin: 2rem 0;
    }
    
    /* Text highlights */
    .highlight-success {
        color: #44cc44;
        font-weight: 600;
    }
    
    .highlight-warning {
        color: #ffaa00;
        font-weight: 600;
    }
    
    .highlight-danger {
        color: #ff4444;
        font-weight: 600;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }
    
    /* Tables */
    .dataframe {
        border-radius: 8px !important;
        border: 1px solid #e0e0e0;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #e8f5e9;
        border: 1px solid #4caf50;
        border-radius: 8px;
    }
    
    .stError {
        background-color: #ffebee;
        border: 1px solid #f44336;
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        border-radius: 8px;
    }
    
    /* Results display */
    .result-item {
        background: white;
        border-left: 5px solid #0066cc;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .result-rank {
        display: inline-block;
        background: linear-gradient(135deg, #0066cc, #0052a3);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: 700;
        font-size: 1.1em;
        margin-right: 1rem;
    }
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if 'kb' not in st.session_state:
    st.session_state.kb = KnowledgeBase()
    st.session_state.fuzzy_logic = FuzzyLogic()
    st.session_state.engine = InferenceEngine(st.session_state.kb, st.session_state.fuzzy_logic)

if 'diagnosis_results' not in st.session_state:
    st.session_state.diagnosis_results = None

if 'last_diagnosis_time' not in st.session_state:
    st.session_state.last_diagnosis_time = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_severity_badge(severity):
    """Return badge HTML for severity level"""
    severity_map = {
        "MILD": '<span class="badge badge-mild">🟢 MILD</span>',
        "MODERATE": '<span class="badge badge-moderate">🟠 MODERATE</span>',
        "SEVERE": '<span class="badge badge-severe">🔴 SEVERE</span>',
        "CRITICAL": '<span class="badge badge-critical">🚨 CRITICAL</span>',
    }
    return severity_map.get(severity, '<span class="badge">Unknown</span>')

def get_confidence_color(confidence):
    """Return color based on confidence level"""
    if confidence >= 0.8:
        return '#d32f2f'  # Red - High
    elif confidence >= 0.6:
        return '#ff8f00'  # Orange - Medium
    else:
        return '#0066cc'  # Blue - Low

def create_confidence_chart(results):
    """Create a professional confidence chart"""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    diseases = [r.disease_name[:20] for r in results[:5]]
    confidences = [r.confidence * 100 for r in results[:5]]
    colors = [get_confidence_color(r.confidence) for r in results[:5]]
    
    bars = ax.barh(diseases, confidences, color=colors, height=0.6, edgecolor='white', linewidth=2)
    
    ax.set_xlabel("Độ Tin Cậy (%)", fontsize=12, fontweight='bold')
    ax.set_title("Xếp Hạng Bệnh Được Chẩn Đoán (Top 5)", fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 100)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    for i, (bar, conf) in enumerate(zip(bars, confidences)):
        ax.text(conf + 2, i, f"{conf:.1f}%", va='center', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    return fig

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏥 Hệ Chuyên Gia Chuẩn Đoán Bệnh</h1>
    <p class="header-subtitle">🤖 Medical Expert System | Fuzzy Logic • AI • Clinical Evidence</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR MENU
# ============================================================================

st.sidebar.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0066cc 0%, #0052a3 100%);
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📋 MENU CHÍNH")

page = st.sidebar.radio(
    "Chọn chức năng:",
    options=[
        "🏠 Trang Chủ",
        "🩺 Chẩn Đoán Tương Tác",
        "🎯 Demo Cases",
        "📊 Cơ Sở Tri Thức",
        "🔬 Phân Tích Fuzzy Logic",
        "📈 Thống Kê"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# System info
with st.sidebar.container():
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric("Bệnh", len(st.session_state.kb.diseases), label_visibility="collapsed")
    with col2:
        st.metric("Triệu Chứng", len(st.session_state.kb.symptoms), label_visibility="collapsed")
    with col3:
        st.metric("Quy Tắc", len(st.session_state.kb.rules), label_visibility="collapsed")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### ⚠️ TUYÊN BỐ PHÁP LÝ

**Hệ thống này dùng cho:**
- ✅ Giáo dục
- ✅ Nghiên cứu
- ✅ Tham khảo

**KHÔNG áp dụng cho:**
- ❌ Chẩn đoán chính thức
- ❌ Thay thế tư vấn y khoa
- ❌ Quyết định y tế độc lập

🚨 **Trường hợp cấp cứu:** Gọi ngay 112
""")

# ============================================================================
# PAGE: TRANG CHỦ
# ============================================================================

if page == "🏠 Trang Chủ":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 👋 Chào Mừng")
        st.write("""
        **Hệ Chuyên Gia Chuẩn Đoán Bệnh** là ứng dụng AI y tế sử dụng **Fuzzy Logic** 
        để hỗ trợ chẩn đoán dựa trên triệu chứng lâm sàn.
        
        ✨ **Tính Năng Chính:**
        - 🏥 **30 Bệnh** phổ biến
        - 💊 **45 Triệu Chứng** y khoa
        - 🧠 **24 Quy Tắc** suy luận
        - 🔬 **Fuzzy Logic** tiên tiến
        - 📊 **Phân Tích** chi tiết
        """)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size: 2em;">🩺</div>
            <div class="metric-value">30</div>
            <div class="metric-label">Bệnh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size: 2em;">💊</div>
            <div class="metric-value">45</div>
            <div class="metric-label">Triệu Chứng</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size: 2em;">🧠</div>
            <div class="metric-value">24</div>
            <div class="metric-label">Quy Tắc</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size: 2em;">⚡</div>
            <div class="metric-value">100%</div>
            <div class="metric-label">Fuzzy</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🚀 Bắt Đầu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🩺 Chẩn Đoán", use_container_width=True, key="btn_diagnostic"):
            st.switch_page("pages/diagnostic.py") if False else None
        st.caption("Nhập triệu chứng để chẩn đoán")
    
    with col2:
        if st.button("🎯 Demo", use_container_width=True, key="btn_demo"):
            st.switch_page("pages/demo.py") if False else None
        st.caption("Xem các trường hợp ví dụ")
    
    with col3:
        if st.button("📊 Tri Thức", use_container_width=True, key="btn_kb"):
            st.switch_page("pages/knowledge.py") if False else None
        st.caption("Xem cơ sở tri thức")

# ============================================================================
# PAGE: CHẨN ĐOÁN TƯƠNG TÁC
# ============================================================================

elif page == "🩺 Chẩn Đoán Tương Tác":
    st.markdown("### 🩺 Phiên Chẩn Đoán Tương Tác")
    
    # Patient Information
    st.markdown("#### 👤 Thông Tin Bệnh Nhân")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        patient_name = st.text_input("Tên bệnh nhân:", value="Bệnh nhân", placeholder="Nhập tên...")
    with col2:
        patient_age = st.number_input("Tuổi:", min_value=0, max_value=120, value=30)
    with col3:
        patient_gender = st.selectbox("Giới tính:", ["👨 Nam", "👩 Nữ", "❓ Khác"])
    
    st.markdown("---")
    
    # Symptoms Selection
    st.markdown("#### 💊 Chọn Triệu Chứng (45 Triệu Chứng)")
    
    symptom_groups = {
        "🌡️ Triệu chứng toàn thân": [
            "fever", "fatigue", "headache", "body_aches", "rash", "sweating", "weakness",
            "chills", "muscle_pain", "joint_pain", "loss_of_appetite", "dizziness",
            "yellow_skin", "itching", "swollen_lymph", "sore_eyes", "back_pain",
            "neck_stiffness", "tremor"
        ],
        "🫁 Triệu chứng hô hấp": [
            "cough", "sore_throat", "runny_nose", "shortness_breath", "wheezing", "sputum_production",
            "hoarseness", "cough_with_blood", "nasal_congestion", "ear_pain", "low_oxygen"
        ],
        "🤢 Triệu chứng tiêu hóa": [
            "nausea", "vomiting", "diarrhea", "abdominal_pain", "acid_reflux", "bloody_stool", "constipation"
        ],
        "❤️ Triệu chứng tim mạch": [
            "high_blood_pressure", "low_blood_pressure", "high_heart_rate", "irregular_heartbeat", "chest_pain", "syncope"
        ],
        "👃 Triệu chứng xoang mũi": ["sinus_pressure", "sneezing"]
    }
    
    selected_symptoms = {}
    
    for group_name, symptom_ids in symptom_groups.items():
        with st.expander(group_name, expanded=(group_name == "🌡️ Triệu chứng toàn thân")):
            cols = st.columns(2)
            col_idx = 0
            
            for symptom_id in symptom_ids:
                symptom = st.session_state.kb.get_symptom(symptom_id)
                if not symptom:
                    continue
                
                with cols[col_idx % 2]:
                    st.write(f"**{symptom.name}**")
                    st.caption(f"_{symptom.description}_")
                    
                    checked = st.checkbox(f"Có {symptom.name}", key=f"check_{symptom_id}")
                    
                    if checked:
                        certainty = st.slider(
                            f"Độ chắc chắn", 0.0, 1.0, 1.0, 0.1,
                            key=f"certainty_{symptom_id}", label_visibility="collapsed"
                        )
                        
                        if symptom.is_measurable:
                            if symptom_id == "fever":
                                value = st.number_input(
                                    f"Nhiệt độ (°C)", min_value=35.0, max_value=42.0,
                                    value=37.5, step=0.1, key=f"value_{symptom_id}"
                                )
                            elif symptom_id in ["high_blood_pressure", "low_blood_pressure"]:
                                value = st.number_input(
                                    f"Huyết áp (mmHg)", min_value=40, max_value=220,
                                    value=120, step=5, key=f"value_{symptom_id}"
                                )
                            else:
                                value = st.number_input(
                                    f"Nhịp tim (lần/phút)", min_value=40, max_value=200,
                                    value=100, step=5, key=f"value_{symptom_id}"
                                )
                        else:
                            value = "có"
                        
                        selected_symptoms[symptom_id] = (value, certainty)
                    
                    col_idx += 1
    
    st.markdown("---")
    
    # Diagnosis Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Thực Hiện Chẩn Đoán", use_container_width=True, type="primary"):
            if not selected_symptoms:
                st.error("⚠️ Vui lòng chọn ít nhất một triệu chứng!")
            else:
                st.session_state.engine.clear_patient_facts()
                
                for symptom_id, (value, certainty) in selected_symptoms.items():
                    confidence_level = "high" if certainty >= 0.8 else "medium" if certainty >= 0.5 else "low"
                    fact = PatientFact(
                        symptom_id=symptom_id, value=value, certainty=certainty,
                        confidence_level=confidence_level
                    )
                    st.session_state.engine.add_patient_fact(fact)
                
                st.session_state.diagnosis_results = st.session_state.engine.diagnose()
                st.session_state.last_diagnosis_time = datetime.now()
                st.success("✅ Chẩn đoán hoàn tất!")
    
    # Display Results
    if st.session_state.diagnosis_results:
        st.markdown("---")
        st.markdown("### 📊 KẾT QUẢ CHẨN ĐOÁN")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Bệnh Nhân", patient_name)
        with col2:
            st.metric("Tuổi", f"{patient_age} tuổi")
        with col3:
            st.metric("Giới Tính", patient_gender.split()[0])
        with col4:
            st.metric("Thời Gian", st.session_state.last_diagnosis_time.strftime('%H:%M:%S'))
        
        st.markdown("---")
        
        results = st.session_state.diagnosis_results
        
        if not results:
            st.warning("⚠️ Không tìm thấy kết quả phù hợp")
        else:
            st.success(f"✅ Tìm thấy {len(results)} kết quả")
            
            # Chart
            fig = create_confidence_chart(results)
            st.pyplot(fig, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🔍 Chi Tiết Chẩn Đoán")
            
            for rank, result in enumerate(results[:3], 1):
                severity_badge = get_severity_badge(result.severity)
                
                with st.expander(f"#{rank} {result.disease_name} ({result.confidence:.1%})", expanded=(rank == 1)):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Độ Tin Cậy", f"{result.confidence:.1%}")
                    with col2:
                        st.metric("Mức Độ", f"{result.severity}")
                    with col3:
                        st.metric("Triệu Chứng", len(result.matching_symptoms))
                    
                    st.markdown("**Lý Do Chẩn Đoán:**")
                    for reason in result.reasoning:
                        st.write(f"• {reason}")

# ============================================================================
# PAGE: DEMO CASES
# ============================================================================

elif page == "🎯 Demo Cases":
    st.markdown("### 🎯 Trường Hợp Demo")
    
    demo_cases = [
        {
            "name": "Cảm Cúm",
            "description": "Sốt cao, ho, đau họng, mệt mỏi",
            "symptoms": [("fever", 39.5, 1.0), ("cough", "có", 0.9), ("sore_throat", "có", 0.85), ("fatigue", "có", 0.9)]
        },
        {
            "name": "Viêm Phổi",
            "description": "Sốt, ho liên tục, khó thở, đau ngực",
            "symptoms": [("fever", 39.0, 1.0), ("cough", "liên tục", 0.95), ("shortness_breath", "có", 0.9), ("chest_pain", "có", 0.85)]
        },
        {
            "name": "Viêm Dạ Dày Ruột",
            "description": "Buồn nôn, nôn, tiêu chảy, đau bụng",
            "symptoms": [("nausea", "có", 0.95), ("vomiting", "có", 0.9), ("diarrhea", "có", 0.95), ("abdominal_pain", "có", 0.85)]
        },
    ]
    
    for i, case in enumerate(demo_cases, 1):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"#### #{i} {case['name']}")
            st.caption(case['description'])
        with col2:
            if st.button(f"🔍 Kiểm Tra", key=f"demo_{i}"):
                st.session_state.engine.clear_patient_facts()
                for symptom_id, value, certainty in case['symptoms']:
                    fact = PatientFact(symptom_id=symptom_id, value=value, certainty=certainty)
                    st.session_state.engine.add_patient_fact(fact)
                st.session_state.diagnosis_results = st.session_state.engine.diagnose()
                st.rerun()
    
    if st.session_state.diagnosis_results:
        st.markdown("---")
        st.markdown("### 📊 Kết Quả")
        
        fig = create_confidence_chart(st.session_state.diagnosis_results)
        st.pyplot(fig, use_container_width=True)

# ============================================================================
# PAGE: CƠ SỞ TRI THỨC
# ============================================================================

elif page == "📊 Cơ Sở Tri Thức":
    st.markdown("### 📚 Cơ Sở Tri Thức")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size: 2em;">🏥</div>
            <div class="metric-value">30</div>
            <div class="metric-label">Bệnh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size: 2em;">💊</div>
            <div class="metric-value">45</div>
            <div class="metric-label">Triệu Chứng</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <div style="font-size: 2em;">🧠</div>
            <div class="metric-value">24</div>
            <div class="metric-label">Quy Tắc</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Diseases
    st.markdown("#### 🏥 30 Bệnh")
    diseases_data = []
    for disease in st.session_state.kb.diseases.values():
        diseases_data.append({
            "Bệnh": disease.name,
            "Mã ICD-10": disease.icd10_code,
            "Mức Độ": disease.severity.name,
            "Tỷ Lệ": f"{disease.prevalence:.1%}"
        })
    
    df_diseases = pd.DataFrame(diseases_data)
    st.dataframe(df_diseases, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Symptoms
    st.markdown("#### 💊 45 Triệu Chứng")
    symptoms_data = []
    for symptom in st.session_state.kb.symptoms.values():
        symptoms_data.append({
            "Triệu Chứng": symptom.name,
            "Mô Tả": symptom.description,
            "Đo Được": "✅" if symptom.is_measurable else "❌"
        })
    
    df_symptoms = pd.DataFrame(symptoms_data)
    st.dataframe(df_symptoms, use_container_width=True, hide_index=True)

# ============================================================================
# PAGE: PHÂN TÍCH FUZZY LOGIC
# ============================================================================

elif page == "🔬 Phân Tích Fuzzy Logic":
    st.markdown("### 🔬 Phân Tích Fuzzy Logic")
    
    st.info("""
    Hệ thống sử dụng **Fuzzy Logic** để xử lý sự không chắc chắn trong chẩn đoán y tế.
    
    **Các Thành Phần:**
    - Hàm Khoảng Cách (Membership Functions)
    - Toán Tử Mờ (Fuzzy Operators)
    - Quy Tắc Suyluận (Fuzzy Rules)
    - Khử Mờ (Defuzzification)
    """)

# ============================================================================
# PAGE: THỐNG KÊ
# ============================================================================

elif page == "📈 Thống Kê":
    st.markdown("### 📈 Thống Kê")
    
    st.write("Phân tích thống kê về cơ sở tri thức...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        severity_counts = {}
        for disease in st.session_state.kb.diseases.values():
            severity = disease.severity.name
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        fig, ax = plt.subplots()
        ax.pie(severity_counts.values(), labels=severity_counts.keys(), autopct='%1.0f%%', colors=['#44cc44', '#ffaa00', '#ff4444', '#ff1744'])
        st.pyplot(fig)
    
    with col2:
        st.write("**Phân Loại Theo Mức Độ Nghiêm Trọng:**")
        for severity, count in severity_counts.items():
            st.write(f"- {severity}: {count}")
