from typing import Dict, List, Optional

from planner_py.grid import Cell, Grid, PlanResult


def heuristic(a: Cell, b: Cell) -> float:

    # TODO 0: a 에서 b 까지의 비용 추정을 계산해 돌려준다.
    #         힌트: dx, dy 를 구하고, 대각선으로 갈 수 있는 만큼 대각선, 나머지는 직선.
    #         (dx, dy) = (abs(ax - bx), abs(ay - by)) 라고 하면
    #         대각선으로 갈 수 있는 칸 수는 min(dx, dy),
    #         직선으로 갈 수 있는 칸 수는 max(dx, dy) - min(dx, dy) 이다.
    #         대각선은 sqrt(2) 만큼, 직선은 1.0 만큼 비용이 든다.
    ax, ay = a
    bx, by = b
    dx = abs(ax - bx)
    dy = abs(ay - by)
    diagonal_steps = min(dx, dy)
    straight_steps = max(dx, dy) - diagonal_steps
    return diagonal_steps * 2 ** 0.5 + straight_steps * 1.0
    raise NotImplementedError('TODO 0: implement heuristic()')


def reconstruct_path(parent: Dict[Cell, Cell], start: Cell, goal: Cell) -> List[Cell]:
    # TODO 4: goal 에서 시작해 parent 를 따라 start 까지 거슬러 올라가며 칸을 모은다.
    #         모은 순서는 goal -> start 이므로 뒤집어서 돌려준다.
    #         start == goal 이면 [start] 하나만 나와야 한다.
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path
    raise NotImplementedError('TODO 4: implement reconstruct_path()')


def astar(grid: Grid, start: Cell, goal: Cell) -> Optional[PlanResult]:
    g = {start: 0.0}        # 칸 -> 시작에서 그 칸까지 지금까지 찾은 가장 작은 비용
    parent = {}             # 칸 -> 그 칸으로 오기 직전의 칸 (경로 복원용)
    open_list = [(heuristic(start, goal), start)]   # (f, 칸). f 가 앞이라 min() 이 f 최솟값
    closed = set()          # 이미 확장을 끝낸 칸
    visited = []            # 확장한 순서 (PlanResult.visited, RViz 에 표시됨)

    # 아래 TODO 1~5 를 모두 채운 뒤 이 줄을 지우세요. (지우기 전에는 테스트가 skip 됩니다.)
    raise NotImplementedError('TODO: fill in the loop below, then delete this line')

    # ---------- 2. 메인 루프 ----------
    while open_list:
        # TODO 1: open_list 에서 f 가 가장 작은 항목을 꺼낸다.
        #         min(open_list) 는 (f, 칸) 을 돌려주고, open_list.remove(항목) 으로 지운다.
        #         꺼낸 칸의 이름을 current 로 한다.
        current = min(open_list, key=lambda x: x[0])[1]
        open_list.remove((g[current] + heuristic(current, goal), current))
        

        # TODO 2: current 가 이미 closed 에 있으면 건너뛴다 (continue).
        #         갱신 때 같은 칸을 open 에 여러 번 넣기 때문에 오래된 항목이 남아 있다.
        #         아니면 closed 에 넣고, visited 에 기록한다. (확장 = 여기서 꺼내는 것)

        # TODO 3: current 가 goal 이면 끝이다.
        #         reconstruct_path(...) 로 경로를 만들고
        #         PlanResult(경로, g[goal], 확장한 칸 수, visited) 를 돌려준다.

        # TODO 5: current 의 이웃을 하나씩 본다.
        for jx, jy, step in grid.neighbors(*current):
            neighbor = (jx, jy)
            # 5-1: neighbor 가 closed 에 있으면 건너뛴다.
            # 5-2: new_g = g[current] + step
            # 5-3: neighbor 를 처음 보거나(g 에 없거나) new_g 가 g[neighbor] 보다 작으면
            #      g[neighbor] 와 parent[neighbor] 를 갱신하고
            #      open_list 에 (new_g + heuristic(neighbor, goal), neighbor) 를 추가한다.
            pass

    # ---------- 3. 경로 없음 ----------
    # open_list 가 비었는데 goal 을 못 꺼냈다면 갈 수 없는 목표다.
    return None
