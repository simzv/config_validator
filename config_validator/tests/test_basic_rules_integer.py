import unittest

from ..basic_rules import IntegerNode


class IntegerNodeTest(unittest.TestCase):

    def test_rule_init(self):
        rule = IntegerNode('value', 'path')
        self.assertEqual(rule.value, 'value')
        self.assertEqual(rule.path, 'path')

    def test_validate_with_none_value(self):
        rule = IntegerNode(None, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_integer_value(self):
        rule = IntegerNode(1, 'root')
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_boolean_true_value(self):
        rule = IntegerNode(True, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_boolean_false_value(self):
        rule = IntegerNode(False, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_empty_string_value(self):
        rule = IntegerNode('', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_not_empty_string_value(self):
        rule = IntegerNode('test string', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_unsigned_integer_value(self):
        rule = IntegerNode('123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_signed_positive_integer_value(self):
        rule = IntegerNode('+123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_signed_negative_integer_value(self):
        rule = IntegerNode('-123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_dictionary_value(self):
        rule = IntegerNode({'value': 123}, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_list_value(self):
        rule = IntegerNode(['value', 123], 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_adding_child(self):
        parent_rule = IntegerNode(123, 'root')
        child_rule = IntegerNode(456, 'child')
        with self.assertRaises(NotImplementedError):
            parent_rule.add_child(child_rule)

    def test_removing_child(self):
        parent_rule = IntegerNode(123, 'root')
        child_rule = IntegerNode(456, 'child')
        with self.assertRaises(NotImplementedError):
            parent_rule.remove_child(child_rule)
