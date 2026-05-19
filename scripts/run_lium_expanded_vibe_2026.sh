#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: scripts/run_lium_expanded_vibe_2026.sh <pod-name-or-index>" >&2
  exit 2
fi

POD="$1"
ROOT="$(git rev-parse --show-toplevel)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
ARCHIVE="/tmp/hrm-text-sense-probes-expanded-${STAMP}.tar"
REMOTE_ARCHIVE="/root/hrm-text-sense-probes.tar"
REMOTE_DIR="/root/hrm-text-sense-probes"
LOCAL_PULL_DIR="${ROOT}/runs/pulled"

mkdir -p "${LOCAL_PULL_DIR}"
git -C "${ROOT}" archive --format=tar --output="${ARCHIVE}" HEAD

lium scp "${POD}" "${ARCHIVE}" "${REMOTE_ARCHIVE}"
UPLOAD_CHECK="$(lium exec "${POD}" "test -s ${REMOTE_ARCHIVE} && echo __UPLOAD_OK__" || true)"
if ! grep -q "__UPLOAD_OK__" <<<"${UPLOAD_CHECK}"; then
  echo "upload did not produce ${REMOTE_ARCHIVE} on ${POD}" >&2
  exit 1
fi

lium exec "${POD}" "rm -rf ${REMOTE_DIR} && mkdir -p ${REMOTE_DIR} && tar -xf ${REMOTE_ARCHIVE} -C ${REMOTE_DIR}"
lium exec "${POD}" "chmod +x ${REMOTE_DIR}/scripts/remote_expanded_vibe_2026.sh"
lium exec "${POD}" "${REMOTE_DIR}/scripts/remote_expanded_vibe_2026.sh"

REMOTE_BUNDLE="$(
  lium exec "${POD}" "find /root -maxdepth 1 -name 'vibe-2026-expanded-120-harness-*.tgz' -type f -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-" \
    | awk '/^\/root\/vibe-2026-expanded-120-harness-.*\.tgz$/ {print; exit}' \
    | tr -d '\r'
)"
if [ -z "${REMOTE_BUNDLE}" ]; then
  echo "remote run did not produce a /root/vibe-2026-expanded-120-harness-*.tgz bundle" >&2
  exit 1
fi

LOCAL_BUNDLE="${LOCAL_PULL_DIR}/$(basename "${REMOTE_BUNDLE}")"
rm -f "${LOCAL_BUNDLE}"
lium scp "${POD}" "${REMOTE_BUNDLE}" "${LOCAL_PULL_DIR}/" --download
if [ ! -s "${LOCAL_BUNDLE}" ]; then
  echo "download did not produce ${LOCAL_BUNDLE}" >&2
  exit 1
fi

echo "Pulled ${REMOTE_BUNDLE} into ${LOCAL_PULL_DIR}"
