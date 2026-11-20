#!/usr/bin/env bash
# NEXMAP installer for Termux and Linux. Run from the cloned repository.
set -eu

SOURCE_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if [ ! -f "$SOURCE_DIR/main.py" ]; then
  echo "Error: main.py was not found. Run this installer from the NEXMAP repository." >&2
  exit 1
fi

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "Error: Python 3 is required. Install it with your system package manager first." >&2
  exit 1
fi

"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' || {
  echo "Error: NEXMAP requires Python 3.10 or newer." >&2
  exit 1
}

# Termux provides PREFIX; on regular Linux use the per-user local bin directory.
if [ -n "${PREFIX:-}" ] && [ -d "$PREFIX/bin" ]; then
  BIN_DIR="$PREFIX/bin"
else
  BIN_DIR="$HOME/.local/bin"
fi

mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/nexmap"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env sh
exec "$PYTHON_BIN" "$SOURCE_DIR/main.py" "\$@"
EOF
chmod 755 "$LAUNCHER"

echo "NEXMAP command installed: $LAUNCHER"
case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *)
    echo "Note: $BIN_DIR is not currently in PATH."
    if [ -n "${PREFIX:-}" ]; then
      echo 'Run: export PATH="$PREFIX/bin:$PATH"'
    else
      echo 'Add this line to ~/.profile: export PATH="$HOME/.local/bin:$PATH"'
    fi
    ;;
esac

echo "Try: nexmap --help"
echo "Source directory: $SOURCE_DIR"
