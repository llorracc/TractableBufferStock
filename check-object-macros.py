#!/usr/bin/env python3
"""Fail any object in the handout's math that isn't written with its own macro (rule D).

Rule D, Chris Carroll, 2026-11-15 10:16:51 EST (typed in the workspace-course-choice session): "I want you to ensure
that the handouts/chapters always use the macro for the object, rather than writing it in plain latex; e.g., there
should never be simply "$C$" but instead "$\\CLvl$" etc". So every symbol in math that names an economic object is
written with its macro: the registry's (@resources/notation), or @local's for an object the registry lacks. The print
is then decided in one place, the macro's definition.

Two checks:

- **A raw letter that names an object.** A raw letter may stay only where it names no object (a date, an index,
  Euler's e, the differential d, an operator, the generic variables of a math fact) or is a throwaway letter (Chris,
  2026-11-11: a regression's or a fitted function's coefficients, a small perturbation). ALLOWED lists each, with
  where it is allowed and why.
- **A function's macro used as a number:** a \\xFunc or \\XFunc with a date subscript and no argument, as in
  \\VFunc_{t}. The function's macro names the function; the number is another object, with a macro of its own. Chris,
  2026-11-15 10:45:09 EST, of value: "It can be \\vLvl_{t} or \\VLvl_{t} but \\vFunc_{t} is the value function always
  and everywhere (nonitalic roman)". A function named with its date, not used as a number, goes in FUNC_ALLOWED.

HELD and FUNC_HELD list what waits for a decision of Chris's; it is reported, and doesn't fail the check. An entry of
any list that no longer matches anything fails it, so the lists can't go stale.

    ./check-object-macros.py            check TractableBufferStock.tex
    ./check-object-macros.py FILE ...   check other files

Math is $...$, \\(...\\), \\[...\\], \\ensuremath{...} and the equation environments; inside it, the arguments of
\\text, \\label, \\mathtt and the like are not math. Comments, comment environments and everything after
\\end{document} don't print, so they are skipped. A letter is a Latin letter, or a Greek or Hebrew letter written
with its command; \\nabla counts too, since this handout once wrote an object with it.

Exit status: 0 nothing to fix, 1 something to fix.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = ['TractableBufferStock.tex']

# Raw letters. (letter, where it may stay raw, why). Where: a pattern searched near the letter, which is marked
# [[ ]]; None for anywhere.
ALLOWED = [
    ('t', None, 'the date'),
    ('i', None, 'an index: a country, in the cross-country regression'),
    ('n', None, 'an index: periods back from the target, in reverse shooting'),
    ('N', r'\[\[N\]\]\]|\$\[\[N\]\]\$ is the number of points', "an index's bound: the number of grid points, as in"
     ' m[N]'),
    ('d', r'\[\[d\]\]\s*\\', 'the differential, as in d\\cFunc'),
    ('e', r'\[\[e\]\]\s*\^', "Euler's e, raised to a power"),
    ('C', r'\\mathbf\{\[\[C\]\]\}\^4', 'the class of functions with four continuous derivatives'),
    ('x', r'\\uFunc\((\[\[)?x(\]\])?(\[\[)?y(\]\])?\)', 'the generic variables of a property of CRRA utility'),
    ('y', r'\\uFunc\((\[\[)?x(\]\])?(\[\[)?y(\]\])?\)', 'the generic variables of a property of CRRA utility'),
    ('\\Delta', None, 'the difference operator, like the differential d'),
    ('\\eta', r'\[\[\\eta\]\]_\{[01]\}', "a regression's coefficients: throwaway letters"),
    ('\\epsilon', r'\[\[\\epsilon\]\]_\{i\}', "a regression's error: a throwaway letter"),
    ('\\epsilon', r'\(1\+(\[\[)?\\epsilon(\]\])?\)\^\{(\[\[)?\\zeta(\]\])?\}', "the generic variables of the Math Facts'"
     ' Taylor approximations'),
    ('\\zeta', r'\(1\+(\[\[)?\\epsilon(\]\])?\)\^\{(\[\[)?\\zeta(\]\])?\}', "the generic variables of the Math Facts'"
     ' Taylor approximations'),
    ('\\phi', r'\[\[\\phi\]\]_\{[01]\}', "a fitted function's coefficients: throwaway letters"),
    ('\\gamma', r'\[\[\\gamma\]\]_\{[01]\}', "a fitted function's coefficients: throwaway letters"),
    ('\\phi', r'\$(\[\[)?\\(phi|gamma)(\]\])?\$ and \$(\[\[)?\\(phi|gamma)(\]\])?\$', "the fitted function's"
     ' coefficients, named in the text'),
    ('\\gamma', r'\$(\[\[)?\\(phi|gamma)(\]\])?\$ and \$(\[\[)?\\(phi|gamma)(\]\])?\$', "the fitted function's"
     ' coefficients, named in the text'),
    ('\\varepsilon', r'\\pmb\{\\circ\}\(-?\[\[\\varepsilon\]\]\)', 'a small perturbation: a throwaway letter'),
]

# (letter, where, why it waits): raw object letters left for a decision of Chris's, which the macro would anticipate.
HELD = [
    ('C', r'\\uFunc\(\[\[C\]\]_\{t', "the unemployed consumer's consumption, a level: levels wait for Chris's levels"
     ' decision'),
    ('c', r'\\tilde\{\\mathbf\{\[\[c\]\]\}\}', "reverse shooting's approximation to the consumption function, a bold c:"
     ' its macro, \\cFunc, prints an upright c (a symbol batch)'),
    ('c', r'Aggregate \$\[\[c\]\]\$', "aggregate consumption, in two figures' captions: the registry's aggregate prints"
     ' a capital (a symbol batch)'),
]

# Functions' macros used as numbers. (macro, where, why): the macro, as a pattern; where, a pattern searched in the
# math around it (its whole equation).
FUNC_ALLOWED = []
FUNC_HELD = [
    (r'\\VFunc', r'_\{\\equiv \\vMultUnemp\}', "the unemployed consumer's value at t, a level: \\vLvl_{t}^{\\UnempLbl}"
     " with the levels decision, which the equation's raw C waits for too"),
    (r'\\cFunc|\\MPCFunc', r'\\label\{eq:kappaP(Expr|Reverse)\}', "c and kappa written as their functions in the"
     " consumption function's curvature (Numerical Solution), whose numbers' macros print an italic c and a plain"
     ' kappa (a symbol batch); the section goes to its notebook at the split'),
]

GREEK = set('alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa varkappa lambda mu nu xi '
            'pi varpi rho varrho sigma varsigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi '
            'Sigma Upsilon Phi Psi Omega varGamma varDelta varTheta varLambda varXi varPi varSigma varUpsilon varPhi '
            'varPsi varOmega aleph beth gimel daleth ell mho eth nabla'.split())
MATH_ENVS = r'equation|align|gather|multline|eqnarray|displaymath|flalign|alignat'
NOT_MATH = re.compile(r'\\(label|ref|eqref|pageref|hyperref|href|url|cite[a-z]*|text[a-z]*|mathtt|mbox|hbox|'
                      r'operatorname|tag|begin|end)\*?\s*(\[[^\]]*\])?\s*\{')
WINDOW = 160  # how far around a letter its pattern may look
GROUP = r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'  # a brace group, nested up to three deep
FUNC = re.compile(r'\\[A-Za-z]*Func(?![A-Za-z])((?:\s*(?:[_^]\s*(?:' + GROUP + r"|\\[A-Za-z]+|[^\s{}])|'))+)")
SUBSCRIPT = re.compile(r'_\s*(' + GROUP + r'|\\[A-Za-z]+|[^\s{}])')
DATE = re.compile(r'(?<![A-Za-z\\])[tT](?![A-Za-z])|\\prd[tT](?![A-Za-z])|\\Alt\{')
ARGUMENT = re.compile(r'\s*(\\(left|bigl?|Bigl?|biggl?|Biggl?)\s*)?\(')


def blank(s, a, b):
    """Replace s[a:b] by spaces, keeping newlines, so offsets stay put."""
    return s[:a] + ''.join(ch if ch == '\n' else ' ' for ch in s[a:b]) + s[b:]


def printed(text):
    """The source with what doesn't print blanked: comments, comment environments, what follows \\end{document}."""
    for m in list(re.finditer(r'(?<!\\)%[^\n]*', text)):
        text = blank(text, m.start(), m.end())
    m = re.search(r'\\end\{document\}', text)
    if m:
        text = blank(text, m.start(), len(text))
    for m in list(re.finditer(r'\\begin\{comment\}.*?\\end\{comment\}', text, re.S)):
        text = blank(text, m.start(), m.end())
    return text


