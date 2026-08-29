# Figure 7 design notes: remediation as a closed loop

## Files and reproducibility

- `fig7_remediation_taxonomy.dot` records the editable graph topology.
- `fig7_remediation_taxonomy.tex` is the deterministic TikZ renderer used for the supplied PDF, SVG, and PNG. It fixes the branch positions for a 7.1-inch two-column figure; Graphviz `dot` was unavailable in the provided environment.
- `fig7_remediation_taxonomy.svg` and `fig7_remediation_taxonomy.pdf` are vector publication assets. `fig7_remediation_taxonomy.png` is a 300 dpi review preview.

Render the figure again with:

```bash
pdflatex -interaction=nonstopmode -halt-on-error fig7_remediation_taxonomy.tex
latex -interaction=nonstopmode -halt-on-error fig7_remediation_taxonomy.tex
dvisvgm --libgs=/opt/homebrew/lib/libgs.dylib \
  --output=fig7_remediation_taxonomy.svg fig7_remediation_taxonomy.dvi
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -r300 \
  -sOutputFile=fig7_remediation_taxonomy.png fig7_remediation_taxonomy.pdf
```

## Graph structure

The left-to-right source path is:

`Automated Red-Team Failure Discovery` -> `Confirmed / Reproducible Failure`.

The confirmed case branches to four remediation levels:

1. Training-time safety tuning.
2. Runtime safety control.
3. Application-level system controls.
4. Continuous testing.

Continuous testing contains two visible subcomponents: **Persistence** retains and replays verified failures, while **Renewal** discovers new attacks or refreshes evaluation artifacts. Its feedback edge returns retained and newly discovered failures to discovery, making the closed loop explicit.

## Design rationale

The composition uses a compact taxonomy grammar: a neutral source pair, four softly colored remediation families, concise mechanism lines, and smaller representative-work labels. Thin gray arrows encode only causal reuse or feedback. The white inset boxes distinguish persistence from renewal without adding decoration. The restrained pastel palette separates branches while remaining suitable for grayscale print and a two-column survey figure.

## Mapping to Section 7

| Figure branch | Survey section | Meaning |
|---|---|---|
| Training-Time Safety Tuning | 7.1 | Reuse traces as supervision and update model parameters. |
| Runtime Safety Control | 7.2 | Use judgments as input-, decoding-, or output-time interventions. |
| Application-Level System Controls | 7.3 | Separate model choices from authority and limit external effects. |
| Continuous Testing | 7.4 | Preserve failures for replay and renew attack or evaluation artifacts. |

## Suggested caption

**Figure 7. Closed-loop remediation after automated red-team failure discovery.** Confirmed, reproducible failures can be reused for training-time tuning, runtime safety control, application-level containment, or continuous testing. Continuous testing combines persistence of verified failures with renewal of attacks or evaluation artifacts, feeding both retained and newly discovered failures back into red-team discovery.

## Suggested LaTeX inclusion

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=0.98\textwidth]{fig/fig7_remediation_taxonomy.pdf}
  \caption{Closed-loop remediation after automated red-team failure discovery. Confirmed, reproducible failures can be reused for training-time tuning, runtime safety control, application-level containment, or continuous testing. Continuous testing combines persistence of verified failures with renewal of attacks or evaluation artifacts, feeding both retained and newly discovered failures back into red-team discovery.}
  \label{fig:remediation-loop}
\end{figure*}
```
