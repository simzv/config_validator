import unittest

from ..basic_builder import BasicRulesBuilder
from ..basic_director import BasicRulesDirector, HandledDirector
from .. import basic_rules
from ..basic_director_handlers import RuleParseHandler


class DirectorWithBasicRulesBuilderTest(unittest.TestCase):

    def setUp(self):
        self.builder = BasicRulesBuilder()

    def test_one_rule_scheme_integer(self):
        schema = {'type': 'integer'}
        value = 10
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.IntegerNode)
        self.assertEqual(rules.value, value)
        self.assertEqual(rules.path, '/')

    def test_one_rule_scheme_boolean(self):
        schema = {'type': 'boolean'}
        value = True
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.BooleanNode)
        self.assertEqual(rules.value, value)
        self.assertEqual(rules.path, '/')

    def test_one_rule_scheme_string(self):
        schema = {'type': 'string'}
        value = ''
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.StringNode)
        self.assertEqual(rules.value, value)
        self.assertEqual(rules.path, '/')

    def test_one_rule_scheme_not_empty_string(self):
        schema = {'type': 'not_empty_string'}
        value = 'test string'
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.NotEmptyStringNode)
        self.assertEqual(rules.value, value)
        self.assertEqual(rules.path, '/')

    def test_one_rule_scheme_string_of_unsigned_integers(self):
        schema = {'type': 'string_of_unsigned_integers'}
        value = '12122013'
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.StringOfUnsignedInteger)
        self.assertEqual(rules.value, value)
        self.assertEqual(rules.path, '/')

    def test_meta_rule(self):
        schema = [{'type': 'integer'},
                  {'type': 'string_of_unsigned_integers'},
                  {'type': 'boolean'}]
        value = '777'
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.MetaNode)
        self.assertEqual(rules.value, value)
        self.assertEqual(rules.path, '/')
        self.assertIsInstance(rules._children, set)
        self.assertEqual(len(rules._children), 3)
        expected_children_types = {
            basic_rules.IntegerNode,
            basic_rules.StringOfUnsignedInteger,
            basic_rules.BooleanNode
        }
        real_children_types_set = set()
        for rule in rules._children:
            real_children_types_set.add(type(rule))
            self.assertIsInstance(rule, basic_rules.Node)
            self.assertEqual(rule.value, value)
            self.assertRegexpMatches(rule.path, '^\(alt.#\d\)')

        self.assertEqual(expected_children_types, real_children_types_set)

    def test_list_rule_without_allowed(self):
        min_length = 0
        max_length = 10
        schema = {
            'type': 'list',
            'min_length': min_length,
            'max_length': max_length,
        }
        value = [1, 2, 3, 4, 5]
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.ListNode)
        self.assertEqual(rules.value, value)
        self.assertEqual(rules.path, '/')
        self.assertEqual(rules.min_length, min_length)
        self.assertEqual(rules.max_length, max_length)
        self.assertIsInstance(rules._children, set)
        self.assertEqual(len(rules._children), 0)

    def test_list_rule_with_allowed(self):
        min_length = 0
        max_length = 10
        schema = {
            'type': 'list',
            'min_length': min_length,
            'max_length': max_length,
            'allowed': {'type': 'integer'}
        }
        value = [1, 2, 3, 4, 5]
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.ListNode)
        self.assertEqual(rules.value, value)
        self.assertEqual(rules.path, '/')
        self.assertEqual(rules.min_length, min_length)
        self.assertEqual(rules.max_length, max_length)
        self.assertIsInstance(rules._children, set)
        self.assertEqual(len(rules._children), len(value))
        expected_map = {'/%d' % i: value[i] for i in range(len(value))}
        real_map = {}
        for rule in rules._children:
            self.assertIsInstance(rule, basic_rules.IntegerNode)
            real_map[rule.path] = rule.value
        self.assertEqual(expected_map, real_map)

    def test_dict_rule_not_strict_with_allowed(self):
        strict_keys_set = False
        schema = {
            'type': 'dictionary',
            'mandatory': {
                'm1': {'type': 'string'},
                'm2': {'type': 'boolean'}
            },
            'optional': {
                'o1': {'type': 'integer'},
                'o2': {'type': 'boolean'}
            },
            'strict_keys_set': strict_keys_set,
            'allowed': {
                'type': 'dictionary',
                'mandatory': {
                    'mm1': {'type': 'string'},
                    'mm2': {'type': 'boolean'}
                }
            }
        }
        value = {
            'm1': 'm1_value',
            'm2': False,
            'o2': True,
            'allowed_1': {
                'mm1': 'mm1-1_value',
                'mm2': False
            },
            'allowed_2': {
                'mm1': 'mm1-2_value',
                'mm2': True
            }
        }
        director = BasicRulesDirector(schema, self.builder)
        rules = director.build_rules_tree(value)
        self.assertTrue(rules.validate())
        self.assertIsInstance(rules, basic_rules.DictNode)
        self.assertEqual(rules.mandatory_keys, {'m1', 'm2'})
        self.assertEqual(rules.optional_keys, {'o1', 'o2'})
        self.assertEqual(rules.strict_keys_set, strict_keys_set)
        self.assertEqual(rules.path, '/')
        self.assertEqual(rules.value, value)

        self.assertIsInstance(rules._children, set)
        self.assertEqual(len(rules._children), 5)

        expected_map = {
            '/m1': {
                'value': value['m1'],
                'type': basic_rules.StringNode
            },
            '/m2': {
                'value': value['m2'],
                'type': basic_rules.BooleanNode
            },
            '/o2': {
                'value': value['o2'],
                'type': basic_rules.BooleanNode
            },
            '/allowed_1': {
                'value': value['allowed_1'],
                'type': basic_rules.DictNode
            },
            '/allowed_2': {
                'value': value['allowed_2'],
                'type': basic_rules.DictNode
            }
        }

        real_list_of_paths = []

        for rule in rules._children:
            real_list_of_paths.append(rule.path)
            self.assertIn(rule.path, expected_map)
            self.assertEqual(rule.value, expected_map[rule.path]['value'])
            self.assertIsInstance(rule, expected_map[rule.path]['type'])

        self.assertEqual(sorted(real_list_of_paths),
                         sorted(expected_map.keys()))


