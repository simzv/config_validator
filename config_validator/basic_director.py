# To validate the values in the config data structure (config dictionary)
# there is a need for some callable that performs the action. But we don't want
# to hardcode the proccess of validation in a function or method.
# So the "true way" is to construct some oject, that can perform
# the validation, at runtime.
# A good approach is to use the OOP pattern 'Builder'.
# For more flexibility and loose coupling it is divided into two parts.
# Here we introduce the 'Director' class.


import basic_director_handlers


class BaseDirector(object):
    """Base class for director, that gets the 'rules_scheme' definition
    and builds validator callable with the use of some concrete builder.
    To make the director reusable, we do not hardcode requrements
    for config elements values, but use the 'rules_scheme' definition as an
    argument of director constructor.
    Should not be used directly."""
    def __init__(self, rules_scheme, builder):
        self._rules_scheme = rules_scheme
        self._builder = builder

    def build_rules_tree(self, value):
        """This is the main method of the director class. It should return
        config validator callable
        (possibly constructed with builder by rules scheme,
        but you can inherite from that class and even hardcode your own
        implementation)."""
        raise NotImplementedError()


# To make it easy to expand a number of types definitions in rules scheme,
# we do not hardcode them inside director class or it's subclasses.
# We use a system of rules definition parser classes, that works independently.
# A good way to implenet this independency is to use
# the OOP pattern 'Chain Of Responsibility'.

class HandledDirector(BaseDirector):

    """This director defines methods for mainipulating
    with it's chain of rules definition parsers. And it uses the handlers
    in the chain to construct the validator callable.
    It is a basic class and it's chain has no handlers.
    Should not be used directly. Define your own set of handlers and
    add them to the chain in a subclass of HandledDirector."""

    def __init__(self, rules_scheme, builder):
        super(HandledDirector, self).__init__(rules_scheme, builder)
        self._head_handler = None
        self._tail_handler = None

    def push_handler(self, handler):
        if self._head_handler is None:
            self._head_handler = handler
            self._tail_handler = handler
        else:
            handler.next_handler = self._head_handler
            self._head_handler = handler

    def append_handler(self, handler):
        if self._tail_handler is None:
            self._tail_handler = handler
            self._head_handler = handler
        else:
            self._tail_handler.next_handler = handler
            self._tail_handler = handler

    def pop_handler(self):
        if self._tail_handler is None:
            return None
        elif self._head_handler is self._tail_handler:
            handler = self._tail_handler
            self._head_handler = None
            self._tail_handler = None
            return handler
        else:
            handler = self._head_handler
            while handler.next_handler is not None:
                if handler.next_handler is self._tail_handler:
                    new_tail_handler = handler
                    handler = self._tail_handler
                    self._tail_handler = new_tail_handler
                    self._tail_handler.next_handler = None
                    return handler

    def shift_handler(self):
        if self._head_handler is None:
            return None
        elif self._head_handler is self._tail_handler:
            handler = self._head_handler
            self._head_handler = None
            self._tail_handler = None
            return handler
        else:
            handler = self._head_handler
            self._head_handler = self._head_handler.next_handler
            return handler

    def build_rules_tree(self, value):
        self._builder.clean()

        root_message = {
            'rule_definition': self._rules_scheme,
            'parent_rule_id': None,
            'value': value,
            'path': ''
        }

        messages_queue = [root_message]
        bad_messages = []

        while len(messages_queue) > 0:
            message = messages_queue.pop(0)
            rule_id, new_messages = self._head_handler.handle_message(message)

            if rule_id is None:
                # 'Oups! Non-parseble rule definition!'
                bad_messages.append(message)

            messages_queue.extend(new_messages)

        if len(bad_messages) > 0:
            error_msg = ('Got %d bad rules definitions in rules scheme.'
                         % len(bad_messages))
            raise ValueError(error_msg)

        return self._builder.get_product()


class BasicRulesDirector(HandledDirector):
    """Extended HandledDirector. It's handlers chain is filled
    with a set of basic rules definition parsers.
    It reflects a set of basic rules classes (or BasicRulesBuilder methods)."""

    def __init__(self, rules_scheme, builder):
        super(BasicRulesDirector, self).__init__(rules_scheme, builder)

        self.append_handler(
            basic_director_handlers.SimpleRuleParseHandler(self._builder))

        self.append_handler(
            basic_director_handlers.ListRuleParseHandler(self._builder))

        self.append_handler(
            basic_director_handlers.DictRuleParseHandler(self._builder))

        self.append_handler(
            basic_director_handlers.MetaRuleParseHandler(self._builder))

