#!/bin/bash

# run to connect the .git/hooks directory to local repository .githooks directroy
ln -sf $PWD/.githooks/* $PWD/.git/hooks/
find . -type f ! -name "*.*" -exec chmod +x {} +
