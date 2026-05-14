"""
Debug Script - Xác định vấn đề
"""

from knowledge_base import KnowledgeBase
from fuzzy_system import FuzzyLogic
from inference_engine import InferenceEngine, PatientFact

kb = KnowledgeBase()
fuzzy_logic = FuzzyLogic()
engine = InferenceEngine(kb, fuzzy_logic)

print("=" * 80)
print("🔧 DEBUG: Kiểm tra logic tính toán")
print("=" * 80)

# Test case đơn giản
engine.clear_patient_facts()

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

# Debug riêng từng bệnh
print("\n📋 Kiểm tra từng bệnh:")

for disease_id, disease in kb.diseases.items():
    print(f"\n🔹 Bệnh: {disease.name} (id={disease_id})")
    
    applicable_rules = kb.get_applicable_rules(disease_id)
    print(f"   Số quy tắc: {len(applicable_rules)}")
    
    if applicable_rules:
        for rule in applicable_rules:
            print(f"\n   Quy tắc: {rule.id}")
            print(f"     Antecedents: {rule.antecedents}")
            print(f"     Weight: {rule.weight}")
            
            # Debug quy tắc này
            rule_score = engine._evaluate_rule_fuzzy(rule)
            print(f"     Rule score: {rule_score:.4f}")
    
    # Tính confidence
    confidence, symptoms = engine._calculate_disease_confidence(disease_id)
    print(f"\n   ✅ Confidence: {confidence:.4f} ({confidence:.1%})")
    print(f"   Matching symptoms: {symptoms}")

print("\n" + "=" * 80)
