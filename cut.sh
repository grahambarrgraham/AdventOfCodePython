#!/bin/bash

echo "creating : day$1.kt"
sed  "s|dayn|day$1|g" "day_n.py" | sed "s|/day/n|/day/$1|g" > "day$1.py"

echo "creating : input/day$1_sample"
touch "input/day$1_sample"

echo "creating : input/day$1"
touch "input/day$1"

SESSION_ID='53616c7465645f5f919990cf7f29b434e81f5acfd849e4f7876ab9e314de0f9653b902edfa43f9dca525c16304a525295008d060267d871594ff0c28fc5f12de'

echo "loading from : https://adventofcode.com/2022/day/$1/input to input/day$1"

curl "https://adventofcode.com/2022/day/$1/input" \
  -H 'authority: adventofcode.com' \
  -H 'cache-control: max-age=0' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-user: ?1' \
  -H 'sec-fetch-dest: document' \
  -H 'referer: https://adventofcode.com/2021/day/1' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H "cookie: _ga=GA1.2.510370946.1605541548; session=$SESSION_ID; _gid=GA1.2.1838548585.1606854098" \
  --compressed > "input/day$1"
