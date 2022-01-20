#!/bin/bash

# run to connect the hook to local repository

cd ..
ln -sf $PWD/.githooks/* $PWD/.git/hooks/
chmod +x $PWD/.githooks/commit-msg
