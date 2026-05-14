"""
Module Fuzzy Logic cho Hệ Chuyên Gia Chuẩn Đoán Bệnh
Xử lý logic mờ để đánh giá độ tin cậy của các triệu chứng
"""

import math
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple


class MembershipFunction(Enum):
    """Các hàm thành viên mờ"""
    TRIANGULAR = "triangular"
    TRAPEZOIDAL = "trapezoidal"
    GAUSSIAN = "gaussian"


@dataclass
class FuzzySet:
    """Tập mờ với tên và thông số"""
    name: str
    function_type: MembershipFunction
    params: List[float]  # [a, b, c] cho triangular, [a, b, c, d] cho trapezoidal, [mean, std_dev] cho gaussian


class FuzzyLogic:
    """Hệ thống Fuzzy Logic cho xử lý độ không chắc chắn"""
    
    def __init__(self):
        self.fuzzy_sets: Dict[str, Dict[str, FuzzySet]] = {}
        self._initialize_membership_functions()
    
    def _initialize_membership_functions(self):
        """Khởi tạo các hàm thành viên mờ cho các biến lâm sàng"""
        
        # Nhiệt độ (°C)
        self.fuzzy_sets['temperature'] = {
            'low': FuzzySet('thấp', MembershipFunction.TRIANGULAR, [35, 36.5, 37.5]),
            'normal': FuzzySet('bình thường', MembershipFunction.TRAPEZOIDAL, [36.5, 37, 37.5, 38]),
            'high': FuzzySet('cao', MembershipFunction.GAUSSIAN, [38.5, 1.0])
        }
        
        # Huyết áp tâm thu (mmHg)
        self.fuzzy_sets['systolic_bp'] = {
            'low': FuzzySet('thấp', MembershipFunction.TRIANGULAR, [90, 100, 110]),
            'normal': FuzzySet('bình thường', MembershipFunction.TRAPEZOIDAL, [100, 110, 130, 140]),
            'high': FuzzySet('cao', MembershipFunction.GAUSSIAN, [150, 15])
        }
        
        # Nhịp tim (nhịp/phút)
        self.fuzzy_sets['heart_rate'] = {
            'low': FuzzySet('thấp', MembershipFunction.TRIANGULAR, [40, 50, 60]),
            'normal': FuzzySet('bình thường', MembershipFunction.TRAPEZOIDAL, [50, 60, 80, 100]),
            'high': FuzzySet('cao', MembershipFunction.GAUSSIAN, [110, 15])
        }
        
        # Độ tin cậy chẩn đoán (0-100%)
        self.fuzzy_sets['confidence'] = {
            'low': FuzzySet('thấp', MembershipFunction.TRIANGULAR, [0, 0, 30]),
            'medium': FuzzySet('trung bình', MembershipFunction.TRAPEZOIDAL, [20, 40, 60, 80]),
            'high': FuzzySet('cao', MembershipFunction.TRIANGULAR, [70, 100, 100])
        }
    
    def triangular_membership(self, x: float, a: float, b: float, c: float) -> float:
        """
        Hàm thành viên tam giác
        a: điểm thấp nhất, b: đỉnh, c: điểm cao nhất
        """
        if x <= a or x >= c:
            return 0.0
        elif x <= b:
            return (x - a) / (b - a) if b != a else 0.0
        else:
            return (c - x) / (c - b) if c != b else 0.0
    
    def trapezoidal_membership(self, x: float, a: float, b: float, c: float, d: float) -> float:
        """
        Hàm thành viên hình thang
        a: điểm thấp nhất, b: bắt đầu cao, c: kết thúc cao, d: điểm cao nhất
        """
        if x <= a or x >= d:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 0.0
        elif b < x < c:
            return 1.0
        else:  # c <= x < d
            return (d - x) / (d - c) if d != c else 0.0
    
    def gaussian_membership(self, x: float, mean: float, std_dev: float) -> float:
        """
        Hàm thành viên Gaussian
        mean: trung bình, std_dev: độ lệch chuẩn
        """
        if std_dev == 0:
            return 1.0 if x == mean else 0.0
        return math.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    
    def get_membership_value(self, variable: str, fuzzy_set_name: str, value: float) -> float:
        """
        Tính độ thành viên của một giá trị trong tập mờ
        
        Args:
            variable: tên biến (temperature, heart_rate, ...)
            fuzzy_set_name: tên tập mờ (low, normal, high, ...)
            value: giá trị cần tính
        
        Returns:
            Độ thành viên [0, 1]
        """
        if variable not in self.fuzzy_sets:
            return 0.0
        
        if fuzzy_set_name not in self.fuzzy_sets[variable]:
            return 0.0
        
        fuzzy_set = self.fuzzy_sets[variable][fuzzy_set_name]
        params = fuzzy_set.params
        
        if fuzzy_set.function_type == MembershipFunction.TRIANGULAR:
            return self.triangular_membership(value, params[0], params[1], params[2])
        elif fuzzy_set.function_type == MembershipFunction.TRAPEZOIDAL:
            return self.trapezoidal_membership(value, params[0], params[1], params[2], params[3])
        elif fuzzy_set.function_type == MembershipFunction.GAUSSIAN:
            return self.gaussian_membership(value, params[0], params[1])
        
        return 0.0
    
    def get_all_memberships(self, variable: str, value: float) -> Dict[str, float]:
        """
        Tính độ thành viên của giá trị trong tất cả các tập mờ của biến
        
        Returns:
            Dict[tên_tập_mờ -> độ_thành_viên]
        """
        if variable not in self.fuzzy_sets:
            return {}
        
        memberships = {}
        for fuzzy_set_name in self.fuzzy_sets[variable]:
            memberships[fuzzy_set_name] = self.get_membership_value(
                variable, fuzzy_set_name, value
            )
        return memberships
    
    @staticmethod
    def and_operator(values: List[float]) -> float:
        """Toán tử AND (min)"""
        return min(values) if values else 0.0
    
    @staticmethod
    def or_operator(values: List[float]) -> float:
        """Toán tử OR (max)"""
        return max(values) if values else 0.0
    
    @staticmethod
    def not_operator(value: float) -> float:
        """Toán tử NOT"""
        return 1.0 - value
    
    @staticmethod
    def defuzzify_centroid(fuzzy_values: Dict[str, float], ranges: Dict[str, Tuple[float, float]]) -> float:
        """
        Giải mờ bằng phương pháp tâm hình (Centroid)
        Tính giá trị thực từ các giá trị mờ
        
        Args:
            fuzzy_values: {fuzzy_set_name -> membership_degree}
            ranges: {fuzzy_set_name -> (min, max)}
        
        Returns:
            Giá trị giải mờ
        """
        total_weighted_value = 0.0
        total_weight = 0.0
        
        for fuzzy_set_name, membership in fuzzy_values.items():
            if membership > 0:
                min_val, max_val = ranges.get(fuzzy_set_name, (0, 100))
                center = (min_val + max_val) / 2
                total_weighted_value += membership * center
                total_weight += membership
        
        return total_weighted_value / total_weight if total_weight > 0 else 0.0


class SymptomFuzzifier:
    """Chuyển đổi các triệu chứng thành giá trị mờ"""
    
    def __init__(self, fuzzy_logic: FuzzyLogic):
        self.fuzzy_logic = fuzzy_logic
    
    def evaluate_symptom_certainty(self, symptom_name: str, certainty: float) -> Dict[str, float]:
        """
        Đánh giá độ tin cậy của triệu chứng
        
        Args:
            symptom_name: tên triệu chứng
            certainty: độ chắc chắn [0, 100]
        
        Returns:
            {level_name -> membership_degree}
        """
        return self.fuzzy_logic.get_all_memberships('confidence', certainty)
    
    def evaluate_clinical_value(self, value_name: str, value: float) -> Dict[str, float]:
        """
        Đánh giá giá trị lâm sàng (nhiệt độ, huyết áp, ...)
        """
        return self.fuzzy_logic.get_all_memberships(value_name, value)
