# 🏥 Hệ Chuyên Gia Chuẩn Đoán Bệnh (Medical Expert System)

## 📋 Tổng Quan

**Hệ Chuyên Gia Chuẩn Đoán Bệnh** là một ứng dụng **AI/Expert System** tiên tiến được phát triển bằng Python, sử dụng các công nghệ:
- **Fuzzy Logic** (Logic Mờ) - Xử lý độ không chắc chắn y khoa
- **Knowledge Base** (Cơ sở Tri Thức) - Chứa quy tắc y khoa chuyên sâu
- **Inference Engine** (Engine Suyluận) - Suy luận logic mờ để chẩn đoán
- **Fact Base** (Cơ sở Dữ Kiện) - Thu thập dữ liệu bệnh nhân

Hệ thống được thiết kế để:
1. ✅ Chuẩn khắt khe về tiêu chí y khoa
2. ✅ Xử lý độ không chắc chắn của dữ liệu lâm sàng
3. ✅ Cung cấp giải thích cho các chẩn đoán
4. ✅ Đưa ra khuyến nghị hành động

---

## 📁 Cấu Trúc Dự Án

```
He_Chuyen_Gia/
├── fuzzy_system.py           # Hệ thống Fuzzy Logic
├── knowledge_base.py          # Cơ sở tri thức y khoa
├── inference_engine.py        # Engine suyluận
├── expert_system.py           # Ứng dụng chính
├── test_expert_system.py      # Bài kiểm thử
└── README.md                  # Tài liệu này
```

---

## 🧬 Các Thành Phần Chính

### 1. **fuzzy_system.py** - Hệ Thống Logic Mờ

#### Các hàm thành viên mờ:
```
- Triangular (Tam giác)
- Trapezoidal (Hình thang)
- Gaussian (Gaussian/Chuông)
```

#### Các biến mờ:
- **Nhiệt độ** (°C): low, normal, high
- **Huyết áp** (mmHg): low, normal, high
- **Nhịp tim** (nhịp/phút): low, normal, high
- **Độ tin cậy** (%): low, medium, high

#### Toán tử mờ:
- **AND** (t-norm): min
- **OR** (t-conorm): max
- **NOT**: 1 - x
- **Defuzzification**: Centroid method

**Ví dụ:**
```python
fuzzy = FuzzyLogic()
# Tính độ thành viên nhiệt độ 38.5°C trong tập "cao"
membership = fuzzy.get_membership_value("temperature", "high", 38.5)
```

---

### 2. **knowledge_base.py** - Cơ Sở Tri Thức

#### Các thành phần:

**a) Triệu Chứng (Symptoms):**
- ID: fever, cough, sore_throat, ...
- Tên: Sốt cao, Ho, Đau họng, ...
- Mô tả chi tiết
- Giá trị điển hình
- Đơn vị đo lường (nếu có)

**b) Bệnh (Diseases):**
- ID: flu, pneumonia, gastroenteritis, ...
- Tên: Cảm cúm, Viêm phổi, Viêm dạ dày ruột, ...
- Mô tả y khoa
- Mã ICD-10
- Mức độ nghiêm trọng (MILD, MODERATE, SEVERE, CRITICAL)
- Tỷ lệ mắc bệnh

**c) Quy Tắc (Rules):**
```
IF (symptoms) THEN (disease) WITH confidence
```

**Ví dụ quy tắc:**
```
Rule: r_flu_1
IF (fever AND cough AND sore_throat AND fatigue)
THEN (flu) WITH confidence 0.85
```

**d) Ánh Xạ:**
- Symptom → Disease
- Disease → Symptoms

#### Xác thực cơ sở tri thức:
```python
kb = KnowledgeBase()
validation = kb.validate_knowledge_base()
# Kiểm tra:
# - Tính nhất quán (referential integrity)
# - Quy tắc tham chiếu đến triệu chứng/bệnh tồn tại
```

---

### 3. **inference_engine.py** - Engine Suyluận

#### Chức năng chính:

**a) Đánh giá quy tắc mờ:**
```
score = min_satisfaction(antecedents) × rule.confidence × rule.weight
```

