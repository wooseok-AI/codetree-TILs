# 마법의 숲 탐색 (코드트리 삼성전자 24년 상반기 오후)
# 1. 아래로 이동
#     - 내려갈수있으면 이동
#     - 1) 못내려가면 왼쪽 1카이동, 시계 반대 회전, 한칸 아래로 ,     - 2) 오른쪽 1칸 이동, 시계 방향 회전, 한칸 아래로
#     -> 셋다 못할떄까지 이동
# 2. 정령 이동
#     최대한 아래로 이동.
#     주변에 다른 골렘이 있을시, 골렘 출구로만 이동가능
# 3. 모두 이동
#     골렘이 맵에 못들어가면 맵 초기화 하고 재시작

R, C, K = map(int, input().split()) # 행, 렬, 정령 수
ELF = [tuple(map(int, input().split())) for _ in range(K)]
GRID = [[0] * C for _ in range(R+3)]
EXIT = [[0] * C for _ in range(R+3)]
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
answer = 0

def inRange(r,c):
    return 3 <= r< R+3 and 0<=c<C

def bfs(x, y):
    global EXIT
    dx = [1,-1,0,0]
    dy = [0,0,1,-1]
    visited = [[0] * C for _ in range(R+3)]
    current = (x, y)
    queue = list()
    queue.append(current)
    visited[x][y] = 1
    max_row = -1

    while queue:
        curr_x, curr_y = queue.pop(0)
        curr_idx = GRID[curr_x][curr_y]
        if curr_x > max_row:
            max_row = curr_x

        for d in range(4):
            new_x, new_y = curr_x+dx[d], curr_y+dy[d]
            if 2 <= new_x < R+3 and 0<=new_y<C:
                if GRID[new_x][new_y] != 0 and not visited[new_x][new_y]:
                    if (GRID[new_x][new_y] == GRID[curr_x][curr_y]) or (EXIT[curr_x][curr_y] and GRID[new_x][new_y] != GRID[curr_x][curr_y]):
                        visited[new_x][new_y] = 1
                        queue.append((new_x,new_y))
    # print("max_row : ", max_row)
    return max_row - 3 + 1

def move(r, c, d, idx):
    global R,C
    while True:
        # 더 내려갈 수 있는지 확인
        # print(r, " " , c)
        if r+2<R+3 and c-1>=0 and c+1<C and GRID[r+1][c-1] + GRID[r+1][c] + GRID[r+1][c+1] + GRID[r+2][c] == 0:
            r += 1
            c += 0
        # 왼쪽 아래
        elif r+2<R+3 and c-2>=0 and GRID[r-1][c-1] + GRID[r][c-2] + GRID[r+1][c-1] + GRID[r+1][c-2] + GRID[r+2][c-1] == 0:
            r += 1
            c -= 1
            d = (d+3)%4
        # 오른쪽 아래
        elif r+2<R+3 and c+2<C and GRID[r-1][c+1] + GRID[r][c+2] + GRID[r+1][c+1] + GRID[r+1][c+2] + GRID[r+2][c+1] == 0:
            r += 1
            c += 1
            d = (d+1)%4
        else:
            break
    # 맵 안에 있는지 확인
    if inRange(r,c) and all(inRange(r+dr[i],c+dc[i]) for i in range(4)):
        GRID[r][c] = idx
        for i in range(4):
            GRID[r+dr[i]][c+dc[i]] = idx
        EXIT[r+dr[d]][c+dc[d]] = 1
        # BFS
        global answer
        answer += bfs(r, c)
    else:
        for i in range(R+3):
            for j in range(C):
                GRID[i][j] = 0
                EXIT[i][j] = 0
        return False
    # print("G",GRID)
    # print("E",EXIT)
    return True

def main():
    global answer
    elf_idx = 1
    for data in ELF:
        # print(data)
        r = 0
        c = data[0] - 1
        d = data[1]
        flag = move(r, c, d, elf_idx)
        elf_idx += 1
    print(answer)

main()