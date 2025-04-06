#!/bin/sh

categories=()

for file in $(ls); do
    if [ -d $file ]; then
        categories+=("$file")
    fi
done

prompt="category (values: ${categories[@]})> "

read -p "$prompt" category
found=false
for c in ${categories[@]}; do
    if [ "$c" = "$category" ]; then
        found=true
        break
    fi
done

if ! $found; then
    echo "Invalid category."
    exit 1
fi
read -p "author> " author
read -p "difficulty (values: warmup easy medium hard tough)> " diff

difficulties=("warmup" "easy" "medium" "hard" "tough")
for d in "${difficulties[@]}"; do
  if [ "$diff" = "$d" ]; then
    valid=true
    break
  fi
done

if [ "$valid" = false ]; then
  echo "Invalid difficulty."
  exit 1
fi

read -p "challenge name> " name

mkdir -p "$category/$diff-[$name]/challenge"
mkdir -p "$category/$diff-[$name]/solution"
touch "$category/$diff-[$name]/solution/.gitkeep"
touch "$category/$diff-[$name]/challenge/.gitkeep"

cat ./challenge.yml | \
    sed "s/{{name}}/$name/g" | \
    sed "s/{{difficulty}}/{{$diff}}/g" | \
    sed "s/{{author}}/$author/g" | \
    sed "s/{{category}}/category/g" > "$category/$diff-[$name]/challenge.yml"

