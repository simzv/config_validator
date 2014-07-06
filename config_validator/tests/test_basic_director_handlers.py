import unittest
from ..basic_builder import BasicRulesBuilder
from .. import basic_director_handlers


class FakeHandler(object):

    FAKE_MESSAGE = {
        "rule_definition": "Fake message"
    }
    FAKE_RULE_ID = -1

    def handle_message(self, message):
        if message is self.FAKE_MESSAGE:
            return self.FAKE_RULE_ID, []


class SimpleRuleHandlerTest(unittest.TestCase):

    def setUp(self):
        self.builder = BasicRulesBuilder()
        self.parser = basic_director_handlers.SimpleRuleParseHandler(
            self.builder)

        self.parser.next_handler = FakeHandler()

    def test_parse_integer_rule_definition(self):
        message = {
            "rule_definition": {
                "type": "integer"
            },
            "parent_rule_id": None,
            "value": 100,
            "path": ""
        }
        rule_id, new_messages = self.parser.handle_message(message)
        self.assertEqual(rule_id, 0)
        self.assertEqual(new_messages, [])

    def test_parse_string_rule_definition(self):
        message = {
            "rule_definition": {
                "type": "string"
            },
            "parent_rule_id": None,
            "value": "one hundred",
            "path": ""
        }
        rule_id, new_messages = self.parser.handle_message(message)
        self.assertEqual(rule_id, 0)
        self.assertEqual(new_messages, [])

    def test_parse_not_empty_string_rule_definition(self):
        message = {
            "rule_definition": {
                "type": "not_empty_string"
            },
            "parent_rule_id": None,
            "value": "not empty string",
            "path": ""
        }
        rule_id, new_messages = self.parser.handle_message(message)
        self.assertEqual(rule_id, 0)
        self.assertEqual(new_messages, [])

    def test_parse_string_of_unsigned_integers_rule_definition(self):
        message = {
            "rule_definition": {
                "type": "string_of_unsigned_integers"
            },
            "parent_rule_id": None,
            "value": "100",
            "path": ""
        }
        rule_id, new_messages = self.parser.handle_message(message)
        self.assertEqual(rule_id, 0)
        self.assertEqual(new_messages, [])

    def test_parse_boolean_rule_definition(self):
        message = {
            "rule_definition": {
                "type": "integer"
            },
            "parent_rule_id": None,
            "value": False,
            "path": ""
        }
        rule_id, new_messages = self.parser.handle_message(message)
        self.assertEqual(rule_id, 0)
        self.assertEqual(new_messages, [])

    def test_parse_fake_message(self):
        rule_id, new_messages = self.parser.handle_message(
            FakeHandler.FAKE_MESSAGE)
        self.assertEqual(rule_id, FakeHandler.FAKE_RULE_ID)
        self.assertEqual(new_messages, [])

    def test_parse_unknown_message(self):
        self.parser.next_handler = None
        rule_id, new_messages = self.parser.handle_message(
            FakeHandler.FAKE_MESSAGE)
        self.assertIsNone(rule_id)
        self.assertEqual(new_messages, [])


class ListRuleParseHandlerTest(unittest.TestCase):

    def setUp(self):
        self.builder = BasicRulesBuilder()
        self.parser = basic_director_handlers.ListRuleParseHandler(
            self.builder)

        self.parser.next_handler = FakeHandler()

    def test_parse_list_rule_definition(self):
        message = {
            "rule_definition": {
                "type": "list",
                "allow": {
                    "type": "string"
                }
            },
            "parent_rule_id": None,
            "value": ['a', 'b', 'c'],
            "path": ""
        }
        rule_id, new_messages = self.parser.handle_message(message)
        self.assertEqual(rule_id, 0)
        self.assertEqual(new_messages, [])

    def test_parse_fake_message(self):
        rule_id, new_messages = self.parser.handle_message(
            FakeHandler.FAKE_MESSAGE)
        self.assertEqual(rule_id, FakeHandler.FAKE_RULE_ID)
        self.assertEqual(new_messages, [])

    def test_parse_unknown_message(self):
        self.parser.next_handler = None
        rule_id, new_messages = self.parser.handle_message(
            FakeHandler.FAKE_MESSAGE)
        self.assertIsNone(rule_id)
        self.assertEqual(new_messages, [])


class DictRuleParseHandlerTest(unittest.TestCase):

    def setUp(self):
        self.builder = BasicRulesBuilder()
        self.parser = basic_director_handlers.DictRuleParseHandler(
            self.builder)

        self.parser.next_handler = FakeHandler()

    def test_parse_dict_rule_definition(self):
        message = {
            "rule_definition": {
                "type": "dictionary",
                "strict_keys_set": False,
                "allowed": {
                    "type": "string"
                }
            },
            "parent_rule_id": None,
            "value": {'a': 'aa', 'b': 'bb', 'c': 'cc'},
            "path": ""
        }
        rule_id, new_messages = self.parser.handle_message(message)
        self.assertEqual(rule_id, 0)
        self.assertIsInstance(new_messages, list)
        self.assertEqual(len(new_messages), 3)

    def test_parse_fake_message(self):
        rule_id, new_messages = self.parser.handle_message(
            FakeHandler.FAKE_MESSAGE)
        self.assertEqual(rule_id, FakeHandler.FAKE_RULE_ID)
        self.assertEqual(new_messages, [])

    def test_parse_unknown_message(self):
        self.parser.next_handler = None
        rule_id, new_messages = self.parser.handle_message(
            FakeHandler.FAKE_MESSAGE)
        self.assertIsNone(rule_id)
        self.assertEqual(new_messages, [])


class MetaRulesParseHandlerTest(unittest.TestCase):

    def setUp(self):
        self.builder = BasicRulesBuilder()
        self.parser = basic_director_handlers.MetaRuleParseHandler(
            self.builder)

        self.parser.next_handler = FakeHandler()

    def test_parse_meta_rule_definition(self):
        message = {
            "rule_definition": [
                {'type': 'integer'},
                {'type': 'string_of_unsigned_integers'}
            ],
            "parent_rule_id": None,
            "value": '123456789',
            "path": ""
        }
        rule_id, new_messages = self.parser.handle_message(message)
        self.assertEqual(rule_id, 0)
        self.assertIsInstance(new_messages, list)
        self.assertEqual(len(new_messages), 2)

    def test_parse_fake_message(self):
        rule_id, new_messages = self.parser.handle_message(
            FakeHandler.FAKE_MESSAGE)
        self.assertEqual(rule_id, FakeHandler.FAKE_RULE_ID)
        self.assertEqual(new_messages, [])

    def test_parse_unknown_message(self):
        self.parser.next_handler = None
        rule_id, new_messages = self.parser.handle_message(
            FakeHandler.FAKE_MESSAGE)
        self.assertIsNone(rule_id)
        self.assertEqual(new_messages, [])
