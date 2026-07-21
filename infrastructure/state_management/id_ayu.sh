#!/bin/bash
# ==============================================================================
# id_ayu.sh : Universal Discovery & Context Onboarding Probe (v1.3)
# ==============================================================================
# [AI CONTEXT]
# PROTOCOL: Yugayu Framework
# ENGINE: id_ayu_v1.3 (Agentic Context Engine)
# MODULE_ROLE: Discovery and deterministic onboarding of isolated subsystems.
# PURPOSE: Interrogate bare-metal hosts, GPUs, storage arrays, and containers
#          to establish a ground-truth JSON baseline for AI orchestration.
# OUTPUT: Strict JSON payload (infrastructure_state.json) mapping hardware reality.
# ==============================================================================

OUTPUT_FILE="/root/infrastructure_state.json"
TEMP_DATA="/tmp/yugayu_state.txt"
STORAGE_JSON="/tmp/yugayu_storage.json"
> $TEMP_DATA

# 1. Gather Host Baseline
CPU_MODEL=$(lscpu | grep "Model name:" | sed 's/Model name:\s*//')
CPU_CORES=$(lscpu | grep "^CPU(s):" | awk '{print $2}')
TOTAL_RAM=$(free -h | awk '/^Mem:/ {print $2}')
HOST_IP=$(ip route get 1 | awk '{print $7; exit}')

echo "HOST_CPU_MODEL|$CPU_MODEL" >> $TEMP_DATA
echo "HOST_CPU_CORES|$CPU_CORES" >> $TEMP_DATA
echo "HOST_RAM|$TOTAL_RAM" >> $TEMP_DATA
echo "HOST_IP|$HOST_IP" >> $TEMP_DATA

# 2. Gather GPUs natively
lspci | grep -i -E "vga|3d|display" | while read -r line; do
    echo "HOST_GPU|$line" >> $TEMP_DATA
done

# 3. Gather Storage Topology natively as JSON
lsblk -J > $STORAGE_JSON

# 4. Iterate through Subsystems (LXCs)
for ct in $(pct list | awk 'NR>1 {print $1}'); do
    HOSTNAME=$(pct config $ct | awk -F: '/^hostname/ {print $2}' | xargs)
    OSTYPE=$(pct config $ct | awk -F: '/^ostype/ {print $2}' | xargs)
    CORES=$(pct config $ct | awk -F: '/^cores/ {print $2}' | xargs)
    MEMORY=$(pct config $ct | awk -F: '/^memory/ {print $2}' | xargs)
    IP=$(pct config $ct | awk -F= '/^net0/ {print $2}' | cut -d/ -f1 | cut -d, -f1 | xargs)

    # Fallbacks for empty limits
    if [ -z "$CORES" ]; then CORES="unlimited"; fi
    if [ -z "$MEMORY" ]; then MEMORY="unlimited"; fi
    if [ -z "$IP" ]; then IP="none"; fi

    # Extract and decode Proxmox Container Notes
    RAW_DESC=$(pct config $ct | grep '^description:' | sed 's/^description: //')
    if [ -n "$RAW_DESC" ]; then
        NOTES=$(python3 -c "import urllib.parse, sys; print(urllib.parse.unquote(sys.argv[1]).replace('\n', ' '))" "$RAW_DESC")
    else
        NOTES="none"
    fi

    # Check power state before executing internal probes
    STATUS=$(pct status $ct | awk '{print $2}')

    if [ "$STATUS" == "running" ]; then
        # Ensure Semantic Intent (Lore) exists
        LORE_CHECK=$(pct exec $ct -- test -f /root/ayu_lore.md && echo "EXISTS" || echo "MISSING")

        if [ "$LORE_CHECK" == "MISSING" ]; then
            DEFAULT_LORE="SYSTEM INTENT PENDING. Awaiting Yugayu protocol classification."
            pct exec $ct -- bash -c "echo \"$DEFAULT_LORE\" > /root/ayu_lore.md"
            LORE_TEXT="$DEFAULT_LORE"
        else
            LORE_TEXT=$(pct exec $ct -- cat /root/ayu_lore.md | tr '\n' ' ')
        fi

        # Dynamic Raw Port Sweep
        RAW_PORTS=$(pct exec $ct -- ss -tuln | awk 'NR>1 {if (match($5, /:[0-9]+$/)) {port = substr($5, RSTART+1, RLENGTH-1); if (port < 60000) print port;}}' | sort -nu | paste -sd, -)
        if [ -z "$RAW_PORTS" ]; then RAW_PORTS="none"; fi
    else
        LORE_TEXT="NODE_OFFLINE"
        RAW_PORTS="none"
    fi

    echo "LXC|$ct|$HOSTNAME|$OSTYPE|$CORES|$MEMORY|$IP|$NOTES|$LORE_TEXT|$RAW_PORTS" >> $TEMP_DATA
done

# 5. Python JSON Compiler
python3 -c '
import json, datetime

data = {
    "_system_metadata": {
        "protocol": "Yugayu Framework",
        "engine": "id_ayu_v1.3",
        "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "telemetry": "Deterministic Infrastructure State for autonomous onboarding."
    },
    "host_node": {
        "cpu_model": "",
        "cpu_cores": "",
        "memory_total": "",
        "management_ip": "",
        "gpus": [],
        "storage_topology": []
    },
    "sub_systems": []
}

# Load Storage JSON directly from Linux lsblk natively
try:
    with open("'$STORAGE_JSON'", "r") as f:
        data["host_node"]["storage_topology"] = json.load(f).get("blockdevices", [])
except Exception:
    data["host_node"]["storage_topology"] = []

# Parse Temp Data for Host and LXCs
with open("'$TEMP_DATA'", "r") as f:
    for line in f:
        parts = line.strip().split("|")
        if parts[0] == "HOST_CPU_MODEL": data["host_node"]["cpu_model"] = parts[1]
        elif parts[0] == "HOST_CPU_CORES": data["host_node"]["cpu_cores"] = parts[1]
        elif parts[0] == "HOST_RAM": data["host_node"]["memory_total"] = parts[1]
        elif parts[0] == "HOST_IP": data["host_node"]["management_ip"] = parts[1]
        elif parts[0] == "HOST_GPU": data["host_node"]["gpus"].append(parts[1])
        elif parts[0] == "LXC":
            ports = [int(p) for p in parts[9].split(",")] if parts[9] != "none" and parts[9] != "" else []
            data["sub_systems"].append({
                "node_id": parts[1],
                "designation": parts[2],
                "os_template": parts[3],
                "allocated_cores": parts[4],
                "allocated_memory_mb": parts[5],
                "network_ipv4": parts[6],
                "management_notes": parts[7] if parts[7] != "none" else None,
                "semantic_intent": parts[8],
                "active_sockets": ports
            })

with open("'$OUTPUT_FILE'", "w") as f:
    json.dump(data, f, indent=4)
'

rm $TEMP_DATA
rm $STORAGE_JSON
echo "Discovery sequence complete. Protocol state compiled to: $OUTPUT_FILE"
