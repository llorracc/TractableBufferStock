#!/usr/bin/env python3
"""Fail any raw letter in the handout's math that names an object (rule D).

Rule D, Chris Carroll, 2026-11-15 10:16:51 EST (typed in the workspace-course-choice session): "I want you to ensure
that the handouts/chapters always use the macro for the object, rather than writing it in plain latex; e.g., there
should never be simply "$C$" but instead "$\\CLvl$" etc". So every symbol in math that names an economic object is
written with its macro: the registry's (@resources/notation), or @local's for an object the registry lacks. The print
is then decided in one place, the macro's definition.

A raw letter may stay only where it names no object (a date, an index, Euler's e, the differential d, an operator,
the generic variables of a math fact) or is a throwaway letter (Chris, 2026-11-11: a regression's or a fitted
function's coefficients, a small perturbation). ALLOWED lists each, with where it is allowed and why. HELD lists the
raw object letters that wait for a decision of Chris's; they are reported, and don't fail the check. An entry of
either list that no longer matches anything fails it, so the lists can't go stale.

    ./check-raw-letters.py            check TractableBufferStock.tex
    ./check-raw-letters.py FILE ...   check other files

Math is $...$, \\(...\\), \\[...\\], \\ensuremath{...} and the equation environments; inside it, the arguments of
\\text, \\label, \\mathtt and the like are not math. Comments, comment environments and everything after
\\end{document} don't print, so they are skipped. A letter is a Latin letter, or a Greek or Hebrew letter written
with its command; \\nabla counts too, since this handout once wrote an object with it.

Exit status: 0 no raw object letter, 1 at least one.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = ['TractableBufferStock.tex']

# (letter, where it may stay raw, why). Where: a pattern searched near the letter, which is marked [[ ]]; None for
# anywhere.
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

GREEK = set('alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa varkappa lambda mu nu xi '
            'pi varpi rho varrho sigma varsigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi '
            'Sigma Upsilon Phi Psi Omega varGamma varDelta varTheta varLambda varXi varPi varSigma varUpsilon varPhi '
            'varPsi varOmega aleph beth gimel daleth ell mho eth nabla'.split())
MATH_ENVS = r'equation|align|gather|multline|eqnarray|displaymath|flalign|alignat'
NOT_MATH = re.compile(r'\\(label|ref|eqref|pageref|hyperref|href|url|cite[a-z]*|text[a-z]*|mathtt|mbox|hbox|'
                      r'operatorname|tag|begin|end)\*?\s*(\[[^\]]*\])?\s*\{')
WINDOW = 160  # how far around a letter its pattern may look


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


def raw_letters(text):
    """Yield (offset, letter) for each raw letter in the math of the printed source."""
    for s, e in math_spans(text):
        span = text[s:e]
        for m in NOT_MATH.finditer(span):
            span = blank(span, m.end(), argument_end(span, m.end()) - 1)
        # TeX's own reading: a control word, a control symbol, or one character
        for m in re.finditer(r'\\[A-Za-z]+|\\.|[A-Za-z]', span, re.S):
            tok = m.group()
            if tok.startswith('\\'):
                if tok[1:] in GREEK:
                    yield s + m.start(), tok
            else:
                yield s + m.start(), tok


def check(path, problems, held_found, used):
    source = open(path, encoding='utf-8').read()
    text = printed(source)
    line_of = lambda pos: source.count('\n', 0, pos) + 1
    for pos, letter in raw_letters(text):
        lo, hi = max(0, pos - WINDOW), pos + len(letter) + WINDOW
        near = text[lo:pos] + '[[' + letter + ']]' + text[pos + len(letter):hi]
        hit = None
        for k, (who, where, _) in enumerate(ALLOWED):
            if who == letter and (where is None or re.search(where, near)):
                hit = ('allowed', k)
                break
        if hit is None:
            for k, (who, where, _) in enumerate(HELD):
                if who == letter and re.search(where, near):
                    hit = ('held', k)
                    held_found.append((path, line_of(pos), letter, HELD[k][2]))
                    break
        if hit is None:
            problems.append(f'{os.path.basename(path)}:{line_of(pos)}: raw {letter} in math. Write the macro for the '
                            'object it names; if it names none, add it to ALLOWED with the reason')
        else:
            used.add(hit)


def main():
    files = sys.argv[1:] or [os.path.join(HERE, f) for f in DEFAULT]
    problems, held_found, used = [], [], set()
    for path in files:
        check(path, problems, held_found, used)
    for name, table in (('allowed', ALLOWED), ('held', HELD)):
        for k, (letter, where, why) in enumerate(table):
            if (name, k) not in used:
                problems.append(f'The {name} entry for {letter} ({why}) matches nothing now: remove it')
    for path, line, letter, why in held_found:
        print(f'held: {os.path.basename(path)}:{line}: {letter}: {why}')
    for p in problems:
        print(p)
    print(f'{len(problems)} problem(s), {len(held_found)} held letter(s)')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
