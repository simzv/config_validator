import unittest

from ..basic_rules import CompositeNode, BooleanNode


class CompositeNodeTest(unittest.TestCase):

    def test_rule_init(self):
        rule = CompositeNode('value', 'path')
        self.assertEqual(rule.value, 'value')
        self.assertEqual(rule.path, 'path')

    def test_adding_child(self):
        parent_rule = CompositeNode(None, 'root')
        child_rule = BooleanNode(True, 'child')
        self.assertNotIn(child_rule, parent_rule._children)
        parent_rule.add_child(child_rule)
        self.assertIn(child_rule, parent_rule._children)

    def test_removing_child(self):
        parent_rule = CompositeNode(None, 'root')
        child_rule = BooleanNode(True, 'child')
        parent_rule._children.add(child_rule)
        self.assertIn(child_rule, parent_rule._children)
        parent_rule.remove_child(child_rule)
        self.assertNotIn(child_rule, parent_rule._children)

    def test_validate_without_children_for_all_values(self):
        values = (None, 1, True, False, '', 'test string', '123', '+123',
                  '-123', {'value': 123}, ['value', 123])
        for value in values:
            rule = CompositeNode(value, 'root')
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())

    def test_validate_whith_one_valid_child(self):
        rule = CompositeNode(None, 'root')
        rule.add_child(BooleanNode(True, 'child'))
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_whith_one_invalid_child(self):
        rule = CompositeNode(None, 'root')
        rule.add_child(BooleanNode('Invalid Value', 'child'))
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1+1)

    def test_validate_whith_all_valid_children(self):
        rule = CompositeNode(None, 'root')
        for i in range(10):
            rule.add_child(BooleanNode(True, 'child#%d' % i))

        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_whith_not_all_valid_children(self):
        rule = CompositeNode(None, 'root')
        good_child_value = True
        bad_child_value = 'Invalid Value'
        for i in range(10):
            rule.add_child(BooleanNode(good_child_value, 'child#%d' % i*2))
            rule.add_child(BooleanNode(bad_child_value, 'child#%d' % (i*2+1)))

        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 10+1)

    def test_validate_whith_all_invalid_children(self):
        rule = CompositeNode(None, 'root')
        for i in range(10):
            rule.add_child(BooleanNode('Invalid Value', 'child#%d' % i))

        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 10+1)
