import unittest

from ..basic_rules import ListNode, BooleanNode


class ListNodeTest(unittest.TestCase):

    def test_rule_init(self):
        rule = ListNode('value', 'path')
        self.assertEqual(rule.value, 'value')
        self.assertEqual(rule.path, 'path')

    def test_validate_with_none_value(self):
        rule = ListNode(None, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_integer_value(self):
        rule = ListNode(1, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_boolean_true_value(self):
        rule = ListNode(True, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_boolean_false_value(self):
        rule = ListNode(False, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_empty_string_value(self):
        rule = ListNode('', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_not_empty_string_value(self):
        rule = ListNode('test string', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_unsigned_integer_value(self):
        rule = ListNode('123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_signed_positive_integer_value(self):
        rule = ListNode('+123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_signed_negative_integer_value(self):
        rule = ListNode('-123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_dictionary_value(self):
        rule = ListNode({'value': 123}, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_list_value(self):
        rule = ListNode(['value', 123], 'root')
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors(), list)

    def test_adding_child(self):
        parent_rule = ListNode([], 'root')
        child_rule = BooleanNode(True, 'child')
        self.assertNotIn(child_rule, parent_rule._children)
        parent_rule.add_child(child_rule)
        self.assertIn(child_rule, parent_rule._children)

    def test_removing_child(self):
        parent_rule = ListNode([], 'root')
        child_rule = BooleanNode(True, 'child')
        parent_rule._children.add(child_rule)
        self.assertIn(child_rule, parent_rule._children)
        parent_rule.remove_child(child_rule)
        self.assertNotIn(child_rule, parent_rule._children)

    def test_validate_whith_one_valid_child(self):
        rule = ListNode([], 'root')
        rule.add_child(BooleanNode(True, 'child'))
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_whith_one_invalid_child(self):
        rule = ListNode([], 'root')
        rule.add_child(BooleanNode('Invalid Value', 'child'))
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1+1)

    def test_validate_whith_all_valid_children(self):
        rule = ListNode([], 'root')
        for i in range(10):
            rule.add_child(BooleanNode(True, 'child#%d' % i))

        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_whith_not_all_valid_children(self):
        rule = ListNode([], 'root')
        good_child_value = True
        bad_child_value = 'Invalid Value'
        for i in range(10):
            rule.add_child(BooleanNode(good_child_value, 'child#%d' % i*2))
            rule.add_child(BooleanNode(bad_child_value, 'child#%d' % (i*2+1)))

        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 10+1)

    def test_validate_whith_all_invalid_children(self):
        rule = ListNode([], 'root')
        for i in range(10):
            rule.add_child(BooleanNode('Invalid Value', 'child#%d' % i))

        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 10+1)

    def test_validate_smaller_than_min_length(self):
        values = ([], [1], [1, 2])
        for value in values:
            rule = ListNode(value, 'root')
            rule.min_length = 3
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_larger_than_max_length(self):
        values = ([1], [1, 2], [1, 2, 3])
        for value in values:
            rule = ListNode(value, 'root')
            rule.max_length = 0
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_not_smaller_than_min_length(self):
        values = ([], [1], [1, 2])
        for value in values:
            rule = ListNode(value, 'root')
            rule.min_length = 0
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())

    def test_validate_not_larger_than_max_length(self):
        values = ([1], [1, 2], [1, 2, 3])
        for value in values:
            rule = ListNode(value, 'root')
            rule.max_length = 3
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())
