### 1. Why does `DATABASE_URL` use `mongo` as the hostname instead of `localhost`? What would happen if you kept `localhost`?

Because FastAPI and MongoDB run in separate containers, `localhost` refers to the FastAPI container, not MongoDB. Using the `mongo` hostname ensures that FastAPI connects to the MongoDB container correctly.

### 2. What does `depends_on` in `docker-compose.yml` do? Does it guarantee MongoDB is fully ready before FastAPI starts — and if not, what would?

The `depends_on` only controls the startup order in the `docker-compose.yml` file. This directive starts MongoDB before FastAPI.

To ensure MongoDB is ready, implement a health check on MongoDB and bind FastAPI to `service_healthy`, or add a retry/wait script to the FastAPI container.

### 3. What is the purpose of the volume in the `mongo` service? What happens to your data if you remove it and run `docker compose down`?

The volume keeps MongoDB data persistent outside the container. If you remove it and run `docker compose down`, the data is lost.

### 4. Why do we copy `requirements.txt` and run `pip install` before copying the rest of the app code in the Dockerfile?

Allows Docker to utilize the build cache. If only the app code changes, Docker will reuse the cached dependencies.
