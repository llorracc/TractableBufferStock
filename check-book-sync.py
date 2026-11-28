#!/usr/bin/env python3
"""Report where this handout has drifted from its source, the book's chapter.

The chapter content/consumption/TractableBufferStock/index.md in
intertemporal-choice/intertemporal-choice.github.io is the source: edits start there and are
carried into TractableBufferStock.tex by hand (decision 4 of the split-chapter-appendix skill in
llorracc/workspace-course-choice). This script only reports; it changes nothing. Adapted from
llorracc/PerfForesightCRRA's on 2026-11-15.

    ./check-book-sync.py                  compare with the book's main branch on GitHub
    ./check-book-sync.py --ref REF        compare with a book branch or commit on GitHub
    ./check-book-sync.py --book-git DIR   read the book at --ref from a local clone (git show)
    ./check-book-sync.py --book-dir DIR   read the book from a local checkout's working tree

The handout's appendix is a document of its own, TractableBufferStock-Appendix.tex, which the
handout summarizes in its section "Results in the Appendix" (the split-chapter-appendix skill).
Until the book splits off its appendix too, its chapter keeps it after the heading "Appendix", and
the chapter is compared with the handout and the appendix taken together, without the handout's
summary or the appendix's opening line. Once the book has its page in "Chapter Appendices"
(BOOK_APPENDIX), the chapter is compared with the handout, and that page with the appendix. In the
appendix, "the handout" and "the handout's" are accepted wherever the page says "the chapter" and
"the chapter's": the appendix names the document it belongs to.

It compares the title, the wording (headings, equations, notes and figure captions), equation
labels, citations, external links, the figures, the notebook beside the chapter, and the symbols
the macros render. It ignores macro names that render the same, a macro that prints a single
letter or symbol against that symbol written raw (rule D's conversions), quotation marks and
emphasis, and does not compare the bibliography's entries or the second argument of a heading's
\\texorpdfstring, the words of its PDF bookmark.

A symbol that prints differently in the two documents is a difference to fix, never one to accept
(Chris Carroll, 2026-11-16 11:11:13 EST: "This is exactly the kind of thing that should be sync'd
when we sync handout and chapter"). So nothing that prints is accepted: delimiter sizes and spacing
are compared too. What it still sets aside is how each format lays out a display: the environments
that wrap it, its row breaks, and \\lefteqn, which KaTeX lacks; marks that print nothing (\\hideSup,
\\tSS); and the labels' letters in the wording, whose upright print is compared once, by
compare_labels.

The notes: the chapters write their notes as margin notes and the handouts keep footnotes (Chris
Carroll, 2026-11-15 15:58:48 EST). The handout's footnotes are compared with the chapter's notes,
footnotes or margin notes, as one sequence of words in order. A footnote marks a word mid-sentence
and a margin note sits beside its paragraph, so where a note hangs is not compared, and two notes
merged into one compare the same as two. The handout's instructor notes, \\opt{MarginNotes}{...},
print only with that option and aren't in the chapter, so they are left out.

It also runs ./check-object-macros.py, the handout's rule-D check, and reports its problems.

A difference that should stay goes in one of the ACCEPTED lists below, with its reason. An entry
that no longer matches anything is reported too, so the lists can't go stale. The handout's
symbols are read from the registry's KaTeX file, the published twin of the LaTeX macros it loads,
and from @local/TractableBufferStock.sty; the chapter's from the book's registry, its
notation/course-local-math.yml, and the chapter's own front matter.

Exit status: 0 nothing to resolve, 1 something to resolve, 2 the book could not be read.
"""
import argparse
import difflib
import hashlib
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = 'https://raw.githubusercontent.com/intertemporal-choice/intertemporal-choice.github.io/{ref}/{path}'
CHAPTER = 'content/consumption/TractableBufferStock'
HANDOUT = 'TractableBufferStock.tex'
# Where the shared text starts, in both, and where the handout's ends.
# Both documents are compared from their introductions on (the notebook paragraph follows the introduction).
HAND_START, BOOK_START = '\\section{Introduction}', '## Introduction'
HAND_END = '\\bibliographystyle'
REGISTRY = '@resources/notation/econark-math.yml'
LOCAL_STY = os.path.join('@local', 'TractableBufferStock.sty')
NOTEBOOK = 'TractableBufferStock.ipynb'
# The appendix, a document of its own since the split (plan: workspace-course-choice's
# artifacts/book-drafts/2026-11-22_TractableBufferStock-appendix/plan.md), and the book's page for it.
APPENDIX_TEX = 'TractableBufferStock-Appendix.tex'
BOOK_APPENDIX = 'content/appendices/chapters/TractableBufferStock.md'
APPENDIX_START = 'This is the appendix to'  # the first words of the appendix's shared text, in both
SUMMARY = '\\section{Results in the Appendix}'  # the handout's summary of the appendix
INLINE_APPENDIX = r'^## Appendix\s*$'  # the chapter's heading while the appendix is still inside it
# The note made from the handout's section "A Macroeconomic Interpretation" (plan: workspace-course-choice's
# records, 2026-11-25), a document of its own; the book's Supplemental Note for it; and the first words of its
# shared text, in both.
MACRO_TEX = 'TractableBufferStock-Macro.tex'
BOOK_MACRO = 'content/supplemental/TractableBufferStockMacro.md'
MACRO_START = 'Loosely following'
# The documents' links to each other, which the book writes as links to labels; none is compared.
CROSS_LINKS = ('\\HandoutPDF', '\\AppendixPDF', '\\MacroPDF')