def argument_end(text, i):
    """The index just past the brace group whose opening brace is just before i."""
    depth = 1
    while i < len(text) and depth:
        depth += {'{': 1, '}': -1}.get(text[i], 0)
        i += 1
    return i


def math_spans(text):
    spans = []
    for m in re.finditer(r'\\begin\{(' + MATH_ENVS + r')\*?\}(.*?)\\end\{\1\*?\}', text, re.S):
        spans.append((m.start(2), m.end(2)))
    for pattern in (r'\\\[(.*?)\\\]', r'\\\((.*?)\\\)', r'(?<![\\$])\$\$(.+?)\$\$', r'(?<![\\$])\$(?!\$)(.+?)(?<!\\)\$'):
        spans += [(m.start(1), m.end(1)) for m in re.finditer(pattern, text, re.S)]
    for m in re.finditer(r'\\ensuremath\s*\{', text):
        spans.append((m.end(), argument_end(text, m.end()) - 1))
    spans.sort()
    kept = []
    for s, e in spans:
        if not kept or s >= kept[-1][1]:
            kept.append((s, e))
    return kept


def raw_letters(text, spans):
    """Yield (offset, letter) for each raw letter in the math."""
    for s, e in spans:
        span = text[s:e]
        for m in NOT_MATH.finditer(span):
            span = blank(span, m.end(), argument_end(span, m.end()) - 1)
        # TeX's own reading: a control word, a control symbol, or one character
        for m in re.finditer(r'\\[A-Za-z]+|\\.|[A-Za-z]', span, re.S):
            tok = m.group()
            if not tok.startswith('\\') or tok[1:] in GREEK:
                yield s + m.start(), tok


