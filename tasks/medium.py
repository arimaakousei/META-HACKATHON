"""
Medium task: Reduce total running cost below thresholds.
Score is tiered based on how much cost was reduced.
"""


def grade(env) -> float:
    cost = sum(i.cost for i in env.instances if i.status == "running")

    if cost < 40:
        return 1.0
    elif cost < 60:
        return 0.5
    return 0.2