# The book's macro names, where they differ, and the handout's for the same objects.
BOOK_TO_HANDOUT = {}

# The employment states' labels. The handout writes them with macros, which print them upright (Chris,
# 2026-11-15 12:07:32: "labels upright"); in the wording each counts as its letter, and the print is
# compared once, by compare_labels.
LABELS = {'EmpLbl': 'e', 'UnempLbl': 'u'}

# (book pattern, what the handout writes, why the difference is accepted). Applied to the book's text.
NBSELF_REWRITE = "the handout calls the chapter's notebook its own"
PFCRRA = ('each document points to the perfect-foresight material its own way: the handout names that handout or links its '
          "appendix's PDF, the chapter links its section")
ACCEPTED_REWRITES = [
    (r'(?:[Tt]he )?\[[Pp]erfect foresight CRRA\]\(#sec:PerfForesightCRRA\)(?: section)?', 'PFCRRAREF', PFCRRA),
    (r'\[appendix to perfect foresight CRRA\]\(#sec:\w+\)', 'appendix to PFCRRAREF', PFCRRA),
    (r"\bthe chapter's (?=\[notebook\])", "the handout's ", NBSELF_REWRITE),
    (r"\b([Tt]his) chapter's figures", r"\1 handout's figures", NBSELF_REWRITE),
    (r"\b([Tt]he) chapter's notebook\b", r"\1 handout's notebook", NBSELF_REWRITE),
    # The appendix's value function links the perfect-foresight model's closed-form value (finding 8 of the
    # 2026-11-22 review); the handout links that handout's appendix, as a PDF.
    (r'(?:the )?\[perfect foresight model\]\(#sec:PerfForesightCRRA-ValueClosedForm\)', 'PFCRRAREF', PFCRRA),
]
# The handout's side of the same: its names for other handouts, and its links to their appendices' PDFs, in the
# chapter's words (Chris Carroll, 2026-11-22: link the public appendix PDF).
HAND_REWRITES = [
    (r'\\handoutC\{PerfForesightCRRA\}', 'PFCRRAREF'),
    (r'\\href\{https://llorracc\.github\.io/PerfForesightCRRA/PerfForesightCRRA-Appendix\.pdf\}\{appendix to perfect foresight CRRA\}', 'appendix to PFCRRAREF'),
    (r'(?:the )?\\href\{https://llorracc\.github\.io/PerfForesightCRRA/PerfForesightCRRA-Appendix\.pdf\}\{perfect foresight model\}', 'PFCRRAREF'),
]

# Both documents' figures are drawn by the chapter's notebook, and the handout links its own copy of it (Chris,
# 2026-11-21 14:34:22 EST, in this repo's session: "(a), commit and push"). Binder opens the handout's copy too
# since binder/ was fixed (Chris, 2026-11-22: "2. fix"); JupyterLite opens the book's in-browser copy, the
# same notebook, in both documents.
NBSELF = "the handout links its own copy of the chapter's notebook, and calls it the handout's"

# (the handout's words just before it, handout words, book words, why accepted)
# Words are as tokenized, with spaces between them.
ACCEPTED_TEXT = [
    ('Introduction This', 'handout', 'chapter', 'each document names its own format'),
    ('The conditions used in this', 'handout', 'chapter', 'each document names its own format'),
]

# Differences that exist only once the book has split off its appendix, in the form of ACCEPTED_TEXT: the
# summary's wording, which the chapter has only then. Used, and checked for staleness, only after the split.
ACCEPTED_AFTER_SPLIT_TEXT = [
    ('the approximation this', 'handout', 'chapter', 'each document names its own format'),
]
# Rewrites in ACCEPTED_REWRITES that apply only to the book's appendix page, so only after the split.
AFTER_SPLIT_REWRITES = {r'(?:the )?\[perfect foresight model\]\(#sec:PerfForesightCRRA-ValueClosedForm\)'}

# Differences that wait for the book to split off its appendix, in the form of ACCEPTED_TEXT. Used only while
# the chapter still has its Appendix section; empty this list once it doesn't.
PENDING_SPLIT_TEXT = []

# Links only in the chapter, by their text, and why.
ACCEPTED_LINKS = {}

# Links in both documents whose addresses differ, by their text, and why.
ACCEPTED_LINK_URLS = {'notebook': NBSELF, 'figure notebook': NBSELF, 'Colab': NBSELF, 'Binder': NBSELF}

# The figures, in order: (the chapter's file, the handout's), and why their pictures differ.
FIGURES_DIFFER = ("both are drawn by the chapter's notebook, with its own solver: the chapter shows "
                  "its PNGs, the handout PDFs saved by the same notebook with the same settings")

# Handout macros that render differently from the book's, and why.
ACCEPTED_SYMBOLS = {}

COMMENT = r'(?<!\\)%.*$'
BOOK_DIR = None  # a local checkout of the book, from --book-dir
BOOK_GIT = None  # a local clone of the book, from --book-git
# The handout's macros that print a single letter or symbol, e.g. \cNrm as c and \cGap as \nabla. In the
# wording, on both sides, each counts as what it prints, so an object written with its macro (rule D) is
# not drift until the other side does the same; compare_symbols still compares how they print.
SYMBOL_MACROS = {}


