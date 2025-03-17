#!bin/sh


# Wait for Minio to start and add minio admin alias
until mc alias set myminio http://minio:9000 minioadmin minioadmin; do
    echo "MinIO is not ready yet. Retrying in 5 seconds..."
    sleep 5
done

# Make bucket and add data
mc mb myminio/bucket1
mc cp ./sample.csv myminio/bucket1/sample.csv

# Add new user and attach new policy 
mc admin user add myminio testuser password
mc admin policy create myminio read-write policy.json
mc admin policy attach myminio read-write --user testuser
