#!/bin/bash
set -euo pipefail

# Cleanup Validation Worktrees
# Archives old validation worktrees and removes them from git

# Configuration
WORKTREE_BASE="/home/donbr/ai2026/lifesciences-deepagents-worktrees"
ARCHIVE_DIR="/home/donbr/ai2026/lifesciences-deepagents/archives/validation-runs"
DAYS_TO_KEEP=${1:-7}  # Default: keep last 7 days

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Calculate cutoff date
CUTOFF_DATE=$(date -d "${DAYS_TO_KEEP} days ago" +%Y-%m-%d 2>/dev/null || date -v-${DAYS_TO_KEEP}d +%Y-%m-%d)

log_info "Cleaning up validation worktrees older than ${CUTOFF_DATE}"
log_info "Worktree base: ${WORKTREE_BASE}"
log_info "Archive directory: ${ARCHIVE_DIR}"

# Create archive directory
mkdir -p "${ARCHIVE_DIR}"

# Find and process old worktrees
ARCHIVED_COUNT=0
REMOVED_COUNT=0

if [[ ! -d "${WORKTREE_BASE}" ]]; then
  log_warning "Worktree base directory does not exist: ${WORKTREE_BASE}"
  exit 0
fi

for worktree in "${WORKTREE_BASE}"/cq-validation-*; do
  if [[ ! -d "$worktree" ]]; then
    continue
  fi

  # Extract date from worktree name (format: cq-validation-YYYY-MM-DDTHH-MM)
  worktree_name=$(basename "$worktree")
  worktree_date=$(echo "$worktree_name" | grep -oP '\d{4}-\d{2}-\d{2}' || echo "")

  if [[ -z "$worktree_date" ]]; then
    log_warning "Cannot parse date from worktree: $worktree_name"
    continue
  fi

  # Compare dates
  if [[ "$worktree_date" < "$CUTOFF_DATE" ]]; then
    log_info "Processing old worktree: $worktree_name (date: $worktree_date)"

    # Archive outputs if they exist
    if [[ -d "$worktree/output" ]]; then
      archive_file="${ARCHIVE_DIR}/${worktree_name}.tar.gz"
      log_info "Archiving outputs to: $archive_file"

      tar -czf "$archive_file" -C "$worktree" output

      if [[ -f "$archive_file" ]]; then
        log_success "Archived: $archive_file"
        ((ARCHIVED_COUNT++))
      else
        log_error "Failed to create archive: $archive_file"
        continue
      fi
    fi

    # Remove worktree
    log_info "Removing worktree: $worktree"
    git worktree remove "$worktree" --force

    if [[ $? -eq 0 ]]; then
      log_success "Removed: $worktree"
      ((REMOVED_COUNT++))
    else
      log_error "Failed to remove worktree: $worktree"
    fi
  else
    log_info "Keeping recent worktree: $worktree_name (date: $worktree_date)"
  fi
done

# Summary
echo ""
echo "=========================================="
echo "CLEANUP SUMMARY"
echo "=========================================="
echo "Archived: ${ARCHIVED_COUNT} worktrees"
echo "Removed: ${REMOVED_COUNT} worktrees"
echo "Archive location: ${ARCHIVE_DIR}"
echo "=========================================="

# List remaining worktrees
echo ""
log_info "Remaining worktrees:"
git worktree list | grep "cq-validation" || echo "  (none)"
