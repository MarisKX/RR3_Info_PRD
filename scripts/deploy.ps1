# deploy.ps1
# Script to automate the Heroku deployment process

# Step 1: Build the Docker image
docker-compose build

# Step 2: Push the Docker image to Heroku
heroku container:push web --app rr3info

# Step 3: Release the Docker image on Heroku
heroku container:release web --app rr3info

# Step 4: Apply database migrations
heroku run python manage.py migrate --app rr3info

# Step 5: Collect static files
heroku run python manage.py collectstatic --noinput --app rr3info
