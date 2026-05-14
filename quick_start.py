"""
Quick Start Guide - Hướng Dẫn Nhanh
Cách bắt đầu sử dụng Hệ Chuyên Gia Chuẩn Đoán Bệnh
"""

# ============================================================================
# HƯỚNG DẪN 1: CHẠY CHƯƠNG TRÌNH CHÍNH
# ============================================================================

"""
Mở terminal và chạy:
    python expert_system.py

Sau đó chọn:
1. 🩺 Phiên chẩn đoán tương tác - nhập triệu chứng của bệnh nhân
2. 🎯 Xem demo - xem các ví dụ chẩn đoán
3. 📊 Xem cơ sở tri thức - xem danh sách bệnh, triệu chứng, quy tắc
4. 🚪 Thoát
"""

# ============================================================================
# HƯỚNG DẪN 2: SỬ DỤNG BẰNG CODE PYTHON
# ============================================================================

from knowledge_base import KnowledgeBase
from fuzzy_system import FuzzyLogic
from inference_engine import InferenceEngine, PatientFact

# Khởi tạo hệ thống
kb = KnowledgeBase()
fuzzy_logic = FuzzyLogic()
engine = InferenceEngine(kb, fuzzy_logic)

# Ví dụ 1: Chẩn đoán cảm cúm
print("=" * 60)
print("VÍ DỤ 1: Chẩn đoán Cảm Cúm")
print("=" * 60)

engine.clear_patient_facts()

# Thêm triệu chứng
engine.add_patient_fact(PatientFact(
    symptom_id='fever',
    value=39.5,
    certainty=1.0,
    confidence_level='high'
))

engine.add_patient_fact(PatientFact(
    symptom_id='cough',
    value='có',
    certainty=0.9,
    confidence_level='high'
))

engine.add_patient_fact(PatientFact(
    symptom_id='sore_throat',
    value='có',
    certainty=0.85,
    confidence_level='high'
))

engine.add_patient_fact(PatientFact(
    symptom_id='fatigue',
    value='có',
    certainty=0.9,
    confidence_level='high'
))

# Chẩn đoán
results = engine.diagnose()

print(f"\n✅ Kết quả chẩn đoán ({len(results)} bệnh):")
for rank, result in enumerate(results, 1):
    print(f"\n{rank}. {result.disease_name}")
    print(f"   Độ tin cậy: {result.confidence:.1%}")
    print(f"   Mức độ: {result.severity}")

# ============================================================================
# VÍ DỤ 2: Chẩn đoán Viêm Phổi
# ============================================================================

print("\n" + "=" * 60)
print("VÍ DỤ 2: Chẩn đoán Viêm Phổi")
print("=" * 60)

engine.clear_patient_facts()

# Thêm triệu chứng của viêm phổi
engine.add_patient_fact(PatientFact(
    symptom_id='fever',
    value=39.0,
    certainty=1.0,
    confidence_level='high'
))

engine.add_patient_fact(PatientFact(
    symptom_id='cough',
    value='liên tục',
    certainty=0.95,
    confidence_level='high'
))

engine.add_patient_fact(PatientFact(
    symptom_id='shortness_breath',
    value='có',
    certainty=0.9,
    confidence_level='high'
))

engine.add_patient_fact(PatientFact(
    symptom_id='chest_pain',
    value='có',
    certainty=0.85,
    confidence_level='high'
))

results = engine.diagnose()

print(f"\n✅ Kết quả chẩn đoán ({len(results)} bệnh):")
for rank, result in enumerate(results, 1):
    print(f"\n{rank}. {result.disease_name}")
    print(f"   Độ tin cậy: {result.confidence:.1%}")

# ============================================================================
# VÍ DỤ 3: Sử Dụng Fuzzy Logic Trực Tiếp
# ============================================================================

print("\n" + "=" * 60)
print("VÍ DỤ 3: Sử Dụng Fuzzy Logic")
print("=" * 60)

fuzzy = FuzzyLogic()

# Tính độ thành viên của nhiệt độ 38.5°C
temperatures = [36.5, 37, 37.5, 38, 38.5, 39, 39.5]

