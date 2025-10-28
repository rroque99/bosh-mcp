FROM rroque99/bosh-tools:latest

COPY pyproject.toml /workspace

COPY src/ /workspace/src/
#COPY .venv/* /workspace/.venv/


ENV PATH="/root/.local/bin/:/root/.cargo/bin:${PATH}"

EXPOSE 80

WORKDIR /workspace

RUN uv sync

CMD ["uv", "run", "src/main.py"]
#CMD ["/bin/bash"]