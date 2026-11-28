#!/bin/bash
# Rebuild a web page, in this directory: the handout (the default), its appendix, or its note.
#   bash docs/TractableBufferStock.sh                                the handout, TractableBufferStock.html
#   bash docs/TractableBufferStock.sh TractableBufferStock-Appendix  the appendix, TractableBufferStock-Appendix.html
#   bash docs/TractableBufferStock.sh TractableBufferStock-Macro     the note, TractableBufferStock-Macro.html
# The pages link to each other through each other's .aux, so after a change that moves labels, build the
# handout, then the appendix and the note, then the handout again. All use TractableBufferStock.cfg, and the build file
# TractableBufferStock.mk4, which make4ht would otherwise look for under the job's own name.
# CLEAR_OLD_PAGES=1 first removes the page's numbered pages (one per footnote) from earlier builds, which
# make4ht never deletes: a page with fewer footnotes than before otherwise leaves the old ones served.
job="${1:-TractableBufferStock}"
cd "$(dirname "$0")" || exit 1

# Read the vendored TeX files first, as latexmkrc does for the PDF.
export TEXINPUTS=./@resources/texlive/texmf-local/tex/latex//:
export BIBINPUTS=./@resources/texlive/texmf-local/bibtex/bib:
export BSTINPUTS=./@resources/texlive/texmf-local/bibtex/bst:

# dvisvgm needs Ghostscript's library.
for g in /opt/homebrew/lib/libgs.dylib /usr/local/lib/libgs.dylib; do
  [ -e "$g" ] && { export LIBGS="$g"; break; }
done

[ "${CLEAR_OLD_PAGES:-0}" = 1 ] && rm -f "$job"[0-9]*.html

# The page uses .svg figures: make them from the PDFs.
for f in $(grep -o 'FigDir/[A-Za-z0-9_-]*' "$job.tex" | sed 's#FigDir/##'); do
  pdf2svg "Figures/$f.pdf" "Figures/$f.svg"
  (cd Figures && extractbb "$f.pdf")
done
make4ht --utf8 --config TractableBufferStock.cfg --build-file TractableBufferStock.mk4 --format html5-common_domfilters "$job" "svg" "-cunihtf -utf8"
ditto "$job.css" "$job-generated-by-make4ht.css"
cat page-style.css "$job-generated-by-make4ht.css" > "$job-page-style.css" && mv "$job-page-style.css" "$job.css"
if [ "$job" = TractableBufferStock ]; then
  ditto TractableBufferStock.html index.html || exit 1  # the site's front page is the handout
fi
