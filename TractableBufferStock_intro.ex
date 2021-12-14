\input{./econtexRoot}
\documentclass{\handout}
\providecommand{\texname}{TractableBufferStock}% Keyname for the paper
\usepackage{\LaTeXInputs/\texname}% Styling for whole paper (and subfiles)
\usepackage{\econtexSetup}\usepackage{\econtexShortcuts}

% Lines containing CDCPrivate are excised when the public version of the document is created 
% \setboolean{BigAndWide}{true} % CDCPrivate 

% Items within a CDCPrivate environment are excised when the public version of the document is created
\begin{CDCPrivate}
\centerline{CDC Private Version}                                % CDCPrivate
\end{CDCPrivate}

%\usepackage{endfloat}  % uncomment to put figures at the end

\begin{document}
%\handoutHeader
\providecommand{\dmEqZero}{\ensuremath{\Delta\mRatE=0}}
\providecommand{\dcEqZero}{\ensuremath{\Delta\cRatE=0}}

\begin{verbatimwrite}{\jobname.title}
A Tractable Model of Buffer Stock Saving
\end{verbatimwrite}

%\handoutNameMake

%\section{Introduction} 


\subsubsection{The Phase Diagram}

Figure~\ref{fig:PhaseDiag} presents the phase diagram.
\begin{figure}
\caption{Phase Diagram}\label{fig:PhaseDiag}
\write18{ln -fs /Volumes/Data/Courses/Choice/LectureNotes/Consumption/Handouts/TractableBufferStock/Code/Mathematica/Examples/TractableBufferStock/Figures/TractableBufferStockPhaseDiag.pdf /Volumes/Data/Courses/Choice/LectureNotes/Consumption/Handouts/TractableBufferStock/Figures/TractableBufferStockPhaseDiag.pdf} % CDCPrivate
\write18{ln -fs /Volumes/Data/Courses/Choice/LectureNotes/Consumption/Handouts/TractableBufferStock/Code/Mathematica/Examples/TractableBufferStock/Figures/TractableBufferStockPhaseDiag.png /Volumes/Data/Courses/Choice/LectureNotes/Consumption/Handouts/TractableBufferStock/Figures/TractableBufferStockPhaseDiag.png} % CDCPrivate
\includegraphics[width=6in]{../Figures/TractableBufferStockPhaseDiag}
\end{figure}

\input{/Volumes/Data/Papers/BufferStockTheory/BufferStockTheory-Public/Resources/LaTeXInputs/bibliography_blend.tex}

\end{document}\endinput

% Stuff below configures compilation for AucTeX in Emacs

% Local Variables:
% TeX-master-file: t
% eval: (setq TeX-command-list  (assq-delete-all (car (assoc "BibTeX" TeX-command-list)) TeX-command-list))
% eval: (setq TeX-command-list  (assq-delete-all (car (assoc "Biber"  TeX-command-list)) TeX-command-list))
% eval: (setq TeX-command-list  (remove '("BibTeX" "%(bibtex) ../LaTeX/%s"    TeX-run-BibTeX nil t :help "Run BibTeX") TeX-command-list))
% eval: (setq TeX-command-list  (remove '("BibTeX" "bibtex ../LaTeX/%s"    TeX-run-BibTeX nil t :help "Run BibTeX") TeX-command-list))
% eval: (add-to-list 'TeX-command-list '("BibTeX" "bibtex LaTeX/%s" TeX-run-BibTeX nil t                                                                              :help "Run BibTeX") t)
% eval: (add-to-list 'TeX-command-list '("BibTeX" "bibtex LaTeX/%s" TeX-run-BibTeX nil (plain-tex-mode latex-mode doctex-mode ams-tex-mode texinfo-mode context-mode) :help "Run BibTeX") t)
% TeX-PDF-mode: t
% TeX-file-line-error: t
% TeX-debug-warnings: t
% LaTeX-command-style: (("" "%(PDF)%(latex) %(file-line-error) %(extraopts) -output-directory=LaTeX %S%(PDFout)"))
% TeX-source-correlate-mode: t
% TeX-parse-self: t
% TeX-parse-all-errors: t
% eval: (cond ((string-equal system-type "darwin") (progn (setq TeX-view-program-list '(("Skim" "/Applications/Skim.app/Contents/SharedSupport/displayline -b %n LaTeX/%o %b"))))))
% eval: (cond ((string-equal system-type "gnu/linux") (progn (setq TeX-view-program-list '(("Evince" "evince --page-index=%(outpage) LaTeX/%o"))))))
% eval: (cond ((string-equal system-type "gnu/linux") (progn (setq TeX-view-program-selection '((output-pdf "Evince"))))))
% End:
