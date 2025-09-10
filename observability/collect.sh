JQ=http://192.168.49.2:32688
LOOKBACK=55m
LIMIT=50000

services=(
  "read-post"
  "follow-user"
  "recommender"
  "ads"
  "unique-id"
  "url-shorten"
  "video"
  "image"
  "text"
  "user-tag"
  "favorite"
  "search"
)

for svc in "${services[@]}"; do
  echo "Exporting $svc ..."
  ./jaeger-exporter \
    -host "$JQ" \
    -service "$svc" \
    -limit "$LIMIT" \
    -lookback "$LOOKBACK" \
    -filename "$svc".csv

done

echo "Done"
