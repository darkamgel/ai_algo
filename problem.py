from typing import List, Tuple
import graphviz

# Initial no. of missionaries, cannibals, and position of canoe/boat
M, C, P = 3, 3, 1

State = Tuple[int, int, int]
Action = Tuple[int, int]

class MissionariesCannibal:
    __graph_matrix: List[List[State]]
    __possible_actions: List[Action]
    __visited: List[State]
    __unique_states: List[State]

    def __init__(self) -> None:
        __ini_state = (M, C, P)
        self.__graph_matrix: List[List[State]] = [[(__ini_state)]]
        self.__possible_actions: List[Action] = [
            (0, 1), (1, 0), (1, 1), (2, 0), (0, 2)]
        self.f = graphviz.Digraph('finite_state_machine', filename='fsm.gv')
        self.__unique_states = []
        self.__node_format = "[{}, {}, {}]"
        self.__visited = []

    def isGoalState(self, state: State) -> bool:
        m, c, _ = state
        return (not m) and (not c)

    def addTreeNode(self, current: State, child: State, action: Action, isGoal: bool) -> None:
        pc, pm, pp = current
        cc, cm, cp = child
        ac, am = action
        self.f.attr("node", shape="circle")
        if isGoal:
            self.f.attr("node", shape="doublecircle")
        self.f.edge(self.__node_format.format(pc, pm, pp),
                    self.__node_format.format(cc, cm, cp),
                    label="({}, {})".format(ac, am))

    def find_possible_path(self, state: State) -> List[State]:
        poss_st: List[State] = []
        for p in self.__possible_actions:
            m, c, b = state
            _m, _c = 3 - m, 3 - c
            __m, __c = p
            if not b:
                m += __m
                c += __c
                _m -= __m
                _c -= __c
            else:
                m -= __m
                c -= __c
                _m += __m
                _c += __c
            if m > 3 or c > 3:
                continue
            if m < 0 or c < 0:
                continue
            if _m > 3 or _c > 3:
                continue
            if _m < 0 or _c < 0:
                continue
            if (m and m < c) or (_m and _m < _c):
                continue
            poss_st.append((m , c, int(not bool(b))))
        return poss_st

    def generateNextStates(self, state: State) -> List[State]:
        states: List[State] = []
        if self.__visited.count(state):
            return []
        possible_next = self.find_possible_path(state)
        for possible in possible_next:
            if self.__visited.count(possible): continue
            m, c, _ = state
            _m, _c, __ = possible
            goal = self.isGoalState(possible)
            self.addTreeNode(state, possible, (abs(m-_m), abs(c-_c)), isGoal=goal)
            states.append(possible)
            if goal: break
        self.__visited.append(state)
        return states

    def solve(self) -> List[List[State]]:
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
                    self.__unique_states.append(st)
                    isGoal = self.isGoalState(st)
                    if isGoal:
                        self.__graph_matrix.append(states)
                        goal = True
                        break
            row += 1
            self.__graph_matrix.append(states)
        self.f.render(filename="missionaries_cannibals", format="png", view=False)
        return self.__graph_matrix

if __name__ == "__main__":
    problem = MissionariesCannibal()
    matrix = problem.solve()
    for row in matrix:
        print(row)