def fetch(ref, path):
    """The bytes of a file in the book at ref, or None if it isn't there.

    With --book-git, files are read from that clone with git show; with --book-dir, a file that
    is in that checkout is read from it, and the rest come from GitHub."""
    if BOOK_GIT:
        run = subprocess.run(['git', '-C', BOOK_GIT, 'show', f'{ref}:{path}'], capture_output=True)
        return run.stdout if run.returncode == 0 else None
    if BOOK_DIR and os.path.exists(os.path.join(BOOK_DIR, path)):
        with open(os.path.join(BOOK_DIR, path), 'rb') as f:
            return f.read()
    url = RAW.format(ref=urllib.parse.quote(ref, safe=''), path=urllib.parse.quote(path, safe='/'))
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


def need(ref, path):
    """The text of a file the check can't run without."""
    data = fetch(ref, path)
    if data is None:
        raise OSError(f'{path} is not there')
    return data.decode('utf8')


def read_macros(text):
    """A MyST math block, either  '\\name': 'definition'  or  "\\\\name": "definition"."""
    table = {}
    for line in text.split('\n'):
        m = re.match(r"""\s*(['"]?)(\\{1,2}[A-Za-z]+)\1\s*:\s*(.*)$""", line)
        if not m:
            continue
        value = m[3].split(' #')[0].strip()
        if len(value) > 1 and value[0] == value[-1] and value[0] in '\'"':
            quote, value = value[0], value[1:-1]
            if quote == '"':
                value = value.replace('\\\\', '\\')
        table[m[2].lstrip('\\')] = value
    return table


def expand(definition, table):
    """Replace macros with their definitions until none are left, then drop what doesn't print."""
    for _ in range(12):
        new = re.sub(r'\\([A-Za-z]+)', lambda m: table.get(m[1], m[0]), definition)
        if new == definition:
            break
        definition = new
    definition = re.sub(r'[\s{}]+', '', definition.replace('\\ensuremath', ''))
    return re.sub(r'(\\textbf|\\text)\\text(?![a-z])', r'\1', definition)  # text nested in text prints the same


def matching_brace(text, start):
    depth, i = 0, start
    while i < len(text):
        if text[i] == '\\':
            i += 2
            continue
        depth += (text[i] == '{') - (text[i] == '}')
        if depth == 0:
            return i
        i += 1
    raise ValueError('unbalanced braces after: ' + text[start:start + 60])


def unwrap(text, opener, before='', after=''):
    """Remove a command and its braces, keeping what they enclose."""
    pattern = re.compile(opener + r'\{')
    while True:
        m = pattern.search(text)
        if not m:
            return text
        close = matching_brace(text, m.end() - 1)
        text = text[:m.start()] + before + text[m.end():close] + after + text[close + 1:]


def drop(text, opener):
    """Remove a command and its braces, with what they enclose."""
    pattern = re.compile(opener + r'\{')
    while True:
        m = pattern.search(text)
        if not m:
            return text
        text = text[:m.start()] + text[matching_brace(text, m.end() - 1) + 1:]


def between(text, start, end):
    """The text from the first `start` up to the first `end` after it, or to the end if `end` is None."""
    i = text.index(start)
    return text[i:] if end is None else text[i:text.index(end, i)]


def strip_label(x):
    return re.sub(r'^(?:eq|fig|sec):(?:TBS-)?', '', x)


def printed_source(tex):
    """The handout as it prints: comments and comment environments removed, and nothing after \\end{document}
    (where it keeps superseded material). A comment can hold \\end{document}, so comments go first."""
    plain = re.sub(COMMENT, '', tex, flags=re.M)
    plain = re.sub(r'\\begin\{comment\}.*?\\end\{comment\}', '', plain, flags=re.S)
    return plain[:plain.index('\\end{document}')]


