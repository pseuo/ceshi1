#!/bin/sh

LOG_FILE="/path/to/your/logfile.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

log "Script started."

while true; do
    log "Starting update process..."
    echo "Updating GeoLite2-City.mmdb..."
    curl -L -o "GeoLite2-City.mmdb" "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb" || { log "Failed to update GeoLite2-City.mmdb"; continue; }
    
    echo "Updating GeoLite2-ASN.mmdb..."
    curl -L -o "GeoLite2-ASN.mmdb" "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb" || { log "Failed to update GeoLite2-ASN.mmdb"; continue; }
    
    echo "Updating GeoCN.mmdb..."
    curl -L -o "GeoCN.mmdb" "http://github.com/ljxi/GeoCN/releases/download/Latest/GeoCN.mmdb" || { log "Failed to update GeoCN.mmdb"; continue; }

    log "Attempting to restart uvicorn..."
    pkill -f "uvicorn"
    
    nohup uvicorn main:app --host 0.0.0.0 --port 7887 --no-server-header --proxy-headers &
    
    sleep 5
    
    if pgrep -f "uvicorn" > /dev/null; then
        log "uvicorn restarted successfully."
    else
        log "Failed to restart uvicorn, retrying..."
        continue
    fi

    log "Update process completed. Sleeping for 24 hours."
    sleep 86400
done