print("\nĐộ thành viên nhiệt độ trong các tập mờ:")
print("Nhiệt độ | Thấp (low) | Bình thường (normal) | Cao (high)")
print("-" * 55)

for temp in temperatures:
    low_membership = fuzzy.get_membership_value("temperature", "low", temp)
    normal_membership = fuzzy.get_membership_value("temperature", "normal", temp)
    high_membership = fuzzy.get_membership_value("temperature", "high", temp)
    
    print(f"{temp:6.1f}°C | {low_membership:9.3f} | {normal_membership:18.3f} | {high_membership:8.3f}")

# ============================================================================
# VÍ DỤ 4: Xem Chi Tiết Quy Tắc
# ============================================================================

print("\n" + "=" * 60)
print("VÍ DỤ 4: Xem Chi Tiết Quy Tắc Chẩn Đoán Cảm Cúm")
print("=" * 60)

# Xem các quy tắc cho bệnh cảm cúm
flu_rules = kb.get_applicable_rules('flu')

print(f"\nSố quy tắc cho bệnh cảm cúm: {len(flu_rules)}")

for rule in flu_rules:
    print(f"\nQuy tắc: {rule.id}")
    print(f"  Điều kiện (AND): {', '.join(rule.antecedents)}")
    print(f"  Bệnh: {kb.get_disease(rule.consequent).name}")
    print(f"  Độ tin cậy: {rule.confidence:.0%}")
    print(f"  Trọng số: {rule.weight}")
    print(f"  Nguồn: {rule.source}")

# ============================================================================
# VÍ DỤ 5: Xem Cơ Sở Tri Thức
# ============================================================================

print("\n" + "=" * 60)
print("VÍ DỤ 5: Thông Tin Cơ Sở Tri Thức")
print("=" * 60)

# Xem danh sách bệnh
print(f"\nTổng số bệnh: {len(kb.diseases)}")
print("\nDanh sách bệnh:")
for disease in kb.diseases.values():
    print(f"  • {disease.name:30s} [Mã: {disease.icd10_code:8s}] Tỷ lệ: {disease.prevalence:.1%}")

# Xem danh sách triệu chứng
print(f"\nTổng số triệu chứng: {len(kb.symptoms)}")
print("\nDanh sách triệu chứng:")
for symptom in list(kb.symptoms.values())[:10]:
    unit = f" ({symptom.measurement_unit})" if symptom.measurement_unit else ""
    print(f"  • {symptom.name:30s}{unit}")
print(f"  ... và {len(kb.symptoms) - 10} triệu chứng khác")

# Xem quy tắc
print(f"\nTổng số quy tắc: {len(kb.rules)}")

# ============================================================================
# VÍ DỤ 6: Chẩn Đoán Với Độ Tin Cậy Thấp
# ============================================================================

print("\n" + "=" * 60)
print("VÍ DỤ 6: Chẩn Đoán Với Triệu Chứng Không Chắc")
print("=" * 60)

engine.clear_patient_facts()

# Thêm triệu chứng với mức độ tin cậy khác nhau
engine.add_patient_fact(PatientFact(
    symptom_id='fever',
    value=37.2,
    certainty=0.5,  # Không chắc - có thể không sốt
    confidence_level='low'
))

engine.add_patient_fact(PatientFact(
    symptom_id='cough',
    value='nhẹ',
    certainty=0.6,
    confidence_level='medium'
))

results = engine.diagnose(include_threshold=0.2)

print(f"\nKết quả chẩn đoán (ngưỡng 0.2):")
if results:
    for rank, result in enumerate(results, 1):
        print(f"{rank}. {result.disease_name:30s}: {result.confidence:.1%}")
else:
    print("Không có kết quả chẩn đoán")

# ============================================================================
# VÍ DỤ 7: Xem Quá Trình Suyluận
# ============================================================================

print("\n" + "=" * 60)
print("VÍ DỤ 7: Quá Trình Suyluận Chi Tiết")
print("=" * 60)

engine.clear_patient_facts()

# Thêm một số triệu chứng
engine.add_patient_fact(PatientFact(
    symptom_id='fever',
    value=39.0,
    certainty=1.0,
    confidence_level='high'
))

