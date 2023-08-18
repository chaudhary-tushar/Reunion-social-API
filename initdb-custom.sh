#!/bin/bash

echo "Restoring custom-format dump..."
pg_restore -U romeo7 -d reapion /var/local/backup.sql
echo $?


if [ $? -eq 0 ]; then
    echo "pg_restore executed successfully."
else
    echo "pg_restore failed."
fi