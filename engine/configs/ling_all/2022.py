ORIG = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ans = S.get('ans')
    n = S.get('n', 1)
    cv.text((x0 + 18, y0 + 4), 'ans（每一行是 original 的一段切片）', 24, T['muted'], bold=True)
    if not ans:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2 + 10), '空', 30, T['dim'], anchor='mm')
        return
    cell = min(84, (x1 - x0 - 120) / max(n, 1))
    rh = min(84, (y1 - y0 - 60) / max(len(ans), 1))
    sx = x0 + 90 + ((x1 - x0 - 120) - cell * n) / 2
    sy = y0 + 56
    for r, row in enumerate(ans):
        cv.text((sx - 14, sy + r * rh + rh / 2), f'行{r}', 20, T['muted'], anchor='rm')
        for c, v in enumerate(row):
            fresh = r == len(ans) - 1
            X, Y = sx + c * cell, sy + r * rh
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + rh - 2), fill=T['green'] if fresh else T['panel2'], r=6,
                    outline=T['yellow'] if fresh else T['border'], width=3 if fresh else 1)
            cv.text((X + cell / 2, Y + rh / 2), v, 28, T['bg'] if fresh else T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=2022, title='将一维数组转变成二维数组', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='长度校验 + 按列数切片（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        k = len(original)
        if k != m * n:
            return []
        ans = []
        for i in range(0, k, n):
            ans.append(original[i:i + n])
        return ans
''',
    call=f'Solution().construct2DArray({ORIG}, 3, 3)',
    expect=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    views=[
        dict(type='array', var='original', label='original（蓝框 = 这一步切出的一段 original[i:i+n]）', cell=70, h=190,
             pointers={'i': 'blue'}, window=('i', 'min(i + n - 1, k - 1)'),
             dim=lambda S, i, v: 'i' in S and i < S['i']),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('m', 'm'), ('n', 'n'), ('k', 'k'), ('i', 'i', 'blue')],
    captions={
        'k = len(original)': '`original` 一共 `k = {k}` 个数',
        'if k != m * n': lambda S, B, r: (f'`k = {S.k}`，`m × n = {S.m * S.n}` → 个数对不上，==没法恰好填满== → 返回空数组' if S.k != S.m * S.n
                                          else f'`k = {S.k}` = `m × n = {S.m * S.n}` → 个数刚好，可以切'),
        'ans = []': '`ans` 先放空，后面一行一行加',
        'for i in range(0, k, n)': lambda S, B, r: ('已经切到末尾了，循环结束' if 'i' in B and S.i == B.i
                                                     else f'每隔 `n = {S.n}` 个数切一行：这一行从 `i = {S.i}` 开始'),
        'ans.append': '切出 `original[{i}:{i + n}]` = `{original[i:i + n]}`，作为第 {len(ans)} 行加入 `ans`',
        'return ans': '`m = {m}` 行都切好了 → 返回 `{ans}`',
    },
    cards=dict(
        one_liner='个数对得上，就每隔 n 个切一刀',
        complexity='时间 `O(mn)`，空间 `O(1)`（不计返回值）',
        problem=['把一维数组 `original` 按顺序填成 `m` 行 `n` 列的二维数组',
                 '`original` 的个数必须==恰好等于== `m × n`，否则返回空数组',
                 '示例：`[1,2,3,4], m=2, n=2` → `[[1,2],[3,4]]`；`[1,2], m=1, n=1` → `[]`'],
        quote='k := len(original); if k != m*n { return nil }；for i := 0; i < k; i += n { ans = append(ans, original[i:i+n]) }',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['先判长度：`k != m * n` 就一定填不满（或放不下）',
              '否则 `i` 每次加 `n`，`original[i:i+n]` 正好是一行',
              '切片是左闭右开，不会越界，最后一行刚好在 `k` 处结束'],
        summary=['时间 `O(mn)`（切片复制），空间 `O(1)`（不计答案）',
                 '原文为 Go，已按原逻辑逐行转写为 Python（Go 返回 `nil` → `[]`，`append` → `ans.append`，`i += n` → `range(0, k, n)`）',
                 '易错：必须先判断 `k == m * n`，不然最后一行会不满',
                 '`i` 的步长是列数 `n`，不是行数 `m`'],
    ),
)
