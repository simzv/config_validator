# To make it easy to expand a number of types definitions in rules scheme,
# we do not hardcode them inside director class or it's subclasses.
# We use a system of rules definition parser classes, that works independently.
# A good way to implenet this independency is to use
# the OOP pattern 'Chain Of Responsibility'.
# This file contains implementations of basic rules definition parsers -
# chain messages handlers.


class RuleParseHandler(object):
    """Base rule definition parser class. It is condfigured with builder via
    a constructor argument. And it also can have a 'next' handler
    in the 'chain of responsibility'. It has a base 'handle_message' method."""

    def __init__(self, builder):
        self.builder = builder
        self.next_handler = None

    def handle_message(self, message):
        """Base handle message method. It doesn't handle message by it's own,
        but tries to redirect message to the next handler in the chain.
        If there is no next handler, it returns 'None' rule_id as a mark,
        that message has not been handled.
        It also return a list of 'new messages' (empty by default),
        that is used when constructing nested rules validators."""
        if self.next_handler:
            return self.next_handler.handle_message(message)
        else:
            return None, []


class SimpleRuleParseHandler(RuleParseHandler):
    """Rules definitions parser for simple rules types.
    These rules definition do not contain nested definitions,
    and use simple builder's methods, that have the same arguments list."""

    def handle_message(self, message):
        if (isinstance(message['rule_definition'], dict)
                and 'type' in message['rule_definition']):

            rule_type = message['rule_definition']['type']
            if rule_type in ('integer', 'string', 'not_empty_string',
                             'string_of_unsigned_integers', 'boolean'):
                build_method = getattr(self.builder, 'build_' + rule_type)
                if build_method and callable(build_method):
                    rule_id = build_method(message['value'],
                                           message['parent_rule_id'],
                                           message['path'] if message['path'] else '/')
                    return rule_id, []

        return super(SimpleRuleParseHandler, self).handle_message(message)


class ListRuleParseHandler(RuleParseHandler):
    """Rule definition parser, that recognizes definition of validation rules
     for values of the 'list' type.
     List value rule's definition may contain nested rules definitions."""

    def handle_message(self, message):
        if (isinstance(message['rule_definition'], dict)
                and 'type' in message['rule_definition']
                and message['rule_definition']['type'] == 'list'):

            rule_id = self.builder.build_list(
                message['value'],
                message['parent_rule_id'],
                min_length=message['rule_definition'].get('min_length'),
                max_length=message['rule_definition'].get('max_length'),
                path=message['path'] if message['path'] else '/'
            )

            new_messages = []

            if isinstance(message['value'], list):
                inner_index = 0

                for inner_value in message['value']:

                    newpath = message['path'] + "/" + str(inner_index)

                    inner_rule_definition = message['rule_definition']\
                        .get('allowed')

                    if inner_rule_definition is not None:
                        new_messages.append({
                            'value': inner_value,
                            'rule_definition': inner_rule_definition,
                            'parent_rule_id': rule_id,
                            'path': newpath,
                        })
                        inner_index += 1

            return rule_id, new_messages

        return super(ListRuleParseHandler, self).handle_message(message)


class DictRuleParseHandler(RuleParseHandler):
    """Rule definition parser, that recognizes definition of validation rules
     for values of the 'dictionary' type.
     Dict value rule's definition may contain nested rules definitions."""

    def handle_message(self, message):

        if (isinstance(message['rule_definition'], dict)
                and 'type' in message['rule_definition']
                and message['rule_definition']['type'] == 'dictionary'):

            mandatory = message['rule_definition'].get('mandatory', {})
            mandatory_keys = set(mandatory.iterkeys())

            optional = message['rule_definition'].get('optional', {})
            optional_keys = set(optional.iterkeys())

            strict_keys = message['rule_definition']\
                .get('strict_keys_set', True)

            rule_id = self.builder.build_dictionary(
                message['value'],
                message['parent_rule_id'],
                mandatory_keys=mandatory_keys,
                optional_keys=optional_keys,
                strict_keys_set=strict_keys,
                path=message['path'] if message['path'] else '/')

            new_messages = []

            if isinstance(message['value'], dict):

                for key in message['value']:

                    if key in mandatory:
                        inner_rule_definition = mandatory[key]

                    elif key in optional:
                        inner_rule_definition = optional[key]

                    elif not strict_keys:
                        inner_rule_definition = message['rule_definition']\
                            .get('allowed')

                    else:
                        inner_rule_definition = None

                    if inner_rule_definition is not None:
                        newpath = message['path'] + '/' + key

                        new_messages.append({
                            'value': message['value'][key],
                            'rule_definition': inner_rule_definition,
                            'parent_rule_id': rule_id,
                            'path': newpath
                        })

            return rule_id, new_messages

        return super(DictRuleParseHandler, self).handle_message(message)


class MetaRuleParseHandler(RuleParseHandler):
    """Rule definition parser, that recognizes definition of 'meta' rules.
    'Meta' rule's definition may contain nested rules definitions."""

    def handle_message(self, message):
        if isinstance(message['rule_definition'], list):
            # meta rule: a list of alternative rules
            rule_id = self.builder.build_meta_rule(
                message['value'],
                message['parent_rule_id'],
                message['path'] if message['path'] else '/')

            new_messages = []

            index = 1
            for inner_rule_definition in message['rule_definition']:
                new_messages.append({
                    'value': message['value'],
                    'rule_definition': inner_rule_definition,
                    'parent_rule_id': rule_id,
                    'path': message['path'] + ('(alt.#%d)' % index)
                })
                index += 1

            return rule_id, new_messages

        return super(MetaRuleParseHandler, self).handle_message(message)
