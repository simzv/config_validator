import unittest

from ..basic_rules import NotEmptyStringNode


class NotEmptyNotEmptyStringNodeTest(unittest.TestCase):

    def test_rule_init(self):
        rule = NotEmptyStringNode('value', 'path')
        self.assertEqual(rule.value, 'value')
        self.assertEqual(rule.path, 'path')

    def test_validate_with_none_value(self):
        rule = NotEmptyStringNode(None, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_integer_value(self):
        rule = NotEmptyStringNode(1, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_boolean_true_value(self):
        rule = NotEmptyStringNode(True, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_boolean_false_value(self):
        rule = NotEmptyStringNode(False, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_empty_string_value(self):
        rule = NotEmptyStringNode('', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_not_empty_string_value(self):
        rule = NotEmptyStringNode('test string', 'root')
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_string_of_unsigned_integer_value(self):
        rule = NotEmptyStringNode('123', 'root')
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_string_of_signed_positive_integer_value(self):
        rule = NotEmptyStringNode('+123', 'root')
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_string_of_signed_negative_integer_value(self):
        rule = NotEmptyStringNode('-123', 'root')
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_dictionary_value(self):
        rule = NotEmptyStringNode({'value': 123}, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_list_value(self):
        rule = NotEmptyStringNode(['value', 123], 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_adding_child(self):
        parent_rule = NotEmptyStringNode(123, 'root')
        child_rule = NotEmptyStringNode(456, 'child')
        with self.assertRaises(NotImplementedError):
            parent_rule.add_child(child_rule)

    def test_removing_child(self):
        parent_rule = NotEmptyStringNode(123, 'root')
        child_rule = NotEmptyStringNode(456, 'child')
        with self.assertRaises(NotImplementedError):
            parent_rule.remove_child(child_rule)
