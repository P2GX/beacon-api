#!/usr/bin/env bash
#
# Sync Beacon v2 schemas and compare against current models for drift detection.
#
# Usage:
#   ./scripts/sync_beacon_schemas.sh [--version VERSION] [--clean]
#
# Options:
#   --version VERSION   Specific release tag (default: latest)
#   --clean             Remove downloaded schemas and re-download
#
# This script:
#   1. Downloads beacon-v2 release from GitHub
#   2. Bundles schemas (resolves $ref)
#   3. Compares against src/beacon_api/models/ to detect drift
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Directories
TMP_DIR="$PROJECT_ROOT/tmp"
SCHEMAS_DIR="$TMP_DIR/beacon-v2-schemas"
BUNDLED_DIR="$TMP_DIR/bundled_schemas"

# GitHub release info
GITHUB_REPO="ga4gh-beacon/beacon-v2"
DEFAULT_VERSION="latest"

# Parse arguments
VERSION="$DEFAULT_VERSION"
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --version)
            VERSION="$2"
            shift 2
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        -h|--help)
            head -17 "$0" | tail -15
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Clean if requested
if [[ "$CLEAN" == true ]]; then
    log_info "Cleaning tmp directory..."
    rm -rf "$TMP_DIR"
fi

# Create directories
mkdir -p "$TMP_DIR" "$SCHEMAS_DIR" "$BUNDLED_DIR"

# Get release info
get_release_info() {
    local version="$1"
    if [[ "$version" == "latest" ]]; then
        curl -s "https://api.github.com/repos/$GITHUB_REPO/releases/latest"
    else
        curl -s "https://api.github.com/repos/$GITHUB_REPO/releases/tags/$version"
    fi
}

# Download and extract release
download_schemas() {
    local version="$1"

    log_info "Fetching release info for: $version"
    local release_info
    release_info=$(get_release_info "$version")

    local tag_name
    tag_name=$(echo "$release_info" | jq -r '.tag_name')

    if [[ -z "$tag_name" ]]; then
        log_error "Could not find release: $version"
        exit 1
    fi

    log_info "Found release: $tag_name"

    # Check if already downloaded
    local version_file="$SCHEMAS_DIR/.version"
    if [[ -f "$version_file" ]] && [[ "$(cat "$version_file")" == "$tag_name" ]]; then
        log_info "Schemas already downloaded for $tag_name"
        return 0
    fi

    # Download tarball
    local tarball_url="https://github.com/$GITHUB_REPO/archive/refs/tags/$tag_name.tar.gz"
    local tarball_path="$TMP_DIR/beacon-v2-$tag_name.tar.gz"

    log_info "Downloading: $tarball_url"
    curl -L -o "$tarball_path" "$tarball_url"

    # Extract
    log_info "Extracting schemas..."
    rm -rf "$SCHEMAS_DIR"/*
    tar -xzf "$tarball_path" -C "$SCHEMAS_DIR" --strip-components=1

    # Save version
    echo "$tag_name" > "$version_file"

    # Cleanup tarball
    rm -f "$tarball_path"

    log_info "Schemas extracted to: $SCHEMAS_DIR"
}

# Bundle schemas
bundle_schemas() {
    log_info "Bundling schemas..."

    # Update the bundler to use downloaded schemas
    export BEACON_V2_ROOT="$SCHEMAS_DIR"

    cd "$PROJECT_ROOT"
    node scripts/bundle_schemas.js
}

# Compare models
compare_models() {
    log_info "Comparing models against schema..."
    echo ""

    cd "$PROJECT_ROOT"
    uv run python scripts/compare_models.py
}

# Main
main() {
    echo "========================================"
    echo "Beacon v2 Schema Sync"
    echo "========================================"
    echo ""

    download_schemas "$VERSION"
    echo ""

    bundle_schemas
    echo ""

    compare_models

    echo ""
    log_info "Done!"
}

main
