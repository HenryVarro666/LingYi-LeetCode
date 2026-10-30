GUARDS = [[0, 0], [2, 2]]
WALLS = [[0, 2], [1, 1]]


def _color(S, i, j, v):
    if v == -1:
        return 'blue' if [i, j] in S['guards'] else 'purple'
    if v == 1:
        return 'orange'
    return None


CONFIG = dict(
    num=2257, title='统计网格图中没有被保卫的格子数', difficulty='Medium', category='网格图',
    author='灵茶山艾府', technique='模拟 · 从警卫出发标记视线',
    tags=[],
    code='''
# 左右上下
DIRS = (0, -1), (0, 1), (-1, 0), (1, 0)

class Solution:
    def countUnguarded(self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]) -> int:
        guarded = [[0] * n for _ in range(m)]

        # 标记警卫格子、墙格子
        for x, y in guards:
            guarded[x][y] = -1
        for x, y in walls:
            guarded[x][y] = -1

        # 遍历警卫
        for x0, y0 in guards:
            # 遍历视线方向（左右上下）
            for dx, dy in DIRS:
                # 视线所及之处，被保卫
                x, y = x0 + dx, y0 + dy
                while 0 <= x < m and 0 <= y < n and guarded[x][y] != -1:
                    guarded[x][y] = 1  # 被保卫
                    x += dx
                    y += dy

        # 统计没被保卫（值为 0）的格子数
        return sum(row.count(0) for row in guarded)
''',
    call='Solution().countUnguarded(3, 4, %r, %r)' % (GUARDS, WALLS),
    expect=2,
    skip=['x += dx', 'for x, y in guards', 'for x, y in walls', 'for dx, dy in DIRS', 'for x0, y0 in guards', 'DIRS = '],
    max_steps=80,
    views=[
        dict(type='grid', var='guarded', label='guarded（蓝=警卫 紫=墙 橙=被保卫；黄框=当前警卫，粉框=视线）', cell=110,
             color=_color, cursors=[('x0', 'y0', 'yellow'), ('x', 'y', 'pink')], h=420),
        dict(type='text', fn=lambda S: (f"警卫 `({S['x0']},{S['y0']})`，方向 `({S['dx']},{S['dy']})`" if 'dx' in S and 'x0' in S else ''), size=28, h=60),
    ],
    watch=[('警卫', '(x0, y0)', 'yellow'), ('方向', '(dx, dy)', 'blue'), ('视线', '(x, y)', 'pink')],
    captions={
        'guarded = [[0]': '`guarded` 全 0：0 = 空格且没人看到；先不管视线',
        'guarded[x][y] = -1': '`({x},{y})` 是警卫或墙，标记 `-1`：==以后视线走到这里就停==',
        'x, y = x0 + dx, y0 + dy': '从警卫 `({x0},{y0})` 出发，朝方向 `({dx},{dy})` 走一步，到 `({x},{y})`',
        'while 0 <= x < m': lambda S, B, r: (
            ('`({0},{1})` 越界 → 这个方向看到头了'.format(S.x, S.y) if not (0 <= S.x < S.m and 0 <= S.y < S.n)
             else '`({0},{1})` 是警卫或墙（-1）→ 视线被挡住，换方向'.format(S.x, S.y) if S.guarded[S.x][S.y] == -1
             else '`({0},{1})` 在界内且不是 -1 → 视线能到，继续'.format(S.x, S.y))),
        'guarded[x][y] = 1': '`({x},{y})` 被警卫看到，标记 `1`（已经是 1 也没关系，重复标记不影响）',
        'y += dy': '沿方向 `({dx},{dy})` 再走一步，到 `({x},{y})`',
        'return sum': lambda S, B, r: '每行数 0 的个数再求和：没被保卫的空格子共 =={}== 个'.format(r),
    },
    cards=dict(
        one_liner='别查格子被谁看到，让警卫沿四个方向把视线走一遍',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 网格里有警卫和墙；警卫能看见上下左右四个方向的所有格子',
                 '视线被墙或别的警卫==挡住==就停；被至少一个警卫看到的格子算被保卫',
                 '求空格子里有多少个没被保卫',
                 '示例：`3×4`，警卫 `[0,0] [2,2]`，墙 `[0,2] [1,1]` → `2`'],
        quote='反过来，遍历警卫及其四个方向的视线，视线所及之处的空格子，标记为被保卫。……如果 (x,y) 处是警卫或者墙，那么标记 guarded[x][y]=-1。当我们遍历到 guarded[x][y]=-1 时，就不再继续遍历。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力：对每个空格子检查四个方向，`O(mn(m+n))`，太慢',
              '反过来：从警卫出发，沿四个方向一直走，走过的格子标记为 `1`',
              '警卫和墙标成 `-1`：当作挡板，同时避免把它们当成空格子数',
              '每个格子至多被标记 4 次（四个方向各一次），总共 `O(mn)`'],
        summary=['时间 `O(mn)`：每个格子至多被 4 个方向各扫一次；空间 `O(mn)`',
                 '易错：先把==所有警卫和墙==都标成 -1，再开始扫视线，否则会穿过后放置的墙',
                 '易错：最后统计的是值为 `0` 的格子，警卫和墙（-1）不算',
                 '相似题：1222. 可以攻击国王的皇后'],
    ),
)
