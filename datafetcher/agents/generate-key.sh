#!/bin/bash
gpg --batch --generate-key <<EOF
Key-Type: RSA
Key-Length: 2048
Subkey-Type: ELG-E
Subkey-Length: 2048
Name-Real: server
Name-Comment: server
Name-Email: dev@example.com
Expire-Date: 0
Passphrase: b!Y2nFvys^n%e3P8tU9dnD%LAs6mVVs$F8GGfFeC
EOF
