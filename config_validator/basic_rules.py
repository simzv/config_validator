# To validate configuration dictionary,
# we need to validate each of it's components.
# More over, validation should be made not only on leaf elements,
# but also on all inner tree elements.
# To reflect the complexity of validation target,
# we will use complex structure of validation rules.
# Good aproach to implement this is to use OOP pattern 'Composite'.
# We will define simple and complex validation rules
# as components in terms of that pattern.


class Node(object):
    """Base component of Composite pattern.
    Shouldn't be used."""
    def __init__(self, value, path):
        """value is a subtree of config dict,
        that shuld be validated by this rule (Node instance)."""
        self.value = value
        self.path = path
        self.errors = []

    def validate(self):
        raise NotImplementedError()

    def add_child(self, node):
        raise NotImplementedError()

    def remove_child(self, node):
        raise NotImplementedError()

    def get_all_errors(self):
        if self.errors:
            return self.errors
        else:
            return None


class IntegerNode(Node):
    """Simple rule, to validate integer values."""
    def validate(self):
        if not type(self.value) == int:
            self.errors.append("Config Error at %s : value must be integer."
                               % self.path)
        return not self.errors


class BooleanNode(Node):
    """Simple rule, to validate boolean values."""
    def validate(self):
        if not isinstance(self.value, bool):
            self.errors.append("Config Error at %s : value must be boolean."
                               % self.path)
        return not self.errors


class StringNode(Node):
    """Simple rule, to validate string values."""
    def validate(self):
        if not isinstance(self.value, basestring):
            self.errors.append("Config Error at %s : value must be string."
                               % self.path)
        return not self.errors


class NotEmptyStringNode(StringNode):
    """Simple rule, to validate non-empty string values."""
    def validate(self):
        super(NotEmptyStringNode, self).validate()
        if not self.errors and len(self.value) == 0:
            self.errors.append("Config Error at %s : value must "
                               "be not empty string." % self.path)
        return not self.errors


class StringOfUnsignedInteger(NotEmptyStringNode):
    """Simple rule, to validate strings of unsigned integer values."""
    def validate(self):
        super(StringOfUnsignedInteger, self).validate()
        if not self.errors and not self.value.isdigit():
            self.errors.append("Config Error at %s : value must be not empty"
                               " string representing unsigned integer."
                               % self.path)
        return not self.errors


class CompositeNode(Node):
    """Base complex rule: a 'composite' in terms of 'Composite pattern'.
    Shouldn't be used directly."""
    def __init__(self, value, path):
        super(CompositeNode, self).__init__(value, path)
        self._children = set()

    def add_child(self, node):
        self._children.add(node)

    def remove_child(self, node):
        self._children.discard(node)

    def validate(self):
        """This rule returns 'ok',
        if all of it's inner rules also returns 'ok'."""
        valid_children = True
        for node in self._children:
            valid_children = node.validate() and valid_children
        if not valid_children:
            self.errors.append("Config Error at %s : each of nested values"
                               " must be valid." % self.path)

        return not self.errors

    def get_all_errors(self):
        errors = []
        if self.errors:
            errors += self.errors
        for child in self._children:
            child_errors = child.get_all_errors()
            if child_errors:
                errors += child_errors
        if errors:
            return errors
        else:
            return None


# To reduce the number of classes for complex rules,
# we define only a few general complex rules' classes,
# that can be parametrized by their attributes.
# It is better to declare the rules scheme, than to develop many new classes.
# Parameters should be set properly during the construction of rules tree.


class ListNode(CompositeNode):
    """Complex rule, to validate a list of inner rules."""
    def __init__(self, value, path):
        super(ListNode, self).__init__(value, path)
        self.min_length = None
        self.max_length = None

    def validate(self):
        """This rule returns 'ok', if:
         - the number of list items is between min_length and max_length;
         - all child rules, for all elements of value-list returns 'ok'."""

        if not isinstance(self.value, list):
            self.errors.append("Config Error at %s : value must be list."
                               % self.path)
        else:
            if self.min_length is not None and len(self.value) < self.min_length:
                self.errors.append("Config Error at %s : the value must have "
                                   "at list %d items."
                                   % (self.path, self.min_length))

            if self.max_length is not None and len(self.value) > self.max_length:
                self.errors.append("Config Error at %s : the value must have "
                                   "not more than %d items."
                                   % (self.path, self.max_length))

        if not self.errors:
            super(ListNode, self).validate()

        return not self.errors


class DictNode(CompositeNode):
    """Complex rule, to validate a dictionary of inner rules."""
    def __init__(self, value, path):
        super(DictNode, self).__init__(value, path)
        self.mandatory_keys = set()
        self.optional_keys = set()
        self.strict_keys_set = True

    def validate(self):
        """This rule is 'ok', if:
        - all mandatory keys exists in value;
        - there is no unknown keys (not in mandatory or optional),
        if they are on allowed,
        - all rules for all keys says 'ok'."""
        if not isinstance(self.value, dict):
            self.errors.append("Config Error at %s : value must be dictionary."
                               % self.path)
        else:
            dict_keys = set(self.value.keys())
            missed_keys = self.mandatory_keys.difference(dict_keys)
            if len(missed_keys) > 0:
                self.errors.append("Config Error at %s :"
                                   " missing key(s): %s."
                                   % (self.path, list(missed_keys)))

            if self.strict_keys_set:
                valid_keys_set = self.mandatory_keys.union(self.optional_keys)
                unknown_keys = dict_keys.difference(valid_keys_set)
                if len(unknown_keys) > 0:
                    self.errors.append("Config Error at %s :"
                                       " unknown key(s): %s."
                                       % (self.path, list(unknown_keys)))

        if not self.errors:
            super(DictNode, self).validate()

        return not self.errors


class MetaNode(CompositeNode):
    """Complex rule, to validate a set of alternative rules.
    Should be used carefully.
    Child rules are treated as alternatives to each other.
    Each child rule should validate the same value: the parent's value."""
    def __init__(self, value, path):
        super(MetaNode, self).__init__(value, path)

    def validate(self):
        """Validation mechanism fully replaces the baseclass validatioin logic.
        In case of alternative rules, this rule is 'ok',
        if even one of alternatives says 'ok'."""
        is_valid = False
        for alternate in self._children:
            valid_alternate = alternate.validate()
            is_valid = is_valid or valid_alternate

        if not is_valid:
            self.errors.append("Config Error at %s : All allowed alternatives "
                               "are not valid." % self.path)

        return is_valid

    def get_all_errors(self):
        # Almost like at the base class, but showing errors only if
        # all alternatives are not valid (in this case validate() on meta-node
        # will add error to self).
        errors = []
        if self.errors:
            errors += self.errors
            for child in self._children:
                child_errors = child.get_all_errors()
                if child_errors:
                    errors += child_errors
        if errors:
            return errors
        else:
            return None
