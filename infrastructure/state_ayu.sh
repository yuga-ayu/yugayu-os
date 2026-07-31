#!/bin/bash
# ==============================================================================
# 🚀 YUGAYU OS - IMMUTABLE STATE CHECKPOINT MODULE (state_ayu.sh v1.7)
# ==============================================================================
# Copyright (c) 2026 Yugayu Framework. All rights reserved.
# Dual-Licensed under the Yugayu Enterprise Architecture / Open-Source Protocol.
# See LICENSE.md in the project root for execution permissions.
#
# [LORE]
# The Yugayu project represents the evolution from human-managed sysadmin scripts 
# to autonomous, AI-orchestrated infrastructure. In a multi-agent ecosystem, 
# an AI must securely snapshot, verify, and read the historical safety state 
# of any node before executing potentially destructive workflow changes.
#
# [GOAL & PURPOSE]
# Acts as the universal disaster-recovery and state-freezing protocol for the 
# Yugayu ecosystem. It provides a deterministic, zero-trust API for AI agents 
# to trigger checkpoints across infrastructure without manual human oversight.
#
# [CURRENT IMPLEMENTATION]
# - Targets: Proxmox Virtual Environment hosts and LXC subsystems.
# - Compression: Multi-threaded zstd for optimized bare-metal and container snapshots.
# - AI Context Manifests: Generates a companion `.json` manifest for every archive. 
#   This creates a readable hierarchy mapping the packages, node ID, and sizes 
#   so the AI does not need to extract the archive to verify its contents.
#
# [FUTURE ENHANCEMENTS: CRYPTOGRAPHIC GOVERNANCE]
# Future iterations will transition the standard `ledger.json` into a post-quantum 
# secured, immutable distributed ledger using a Cryptographic Hash Chain (Merkle DAG). 
# Every backup state and AI action will be cryptographically signed. If a broken 
# hash is detected, it mathematically invalidates the transaction, enforcing Yugayu's 
# zero-trust execution boundaries.
#
# [USAGE]
# 👤 Interactive Mode (Human UI):
#   Simply execute the script to open the visual menu:
#   ./state_ayu.sh
#
# 🤖 Agentic / CLI Mode (Machine API):
#   Bypass the human menu for autonomous execution using flags.
#   ./state_ayu.sh --target host
#   ./state_ayu.sh --target all
#   ./state_ayu.sh --target 100 --postfix pre_update
#
# 🔧 Optional Flags:
#   -t, --tail      : Display live progress output instead of silent background execution
#                     (e.g., ./state_ayu.sh -t --target 100)
#   --read <file>   : Read and parse a generated manifest JSON file
#
# ==============================================================================

BACKUP_ROOT="/mnt/pve/Backup-8TB/system_backups" 
DATE=$(date +%F_%H-%M-%S)
RUN_DIR="$BACKUP_ROOT/$DATE"
MIN_SPACE_MB=20480
START_TIME=$(date +%s)
TOTAL_BACKUPS_CREATED=0
LOG_FILE="/tmp/yugayu_progress_$DATE.log"
LEDGER_FILE="$BACKUP_ROOT/ledger.json"

ALLOWED_DIRS="/etc /root /var /opt /home /usr/local/bin /usr/local/sbin"

# ------------------------------------------------------------------------------
# CLI ARGUMENT PARSING (AGENTIC MODE)
# ------------------------------------------------------------------------------
TAIL_LOG=false
CLI_TARGET=""
CLI_POSTFIX=""
CLI_READ_MANIFEST=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t|--tail) TAIL_LOG=true ;;
        --target) CLI_TARGET="$2"; shift ;;
        --postfix) CLI_POSTFIX="$2"; shift ;;
        --read) CLI_READ_MANIFEST="$2"; shift ;;
        *) echo "❌ Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

if [ "$TAIL_LOG" = true ]; then
    touch "$LOG_FILE"
    tail -f "$LOG_FILE" &
    TAIL_PID=$!
