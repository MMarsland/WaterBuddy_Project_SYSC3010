#!/bin/bash

git config core.hooksPath .githooks
find .githooks -type f ! -name "*.*" -exec chmod +x {} +
read -p "Press any key to exit..."