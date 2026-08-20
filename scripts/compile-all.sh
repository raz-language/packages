#!/usr/bin/env bash
# Copyright 2026 Mario Vinciguerra
# SPDX-License-Identifier: Apache-2.0

set -uo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
package_root=$(CDPATH= cd -- "$script_dir/../sources" && pwd)
compiler=${RAZ_COMPILER:-raz}
clean_first=0

if [[ ${1:-} == "--clean" ]]; then
    clean_first=1
elif [[ $# -ne 0 ]]; then
    echo "usage: $0 [--clean]" >&2
    exit 2
fi

if [[ $compiler == */* ]]; then
    if [[ ! -x $compiler ]]; then
        echo "error: RAZ_COMPILER is not executable: $compiler" >&2
        exit 2
    fi
else
    resolved_compiler=$(command -v -- "$compiler" 2>/dev/null || true)
    if [[ -z $resolved_compiler ]]; then
        echo "error: Raz compiler not found; set RAZ_COMPILER=/path/to/raz" >&2
        exit 2
    fi
    compiler=$resolved_compiler
fi

pass_count=0
fail_count=0

while IFS= read -r package_dir; do
    package_name=${package_dir##*/}

    if [[ $clean_first -eq 1 ]]; then
        (cd "$package_dir" && "$compiler" clean >/dev/null) || {
            printf 'FAIL  %-16s clean\n' "$package_name"
            fail_count=$((fail_count + 1))
            continue
        }
    fi

    if (cd "$package_dir" && "$compiler" check raz.toml); then
        printf 'PASS  %s\n' "$package_name"
        pass_count=$((pass_count + 1))
    else
        printf 'FAIL  %s\n' "$package_name"
        fail_count=$((fail_count + 1))
    fi
done < <(find "$package_root" -mindepth 1 -maxdepth 1 -type d -print | sort)

printf '\nPackage compile check: %d passed, %d failed\n' "$pass_count" "$fail_count"

if [[ $fail_count -ne 0 ]]; then
    exit 1
fi