engine.add_patient_fact(PatientFact(
    symptom_id='cough',
    value='có',
    certainty=0.9,
    confidence_level='high'
))

# Chẩn đoán
results = engine.diagnose()

# Xem chi tiết suyluận
print("\nChi tiết quá trình suyluận:")
print(engine.get_explanation_trace())

# ============================================================================
# VÍ DỤ 8: Debug Đánh Giá Quy Tắc
# ============================================================================

print("\n" + "=" * 60)
print("VÍ DỤ 8: Debug Đánh Giá Quy Tắc")
print("=" * 60)

engine.clear_patient_facts()

# Thêm triệu chứng
engine.add_patient_fact(PatientFact(
    symptom_id='fever',
    value=39.5,
    certainty=1.0,
    confidence_level='high'
))

engine.add_patient_fact(PatientFact(
    symptom_id='cough',
    value='có',
    certainty=0.9,
    confidence_level='high'
))

# Debug
debug_info = engine.debug_rule_evaluation('flu')

print(f"\nDebug chẩn đoán: {debug_info['disease_name']}")
print(f"Số quy tắc: {len(debug_info['rules'])}")

for i, rule in enumerate(debug_info['rules'], 1):
    print(f"\nQuy tắc {i}: {rule['rule_id']}")
    print(f"  Điều kiện: {', '.join(rule['antecedents'])}")
    print(f"  Độ tin cậy quy tắc: {rule['confidence']:.0%}")
    print(f"  Trọng số: {rule['weight']}")
    print(f"  Độ tin cậy đánh giá: {rule['evaluated_confidence']:.1%}")

# ============================================================================
# VÍ DỤ 9: Tạo Hệ Thống Mới Với Cơ Sở Tri Thức Tùy Chỉnh
# ============================================================================

print("\n" + "=" * 60)
print("VÍ DỤ 9: Cơ Sở Tri Thức Tùy Chỉnh (Advanced)")
print("=" * 60)

from knowledge_base import Symptom, Disease, Rule, Severity

# Tạo cơ sở tri thức mới
custom_kb = KnowledgeBase()

# Thêm triệu chứng mới
custom_kb.add_symptom(Symptom(
    id="rash",
    name="Phát ban",
    description="Phát ban trên da",
    is_measurable=False
))

# Thêm bệnh mới
custom_kb.add_disease(Disease(
    id="measles",
    name="Sởi",
    description="Bệnh sởi",
    severity=Severity.MODERATE,
    icd10_code="B05"
))

# Thêm quy tắc mới
custom_kb.add_rule(Rule(
    id="r_measles_1",
    antecedents=["fever", "rash", "cough"],
    consequent="measles",
    confidence=0.8
))

print("✅ Thêm thành công:")
print(f"  Triệu chứng: {custom_kb.get_symptom('rash').name}")
print(f"  Bệnh: {custom_kb.get_disease('measles').name}")
print(f"  Quy tắc: r_measles_1")

# ============================================================================
# NHƯNG NHỚ: LUÔN LIÊN HỆ BÁC SĨ CHO CHẨN ĐOÁN CHÍNH THỨC
# ============================================================================

print("\n" + "=" * 70)
print("⚠️  LƯU Ý QUAN TRỌNG")
print("=" * 70)
print("""
Hệ chuyên gia này chỉ dùng cho MỤC ĐÍCH GIÁO DỤC VÀ NGHIÊN CỨU.

🚨 KHÔNG THAY THẾ TƯ VẤN Y KHOA CHUYÊN NGHIỆP

⚠️  Kết quả từ hệ chuyên gia CÓ THỂ CÓ SAI SÓT
⚠️  LUÔN LIÊN HỆ BÁC SĨ CHO CHẨN ĐOÁN VÀ ĐIỀU TRỊ CHÍNH THỨC
⚠️  TRƯỜNG HỢP CẤP CỨU: GỌI NGAY ĐƯỜNG DÂY CẤPỨU

Người dùng chịu trách nhiệm hoàn toàn về các quyết định y tế của mình.
""")

print("=" * 70)
print("\n✅ Hoàn tất các ví dụ Quick Start!")
print("\nNhập lệnh sau để chạy chương trình chính:")
print("    python expert_system.py")
print("=" * 70)
