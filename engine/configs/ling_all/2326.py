M, N = 3, 4
VALS = [1, 2, 3, 4, 5, 6, 7]


CONFIG = dict(
    num=2326, title='螺旋矩阵 IV', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · 方向数组 + 撞墙转向',
    code='''
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

class Solution:
    def spiralMatrix(self, m: int, n: int, head: Optional[ListNode]) -> List[List[int]]:
        ans = [[-1] * n for _ in range(m)]
        i = j = di = 0
        while head:
            ans[i][j] = head.val
            head = head.next
            dx, dy = DIRS[di]
            if not (0 <= i + dx < m and 0 <= j + dy < n and ans[i + dx][j + dy] == -1):
                di = (di + 1) % 4
                dx, dy = DIRS[di]
            i += dx
            j += dy
        return ans
''',
    call=f'Solution().spiralMatrix({M}, {N}, L({VALS}))',
    expect=[[1, 2, 3, 4], [-1, -1, -1, 5], [-1, -1, 7, 6]],
    views=[
        dict(type='linked', label='链表（蓝 = 当前要填的节点 head）', pointers={'head': 'blue'}, h=170),
        dict(type='grid', var='ans', label='ans（黄框 = 当前位置 (i, j)；-1 = 还没填）', cell=90, h=330,
             cursors=[('i', 'j', 'yellow', '(i,j)')],
             color=lambda S, i, j, v: 'green' if v != -1 else None),
        dict(type='text', size=30, fn=lambda S: ('方向 `di = ' + str(S['di']) + '`：' + ('右', '下', '左', '上')[S['di']] + f'，`(dx, dy) = {((0, 1), (1, 0), (0, -1), (-1, 0))[S["di"]]}`') if 'di' in S else ''),
    ],
    watch=['i', 'j', ('di', 'di', 'orange'), 'dx', 'dy'],
    captions={
        'ans = [[-1]': '先造 `{m} × {n}` 的矩阵，全部填 `-1`：==没被链表覆盖的格子最后就是 -1==，同时 `-1` 还能当「没访问过」的标记',
        'i = j = di = 0': '从左上角 `(0, 0)` 出发，方向下标 `di = 0` → 向右（`DIRS` 按右、下、左、上 顺时针排列）',
        'while head': lambda S, B, r: (f'`head` 是节点 `{S.head.val}` → 还有数没填，继续' if S.head else '链表用完了 → 结束，剩下的格子保持 -1'),
        'ans[i][j] = head.val': '把当前节点的值填到 `({i},{j})`：`ans[{i}][{j}] = {ans[i][j]}`',
        'head = head.next': '链表指针后移到下一个节点',
        'dx, dy = DIRS[di]': lambda S, B, r: (f'按当前方向 `di = {S.di}` 取步长 `(dx, dy) = ({S.dx}, {S.dy})`' if S._line == 10
                                              else f'已转向：换成新方向 `di = {S.di}` 的步长 `(dx, dy) = ({S.dx}, {S.dy})`'),
        'if not (0 <=': lambda S, B, r: (f'下一格 `({S.i + S.dx},{S.j + S.dy})` ' + (
            '==越界== → 撞墙，需要转向' if not (0 <= S.i + S.dx < S.m and 0 <= S.j + S.dy < S.n)
            else ('已经填过 → 撞到自己，需要转向' if S.ans[S.i + S.dx][S.j + S.dy] != -1 else '在界内且是 -1 → 直行'))),
        'di = (di + 1) % 4': '顺时针转 90 度：`di = ({B.di} + 1) % 4 = {di}`',
        'i += dx': '`i` += `{dx}` → {i}',
        'j += dy': '`j` += `{dy}` → ({i},{j}) 成为下一个要填的格子',
        'return ans': '链表填完，返回矩阵',
    },
    cards=dict(
        one_liner='沿当前方向直走，撞墙或撞到已填的格子就顺时针转向',
        complexity='时间 `O(mn)`，空间 `O(1)`（不计返回的矩阵）',
        problem=['给 `m`、`n` 和一个链表，按==顺时针螺旋==从左上角填进 `m × n` 矩阵',
                 '多出来的格子填 `-1`',
                 '示例：`m = 3, n = 5, head = [3,0,2,6,8,1,7,9,4,2,5,5,0]`',
                 '本视频：`m = 3, n = 4, head = [1,2,3,4,5,6,7]`'],
        quote='代码同 59. 螺旋矩阵 II，改为在链表上遍历即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`DIRS` 按右、下、左、上顺时针存好，`di` 是当前方向',
              '填完一格就看==下一格==：越界或已经填过（不是 -1）→ `di = (di + 1) % 4`',
              '先把矩阵全填 `-1`，一举两得：既是题目要求的空位值，也是「没访问」标记'],
        summary=['时间 `O(mn)`，空间 `O(1)`（不计答案）',
                 '转向的判断写在==移动之前==：先看下一格行不行，不行先转再走',
                 '链表一空就停，不用单独处理剩余的格子（本来就是 `-1`）',
                 '链表长度不超过 `m * n`，所以不会写出界'],
    ),
)
