# Google 'latexmk' for explanation of this config file
# latexmk at unix command line will compile the paper
$do_cd = 1;
$clean_ext = "bbl nav out snm dvi idv mk4 css cfg tmp xref 4tc out aux log fls fdb_latexmk synctex.gz toc svg png html 4ct ps dep out.ps upa upb";
$bibtex_use=2;
# econark-bibfilesfind lists the machine's system.bib (economics.bib) before TractableBufferStock.bib, so
# BibTeX reports each key in both as a "Repeated entry" error; the wrapper drops exactly those.
$bibtex = 'sh ./@resources/latexmk/latexmkrc/tools/bibtex_wrapper.sh %O %B';
$pdf_mode = 1;
#$out_dir = './LaTeX';
$rc_report = 1;
# \input@path in @resources/tex-add-search-paths is consulted only after kpathsea,
# so without this a bare \usepackage{econark} finds the machine's TEXMFLOCAL copy.
$ENV{'TEXINPUTS'} = './@resources/texlive/texmf-local/tex/latex//:' . ($ENV{'TEXINPUTS'} || '');
$ENV{'BIBINPUTS'} = './@resources/texlive/texmf-local/bibtex/bib:' . ($ENV{'BIBINPUTS'} || '');
$ENV{'BSTINPUTS'} = './@resources/texlive/texmf-local/bibtex/bst:' . ($ENV{'BSTINPUTS'} || '');
$pdflatex="pdflatex -interaction=nonstopmode %O %S";
@default_files = ('TractableBufferStock-Appendix.tex', 'TractableBufferStock.tex', 'TractableBufferStock-Macro.tex');
$aux_out_dir_report = 1;
$silent  = 0;
warn "PATH = '$ENV{PATH}'\n";
