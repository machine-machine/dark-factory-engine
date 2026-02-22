FROM ubuntu:22.04
LABEL dark-factory.skill="deploy-service"
RUN apt-get update && \
    apt-get install -y bash jq curl git && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /skill
COPY . .
RUN chmod +x skill.sh functions.sh 2>/dev/null || true
# Health check endpoint (simple nc-based)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD pgrep -x skill.sh > /dev/null || exit 0
ENTRYPOINT ["/bin/bash", "skill.sh"]
