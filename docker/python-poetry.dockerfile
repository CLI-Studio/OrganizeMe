FROM python:latest

# Install poetry (Python packge manager)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

ENTRYPOINT [ "/bin/bash" ]