def handout_words(t):
    t = drop(t, r'\\opt\{MarginNotes\}')  # the instructor notes
    # A figure note's last words, "[live version]", linked to the footnote with the notebook's links (Chris,
    # 2026-11-27 22:11:09 EST), and that footnote's label.
    t = re.sub(r'\\LiveVersion\{[^}]*\}', ' LIVEVERSION ', t)
    t = re.sub(r'\\footnoteLabel\{[^}]*\}', '', t)
    for pattern, replacement in HAND_REWRITES:
        t = re.sub(pattern, replacement, t)
    t = re.sub(r'\\(begin|end)\{(itemize|enumerate)\}|\\item\b', '', t)
    t = re.sub(r'\\(?:label|labelEqInFootnote)\{[^}]*\}', '', t)
    t = re.sub(r'\\hypertarget\{[^}]*\}\{\}', '', t)
    t = re.sub(r'\\set(?:counter|length)\{[^}]*\}\{[^}]*\}', '', t)
    # Marks that print nothing: an empty superscript that aligns, and the steady state's empty subscript.
    t = re.sub(r'[\^_]\{?\\(?:hideSup|tSS)\}?', '', t)
    t = re.sub(r'\\eqref\{([^}]*)\}', lambda m: 'EQ' + strip_label(m[1]), t)
    # A link that names an equation, as the chapter's do.
    t = re.sub(r'\\hyperref\[(eq:[^\]]*)\]\{([^{}]*)\}', lambda m: m[2] + ' EQ' + strip_label(m[1]), t)
    t = re.sub(r'(?:[Ff]igures?[~ ]?)?\\ref\{(fig:[^}]*)\}', lambda m: 'FIGREF' + strip_label(m[1]), t)
    t = re.sub(r'\\ref\{(sec:[^}]*)\}', lambda m: 'SECREF' + strip_label(m[1]), t)
    t = re.sub(r'\\cite[tp]?\{([^}]*)\}', r'CITE\1', t)
    t = re.sub(r'\\includegraphics(\[[^\]]*\])?\{[^}]*\}', '', t)
    t = re.sub(r'\\(begin|end)\{(figure|center|table)\}(\[[^\]]*\])?', '', t)
    t = re.sub(r'\\renewcommand\{\\arraystretch\}\{[^}]*\}', '', t)
    t = re.sub(r'\\(notag|nonumber|medskip|bigskip|smallskip|pagebreak|newpage|appendix|centering|LARGE|Large|large|'
               r'bf|it|em|small|footnotesize|par|noindent|indent|raggedright|strut)\b', '', t)
    t = re.sub(r'\\centerline(?=\s*[^\s{])', '', t)
    # The handout's names for linked facts and handouts, which the chapter writes as plain words or links.
    t = t.replace('\\Mma', 'Mathematica').replace('\\MathFactsList', 'Math Facts')
    t = re.sub(r'\\(TaylorOne|TaylorTwo|InfSum|FinSum)(?![A-Za-z])', r'\1', t)
    # A table's layout, which the chapter writes as a Markdown table: & becomes a space in tokens().
    t = re.sub(r'\\begin\{tabular\}\{[^}]*\}|\\end\{tabular\}|\\hline', '', t)
    t = unwrap(t, r'\\parbox(?:\[[a-z]\])?\{[^}]*\}')
    t = t.replace('\\\\', ' ')  # a display's rows, before \& is read as an ampersand
    t = t.replace('\\%', '%').replace('\\&', '&')
    # A heading's \texorpdfstring{what prints}{its PDF bookmark}: what prints is compared, the bookmark is not.
    t = re.sub(r'\\texorpdfstring\{((?:[^{}]|\{[^{}]*\})*)\}\{(?:[^{}]|\{[^{}]*\})*\}', r'\1', t)
    for opener in (r'\\hyperref\[[^\]]*\]', r'\\href\{[^}]*\}', r'\\textit', r'\\textbf', r'\\emph', r'\\texttt',
                   r'\\centerline', r'\\lefteqn', r'\\handout[CM]', r'\\(?:sub)*section\*?'):
        t = unwrap(t, opener)
    t = unwrap(t, r'\\caption', ' CAP ', ' ENDCAP ')
    t = unwrap(t, r'\\FigNote', ' CAP Note: ', ' ENDCAP ')  # the note under a figure, which is part of its caption
    t = unwrap(t, r'\\marginFootnote', ' FOOT ', ' ENDFOOT ')  # a margin note in the chapter
    return tokens(unwrap(t, r'\\footnote', ' FOOT ', ' ENDFOOT '))


def book_words(md, used, start=BOOK_START):
    """The words from `start` on, in the handout's macro names; `used` counts the rewrites."""
    b = md[md.index(start):]
    for pattern, replacement, _ in ACCEPTED_REWRITES:
        b, count = re.subn(pattern, replacement, b)
        used[pattern] = used.get(pattern, 0) + count
    # "[live version]", the link a figure's note ends with: [[live version]](#…) or [\[live version\]](#…).
    b = re.sub(r'\[(?:\\?\[)live version(?:\\?\])\]\(#[^)]*\)', ' LIVEVERSION ', b)
    b = re.sub(r'\\([A-Za-z]+)', lambda m: '\\' + BOOK_TO_HANDOUT.get(m[1], m[1]), b)
    b = re.sub(r'^- ', '', b, flags=re.M)  # list items, which the handout writes as \item
    # A Markdown table: its rule line and the bars between cells are layout, as the handout's \hline and & are.
    b = re.sub(r'^\|(?:\s*:?-+:?\s*\|)+\s*$', '', b, flags=re.M)
    b = re.sub(r'^\|(.*)\|\s*$', lambda m: m[1].replace('|', ' '), b, flags=re.M)
    footnotes = {}

    def keep(m):
        footnotes[m[1]] = m[2]
        return ''

    b = unwrap(b, r'\\texttt')  # as the handout's side does
    b = re.sub(r'^\[\^([\w-]+)\]:[ \n]((?:.*\n?)(?:(?:[ ]{4}.*|)\n)*)', keep, b, flags=re.M)
    b = re.sub(r'\[\^([\w-]+)\]', lambda m: ' FOOT ' + footnotes.get(m[1], 'MISSING') + ' ENDFOOT ', b)
    # A margin block is read as the same note as the handout's footnote (Chris, 2026-11-15 15:58:48 EST).
    # A target on a margin note's first line is where a link lands (the figure notes' "[live version]"), not words.
    b = re.sub(r'^:::\{margin\}\n(?:\([A-Za-z:-]+\)=\n)?(.*?)\n:::$', r' FOOT \1 ENDFOOT ', b, flags=re.M | re.S)
    # A figure's caption: its title, and the paragraph "Note: ..." under it, which the handout writes as \caption and
    # \FigNote (Chris, 2026-11-27 14:36:37 EST).
    b = re.sub(r'^:::\{figure\}[^\n]*\n(?::[a-z]+:[^\n]*\n)*(.*?)\n:::$', r' CAP \1 ENDCAP ', b, flags=re.M | re.S)
    b = re.sub(r'^:name:.*$|^:align:.*$|^:width:.*$|^:::$|^:label:.*$', '', b, flags=re.M)
    b = b.replace('```{math}', '').replace('```', '')
    b = re.sub(r'\{math\}`([^`]*)`', r'\1', b)
    b = re.sub(r'\{eq\}`([^`]*)`', lambda m: 'EQ' + strip_label(m[1]), b)
    b = re.sub(r'\{numref\}`([^`]*)`', lambda m: 'FIGREF' + strip_label(m[1]), b)
    b = re.sub(r'\{cite:[tp]\}`([^`]*)`', r'CITE\1', b)
    b = re.sub(r'^\([A-Za-z:-]+\)=$', '', b, flags=re.M)
    b = re.sub(r'^#+ ', '', b, flags=re.M)
    # A link to an equation names it where the handout prints its number: keep both.
    b = re.sub(r'\[([^\]]*)\]\(#(eq:[^)]*)\)', lambda m: m[1] + ' EQ' + strip_label(m[2]), b)
    b = re.sub(r'\[([^\]]*)\]\((?:\\.|[^)\\])*\)', r'\1', b)
    return tokens(b)


