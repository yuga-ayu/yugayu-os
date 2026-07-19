#!/bin/bash
# ==============================================================================
# id_ayu.sh : Universal Discovery & Context Onboarding Probe
# ==============================================================================
# [AI CONTEXT]
# PROTOCOL: Yugayu Framework
# MODULE_ROLE: Discovery and deterministic onboarding of isolated subsystems.
# PURPOSE: Interrogate bare-metal hosts and containers to establish a ground-truth 
#          baseline (IP, CPU, active network sockets) and semantic design intent 
#          before an AI agent assumes management.
# OUTPUT: Strict JSON payload (infrastructure_state.json) mapping hardware reality.
# 
# [FUTURE TO-DO / ENHANCEMENTS]
# 1. INTEGRATION: Feed the JSON output into the upcoming `auth_ayu` module.
# 2. SECURITY: Implement post-quantum blockchain ledger hashing. The JSON state 
#    must be cryptographically signed to enforce a zero-trust architecture. Any 
#    unauthorized changes to the system state or `ayu_lore.md` will break the 
#    hash and trigger subsystem isolation.
# ==============================================================================

OUTPUT_FILE="/root/infrastructure_state.json"
TEMP_DATA="/tmp/yugayu_state.txt"
> $TEMP_DATA 

# 1. Gather Host Baseline
CPU_MODEL=$(lscpu | grep "Model name:" | sed 's/Model name:\s*//')
TOTAL_RAM=$(free -h | awk '/^Mem:/ {print $2}')
HOST_IP=$(ip route get 1 | awk '{print $7; exit}')

echo "HOST_CPU|$CPU_MODEL" >> $TEMP_DATA
echo "HOST_RAM|$TOTAL_RAM" >> $TEMP_DATA

# 2. Iterate through Subsystems
for ct in $(pct list | awk 'NR>1 {print $1}'); do
    HOSTNAME=$(pct config $ct | awk -F: '/^hostname/ {print $2}' | xargs)
    IP=$(pct config $ct | grep '^net0' | grep -o 'ip=[^,]*' | cut -d= -f2 | cut -d/ -f1)
    
    # Check power state before executing internal probes
    STATUS=$(pct status $ct | awk '{print $2}')
    
    if [ "$STATUS" == "running" ]; then
        LORE_CHECK=$(pct exec $ct -- test -f /root/ayu_lore.md && echo "EXISTS" || echo "MISSING")
        
        if [ "$LORE_CHECK" == "MISSING" ]; then
            DEFAULT_LORE="SYSTEM INTENT PENDING. Awaiting Yugayu protocol classification."
            pct exec $ct -- bash -c "echo \"$DEFAULT_LORE\" > /root/ayu_lore.md"
            LORE_TEXT="$DEFAULT_LORE"
        else
            LORE_TEXT=$(pct exec $ct -- cat /root/ayu_lore.md | tr '\n' ' ')
        fi

        RAW_PORTS=$(pct exec $ct -- ss -tuln | awk 'NR>1 {if (match($5, /:[0-9]+$/)) {port = substr($5, RSTART+1, RLENGTH-1); if (port < 60000) print port;}}' | sort -nu | paste -sd, -)
        if [ -z "$RAW_PORTS" ]; then RAW_PORTS="none"; fi
    else
        LORE_TEXT="NODE_OFFLINE"
        RAW_PORTS="none"
    fi

    echo "LXC|$ct|$HOSTNAME|$IP|$LORE_TEXT|$RAW_PORTS" >> $TEMP_DATA
done

# 3. Python JSON Compiler
python3 -c '
import json, datetime

data = {
    "_system_metadata": {
        "protocol": "Yugayu Framework",
        "engine": "id_ayu_v1.2",
        "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "telemetry": "Deterministic Infrastructure State for autonomous onboarding."
    },
    "host_node": {},
    "sub_systems": []
}

with open("/tmp/yugayu_state.txt", "r") as f:
    for line in f:
        parts = line.strip().split("|")
        if parts[0] == "HOST_CPU": data["host_node"]["cpu"] = parts[1]
        elif parts[0] == "HOST_RAM": data["host_node"]["memory_total"] = parts[1]
        elif parts[0] == "LXC":
            ports = [int(p) for p in parts[5].split(",")] if parts[5] != "none" else []
            data["sub_systems"].append({
                "node_id": parts[1],
                "designation": parts[2],
                "network_ipv4": parts[3],
                "semantic_intent": parts[4],
                "active_sockets": ports
            })

with open("'$OUTPUT_FILE'", "w") as f:
    json.dump(data, f, indent=4)
'

rm $TEMP_DATA
echo "Discovery sequence complete. Protocol state compiled to: $OUTPUT_FILE"
