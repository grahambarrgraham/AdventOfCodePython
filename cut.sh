#!/bin/bash

YEAR="${2:-2024}"
SESSION_ID='53616c7465645f5fc7e9d66574d544cf2ba77a5dc52957e1a5c0a1bbe62f804e4f5c7964b2e5245e6a0b25684d68704c040c361a4b5938624c4ffb3bf30d7435'

echo "creating : $YEAR/day$1.py"
sed  "s|dayn|day$1|g" "day_n.py" | sed "s|/day/n|/day/$1|g" > "$YEAR/day$1.py"

echo "creating : $YEAR/input/day$1_sample"
touch "$YEAR/input/day$1_sample"

echo "creating : $YEAR/input/day$1"
touch "$YEAR/input/day$1"

echo "loading from : https://adventofcode.com/$YEAR/day/$1/input to input/day$1"

curl "https://adventofcode.com/$YEAR/day/$1/input" \
  -H 'authority: adventofcode.com' \
  -H 'cache-control: max-age=0' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-user: ?1' \
  -H 'sec-fetch-dest: document' \
  -H "referer: https://adventofcode.com/$YEAR/day/1" \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H "cookie: _ga=GA1.2.510370946.1605541548; session=$SESSION_ID; _gid=GA1.2.1838548585.1606854098" \
  --compressed > "$YEAR/input/day$1"

