#!/bin/sh
# Download the original Bridge Squad from noclipepe's site and build the multi-level version locally.
set -e
cd "$(dirname "$0")"
mkdir -p original
curl -fsSL https://noclipepe.pages.dev/bridge/ -o original/bridge.html
curl -fsSL https://noclipepe.pages.dev/bridge/three.min.js -o three.min.js
python3 build.py original/bridge.html .
echo "Play: python3 -m http.server 8731  then open http://127.0.0.1:8731/?level=1 (or ?flood=1 for Flood Rescue)"
