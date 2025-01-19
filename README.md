# HomeAgent
An LLM agent hosted for on my local network

## Set-up
#### To use venv
- `source .env/bin/activate`

## Testing
- Sample curl request to ollama container
```
curl http://192.168.2.17:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt":"Why is the sky blue?"
}'
```
