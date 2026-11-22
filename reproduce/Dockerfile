# The handout's computed results, in a container:
#
#   docker build --load -f reproduce/Dockerfile -t tractable-buffer-stock .
#   docker run --rm tractable-buffer-stock
#
# To keep the executed notebook and its figures, add -v "$PWD/reproduce/output:/handout/reproduce/output" to the
# run. Building the PDF and the web page needs TeX Live as well; see README.md.
FROM python:3.12-slim

# pip needs git to install the book's package from GitHub.
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
COPY binder/requirements.txt /handout/binder/requirements.txt
RUN pip install --no-cache-dir -r /handout/binder/requirements.txt nbconvert ipykernel

COPY TractableBufferStock.ipynb /handout/
COPY reproduce/computed.sh /handout/reproduce/
WORKDIR /handout
CMD ["bash", "reproduce/computed.sh"]
