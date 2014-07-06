# To validate the values in the config data structure (config dictionary)
# there is a need in some callable that performs the action. But we don't want
# to hardcode the proccess of validation in a function or method.
# So the "true way" is to construct some oject, that can perform
# the validation, at runtime.
# A good approach is to use the OOP pattern 'Builder'.
# For more flexibility and loose coupling it is divided into two parts.
# Here we introduce the 'Builder' class.

import basic_rules


class BaseBuilder(object):

    """The simplest and therefore base builder class.
    Shouldn't be used directly.
    You can difine your own builer inherited from that class and even hardcode
    the construction of 'rules validator' in 'get_product()' mathod."""

    def get_product(self):
        """Method should return the callable - 'rules validator'"""
        raise NotImplementedError()


class RulesBuilder(BaseBuilder):

    """Template class for builder that constructs a validation callable
    as a heirarchy of simple objects
    (posssible use of 'composite' OOP pattern).
    It operates with 'rule_id's, Rule id is a way to define a parent object
    when adding a new rule to the heirarchy.
    Should not be used directly.
    You may inherite from this class, if you don't want to work
    with basic rules subsystem, but still want to construct rules validator
    as a heirarchy of your own objects."""

    def __init__(self):
        self._rules_list = []

    def _add_new_rule(self, rule, parent_id):
        self._rules_list.append(rule)
        if parent_id is not None and parent_id < len(self._rules_list):
            self._rules_list[parent_id].add_child(rule)

        rule_id = len(self._rules_list) - 1
        return rule_id

    def clean(self):
        self._rules_list = []

    def get_product(self):
        if len(self._rules_list) > 0:
            product = self._rules_list[0]
        else:
            product = None
        return product


class RulesBuilderMixIn(object):

    """Rules builder mixin class, Use it's subclasses to implement your own
    builder mixins and construct your own rules builder as a combination of
    builder mixins. Rules builder mixins should contain methods for building
    the corresponding rule node object."""

    def _add_new_rule(self, rule, parent_id):
        raise NotImplementedError()


class BasicRulesBuilderMixIn(RulesBuilderMixIn):

    """A collection of build methods that reflects basic rules.
    All of that build methods gets 'parent rule_id' and a 'path' for
    the new rule object as arguments and returns its rule id.
    Path is just a string for out in error messages, it helps to find
    invalid element in config data structure."""

    def build_integer(self, value, parent_id, path=''):
        rule = basic_rules.IntegerNode(value, path)
        return self._add_new_rule(rule, parent_id)

    def build_boolean(self, value, parent_id, path=''):
        rule = basic_rules.BooleanNode(value, path)
        return self._add_new_rule(rule, parent_id)

    def build_string(self, value, parent_id, path=''):
        rule = basic_rules.StringNode(value, path)
        return self._add_new_rule(rule, parent_id)

    def build_string_of_unsigned_integers(self, value, parent_id, path=''):
        rule = basic_rules.StringOfUnsignedInteger(value, path)
        return self._add_new_rule(rule, parent_id)

    def build_not_empty_string(self, value, parent_id, path=''):
        rule = basic_rules.NotEmptyStringNode(value, path)
        return self._add_new_rule(rule, parent_id)

    def build_dictionary(self, value, parent_id,
                         mandatory_keys=set(),
                         optional_keys=set(),
                         strict_keys_set=True, path=''):
        rule = basic_rules.DictNode(value, path)
        rule.mandatory_keys = mandatory_keys
        rule.optional_keys = optional_keys
        rule.strict_keys_set = strict_keys_set
        return self._add_new_rule(rule, parent_id)

    def build_list(self, value, parent_id, min_length=None,
                   max_length=None, path=''):
        rule = basic_rules.ListNode(value, path)
        rule.min_length = min_length
        rule.max_length = max_length
        return self._add_new_rule(rule, parent_id)

    def build_meta_rule(self, value, parent_id, path=''):
        rule = basic_rules.MetaNode(value, path)
        return self._add_new_rule(rule, parent_id)


class BasicRulesBuilder(RulesBuilder, BasicRulesBuilderMixIn):

    """A concrete builder implementation. This builder class is faced to
     basic rules classes."""

    pass