def tokens(s):
    s = re.sub(r'\\(begin|end)\{(equation|gathered|aligned|align|split|eqnarray|gather|multline)\*?\}', '', s)
    s = s.replace('\\\\', ' ')  # rows of a display, which are layout
    # Delimiter sizes and spacing print, so they are compared (Chris, 2026-11-16 11:11:13, below).
    s = s.replace('\\\n', ' ').replace('\\ ', ' ').replace('~', ' ').replace('``', '').replace("''", '')
    for mark in '"`*“”':
        s = s.replace(mark, '')
    s = s.replace('$', ' ').replace('&', ' ').replace('—', ' ').replace('–', ' ').replace('−', '-')
    s = re.sub(r'(?<!-)---?(?!-)', ' ', s)  # TeX's dashes
    s = re.sub(r"(?<![A-Za-z])'|'(?![a-z])|’(?![a-z])", '', s)
    s = s.replace('’', "'").replace('{', ' ').replace('}', ' ')
    words = re.findall(r'\\[A-Za-z]+|\\\\|[A-Za-z]+(?:\'[a-z]+)?|\d+(?:\.\d+)?|\S', s)
    out = []
    for w in words:
        name = w[1:] if w[:1] == '\\' else None
        if name in LABELS:
            out.append(LABELS[name])
        elif name in SYMBOL_MACROS:
            out.extend(SYMBOL_MACROS[name])
        else:
            out.append(w)
    return out


def split_notes(words):
    """The words of the text, of the notes and of the figure captions, each in order, and how many notes.

    Notes and captions are compared by order, not by where they sit: a footnote sits at its mark and a
    margin note beside its paragraph, and a LaTeX figure floats away from where the chapter places it."""
    streams = {None: [], 'FOOT': [], 'CAP': []}
    inside, count = None, 0
    for w in words:
        if w in ('FOOT', 'CAP'):
            inside = w
            count += w == 'FOOT'
        elif w in ('ENDFOOT', 'ENDCAP'):
            inside = None
        else:
            streams[inside].append(w)
    return streams[None], streams['FOOT'], streams['CAP'], count


def diff_words(hand, book, accepted, problems, what):
    """Report differing words that no entry of `accepted` explains; return the entries that matched."""
    matched = set()
    ops = difflib.SequenceMatcher(None, hand, book, autojunk=False).get_opcodes()
    for tag, i1, i2, j1, j2 in ops:
        if tag == 'equal':
            continue
        h, b = ' '.join(hand[i1:i2]), ' '.join(book[j1:j2])
        near = ' '.join(hand[max(0, i1 - 9):i1])
        for entry in accepted:
            if (h, b) == (entry[1], entry[2]) and near.endswith(entry[0]):
                matched.add(entry)
                break
        else:
            problems.append(f'{what}, after "... {near}":\n    book:    {b[:600]}\n    handout: {h[:600]}')
    return matched


def compare_words(hand, book, accepted, problems):
    """The text, and then the notes as one sequence, each against the other document's."""
    (h_text, h_notes, h_caps, h_n), (b_text, b_notes, b_caps, b_n) = split_notes(hand), split_notes(book)
    matched = diff_words(h_text, b_text, accepted, problems, 'Wording')
    matched |= diff_words(h_notes, b_notes, accepted, problems, 'Wording in the notes')
    matched |= diff_words(h_caps, b_caps, accepted, problems, 'Wording in the figure captions')
    return matched, h_n, b_n


