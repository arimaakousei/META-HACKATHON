"""
Easy task: Stop any instance with low CPU usage (< 20%).
Full score if at least one idle instance has been stopped.
"""


def grade(env) -> float:
    for i in env.instances:
        if i.cpu_usage < 20 and i.status == "stopped":
            return 1.0
    return 0.0
