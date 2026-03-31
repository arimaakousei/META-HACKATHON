"""
Baseline policy for the Cloud Cost Optimization Environment.

Simple rule-based agent:
  1. Stop any instance with CPU usage below 20% (idle).
  2. Resize the most expensive running instance if no idle instances found.
  3. Stops after MAX_STEPS to prevent infinite loops.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from env.environment import CloudEnv
from env.models import Action

MAX_STEPS = 20  # safety cap — prevents infinite loops


def simple_policy(obs) -> Action:
    """Rule-based policy: stop idle instances first, then resize the costliest."""
    # Step 1: stop any idle running instance
    for instance in obs.instances:
        if instance.status == "running" and instance.cpu_usage < 20:
            return Action(action_type="stop", instance_id=instance.id)

    # Step 2: resize the most expensive running instance
    running = [i for i in obs.instances if i.status == "running"]
    if running:
        target = max(running, key=lambda i: i.cost)
        return Action(action_type="resize", instance_id=target.id)

    # Fallback (all instances already stopped)
    return Action(action_type="resize", instance_id=1)


def run(verbose: bool = True):
    env = CloudEnv()
    obs = env.reset()

    if verbose:
        print("=== Cloud Cost Optimization — Baseline Agent ===")
        print(f"Initial total cost: ${obs.total_cost:.2f}\n")

    done = False
    step = 0
    reward = None

    while not done and step < MAX_STEPS:
        action = simple_policy(obs)
        obs, reward, done, _ = env.step(action)
        step += 1

        if verbose:
            print(f"Step {step}: action={action.action_type} on instance {action.instance_id}")
            print(f"  Reward: {reward.score:.2f} | Total cost: ${obs.total_cost:.2f}")

    if verbose:
        if done:
            print(f"\n✅ Done in {step} steps. Final reward: {reward.score:.2f}")
        else:
            print(f"\n⚠️  Stopped after {MAX_STEPS} steps. Final cost: ${obs.total_cost:.2f}")

    return reward.score if reward else 0.0


if __name__ == "__main__":
    run()