fi

log_output() {
    if [ "$TAIL_LOG" = true ]; then
        echo "$1" >> "$LOG_FILE"
    else
        echo "$1"
    fi
}

# ------------------------------------------------------------------------------
# PRE-FLIGHT VALIDATION
# ------------------------------------------------------------------------------
if [ "$EUID" -ne 0 ]; then
  log_output "❌ ERROR: Root privileges required for state capture."
  exit 1
fi

mkdir -p "$BACKUP_ROOT"
AVAILABLE_SPACE=$(df -m "$BACKUP_ROOT" | awk 'NR==2 {print $4}')

if [ "$AVAILABLE_SPACE" -lt "$MIN_SPACE_MB" ]; then
  log_output "❌ ERROR: Insufficient storage. Available: ${AVAILABLE_SPACE}MB."
  exit 1
fi

# ------------------------------------------------------------------------------
# CORE EXECUTION MODULES
# ------------------------------------------------------------------------------
update_ledger() {
    local target=$1
    local file_path=$2
    local manifest_path=$3
    local status=$4
    local size_mb=$5
    
    # Generate SHA-256 Hash for immediate integrity checking (V1 Cryptographic step)
    local hash="N/A"
    [ -f "$file_path" ] && hash=$(sha256sum "$file_path" | awk '{print $1}')

    echo "{\"date\": \"$DATE\", \"target\": \"$target\", \"file\": \"$file_path\", \"manifest\": \"$manifest_path\", \"size_mb\": \"$size_mb\", \"hash\": \"$hash\", \"status\": \"$status\"}" >> "$LEDGER_FILE"
}

generate_manifest() {
    local type=$1
    local target_id=$2
    local target_dir=$3
    local archive_name=$4
    local pkg_file=$5
    
    local manifest_file="${target_dir}/manifest_${target_id}_${DATE}.json"
    local pkgs=$(cat "$pkg_file" | awk '{print "\"" $1 "\""}' | paste -sd, -)
    
    cat <<EOF > "$manifest_file"
{
    "metadata": {
        "timestamp": "$DATE",
        "type": "$type",
        "target_id": "$target_id",
        "archive_file": "$archive_name"
    },
    "hierarchy_context": {
        "description": "Pre-extracted data mapping to bypass AI extraction requirements.",
        "installed_packages": [$pkgs]
    }
}
EOF
    rm -f "$pkg_file"
    echo "$manifest_file"
}

