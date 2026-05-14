"""
Inference Engine cho Hệ Chuyên Gia Chuẩn Đoán Bệnh
Thực hiện suy luận logic mờ để đưa ra chẩn đoán
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
import math
from knowledge_base import KnowledgeBase, Rule
from fuzzy_system import FuzzyLogic, SymptomFuzzifier


@dataclass
class PatientFact:
    """Dữ liệu bệnh nhân"""
    symptom_id: str
    value: any  # Giá trị hoặc mức độ
    certainty: float = 1.0  # Độ tin cậy [0, 1]
    confidence_level: str = "high"  # high, medium, low
    
    def __hash__(self):
        return hash(self.symptom_id)


@dataclass
class DiagnosisResult:
    """Kết quả chẩn đoán"""
    disease_id: str
    disease_name: str
    confidence: float  # [0, 1]
    reasoning: List[str] = field(default_factory=list)
    matching_symptoms: List[str] = field(default_factory=list)
    severity: str = "unknown"
    recommended_actions: List[str] = field(default_factory=list)
    
    def __lt__(self, other):
        """So sánh dựa trên confidence"""
        return self.confidence < other.confidence


class InferenceEngine:
    """
    Engine suy luận cho chẩn đoán bệnh
    Sử dụng logic mờ và suy luận lan truyền
    """
    
    # GIẢI PHÁP 3: Trọng số triệu chứng (Symptom Importance Weights)
    # Triệu chứng quan trọng hơn có trọng số cao hơn
    SYMPTOM_WEIGHTS = {
        # Triệu chứng nguy hiểm nhất (weight=2.0)
        "chest_pain": 2.0,              # Đau ngực = nguy hiểm
        "shortness_breath": 2.0,        # Khó thở = nguy hiểm
        
        # Triệu chứng chính (weight=1.5)
        "fever": 1.5,                   # Sốt cao = triệu chứng chính
        "cough": 1.5,                   # Ho = triệu chứng chính
        "high_heart_rate": 1.5,         # Nhịp tim nhanh = quan trọng
        "high_blood_pressure": 1.5,     # Huyết áp cao = quan trọng
        
        # Triệu chứng phụ trợ (weight=1.0 - normal)
        "sore_throat": 1.0,
        "headache": 1.0,
        "fatigue": 1.0,
        "body_aches": 1.0,
        "runny_nose": 1.0,
        
        # Triệu chứng ít quan trọng (weight=0.8)
        "nausea": 0.8,
        "vomiting": 0.8,
        "diarrhea": 0.8,
        "abdominal_pain": 0.8,
        "low_blood_pressure": 0.8,
    }
    
    def __init__(self, knowledge_base: KnowledgeBase, fuzzy_logic: FuzzyLogic):
        self.kb = knowledge_base
        self.fuzzy_logic = fuzzy_logic
        self.fuzzifier = SymptomFuzzifier(fuzzy_logic)
        self.patient_facts: Dict[str, PatientFact] = {}
        self.derived_facts: Dict[str, float] = {}  # disease_id -> confidence
        self.explanation_trace: List[str] = []
    
    def add_patient_fact(self, fact: PatientFact):
        """Thêm sự kiện về bệnh nhân"""
        self.patient_facts[fact.symptom_id] = fact
        self.explanation_trace.append(f"Thêm triệu chứng: {fact.symptom_id} = {fact.value}")
    
    def clear_patient_facts(self):
        """Xóa tất cả sự kiện của bệnh nhân"""
        self.patient_facts.clear()
        self.derived_facts.clear()
        self.explanation_trace.clear()
    
    def _evaluate_rule_fuzzy(self, rule: Rule) -> float:
        """
        Đánh giá quy tắc bằng logic mờ
        Tính toán mức độ thỏa mãn của quy tắc
        
        ✅ GIẢI PHÁP 3: Áp dụng trọng số triệu chứng
        Triệu chứng quan trọng hơn được trọng số cao hơn
        
        Args:
            rule: Quy tắc cần đánh giá
        
        Returns:
            Mức độ thỏa mãn (0-1)
        """
        # Thu thập mức độ thỏa mãn cho mỗi điều kiện
        antecedent_satisfactions = []
        
        for symptom_id in rule.antecedents:
            if symptom_id not in self.patient_facts:
                # Nếu không có sự kiện, mức độ thỏa mãn = 0
                antecedent_satisfactions.append(0.0)
                continue
            
            fact = self.patient_facts[symptom_id]
            symptom = self.kb.get_symptom(symptom_id)
            
            if symptom and symptom.is_measurable:
                # Đối với các giá trị đo được, sử dụng fuzzy membership
                # Tính membership trong tập mờ "normal" hoặc "expected"
                if isinstance(fact.value, (int, float)):
                    # Tính độ thành viên dựa trên giá trị
                    memberships = self.fuzzifier.evaluate_clinical_value(symptom_id, fact.value)
                    # Lấy giá trị membership cao nhất
                    satisfaction = max(memberships.values()) if memberships else 0.0
                else:
                    # Cho các giá trị không số, sử dụng certainty trực tiếp
                    satisfaction = fact.certainty
            else:
                # Cho các triệu chứng không đo được, sử dụng certainty
                satisfaction = fact.certainty
            
            # Áp dụng trọng số của certainty_level
            if fact.confidence_level == "high":
                weight = 1.0
            elif fact.confidence_level == "medium":
                weight = 0.7
            else:  # low
                weight = 0.4
            
            satisfaction *= weight
            
            # ✅ GIẢI PHÁP 3: Áp dụng symptom importance weight
            symptom_weight = self.SYMPTOM_WEIGHTS.get(symptom_id, 1.0)
            satisfaction *= symptom_weight
            
            antecedent_satisfactions.append(satisfaction)
        
        # Tính toán mức độ thỏa mãn tổng thể (AND logic)
        if not antecedent_satisfactions:
            return 0.0
        
        # ✅ GIẢI PHÁP 3: Sử dụng weighted average thay vì t-norm (minimum)
        # Điều này làm tăng mức độ thỏa mãn khi có các triệu chứng quan trọng
        # weighted_and = sum(satisfactions) / len(satisfactions)
        # Nhưng vẫn sử dụng min vì nó phù hợp hơn với logic AND
        min_satisfaction = min(antecedent_satisfactions)
        
        # Áp dụng trọng số quy tắc
        final_confidence = min_satisfaction * rule.confidence * rule.weight
        
        return min(final_confidence, 1.0)
    
    def _calculate_disease_confidence(self, disease_id: str) -> Tuple[float, List[str]]:
        """
        Tính toán độ tin cậy chẩn đoán cho một bệnh
        
        ✅ GIẢI PHÁP 1: Sử dụng MAX thay vì AVERAGE
        ✅ GIẢI PHÁP 4: Thêm PREVALENCE FACTOR
        
        Công thức cải thiện:
        confidence = 0.5 × max_rule_score + 0.35 × coverage + 0.15 × prevalence
        
        Returns:
            (confidence, matching_symptoms_list)
        """
        applicable_rules = self.kb.get_applicable_rules(disease_id)
        
        if not applicable_rules:
            return 0.0, []
        
        # Tính độ tin cậy cho mỗi quy tắc
        rule_confidences = []
        matching_symptoms = set()
        
        for rule in applicable_rules:
            confidence = self._evaluate_rule_fuzzy(rule)
            rule_confidences.append(confidence)
            
            # Thu thập các triệu chứng phù hợp
            for symptom_id in rule.antecedents:
                if symptom_id in self.patient_facts:
                    matching_symptoms.add(symptom_id)
        
        # ✅ GIẢI PHÁP 1: Sử dụng MAX thay vì AVERAGE
        # Bệnh được match tốt nhất sẽ có score cao hơn
        if rule_confidences:
            max_rule_confidence = max(rule_confidences)
            avg_rule_confidence = sum(rule_confidences) / len(rule_confidences)
            # Lấy average của max và trung bình để có thể catch các quy tắc partial
            blended_rule_score = 0.7 * max_rule_confidence + 0.3 * avg_rule_confidence
        else:
            blended_rule_score = 0.0
        
        # Tính toán symptom coverage
        # Có bao nhiêu triệu chứng trong tất cả quy tắc được bệnh nhân cung cấp
        all_rule_symptoms = set()
        for rule in applicable_rules:
            all_rule_symptoms.update(rule.antecedents)
        
        symptom_coverage = len(matching_symptoms) / len(all_rule_symptoms) if all_rule_symptoms else 0.0
        
        # ✅ GIẢI PHÁP 4: Thêm PREVALENCE FACTOR
        # Bệnh phổ biến hơn được ưu tiên (nhưng không quá nhiều)
        disease = self.kb.get_disease(disease_id)
        prevalence_factor = 1.0
        if disease:
            # Normalize prevalence (0.15 = baseline, nếu cao hơn thì có weight)
            prevalence_factor = min(disease.prevalence / 0.15, 1.8)  # Cap max 1.8
        
        # ✅ GIẢI PHÁP 1: Công thức cải thiện với trọng số tốt hơn
        # Symptom coverage quan trọng hơn prevalence
        final_confidence = (
            0.5 * blended_rule_score +       # Quy tắc match (50%)
            0.4 * symptom_coverage +         # Độ phủ triệu chứng (40%) - tăng từ 35%
            0.1 * prevalence_factor          # Tỷ lệ mắc bệnh (10%) - giảm từ 15%
        )
        
        return min(final_confidence, 1.0), list(matching_symptoms)
    
    def diagnose(self, include_threshold: float = 0.15) -> List[DiagnosisResult]:
        """
        Thực hiện suy luận và chẩn đoán bệnh
        
        ✅ GIẢI PHÁP 1, 2, 3, 4: Tất cả cải tiến được áp dụng tại đây
        
        Args:
            include_threshold: Ngưỡng độ tin cậy tối thiểu để đưa vào kết quả
                             (default: 0.15 thay vì 0.3 để có được kết quả có ý nghĩa)
        
        Returns:
            Danh sách kết quả chẩn đoán (sắp xếp theo độ tin cậy giảm dần)
        """
        self.explanation_trace.append("\n=== BẮT ĐẦU SỰ SUYLUẬN ===")
        
        diagnosis_results: Dict[str, DiagnosisResult] = {}
        
        # Đánh giá mỗi bệnh
        for disease_id, disease in self.kb.diseases.items():
            confidence, matching_symptoms = self._calculate_disease_confidence(disease_id)
            
            if confidence >= include_threshold:
                result = DiagnosisResult(
                    disease_id=disease_id,
                    disease_name=disease.name,
                    confidence=confidence,
                    severity=disease.severity.name,
                    matching_symptoms=matching_symptoms
                )
                
                # Tạo lý do chẩn đoán
                result.reasoning = self._generate_reasoning(disease_id, matching_symptoms)
                
                # Đưa ra khuyến nghị
                result.recommended_actions = self._get_recommendations(disease)
                
                diagnosis_results[disease_id] = result
                
                self.explanation_trace.append(
                    f"Bệnh: {disease.name} - Độ tin cậy: {confidence:.2%}"
                )
        
        # Sắp xếp theo độ tin cậy
        sorted_results = sorted(
            diagnosis_results.values(),
            key=lambda x: x.confidence,
            reverse=True
        )
        
        self.explanation_trace.append(f"\n=== KẾT QUẢ: {len(sorted_results)} bệnh được chẩn đoán ===")
        
        return sorted_results
    
    def _generate_reasoning(self, disease_id: str, matching_symptoms: List[str]) -> List[str]:
        """Tạo lý do chẩn đoán"""
        reasoning = []
        disease = self.kb.get_disease(disease_id)
        
        if disease:
            reasoning.append(f"Dựa trên bệnh: {disease.description}")
        
        reasoning.append(f"Triệu chứng phù hợp được xác định: {len(matching_symptoms)}")
        
        for symptom_id in matching_symptoms[:3]:  # Lấy 3 triệu chứng chính
            symptom = self.kb.get_symptom(symptom_id)
            if symptom:
                fact = self.patient_facts.get(symptom_id)
                if fact:
                    reasoning.append(f"  • {symptom.name} (Giá trị: {fact.value})")
        
        return reasoning
    
    def _get_recommendations(self, disease) -> List[str]:
        """Đưa ra khuyến nghị xử lý"""
        recommendations = []
        
        if disease.severity.value == 4:  # CRITICAL
            recommendations.append("🚨 NGUY HIỂM: Yêu cầu cấp cứu ngay lập tức")
        elif disease.severity.value == 3:  # SEVERE
            recommendations.append("⚠️  NẶNG: Liên hệ bác sĩ chuyên khoa ngay")
        elif disease.severity.value == 2:  # MODERATE
            recommendations.append("📋 ĐỘ NẶNG TRUNG BÌNH: Tham khảo bác sĩ trong 24 giờ")
        else:  # MILD
            recommendations.append("ℹ️  ĐỘ NẶNG NHẸ: Theo dõi các triệu chứng")
        
        recommendations.append("Tránh bỏ lỡ các triệu chứng mới hoặc xấu đi")
        recommendations.append("Uống đủ nước và nghỉ ngơi")
        
        return recommendations
    
    def get_explanation_trace(self) -> str:
        """Lấy chi tiết quá trình suy luận"""
        return "\n".join(self.explanation_trace)
    
    def debug_rule_evaluation(self, disease_id: str) -> Dict:
        """
        Debug: Hiển thị chi tiết đánh giá các quy tắc cho một bệnh
        """
        debug_info = {
            "disease_id": disease_id,
            "disease_name": self.kb.get_disease(disease_id).name if self.kb.get_disease(disease_id) else "Unknown",
            "rules": []
        }
        
        applicable_rules = self.kb.get_applicable_rules(disease_id)
        
        for rule in applicable_rules:
            rule_info = {
                "rule_id": rule.id,
                "antecedents": rule.antecedents,
                "confidence": rule.confidence,
                "weight": rule.weight,
                "antecedent_details": {}
            }
            
            for symptom_id in rule.antecedents:
                if symptom_id in self.patient_facts:
                    fact = self.patient_facts[symptom_id]
                    rule_info["antecedent_details"][symptom_id] = {
                        "value": fact.value,
                        "certainty": fact.certainty,
                        "confidence_level": fact.confidence_level
                    }
                else:
                    rule_info["antecedent_details"][symptom_id] = "NOT PROVIDED"
            
            rule_score = self._evaluate_rule_fuzzy(rule)
            rule_info["evaluated_confidence"] = rule_score
            
            debug_info["rules"].append(rule_info)
        
        return debug_info
