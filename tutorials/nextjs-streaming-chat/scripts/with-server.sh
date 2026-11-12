#!/bin/sh
# Start the production server on port 8129, run the command given, stop the server,
# then print the lines the route handler wrote to its log.
# usage: scripts/with-server.sh node scripts/call-route.mjs
./node_modules/.bin/next start -p 8129 > server.log 2>&1 &
PID=$!
for i in $(seq 1 60); do
  curl -s -o /dev/null http://127.0.0.1:8129/ && break
  sleep 0.5
done
"$@"
STATUS=$?
kill $PID 2>/dev/null
wait $PID 2>/dev/null
echo "--- server log"
grep -E '^(done|client left|api error|stream error)' server.log || echo "(no route log lines)"
exit $STATUS
