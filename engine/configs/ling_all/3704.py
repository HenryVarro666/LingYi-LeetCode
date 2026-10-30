def _txt(S):
    I = S['_inner']
    if 'borrowed' not in I:
        return '从最低位往高位填：`s` 是 `n` 的各位数字，借位和前导零都记在状态里'
    d = I.get('d')
    br = '被低位借走 1' if I['borrowed'] else '没被借'
    num = '两数都无前导零' if I['is_num'] else '其中一个数已进入前导零'
    base = f"`dfs(i={I['i']}, borrowed={I['borrowed']}, is_num={I['is_num']})`：{br}，{num}"
    if d is not None:
        base += f'；当前位 `d = {d}`'
    return base


def _ii(S):
    I = S['_inner']
    return I.get('i') if 'borrowed' in I else None


CONFIG = dict(
    num=3704, title='统计和为 N 的无零数对', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP · 借位 + 前导零',
    tags=['灵神题单', '难度分 2419'],
    code='''
# 返回两个 1~9 的整数和为 target 的方案数
def two_sum_ways(target: int) -> int:
    return max(min(target - 1, 19 - target), 0)  # 保证结果非负

class Solution:
    def countNoZeroPairs(self, n: int) -> int:
        s = list(map(int, str(n)))
        m = len(s)

        # borrowed = True 表示被低位（i+1）借了个 1
        # is_num = True 表示之前填的数位，两个数都无前导零
        @cache
        def dfs(i: int, borrowed: bool, is_num: bool) -> int:
            if i < 0:
                # borrowed 必须为 False
                return 0 if borrowed else 1

            d = s[i] - borrowed
            res = 0

            # 情况一：两个数位都不为 0
            if is_num:
                res = dfs(i - 1, False, True) * two_sum_ways(d)  # 不向高位借 1
                res += dfs(i - 1, True, True) * two_sum_ways(d + 10) # 向高位借 1

            # 情况二：其中一个数位填前导零
            if i < m - 1:  # 不能是最低位
                if d:
                    # 如果 d < 0，必须向高位借 1
                    # 如果 is_num = True，根据对称性，方案数要乘以 2
                    res += dfs(i - 1, d < 0, False) * (is_num + 1)
                elif i == 0:  # 两个数位都填 0，只有当 i = 0 的时候才有解
                    res += 1

            return res

        return dfs(m - 1, False, True)
''',
    call='Solution().countNoZeroPairs(101)',
    expect=80,
    views=[
        dict(type='text', h=100, size=26, fn=_txt),
        dict(type='array', var='s', label='s（n 的各位数字，下标 0 是最高位）', cell=100, h=230,
             color=lambda S, i, v: 'blue' if i == _ii(S) else None),
        dict(type='calls', h=330, hide=('s', 'm')),
    ],
    watch=[('i', 'i', 'blue'), ('borrowed', 'borrowed', 'orange'), ('is_num', 'is_num', 'purple'), ('d', 'd', 'yellow'), ('res', 'res', 'green')],
    skip=['res = 0', 'm = len(s)', 'if is_num:', 'if i < 0:', 'if i < m - 1:'],
    max_steps=90,
    captions={
        'return max(min(target - 1, 19 - target), 0)': '两个 1~9 的数和为 `{target}`：一共 `min({target}-1, 19-{target})` 种，负数按 0 算 → ==`{ret}`==',
        's = list(map(int, str(n)))': '把 `n` 拆成数字：`s = {s}`',
        'm = len(s)': '`n` 有 `m = {m}` 位',
        'if i < 0': lambda S, B, r: ('`i < 0`：所有数位填完，要求没有欠着高位的借位' if S.i < 0 else f'`i = {S.i}`：还要填这一位'),
        'return 0 if borrowed else 1': lambda S, B, r: ('还欠着一个借位（`borrowed = True`）→ 这条路无解 ==0==' if S.borrowed else '没有欠借位 → 这条路合法 ==1 种=='),
        'd = s[i] - borrowed': '当前位 `d = s[{i}] - borrowed = {s[i]} - {int(borrowed)} = {d}`：被低位借走就减 1',
        'res = 0': '`res` 累计这个状态的方案数',
        'if is_num': lambda S, B, r: ('`is_num = True`：两个数目前都没有前导零 → 先算两位都是 1~9 的情况' if S.is_num else '`is_num = False`：已有前导零 → 不能再填两个非零数位'),
        'res = dfs(i - 1, False, True)': '==情况一（不借位）==：`d = {B.d}` 拆成两个 1~9 的数，方案数 `two_sum_ways({B.d})` 乘上高位方案',
        'res += dfs(i - 1, True, True)': '==情况一（借位）==：向高位借 1，`d + 10 = {B.d + 10}` 拆成两个 1~9 的数，再乘上高位方案',
        'if i < m - 1': lambda S, B, r: (f'`i = {S.i} < m-1`：不是最低位 → 可以让一个数在这里是前导零' if S.i < S.m - 1 else '`i = m-1` 是最低位：两个数都不能是前导零'),
        'if d:': lambda S, B, r: (f'`d = {S.d} ≠ 0`：另一个数必须填 `d`（有前导零的那个填 0）' if S.d else '`d = 0`：两个数位都只能是 0'),
        'res += dfs(i - 1, d < 0': '==情况二==：一个数填前导零，另一个数位只能是 `d`；`d < 0` 就必须向高位借 1。`is_num` 时左右对称，乘 2',
        'elif i == 0': lambda S, B, r: ('`i = 0`：两个数的最高位都是 0 → 合法，加 1 种' if S.i == 0 else '`i > 0` 且 `d = 0`：高位还有非零数字 → 无解'),
        'res += 1': '两个数最高位都填 0 → `res` += 1',
        'return res': '这个状态的方案数 ==`{res}`==（`@cache` 保证同一状态只算一次）',
        'return dfs(m - 1, False, True)': '从最低位 `i = m-1` 开始：一开始没借位，也没有前导零',
    },
    cards=dict(
        one_liner='从低位往高位填，状态记「借位」和「前导零」',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['无零整数：十进制里没有数字 `0` 的正整数',
                 '给定 `n`，数有多少对无零整数 `(a, b)` 满足 `a + b = n`',
                 '示例：`n = 11` → `8`；视频用 `n = 101` → ==80=='],
        quote='`dfs(i, borrowed, isNum)` 表示在 [0, i] 中填数字，borrowed = true 表示被低位（i+1）借 1，isNum = true 表示右边所填数位没有 0（无前导零）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['当前位 `d = s[i] - borrowed`；向高位借 1 就是 `d + 10`',
              '情况一：两位都在 1~9，方案数 `two_sum_ways(d)` 或 `two_sum_ways(d + 10)`',
              '情况二：一个数是前导零，另一个只能填 `d`；刚开始填前导零时左右对称，乘 2',
              '从最低位开始递归，才能知道要不要借位'],
        summary=['时间、空间都是 `O(log n)`：状态数只有位数 × 4',
                 '易错：`d = 0` 且还不是最高位时，前导零那一支无解',
                 '`two_sum_ways` 用 `max(..., 0)` 保证非负',
                 '同类题：1317 将整数转换为两个无零整数的和',
                 '`cache` 是 Python 3.9+ 的写法，可视化里已预置'],
    ),
)