def compare_marks(plain, md, problems, links_used):
    """Equation labels, citations and external links: `plain` is handout source, `md` the chapter.
    `links_used` collects the ACCEPTED_LINKS entries that applied."""
    h_labels = {strip_label(x) for x in re.findall(r'\\(?:label|labelEqInFootnote)\{(eq:[^}]*)\}', plain)}
    b_labels = {strip_label(x) for x in re.findall(r'^\s*:label:\s*(eq:\S+)', md, re.M)}
    for x in sorted(b_labels - h_labels):
        problems.append(f'Equation label only in the book: {x}')
    for x in sorted(h_labels - b_labels):
        problems.append(f'Equation label only in the handout: {x}')
    for display in re.findall(r'\\begin\{equation\*\}.*?\\end\{equation\*\}', plain, re.S):
        for x in re.findall(r'\\label\{([^}]*)\}', display):
            problems.append(f'Label in an unnumbered equation, so citations of it print the wrong number: {x}')
    # One \\notag or \\nonumber anywhere in an equation environment removes its only number, and a label in it
    # then takes the next equation's number (found 2026-11-21: four labels, two of them cited).
    for display in re.findall(r'\\begin\{equation\}.*?\\end\{equation\}', plain, re.S):
        if re.search(r'\\(?:notag|nonumber)(?![A-Za-z])', display):
            for x in re.findall(r'\\label\{([^}]*)\}', display):
                problems.append(f'Label in an equation whose number a \\notag or \\nonumber removes, so citations '
                                f"of it print the next equation's number: {x}")

    h_cites = {k.strip() for g in re.findall(r'\\cite[tp]?\{([^}]*)\}', plain) for k in g.split(',')}
    b_cites = {k.strip() for g in re.findall(r'\{cite:[tp]\}`([^`]*)`', md) for k in g.split(',')}
    for k in sorted(b_cites ^ h_cites):
        problems.append(f'Citation only in the {"book" if k in b_cites else "handout"}: {k}')

    # The handout's links to other handouts' appendices are compared, like its names for those handouts, after
    # HAND_REWRITES has turned them into the tokens the chapter's links to the same sections become.
    for pattern, replacement in HAND_REWRITES:
        plain = re.sub(pattern, replacement, plain)
    h_links = {text: url for url, text in re.findall(r'\\href\{([^}]*)\}\{([^}]*)\}', plain) if url not in CROSS_LINKS}
    # A link's text in code font is `x` in the chapter and \texttt{\href{..}{x}} in the handout: compare x.
    b_links = {text.strip('`'): url for text, url in re.findall(r'\[([^\]]*)\]\(([^)#][^)]*)\)', md)}
    for text in sorted(set(b_links) | set(h_links)):
        b_url, h_url = b_links.get(text), h_links.get(text)
        if h_url is None and text in ACCEPTED_LINKS:
            links_used.add(text)
        elif b_url is None or h_url is None:
            problems.append(f'Link only in the {"handout" if b_url is None else "book"}: {text}')
        elif b_url != h_url and text in ACCEPTED_LINK_URLS:
            links_used.add(text)
        elif b_url != h_url:
            problems.append(f'Link "{text}":\n    book:    {b_url}\n    handout: {h_url}')


def compare_title(tex, md, problems):
    h_title = re.search(r'\\begin\{verbatimwrite\}\{\\jobname\.title\}\s*(.*?)\s*\\end\{verbatimwrite\}', tex, re.S)[1]
    b_title = re.search(r'^# (.*)$', md, re.M)[1].strip()
    if h_title != b_title:
        problems.append(f'Title:\n    book:    {b_title}\n    handout: {h_title}')


def compare_figures(plain, md, problems):
    """The figures each document shows, in order. Their pictures differ by design (FIGURES_DIFFER)."""
    h_figs = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{\\FigDir/([^}]*)\}', plain)
    b_figs = [os.path.splitext(os.path.basename(p))[0] for p in re.findall(r'^:::\{figure\}\s*(\S+)', md, re.M)]
    if len(h_figs) != len(b_figs):
        problems.append(f'Figures: the book shows {len(b_figs)}, the handout {len(h_figs)}:\n'
                        f'    book:    {", ".join(b_figs)}\n    handout: {", ".join(h_figs)}')
    return list(zip(b_figs, h_figs))


def compare_labels(md, label_macros, problems):
    """The employment labels: upright in the handout, by its macros; report the chapter's raw ones once,
    with the chapter's macros that differ from the handout's only in them."""
    raw = len(re.findall(r'\^\{?[eu]\}?(?![A-Za-z])', md))
    if raw:
        built = f', and in its macros built on them ({", ".join(chr(92) + m for m in label_macros)})' if label_macros else ''
        problems.append(f'Labels: the chapter writes the employment labels raw, ^{{e}} and ^{{u}}, {raw} times{built}, '
                        'which print them italic; the handout writes \\EmpLbl and \\UnempLbl, which print them upright '
                        '(Chris, 2026-11-15 12:07:32: "labels upright")')


def compare_symbols(md, tex_body, book_table, hand_table, problems):
    """Report the macros both use that render differently; return how many are accepted, and the
    macros that differ only in the labels' upright e and u, which compare_labels reports."""
    differing, label_only = set(), []
    hand_used = set(re.findall(r'\\([A-Za-z]+)', tex_body))
    for c in sorted(set(re.findall(r'\\([A-Za-z]+)', md)) & set(book_table)):
        h = BOOK_TO_HANDOUT.get(c, c)
        if h not in hand_used:
            continue
        b_def, h_def = expand('\\' + c, book_table), expand('\\' + h, hand_table)
        if b_def == h_def:
            continue
        if h in ACCEPTED_SYMBOLS:
            differing.add(h)
        elif re.sub(r'\\mathrm([eu])', r'\1', h_def) == b_def:
            label_only.append(h)
        else:
            problems.append(f'Symbol: book \\{c} is {b_def}, handout \\{h} is {h_def}')
    for h in sorted(set(ACCEPTED_SYMBOLS) - differing):
        problems.append(f'No longer needed in ACCEPTED_SYMBOLS: \\{h} now agrees with the book, or is unused')
    return len(differing), label_only


