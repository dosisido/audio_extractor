FROM python:3.11

RUN apt update && apt upgrade -y
RUN apt install -y build-essential ffmpeg tree

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip
RUN pip install setuptools-rust
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -U openai-whisper

# WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY /app .