class DirectorHandleOpsTest(unittest.TestCase):

    def setUp(self):
        self.builder = BasicRulesBuilder()
        self.director = HandledDirector([], self.builder)

    def test_push_and_shift(self):
        foo = RuleParseHandler(self.builder)
        bar = RuleParseHandler(self.builder)
        baz = RuleParseHandler(self.builder)
        self.assertIsNone(self.director.shift_handler())
        self.director.push_handler(foo)
        self.assertIs(foo, self.director.shift_handler())
        self.assertIsNone(self.director.shift_handler())
        self.director.push_handler(foo)
        self.director.push_handler(bar)
        self.assertIs(bar, self.director.shift_handler())
        self.director.push_handler(baz)
        self.assertIs(baz, self.director.shift_handler())
        self.assertIs(foo, self.director.shift_handler())
        self.assertIsNone(self.director.shift_handler())

    def test_push_and_pop(self):
        foo = RuleParseHandler(self.builder)
        bar = RuleParseHandler(self.builder)
        baz = RuleParseHandler(self.builder)
        self.assertIsNone(self.director.pop_handler())
        self.director.push_handler(foo)
        self.assertIs(foo, self.director.pop_handler())
        self.assertIsNone(self.director.pop_handler())
        self.director.push_handler(foo)
        self.director.push_handler(bar)
        self.assertIs(foo, self.director.pop_handler())
        self.director.push_handler(baz)
        self.assertIs(bar, self.director.pop_handler())
        self.assertIs(baz, self.director.pop_handler())
        self.assertIsNone(self.director.pop_handler())

    def test_append_and_shift(self):
        foo = RuleParseHandler(self.builder)
        bar = RuleParseHandler(self.builder)
        baz = RuleParseHandler(self.builder)
        self.assertIsNone(self.director.shift_handler())
        self.director.append_handler(foo)
        self.assertIs(foo, self.director.shift_handler())
        self.assertIsNone(self.director.shift_handler())
        self.director.append_handler(foo)
        self.director.append_handler(bar)
        self.assertIs(foo, self.director.shift_handler())
        self.director.append_handler(baz)
        self.assertIs(bar, self.director.shift_handler())
        self.assertIs(baz, self.director.shift_handler())
        self.assertIsNone(self.director.shift_handler())

    def test_append_and_pop(self):
        foo = RuleParseHandler(self.builder)
        bar = RuleParseHandler(self.builder)
        baz = RuleParseHandler(self.builder)
        self.assertIsNone(self.director.pop_handler())
        self.director.append_handler(foo)
        self.assertIs(foo, self.director.pop_handler())
        self.assertIsNone(self.director.pop_handler())
        self.director.append_handler(foo)
        self.director.append_handler(bar)
        self.assertIs(bar, self.director.pop_handler())
        self.director.append_handler(baz)
        self.assertIs(baz, self.director.pop_handler())
        self.assertIs(foo, self.director.pop_handler())
        self.assertIsNone(self.director.pop_handler())
