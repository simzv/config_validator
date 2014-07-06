***********************************
Config Validator Documentation.
***********************************

1. Usage.
===================================
TODO: *to be wriiten later*
see 'example.py'


2. Extend HowTo.
===================================

Config validator design allows to extend it's functionality in many ways
at a number of abstraction levels. You can append some rules, checks,
definitions and etc.; or completely replace any of the validator's subsystems.
Near you can find a number of howtos describing common options.

2.1. Add checks for new value type.
-----------------------------------

By default config validator is built on basic rules, builder, director
and director handlers. To define checks for the new value type you should
perform few modifications at all of these layers.

Let's assume that you want to add checks for positive integer values.

First of all you should define a new rule - the subclass of 'basic_rules.Node'
class or it's subclasses. If you want to define complex value type, that may
contain nested values, that also should be checked, then you need to subclass
the 'basic_rules.CompositeNode'. For example::

    class PositiveIntegerNode(IntegerNode):
        def validate(self):
            super(PositiveIntegerNode, self).validate()
            if not self.errors and self.value =< 0:
                self.errors.append("Config Error at %s : value must be"
                                   " positive integer." % self.path)
            return not self.errors

**Note** the usage of 'path' in error message string template.

Next you should make a builder to know your new rule. Define new rules builder
mixin and new builder as a combination of basic rules builder mixin
and your own::

    class PositiveIntegerRuleBuilderMixin(RulesBuilderMixIn):
        def build_positive_integer(self, value, parent_id, path=''):
            rule = PositiveIntegerNode(value, path)
            return self._add_new_rule(rule, parent_id)


    class MyCustomRulesBuilder(RulesBuilder,
                               BasicRulesBuilderMixIn,
                               PositiveIntegerRuleBuilderMixIn)
        pass

**Note** that you can forget about basic rules completely and define your own
set of rules and rules builder mixin faced to them, and create your own
builder without basic rules builder mixin.

Now you have to invent the syntax of rule definition: how you will define your
rule in rules schema. Let's assume it will be simple::

    {
        'type': 'positive_integer'
    }

Then you have to create a parse handler, that will parse you new syntax::

    class PositiveIntegerRuleParseHandler(RuleParseHandler):

        def handle_maessage(self, message):
            if (isinstance(message['rule_definition'], dict)
                    and 'type' in message['rule_definition']):

                rule_id = self.builder.build_positive_integer(
                    message['value'],
                    message['parent_rule_id'],
                    message['path'] if message['path'] else '/'
                )
                return rule_id, []

            return super(PositiveIntegerRuleParseHandler,
                         self).handle_message(message)

**Note** that you use here your own builder method. And **do not forget to**
**call superclass' method by default**.

When you already have a rule, a builder and a rule definition parser, then
create new director subclass::

    class ExtendedRulesDirector(BasicRulesDirector):

        def __init__(self, rules_scheme, builder):
            super(BasicRulesDirector, self).__init__(rules_scheme, builder)

            self.append_handler(PositiveIntegerRuleParseHandler(self._builder))

**Note** that there is a call to superclass' constructor, which appends basic
rule's definition's parsers to the director. It is not mandatory: you can add
them (posibly not all if you want) explicitly, or shift or pop some of them
away... or subclass from HandledDirector and use a custom set of parse
handlers...

And that is all! Next you should just use your new director configured with
your new builder.
