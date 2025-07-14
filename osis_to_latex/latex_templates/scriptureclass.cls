% scriptureclass.cls
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{scriptureclass}[2025/05/25 Scripture typesetting class]

% Base class
\LoadClass{book}

% === PACKAGES ===
\RequirePackage[
    letterpaper,
    bindingoffset=0.2in,
    left=1.5in,
    right=1.5in,
    top=1in,
    bottom=1in,
    footskip=.25in
]{geometry}

\RequirePackage[hang]{footmisc}
% \RequirePackage{mathpazo}
\RequirePackage{newpxtext}
\RequirePackage{multicol}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{zref-user,zref-abspage,zref-lastpage}
\RequirePackage{xstring}
\RequirePackage{chngcntr}
\RequirePackage{enumitem}  % For flexible list customization
\RequirePackage{silence}
\RequirePackage{graphicx}


% === LAYOUT ===
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\thepage}
\fancyhead[RO]{\thepage}
\fancyhead[LO]{\rightmark--\leftmark}
\fancyhead[RE]{\rightmark--\leftmark}
\renewcommand{\headrulewidth}{0pt}

\setlength{\columnsep}{20pt}
\setlength{\columnseprule}{0.4pt}

\widowpenalty=10000
\clubpenalty=10000

% === SECTIONING ===
\makeatletter
\def\chapter{\@startsection{chapter}{1}{0mm}{-4mm}{3mm}{\normalfont\centering CHAPTER }}
\makeatother

% === VERSE AND FOOTNOTE MACROS ===

\newcounter{book}
\newcommand{\currbookshort}{}
\def\book#1#2{%
  \refstepcounter{book}%
  \setcounter{chapter}{0}%
  \renewcommand{\currbookshort}{#2}%
  \section*{\centering\normalfont\huge \MakeUppercase{#1}}%
  \addcontentsline{toc}{section}{#2}%
}

\newcommand{\booksectiontitle}[1]{%
  \begin{center}
    {\MakeUppercase{#1}}
  \end{center}
}

\newcommand{\booksectionsummary}[1]{%
  #1
}

\newcounter{verse}[chapter]
\newcounter{subfn}[verse]

\newcommand{\verseref}{%
  \currbookshort{}~\thechapter:\arabic{verse}%
}
\newcommand\firstverseref{}
\newcommand\lastverseref{}

\AddToHook{shipout/before}{\gdef\firstverseref{}}

\newcommand{\markverse}{%
  \StrGobbleLeft{\verseref}{0}[\currverseref]%
  \ifx\firstverseref\empty%
    \gdef\firstverseref{\currverseref}%
  \fi%
  \gdef\lastverseref{\currverseref}%
  \markboth{\firstverseref}{\lastverseref}%
}

\makeatletter
\newcommand{\bibleverse}[1]{%
    \refstepcounter{verse}%
    \setcounter{subfn}{0}%
    \ifnum\value{verse}=1%
        \par\noindent\markverse#1%
    \else%
        \par\noindent\textnormal{\arabic{verse}}\hspace{0.4em}\markverse#1%
    \fi%
}
\makeatother

\newcommand{\chapterheader}[1]{%
  \vspace{1pt}\textit{#1}\vspace{1pt}%
}

\makeatletter
\newcommand{\vfn}[1]{%
  \refstepcounter{subfn}%
  \textsuperscript{\alph{subfn}}%
  \begingroup%
    \ifnum\value{verse}=1%
        \ifnum\value{subfn}=1%
            \renewcommand{\thefootnote}{\textbf{\small{\thechapter}}\,\arabic{verse}\alph{subfn}}%
        \else%
            \renewcommand{\thefootnote}{\phantom{\small{\thechapter}}\,\arabic{verse}\alph{subfn}}%
        \fi%
    \else%
        \renewcommand{\thefootnote}{\phantom{\small{\thechapter}}\,\arabic{verse}\alph{subfn}}%
    \fi%
    \renewcommand\@makefnmark{\hbox{\textsuperscript{\thefootnote}}}%
    \footnotetext{\hspace{0.5em}#1}%
  \endgroup%
\ignorespaces}
\makeatother

% Custom list environment to mimic OSIS <list>
\newlist{osislist}{itemize}{1}
\setlist[osislist,1]{
    label=--, % default bullet, can be changed
    leftmargin=2em,
    itemsep=0.5em,
    topsep=1em
}
% Custom command to represent a <label> (definition term or heading)
\newcommand{\listlabel}[1]{\textbf{#1}\par\vspace{0.5em}}

% Unicode/font fixes
\DeclareUnicodeCharacter{02B9}{\textquotesingle}
% \makeatletter
% \DeclareFontShape{OT1}{ppl}{m}{scit}{<-> ssub * ppl/m/sc}{}%
% \makeatother



\WarningFilter{multicol}{I moved some lines to the next page}
\WarningFilter{multicol}{Underfull \hbox (badness 10000) in paragraph}

\newlength{\inlineimageheight}
\settoheight{\inlineimageheight}{B}