**b) Tính toán độ tin cậy chẩn đoán:**
```
confidence = 0.7 × avg_rule_confidence + 0.3 × symptom_coverage
```

**c) Suyluận (Forward Chaining):**
1. Thu thập sự kiện bệnh nhân
2. Đánh giá tất cả quy tắc
3. Tính độ tin cậy cho mỗi bệnh
4. Sắp xếp kết quả

#### Thuộc tính PatientFact:
```python
fact = PatientFact(
    symptom_id="fever",
    value=39.5,           # Giá trị hoặc mô tả
    certainty=1.0,        # [0, 1]
    confidence_level="high"  # "high", "medium", "low"
)
```

#### Kết quả chẩn đoán (DiagnosisResult):
```python
result = DiagnosisResult(
    disease_id="pneumonia",
    disease_name="Viêm phổi",
    confidence=0.85,      # [0, 1]
    severity="SEVERE",
    matching_symptoms=[...],
    reasoning=[...],
    recommended_actions=[...]
)
```

---

### 4. **expert_system.py** - Ứng Dụng Chính

#### Các chức năng:

**1. Phiên tương tác:**
- Nhập thông tin bệnh nhân (tên, tuổi, giới tính)
- Chọn triệu chứng
- Nhập giá trị và mức độ tin cậy
- Nhận kết quả chẩn đoán chi tiết

**2. Demo các trường hợp mẫu:**
- Cảm cúm
- Viêm phổi
- Viêm dạ dày ruột
- Bệnh tim mạch
- Cảm lạnh

**3. Xem cơ sở tri thức:**
- Danh sách bệnh, triệu chứng
- Thống kê quy tắc
- Phân bổ quy tắc theo bệnh

---

## 🚀 Cách Sử Dụng

### Chạy ứng dụng chính:

```bash
python expert_system.py
```

**Menu tương tác:**
```
🏥 HỆ CHUYÊN GIA CHUẨN ĐOÁN BỆNH
=====================================
1. 🩺 Phiên chẩn đoán tương tác
2. 🎯 Xem demo các trường hợp mẫu
3. 📊 Xem thông tin cơ sở tri thức
4. 🚪 Thoát
```

### Chạy bài kiểm thử:

```bash
python test_expert_system.py
```

---

## 📊 Ví Dụ Chẩn Đoán

### Trường hợp 1: Cảm cúm

**Nhập:**
```
Triệu chứng:
- Sốt cao: 39.5°C (độ chắc: 1.0)
- Ho: có (độ chắc: 0.9)
- Đau họng: có (độ chắc: 0.85)
- Mệt mỏi: có (độ chắc: 0.9)
- Đau đầu: có (độ chắc: 0.7)
```

**Kết quả:**
```
🔴 CẢM CÚM
Độ tin cậy: 85%
Mức độ nghiêm trọng: MODERATE

Triệu chứng phù hợp (5):
• Sốt cao
• Ho
• Đau họng
• Mệt mỏi
• Đau đầu

Khuyến nghị:
📋 ĐỘ NẶNG TRUNG BÌNH: Tham khảo bác sĩ trong 24 giờ
Tránh bỏ lỡ các triệu chứng mới hoặc xấu đi
Uống đủ nước và nghỉ ngơi
```

### Trường hợp 2: Viêm phổi

**Nhập:**
```
Triệu chứng:
- Sốt cao: 39.0°C
- Ho: liên tục
- Khó thở: có
- Đau ngực: có
- Mệt mỏi: nặng
```

**Kết quả:**
```
🔴 VIÊM PHỔI
Độ tin cậy: 87%
Mức độ nghiêm trọng: SEVERE

Khuyến nghị:
⚠️  NẶNG: Liên hệ bác sĩ chuyên khoa ngay
```

---

## 🔧 Chi Tiết Kỹ Thuật

### 1. Fuzzy Logic Implementation

**Hàm thành viên Triangular:**
```
     |
   / \
  /   \
 /     \
a   b   c

μ(x) = 0           if x ≤ a or x ≥ c
       (x-a)/(b-a) if a < x ≤ b
       (c-x)/(c-b) if b < x < c
```

**Hàm thành viên Trapezoidal:**
```
   |_____|
  /       \
 /         \
a  b  c     d

μ(x) = 0           if x ≤ a or x ≥ d
       (x-a)/(b-a) if a < x ≤ b
       1           if b < x < c
       (d-x)/(d-c) if c ≤ x < d
```

**Hàm thành viên Gaussian:**
```
μ(x) = exp(-0.5 * ((x - mean) / σ)²)
```

### 2. Inference Logic

**Đánh giá quy tắc:**
```
confidence_rule = min(antecedent_satisfactions) × confidence_value × weight
```

**Tính chẩn đoán tổng thể:**
```
confidence_disease = 0.7 × avg(rule_confidences) + 0.3 × symptom_coverage_ratio
```

**Xử lý độ không chắc chắn:**
- Mức độ tin cậy cao (certainty ≥ 0.8): weight = 1.0
- Mức độ tin cậy trung bình (0.5 ≤ certainty < 0.8): weight = 0.7
- Mức độ tin cậy thấp (certainty < 0.5): weight = 0.4

### 3. Decision Making

**Ngưỡng chẩn đoán:**
- confidence ≥ 0.8: Chẩn đoán chắc chắn 🔴
- 0.6 ≤ confidence < 0.8: Chẩn đoán khả năng cao 🟠
- 0.4 ≤ confidence < 0.6: Chẩn đoán khả năng trung bình 🟡
- confidence < 0.4: Chẩn đoán khả năng thấp ⚪

---

## 📚 Cơ Sở Tri Thức Hiện Tại

### Bệnh (7 loại):
1. **Cảm cúm** (Influenza)
2. **Cảm lạnh** (Common Cold)
3. **Viêm phế quản** (Bronchitis)
4. **Viêm phổi** (Pneumonia)
5. **Viêm dạ dày ruột** (Gastroenteritis)
6. **Cao huyết áp** (Hypertension)
7. **Bệnh tim mạch** (Heart Disease)

### Triệu chứng (18 loại):
- Sốt cao, Ho, Đau họng, Chảy nước mũi
- Đau đầu, Mệt mỏi, Đau cơ thể, Khó thở
- Buồn nôn, Nôn, Tiêu chảy, Đau bụng
- Huyết áp cao/thấp, Nhịp tim nhanh, Đau ngực

### Quy tắc (14+ quy tắc):
- Mỗi bệnh có 1-2 quy tắc chẩn đoán
- Độ tin cậy: 0.65 - 0.95
- Nguồn: WHO guidelines, CDC guidelines, Clinical evidence

---

## 🧪 Bài Kiểm Thử

### Chạy tất cả bài kiểm thử:
```bash
python test_expert_system.py
```

### Danh sách bài kiểm thử:

**TestFuzzySystem (5 bài):**
- ✓ test_triangular_membership
- ✓ test_trapezoidal_membership
- ✓ test_gaussian_membership
- ✓ test_fuzzy_operators
- ✓ test_membership_initialization

**TestKnowledgeBase (7 bài):**
- ✓ test_symptoms_added
- ✓ test_diseases_added
- ✓ test_rules_added
- ✓ test_symptom_disease_mapping
- ✓ test_knowledge_base_validation
- ✓ test_get_symptom
- ✓ test_get_disease

**TestInferenceEngine (7 bài):**
- ✓ test_add_patient_fact
- ✓ test_clear_patient_facts
- ✓ test_flu_diagnosis
- ✓ test_pneumonia_diagnosis
- ✓ test_gastroenteritis_diagnosis
- ✓ test_no_diagnosis_with_unrelated_symptoms
- ✓ test_diagnosis_confidence_scores

---

## 📖 API Reference

### Fuzzy Logic
```python
fuzzy = FuzzyLogic()

# Tính độ thành viên
membership = fuzzy.get_membership_value("temperature", "high", 38.5)

# Lấy tất cả độ thành viên
memberships = fuzzy.get_all_memberships("heart_rate", 110)

# Toán tử mờ
and_result = FuzzyLogic.and_operator([0.8, 0.6, 0.9])
or_result = FuzzyLogic.or_operator([0.8, 0.6, 0.9])
not_result = FuzzyLogic.not_operator(0.7)
```

