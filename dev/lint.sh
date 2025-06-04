#!/usr/bin/env bash
# NOTE: If script is sourced, enables via shopt recursive globbing with `**`
# Prefer to run this script (i.e. `./dev/lint.sh`) rather than `source` it

ROOTDIR="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"
PYLINTRC="$ROOTDIR/.pylintrc"
PYVER=$(python - <<<'import sys;v=sys.version_info;print(v[0]*100+v[1])')

# Enable recursive globbing
shopt -s globstar

# If Python < 3.12, remove the new option and schedule a restore
if (( PYVER < 312 )); then
    cp -- "$PYLINTRC" "${PYLINTRC}.orig"
    sed -i '/max-positional-arguments/d' "$PYLINTRC"
    trap 'mv -- "${PYLINTRC}.orig" "$PYLINTRC"' EXIT
fi

# Lint Python project
pylint evaluate_tools/**/*.py main.py
