"""
Module kiểm thử và xác thực hệ chuyên gia
"""

import unittest
from knowledge_base import KnowledgeBase, Disease, Symptom, Rule, Severity
from fuzzy_system import FuzzyLogic, MembershipFunction, FuzzySet
from inference_engine import InferenceEngine, PatientFact


class TestFuzzySystem(unittest.TestCase):
    """Kiểm thử hệ thống Fuzzy Logic"""
    
    def setUp(self):
        self.fuzzy = FuzzyLogic()
    
    def test_triangular_membership(self):
        """Kiểm thử hàm thành viên tam giác"""
        # Kiểm thử điểm dưới
        self.assertEqual(self.fuzzy.triangular_membership(35, 35, 37, 39), 0.0)
        # Kiểm thử điểm trên
        self.assertEqual(self.fuzzy.triangular_membership(39, 35, 37, 39), 0.0)
        # Kiểm thử đỉnh
        self.assertEqual(self.fuzzy.triangular_membership(37, 35, 37, 39), 1.0)
        # Kiểm thử giữa
        self.assertGreater(self.fuzzy.triangular_membership(36, 35, 37, 39), 0.0)
        self.assertLess(self.fuzzy.triangular_membership(36, 35, 37, 39), 1.0)
    
    def test_trapezoidal_membership(self):
        """Kiểm thử hàm thành viên hình thang"""
        # Kiểm thử vùng cao
        self.assertEqual(self.fuzzy.trapezoidal_membership(50, 40, 45, 55, 60), 1.0)
    
    def test_gaussian_membership(self):
        """Kiểm thử hàm thành viên Gaussian"""
        # Tại trung bình phải bằng 1
        self.assertAlmostEqual(self.fuzzy.gaussian_membership(37, 37, 1), 1.0)
    
    def test_fuzzy_operators(self):
        """Kiểm thử các toán tử mờ"""
        # AND
        self.assertEqual(FuzzyLogic.and_operator([0.8, 0.6, 0.9]), 0.6)
        # OR
        self.assertEqual(FuzzyLogic.or_operator([0.8, 0.6, 0.9]), 0.9)
        # NOT
        self.assertAlmostEqual(FuzzyLogic.not_operator(0.7), 0.3)
    
    def test_membership_initialization(self):
        """Kiểm thử khởi tạo các hàm thành viên"""
        self.assertIn('temperature', self.fuzzy.fuzzy_sets)
        self.assertIn('low', self.fuzzy.fuzzy_sets['temperature'])
        self.assertIn('normal', self.fuzzy.fuzzy_sets['temperature'])
        self.assertIn('high', self.fuzzy.fuzzy_sets['temperature'])


class TestKnowledgeBase(unittest.TestCase):
    """Kiểm thử cơ sở tri thức"""
    
    def setUp(self):
        self.kb = KnowledgeBase()
    
    def test_symptoms_added(self):
        """Kiểm thử các triệu chứng được thêm"""
        self.assertGreater(len(self.kb.symptoms), 0)
        self.assertIn('fever', self.kb.symptoms)
        self.assertIn('cough', self.kb.symptoms)
    
    def test_diseases_added(self):
        """Kiểm thử các bệnh được thêm"""
        self.assertGreater(len(self.kb.diseases), 0)
        self.assertIn('flu', self.kb.diseases)
        self.assertIn('pneumonia', self.kb.diseases)
    
    def test_rules_added(self):
        """Kiểm thử các quy tắc được thêm"""
        self.assertGreater(len(self.kb.rules), 0)
    
    def test_symptom_disease_mapping(self):
        """Kiểm thử ánh xạ triệu chứng-bệnh"""
        # Sốt cao liên quan đến cảm cúm
        diseases_for_fever = self.kb.get_diseases_for_symptom('fever')
        self.assertIn('flu', diseases_for_fever)
        
        # Cảm cúm có liên quan đến sốt cao
        symptoms_for_flu = self.kb.get_symptoms_for_disease('flu')
        self.assertIn('fever', symptoms_for_flu)
    
    def test_knowledge_base_validation(self):
        """Kiểm thử xác thực cơ sở tri thức"""
        validation = self.kb.validate_knowledge_base()
        self.assertEqual(validation['validation_status'], 'OK')
        self.assertEqual(len(validation['consistency_issues']), 0)
    
    def test_get_symptom(self):
        """Kiểm thử lấy triệu chứng"""
        symptom = self.kb.get_symptom('fever')
        self.assertIsNotNone(symptom)
        self.assertEqual(symptom.name, 'Sốt cao')
    
    def test_get_disease(self):
        """Kiểm thử lấy bệnh"""
        disease = self.kb.get_disease('flu')
        self.assertIsNotNone(disease)
        self.assertEqual(disease.name, 'Cảm cúm')


