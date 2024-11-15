FROM python:3.12

RUN apt update && apt upgrade -y
RUN apt install -y build-essential ffmpeg tree
RUN apt install libmagic-dev -y

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN python -m pip install --upgrade pip
RUN pip install setuptools-rust
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install -U openai-whisper

WORKDIR /app

COPY ./requirements.txt .
RUN touch ./requirements_filtered.txt
RUN grep -v 'python-magic-bin' requirements.txt > ./requirements_filtered.txt
RUN pip install -r requirements_filtered.txt

COPY ./app .

