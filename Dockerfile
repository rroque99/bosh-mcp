FROM rroque99/bosh-tools:latest

EXPOSE 8080

RUN useradd -m -u 1000 -s /bin/bash boshuser

USER boshuser

RUN mkdir /home/boshuser/workspace

COPY pyproject.toml /home/boshuser/workspace

COPY src/ /home/boshuser/workspace/src/

WORKDIR /home/boshuser/workspace

RUN uv sync

CMD ["uv", "run", "src/main.py"]
