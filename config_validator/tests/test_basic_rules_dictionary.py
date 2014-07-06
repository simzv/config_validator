import unittest

from ..basic_rules import DictNode, BooleanNode


class CommonDictNodeTest(unittest.TestCase):

    def test_rule_init(self):
        rule = DictNode('value', 'path')
        self.assertEqual(rule.value, 'value')
        self.assertEqual(rule.path, 'path')

    def test_adding_child(self):
        parent_rule = DictNode({}, 'root')
        child_rule = BooleanNode(True, 'child')
        self.assertNotIn(child_rule, parent_rule._children)
        parent_rule.add_child(child_rule)
        self.assertIn(child_rule, parent_rule._children)

    def test_removing_child(self):
        parent_rule = DictNode({}, 'root')
        child_rule = BooleanNode(True, 'child')
        parent_rule._children.add(child_rule)
        self.assertIn(child_rule, parent_rule._children)
        parent_rule.remove_child(child_rule)
        self.assertNotIn(child_rule, parent_rule._children)

    def test_validate_whith_one_valid_child(self):
        rule = DictNode({}, 'root')
        rule.add_child(BooleanNode(True, 'child'))
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_whith_one_invalid_child(self):
        rule = DictNode({}, 'root')
        rule.add_child(BooleanNode('Invalid Value', 'child'))
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1+1)

    def test_validate_whith_all_valid_children(self):
        rule = DictNode({}, 'root')
        for i in range(10):
            rule.add_child(BooleanNode(True, 'child#%d' % i))

        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_validate_whith_not_all_valid_children(self):
        rule = DictNode({}, 'root')
        good_child_value = True
        bad_child_value = 'Invalid Value'
        for i in range(10):
            rule.add_child(BooleanNode(good_child_value, 'child#%d' % i*2))
            rule.add_child(BooleanNode(bad_child_value, 'child#%d' % (i*2+1)))

        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 10+1)

    def test_validate_whith_all_invalid_children(self):
        rule = DictNode({}, 'root')
        for i in range(10):
            rule.add_child(BooleanNode('Invalid Value', 'child#%d' % i))

        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 10+1)

    def test_validate_with_none_value(self):
        rule = DictNode(None, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_integer_value(self):
        rule = DictNode(1, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_boolean_true_value(self):
        rule = DictNode(True, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_boolean_false_value(self):
        rule = DictNode(False, 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_empty_string_value(self):
        rule = DictNode('', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_not_empty_string_value(self):
        rule = DictNode('test string', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_unsigned_integer_value(self):
        rule = DictNode('123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_signed_positive_integer_value(self):
        rule = DictNode('+123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_string_of_signed_negative_integer_value(self):
        rule = DictNode('-123', 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)

    def test_validate_with_list_value(self):
        rule = DictNode(['value', 123], 'root')
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)


class NoMandatoryNoOptionalStrictDictNodeTest(unittest.TestCase):

    def test_empty_dictionary(self):
        value = {}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = set()
        rule.optional_keys = set()
        rule.strict_keys_set = True
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_dictionary_with_unknown_keys(self):
        value = {'u1': 1, 'u2': 2}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = set()
        rule.optional_keys = set()
        rule.strict_keys_set = True
        self.assertFalse(rule.validate())
        self.assertIsInstance(rule.get_all_errors(), list)
        self.assertEqual(len(rule.get_all_errors()), 1)


class NoMandatoryNoOptionalNotStrictDictNodeTest(unittest.TestCase):

    def test_empty_dictionary(self):
        value = {}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = set()
        rule.optional_keys = set()
        rule.strict_keys_set = False
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_dictionary_with_unknown_keys(self):
        value = {'u1': 1, 'u2': 2}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = set()
        rule.optional_keys = set()
        rule.strict_keys_set = False
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())


class MandatoryNoOptionalStrictDictNodeTest(unittest.TestCase):

    def test_dictionary_with_not_all_mandatory_keys_no_unknown(self):
        values = (
            {},
            {'m1': 1},
            {'m2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = set()
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_dictionary_with_not_all_mandatory_keys_with_unknown(self):
        values = (
            {'u1': 1},
            {'m1': 1, 'u1': 1},
            {'m2': 2, 'u1': 1}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = set()
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 2)

    def test_dictionary_with_all_mandatory_keys_no_unknown(self):
        value = {'m1': 1, 'm2': 2}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = {'m1', 'm2'}
        rule.optional_keys = set()
        rule.strict_keys_set = True
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_dictionary_with_all_mandatory_keys_with_unknown(self):
        values = (
            {'m1': 1, 'm2': 2, 'u1': 1},
            {'m1': 1, 'm2': 2, 'u2': 2},
            {'m1': 1, 'm2': 2, 'u1': 1, 'u2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = set()
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)


class MandatoryNoOptionalNotStrictDictNodeTest(unittest.TestCase):

    def test_dictionary_with_not_all_mandatory_keys(self):
        values = (
            {},
            {'m1': 1},
            {'m2': 2},
            {'u1': 1},
            {'m1': 1, 'u1': 1},
            {'m2': 2, 'u1': 1}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = set()
            rule.strict_keys_set = False
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_dictionary_with_all_mandatory_keys(self):
        values = (
            {'m1': 1, 'm2': 2},
            {'m1': 1, 'm2': 2, 'u1': 1},
            {'m1': 1, 'm2': 2, 'u2': 2},
            {'m1': 1, 'm2': 2, 'u1': 1, 'u2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = set()
            rule.strict_keys_set = False
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())


class NoMandatoryOptionalStrictDictNodeTest(unittest.TestCase):

    def test_dictionary_not_all_optional_keys_no_unknown(self):
        values = (
            {},
            {'o1': 1},
            {'o2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = set()
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())

    def test_dictionary_with_all_optional_keys_no_unknown(self):
        value = {'o1': 1, 'o2': 2}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = set()
        rule.optional_keys = {'o1', 'o2'}
        rule.strict_keys_set = True
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_dictionary_not_all_optional_keys_with_unknown(self):
        values = (
            {'u1': 1},
            {'u1': 1, 'u2': 2},
            {'o1': 1, 'u1': 1},
            {'o2': 2, 'u2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = set()
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_dictionary_with_all_optional_keys_with_unknown(self):
        values = (
            {'o1': 1, 'o2': 2, 'u1': 1},
            {'o1': 1, 'o2': 2, 'u2': 2},
            {'o1': 1, 'o2': 2, 'u1': 1, 'u2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = set()
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)


class NoMandatoryOptionalNotStrictDictNodeTest(unittest.TestCase):

    def test_dictionary_not_all_optional_keys_no_unknown(self):
        values = (
            {},
            {'o1': 1},
            {'o2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = set()
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())

    def test_dictionary_with_all_optional_keys_no_unknown(self):
        value = {'o1': 1, 'o2': 2}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = set()
        rule.optional_keys = {'o1', 'o2'}
        rule.strict_keys_set = False
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_dictionary_not_all_optional_keys_with_unknown(self):
        values = (
            {'u1': 1},
            {'u1': 1, 'u2': 2},
            {'o1': 1, 'u1': 1},
            {'o2': 2, 'u2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = set()
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())

    def test_dictionary_with_all_optional_keys_with_unknown(self):
        values = (
            {'o1': 1, 'o2': 2, 'u1': 1},
            {'o1': 1, 'o2': 2, 'u2': 2},
            {'o1': 1, 'o2': 2, 'u1': 1, 'u2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = set()
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())


class MandatoryOptionalStrictDictNodeTest(unittest.TestCase):

    def test_not_all_mandatory_not_all_optional_no_unknown(self):
        values = (
            {'m1': 1},
            {'m2': 2},
            {'o1': 1},
            {'o2': 2},
            {'m1': 1, 'o1': 1},
            {'m2': 2, 'o1': 1},
            {'m1': 1, 'o2': 2},
            {'m2': 2, 'o2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_with_all_mandatory_not_all_optional_no_unknown(self):
        values = (
            {'m1': 1, 'm2': 2, 'o1': 1},
            {'m1': 1, 'm2': 2, 'o2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())

    def test_not_all_mandatory_with_all_optional_no_unknown(self):
        values = (
            {'o1': 1, 'o2': 2},
            {'m1': 1, 'o1': 1, 'o2': 2},
            {'m2': 2, 'o1': 1, 'o2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_with_all_mandatory_with_all_optional_no_unknown(self):
        value = {'m1': 1, 'm2': 2, 'o1': 1, 'o2': 2}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = {'m1', 'm2'}
        rule.optional_keys = {'o1', 'o2'}
        rule.strict_keys_set = True
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_not_all_mandatory_not_all_optional_with_unknown(self):
        values = (
            {'m1': 1, 'u1': 1},
            {'m2': 2, 'u2': 2},
            {'o1': 1, 'u2': 2, 'u1': 1},
            {'o2': 2, 'u1': 1, 'u2': 2},
            {'m1': 1, 'o1': 1, 'u1': 1},
            {'m2': 2, 'o1': 1, 'u2': 2},
            {'m1': 1, 'o2': 2, 'u2': 2},
            {'m2': 2, 'o2': 2, 'u1': 1, 'u2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 2)

    def test_with_all_mandatory_not_all_optional_with_unknown(self):
        values = (
            {'m1': 1, 'm2': 2, 'o1': 1, 'u1': 1},
            {'m1': 1, 'm2': 2, 'o2': 2, 'u2': 2, 'u1': 1},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_not_all_mandatory_with_all_optional_with_unknown(self):
        values = (
            {'o1': 1, 'o2': 2, 'u1': 1},
            {'m1': 1, 'o1': 1, 'o2': 2, 'u2': 2},
            {'m2': 2, 'o1': 1, 'o2': 2, 'u1': 1, 'u2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 2)

    def test_with_all_mandatory_with_all_optional_with_unknown(self):
        values = (
            {'m1': 1, 'm2': 2, 'o1': 1, 'o2': 2, 'u1': 1},
            {'m1': 1, 'm2': 2, 'o1': 1, 'o2': 2, 'u2': 2},
            {'m1': 1, 'm2': 2, 'o1': 1, 'o2': 2, 'u1': 1, 'u2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = True
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)


class MandatoryOptionalNotStrictDictNodeTest(unittest.TestCase):

    def test_not_all_mandatory_not_all_optional_no_unknown(self):
        values = (
            {'m1': 1},
            {'m2': 2},
            {'o1': 1},
            {'o2': 2},
            {'m1': 1, 'o1': 1},
            {'m2': 2, 'o1': 1},
            {'m1': 1, 'o2': 2},
            {'m2': 2, 'o2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_with_all_mandatory_not_all_optional_no_unknown(self):
        values = (
            {'m1': 1, 'm2': 2, 'o1': 1},
            {'m1': 1, 'm2': 2, 'o2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())

    def test_not_all_mandatory_with_all_optional_no_unknown(self):
        values = (
            {'o1': 1, 'o2': 2},
            {'m1': 1, 'o1': 1, 'o2': 2},
            {'m2': 2, 'o1': 1, 'o2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_with_all_mandatory_with_all_optional_no_unknown(self):
        value = {'m1': 1, 'm2': 2, 'o1': 1, 'o2': 2}
        rule = DictNode(value, 'root')
        rule.mandatory_keys = {'m1', 'm2'}
        rule.optional_keys = {'o1', 'o2'}
        rule.strict_keys_set = False
        self.assertTrue(rule.validate())
        self.assertIsNone(rule.get_all_errors())

    def test_not_all_mandatory_not_all_optional_with_unknown(self):
        values = (
            {'m1': 1, 'u1': 1},
            {'m2': 2, 'u2': 2},
            {'o1': 1, 'u2': 2, 'u1': 1},
            {'o2': 2, 'u1': 1, 'u2': 2},
            {'m1': 1, 'o1': 1, 'u1': 1},
            {'m2': 2, 'o1': 1, 'u2': 2},
            {'m1': 1, 'o2': 2, 'u2': 2},
            {'m2': 2, 'o2': 2, 'u1': 1, 'u2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_with_all_mandatory_not_all_optional_with_unknown(self):
        values = (
            {'m1': 1, 'm2': 2, 'o1': 1, 'u1': 1},
            {'m1': 1, 'm2': 2, 'o2': 2, 'u2': 2, 'u1': 1},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())

    def test_not_all_mandatory_with_all_optional_with_unknown(self):
        values = (
            {'o1': 1, 'o2': 2, 'u1': 1},
            {'m1': 1, 'o1': 1, 'o2': 2, 'u2': 2},
            {'m2': 2, 'o1': 1, 'o2': 2, 'u1': 1, 'u2': 2},
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertFalse(rule.validate())
            self.assertIsInstance(rule.get_all_errors(), list)
            self.assertEqual(len(rule.get_all_errors()), 1)

    def test_with_all_mandatory_with_all_optional_with_unknown(self):
        values = (
            {'m1': 1, 'm2': 2, 'o1': 1, 'o2': 2, 'u1': 1},
            {'m1': 1, 'm2': 2, 'o1': 1, 'o2': 2, 'u2': 2},
            {'m1': 1, 'm2': 2, 'o1': 1, 'o2': 2, 'u1': 1, 'u2': 2}
        )
        for value in values:
            rule = DictNode(value, 'root')
            rule.mandatory_keys = {'m1', 'm2'}
            rule.optional_keys = {'o1', 'o2'}
            rule.strict_keys_set = False
            self.assertTrue(rule.validate())
            self.assertIsNone(rule.get_all_errors())
