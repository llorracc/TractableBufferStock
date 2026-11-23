#!/bin/bash
# Build the handout and its appendix (latexmkrc's @default_files) with latexmk, which reads latexmkrc.
# Each links to the other's labels, so each reads the other's .aux. From a clean start the first pass
# builds the appendix before the handout's .aux exists; the second sees that file change and rebuilds
# the appendix, and does nothing when both are already current. The repository keeps each document's
# .pdf, .dep and .title; .gitignore ignores the build's other files, which stay to speed up the next build.
cd "$(dirname "$0")" || exit 1
latexmk
latexmk
