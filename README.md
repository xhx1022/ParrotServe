# Parrot: Efficient Serving LLM-based Agents with Dependent Semantic Variables

This project is a research prototype for now. Being eargerly iterated.

## Install

**Install dependencies:**

- Step 1.

```bash
pip install -r requirements.txt
pip install triton==2.1.0
```

(Note: Triton 2.0.0 has some bugs in Kernel memory issues. The similar error also happens in [LightLLM](https://github.com/ModelTC/lightllm) kernels.)

- Step 2.

Follow the official guide of [MLC-LLM](https://github.com/mlc-ai/mlc-llm) to install it. The 
recommended commit refers to `3rdparty` folder.

- Step 3.

Install other dependencies listed in `3rdparty` folder.

**Install Parrot:**

```bash
python3 setup.py develop
```


## Run Parrot

**Run the Compose Script in a Single Machine**

We provide some one-click scripts to run Parrot in a single machine. You can find them in the `scripts` folder.

```bash
sh scripts/launch_single_vicuna_13b.sh
```

<!-- **Run Docker Compose in a Cluster**

TODO -->

**Start an OS Server**

You can separately start an OS server.

```bash
python3 -m parrot.os.http_server --config_path configs/os/localhost_os.json
```

**Start a Vicuna-13b Engine Server**

You can separately start an engine server. If you choose to connect to the OS server, you need to start the OS server first and specify the OS server address in the config file.

```bash
python3 -m parrot.engine.http_server --config_path configs/engine/native/vicuna-13b-v1.3.json
```