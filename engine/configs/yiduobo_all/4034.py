def _board(S):
    s = S['source']
    t = S['target']
    return [['象' if [r, c] == s else '目标' if [r, c] == t else '' for c in range(1, 9)] for r in range(1, 9)]


def _bcolor(S, i, j, v):
    r, c = i + 1, j + 1
    sr, sc = S['source']
    tr, tc = S['target']
    if [r, c] == [sr, sc]:
        return 'blue'
    if [r, c] == [tr, tc]:
        return 'pink'
    if r + c == sr + sc or r - c == sr - sc:
        return 'cyan'
    return None


CONFIG = dict(
    num=4034, title='象到达目标格子的最少移动步数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='坐标和奇偶 + 同对角线判断', tags=[],
    code='''
class Solution(object):
    def minBishopMoves(self, source, target):
        
        if (source[0] + source[1]) % 2 != (target[0] + target[1]) % 2:
            return -1
        
        if source[0] + source[1] == target[0] + target[1] or source[0] - source[1] == target[0] - target[1]:
            return 1
        
        return 2
''',
    call='Solution().minBishopMoves([4, 2], [1, 3])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: f"和：`{S['source'][0]+S['source'][1]}` vs `{S['target'][0]+S['target'][1]}`    差：`{S['source'][0]-S['source'][1]}` vs `{S['target'][0]-S['target'][1]}`", size=26),
        dict(type='grid', var=_board, rows=list(range(1, 9)), cols=list(range(1, 9)), color=_bcolor, cell=64, h=560,
             label='8×8 棋盘（蓝 = 象，粉 = 目标，青 = 象一步能到）'),
    ],
    watch=[('source', 'source', 'blue'), ('target', 'target', 'pink')],
    captions={
        'if (source[0] + source[1]) % 2': '坐标和奇偶：`{source[0]+source[1]}` 是 {"奇" if (source[0]+source[1])%2 else "偶"}，`{target[0]+target[1]}` 是 {"奇" if (target[0]+target[1])%2 else "偶"} → ==奇偶相同，同色可达==',
        'source[0] + source[1] == target[0] + target[1]': '右对角线看和，左对角线看差：和 `{source[0]+source[1]}` ≠ `{target[0]+target[1]}`，差 `{source[0]-source[1]}` ≠ `{target[0]-target[1]}` → ==不在同一对角线==',
        'return 2': '同色但不共线：先左后右（或先右后左）走两步 → 返回 `2`',
    },
    cards=dict(
        one_liner='坐标和的奇偶不变，同色格子最多两步',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['8×8 棋盘，象沿对角线移动任意格',
                 '求恰好到达 `target` 的最少移动次数，无法到达返回 `-1`',
                 '本视频：`[4,2] → [1,3]`，答案 `2`'],
        quote='无论象怎样行走，其坐标之和的奇偶性是不会产生变化的。',
        quote_src='—— yiduobo 题解原文',
        idea=['沿对角线走 `k` 格：横纵坐标同加减 `k`，或一加一减 `k`，和的奇偶不变',
              '同一条对角线：下标之和相等或下标之差相等，一步到位',
              '否则先左后右或先右后左，两步走到'],
        after=[dict(heading='三种情况', lines=['和的奇偶不同：返回 `-1`（异色）', '同色且和相等或差相等：返回 `1`', '其余同色格子：返回 `2`', '例：`[1,1] → [3,4]`：`2` 与 `7` 奇偶不同 → `-1`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '先判奇偶（`-1`），再判共线（`1`），其余是 `2`',
                 '共线要两种都查：和相等、差相等',
                 '对比灵神：同一结论，yiduobo 直接用 `source[0]` 等下标，灵神先拆成 sx, sy'],
    ),
)
