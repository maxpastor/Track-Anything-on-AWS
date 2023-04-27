FROM pytorch/pytorch:latest

# Install system packages
RUN apt-get update && apt-get install -y git python3-pip curl

# Clone the repository
RUN git clone https://github.com/gaomingqi/Track-Anything.git /app
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies for inpainting
RUN pip install --no-cache-dir -U openmim
RUN mim install mmcv

# Install dependencies for editing
RUN pip install --no-cache-dir madgrad

# Expose the port 12212
EXPOSE 12212

# Run the Track-Anything gradio demo
CMD ["python", "app.py", "--device", "cuda:0", "--sam_model_type", "vit_h", "--port", "12212"]
