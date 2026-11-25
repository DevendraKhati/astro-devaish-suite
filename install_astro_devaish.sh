#!/usr/bin/env bash
# ==============================================================================
# Astro DevAish Portable Installer (Skills + Global CLI Commands + Python Package)
# Installs:
#   1. Skills: vedic-jyotish, vedic-numerology, astro-devaish-suite, jyotish-suite
#      into ~/.gemini/skills/ and ~/.claude/skills/
#   2. Global Python Package & CLI Tools (astro-devaish, vedic-jyotish,
#      vedic-numerology, jyotish, numerology) onto PATH (~/.local/bin & /opt/antigravity/bin)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_SLUG="DevendraKhati/astro-devaish-suite"
REPO_URL="https://github.com/${REPO_SLUG}"

echo "=============================================================================="
echo " 🕉️  Astro DevAish Master Suite v2.0 — Vedic Jyotish & Anka-Jyotish Installer"
echo " ⭐  GitHub Repository: ${REPO_URL}"
echo "=============================================================================="
echo "👉 If this suite helps your Vedic Astrology & Numerology workflow, please"
echo "   STAR the repository on GitHub: ${REPO_URL}"
if command -v gh >/dev/null 2>&1; then
    if gh api --method PUT "/user/starred/${REPO_SLUG}" >/dev/null 2>&1; then
        echo "⭐ Thank you! Automatically starred ${REPO_SLUG} via GitHub CLI."
    fi
fi
echo ""

# 1. Install Python dependencies & package globally
if command -v pip3 >/dev/null 2>&1; then
    PIP_CMD="pip3"
elif command -v pip >/dev/null 2>&1; then
    PIP_CMD="pip"
else
    PIP_CMD="python3 -m pip"
fi

if [ -d "$SCRIPT_DIR/astro-devaish-pkg" ]; then
    PKG_DIR="$SCRIPT_DIR/astro-devaish-pkg"
elif [ -d "/home/antigravity/astro-devaish-pkg" ]; then
    PKG_DIR="/home/antigravity/astro-devaish-pkg"
else
    PKG_DIR=""
fi

if [ -n "$PKG_DIR" ]; then
    echo "[1/3] Installing global Python package from $PKG_DIR ..."
    $PIP_CMD install --break-system-packages -e "$PKG_DIR" 2>/dev/null || $PIP_CMD install -e "$PKG_DIR"
fi

# 2. Install CLI symlinks in ~/.local/bin and /opt/antigravity/bin (if writable)
mkdir -p "$HOME/.local/bin"
for BIN_TARGET in "$HOME/.local/bin" "/opt/antigravity/bin"; do
    if [ -d "$BIN_TARGET" ] && [ -w "$BIN_TARGET" ] && [ -n "$PKG_DIR" ]; then
        chmod +x "$PKG_DIR/jyotish.py" "$PKG_DIR/numerology.py" "$PKG_DIR/astro_devaish.py" "$PKG_DIR/vedastro_client.py"
        ln -sf "$PKG_DIR/jyotish.py" "$BIN_TARGET/jyotish"
        ln -sf "$PKG_DIR/jyotish.py" "$BIN_TARGET/vedic-jyotish"
        ln -sf "$PKG_DIR/numerology.py" "$BIN_TARGET/numerology"
        ln -sf "$PKG_DIR/numerology.py" "$BIN_TARGET/vedic-numerology"
        ln -sf "$PKG_DIR/astro_devaish.py" "$BIN_TARGET/astro-devaish"
        ln -sf "$PKG_DIR/astro_devaish.py" "$BIN_TARGET/astro-devaish-suite"
        echo "[2/3] Linked global CLI commands into $BIN_TARGET"
    fi
done

# Ensure ~/.local/bin is in ~/.bashrc and ~/.profile
for RC in "$HOME/.bashrc" "$HOME/.profile" "$HOME/.zshrc"; do
    if [ -f "$RC" ] && ! grep -q '.local/bin' "$RC" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC"
    fi
done

# 3. Install Skills into ~/.gemini/skills and ~/.claude/skills
SKILLS_SRC=""
if [ -d "$SCRIPT_DIR/skills" ]; then
    SKILLS_SRC="$SCRIPT_DIR/skills"
elif [ -d "/home/antigravity/skills_build" ]; then
    SKILLS_SRC="/home/antigravity/skills_build"
fi

if [ -n "$SKILLS_SRC" ]; then
    for DEST_ROOT in "$HOME/.gemini/skills" "$HOME/.claude/skills"; do
        mkdir -p "$DEST_ROOT"
        for SK in vedic-jyotish vedic-numerology astro-devaish-suite jyotish-suite; do
            if [ -d "$SKILLS_SRC/$SK" ]; then
                rm -rf "$DEST_ROOT/$SK"
                cp -r "$SKILLS_SRC/$SK" "$DEST_ROOT/$SK"
                chmod +x "$DEST_ROOT/$SK/scripts/"*.py 2>/dev/null || true
            fi
        done
        echo "[3/3] Installed skills into $DEST_ROOT"
    done
fi

echo "=== Astro DevAish Installation Complete! ==="
echo "You can now run from ANY directory:"
echo "  astro-devaish --name \"Your Name\" --dob YYYY-MM-DD --tob HH:MM --lat LAT --lon LON"
echo "  vedic-jyotish chart --dob YYYY-MM-DD --tob HH:MM --lat LAT --lon LON"
echo "  vedic-numerology --name \"Your Name\" --dob YYYY-MM-DD"
