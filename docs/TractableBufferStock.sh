#!/bin/bash
make4ht --utf8 --config TractableBufferStock.cfg --format html5 TractableBufferStock "svg" "-cunihtf -utf8"
cat page-style.css | cat - TractableBufferStock-generated-by-make4ht.css > TractableBufferStock-page-style.css && mv TractableBufferStock-page-style.css TractableBufferStock.css
cp TractableBufferStock.html index.html
