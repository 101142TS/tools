#!/bin/bash
diff -rqa ./101142ts/translated/ ./jr/translated/ | grep -v "<clinit>" > calc_result.txt