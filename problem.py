from typing import List, Tuple
import graphviz

# Initial no. of missionaries, cannibals, and position of canoe/boat
M, C, P = 3, 3, 0

State = Tuple[int, int, int]
Action = Tuple[int, int]

class MissionariesCannibal:
    __graph_matrix: List[List[State]]
    __possible_actions: List[Action]

    def __init__(self) -> None:
        __ini_state = (M, C, P)
        self.__graph_matrix: List[List[State]] = [[(__ini_state)]]
        self.__possible_actions: List[Action] = [(0, 1), (1, 0), (1, 1), (2, 0), (0, 2)]
        self.f = graphviz.Digraph('finite_state_machine', filename='fsm.gv')
        self.node_format = "[{}, {}, {}]"


    def isGoalState(self, state: State) -> bool:
        m, c, _ = state
        return (not m) and (not c)

    def isValidState(self, state: State, action: Action) -> State | bool:
        m, c, p = state
        _m, _c = action
        m -= _m
        c -= _c
        if m < 0 or c < 0:
            return False
        if m < c:
            return False
        return (m, c, int(not bool(p)))

    def addNode(self, current: State, child: State, action: Action, isGoal: bool) -> None:
        pc, pm, pp = current
        cc, cm, cp = child
        ac, am = action
        self.f.attr("node", shape="circle")
        if isGoal:
            self.f.attr("node", shape="doublecircle")
        self.f.edge(self.node_format.format(pc, pm, pp),
                    self.node_format.format(cc, cm, cp),
                    label="({}, {})".format(ac, am))

    def generateNextStates(self, state: State) -> List[State]:
        states: List[State] = []
        for ac in self.__possible_actions:
            valid_state = self.isValidState(state, ac)
            if valid_state:
                states.append(valid_state)
                goal = self.isGoalState(valid_state)
                self.addNode(state, valid_state, ac, isGoal=goal)
                if goal:
                    break
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
        self.f.view()
        return self.__graph_matrix


if __name__ == "__main__":
    problem = MissionariesCannibal()
    matrix = problem.solve()
    for row in matrix:
        print(row)
