# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. Hardcoded configuration (API key, Redis URL)
2. Không có config management
3. Print thay vì proper logging
4. Không có health check endpoint
5. Port cố định — không đọc từ environment

---

### Exercise 1.3: Comparison table

### Exercise 1.3: Comparison table

### Exercise 1.3: Comparison table

| Feature   | Develop (Basic - Anti-pattern)                     | Production (Advanced - 12-Factor)                     | Why           Important?                                  |
|-----------|---------------------------------------------------|------------------------------------------------------|-------------------------------------------------|
| Config    | Hardcoded API key, DB URL trong code              | Dùng environment variables (`settings`)               | Tránh lộ secret, dễ deploy nhiều môi trường     |
| Database  | localhost DB (không dùng được trên cloud)         | Config qua env → dùng cloud DB/Redis                  | Cho phép scale & multi-instance                 |
| Scaling   | Bind `localhost`, port cứng → chỉ chạy 1 instance | Bind `0.0.0.0`, port từ env → scale container         | Chạy được trên Docker, cloud, load balancing    |
| Security  | Log cả API key, không validate input              | Không log secret, validate request, structured log    | Tránh lộ thông tin nhạy cảm, an toàn hệ thống   |
| Logging   | `print()` raw                                    | Structured JSON logging (`logging`)                   | Dễ debug, tích hợp monitoring (Datadog, Loki)   |
| Health    | Không có `/health`                               | Có `/health` + `/ready`                               | Platform detect crash & load balancer routing   |
| Lifecycle | Không có startup/shutdown control                | Có `lifespan`, graceful shutdown                      | Tránh mất request khi deploy/restart            |
| CORS      | Không cấu hình                                   | Config allowed origins                                | Cho phép frontend gọi API an toàn               |
| Metrics   | Không có                                         | Có `/metrics` endpoint                                | Monitoring & observability                      |
| Deployment| Chạy `localhost`, debug reload luôn bật           | Config theo env, chỉ reload khi debug                 | Phù hợp production environment                  |

---

## Part 2: Docker

### Exercise 2.1: Dockerfile questions

1. Base image: `python:3.11-slim`  
2. Working directory: `/app`  
3. Why multi-stage? → giảm size image, tách build & runtime  
4. CMD: `uvicorn app.main:app --host 0.0.0.0 --port 8000`  
5. Exposed port: `8000`  

---

### Exercise 2.3: Image size comparison

- Develop: ~300 MB  
- Production: ~120 MB  
- Difference: ~60% smaller  

 Nhờ:
- dùng `slim image`
- loại bỏ build dependencies

---

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment

- URL: [https://my-agent-5sd9.onrender.com ](https://my-agent-z78g.onrender.com)
- Screenshot: (add ảnh vào repo, ví dụ `/docs/deploy.png`)

---

## Part 4: API Security

### Exercise 4.1-4.3: Test results

#### Health check
curl /health
→ {"status":"ok"}
#### Ready check:
curl /ready
→ {"status":"ready"}
#### Ask endpoint:
curl -H "X-API-Key: secret" /ask
→ {"answer":"Echo: Hello","history_length":1}
#### Rate limit test:
→ {"detail":"Rate limit exceeded"}

#### Exercise 4.4: Cost guard implementation
Mỗi request tăng chi phí giả lập $0.01
Lưu vào Redis theo key:
cost:{user_id}:{month}
Nếu vượt MONTHLY_BUDGET_USD → block request

👉 Ưu điểm:
đơn giản
dễ mở rộng sang token-based cost

#### Part 5: Scaling & Reliability
Exercise 5.1-5.5: Implementation notes
1. Horizontal scaling
Dùng Docker Compose scale:
--scale agent=3
2. Load balancing
Dùng Nginx upstream:
upstream agents {
    server agent:8000;
}
Request được phân phối tự động
3. Stateful handling
Redis lưu:
conversation history
rate limit
cost tracking
4. Reliability
Redis = shared state → tránh mất data khi scale
Nginx = entry point → đảm bảo availability
5. Test results
Multiple requests → history tăng đúng
Spam request → bị rate limit
Scale 3 instance → hệ thống vẫn hoạt động ổn định
