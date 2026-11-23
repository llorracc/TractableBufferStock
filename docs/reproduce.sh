#!/bin/bash
# Build the handout and its appendix (latexmkrc's @default_files) with latexmk, which reads latexmkrc.
# Each links to the other's labels, so each reads the other's .aux, and a change to one document can change
# what the other prints. So run latexmk until a pass rebuilds nothing (at most five passes): from a clean start
# that takes two or three, and after edits to both documents it can take one more than two. The repository
# keeps each document's .pdf, .dep and .title; .gitignore ignores the build's other files, which stay to speed
# up the next build.
cd "$(dirname "$0")" || exit 1
for pass in 1 2 3 4 5; do
  out=$(latexmk 2>&1)
  status=$?
  printf '%s\n' "$out"
  [ $status -eq 0 ] || exit $status
  printf '%s\n' "$out" | grep -q "applying rule" || break  # nothing was rebuilt: both documents are current
done
