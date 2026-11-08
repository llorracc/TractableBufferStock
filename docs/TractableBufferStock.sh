#!/bin/bash
# Rebuild the web version of the handout, in this directory.
cd "$(dirname "$0")" || exit 1

# Read the vendored TeX files first, as latexmkrc does for the PDF.
export TEXINPUTS=./@resources/texlive/texmf-local/tex/latex//:
export BIBINPUTS=./@resources/texlive/texmf-local/bibtex/bib:
export BSTINPUTS=./@resources/texlive/texmf-local/bibtex/bst:

# dvisvgm needs Ghostscript's library.
for g in /opt/homebrew/lib/libgs.dylib /usr/local/lib/libgs.dylib; do
  [ -e "$g" ] && { export LIBGS="$g"; break; }
done

# The page uses .svg figures: make them from the PDFs.
for f in $(grep -o 'FigDir/[A-Za-z0-9_-]*' TractableBufferStock.tex | sed 's#FigDir/##'); do
  pdf2svg "Figures/$f.pdf" "Figures/$f.svg"
  (cd Figures && extractbb "$f.pdf")
done

make4ht --utf8 --config TractableBufferStock.cfg --format html5 TractableBufferStock "svg" "-cunihtf -utf8"

ditto TractableBufferStock.css TractableBufferStock-generated-by-make4ht.css
cat page-style.css TractableBufferStock-generated-by-make4ht.css > TractableBufferStock-page-style.css && mv TractableBufferStock-page-style.css TractableBufferStock.css
ditto TractableBufferStock.html index.html
