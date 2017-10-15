"""Structure of ABNFEarley grammars.

The following classes are provided to define the structure of and
programmatically create Grammars:
Grammar -- whole grammar consists of rules with names as left-hand sides
           and GrammarElements as right-hand side
GrammarElement is the abstract base class for all of these:
Alternation -- contains alternative GrammarElements
Concatenation -- contains concatenated GrammarElements
Repetition -- contains repeated GrammarElement with lower and upper
              bound
LiteralString --
CaseInsensitiveLiteralString --
LiteralRange --
RuleCall -- call of grammar rule from within right-hand side
"""
import os
from abc import ABCMeta, abstractmethod
from typing import Optional, Union, Sequence, Mapping, Iterator


class Grammar(Mapping[str, 'GrammarElement']):
    """Whole grammar consisting of named rules.

    A grammar consists of a mapping from names to GrammarElement
    instances (which can be arbitrarily nested Alternation,
    Concatenation, Repetition, literal and RuleCall instances).
    """

    __slots__ = ['_name', '_rules', '_imports']

    def __init__(self, name: str,
                 rules: Mapping[str, 'GrammarElement'],
                 imports: Sequence['Grammar'] = []) -> None:
        """Initialise with mapping from rule names to right-hand sides.

        Arguments:
        name -- name of the grammar to identify it to the user
        rules -- mapping from rule names to right-hand sides
        imports -- sequence of other grammars used in this one

        Note: While mutable mappings and sequences could be given as
        arguments, we assume that they are not mutated after
        initialisation.
        """
        self._name = name
        self._rules = rules
        self._imports = imports
        for rule, rhs in self._rules.items():
            rhs._register(self, rule, self)

    @property
    def name(self) -> str:
        """Get name of grammar."""
        return self._name

    def __getitem__(self, rule: str) -> 'GrammarElement':
        """Get rule from grammar or its imports."""
        if rule in self._rules:
            return self._rules[rule]
        for grammar in self._imports:
            if rule in grammar._rules:
                return grammar._rules[rule]
        raise KeyError("Rule '{}' not defined in grammar '{}'.".format(
            rule, self._name))

    def __iter__(self) -> Iterator[str]:
        """Iterate over rules and imported rules."""
        for rule in self._rules:
            yield rule
        for grammar in self._imports:
            for rule in grammar._rules:
                yield rule

    def __len__(self) -> int:
        """Total number of rules in grammar and imports."""
        length = len(self._rules)
        for grammar in self._imports:
            length += len(grammar._rules)
        return length

    def __eq__(self, other: object) -> bool:
        """Recursively check strict structural equality."""
        if not isinstance(other, Grammar):
            return False
        return (self._name == other._name and
                self._rules == other._rules and
                self._imports == other._imports)

    def __repr__(self, indent: int = 0) -> str:
        """Get evaluable representation."""
        result = indent * ' '
        result += 'abnfearley.Grammar({!r}, '.format(self._name)
        result += 'collections.OrderedDict(['
        first = True
        for rule, rhs in self._rules.items():
            if first:
                first = False
            else:
                result += ','
            result += os.linesep
            result += indent * ' '
            result += '    ({!r},'.format(rule) + os.linesep
            result += rhs.__repr__(indent + 5)
            result += ')'
        result += ']), ['
        first = True
        for grammar in self._imports:
            if first:
                first = False
            else:
                result += ','
            result += os.linesep
            result += grammar.__repr__(indent + 4)
        result += '])'
        return result

    def __str__(self) -> str:
        """Get ABNF representation."""
        result = '; ===== Grammar {!s} ====='.format(self._name)
        if self._imports:
            result += os.linesep
            result += '; uses rules from '
            result += ', '.join([g.name for g in self._imports])
        for rule, rhs in self._rules.items():
            result += os.linesep
            result += '{!s} = {!s}'.format(rule, rhs)
        return result


