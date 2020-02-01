\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{base}
\LoadClass[a4paper]{scrartcl}

% -----------------------------------------------------------------------
% Required packages

\RequirePackage[ngerman]{babel}
\RequirePackage{amssymb}
\RequirePackage{epsfig}
\RequirePackage{graphicx}
\RequirePackage{moreverb}
\RequirePackage{parskip}


% -----------------------------------------------------------------------
% define page layout using typearea

\KOMAoptions{headinclude=true}
\KOMAoptions{footinclude=true}
\areaset{16cm}{27cm}
% -----------------------------------------------------------------------
% define page style
\pagestyle{plain}
\thispagestyle{plain}

% -----------------------------------------------------------------------
% Macro für das Abgabeblatt
\newcommand{\Abgabeblatt}[8]
          {\Arbblatt{#1}{#2}{#3}{#4}{#5}{#6}{#7}}

\newcommand{\grenzop}[3]{\mathop{#1}\limits^{#2}_{#3}}

\newcommand{\langrechtspfeil}[2]{\grenzop{\longrightarrow}{#1}{#2}}
\newcommand{\bob}[0]{\hspace*{\fill}$\Box$}

% -----------------------------------------------------------------------

\newcommand{\Arbblatt}[7]
{
\begin{tabular}[t]{lr}
  \begin{tabular}[t]{l}
    \textbf{Applied Computational Engines}\hspace{5ex} SoSe 2018 \\
    Abgabe: {#2}\\
    
    \hspace{50ex} \\
    {\Huge\textsf{{#1}}} \hspace{10ex} \\  \\
  \end{tabular}
  &
  \begin{tabular}[t]{l}
      \textbf{Gruppe:} \\ 
      {#5}\\
      {#6}\\
      {#7}\\
  \end{tabular} \\[2ex]
\end{tabular}\\
\rule{\linewidth}{1pt}
}

%%% Local Variables: 
%%% mode: latex
%%% TeX-master: t
%%% End: 





\newcommand*{\qed}{\hfill\ensuremath{\square}}%<Paste>
\newcommand*{\qedb}{\hfill\ensuremath{\blacksquare}}%

