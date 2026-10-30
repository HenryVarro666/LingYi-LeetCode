def _form(S):
    if 'length' not in S:
        return '`f[v]` = 长度为 `length`、以 `v` 结尾的「^^^^」型数组个数；`s` = `f` 的前缀和'
    L = S['length']
    if L % 2 == 0:
        return f'长度 {L} 是偶数：最后一步==上升== → `f[v] = s[v-1]`（上一个数比 `v` 小）'
    return f'长度 {L} 是奇数：最后一步==下降== → `f[v] = s[-1] - s[v]`（上一个数比 `v` 大）'


CONFIG = dict(
    num=3699, title='锯齿形数组的总数 I', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='对称性 + 前缀和滚动',
    tags=['灵神题单·动态规划', '难度分 2123'],
    code='''
class Solution(object):
    def zigZagArrays(self, n, l, r):
        
        r -= l
        f = []
        s = []
        for v in range(r + 1):
            f.append(v)
            if not s:
                s.append(f[-1])
            else:
                s.append(s[-1] + f[-1])

        mod = 10 ** 9 + 7

        for length in range(3, n + 1):
            for v in range(r + 1):
                if length % 2 == 0:
                    if v == 0:
                        f[v] = 0
                    else:
                        f[v] = s[v - 1]
                else:
                    f[v] = s[-1] - s[v]
                    if f[v] < 0:
                        f[v] += mod
            
            s = []
            for v in range(r + 1):
                if not s:
                    s.append(f[v])
                else:
                    s.append(s[-1] + f[v])
                    if s[-1] >= mod:
                        s[-1] -= mod

        res = s[-1] + s[-1]
        if res >= mod:
            res -= mod
        return res
''',
    call='Solution().zigZagArrays(5, 1, 3)',
    expect=26,
    skip=['for v in range', 'else:', 9, 30, 34],
    max_steps=90,
    views=[
        dict(type='text', h=70, size=24, fn=_form),
        dict(type='array', var='f', label='f[v]：以 v 结尾的方案数（值域 0..r-l）', h=240, cell=110, pointers={'v': 'blue'},
             color=lambda S, i, x: 'yellow' if S.get('v') == i else None),
        dict(type='array', var='s', label='s[v] = f[0] + … + f[v]（前缀和）', h=240, cell=110, pointers={'v': 'pink'}),
    ],
    watch=[('length', 'length', 'blue'), ('v', 'v', 'cyan'), ('res', 'res', 'green')],
    captions={
        4: '值域 `[l, r]` 平移成 `[0, r-l]`：只关心相对大小，`r` 现在是 `{r}`',
        6: '`s` 将放 `f` 的前缀和',
        8: '长度为 2 的 ^ 形：以 `v` 结尾的上一个数有 `v` 种选法 → `f[{v}] = {v}`',
        10: '`s[0] = f[0]`',
        12: '`s[{v}] = s[{v-1}] + f[{v}]` = {s[-1]}',
        14: '取模用的 `mod`',
        16: lambda S, B, r: (f'推到长度 `{S.length}`' if S.length != B.get('length') else f'长度推到了 `n`，循环结束'),
        18: lambda S, B, r: (f'`length = {S.length}` 是偶数 → 这一步==上升== → 上一个数比 `v` 小，用前缀和' if S.length % 2 == 0 else f'`length = {S.length}` 是奇数 → 这一步==下降== → 上一个数比 `v` 大，用后缀和'),
        20: '`v = 0`：没有比 0 更小的数 → `f[0] = 0`',
        22: '上一个数 `< {v}`：`f[{v}] = s[{v-1}] = {f[v]}`',
        24: '上一个数 `> {v}`：后缀和 = 总和 `s[-1]` 减去 `s[{v}]` → `f[{v}] = {f[v]}`',
        25: '取模后相减可能为负：`f[v] < 0` 吗？{f[v] < 0}',
        26: '加回 `mod` 保证非负',
        28: '`f` 这一整行算完了，重新用它建前缀和 `s`',
        31: '`s[0] = f[0] = {f[0]}`',
        33: '`s[{v}] = s[{v-1}] + f[{v}]` = {s[-1]}',
        35: '超过 `mod` 就减掉一次',
        37: '只数了 ^ 形，v 形与它一一对应 → 答案 ×2 = `{res}`',
        38: '`res >= mod` 吗？{res >= mod}',
        40: '返回 `{res}`',
    },
    cards=dict(
        one_liner='^ 形与 v 形一一对应：只数一种再乘 2',
        complexity='时间 `O(n(r-l))`，空间 `O(r-l)`',
        problem=['长度 `n`、取值 `[l, r]`、相邻不等且任意三连不单调的数组个数',
                 '示例：`n=3, l=1, r=3` → `10`',
                 '本视频：`n=5, l=1, r=3`'],
        quote='对于任意一个^^^^^形的锯齿数组，……只需将所有元素都用r - l再减去，就可以得到一个vvvvv形的锯齿数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `[l, r]` 平移成 `[0, r-l]`，下标直接当取值',
              '`f[v]` 表示以 `v` 结尾；偶数长度对应上升、奇数长度对应下降',
              '两种转移都是区间和 → 每轮把 `f` 转成前缀和 `s`，滚动复用'],
        summary=['时间 `O(n(r-l))`，空间 `O(r-l)`',
                 '从长度 2 起手：`f[2][v] = v`，循环从 3 开始',
                 '`v = 0` 时没有更小的数，要单独置 0',
                 '后缀和 = `s[-1] - s[v]`，可能为负，要加回 `mod`',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
