#!/bin/sh
# Print the PR template with this branch's commits filled in.
# Usage: sh pr_body.sh <template> [base-ref]
template="$1"
base="${2:-origin/main}"
while IFS= read -r line; do
  case "$line" in
    *"<!-- commits -->"*) git log --reverse --no-merges --format='- %s' "$base"..HEAD ;;
    *) printf '%s\n' "$line" ;;
  esac
done < "$template"
