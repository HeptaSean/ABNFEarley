# Grammars in _ABNFEarley_
Grammars in _ABNFEarley_ consist of a set of rules, where each rule has
a name (its left-hand side) and a right-hand side.
The right-hand side can consist of different kinds of grammar elements:
- Alternations: One of a set of alternatives is produced.
- Concatenations: A sequence of grammar elements is produced in order.
- Repetition: A grammar element is produced repeatedly.
- Literal String: A string of bytes is produced verbatim.
- Literal Range: One byte from a given range is produced.
- Rule Call: The right-hand side of another rule is produced.

Grammars are implemented by the module `abnfearley.grammar`, which
contains a class `Grammar` to represent the whole grammar and a
hierarchy of grammar elements with the abstract base class
`GrammarElement`.
The classes extending `GrammarElement` are `Alternation`,
`Concatenation`, `Repetition`, `LiteralString`, `LiteralRange`, and
`RuleCall`.

## Creation of Grammars
All of these classes are designed in an “immutable” way.
They are fully configured by their initialisation methods and do not
have setters or other methods to later modify the objects.
The rationale here is that grammars do not change in their lifetime, but
are by nature rather static entities.
They should either be initialised programmatically in code or be
constructed from an ABNF file (this possibility will be discussed
later).

A `Grammar` instance consists of a name, a set of named rules and
optionally imports some other `Grammar` instances.
More specifically, the name has to be an instance of `str`, the
rules have type `Mapping[str, GrammarElement]` and the imports
`Sequence[Grammar]`.
The name can be retrieved again by a read-only property `name`, while
the rules of the grammar itself and all of its imports can be queried,
retrieved, and iterated over with the standard mechanisms for
`dict`-like objects, i.e., `Grammar` itself extends
`Mapping[str, GrammarElement]`.

The initialisations of `Alternation` and `Concatenation` get arguments
of type `Sequence[GrammarElement]` in the constructor and both also
extend `Sequence[GrammarElement]` to retrieve and iterate the contained
elements.
For `Alternation`, the contained elements are the alternatives, while
for `Concatenation`, they are the concatenated elements.

For `Repetition`, the initialisation has the repeated `GrammarElement`
instance as required argument and the lower and upper bound as optional
arguments, where the lower bound is an integer and the upper bound is an
integer or `None` to represent arbitrary many repetitions.
The defaults are 0 as lower bound and `None` as upper bound.
Grammar element, lower and upper bound can be retrieved by the read-only
properties `element`, `lower`, and `upper`.

The constructor of `LiteralString` gets the string itself, a `bytes`
object, as argument.
The second argument `case_sensitive` is an optional Boolean defaulting
to `True`, which allows the string to be matched to the input without
taking the case into account.
The contained byte string can be retrieved by the read-only property
`string` and the case sensitivity by the property `case_sensitive`.

The `LiteralRange` initialisation has two integers, the first and last
byte of the range, as arguments.
They can be retrieved with the read-only `first` and `last` properties.

`RuleCall` initialisations have the name of the called rule as a string
as the only argument, which can later be retrieved by the read-only
`call` property.
When a `RuleCall` object is registered inside a grammar, the
registration checks if the called rule is, in fact, either defined or
imported by the grammar.
If this is not the case, a `ValueError` is raised in the recursive
registration phase of the `Grammar` constructor.

- [ ] Example grammar
- [ ] Unit tests

```python
>>> import abnfearley
>>> import collections
>>> example = abnfearley.Grammar('example', collections.OrderedDict([
...    ('example',
...     abnfearley.Alternation([
...         abnfearley.RuleCall('abccdd'),
...         abnfearley.RuleCall('abbccd')])),
...    ('abccdd',
...     abnfearley.Concatenation([
...         abnfearley.RuleCall('ab'),
...         abnfearley.RuleCall('cd')])),
...    ('ab',
...     abnfearley.Concatenation([
...         abnfearley.LiteralString(b'a'),
...         abnfearley.Repetition(
...             abnfearley.RuleCall('ab'),
...             0, 1),
...         abnfearley.LiteralString(b'b')])),
...    ('cd',
...     abnfearley.Concatenation([
...         abnfearley.LiteralString(b'c'),
...         abnfearley.Repetition(
...             abnfearley.RuleCall('cd'),
...             0, 1),
...         abnfearley.LiteralString(b'd')])),
...    ('abbccd',
...     abnfearley.Concatenation([
...         abnfearley.LiteralString(b'a'),
...         abnfearley.Alternation([
...             abnfearley.RuleCall('abbccd'),
...             abnfearley.RuleCall('bc')]),
...         abnfearley.LiteralString(b'd')])),
...    ('bc',
...     abnfearley.Concatenation([
...         abnfearley.LiteralString(b'b'),
...         abnfearley.Repetition(
...             abnfearley.RuleCall('bc'),
...             0, 1),
...         abnfearley.LiteralString(b'c')]))]), [])

```