class TestInferenceEngine(unittest.TestCase):
    """Kiểm thử engine suyluận"""
    
    def setUp(self):
        self.kb = KnowledgeBase()
        self.fuzzy = FuzzyLogic()
        self.engine = InferenceEngine(self.kb, self.fuzzy)
    
    def test_add_patient_fact(self):
        """Kiểm thử thêm sự kiện bệnh nhân"""
        fact = PatientFact(
            symptom_id='fever',
            value=39.5,
            certainty=1.0,
            confidence_level='high'
        )
        self.engine.add_patient_fact(fact)
        self.assertIn('fever', self.engine.patient_facts)
        self.assertEqual(self.engine.patient_facts['fever'].value, 39.5)
    
    def test_clear_patient_facts(self):
        """Kiểm thử xóa sự kiện bệnh nhân"""
        fact = PatientFact(
            symptom_id='fever',
            value=39.5,
            certainty=1.0
        )
        self.engine.add_patient_fact(fact)
        self.engine.clear_patient_facts()
        self.assertEqual(len(self.engine.patient_facts), 0)
    
    def test_flu_diagnosis(self):
        """Kiểm thử chẩn đoán cảm cúm"""
        # Thêm triệu chứng của cảm cúm
        self.engine.add_patient_fact(PatientFact(
            symptom_id='fever', value=39.5, certainty=1.0, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='cough', value='có', certainty=0.9, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='sore_throat', value='có', certainty=0.85, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='fatigue', value='có', certainty=0.9, confidence_level='high'
        ))
        
        results = self.engine.diagnose(include_threshold=0.5)
        
        # Kiểm thử kết quả
        self.assertGreater(len(results), 0)
        
        # Cảm cúm phải là kết quả hàng đầu
        flu_result = next((r for r in results if r.disease_id == 'flu'), None)
        self.assertIsNotNone(flu_result)
        self.assertGreater(flu_result.confidence, 0.5)
    
    def test_pneumonia_diagnosis(self):
        """Kiểm thử chẩn đoán viêm phổi"""
        # Thêm triệu chứng của viêm phổi
        self.engine.add_patient_fact(PatientFact(
            symptom_id='fever', value=39.0, certainty=1.0, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='cough', value='liên tục', certainty=0.95, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='shortness_breath', value='có', certainty=0.9, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='chest_pain', value='có', certainty=0.85, confidence_level='high'
        ))
        
        results = self.engine.diagnose(include_threshold=0.4)
        
        self.assertGreater(len(results), 0)
        
        # Viêm phổi phải là kết quả hàng đầu
        pneumonia_result = next((r for r in results if r.disease_id == 'pneumonia'), None)
        self.assertIsNotNone(pneumonia_result)
        self.assertGreater(pneumonia_result.confidence, 0.4)
    
    def test_gastroenteritis_diagnosis(self):
        """Kiểm thử chẩn đoán viêm dạ dày ruột"""
        self.engine.add_patient_fact(PatientFact(
            symptom_id='nausea', value='có', certainty=0.95, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='vomiting', value='có', certainty=0.9, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='diarrhea', value='có', certainty=0.95, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='abdominal_pain', value='có', certainty=0.85, confidence_level='high'
        ))
        
        results = self.engine.diagnose(include_threshold=0.4)
        
        self.assertGreater(len(results), 0)
        
        gastro_result = next((r for r in results if r.disease_id == 'gastroenteritis'), None)
        self.assertIsNotNone(gastro_result)
        self.assertGreater(gastro_result.confidence, 0.5)
    
    def test_no_diagnosis_with_unrelated_symptoms(self):
        """Kiểm thử không chẩn đoán với triệu chứng không liên quan"""
        # Thêm triệu chứng không liên quan
        self.engine.add_patient_fact(PatientFact(
            symptom_id='runny_nose', value='có', certainty=0.5, confidence_level='low'
        ))
        
        results = self.engine.diagnose(include_threshold=0.5)
        
        # Không có kết quả hoặc độ tin cậy thấp
        self.assertTrue(len(results) == 0 or all(r.confidence < 0.5 for r in results))
    
    def test_diagnosis_confidence_scores(self):
        """Kiểm thử rằng các kết quả sắp xếp theo độ tin cậy"""
        self.engine.add_patient_fact(PatientFact(
            symptom_id='fever', value=39.5, certainty=1.0, confidence_level='high'
        ))
        self.engine.add_patient_fact(PatientFact(
            symptom_id='cough', value='có', certainty=0.9, confidence_level='high'
        ))
        
        results = self.engine.diagnose()
        
        # Kết quả sắp xếp giảm dần
        for i in range(len(results) - 1):
            self.assertGreaterEqual(results[i].confidence, results[i + 1].confidence)


def run_tests(verbosity=2):
    """Chạy tất cả các bài kiểm thử"""
    # Tạo bộ kiểm thử
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Thêm các bài kiểm thử
    suite.addTests(loader.loadTestsFromTestCase(TestFuzzySystem))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeBase))
    suite.addTests(loader.loadTestsFromTestCase(TestInferenceEngine))
    
    # Chạy kiểm thử
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("=" * 70)
    print("🧪 KIỂM THỬ HỆ CHUYÊN GIA CHUẨN ĐOÁN BỆNH")
    print("=" * 70)
    result = run_tests()
    
    print("\n" + "=" * 70)
    print("📊 KẾT QUẢ KIỂM THỬ")
    print("=" * 70)
    print(f"Tổng số bài kiểm thử: {result.testsRun}")
    print(f"Thành công: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Thất bại: {len(result.failures)}")
    print(f"Lỗi: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ Tất cả bài kiểm thử thành công!")
    else:
        print("\n❌ Một số bài kiểm thử thất bại!")
