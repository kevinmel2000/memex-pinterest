until docker-compose up --no-recreate; do
    echo "SourcePin crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