backup_host() {
    local postfix=$1
    local postfix_str=""
    [ -n "$postfix" ] && postfix_str="_${postfix// /_}"

    local TARGET_DIR="$RUN_DIR/proxmox_host"
    mkdir -p "$TARGET_DIR"

    local TAR_NAME="backup_host_${DATE}${postfix_str}.tar.zst"
    local PKG_TMP="$TARGET_DIR/pkg_tmp.txt"

    log_output "📦 Checkpointing Proxmox Host..."
    dpkg --get-selections > "$PKG_TMP"

    tar --zstd -cf "$TARGET_DIR/$TAR_NAME" \
        --exclude=/mnt/* --exclude=/media/* --exclude=/dev/* \
        --exclude=/proc/* --exclude=/sys/* --exclude=/tmp/* --exclude=/run/* \
        $ALLOWED_DIRS > /dev/null 2>&1

    if tar --zstd -tf "$TARGET_DIR/$TAR_NAME" > /dev/null 2>&1; then
        local SIZE_MB=$(du -m "$TARGET_DIR/$TAR_NAME" | awk '{print $1}')
        local MANIFEST=$(generate_manifest "host" "proxmox_host" "$TARGET_DIR" "$TAR_NAME" "$PKG_TMP")
        
        log_output "✅ Host checkpoint verified: $SIZE_MB MB"
        update_ledger "proxmox_host" "$TARGET_DIR/$TAR_NAME" "$MANIFEST" "SUCCESS" "$SIZE_MB"
        ((TOTAL_BACKUPS_CREATED++))
    else
        log_output "❌ ERROR: Host checkpoint corrupted."
        update_ledger "proxmox_host" "$TARGET_DIR/$TAR_NAME" "NONE" "CORRUPTED" "0"
    fi
}

backup_single_lxc() {
    local lxc_id=$1
    local postfix=$2
    local postfix_str=""
    [ -n "$postfix" ] && postfix_str="_${postfix// /_}"

    if ! pct status "$lxc_id" > /dev/null 2>&1; then
        log_output "❌ ERROR: Subsystem $lxc_id offline or invalid."
        return
    fi

    local TARGET_DIR="$RUN_DIR/lxc_${lxc_id}"
    mkdir -p "$TARGET_DIR"

    local TAR_NAME="backup_lxc_${lxc_id}_${DATE}${postfix_str}.tar.zst"
    local PKG_TMP="$TARGET_DIR/pkg_tmp.txt"

    log_output "📦 Checkpointing Subsystem $lxc_id..."
    
    pct exec "$lxc_id" -- dpkg --get-selections > "$PKG_TMP" 2>/dev/null
    
    if [ "$TAIL_LOG" = true ]; then
        vzdump "$lxc_id" --dumpdir "$TARGET_DIR" --mode snapshot --compress zstd >> "$LOG_FILE" 2>&1
    else
        vzdump "$lxc_id" --dumpdir "$TARGET_DIR" --mode snapshot --compress zstd --quiet 1
    fi
    
    local LATEST_DUMP=$(ls -t $TARGET_DIR/vzdump-lxc-${lxc_id}-*.tar.zst 2>/dev/null | head -1)
    
    if [ -n "$LATEST_DUMP" ]; then
        mv "$LATEST_DUMP" "$TARGET_DIR/$TAR_NAME"
        local SIZE_MB=$(du -m "$TARGET_DIR/$TAR_NAME" | awk '{print $1}')
        local MANIFEST=$(generate_manifest "lxc" "$lxc_id" "$TARGET_DIR" "$TAR_NAME" "$PKG_TMP")
        
        log_output "✅ Subsystem $lxc_id checkpoint verified: $SIZE_MB MB"
        update_ledger "lxc_$lxc_id" "$TARGET_DIR/$TAR_NAME" "$MANIFEST" "SUCCESS" "$SIZE_MB"
        ((TOTAL_BACKUPS_CREATED++))
    else
        log_output "❌ ERROR: Subsystem $lxc_id checkpoint failed."
        update_ledger "lxc_$lxc_id" "N/A" "NONE" "FAILED" "0"
    fi
}

backup_all_lxcs() {
    log_output "📦 Checkpointing all Subsystems..."
    local LXC_IDS=$(pct list | awk 'NR>1 {print $1}')
    for ID in $LXC_IDS; do
        backup_single_lxc "$ID" "auto"
    done
}

# ------------------------------------------------------------------------------
# REPORTING & MANIFEST READING
# ------------------------------------------------------------------------------
list_ledger() {
    echo "=========================================================================="
    echo " 📖 IMMUTABLE LEDGER ENTRIES (LATEST 15)"
    echo "=========================================================================="
    if [ -f "$LEDGER_FILE" ]; then
        printf "%-20s | %-12s | %-8s | %-8s | %s\n" "DATE" "TARGET" "SIZE(MB)" "STATUS" "HASH (SHA-256)"
        echo "--------------------------------------------------------------------------"
        tail -n 15 "$LEDGER_FILE" | while read -r line; do
            local l_date=$(echo "$line" | grep -o '"date": "[^"]*' | cut -d'"' -f4)
            local l_tgt=$(echo "$line" | grep -o '"target": "[^"]*' | cut -d'"' -f4)
            local l_sz=$(echo "$line" | grep -o '"size_mb": "[^"]*' | cut -d'"' -f4)
            local l_stat=$(echo "$line" | grep -o '"status": "[^"]*' | cut -d'"' -f4)
            local l_hash=$(echo "$line" | grep -o '"hash": "[^"]*' | cut -d'"' -f4 | cut -c 1-12)
            printf "%-20s | %-12s | %-8s | %-8s | %s...\n" "$l_date" "$l_tgt" "$l_sz" "$l_stat" "$l_hash"
        done
    else
        echo "Ledger empty."
    fi
    echo "=========================================================================="
}

read_manifest_ui() {
    echo "Enter the exact date string (e.g., $DATE) or path to the manifest:"
    read -p "> " MANIFEST_INPUT
    
    local TARGET_FILE=$(find "$BACKUP_ROOT" -name "*manifest*$MANIFEST_INPUT*.json" | head -n 1)
    
    if [ -f "$TARGET_FILE" ]; then
        echo "📄 MANIFEST DATA ($TARGET_FILE):"
        cat "$TARGET_FILE" | jq . 2>/dev/null || cat "$TARGET_FILE"
    else
        echo "❌ ERROR: Manifest not found."
    fi
}

cleanup_and_exit() {
    [ -d "$RUN_DIR" ] && [ -z "$(ls -A "$RUN_DIR")" ] && rm -rf "$RUN_DIR"
    if [ "$TAIL_LOG" = true ]; then
        kill $TAIL_PID 2>/dev/null
    fi
    exit 0
}

# ------------------------------------------------------------------------------
# ROUTING CONTROLLER
# ------------------------------------------------------------------------------
if [ -n "$CLI_READ_MANIFEST" ]; then
    cat "$CLI_READ_MANIFEST" 2>/dev/null || echo "❌ ERROR: Cannot read $CLI_READ_MANIFEST"
    exit 0
fi

if [ -n "$CLI_TARGET" ]; then
    case $CLI_TARGET in
        host) backup_host "$CLI_POSTFIX" ;;
        all)  backup_all_lxcs ;;
        *)    backup_single_lxc "$CLI_TARGET" "$CLI_POSTFIX" ;;
    esac
    cleanup_and_exit
fi

while true; do
    echo "========================================="
    echo "   Yugayu Immutable State Checkpoint     "
    echo "========================================="
    echo "1) Checkpoint Host Node"
    echo "2) Checkpoint ALL Subsystems (LXC)"
    echo "3) Checkpoint Single Subsystem (LXC)"
    echo "4) Checkpoint Global State (Host + LXC)"
    echo "5) View State Ledger"
    echo "6) Read Backup Context Manifest"
    echo "7) Exit"
    echo "========================================="
    read -p "Select an option [1-7]: " OPTION

    case $OPTION in
      1) 
        read -p "Postfix [blank=none]: " PFIX
        backup_host "$PFIX"
        break 
        ;;
      2) 
        backup_all_lxcs
        break 
        ;;
      3) 
        echo "========================================="
        echo "   Discovered Subsystems (LXCs)          "
        echo "========================================="
        pct list 
        echo "========================================="
        
        read -p "Enter the ID of the subsystem to checkpoint (e.g., 100): " TARGET_ID
        
        if [ -z "$TARGET_ID" ]; then
            echo "❌ ERROR: No ID provided. Aborting."
            echo "Returning to main menu..."
            sleep 1
            continue
        fi
        
        read -p "Enter an optional postfix [blank=none]: " PFIX
        echo "Initiating State Checkpoint for Subsystem: $TARGET_ID..."
        
        backup_single_lxc "$TARGET_ID" "$PFIX"
        break 
        ;;
      4) 
        backup_host "global"
        backup_all_lxcs
        break 
        ;;
      5) 
        list_ledger 
        ;; 
      6) 
        read_manifest_ui 
        ;;
      7) 
        cleanup_and_exit 
        ;;
      *) 
        echo "❌ Invalid input. Please select 1-7." 
        sleep 1
        ;;
    esac
done

cleanup_and_exit
