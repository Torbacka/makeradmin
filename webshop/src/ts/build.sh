#!/bin/bash
set -e
tsc --outDir /tmp/ts_output
rollup /tmp/ts_output/shop.js --file ../static/js/shop.js --format iife -m
rollup /tmp/ts_output/register.js --file ../static/js/register.js --format iife -m
rollup /tmp/ts_output/product_edit.js --file ../static/js/product_edit.js --format iife -m
rollup /tmp/ts_output/product.js --file ../static/js/product.js --format iife -m
rollup /tmp/ts_output/history.js --file ../static/js/history.js --format iife -m
rollup /tmp/ts_output/cartpage.js --file ../static/js/cartpage.js --format iife -m
rm -rf /tmp/ts_output