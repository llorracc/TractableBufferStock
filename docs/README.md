# TractableBufferStock

The source of *A Tractable Model of Buffer Stock Saving*, lecture notes by Christopher D. Carroll, kept in step
with the [chapter of the same name](https://intertemporal-choice.github.io/content/consumption/tractablebufferstock)
in the book *Intertemporal Choice*. The chapter is the source: changes are made there first.

- **Read it** as a [web page](https://llorracc.github.io/TractableBufferStock/) or a [PDF](TractableBufferStock.pdf).
- **The figures** are drawn by [`TractableBufferStock.ipynb`](TractableBufferStock.ipynb), a copy of the chapter's
  notebook, which solves the model itself; its results have been checked against those of HARK's
  [`TractableConsumerType`](https://github.com/econ-ark/HARK/blob/main/examples/TractableBufferStockModel/TractableConsumerType.ipynb).
  Run it in your browser, with nothing to install, in
  [JupyterLite](https://intertemporal-choice.github.io/lite/notebooks/index.html?path=TractableBufferStock.ipynb),
  or open it in [Colab](https://colab.research.google.com/github/llorracc/TractableBufferStock/blob/main/TractableBufferStock.ipynb)
  or [Binder](https://mybinder.org/v2/gh/llorracc/TractableBufferStock/main?labpath=TractableBufferStock.ipynb).

## Building and checking

| What | How | Needs |
|---|---|---|
| The PDF | `./reproduce.sh` | TeX Live, with `latexmk` |
| The web page, in `docs/` | copy `TractableBufferStock.{tex,pdf,bbl,blg,bib}` into `docs/`, then `bash docs/TractableBufferStock.sh` | TeX Live, with `make4ht` and `dvisvgm` |
| The computed results: the notebook's checks and figures | `reproduce/computed.sh`, or in a container, `docker build --load -f reproduce/Dockerfile -t tractable-buffer-stock . && docker run --rm tractable-buffer-stock` | Python 3.12, `uv` or Docker |
| Where the handout differs from the chapter | `./check-book-sync.py` | Python 3 |
| Objects written with their notation macros | `./check-object-macros.py` | Python 3 |

`docs/` is the web page's folder. It also holds copies of this repository's other files.