### Knowledge Base
```python
kb = KnowledgeBase()

# Lấy triệu chứng/bệnh
symptom = kb.get_symptom("fever")
disease = kb.get_disease("flu")

# Ánh xạ
diseases = kb.get_diseases_for_symptom("fever")
symptoms = kb.get_symptoms_for_disease("flu")

# Quy tắc
rules = kb.get_applicable_rules("flu")

# Xác thực
validation = kb.validate_knowledge_base()
```

### Inference Engine
```python
engine = InferenceEngine(kb, fuzzy)

# Thêm sự kiện
fact = PatientFact(
    symptom_id="fever",
    value=39.5,
    certainty=1.0,
    confidence_level="high"
)
engine.add_patient_fact(fact)

# Chẩn đoán
results = engine.diagnose(include_threshold=0.3)

# Giải thích
trace = engine.get_explanation_trace()

# Debug
debug_info = engine.debug_rule_evaluation("flu")
```

---

## 🎯 Cải Tiến Tương Lai

### 1. Mở Rộng Cơ Sở Tri Thức
- [ ] Thêm 50+ bệnh mới
- [ ] Thêm 100+ triệu chứng
- [ ] Thêm xét nghiệm và chỉ số lâm sàn

### 2. Nâng Cao Fuzzy Logic
- [ ] Thêm hàm thành viên phức tạp hơn
- [ ] Hỗ trợ các t-norm/t-conorm khác
- [ ] Fuzzy rules với multiple consequents

### 3. Cải Thiện Suyluận
- [ ] Backward chaining
- [ ] Heuristic search
- [ ] Learning from misdiagnosis
- [ ] Confidence interval calculation

### 4. Giao Diện Người Dùng
- [ ] Web interface (Flask/Django)
- [ ] Mobile app (Flutter)
- [ ] REST API
- [ ] Visualization dashboard

### 5. Tích Hợp Dữ Liệu
- [ ] Đọc kết quả xét nghiệm từ file
- [ ] Kết nối cơ sở dữ liệu bệnh nhân
- [ ] Export kết quả (PDF, JSON, XML)

---

## ⚖️ Tiêu Chuẩn Chất Lượng

### Yêu cầu tiêu chuẩn:
- ✅ Knowledge Base có tính nhất quán
- ✅ Fuzzy Logic xử lý độ không chắc chắn
- ✅ Inference Engine có truy vết giải thích
- ✅ Kết quả có độ tin cậy rõ ràng
- ✅ Code có test coverage > 80%
- ✅ Documentation đầy đủ

### Kiểm thử chất lượng:
- Unit tests: 19 bài
- Integration tests: Demo cases
- Validation: Knowledge base consistency

---

## 📝 Ghi Chú Quan Trọng

⚠️ **TUYÊN BỐ PHÁP LÝ:**

Hệ chuyên gia này được phát triển cho mục đích **GIÁO DỤC VÀ NGHIÊN CỨU**.

⚠️ **KHÔNG thay thế:** Tư vấn y khoa chuyên nghiệp
⚠️ **CÓ THỂ CÓ SAI SÓT:** Kết quả cần xác nhận bởi bác sĩ
⚠️ **TRÁCH NHIỆM:** Người dùng chịu trách nhiệm về quyết định y tế

**LUÔN LIÊN HỆ BÁC SĨ CHO CHẨN ĐOÁN VÀ ĐIỀU TRỊ CHÍNH THỨC**

---

## 👨‍💻 Phát Triển Bởi

**Hệ Chuyên Gia Chuẩn Đoán Bệnh**
- Expert System với Fuzzy Logic
- Knowledge Base Y Khoa
- Inference Engine Python
- Version: 1.0
- Date: 2026

---

## 📞 Liên Hệ & Hỗ Trợ

Để báo cáo lỗi, đề xuất cải tiến, hoặc có câu hỏi:
- 📧 Email: support@medicalsystem.com
- 💬 Issues: GitHub Issues
- 📖 Wiki: Documentation

---

**Made with ❤️ for Medical Education & Research**
