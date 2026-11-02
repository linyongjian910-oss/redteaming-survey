# Closed-loop research agenda illustration

An original, editable scientific figure based on the supplied illustration brief.
The manuscript and existing figures are unchanged.

Figure prose uses objective declarative statements. Oracle components are named
by their functions; arbitrary A/B/C labels, workflow step numbers, and imperative
instructions are omitted. Module names, mathematical variables, and axes retain
concise scientific labels. All labels are direct annotations; there is no legend.

## Deliverables

- `closed_loop_research_agenda.svg`: primary vector artwork with live prose and outlined math.
- `closed_loop_research_agenda.pdf`: vector publication export, 14 inches wide.
- `closed_loop_research_agenda.png`: 5120 × 3620 white-background image.
- `closed_loop_research_agenda.drawio`: editable native shapes, labels, and connectors.
- `build_figure.py`: reproducible generator for the SVG and draw.io source.
- `math_renderer.py`: LaTeX-to-vector renderer for formula assets.
- `assets/brick_wall.svg`: text-free brick-wall isolation symbol.
- `assets/math/`: cached vector formula assets and their baseline metrics.
- `DESIGN_PHILOSOPHY.md`: visual principles used for the scoped detail revision.
- `DETAIL_REVIEW.md`: five-annotation review and the remaining notation issue.
- `review_figure.py`: exported-geometry and arrowhead clearance checks.

The PNG and PDF use the primary SVG artwork. The native draw.io rendering can
differ slightly in font placement and corner radii.

The oracle isolation boundary is shown by a brick-wall icon. It has no text
label. Mathematical symbols, subscripts, superscripts, and the stacked richness
fraction are rendered by LaTeX and embedded as vector outlines. The draw.io
version embeds the same formula assets; each formula cell retains its LaTeX
expression in the `data-source` attribute. Formula edits are made in the generator.

The discovery curve label occupies empty plot space without a sample stroke. Oracle evidence crosses
the wall through a white-backed arrow with a larger arrowhead. The transfer
formula and modality labels sit outside the wireframe. All three transfer axes
and the red transfer vector start at the left-bottom intersection. The modality
axis is parallel to the projected depth edges. Agent injection uses a skull-marked
poison-bottle badge; the rollback loop uses side ports and an outer lane that
clears the state captions. Disclosure stages use proof, fix, and advisory icons
instead of empty circle placeholders.
The six coordinator links use solid gray-blue strokes with increased contrast
and weight, connecting the module rows to the central rounded frame. The frame
uses the third proposed treatment with its two perimeter arrows removed.

## Scientific notation

The brief's expression `S_0 = S_obs + f_1^2/(2 f_2)` is preserved. Its label is
corrected from “Chao-92” to “Chao1 lower bound.” This expression assumes `f_2 > 0`;
zero-doubleton cases require an appropriate adjusted estimator. See Chao et al.,
[A Nonparametric Lower Bound for the Number of Species Shared by Multiple Communities](https://pmc.ncbi.nlm.nih.gov/articles/PMC2899312/).
The curves are conceptual and do not represent measured benchmark results.
Using richness estimators for adaptive mechanism discovery is a research agenda,
not a demonstrated statistical guarantee in this figure.

The transfer panel uses the brief's definition of M as modality. The three
spatial axes are D, M, and E; the parallel wireframe slices represent A. This is
a schematic projection of a four-axis tensor, not a four-dimensional plot.

## Suggested caption

Closed-loop research agenda for automated red teaming. Six open frontiers connect
adaptive mechanism discovery, independent oracle arbitration, durable remediation,
cross-modal threat transfer, reversible agent execution, and governed disclosure.
The upper and lower evidence pipelines share a continuous assurance coordinator.
Governed disclosures and regression findings renew discovery seeds and transfer
tests. Micro-schematics illustrate proposed mechanisms rather than empirical results.

## Rebuild

Run `python3 build_figure.py`. The first build of each formula requires a TeX Live
installation with `latex`, `dvisvgm`, `standalone`, and `amsmath`. Subsequent builds
reuse the cached SVG formulas. Optional Pillow support improves mixed text/math
alignment on macOS. Export with:

```sh
rsvg-convert -w 5120 -o closed_loop_research_agenda.png closed_loop_research_agenda.svg
rsvg-convert -f pdf -w 14in -o closed_loop_research_agenda.pdf closed_loop_research_agenda.svg
```

The full specification is dense. At 14 inches wide, the smallest 18-unit labels
are approximately 7.1 pt. For a typical 7-inch two-column paper width, use a
full-page landscape figure or simplify the annotations before typesetting.

## Coordinator alternatives

`hub_alternatives/coordinator_comparison.pdf` and the matching PNG compare three
same-scale central regions: coordination band, chamfered frame, and loop track.
`hub_alternatives/coordinator_full_variants.pdf` contains three corresponding
full-figure pages in that order. These files preserve the three original proposals;
the main figure uses the selected third treatment without perimeter arrows.

The generator accepts `--hub-style ellipse|band|chamfer|loop|rounded` and
`--output-dir PATH` to build treatments separately. The default is `rounded`.
