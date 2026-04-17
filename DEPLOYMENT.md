## Public URL
https://my-agent-5sd9.onrender.com

## Platform
Render 

## Test Commands
curl -k -X POST https://my-agent-5sd9.onrender.com/ask\
  -H "Content-Type: application/json" \
  -H "X-API-Key: secret" \
  -d '{"question": "Hello, how are you?"}'
Answer:{"answer":"Echo: Hello, how are you?","history_length":1}

curl -k -X POST https://my-agent-5sd9.onrender.com/ask \
  -H "X-API-Key: secret" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
{"answer":"Echo: Hello","history_length":2}
### Health Check
curl https://your-agent.railway.app/health
{"status": "ok"}