def book_macro_table(ref, md):
    """The book's registry, its course-local overrides, and the chapter's own front matter."""
    table = read_macros(need(ref, REGISTRY))
    local = fetch(ref, 'notation/course-local-math.yml')
    if local is not None:
        table.update(read_macros(local.decode('utf8')))
    front = re.match(r'---\n(.*?)\n---\n', md, re.S)
    if front:
        table.update(read_macros(front[1]))
    return table


def hand_macro_table():
    table = read_macros(open(os.path.join(HERE, REGISTRY), encoding='utf8').read())
    sty = open(os.path.join(HERE, LOCAL_STY), encoding='utf8').read()
    table.update(dict(re.findall(r'^\\providecommand\{\\(\w+)\}\{(.*)\}\s*(?:%.*)?$', sty, re.M)))
    return table


def rule_d(problems):
    """The handout's rule-D check: its problems are this check's."""
    run = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'check-object-macros.py')],
                         capture_output=True, text=True)
    lines = run.stdout.strip().split('\n')
    if run.returncode != 0:
        problems.extend('check-object-macros.py: ' + line for line in lines if not line.startswith('held: '))
    return lines[-1] if lines else 'no output'


def as_chapter(words):
    """The appendix's words with its self-references in the page's terms: "the handout" and "the handout's"
    become "the chapter" and "the chapter's" (the split-chapter-appendix skill, step 5). Returns the words and
    how many were changed."""
    out, n = [], 0
    for w in words:
        if w in ('handout', "handout's"):
            out.append(w.replace('handout', 'chapter'))
            n += 1
        else:
            out.append(w)
    return out, n


