import pytest
from DynamicAnalyzer import get_tests

class TestControl:
    expected_for_change_1 = set(["boolCheck_boolIsFalse", "greaterThanZero_minus_1000", "greaterThanZero_minus_1", "greaterThanZero_0", "greaterThanZero_1", "greaterThanZero_1000", "elseIf_0"])
    expected_for_change_2 = set(["boolCheck_boolIsTrue", "greaterThanZero_1", "greaterThanZero_1000", "elseIf_1", "elseIf_1000"])
    expected_for_change_3 = set(["greaterThanZero_minus_1000", "greaterThanZero_minus_1", "greaterThanZero_1", "greaterThanZero_1000", "elseIf_minus_1000", "elseIf_minus_1", "elseIf_1", "elseIf_1000"])

    def test_change_1_exact(self):
        result = get_tests(
            "../../TargetSource/target/classes/org/dtu/analysis/control/Conditions.json",
            "../../TargetSource/target/classes/org/dtu/analysis/controlChanges1/ConditionalChanges1.json",
            "../../TargetSource/target/test-classes/org/dtu/analysis/control/ControlFlowTests.json")
        assert set(result) == self.expected_for_change_1
    
    def test_change_1_complete(self):
        result = get_tests(
            "../../TargetSource/target/classes/org/dtu/analysis/control/Conditions.json",
            "../../TargetSource/target/classes/org/dtu/analysis/controlChanges1/ConditionalChanges1.json",
            "../../TargetSource/target/test-classes/org/dtu/analysis/control/ControlFlowTests.json")
        assert set(result).issuperset(self.expected_for_change_1)
    
    def test_change_2_exact(self):
        result = get_tests(
            "../../TargetSource/target/classes/org/dtu/analysis/control/Conditions.json",
            "../../TargetSource/target/classes/org/dtu/analysis/controlChanges2/ConditionalChanges2.json",
            "../../TargetSource/target/test-classes/org/dtu/analysis/control/ControlFlowTests.json")
        assert set(result) == self.expected_for_change_2
    
    def test_change_2_complete(self):
        result = get_tests(
            "../../TargetSource/target/classes/org/dtu/analysis/control/Conditions.json",
            "../../TargetSource/target/classes/org/dtu/analysis/controlChanges2/ConditionalChanges2.json",
            "../../TargetSource/target/test-classes/org/dtu/analysis/control/ControlFlowTests.json")
        assert set(result).issuperset(self.expected_for_change_2)
    
    def test_change_3_exact(self):
        result = get_tests(
            "../../TargetSource/target/classes/org/dtu/analysis/control/Conditions.json",
            "../../TargetSource/target/classes/org/dtu/analysis/controlChanges3/ConditionalChanges3.json",
            "../../TargetSource/target/test-classes/org/dtu/analysis/control/ControlFlowTests.json")
        assert set(result) == self.expected_for_change_3

    def test_change_3_complete(self):
        result = get_tests(
            "../../TargetSource/target/classes/org/dtu/analysis/control/Conditions.json",
            "../../TargetSource/target/classes/org/dtu/analysis/controlChanges3/ConditionalChanges3.json",
            "../../TargetSource/target/test-classes/org/dtu/analysis/control/ControlFlowTests.json")
        assert set(result).issuperset(self.expected_for_change_3)