## Serialisation of Grammars
All grammar objects implement the `repr()` functionality in such a way
that `eval(repr(g)) == g`, i.e., they return a string with a constructor
call that recreates the object.
On the other hand, the conversion to a string by `str()` is implemented
in such a way that a valid ABNF grammar is constructed.

- [ ] `repr`, `eval(repr(g))` and `str` of example grammar
- [ ] Unit tests

```python
>>> example
abnfearley.Grammar('example', collections.OrderedDict([
    ('example',
     abnfearley.Alternation([
         abnfearley.RuleCall('abccdd'),
         abnfearley.RuleCall('abbccd')])),
    ('abccdd',
     abnfearley.Concatenation([
         abnfearley.RuleCall('ab'),
         abnfearley.RuleCall('cd')])),
    ('ab',
     abnfearley.Concatenation([
         abnfearley.LiteralString(b'a'),
         abnfearley.Repetition(
             abnfearley.RuleCall('ab'),
             0, 1),
         abnfearley.LiteralString(b'b')])),
    ('cd',
     abnfearley.Concatenation([
         abnfearley.LiteralString(b'c'),
         abnfearley.Repetition(
             abnfearley.RuleCall('cd'),
             0, 1),
         abnfearley.LiteralString(b'd')])),
    ('abbccd',
     abnfearley.Concatenation([
         abnfearley.LiteralString(b'a'),
         abnfearley.Alternation([
             abnfearley.RuleCall('abbccd'),
             abnfearley.RuleCall('bc')]),
         abnfearley.LiteralString(b'd')])),
    ('bc',
     abnfearley.Concatenation([
         abnfearley.LiteralString(b'b'),
         abnfearley.Repetition(
             abnfearley.RuleCall('bc'),
             0, 1),
         abnfearley.LiteralString(b'c')]))]), [])
>>> eval(repr(example)) == example
True
>>> print(example)
; ===== Grammar example =====
example = abccdd / abbccd
abccdd = ab cd
ab = %s"a" [ab] %s"b"
cd = %s"c" [cd] %s"d"
abbccd = %s"a" (abbccd / bc) %s"d"
bc = %s"b" [bc] %s"c"

```

## Static Analysis methods

- [ ] `is_nullable`, `has_first_byte`, `max_literal_length`
- [ ] Implementation
- [ ] Documentation and example
- [ ] Unit tests

## Normalisation of Grammars
The `is_normalised()` method of a grammar or grammar element recursively
checks if there are superfluous structures, e.g., an alternation as
direct child alternative of another alternation, a concatenation with
only one element, or a repetition with 1 as lower as well as upper
bound.
The `normalise()` method of a grammar or grammar element returns a
normalised equivalent.

More specifically, the different kinds of grammar elements are
normalised as follows:

Nested alternations and nested concatenations are flattened.
The elements in these flattened lists are recursively normalised and
discarded if the normalisation returns `None`.
If only one element remains, the (in this case trivial) alternation or
concatenation is discarded and the single element is returned.
If no contained element remains at all, the alternation or concatenation
is completely discarded and `None`  is returned.

Repetitions with 1 as lower as well as upper bound are discarded and the
normalisation of the repeated element is returned.
Repetitions with 0 as lower as well as upper bound are completely
discarded and `None` is returned.

If a repetition is contained in another repetition, we need to analyse
their relation more closely:
For example, `Repetition(Repetition(el, 2, 2), 1, 3)` cannot be
flattened, since the requirement of exactly 2, 4 or 6 repetitions of
`el` cannot be expressed with a flat `Repetition` instance.

- [ ] Normalisation implementation
- [ ] Normalisation example
- [ ] Unit tests

## Class Constant for ABNF Grammar
The grammar of ABNF grammars themselves will later be used to construct
`Grammar` instances from files or strings.
In order to have it available, we define it as a class constant.

- [ ] Add constants for `CORE` and `ABNF`
- [ ] Discuss different variants of ABNF
