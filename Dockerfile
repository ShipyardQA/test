FROM python:3.11-alpine

# Declared as a build arg in docker-compose.yml. On QA this is fed by an external (Vault)
# "from provider" build-arg reference named API_KEY, resolved by Shipyard before the build.
ARG API_KEY

# Prove the build arg reached the build WITHOUT baking the raw secret into an image layer:
# record its sha256 and length. A rotated Vault value changes the sha256 (and the image tag),
# which is what we verify. An empty/missing value gives the sha256 of "" — a clear failure signal.
RUN printf '%s' "${API_KEY}" | sha256sum | cut -d' ' -f1 > /build-info.txt \
    && printf 'api_key_len=%s\n' "${#API_KEY}" >> /build-info.txt \
    && cat /build-info.txt

WORKDIR /app
COPY server.py .

EXPOSE 8080
CMD ["python", "server.py"]
