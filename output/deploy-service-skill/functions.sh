#!/bin/bash
# Helper functions for workflow execution

log_info() {
    echo "$(date -Iseconds) [INFO] $*"
}

log_error() {
    echo "$(date -Iseconds) [ERROR] $*" >&2
}

log_debug() {
    echo "$(date -Iseconds) [DEBUG] $*" >&2
}

# Store output value
set_output() {
    local key="$1"
    local value="$2"
    OUTPUTS[$key]="$value"
    
    # Also store in JSON file
    local outputs_file="$SCRIPT_DIR/outputs.json"
    if [[ ! -f "$outputs_file" ]]; then
        echo "{}" > "$outputs_file"
    fi
    
    # Update JSON file (requires jq)
    if command -v jq &> /dev/null; then
        jq --arg key "$key" --arg value "$value" '.[$key] = $value' "$outputs_file" > "${outputs_file}.tmp"
        mv "${outputs_file}.tmp" "$outputs_file"
    else
        log_debug "jq not available, outputs stored in memory only"
    fi
}

# Get input value
get_input() {
    local key="$1"
    echo "${INPUTS[$key]:-}"
}