def main():
    global BOOK_DIR, BOOK_GIT
    parser = argparse.ArgumentParser(description='Report where the handout and its appendix have drifted from the book.')
    parser.add_argument('--ref', default='main', help='book branch or commit (default: main)')
    parser.add_argument('--book-git', help='a local clone of the book, read at --ref with git show')
    parser.add_argument('--book-dir', help='a local checkout of the book; files it lacks are read from GitHub at --ref')
    parser.add_argument('--handout', default=os.path.join(HERE, HANDOUT), help='handout source')
    parser.add_argument('--appendix', default=os.path.join(HERE, APPENDIX_TEX), help="the appendix's source")
    parser.add_argument('--note', default=os.path.join(HERE, MACRO_TEX), help="the note's source")
    args = parser.parse_args()
    BOOK_DIR, BOOK_GIT = args.book_dir, args.book_git
    book_name = args.book_dir or (f'{args.book_git} at {args.ref}' if args.book_git else f'book ref {args.ref}')

    tex = open(args.handout, encoding='utf8').read()
    app = open(args.appendix, encoding='utf8').read()
    note = open(args.note, encoding='utf8').read()
    plain, app_plain, note_plain = printed_source(tex), printed_source(app), printed_source(note)
    try:
        md = need(args.ref, CHAPTER + '/index.md')
        split = not re.search(INLINE_APPENDIX, md, re.M)
        app_md = need(args.ref, BOOK_APPENDIX) if split else ''
        note_raw = fetch(args.ref, BOOK_MACRO)  # None until the book has the note
        note_md = note_raw.decode('utf8') if note_raw is not None else ''
        book_table = book_macro_table(args.ref, md)
    except OSError as err:  # includes urllib's errors
        print(f'Could not read the book at {args.ref}: {err}', file=sys.stderr)
        return 2

    hand_table = hand_macro_table()
    for name in hand_table:
        printed = expand('\\' + name, hand_table)
        if re.fullmatch(r'[A-Za-z]|\\[A-Za-z]+|\\math(?:frak|cal|rm)[A-Za-z]', printed):
            SYMBOL_MACROS[name] = tokens(re.sub(r'(\\math(?:frak|cal|rm))([A-Za-z])$', r'\1 \2', printed))

    problems = []
    used = {}
    links_used = set()
    compare_title(tex, md, problems)
    if split:
        compare_title(app, app_md, problems)
        accepted = ACCEPTED_TEXT + ACCEPTED_AFTER_SPLIT_TEXT
        matched, h_notes, b_notes = compare_words(handout_words(between(plain, HAND_START, HAND_END)),
                                                  book_words(md, used), accepted, problems)
        # Both sides in the page's terms: the book's own rewrites (NBSELF_REWRITE) make its "the chapter's notebook"
        # "the handout's notebook", which as_chapter turns back.
        app_words, n_self = as_chapter(handout_words(between(app_plain, APPENDIX_START, HAND_END)))
        page_words, _ = as_chapter(book_words(app_md, used, APPENDIX_START))
        app_matched, a_h_notes, a_b_notes = compare_words(app_words, page_words, accepted, problems)
        matched |= app_matched
        compare_marks(plain, md, problems, links_used)
        compare_marks(app_plain, app_md, problems, links_used)
        for entry in ACCEPTED_AFTER_SPLIT_TEXT:
            if entry not in matched:
                problems.append(f'No longer needed in ACCEPTED_AFTER_SPLIT_TEXT: {entry[1]!r} / {entry[2]!r}')
        if PENDING_SPLIT_TEXT:
            problems.append('The book has split off its appendix, so PENDING_SPLIT_TEXT can be emptied')
    else:
        # The handout's summary of the appendix, and the appendix's opening line, wait for the book's split.
        hand = between(plain, HAND_START, SUMMARY) + '\n' + between(app_plain, '\\appendix', HAND_END)
        matched, h_notes, b_notes = compare_words(handout_words(hand),
                                                  book_words(re.sub(INLINE_APPENDIX, '', md, flags=re.M), used),
                                                  ACCEPTED_TEXT + PENDING_SPLIT_TEXT, problems)
        a_h_notes = a_b_notes = n_self = 0
        compare_marks(plain + app_plain, md, problems, links_used)
        for entry in PENDING_SPLIT_TEXT:
            if entry not in matched:
                problems.append(f'No longer needed in PENDING_SPLIT_TEXT: {entry[1]!r} / {entry[2]!r}')
    # The note, compared as the appendix is: in the page's terms, its "the handout" read as "the chapter".
    n_note_self = n_h_note = n_b_note = 0
    note_figures = []
    if not note_md:
        problems.append(f'The book has no Supplemental Note {BOOK_MACRO} at this ref, for the handout\'s {MACRO_TEX}')
    elif MACRO_START not in note_md:
        problems.append(f'The book\'s note {BOOK_MACRO} doesn\'t contain the note\'s first words, {MACRO_START!r}')
    else:
        compare_title(note, note_md, problems)
        note_words, n_note_self = as_chapter(handout_words(between(note_plain, MACRO_START, HAND_END)))
        page_words, _ = as_chapter(book_words(note_md, used, MACRO_START))
        note_matched, n_h_note, n_b_note = compare_words(note_words, page_words,
                                                         ACCEPTED_TEXT + ACCEPTED_AFTER_SPLIT_TEXT, problems)
        matched |= note_matched
        compare_marks(note_plain, note_md, problems, links_used)
        note_figures = compare_figures(note_plain, note_md, problems)
    for entry in ACCEPTED_TEXT:
        if entry not in matched:
            problems.append(f'No longer needed in ACCEPTED_TEXT: {entry[1]!r} / {entry[2]!r}')
    for pattern, _, _ in ACCEPTED_REWRITES:
        if not used.get(pattern) and (split or pattern not in AFTER_SPLIT_REWRITES):
            problems.append(f'No longer needed in ACCEPTED_REWRITES: {pattern}')

    for text in sorted(set(ACCEPTED_LINKS) - links_used):
        problems.append(f'No longer needed in ACCEPTED_LINKS: {text}')
    for text in sorted(set(ACCEPTED_LINK_URLS) - links_used):
        problems.append(f'No longer needed in ACCEPTED_LINK_URLS: {text}')
    figures = compare_figures(plain, md, problems)
    bodies = (plain[plain.index('\\begin{document}'):] + app_plain[app_plain.index('\\begin{document}'):]
              + note_plain[note_plain.index('\\begin{document}'):])
    n_sym, label_macros = compare_symbols(md + app_md + note_md, bodies, book_table, hand_table, problems)
    compare_labels(md + app_md + note_md, label_macros, problems)
    book_nb = fetch(args.ref, CHAPTER + '/' + NOTEBOOK)
    if book_nb is None:
        problems.append(f'The notebook {NOTEBOOK} is not beside the chapter at this ref')
    elif not os.path.exists(os.path.join(HERE, NOTEBOOK)):
        problems.append(f'The notebook {NOTEBOOK} is beside the chapter but not beside the handout')
    elif hashlib.sha256(book_nb).digest() != hashlib.sha256(open(os.path.join(HERE, NOTEBOOK), 'rb').read()).digest():
        problems.append(f"The notebook {NOTEBOOK} differs from the book's: copy it again, with ditto")

    rule_d_summary = rule_d(problems)

    if split:
        print(f'Compared the handout with the chapter {CHAPTER}/index.md, and the appendix with its page '
              f'{BOOK_APPENDIX}, in {book_name}.')
        print(f'Notes: the chapter has {b_notes}, the handout {h_notes} printed footnotes (its instructor notes left '
              f'out); the page has {a_b_notes}, the appendix {a_h_notes}.')
        print(f'The appendix names itself the handout\'s where the page says the chapter\'s: {n_self} times, accepted.')
    else:
        print(f'Compared the handout and its appendix with the chapter {CHAPTER}/index.md in {book_name}, which still '
              'has the appendix inside it.')
        print(f'Notes: the chapter has {b_notes}, the handout and its appendix {h_notes} printed footnotes (its '
              'instructor notes left out).')
        print('Waiting for the book to split off its appendix: the handout\'s section "Results in the Appendix", the '
              f'appendix\'s opening line, and {len(matched & set(PENDING_SPLIT_TEXT))} wording difference(s) listed '
              'in PENDING_SPLIT_TEXT.')
    if note_md:
        print(f'Compared the note with the book\'s Supplemental Note {BOOK_MACRO}: notes, the page {n_b_note}, the note '
              f'{n_h_note}; it names the handout where the page names the chapter {n_note_self} times, accepted; '
              f'figures, in order: {len(note_figures)} pairs.')
    print(f'Figures, in order: {len(figures)} pairs; ' + FIGURES_DIFFER + '.')
    print(f'Accepted: {len(matched)} wording differences, {sum(used.values())} rewrites, '
          f'{n_sym} symbols that render differently.')
    print(f'Rule D (check-object-macros.py): {rule_d_summary}.')
    if not problems:
        print('Nothing to resolve.')
        return 0
    print(f'\n{len(problems)} to resolve. The book is the source: carry its version into the handout,')
    print('or add the difference to an ACCEPTED list in this script if it should stay.\n')
    for p in problems:
        print('- ' + p)
    return 1

if __name__ == '__main__':
    sys.exit(main())
