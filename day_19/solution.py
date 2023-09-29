from __future__ import annotations

from dataclasses import dataclass
from typing import Generator

from day_02.solution import yield_rows


@dataclass
class RobotRecipe:
    type: str
    cost_ore: int = 0
    cost_clay: int = 0
    cost_obsidian: int = 0


@dataclass(frozen=True)
class SimulationState:
    step: int
    robots_ore: int
    robots_clay: int
    robots_obsidian: int
    robots_geode: int
    collected_ore: int
    collected_clay: int
    collected_obsidian: int
    collected_geode: int

    def update_resources(self) -> SimulationState:
        return SimulationState(self.step,
                               self.robots_ore,
                               self.robots_clay,
                               self.robots_obsidian,
                               self.robots_geode,
                               self.collected_ore + self.robots_ore,
                               self.collected_clay + self.robots_clay,
                               self.collected_obsidian + self.robots_obsidian,
                               self.collected_geode + self.robots_geode)

    def from_current(self) -> SimulationState:
        state_dict = vars(self).copy()
        state_dict['step'] += 1
        return SimulationState(**state_dict)

    def create_robot(self, recipe: RobotRecipe) -> SimulationState:
        state_dict = vars(self).copy()

        state_dict['collected_ore'] -= recipe.cost_ore
        state_dict['collected_clay'] -= recipe.cost_clay
        state_dict['collected_obsidian'] -= recipe.cost_obsidian

        if recipe.type == 'ore':
            state_dict['robots_ore'] += 1
        elif recipe.type == 'clay':
            state_dict['robots_clay'] += 1
        elif recipe.type == 'obsidian':
            state_dict['robots_obsidian'] += 1
        elif recipe.type == 'geode':
            state_dict['robots_geode'] += 1
        else:
            raise ValueError('Incorrect robot type')

        return SimulationState(**state_dict)


def parse_recipe(recipe: str) -> RobotRecipe:
    recipe = recipe.strip()

    robot_type = recipe.split(' ')[1]

    robot_recipe = RobotRecipe(robot_type)

    required_resources = recipe.split(' ')[4:]
    for resource in chunks(required_resources, 3):
        resource_amount = int(resource[0])
        resource_name = resource[1]

        if resource_name == 'ore':
            robot_recipe.cost_ore = resource_amount
        elif resource_name == 'clay':
            robot_recipe.cost_clay = resource_amount
        elif resource_name == 'obsidian':
            robot_recipe.cost_obsidian = resource_amount

    return robot_recipe


def parse_blueprint(blueprint: str) -> tuple[int, list[RobotRecipe]]:
    blueprint_id = int(blueprint.split(':')[0].split(' ')[1])

    recipes = blueprint.split(':')[1].strip().split('.')[:-1]

    return blueprint_id, [parse_recipe(recipe) for recipe in recipes]


def chunks(lst: list, size: int) -> Generator[list, None, None]:
    start = 0
    end = size
    while start < len(lst):
        yield lst[start: end]
        start = end
        end += size


def find_buildable_robots(state: SimulationState, blueprint: list[RobotRecipe]) -> list[int]:
    buildable_robots = []
    for index, recipe in enumerate(blueprint):
        if recipe.cost_ore <= state.collected_ore and \
                recipe.cost_clay <= state.collected_clay and \
                recipe.cost_obsidian <= state.collected_obsidian:
            buildable_robots.append(index)
    return buildable_robots


def simulate(state: SimulationState, blueprint: list[RobotRecipe], max_steps: int) -> list[SimulationState]:
    prev_buildable_robots = find_buildable_robots(state, blueprint)

    state = state.update_resources()

    if state.step == max_steps:
        return [state]

    buildable_robots = find_buildable_robots(state, blueprint)

    # building a robot that was available in a previous step would never be an optimal solution
    new_buildable_robots = set(buildable_robots).difference(prev_buildable_robots)
    print(buildable_robots, new_buildable_robots)
    if not new_buildable_robots:
        # nothing to build, waiting
        return simulate(state.from_current(), blueprint, max_steps)
    else:
        # try to build every new possible to be build robot
        possible_states = []
        for recipe_id in new_buildable_robots:
            recipe = blueprint[recipe_id]

            new_state = state.create_robot(recipe)
            possible_states.extend(simulate(new_state.from_current(), blueprint, max_steps))

        # not every robot can be built yet, so try to wait as well
        if len(buildable_robots) < len(blueprint):
            possible_states.extend(simulate(state.from_current(), blueprint, max_steps))

        return possible_states

if __name__ == '__main__':
    # path = 'day_19/input2.txt'
    path = './input2.txt'

    blueprints = list(yield_rows(path))
    blueprints = [parse_blueprint(bp) for bp in blueprints]

    total_steps = 24

    blueprint_id, blueprint = blueprints[0]

    res = simulate(SimulationState(1, 1, 0, 0, 0, 0, 0, 0, 0), blueprint, 24)

    res = sorted(res, key=lambda x: x.collected_geode, reverse=True)

    print(res)
