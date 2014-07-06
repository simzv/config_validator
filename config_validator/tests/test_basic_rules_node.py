import unittest

from ..basic_rules import Node


class NodeTest(unittest.TestCase):

    def test_rule_init(self):
        rule = Node('value', 'path')
        self.assertEqual(rule.value, 'value')
        self.assertEqual(rule.path, 'path')

    def test_validate_with_none_value(self):
        rule = Node(None, 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_integer_value(self):
        rule = Node(1, 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_boolean_true_value(self):
        rule = Node(True, 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_boolean_false_value(self):
        rule = Node(False, 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_empty_string_value(self):
        rule = Node('', 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_not_empty_string_value(self):
        rule = Node('test string', 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_string_of_unsigned_integer_value(self):
        rule = Node('123', 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_string_of_signed_positive_integer_value(self):
        rule = Node('+123', 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_string_of_signed_negative_integer_value(self):
        rule = Node('-123', 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_dictionary_value(self):
        rule = Node({'value': 123}, 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_validate_with_list_value(self):
        rule = Node(['value', 123], 'root')
        with self.assertRaises(NotImplementedError):
            self.assertFalse(rule.validate())

        self.assertIsNone(rule.get_all_errors())

    def test_adding_child(self):
        parent_rule = Node(123, 'root')
        child_rule = Node(456, 'child')
        with self.assertRaises(NotImplementedError):
            parent_rule.add_child(child_rule)

    def test_removing_child(self):
        parent_rule = Node(123, 'root')
        child_rule = Node(456, 'child')
        with self.assertRaises(NotImplementedError):
            parent_rule.remove_child(child_rule)
