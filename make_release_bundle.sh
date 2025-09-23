#!/usr/bin/env bash
set -euo pipefail

# make_release_bundle.sh
# Build a local release bundle with docs + notebook (adjust paths as needed).

TAG="${1:-local}"
ROOT_DIR="$(pwd)"
OUT_DIR="${ROOT_DIR}/release_assets"
BUNDLE="NMSI_NS_e_Release_${TAG}.zip"

echo "[info] Tag: ${TAG}"
echo "[info] Root: ${ROOT_DIR}"
rm -rf "${OUT_DIR}"
mkdir -p "${OUT_DIR}"

# Collect files (edit list as the repo evolves)
FILES=(
  "NMSI_NS_e_Operator_Cap1-10_EN.docx"
  "NMSI_NS_e_Operator_Anexe_Tehnice_EN.docx"
  "NMSI_NS_e_Operator_Anexe_Numerice_EN.docx"
  "notebooks/NMSI_NS_e_Notebook_Skeleton.ipynb"
  "config.yaml"
  "README.md"
)

for f in "${FILES[@]}"; do
  if [[ -f "${f}" ]]; then
    echo "[add] ${f}"
    cp "${f}" "${OUT_DIR}/"
  else
    echo "[skip] ${f} (not found)"
  fi
done

pushd "${OUT_DIR}" >/dev/null
zip -r "../${BUNDLE}" .
popd >/dev/null

echo "[done] Created ${BUNDLE} in ${ROOT_DIR}"