def functions_as_numbers(text, spans):
    """Yield (offset, the macro with its scripts, its whole equation) for each function's macro used as a number."""
    for s, e in spans:
        span = text[s:e]
        for m in FUNC.finditer(span):
            dated = any(DATE.search(sub) for sub in SUBSCRIPT.findall(m.group(1)))
            if dated and not ARGUMENT.match(span, m.end()):
                yield s + m.start(), re.sub(r'\s+', '', m.group()), span


def check(path, problems, held_found, used):
    source = open(path, encoding='utf-8').read()
    text = printed(source)
    spans = math_spans(text)
    name = os.path.basename(path)
    line_of = lambda pos: source.count('\n', 0, pos) + 1

    for pos, letter in raw_letters(text, spans):
        near = text[max(0, pos - WINDOW):pos] + '[[' + letter + ']]' + text[pos + len(letter):pos + len(letter) + WINDOW]
        hit = next((('allowed', k) for k, (who, where, _) in enumerate(ALLOWED)
                    if who == letter and (where is None or re.search(where, near))), None)
        if hit is None:
            hit = next((('held', k) for k, (who, where, _) in enumerate(HELD)
                        if who == letter and re.search(where, near)), None)
            if hit:
                held_found.setdefault(hit, []).append(line_of(pos))
        if hit is None:
            problems.append(f'{name}:{line_of(pos)}: raw {letter} in math. Write the macro for the object it names; '
                            'if it names none, add it to ALLOWED with the reason')
        else:
            used.add(hit)

    for pos, macro, equation in functions_as_numbers(text, spans):
        hit = next((('func allowed', k) for k, (what, where, _) in enumerate(FUNC_ALLOWED)
                    if re.match(what, macro) and re.search(where, equation)), None)
        if hit is None:
            hit = next((('func held', k) for k, (what, where, _) in enumerate(FUNC_HELD)
                        if re.match(what, macro) and re.search(where, equation)), None)
            if hit:
                held_found.setdefault(hit, []).append(line_of(pos))
        if hit is None:
            problems.append(f'{name}:{line_of(pos)}: {macro} is a function\'s macro used as a number (no argument). '
                            'Write the number\'s own macro; if it names the function, add it to FUNC_ALLOWED with the '
                            'reason')
        else:
            used.add(hit)


def main():
    files = sys.argv[1:] or [os.path.join(HERE, f) for f in DEFAULT]
    problems, held_found, used = [], {}, set()
    for path in files:
        check(path, problems, held_found, used)
    tables = (('allowed', ALLOWED), ('held', HELD), ('func allowed', FUNC_ALLOWED), ('func held', FUNC_HELD))
    for kind, table in tables:
        for k, (what, _, why) in enumerate(table):
            if (kind, k) not in used:
                problems.append(f'The {kind} entry for {what} ({why}) matches nothing now: remove it')
    held = 0
    for kind, table in tables:
        for k, (what, _, why) in enumerate(table):
            lines = held_found.get((kind, k))
            if lines:
                held += len(lines)
                where = ', '.join(str(n) for n in sorted(set(lines)))
                print(f'held: {what.replace(chr(92) * 2, chr(92))}, {len(lines)} time(s), line(s) {where}: {why}')
    for p in problems:
        print(p)
    print(f'{len(problems)} problem(s), {held} held')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
