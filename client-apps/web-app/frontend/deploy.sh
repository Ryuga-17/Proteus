#!/usr/bin/env bash
# Deploy this web app to Vercel.
# Run from this directory: ./deploy.sh
# First time: run `npx vercel login` in terminal, then run this script again.

set -e
cd "$(dirname "$0")"

echo "Building..."
npm run build

echo "Deploying to Vercel..."
npx vercel --prebuilt --yes

echo "Done. Check the URL printed above."