class GrammarElement(metaclass=ABCMeta):
    """Abstract base class for all kinds of grammar elements."""

    __slots__ = ['_parent', '_rule', '_grammar']

    def __init__(self) -> None:
        """Trivially initialise GrammarElement."""
        self._parent: Union['GrammarElement', Grammar, None] = None
        self._rule = ''
        self._grammar: Union[Grammar, None] = None

    def _location(self,
                  parent: Union['GrammarElement', Grammar, None] = None,
                  rule: str = '',
                  grammar: Union[Grammar, None] = None) -> str:
        if parent is None and hasattr(self, '_parent'):
            parent = self._parent
        if not rule and hasattr(self, '_rule'):
            rule = self._rule
        if grammar is None and hasattr(self, '_grammar'):
            grammar = self._grammar
        if isinstance(parent, Grammar):
            return "rule '{}' in grammar '{}'".format(rule, parent.name)
        elif isinstance(grammar, Grammar):
            return "{} in rule '{}' in grammar '{}'".format(
                type(parent), rule, grammar.name)
        return "unknown location"

    @abstractmethod
    def _register(self, parent: Union['GrammarElement', Grammar],
                  rule: str, grammar: Grammar) -> None:
        if hasattr(self, '_parent'):
            raise ValueError(
                '{} registered at {} is already registered at {}.'.format(
                    type(self),
                    self._location(parent, rule, grammar),
                    self._location()))
        self._parent = parent
        self._rule = rule
        self._grammar = grammar

    @property
    def parent(self) -> Union['GrammarElement', Grammar, None]:
        """Get parent element."""
        if not hasattr(self, '_parent'):
            return None
        return self._parent

    @property
    def rule(self) -> str:
        """Get name of rule containing element."""
        if not hasattr(self, '_rule'):
            return ''
        return self._rule

    @property
    def grammar(self) -> Union[Grammar, None]:
        """Get grammar containing element."""
        if not hasattr(self, '_grammar'):
            return None
        return self._grammar

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Recursively check strict structural equality."""
        raise NotImplementedError

    @abstractmethod
    def __repr__(self, indent: int = 0) -> str:
        """Get evaluable representation."""
        raise NotImplementedError

    @abstractmethod
    def __str__(self, needs_parens: bool = False) -> str:
        """Get ABNF representation."""
        raise NotImplementedError


class Alternation(GrammarElement, Sequence[GrammarElement]):
    """Alternation between GrammarElement instances.

    At least one of the alternatives has to match the input for the
    Alternation to match.
    """

    __slots__ = ['_elements']

    def __init__(self, elements: Sequence[GrammarElement]) -> None:
        """Initialise with sequence of alternatives.

        Argument:
        elements -- the alternatives

        Note: While a mutable sequence could be given as argument, we
        assume that it is not mutated after initialisation.
        """
        self._elements = elements

    def __getitem__(self, key):  # type: ignore
        """Get alternative(s) at index or slice key."""
        return self._elements[key]  # type: ignore

    def __len__(self) -> int:
        """Get number of alternatives."""
        return len(self._elements)

    def _register(self, parent: Union[GrammarElement, Grammar],
                  rule: str, grammar: Grammar) -> None:
        super()._register(parent, rule, grammar)
        for element in self._elements:
            element._register(self, rule, grammar)

    def __eq__(self, other: object) -> bool:
        """Recursively check strict structural equality."""
        if not isinstance(other, Alternation):
            return False
        return self._elements == other._elements

    def __repr__(self, indent: int = 0) -> str:
        """Get evaluable representation."""
        result = indent * ' '
        result += 'abnfearley.Alternation(['
        first = True
        for element in self._elements:
            if first:
                first = False
            else:
                result += ','
            result += os.linesep
            result += element.__repr__(indent + 4)
        result += '])'
        return result

    def __str__(self, needs_parens: bool = False) -> str:
        """Get ABNF representation."""
        if self._elements:
            if len(self._elements) == 1:
                return self._elements[0].__str__(needs_parens)
            result = ' / '.join(
                [element.__str__(True) for element in self._elements])
            if needs_parens:
                return '(' + result + ')'
            else:
                return result
        return '()'


class Concatenation(GrammarElement, Sequence[GrammarElement]):
    """Concatenation of GrammarElements instances.

    All contained elements have to match the input in order for the
    Concatenation to match.
    """

    __slots__ = ['_elements']

    def __init__(self, elements: Sequence[GrammarElement]) -> None:
        """Initialise with sequence of concatenated elements.

        Argument:
        elements -- the concatenated elements

        Note: While a mutable sequence could be given as argument, we
        assume that it is not mutated after initialisation.
        """
        self._elements = elements

    def __getitem__(self, key):  # type: ignore
        """Get concatenated element(s) at index or slice key."""
        return self._elements[key]  # type: ignore

    def __len__(self) -> int:
        """Get length of concatenation."""
        return len(self._elements)

    def _register(self, parent: Union[GrammarElement, Grammar],
                  rule: str, grammar: Grammar) -> None:
        super()._register(parent, rule, grammar)
        for element in self._elements:
            element._register(self, rule, grammar)

    def __eq__(self, other: object) -> bool:
        """Recursively check strict structural equality."""
        if not isinstance(other, Concatenation):
            return False
        return self._elements == other._elements

    def __repr__(self, indent: int = 0) -> str:
        """Get evaluable representation."""
        result = indent * ' '
        result += 'abnfearley.Concatenation(['
        first = True
        for element in self._elements:
            if first:
                first = False
            else:
                result += ','
            result += os.linesep
            result += element.__repr__(indent + 4)
        result += '])'
        return result

    def __str__(self, needs_parens: bool = False) -> str:
        """Get ABNF representation."""
        if self._elements:
            if len(self._elements) == 1:
                return self._elements[0].__str__(needs_parens)
            result = ' '.join(
                [element.__str__(True) for element in self._elements])
            if needs_parens:
                return '(' + result + ')'
            else:
                return result
        return '()'


class Repetition(GrammarElement):
    """Repetition of a GrammarElement instance.

    The contained element has to match at least lower times and at most
    upper times for the Repetition to match. If upper is None, it can
    match arbitrarily often.
    """

    __slots__ = ['_element', '_lower', '_upper']

    def __init__(self, element: GrammarElement,
                 lower: int = 0, upper: Optional[int] = None) -> None:
        """Initialise with repeated element and optionally bounds.

        Arguments:
        element -- the repeated element
        lower -- lower bound (defaults to 0)
        upper -- upper bound (defaults to unbound, represented by None)
        """
        self._element = element
        self._lower = lower
        self._upper = upper

    @property
    def element(self) -> GrammarElement:
        """Get repeated element."""
        return self._element

    @property
    def lower(self) -> int:
        """Get lower bound."""
        return self._lower

    @property
    def upper(self) -> Optional[int]:
        """Get upper bound."""
        return self._upper

    def _register(self, parent: Union[GrammarElement, Grammar],
                  rule: str, grammar: Grammar) -> None:
        super()._register(parent, rule, grammar)
        self._element._register(self, rule, grammar)

    def __eq__(self, other: object) -> bool:
        """Recursively check strict structural equality."""
        if not isinstance(other, Repetition):
            return False
        return (self._element == other._element and
                self._lower == other._lower and
                self._upper == other._upper)

    def __repr__(self, indent: int = 0) -> str:
        """Get evaluable representation."""
        result = indent * ' '
        result += 'abnfearley.Repetition('
        result += os.linesep
        result += self._element.__repr__(indent + 4)
        result += ',' + os.linesep + (indent + 4) * ' '
        result += repr(self._lower) + ', '
        result += repr(self._upper) + ')'
        return result

    def __str__(self, needs_parens: bool = False) -> str:
        """Get ABNF representation."""
        if self._lower == self._upper:
            if self._lower == 1:
                return self._element.__str__(needs_parens)
            elif self._lower > 1:
                return str(self._lower) + self._element.__str__(True)
        elif self._upper is None:
            if self._lower == 0:
                return '*' + self._element.__str__(True)
            else:
                return str(self._lower) + '*' + self._element.__str__(True)
        else:
            if self._upper == 1:
                return '[' + self._element.__str__(False) + ']'
            else:
                return (str(self._lower) + '*' + str(self._upper) +
                        self._element.__str__(True))
        return '()'


class LiteralString(GrammarElement):
    """Terminal literal string of grammar.

    The string is matched verbatim against the input.
    """

    __slots__ = ['_string', '_case_sensitive']

    def __init__(self, string: bytes, case_sensitive: bool = True) -> None:
        """Initialise with string to accept.

        Arguments:
        string -- the string of bytes to match
        case_sensitive -- whether the string should match case-sensitive
        """
        self._string = string
        self._case_sensitive = case_sensitive

    @property
    def string(self) -> bytes:
        """Get matched string of bytes."""
        return self._string

    @property
    def case_sensitive(self) -> bool:
        """Get case-sensitivity."""
        return self._case_sensitive

    def _register(self, parent: Union[GrammarElement, Grammar],
                  rule: str, grammar: Grammar) -> None:
        super()._register(parent, rule, grammar)

    def __eq__(self, other: object) -> bool:
        """Recursively check strict structural equality."""
        if not isinstance(other, LiteralString):
            return False
        return (self._string == other._string and
                self._case_sensitive == other._case_sensitive)

    def __repr__(self, indent: int = 0) -> str:
        """Get evaluable representation."""
        result = indent * ' '
        result += 'abnfearley.LiteralString('
        result += repr(self._string)
        if not self._case_sensitive:
            result += ', False'
        result += ')'
        return result

    def __str__(self, needs_parens: bool = False) -> str:
        """Get ABNF representation."""
        result = ''
        components = 0
        in_char_val = False
        in_hex_val = False
        for byte in self._string:
            if byte >= 0x20 and byte <= 0x7E and byte != 0x22:
                if in_hex_val:
                    result += ' '
                    in_hex_val = False
                if not in_char_val:
                    if self._case_sensitive:
                        result += '%s'
                    result += '"'
                    in_char_val = True
                    components += 1
                result += chr(byte)
            else:
                if in_char_val:
                    result += '" '
                    in_char_val = False
                if in_hex_val:
                    result += '.'
                else:
                    result += '%x'
                    in_hex_val = True
                    components += 1
                result += '{2X}'.format(byte)
        if in_char_val:
            result += '"'
            in_char_val = False
        if needs_parens and components != 1:
            result = '(' + result + ')'
        return result


class LiteralRange(GrammarElement):
    """Range of terminal literal bytes.

    The current byte of the string is matched against a range of bytes.
    """

    __slots__ = ['_first', '_last']

    def __init__(self, first: int, last: int) -> None:
        """Initialise with first and last byte of range.

        Arguments:
        first -- code of the first byte of the matched range
        last -- codef of the last byte of the matched range
        """
        self._first = first
        self._last = last

    @property
    def first(self) -> int:
        """Get code of first byte of matched range."""
        return self._first

    @property
    def last(self) -> int:
        """Get code of last byte of matched range."""
        return self._last

    def _register(self, parent: Union[GrammarElement, Grammar],
                  rule: str, grammar: Grammar) -> None:
        super()._register(parent, rule, grammar)

    def __eq__(self, other: object) -> bool:
        """Recursively check strict structural equality."""
        if not isinstance(other, LiteralRange):
            return False
        return (self._first == other._first and
                self._last == other._last)

    def __repr__(self, indent: int = 0) -> str:
        """Get evaluable representation."""
        result = indent * ' '
        result += 'abnfearley.LiteralRange('
        result += repr(self._first)
        result += ', '
        result += repr(self._last)
        result += ')'
        return result

    def __str__(self, needs_parens: bool = False) -> str:
        """Get ABNF representation."""
        result = '%x{2X}-{2X}'.format(self._first, self._last)
        return result


class RuleCall(GrammarElement):
    """Call to rule of the Grammar.

    The called rule has to match the input for the RuleCall to match.
    """

    __slots__ = ['_call']

    def __init__(self, call: str) -> None:
        """Initialise with name of called rule.

        Arguments:
        call -- the called rule
        """
        self._call = call

    @property
    def call(self) -> str:
        """Get called rule."""
        return self._call

    def _register(self, parent: Union[GrammarElement, Grammar],
                  rule: str, grammar: Grammar) -> None:
        super()._register(parent, rule, grammar)
        if self._call not in grammar:
            raise ValueError(
                "Called rule '{}' not defined in grammar {}.".format(
                    self._call, grammar.name))

    def __eq__(self, other: object) -> bool:
        """Recursively check strict structural equality."""
        if not isinstance(other, RuleCall):
            return False
        return self._call == other._call

    def __repr__(self, indent: int = 0) -> str:
        """Get evaluable representation."""
        result = indent * ' '
        result += 'abnfearley.RuleCall('
        result += repr(self._call)
        result += ')'
        return result

    def __str__(self, needs_parens: bool = False) -> str:
        """Get ABNF representation."""
        return self._call
