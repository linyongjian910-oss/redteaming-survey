# Scoped detail review

The five annotations are addressed without moving the six panels, coordinator,
or main evidence pipelines. The `canvas-design` skill supplies spacing and visual
hierarchy criteria; `ml-paper-writing` supplies vector, notation, and scientific
consistency checks. Existing content and manuscript files remain unchanged.

| Annotation | Change | Review criterion |
| --- | --- | --- |
| No legend | The adaptive label sits in empty plot space; its sample stroke and the footer legend are removed. | No legend substitutes for a direct label. |
| Poison symbol | A skull-marked poison bottle replaces the lightning bolt. | The silhouette denotes poisoning and clears the state circle. |
| Empty disclosure stage | Document, checked-shield, and megaphone icons replace empty timeline circles. | Proof, remediation, and advisory stages have visible meanings. |
| Red vector origin | The red transfer vector starts at the left-bottom intersection of D and E. | Its start equals the coordinate origin. |
| Modality axis origin | M starts at that same intersection and follows the projected depth direction. | D, E, M, and the red vector share one origin. |

The SVG coordinate origin is `(254, 1431)`. Endpoint checks read the exported
geometry, independently of the generator. Bounds checks include mathematical
outlines and arrowheads. Color is reinforced by solid and dashed strokes and
direct labels. PDF and grayscale render inspection cover small icons, text
clearance, clipping, and runtime arrow direction.

Verified in this revision: all 124 text/math bounds clear lines and arrowheads;
all four transfer arrows share the same origin; the modality direction is
parallel to cube depth. The exported PDF contains vector artwork, and both
color and grayscale panel renders were inspected. The native draw.io export
was also inspected after regeneration.

The later coordinator-visibility annotation is addressed by changing all six
hub links from pale dashed strokes to solid gray-blue strokes (`#69849C`,
3.2 design units). Their routes, attachment positions, and arrow-free coordination
semantics are preserved.

The selected coordinator treatment replaces the ellipse with the third proposal's
rounded rectangle, omitting its two perimeter arrows. The six solid links meet
three ports on each horizontal edge; module positions and all evidence-flow
arrows remain unchanged.

## Content consistency for a later revision

The supplied illustration brief defines M as modality. The current manuscript
at `7-9.tex:389` defines M as target foundation models. This semantic difference
is recorded for the content review; the requested modality axis is preserved in
this layout revision. No new references, empirical results, or guarantees are
introduced.
