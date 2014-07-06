import unittest

from ..basic_builder import BasicRulesBuilder
from .. import basic_rules


class BuilderTest(unittest.TestCase):

    def setUp(self):
        self.builder = BasicRulesBuilder()

    def test_build_integer(self):
        self.builder.build_integer(1, None, 'int path')
        rule = self.builder.get_product()
        self.assertIsInstance(rule, basic_rules.IntegerNode)
        self.assertEqual(rule.value, 1)
        self.assertEqual(rule.path, 'int path')

    def test_build_boolean(self):
        self.builder.build_boolean(True, None, 'true path')
        rule = self.builder.get_product()
        self.assertIsInstance(rule, basic_rules.BooleanNode)
        self.assertEqual(rule.value, True)
        self.assertEqual(rule.path, 'true path')

    def test_build_string(self):
        self.builder.build_string('test string', None, 'string path')
        rule = self.builder.get_product()
        self.assertIsInstance(rule, basic_rules.StringNode)
        self.assertEqual(rule.value, 'test string')
        self.assertEqual(rule.path, 'string path')

    def test_build_string_of_unsigned_integers(self):
        self.builder.build_string_of_unsigned_integers('123', None, '321 path')
        rule = self.builder.get_product()
        self.assertIsInstance(rule, basic_rules.StringOfUnsignedInteger)
        self.assertEqual(rule.value, '123')
        self.assertEqual(rule.path, '321 path')

    def test_build_not_empty_string(self):
        self.builder.build_not_empty_string('not empty string', None, 'a path')
        rule = self.builder.get_product()
        self.assertIsInstance(rule, basic_rules.NotEmptyStringNode)
        self.assertEqual(rule.value, 'not empty string')
        self.assertEqual(rule.path, 'a path')

    def test_build_dictiionary(self):
        self.builder.build_dictionary({}, None,
                                      mandatory_keys={'m1', 'm2'},
                                      optional_keys={'o1', 'o2'},
                                      strict_keys_set=False,
                                      path='dict path')
        rule = self.builder.get_product()
        self.assertIsInstance(rule, basic_rules.DictNode)
        self.assertEqual(rule.value, {})
        self.assertEqual(rule.mandatory_keys, {'m1', 'm2'})
        self.assertEqual(rule.optional_keys, {'o1', 'o2'})
        self.assertFalse(rule.strict_keys_set)
        self.assertEqual(rule.path, 'dict path')

    def test_build_list(self):
        self.builder.build_list([1, 2, 3], None, min_length=0,
                                max_length=10,
                                path='list path')
        rule = self.builder.get_product()
        self.assertIsInstance(rule, basic_rules.ListNode)
        self.assertEqual(rule.value, [1, 2, 3])
        self.assertEqual(rule.min_length, 0)
        self.assertEqual(rule.max_length, 10)
        self.assertEqual(rule.path, 'list path')

    def test_build_meta_rule(self):
        self.builder.build_meta_rule('meta value', None, 'meta path')
        rule = self.builder.get_product()
        self.assertIsInstance(rule, basic_rules.MetaNode)
        self.assertEqual(rule.value, 'meta value')
        self.assertEqual(rule.path, 'meta path')

    def test_clean(self):
        self.builder.build_integer(1, None)
        self.assertIsNotNone(self.builder.get_product())
        self.builder.clean()
        self.assertIsNone(self.builder.get_product())

    def test_rules_hierarchy(self):
        root_id = self.builder.build_dictionary(
            {'a': {'b': 1}, 'c': ['d', 'e']},
            None,
            strict_keys_set=False,
            path='/'
        )
        rule_a_id = self.builder.build_dictionary(
            {'b': 1},
            root_id,
            strict_keys_set=False,
            path='/a'
        )
        rule_c_id = self.builder.build_list(
            ['d', 'e'],
            root_id,
            path='/c'
        )
        rule_d_id = self.builder.build_string('d', rule_c_id, path='/c/0')
        rule_b_id = self.builder.build_integer(1, rule_a_id, path='/a/b')
        rule_e_id = self.builder.build_string('e', rule_c_id, path='/c/1')

        root_rule = self.builder.get_product()

        rule_a = self.builder._rules_list[rule_a_id]
        rule_b = self.builder._rules_list[rule_b_id]
        rule_c = self.builder._rules_list[rule_c_id]
        rule_d = self.builder._rules_list[rule_d_id]
        rule_e = self.builder._rules_list[rule_e_id]

        self.assertIn(rule_a, root_rule._children)
        self.assertIn(rule_c, root_rule._children)
        self.assertEqual(len(root_rule._children), 2)

        self.assertIn(rule_b, rule_a._children)
        self.assertEqual(len(rule_a._children), 1)

        self.assertIn(rule_d, rule_c._children)
        self.assertIn(rule_e, rule_c._children)
        self.assertEqual(len(rule_c._children), 2)
