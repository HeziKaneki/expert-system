"""
Hệ Chuyên Gia Chuẩn Đoán Bệnh
Ứng dụng chính tích hợp tất cả các thành phần
"""

import sys
from typing import List, Dict, Optional
from datetime import datetime
from knowledge_base import KnowledgeBase, Disease, Symptom
from fuzzy_system import FuzzyLogic
from inference_engine import InferenceEngine, PatientFact, DiagnosisResult


class MedicalExpertSystem:
    """Hệ chuyên gia chuẩn đoán bệnh chính"""
    
    def __init__(self):
        """Khởi tạo hệ chuyên gia"""
        print("🏥 Khởi tạo Hệ Chuyên Gia Chuẩn Đoán Bệnh...")
        
        self.kb = KnowledgeBase()
        self.fuzzy_logic = FuzzyLogic()
        self.inference_engine = InferenceEngine(self.kb, self.fuzzy_logic)
        
        # Xác thực cơ sở tri thức
        validation_result = self.kb.validate_knowledge_base()
        print(f"✅ Cơ sở tri thức: {validation_result['total_diseases']} bệnh, "
              f"{validation_result['total_symptoms']} triệu chứng, "
              f"{validation_result['total_rules']} quy tắc")
        print(f"   Trạng thái: {validation_result['validation_status']}")
        
        if validation_result['consistency_issues']:
            print("⚠️  Các vấn đề nhất quán:")
            for issue in validation_result['consistency_issues']:
                print(f"   - {issue}")
        
        print("=" * 70)
    
    def interactive_session(self):
        """Phiên làm việc tương tác với người dùng"""
        print("\n🔍 PHIÊN TƯƠNG TÁC - NHẬP THÔNG TIN BỆNH NHÂN")
        print("=" * 70)
        
        # Thu thập thông tin bệnh nhân
        patient_info = self._collect_patient_information()
        
        # Thực hiện chẩn đoán
        diagnosis_results = self.inference_engine.diagnose()
        
        # Hiển thị kết quả
        self._display_diagnosis_results(diagnosis_results, patient_info)
    
    def _collect_patient_information(self) -> Dict:
        """Thu thập thông tin bệnh nhân"""
        patient_info = {}
        
        print("\n📝 Nhập thông tin bệnh nhân:")
        patient_info['name'] = input("Tên bệnh nhân: ").strip() or "Bệnh nhân"
        patient_info['age'] = input("Tuổi: ").strip() or "N/A"
        patient_info['gender'] = input("Giới tính (Nam/Nữ): ").strip() or "N/A"
        
        print("\n🩺 Nhập các triệu chứng hiện tại (nhập 'done' để kết thúc):")
        print("-" * 70)
        self._print_available_symptoms()
        
        print("\n💡 Nhập các triệu chứng (ID hoặc tên):")
        
        while True:
            user_input = input("Triệu chứng: ").strip().lower()
            
            if user_input == 'done':
                break
            
            if not user_input:
                continue
            
            # Tìm triệu chứng theo ID hoặc tên
            symptom = self._find_symptom(user_input)
            
            if symptom:
                value = input(f"  Giá trị/Mô tả cho '{symptom.name}': ").strip() or "Có"
                
                # Xác định mức độ tin cậy
                if symptom.is_measurable:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                
                certainty_input = input("  Độ chắc chắn (1=chắc, 0.7=khá chắc, 0.5=không chắc) [mặc định 1.0]: ").strip()
                try:
                    certainty = float(certainty_input) if certainty_input else 1.0
                    certainty = max(0.0, min(1.0, certainty))
                except ValueError:
                    certainty = 1.0
                
                # Xác định mức độ tin cậy
                if certainty >= 0.8:
                    confidence_level = "high"
                elif certainty >= 0.5:
                    confidence_level = "medium"
                else:
                    confidence_level = "low"
                
                # Thêm sự kiện
                fact = PatientFact(
                    symptom_id=symptom.id,
                    value=value,
                    certainty=certainty,
                    confidence_level=confidence_level
                )
                self.inference_engine.add_patient_fact(fact)
                print(f"  ✓ Đã thêm: {symptom.name}")
            else:
                print(f"  ❌ Không tìm thấy triệu chứng: '{user_input}'")
        
        return patient_info
    
    def _find_symptom(self, user_input: str) -> Optional[Symptom]:
        """Tìm triệu chứng theo ID hoặc tên"""
        # Tìm theo ID trước
        if user_input in self.kb.symptoms:
            return self.kb.symptoms[user_input]
        
        # Tìm theo tên (không phân biệt chữ hoa/thường)
        for symptom in self.kb.symptoms.values():
            if user_input in symptom.name.lower() or symptom.name.lower() in user_input:
                return symptom
        
        return None
    
    def _print_available_symptoms(self):
        """Hiển thị danh sách triệu chứng có sẵn"""
        print("\nTriệu chứng khả dụng:")
        for i, (symptom_id, symptom) in enumerate(self.kb.symptoms.items(), 1):
            unit = f" ({symptom.measurement_unit})" if symptom.measurement_unit else ""
            print(f"  {i:2d}. {symptom_id:20s} - {symptom.name}{unit}")
            if i % 3 == 0:
                print()
    
    def _display_diagnosis_results(self, results: List[DiagnosisResult], patient_info: Dict):
        """Hiển thị kết quả chẩn đoán"""
        print("\n" + "=" * 70)
        print("📊 KẾT QUẢ CHẨN ĐOÁN")
        print("=" * 70)
        
        print(f"\n👤 Bệnh nhân: {patient_info['name']}")
        print(f"   Tuổi: {patient_info['age']}, Giới tính: {patient_info['gender']}")
        print(f"   Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not results:
            print("\n⚠️  Không tìm thấy bệnh phù hợp dựa trên các triệu chứng cung cấp.")
            print("💡 Vui lòng liên hệ bác sĩ để được khám sâu hơn.")
        else:
            print(f"\n🔍 Tìm thấy {len(results)} kết quả chẩn đoán:")
            print("-" * 70)
            
            for rank, result in enumerate(results, 1):
                self._print_diagnosis_result(rank, result)
        
        # Hiển thị lịch sử suy luận
        if input("\n📋 Xem chi tiết quá trình suy luận? (y/n): ").lower() == 'y':
            print("\n" + "=" * 70)
            print("🔬 CHI TIẾT SỰ SUYLUẬN")
            print("=" * 70)
            trace = self.inference_engine.get_explanation_trace()
            print(trace)
    
    def _print_diagnosis_result(self, rank: int, result: DiagnosisResult):
        """Hiển thị một kết quả chẩn đoán"""
        # Chọn biểu tượng dựa trên độ tin cậy
        if result.confidence >= 0.8:
            icon = "🔴"
        elif result.confidence >= 0.6:
            icon = "🟠"
        elif result.confidence >= 0.4:
            icon = "🟡"
        else:
            icon = "⚪"
        
        print(f"\n{rank}. {icon} {result.disease_name.upper()}")
        print(f"   Độ tin cậy: {result.confidence:.1%}")
        print(f"   Mức độ nghiêm trọng: {result.severity}")
        
        print(f"   Triệu chứng phù hợp ({len(result.matching_symptoms)}):")
        for symptom_id in result.matching_symptoms[:5]:
            symptom = self.kb.get_symptom(symptom_id)
            if symptom:
                print(f"      • {symptom.name}")
        
        if len(result.matching_symptoms) > 5:
            print(f"      ... và {len(result.matching_symptoms) - 5} triệu chứng khác")
        
        print(f"   Lý do chẩn đoán:")
        for reason in result.reasoning:
            print(f"      • {reason}")
        
        print(f"   Khuyến nghị:")
        for recommendation in result.recommended_actions:
            print(f"      ⚕️  {recommendation}")
    
    def demo_session(self):
        """Phiên demo với dữ liệu mẫu"""
        print("\n" + "=" * 70)
        print("🎯 DEMO - CÁC TRƯỜNG HỢP CHẨN ĐOÁN MẪU")
        print("=" * 70)
        
        demo_cases = [
            {
                "name": "TRƯỜNG HỢP 1: Triệu chứng cảm cúm",
                "symptoms": [
                    ("fever", 39.5, 1.0),
                    ("cough", "có", 0.9),
                    ("sore_throat", "có", 0.85),
                    ("fatigue", "có", 0.9),
                    ("headache", "có", 0.7),
                ]
            },
            {
                "name": "TRƯỜNG HỢP 2: Triệu chứng viêm phổi",
                "symptoms": [
                    ("fever", 39.0, 1.0),
                    ("cough", "liên tục", 0.95),
                    ("shortness_breath", "có", 0.9),
                    ("chest_pain", "có", 0.85),
                    ("fatigue", "nặng", 0.9),
                ]
            },
            {
                "name": "TRƯỜNG HỢP 3: Triệu chứng viêm dạ dày ruột",
                "symptoms": [
                    ("nausea", "có", 0.95),
                    ("vomiting", "đột ngột", 0.9),
                    ("diarrhea", "có", 0.95),
                    ("abdominal_pain", "đau", 0.85),
                    ("fever", 37.8, 0.6),
                ]
            },
            {
                "name": "TRƯỜNG HỢP 4: Triệu chứng bệnh tim mạch",
                "symptoms": [
                    ("chest_pain", "đau tức", 0.95),
                    ("shortness_breath", "nặng", 0.9),
                    ("high_heart_rate", 120, 0.95),
                    ("high_blood_pressure", 160, 0.9),
                    ("fatigue", "có", 0.8),
                ]
            },
            {
                "name": "TRƯỜNG HỢP 5: Cảm lạnh thông thường",
                "symptoms": [
                    ("runny_nose", "chảy", 0.95),
                    ("sore_throat", "nhẹ", 0.8),
                    ("cough", "nhẹ", 0.7),
                    ("headache", "nhẹ", 0.6),
                    ("fever", 37.2, 0.5),
                ]
            }
        ]
        
        for case in demo_cases:
            print(f"\n{'='*70}")
            print(f"📋 {case['name']}")
            print(f"{'='*70}")
            
            self.inference_engine.clear_patient_facts()
            
            # Thêm các triệu chứng
            for symptom_id, value, certainty in case['symptoms']:
                confidence_level = "high" if certainty >= 0.8 else "medium" if certainty >= 0.5 else "low"
                fact = PatientFact(
                    symptom_id=symptom_id,
                    value=value,
                    certainty=certainty,
                    confidence_level=confidence_level
                )
                self.inference_engine.add_patient_fact(fact)
            
            # Chẩn đoán
            results = self.inference_engine.diagnose()
            
            # Hiển thị
            patient_info = {
                'name': f"Demo {case['name'].split(':')[0]}",
                'age': "N/A",
                'gender': "N/A"
            }
            
            if results:
                print(f"\n✅ Kết quả chẩn đoán ({len(results)} bệnh):")
                for rank, result in enumerate(results[:3], 1):
                    print(f"  {rank}. {result.disease_name}: {result.confidence:.1%}")
            else:
                print("\n⚠️  Không có kết quả chẩn đoán")
    
    def run(self):
        """Chạy hệ chuyên gia"""
        while True:
            print("\n" + "=" * 70)
            print("🏥 HỆ CHUYÊN GIA CHUẨN ĐOÁN BỆNH")
            print("=" * 70)
            print("1. 🩺 Phiên chẩn đoán tương tác (nhập triệu chứng)")
            print("2. 🎯 Xem demo các trường hợp mẫu")
            print("3. 📊 Xem thông tin cơ sở tri thức")
            print("4. 🚪 Thoát")
            print("=" * 70)
            
            choice = input("Lựa chọn (1-4): ").strip()
            
            if choice == '1':
                self.interactive_session()
            elif choice == '2':
                self.demo_session()
            elif choice == '3':
                self._display_knowledge_base_info()
            elif choice == '4':
                print("\n👋 Cảm ơn bạn đã sử dụng Hệ Chuyên Gia Chuẩn Đoán Bệnh!")
                break
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng thử lại.")
    
    def _display_knowledge_base_info(self):
        """Hiển thị thông tin cơ sở tri thức"""
        print("\n" + "=" * 70)
        print("📚 THÔNG TIN CƠ SỞ TRI THỨC")
        print("=" * 70)
        
        print(f"\n📋 Các bệnh trong cơ sở dữ liệu ({len(self.kb.diseases)}):")
        for disease in self.kb.diseases.values():
            print(f"  • {disease.name:30s} [Mã ICD-10: {disease.icd10_code}]")
            print(f"    Mức độ: {disease.severity.name:12s} Tỷ lệ: {disease.prevalence:.1%}")
        
        print(f"\n🩺 Triệu chứng trong cơ sở dữ liệu ({len(self.kb.symptoms)}):")
        for i, symptom in enumerate(self.kb.symptoms.values(), 1):
            unit = f" ({symptom.measurement_unit})" if symptom.measurement_unit else ""
            print(f"  {i:2d}. {symptom.name:30s}{unit}")
        
        print(f"\n📏 Quy tắc suyluận ({len(self.kb.rules)}):")
        print(f"  Tổng số quy tắc: {len(self.kb.rules)}")
        
        # Thống kê quy tắc theo bệnh
        rules_by_disease = {}
        for rule in self.kb.rules.values():
            disease_id = rule.consequent
            rules_by_disease[disease_id] = rules_by_disease.get(disease_id, 0) + 1
        
        print(f"  Phân bổ theo bệnh:")
        for disease_id, count in sorted(rules_by_disease.items()):
            disease = self.kb.get_disease(disease_id)
            if disease:
                print(f"    • {disease.name:30s}: {count} quy tắc")


def main():
    """Hàm chính"""
    try:
        expert_system = MedicalExpertSystem()
        expert_system.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Chương trình bị dừng bởi người dùng.")
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
