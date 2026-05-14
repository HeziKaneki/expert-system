"""
Knowledge Base cho Hệ Chuyên Gia Chuẩn Đoán Bệnh
Chứa các quy tắc y khoa, triệu chứng, bệnh, và mối liên hệ
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from enum import Enum


class Severity(Enum):
    """Mức độ nghiêm trọng"""
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    CRITICAL = 4


@dataclass
class Symptom:
    """Triệu chứng lâm sàng"""
    id: str
    name: str
    description: str
    typical_values: Dict[str, float] = field(default_factory=dict)  # Giá trị điển hình
    measurement_unit: str = ""
    is_measurable: bool = False  # True nếu là chỉ số đo được (nhiệt độ, huyết áp)
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class Disease:
    """Bệnh"""
    id: str
    name: str
    description: str
    severity: Severity
    icd10_code: str = ""
    prevalence: float = 0.0  # Tỷ lệ mắc bệnh
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class Rule:
    """Quy tắc y khoa (IF-THEN)"""
    id: str
    antecedents: List[str]  # Điều kiện (symptom IDs)
    consequent: str  # Kết luận (disease ID)
    confidence: float  # Độ tin cậy [0, 1]
    weight: float = 1.0  # Trọng số của quy tắc
    source: str = "clinical_evidence"  # Nguồn bằng chứng
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class DiagnosticRule:
    """Quy tắc chẩn đoán phức tạp"""
    id: str
    name: str
    description: str
    symptoms: Dict[str, float]  # {symptom_id -> importance_weight}
    disease: str  # disease_id
    minimum_confidence: float = 0.3
    threshold: float = 0.5  # Ngưỡng tổng hợp để chẩn đoán
    logic: str = "and"  # "and" hoặc "or"


class KnowledgeBase:
    """Cơ sở tri thức cho hệ chuyên gia"""
    
    def __init__(self):
        self.symptoms: Dict[str, Symptom] = {}
        self.diseases: Dict[str, Disease] = {}
        self.rules: Dict[str, Rule] = {}
        self.diagnostic_rules: Dict[str, DiagnosticRule] = {}
        self.symptom_disease_map: Dict[str, Set[str]] = {}  # symptom_id -> set(disease_ids)
        self.disease_symptom_map: Dict[str, Set[str]] = {}  # disease_id -> set(symptom_ids)
        
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Khởi tạo cơ sở tri thức với dữ liệu y khoa"""
        
        # ============= TRIỆU CHỨNG =============
        
        # Triệu chứng chung
        self.add_symptom(Symptom(
            id="fever",
            name="Sốt cao",
            description="Nhiệt độ cơ thể tăng cao",
            typical_values={"high": 38.5, "very_high": 39.5},
            measurement_unit="°C",
            is_measurable=True
        ))
        
        self.add_symptom(Symptom(
            id="cough",
            name="Ho",
            description="Ho kéo dài hoặc ho tái phát",
            typical_values={"frequency": "multiple times per day"}
        ))
        
        self.add_symptom(Symptom(
            id="sore_throat",
            name="Đau họng",
            description="Đau và khó chịu ở cổ họng",
            typical_values={"severity": "moderate"}
        ))
        
        self.add_symptom(Symptom(
            id="runny_nose",
            name="Chảy nước mũi",
            description="Dịch mũi chảy liên tục",
            typical_values={"amount": "moderate to heavy"}
        ))
        
        self.add_symptom(Symptom(
            id="headache",
            name="Đau đầu",
            description="Đau ở vùng đầu",
            typical_values={"severity": "moderate"}
        ))
        
        self.add_symptom(Symptom(
            id="fatigue",
            name="Mệt mỏi",
            description="Cảm giác mệt mỏi, thiếu sức lực",
            typical_values={"duration": "sustained"}
        ))
        
        self.add_symptom(Symptom(
            id="body_aches",
            name="Đau cơ thể",
            description="Đau cơ và xương",
            typical_values={"severity": "moderate to severe"}
        ))
        
        self.add_symptom(Symptom(
            id="shortness_breath",
            name="Khó thở",
            description="Khó khăn trong hô hấp",
            typical_values={"severity": "variable"}
        ))
        
        # Triệu chứng đường tiêu hóa
        self.add_symptom(Symptom(
            id="nausea",
            name="Buồn nôn",
            description="Cảm giác muốn nôn",
            typical_values={}
        ))
        
        self.add_symptom(Symptom(
            id="vomiting",
            name="Nôn",
            description="Nôn mửa",
            typical_values={"frequency": "multiple episodes"}
        ))
        
        self.add_symptom(Symptom(
            id="diarrhea",
            name="Tiêu chảy",
            description="Phân lỏng, tiêu chảy",
            typical_values={"frequency": "3+ times daily"}
        ))
        
        self.add_symptom(Symptom(
            id="abdominal_pain",
            name="Đau bụng",
            description="Đau ở vùng bụng",
            typical_values={"severity": "mild to moderate"}
        ))
        
        # Các chỉ số lâm sàng
        self.add_symptom(Symptom(
            id="high_blood_pressure",
            name="Huyết áp cao",
            description="Huyết áp cao",
            typical_values={"systolic": 150},
            measurement_unit="mmHg",
            is_measurable=True
        ))
        
        self.add_symptom(Symptom(
            id="low_blood_pressure",
            name="Huyết áp thấp",
            description="Huyết áp thấp",
            typical_values={"systolic": 90},
            measurement_unit="mmHg",
            is_measurable=True
        ))
        
        self.add_symptom(Symptom(
            id="high_heart_rate",
            name="Nhịp tim nhanh",
            description="Nhịp tim vượt quá 100 lần/phút",
            typical_values={"rate": 110},
            measurement_unit="nhịp/phút",
            is_measurable=True
        ))
        
        self.add_symptom(Symptom(
            id="chest_pain",
            name="Đau ngực",
            description="Đau tại vùng ngực",
            typical_values={"severity": "moderate to severe"}
        ))
        
        # Triệu chứng hô hấp bổ sung
        self.add_symptom(Symptom(
            id="wheezing",
            name="Ran rào khi thở",
            description="Âm thanh kêu khò khè khi thở",
            typical_values={"frequency": "intermittent or constant"}
        ))
        
        self.add_symptom(Symptom(
            id="sputum_production",
            name="Ho có đờm",
            description="Ho kèm theo đờm hoặc chất nhầy",
            typical_values={"color": "clear to yellowish"}
        ))
        
        self.add_symptom(Symptom(
            id="hoarseness",
            name="Khàn tiếng",
            description="Giọng nói thay đổi, khàn",
            typical_values={"severity": "mild to moderate"}
        ))
        
        self.add_symptom(Symptom(
            id="sinus_pressure",
            name="Ứ đặc xoang mũi",
            description="Cảm giác áp lực ở vùng xoang mũi",
            typical_values={"location": "face"}
        ))
        
        self.add_symptom(Symptom(
            id="sneezing",
            name="Hắt xì",
            description="Hắt xì liên tục",
            typical_values={"frequency": "multiple times"}
        ))
        
        self.add_symptom(Symptom(
            id="cough_with_blood",
            name="Ho ra máu",
            description="Ho có máu hoặc máu trong đờm",
            typical_values={"severity": "severe"}
        ))
        
        # Triệu chứng tim mạch bổ sung
        self.add_symptom(Symptom(
            id="syncope",
            name="Ngất xỉu",
            description="Mất ý thức tạm thời",
            typical_values={"severity": "severe"}
        ))
        
        self.add_symptom(Symptom(
            id="irregular_heartbeat",
            name="Nhịp tim không đều",
            description="Nhịp tim bất thường, rối loạn nhịp",
            typical_values={"severity": "variable"},
            is_measurable=True
        ))
        
        # Triệu chứng tiêu hóa bổ sung
        self.add_symptom(Symptom(
            id="acid_reflux",
            name="Trào ngược axit",
            description="Axit từ dạ dày trào ngược lên thực quản",
            typical_values={"frequency": "multiple times daily"}
        ))
        
        self.add_symptom(Symptom(
            id="bloody_stool",
            name="Phân có máu",
            description="Phân có máu hoặc máu tươi",
            typical_values={"severity": "moderate to severe"}
        ))
        
        self.add_symptom(Symptom(
            id="constipation",
            name="Táo bón",
            description="Khó đi ngoài, phân khô",
            typical_values={"frequency": "reduced bowel movements"}
        ))
        
        # Triệu chứng chung bổ sung
        self.add_symptom(Symptom(
            id="rash",
            name="Phát ban",
            description="Phát ban hoặc nổi mẩn trên da",
            typical_values={"location": "generalized or localized"}
        ))
        
        self.add_symptom(Symptom(
            id="sweating",
            name="Hôi ra mồ hôi",
            description="Tiết mồ hôi nhiều, đặc biệt đêm",
            typical_values={"intensity": "profuse"}
        ))
        
        self.add_symptom(Symptom(
            id="weakness",
            name="Yếu đuối",
            description="Cảm giác yếu, mất sức",
            typical_values={"severity": "variable"}
        ))
        
        # 15 triệu chứng mới (31-45)
        self.add_symptom(Symptom(
            id="chills",
            name="Run lạnh",
            description="Cảm giác lạnh run, rùng mình",
            typical_values={"intensity": "moderate to severe"}
        ))
        
        self.add_symptom(Symptom(
            id="muscle_pain",
            name="Đau cơ",
            description="Đau cơ cơ thể",
            typical_values={"location": "generalized"}
        ))
        
        self.add_symptom(Symptom(
            id="joint_pain",
            name="Đau khớp",
            description="Đau ở các khớp",
            typical_values={"location": "multiple joints"}
        ))
        
        self.add_symptom(Symptom(
            id="loss_of_appetite",
            name="Mất cảm giác ăn",
            description="Không muốn ăn, mất cảm giác ngon miệng",
            typical_values={"severity": "moderate"}
        ))
        
        self.add_symptom(Symptom(
            id="dizziness",
            name="Chóng mặt",
            description="Cảm giác quay cuồng, mất thăng bằng",
            typical_values={"severity": "variable"}
        ))
        
        self.add_symptom(Symptom(
            id="low_oxygen",
            name="Nồng độ oxy thấp",
            description="SpO2 < 95%, hơi không đủ oxy",
            typical_values={"level": 92},
            measurement_unit="%",
            is_measurable=True
        ))
        
        self.add_symptom(Symptom(
            id="yellow_skin",
            name="Da vàng",
            description="Da và tròng mắt chuyển màu vàng",
            typical_values={"severity": "moderate"}
        ))
        
        self.add_symptom(Symptom(
            id="itching",
            name="Ngứa",
            description="Cảm giác ngứa trên da",
            typical_values={"intensity": "mild to severe"}
        ))
        
        self.add_symptom(Symptom(
            id="swollen_lymph",
            name="Hạch sưng",
            description="Hạch bạch huyết sưng phù",
            typical_values={"location": "neck, underarm, groin"}
        ))
        
        self.add_symptom(Symptom(
            id="sore_eyes",
            name="Mắt sưng",
            description="Mắt đỏ, sưng, chảy nước",
            typical_values={"severity": "mild to moderate"}
        ))
        
        self.add_symptom(Symptom(
            id="nasal_congestion",
            name="Nghẹt mũi",
            description="Mũi bị tắc, khó thở qua mũi",
            typical_values={"severity": "moderate"}
        ))
        
        self.add_symptom(Symptom(
            id="ear_pain",
            name="Đau tai",
            description="Đau ở tai hoặc vùng xung quanh",
            typical_values={"severity": "mild to severe"}
        ))
        
        self.add_symptom(Symptom(
            id="back_pain",
            name="Đau lưng",
            description="Đau vùng lưng dưới hoặc trên",
            typical_values={"location": "lower or upper back"}
        ))
        
        self.add_symptom(Symptom(
            id="neck_stiffness",
            name="Cứng cổ",
            description="Cúp cổ, khó xoay đầu",
            typical_values={"severity": "moderate"}
        ))
        
        self.add_symptom(Symptom(
            id="tremor",
            name="Run tay chân",
            description="Run tay hoặc chân không kiểm soát được",
            typical_values={"intensity": "mild to severe"}
        ))
        
        # ============= BỆNH =============
        
        self.add_disease(Disease(
            id="flu",
            name="Cảm cúm",
            description="Bệnh cúm do virus gây ra",
            severity=Severity.MODERATE,
            icd10_code="J09-J11",
            prevalence=0.15
        ))
        
        self.add_disease(Disease(
            id="common_cold",
            name="Cảm lạnh",
            description="Bệnh cảm lạnh thông thường",
            severity=Severity.MILD,
            icd10_code="J00",
            prevalence=0.2
        ))
        
        self.add_disease(Disease(
            id="bronchitis",
            name="Viêm phế quản",
            description="Viêm phế quản cấp hoặc mãn tính",
            severity=Severity.MODERATE,
            icd10_code="J20-J22",
            prevalence=0.05
        ))
        
        self.add_disease(Disease(
            id="pneumonia",
            name="Viêm phổi",
            description="Viêm phổi cộng đồng",
            severity=Severity.SEVERE,
            icd10_code="J13-J18",
            prevalence=0.02
        ))
        
        self.add_disease(Disease(
            id="gastroenteritis",
            name="Viêm dạ dày ruột",
            description="Viêm đường tiêu hóa",
            severity=Severity.MODERATE,
            icd10_code="A09",
            prevalence=0.03
        ))
        
        self.add_disease(Disease(
            id="hypertension",
            name="Cao huyết áp",
            description="Tăng huyết áp",
            severity=Severity.MODERATE,
            icd10_code="I10-I15",
            prevalence=0.25
        ))
        
        self.add_disease(Disease(
            id="heart_disease",
            name="Bệnh tim mạch",
            description="Bệnh tim mạch",
            severity=Severity.SEVERE,
            icd10_code="I20-I52",
            prevalence=0.05
        ))
        
        # Thêm 13 bệnh mới
        
        # Bệnh hô hấp
        self.add_disease(Disease(
            id="asthma",
            name="Hen suyễn",
            description="Bệnh viêm phế quản hen suyễn",
            severity=Severity.MODERATE,
            icd10_code="J45",
            prevalence=0.08
        ))
        
        self.add_disease(Disease(
            id="tuberculosis",
            name="Lao phổi",
            description="Bệnh lao do mycobacterium tuberculosis gây ra",
            severity=Severity.SEVERE,
            icd10_code="A15",
            prevalence=0.002
        ))
        
        self.add_disease(Disease(
            id="whooping_cough",
            name="Ho gà",
            description="Bệnh ho gà do vi khuẩn Bordetella pertussis gây ra",
            severity=Severity.MODERATE,
            icd10_code="A37",
            prevalence=0.001
        ))
        
        self.add_disease(Disease(
            id="laryngitis",
            name="Viêm thanh quản",
            description="Viêm thanh quản cấp tính",
            severity=Severity.MILD,
            icd10_code="J04",
            prevalence=0.04
        ))
        
        self.add_disease(Disease(
            id="sinusitis",
            name="Viêm xoang mũi",
            description="Viêm xoang mũi cấp hoặc mãn tính",
            severity=Severity.MILD,
            icd10_code="J32",
            prevalence=0.10
        ))
        
        # Bệnh tiêu hóa
        self.add_disease(Disease(
            id="appendicitis",
            name="Viêm ruột thừa",
            description="Viêm cấp tính của ruột thừa",
            severity=Severity.SEVERE,
            icd10_code="K35",
            prevalence=0.01
        ))
        
        self.add_disease(Disease(
            id="peptic_ulcer",
            name="Loét dạ dày",
            description="Loét trong dạ dày hoặc tá tràng",
            severity=Severity.MODERATE,
            icd10_code="K25-K28",
            prevalence=0.04
        ))
        
        self.add_disease(Disease(
            id="pancreatitis",
            name="Viêm tụ tuyến",
            description="Viêm cấp tính hoặc mãn tính của tụ tuyến",
            severity=Severity.SEVERE,
            icd10_code="K85",
            prevalence=0.002
        ))
        
        self.add_disease(Disease(
            id="hepatitis",
            name="Viêm gan",
            description="Viêm gan do virus hoặc do ít gây ra",
            severity=Severity.MODERATE,
            icd10_code="B15-B19",
            prevalence=0.01
        ))
        
        # Bệnh tim mạch bổ sung
        self.add_disease(Disease(
            id="stroke",
            name="Đột quỵ",
            description="Đột quỵ não do tắc mạch hoặc chảy máu",
            severity=Severity.CRITICAL,
            icd10_code="I63-I64",
            prevalence=0.003
        ))
        
        self.add_disease(Disease(
            id="arrhythmia",
            name="Rối loạn nhịp tim",
            description="Rối loạn nhịp tim",
            severity=Severity.MODERATE,
            icd10_code="I47-I49",
            prevalence=0.03
        ))
        
        self.add_disease(Disease(
            id="angina",
            name="Đau thắt ngực",
            description="Đau thắt ngực do thiếu máu tim",
            severity=Severity.SEVERE,
            icd10_code="I20",
            prevalence=0.02
        ))
        
        # Bệnh nội tiết
        self.add_disease(Disease(
            id="diabetes",
            name="Bệnh tiểu đường",
            description="Bệnh tiểu đường loại 1 hoặc 2",
            severity=Severity.MODERATE,
            icd10_code="E10-E14",
            prevalence=0.07
        ))
        
        # 10 bệnh mới (21-30)
        self.add_disease(Disease(
            id="sepsis",
            name="Nhiễm khuẩn huyết",
            description="Nhiễm khuẩn toàn thân nguy hiểm",
            severity=Severity.CRITICAL,
            icd10_code="A40-A41",
            prevalence=0.005
        ))
        
        self.add_disease(Disease(
            id="meningitis",
            name="Viêm màng não",
            description="Viêm màng bọc não và tủy sống",
            severity=Severity.CRITICAL,
            icd10_code="G00-G03",
            prevalence=0.001
        ))
        
        self.add_disease(Disease(
            id="influenza_b",
            name="Cúm B",
            description="Cúm do virus influenza B gây ra",
            severity=Severity.MODERATE,
            icd10_code="J10",
            prevalence=0.08
        ))
        
        self.add_disease(Disease(
            id="covid_19",
            name="COVID-19",
            description="Bệnh do virus SARS-CoV-2 gây ra",
            severity=Severity.SEVERE,
            icd10_code="U07.1",
            prevalence=0.01
        ))
        
        self.add_disease(Disease(
            id="allergy",
            name="Dị ứng",
            description="Phản ứng miễn dịch quá mức với tác nhân ngoại",
            severity=Severity.MILD,
            icd10_code="T78",
            prevalence=0.20
        ))
        
        self.add_disease(Disease(
            id="migraine",
            name="Đau nửa đầu",
            description="Đau đầu kiểu nửa thái dương",
            severity=Severity.MODERATE,
            icd10_code="G43",
            prevalence=0.12
        ))
        
        self.add_disease(Disease(
            id="thyroid_disease",
            name="Bệnh tuyến giáp",
            description="Suy giáp hoặc cường giáp",
            severity=Severity.MODERATE,
            icd10_code="E00-E07",
            prevalence=0.05
        ))
        
        self.add_disease(Disease(
            id="kidney_disease",
            name="Bệnh thận",
            description="Bệnh thận mãn tính hoặc cấp tính",
            severity=Severity.SEVERE,
            icd10_code="N17-N19",
            prevalence=0.04
        ))
        
        self.add_disease(Disease(
            id="arthritis",
            name="Viêm khớp",
            description="Viêm các khớp",
            severity=Severity.MODERATE,
            icd10_code="M05-M19",
            prevalence=0.08
        ))
        
        self.add_disease(Disease(
            id="anemia",
            name="Thiếu máu",
            description="Thiếu hồng cầu hoặc hemoglobin",
            severity=Severity.MODERATE,
            icd10_code="D50-D64",
            prevalence=0.15
        ))
        
        # ============= QUY TẮC =============
        # ✅ GIẢI PHÁP 2: Thêm trọng số phân biệt cho quy tắc
        # weight: 1.0 = bình thường, > 1.0 = ưu tiên cao, < 1.0 = ưu tiên thấp
        
        # Cảm cúm (MODERATE - weight = 2.0)
        self.add_rule(Rule(
            id="r_flu_1",
            antecedents=["fever", "cough", "sore_throat", "fatigue"],
            consequent="flu",
            confidence=0.85,
            weight=2.0,  # ✅ WHO guidelines, quy tắc chính xác cao
            source="WHO guidelines"
        ))
        
        self.add_rule(Rule(
            id="r_flu_2",
            antecedents=["fever", "body_aches", "fatigue", "headache"],
            consequent="flu",
            confidence=0.75,
            weight=1.8,  # ✅ Clinical experience, quy tắc phụ
            source="clinical experience"
        ))
        
        # Cảm lạnh (MILD - weight = 1.2)
        self.add_rule(Rule(
            id="r_cold_1",
            antecedents=["runny_nose", "sore_throat", "cough"],
            consequent="common_cold",
            confidence=0.8,
            weight=1.2,  # ✅ Bệnh nhẹ, ưu tiên thấp hơn
            source="CDC guidelines"
        ))
        
        self.add_rule(Rule(
            id="r_cold_2",
            antecedents=["runny_nose", "cough", "headache"],
            consequent="common_cold",
            confidence=0.7,
            weight=1.0,  # ✅ Bằng thường
            source="clinical experience"
        ))
        
        # Viêm phế quản (MODERATE - weight = 1.6)
        self.add_rule(Rule(
            id="r_bronchitis_1",
            antecedents=["cough", "shortness_breath", "fatigue"],
            consequent="bronchitis",
            confidence=0.75,
            weight=1.6,  # ✅ Đỡ nặng hơn cảm cúm
            source="clinical guidelines"
        ))
        
        # Viêm phổi (SEVERE - weight = 3.0)
        self.add_rule(Rule(
            id="r_pneumonia_1",
            antecedents=["fever", "cough", "shortness_breath", "chest_pain"],
            consequent="pneumonia",
            confidence=0.85,
            weight=3.0,  # ✅ NGUY HIỂM - weight cao nhất
            source="medical standards"
        ))
        
        self.add_rule(Rule(
            id="r_pneumonia_2",
            antecedents=["fever", "shortness_breath", "fatigue"],
            consequent="pneumonia",
            confidence=0.65,
            weight=2.5,  # ✅ Quy tắc phụ nhưng vẫn nguy hiểm
            source="clinical experience"
        ))
        
        # Viêm dạ dày ruột (MODERATE - weight = 1.5)
        self.add_rule(Rule(
            id="r_gastro_1",
            antecedents=["nausea", "vomiting", "diarrhea", "abdominal_pain"],
            consequent="gastroenteritis",
            confidence=0.9,
            weight=1.5,  # ✅ Độ tin cậy cao nhưng không nguy hiểm
            source="gastroenterology guidelines"
        ))
        
        # Cao huyết áp (MODERATE - weight = 1.7)
        self.add_rule(Rule(
            id="r_hypertension_1",
            antecedents=["high_blood_pressure", "headache", "fatigue"],
            consequent="hypertension",
            confidence=0.8,
            weight=1.7,  # ✅ Cần lưu ý, nhưng không cấp cứu
            source="cardiology standards"
        ))
        
        # Bệnh tim mạch (SEVERE - weight = 3.0)
        self.add_rule(Rule(
            id="r_heart_1",
            antecedents=["chest_pain", "shortness_breath", "high_heart_rate"],
            consequent="heart_disease",
            confidence=0.85,
            weight=3.0,  # ✅ NGUY HIỂM - weight cao nhất
            source="cardiology guidelines"
        ))
        
        self.add_rule(Rule(
            id="r_heart_2",
            antecedents=["high_blood_pressure", "chest_pain", "fatigue"],
            consequent="heart_disease",
            confidence=0.7,
            weight=2.8,  # ✅ Quy tắc phụ nhưng vẫn nguy hiểm
            source="clinical evidence"
        ))
        
        # 3 Quy tắc mới cho bệnh mới
        
        # Hen suyễn (MODERATE - weight = 1.9)
        self.add_rule(Rule(
            id="r_asthma_1",
            antecedents=["wheezing", "shortness_breath", "cough"],
            consequent="asthma",
            confidence=0.82,
            weight=1.9,  # ✅ Bệnh mãn tính, cần chẩn đoán
            source="pulmonary guidelines"
        ))
        
        # Lao phổi (SEVERE - weight = 3.0)
        self.add_rule(Rule(
            id="r_tuberculosis_1",
            antecedents=["fever", "cough_with_blood", "sweating", "fatigue"],
            consequent="tuberculosis",
            confidence=0.88,
            weight=3.0,  # ✅ NGUY HIỂM - bệnh lây nhiễm
            source="WHO tuberculosis guidelines"
        ))
        
        # Đột quỵ (CRITICAL - weight = 4.0)
        self.add_rule(Rule(
            id="r_stroke_1",
            antecedents=["high_blood_pressure", "syncope", "weakness", "headache"],
            consequent="stroke",
            confidence=0.85,
            weight=4.0,  # ✅ NGUY HIỂM CẤP CỨU - weight cao nhất
            source="neurological emergency protocols"
        ))
        
        # Loét dạ dày (MODERATE - weight = 1.7)
        self.add_rule(Rule(
            id="r_ulcer_1",
            antecedents=["abdominal_pain", "acid_reflux", "nausea"],
            consequent="peptic_ulcer",
            confidence=0.78,
            weight=1.7,
            source="gastroenterology guidelines"
        ))
        
        # Rối loạn nhịp tim (MODERATE - weight = 1.8)
        self.add_rule(Rule(
            id="r_arrhythmia_1",
            antecedents=["irregular_heartbeat", "shortness_breath", "chest_pain"],
            consequent="arrhythmia",
            confidence=0.80,
            weight=1.8,
            source="cardiology standards"
        ))
        
        # Viêm xoang mũi (MILD - weight = 1.3)
        self.add_rule(Rule(
            id="r_sinusitis_1",
            antecedents=["sinus_pressure", "runny_nose", "headache"],
            consequent="sinusitis",
            confidence=0.75,
            weight=1.3,
            source="ENT guidelines"
        ))
        
        # 7 quy tắc mới (18-24)
        
        # Nhiễm khuẩn huyết (CRITICAL - weight = 4.0)
        self.add_rule(Rule(
            id="r_sepsis_1",
            antecedents=["fever", "chills", "weakness", "low_oxygen"],
            consequent="sepsis",
            confidence=0.88,
            weight=4.0,
            source="sepsis clinical protocols"
        ))
        
        # Viêm màng não (CRITICAL - weight = 4.0)
        self.add_rule(Rule(
            id="r_meningitis_1",
            antecedents=["fever", "neck_stiffness", "headache", "syncope"],
            consequent="meningitis",
            confidence=0.85,
            weight=4.0,
            source="neurological emergency"
        ))
        
        # Cúm B (MODERATE - weight = 2.1)
        self.add_rule(Rule(
            id="r_influenza_b_1",
            antecedents=["fever", "cough", "muscle_pain", "fatigue"],
            consequent="influenza_b",
            confidence=0.80,
            weight=2.1,
            source="influenza guidelines"
        ))
        
        # COVID-19 (SEVERE - weight = 3.2)
        self.add_rule(Rule(
            id="r_covid_1",
            antecedents=["fever", "cough", "shortness_breath", "loss_of_appetite"],
            consequent="covid_19",
            confidence=0.82,
            weight=3.2,
            source="COVID-19 protocols"
        ))
        
        # Dị ứng (MILD - weight = 1.4)
        self.add_rule(Rule(
            id="r_allergy_1",
            antecedents=["runny_nose", "sneezing", "itching", "sore_eyes"],
            consequent="allergy",
            confidence=0.78,
            weight=1.4,
            source="immunology guidelines"
        ))
        
        # Bệnh tuyến giáp (MODERATE - weight = 1.6)
        self.add_rule(Rule(
            id="r_thyroid_1",
            antecedents=["fatigue", "weakness", "tremor", "loss_of_appetite"],
            consequent="thyroid_disease",
            confidence=0.76,
            weight=1.6,
            source="endocrinology standards"
        ))
        
        # Thiếu máu (MODERATE - weight = 1.5)
        self.add_rule(Rule(
            id="r_anemia_1",
            antecedents=["fatigue", "weakness", "dizziness", "shortness_breath"],
            consequent="anemia",
            confidence=0.75,
            weight=1.5,
            source="hematology guidelines"
        ))
    
    def add_symptom(self, symptom: Symptom):
        """Thêm triệu chứng vào cơ sở tri thức"""
        self.symptoms[symptom.id] = symptom
    
    def add_disease(self, disease: Disease):
        """Thêm bệnh vào cơ sở tri thức"""
        self.diseases[disease.id] = disease
    
    def add_rule(self, rule: Rule):
        """Thêm quy tắc vào cơ sở tri thức"""
        self.rules[rule.id] = rule
        
        # Cập nhật ánh xạ
        for antecedent in rule.antecedents:
            if antecedent not in self.symptom_disease_map:
                self.symptom_disease_map[antecedent] = set()
            self.symptom_disease_map[antecedent].add(rule.consequent)
        
        if rule.consequent not in self.disease_symptom_map:
            self.disease_symptom_map[rule.consequent] = set()
        for antecedent in rule.antecedents:
            self.disease_symptom_map[rule.consequent].add(antecedent)
    
    def get_symptom(self, symptom_id: str) -> Optional[Symptom]:
        """Lấy triệu chứng theo ID"""
        return self.symptoms.get(symptom_id)
    
    def get_disease(self, disease_id: str) -> Optional[Disease]:
        """Lấy bệnh theo ID"""
        return self.diseases.get(disease_id)
    
    def get_applicable_rules(self, disease_id: str) -> List[Rule]:
        """Lấy tất cả quy tắc áp dụng cho một bệnh"""
        return [rule for rule in self.rules.values() if rule.consequent == disease_id]
    
    def get_diseases_for_symptom(self, symptom_id: str) -> Set[str]:
        """Lấy danh sách bệnh có liên quan đến triệu chứng"""
        return self.symptom_disease_map.get(symptom_id, set())
    
    def get_symptoms_for_disease(self, disease_id: str) -> Set[str]:
        """Lấy danh sách triệu chứng của bệnh"""
        return self.disease_symptom_map.get(disease_id, set())
    
    def validate_knowledge_base(self) -> Dict[str, any]:
        """Xác thực tính nhất quán của cơ sở tri thức"""
        report = {
            "total_symptoms": len(self.symptoms),
            "total_diseases": len(self.diseases),
            "total_rules": len(self.rules),
            "consistency_issues": [],
            "validation_status": "OK"
        }
        
        # Kiểm tra các quy tắc tham chiếu đến triệu chứng/bệnh không tồn tại
        for rule in self.rules.values():
            for symptom_id in rule.antecedents:
                if symptom_id not in self.symptoms:
                    report["consistency_issues"].append(
                        f"Rule {rule.id}: triệu chứng {symptom_id} không tồn tại"
                    )
            
            if rule.consequent not in self.diseases:
                report["consistency_issues"].append(
                    f"Rule {rule.id}: bệnh {rule.consequent} không tồn tại"
                )
        
        if report["consistency_issues"]:
            report["validation_status"] = "WARNING"
        
        return report
