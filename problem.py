from typing import List, Tuple
import graphviz

# Initial no. of missionaries, cannibals, and position of canoe/boat
M, C, P = 3, 3, 0

State = Tuple[int, int, int]
Action = Tuple[int, int]


class MissionariesCannibal:
    __graph_matrix: List[List[State]]
    __possible_actions: List[Action]
    __visited: List[State]

    def __init__(self) -> None:
        __ini_state = (M, C, P)
        self.__graph_matrix: List[List[State]] = [[(__ini_state)]]
        self.__possible_actions: List[Action] = [
            (0, 1), (1, 0), (1, 1), (2, 0), (0, 2)]
        self.f = graphviz.Digraph('finite_state_machine', filename='fsm.gv')
        self.__node_format = "[{}, {}, {}]"
        self.__visited = []

    def isGoalState(self, state: State) -> bool:
        m, c, _ = state
        return (not m) and (not c)

    def isValidState(self, state: State, action: Action) -> State | bool:
        m, c, p = state
        _m, _c = action

        if p == 0:
            m -= _m
            c -= _c
        else:
            m += _m
            c += _c
        if m > 3 or c > 3:
            return False
        if m < 0 or c < 0:
            return False
        if m < c:
            return False
        state = (m, c, int(not bool(p)))
        return state

    def addNode(self, current: State, child: State, action: Action, isGoal: bool) -> None:
        pc, pm, pp = current
        cc, cm, cp = child
        ac, am = action
        self.f.attr("node", shape="circle")
        if isGoal:
            self.f.attr("node", shape="doublecircle")
        self.f.edge(self.__node_format.format(pc, pm, pp),
                    self.__node_format.format(cc, cm, cp),
                    label="({}, {})".format(ac, am))

    def generateNextStates(self, state: State) -> List[State]:
        states: List[State] = []
        if self.__visited.count(state):
            return []
        for ac in self.__possible_actions:
            valid_state = self.isValidState(state, ac)
            if valid_state:
                if self.__visited.count(valid_state):
                    continue
                states.append(valid_state)
                goal = self.isGoalState(valid_state)
                self.addNode(state, valid_state, ac, isGoal=goal)
                if goal:
                    break
        self.__visited.append(state)
        return states

    def solve(self):
        row = 0
        goal = False
        while len(self.__graph_matrix[row]) and not goal:
            states: List[State] = []
            for state in self.__graph_matrix[row]:
                if goal:
                    break
                local_states = self.generateNextStates(state)
                for st in local_states:
                    states.append(st)
                    isGoal = self.isGoalState(st)
                    if isGoal:
                        self.__graph_matrix.append(states)
                        goal = True
                        break
            row += 1
            self.__graph_matrix.append(states)
        self.f.render(filename="missionaries_cannibals", format="png", view=True)
        return self.__graph_matrix


if __name__ == "__main__":
    problem = MissionariesCannibal()
    matrix = problem.solve()
    for row in matrix:
        print(row)
