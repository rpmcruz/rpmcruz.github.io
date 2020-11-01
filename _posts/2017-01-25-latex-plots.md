---
layout: post
title: Latex plots
category: latex
---

Many attempts exist to make graphical plots look well and integrated with the rest of the latex document.

Some people modify the fonts of R or Matplotlib to match those of latex. Others export the plot into a latex tikz primitives.

Personally, I recommend pgfplots for simple data.

This is a sophisticated package built on top of tikz.

These are a couple of examples from two manuscripts of mine:

```LaTeX
\begin{tikzpicture}
\begin{axis}[
    width=0.5\linewidth,
    height=5cm,
    axis lines=left,
    grid=both,
    legend style={draw=none, font=\scriptsize},
    legend cell align=left,
    legend style={at={(0.5,-0.25)}, anchor=north},
    label style={font=\scriptsize},
    ticklabel style={font=\tiny},
    xlabel style={at={(0.5, 0.03)}},
    ylabel style={at={(0.08, 0.5)}},
    ymin=0,
    xmin=0,
    ymax=400,
    xmax=140,
    xtick={0,20,...,140},
    ytick={0,50,...,400},
    xlabel=Users ($n$),
    ylabel=Running Time (seconds),
    legend entries={{"{{"}}$m=8$, $p=1$ (Centralized)}, {$m=8$, $p=2$ (Distributed)}, {$m=8$, $p=4$ (Distributed){{"}}"}},
]
\addplot[color=blue, mark=*, thick, mark options={scale=0.5}] coordinates {
    (25, 1) (50, 1) (75, 18) (100, 100) (125, 380) };
\addplot[color=red, mark=asterisk, thick, mark options={scale=0.5}, dashdotted] coordinates {
    (25, 1) (50, 1) (75, 15) (100, 65) (125, 190) };
\addplot[color=black!40!green, mark=diamond*, thick, mark options={scale=0.5}, dashed] coordinates {
    (25, 1) (50, 1) (75, 10) (100, 35) (125, 140) };
\end{axis}
\end{tikzpicture}
```

![scatter](/imgs/blog/2017-01-25/04-pgfplots-scatter.png)

```LaTeX
\begin{tikzpicture}
\begin{axis}[
    width=10cm,
    height=4cm,
    axis lines=left,
    axis x line=middle,
    xlabel=$\widehat{\rho}$,
    ticklabel style={font=\small},
    legend style={font=\small, cells={anchor=west}, at=({1,1})}]
\addplot[very thick, domain=0:1] {exp(x-0.10)-1};
\draw (axis cs:0,1.4) node[font=\small, anchor=west] {Loss};
\end{axis}
\end{tikzpicture}
```

![plot](/imgs/blog/2017-01-25/04-pgfplots-plot.png)

There is another cool latex package called pgfplotstable, which is an extension to support importing CSV files and others. Furthermore, tables can be directly built from such files. But I haven't yet used that package.
