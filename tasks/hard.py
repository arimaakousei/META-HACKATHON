"""
Hard task: Reduce cost AND keep busy instances (cpu > 20%) running.
Requires balancing cost reduction with availability constraints.
"""


def grade(env) -> float:
    cost = sum(i.cost for i in env.instances if i.status == "running")

    score = 0.0

    if cost < 40:
        score += 0.5

    # Penalise stopping instances that are actually busy
    if all(i.cpu_usage > 20 or i.status == "running" for i in env.instances):
        score += 0.5

    return score
