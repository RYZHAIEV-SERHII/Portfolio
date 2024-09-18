#!/bin/bash

cd ..

awk -F "=" '{
    if ($1 != "" && substr($1, 1, 1) != "#")
        print $1 "="
    else
        print $0
}' .env > .env.example

echo "Done!"
