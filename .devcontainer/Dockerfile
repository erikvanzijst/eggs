FROM mcr.microsoft.com/devcontainers/python:3.11

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update -y \
    && apt-get install -y nodejs neovim btop httpie sqlite3 \
    && npm install -g opencode-ai \
    && apt-get clean

USER vscode
ENV PATH=/home/vscode/.local/bin:$PATH
ENV COLORTERM=truecolor
RUN curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN curl -fsSL https://claude.ai/install.sh | bash
