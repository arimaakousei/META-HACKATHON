---

title: Cloud Cost Env
emoji: ☁️
colorFrom: blue
colorTo: green
sdk: docker
-----------

# ☁️ Cloud Cost Optimization Environment

An open agentic environment where an AI agent learns to reduce cloud infrastructure costs by making smart decisions about running instances.

---

## 🧩 Problem

Cloud infrastructure is expensive. Servers often run at low utilization, wasting money. This environment simulates a small cloud cluster where an agent must:

* **Stop** idle instances (low CPU usage)
* **Resize** over-provisioned instances to cut their cost
* **Avoid** stopping busy instances that are still needed

---

## 🏗️ Project Structure

```
cloud-cost-env/
├── env/
│   ├── __init__.py
│   ├── models.py         # Pydantic data models
│   └── environment.py    # Core environment logic
├── tasks/
│   ├── __init__.py
│   ├── easy.py           # Stop any idle instance
│   ├── medium.py         # Reduce total cost below $40
│   └── hard.py           # Cut cost + keep busy instances alive
├── inference/
│   ├── __init__.py
│   └── baseline.py       # Rule-based baseline agent
├── openenv.yaml          # Environment spec
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ⚙️ How the Environment Works

The environment starts with two cloud instances:

| Instance | Status  | CPU Usage | Cost |
| -------- | ------- | --------- | ---- |
| 1        | running | 10%       | $20  |
| 2        | running | 80%       | $50  |

Each step, the agent receives an **Observation** and must return an **Action**.

The episode ends when total running cost drops below **$30**.

---

## 🎮 Actions

| Action   | Description                                   |
| -------- | --------------------------------------------- |
| `stop`   | Stop an instance. Rewarded only if CPU < 20%. |
| `resize` | Halve the cost of an instance.                |

---

## 👁️ Observations

| Field        | Type             | Description                              |
| ------------ | ---------------- | ---------------------------------------- |
| `instances`  | `List[Instance]` | All instances with id, status, CPU, cost |
| `total_cost` | `float`          | Sum of costs for all running instances   |

---

## 🏆 Reward System

| Event                           | Reward |
| ------------------------------- | ------ |
| Stop an idle instance (CPU<20%) | +0.5   |
| Resize an instance              | +0.3   |
| Total cost decreases            | +0.3   |
| Stop a busy instance (CPU≥20%)  | -0.3   |

All rewards are clipped to `[0.0, 1.0]`.

---

## 📋 Tasks

### Easy

Stop at least one idle instance (CPU < 20%). Full score: **1.0**

### Medium

Reduce total running cost below thresholds:

* Cost < $40 → **1.0**
* Cost < $60 → **0.5**
* Otherwise → **0.2**

### Hard

Reduce cost AND keep all high-utilization instances running:

* Cost < $40 → +0.5
* No busy instance was stopped → +0.5

---

## 🚀 Setup & Run

### Local

```bash
pip install -r requirements.txt
python inference/baseline.py
```

### Docker

```bash
docker build -t cloud-cost-env .
docker run cloud-cost-env
```

---

## 🔌 API Usage

```python
from env.environment import CloudEnv
from env.models import Action

env = CloudEnv()
obs = env.reset()

action = Action(action_type="stop", instance_id=1)
obs, reward, done, info = env.step(action)

print(reward.score)
print(obs.total_cost)
```

---

## 📊 Baseline Results

The rule-based baseline agent (`inference/baseline.py`) achieves:

* Stops idle instance #1 (CPU = 10%) → reward +0.5
* Resizes instance #1 if needed → reward +0.3
* Terminates when total cost < $30

Typical final reward: **~0.8**

---

## 📄 License

MIT
