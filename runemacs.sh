#!/bin/sh

# Only ttys have $WINDOWID set correctly? Firefox doesn't, anyway.

if ! which wmctrl >/dev/null 2>&1; then
  me=$(basename $0)
  echo "$me: wmctrl not found; aborting." >&2
  exit 1
fi

if wmctrl -lx | grep 'emacs.Emacs'; then
    emacsclient -n -a "" "$@"
    wmctrl -xa emacs.Emacs
else
    emacsclient -nc -a "" "$@"
fi
