from .models import Instance, Observation, Action, Reward


class CloudEnv:

    def __init__(self):
        self.reset()

    def reset(self):
        self.instances = [
            Instance(id=1, status="running", cpu_usage=10, cost=20),
            Instance(id=2, status="running", cpu_usage=80, cost=50),
        ]
        self.prev_cost = self._total_cost()
        return self._get_obs()

    def _total_cost(self):
        return sum(i.cost for i in self.instances if i.status == "running")

    def _get_obs(self):
        return Observation(
            instances=self.instances,
            total_cost=self._total_cost()
        )

    def step(self, action: Action):
        reward = 0

        for i in self.instances:
            if i.id == action.instance_id:

                if action.action_type == "stop":
                    if i.cpu_usage < 20:
                        i.status = "stopped"
                        reward += 0.5
                    else:
                        reward -= 0.3

                if action.action_type == "resize":
                    i.cost *= 0.5
                    reward += 0.3

        new_cost = self._total_cost()

        # Bonus reward for reducing total cost
        if new_cost < self.prev_cost:
            reward += 0.3

        self.prev_cost = new_cost

        done = new_cost < 30

        return self._get_obs(), Reward(score=min(max(reward, 0), 1)), done, {}

    def state(self):
        return self.instances
