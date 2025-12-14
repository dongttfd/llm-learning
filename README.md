## My LLM learning

### Pre-running

- Run with `virtualenv`

```
python3 -m venv .venv
source .venv/bin/activate
```

### Installation
- Install libraries

```
python3 -m pip install fastapi uvicorn langchain langchain-community mesop llama-cpp-python
python3 -m pip install --upgrade pip
```

### Download models

Download model at [Link](https://huggingface.co/bartowski/Phi-3-mini-4k-instruct-GGUF/resolve/main/Phi-3-mini-4k-instruct-Q4_K_M.gguf)


### Running
- Chat at terminal
  ```
  python3 hello_llm.py
  ```

### Start
- Only api
  ```
  python3 -m uvicorn app.api:app --reload --port 9696
  ```
- Only web
  ```
  cd client && mesop mesop_app.py 
  ```

- **Start all**
  ```sh
    sh start.sh
  ```
  - Access test: http://localhost:32123

### Fix cannot run mesop at python3
  - Exit and delete old `venv`
  ```
  deactivate
  rm -rf .venv
  ```
  - Create new venv with Python ≥ 3.10
  ```
  python3.11 -m venv .venv
  source .venv/bin/activate
  ```
  - Reinstall all package