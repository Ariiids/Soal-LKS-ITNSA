#!/bin/bash

# Check grading scripts are there
# TODO: unsafe check, if decompression fails!
if [ ! -d /usr/local/share/grading/bin ]; then
    echo "Please enter the passphrase to decrypt the marking scripts"
    if ! unzip -qq /usr/local/share/grading/wsc_grading.zip -d /usr/local/share/grading/bin; then
        rm -rf /usr/local/share/grading/bin
    fi
fi
# Run grading script
/usr/local/share/grading/bin/grading.py "$@"