"""Render real LaTeX math as portable vector outlines for figure labels."""
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parent / 'assets' / 'math'

@lru_cache(maxsize=None)
def render_math(expression, bold=False):
    key = sha256((expression + str(bold)).encode()).hexdigest()[:14]
    ASSETS.mkdir(parents=True, exist_ok=True)
    svg_path = ASSETS / (key + '.svg')
    metrics_path = ASSETS / (key + '.metrics')
    if not svg_path.exists() or not metrics_path.exists():
        formula = r'\boldsymbol{' + expression + '}' if bold else expression
        source = r'''\documentclass[border=0pt]{standalone}
\usepackage{amsmath,amssymb}
\newsavebox{\figuremath}
\begin{document}
\sbox{\figuremath}{$\displaystyle FORMULA$}
\typeout{FIGUREMETRICS:\the\wd\figuremath:\the\ht\figuremath:\the\dp\figuremath}
\usebox{\figuremath}
\end{document}
'''.replace('FORMULA', formula)
        with tempfile.TemporaryDirectory(prefix='closed-loop-math-') as directory:
            work = Path(directory)
            (work / 'formula.tex').write_text(source)
            result = subprocess.run(['/Library/TeX/texbin/latex', '-interaction=nonstopmode', '-halt-on-error', 'formula.tex'], cwd=work, text=True, capture_output=True, check=True)
            metrics = re.search(r'FIGUREMETRICS:([\d.]+)pt:([\d.]+)pt:([\d.]+)pt', result.stdout)
            if not metrics:
                raise ValueError('LaTeX did not return formula dimensions')
            subprocess.run(['/Library/TeX/texbin/dvisvgm', '--no-fonts', '--bbox=preview', '--output=formula.svg', 'formula.dvi'], cwd=work, text=True, capture_output=True, check=True)
            svg_path.write_text((work / 'formula.svg').read_text())
            metrics_path.write_text(' '.join(metrics.groups()))
    width, height, depth = map(float, metrics_path.read_text().split())
    return svg_path.read_text(), width, height, depth
