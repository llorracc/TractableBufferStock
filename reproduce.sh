#!/bin/bash
# Build the PDF with latexmk, which reads latexmkrc. The build's files that the repository keeps (.aux, .bbl,
# .log and .synctex.gz) stay; only latexmk's own bookkeeping goes.
cd "$(dirname "$0")" || exit 1
latexmk
rm -f TractableBufferStock.fls TractableBufferStock.fdb_latexmk
