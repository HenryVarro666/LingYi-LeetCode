def _mode(S):
    if 'i' not in S or 'f' not in S:
        return '`f[j]` = 以值 `j` 结尾、按「增减增减…」摆放的数组个数（值域已平移到 `0..r-l`）'
    if S['i'] % 2:
        return f"第 {S['i'] + 1} 个数：==增==，上一个数 `< j` → `f[j]` = 前缀和 `f[0..j-1]`"
    return f"第 {S['i'] + 1} 个数：==减==，上一个数 `> j` → `f[j]` = 后缀和 `f[j+1..]`"


def _run(S):
    if 'pre' in S and 'suf' not in S:
        return f"前缀和 `pre` = {S['pre']}"
    if 'suf' in S:
        return f"后缀和 `suf` = {S['suf']}"
    return ''


def _run2(S):
    if 'i' not in S or 'j' not in S:
        return ''
    if S['i'] % 2 and 'pre' in S:
        return f"`pre` = 已扫过的 `f[0..j-1]` 之和 = =={S['pre']}=="
    if 'suf' in S:
        return f"`suf` = 已扫过的 `f[j+1..]` 之和 = =={S['suf']}=="
    return ''


CONFIG = dict(
    num=3699, title='锯齿形数组的总数 I', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前缀和优化 DP + 对称性',
    tags=['灵神题单·动态规划', '前缀和优化 DP', '难度分 2123'],
    code='''
class Solution:
    def zigZagArrays(self, n: int, l: int, r: int) -> int:
        MOD = 1_000_000_007
        k = r - l + 1
        f = [1] * k

        for i in range(1, n):
            if i % 2:  # 增
                pre = 0
                for j, v in enumerate(f):
                    f[j] = pre % MOD
                    pre += v
            else:  # 减
                suf = 0
                for j in range(k - 1, -1, -1):
                    v = f[j]
                    f[j] = suf % MOD
                    suf += v

        return sum(f) * 2 % MOD
''',
    call='Solution().zigZagArrays(4, 1, 3)',
    expect=16,
    skip=['for j, v in enumerate', 'for j in range(k - 1'],
    views=[
        dict(type='text', h=70, size=24, fn=_mode),
        dict(type='array', var='f', label='f（值域平移为 0..k-1，下标 = 值）', h=300, cell=110,
             pointers={'j': 'blue'},
             color=lambda S, i, v: 'yellow' if S.get('j') == i else None),
        dict(type='text', h=70, size=24, fn=_run2),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'cyan'), 'pre', 'suf', ('f', 'f', 'green')],
    captions={
        'k = r - l + 1': '值域 `[l, r]` 平移成 `[0, k-1]`，`k = {k}` 个取值',
        'f = [1] * k': '`f[j] = 1`：只放 1 个数时，以 `j` 结尾的方案各 1 种',
        'for i in range': lambda S, B, r: (f'放第 `{S.i + 1}` 个数（`i = {S.i}`）' if S.get('i') != B.get('i') or S.i == 1 and B.get('i') is None else '`n - 1` 轮都做完了，循环结束'),
        'if i % 2': lambda S, B, r: (f'`i = {S.i}` 是奇数 → ==增==：新数比上一个数大' if S.i % 2 else f'`i = {S.i}` 是偶数 → ==减==：新数比上一个数小'),
        'pre = 0': '`pre` 从 0 开始，累加 `f[0..j-1]`',
        'f[j] = pre % MOD': '新的 `f[{j}]` = 前缀和 `{pre}`（上一个数只能取比 `{j}` 小的值）',
        'pre += v': '把旧的 `f[{j}] = {v}` 并入前缀和 → `pre = {pre}`',
        'suf = 0': '`suf` 从 0 开始，从右往左累加 `f[j+1..]`',
        'v = f[j]': '先取出旧的 `f[{j}] = {v}`，下一句才会覆盖它',
        'f[j] = suf % MOD': '新的 `f[{j}]` = 后缀和 `{suf}`（上一个数只能取比 `{j}` 大的值）',
        'suf += v': '把旧的 `f[{j}] = {v}` 并入后缀和 → `suf = {suf}`',
        'return': '只算了「增减增减」型，再 ×2 得到「减增减增」型：`{sum(f)} × 2` = =={ret}==',
    },
    cards=dict(
        one_liner='增减交替，只算一种走向，答案乘 2',
        complexity='时间 `O(n(r-l))`，空间 `O(r-l)`',
        problem=['长度为 `n`、取值在 `[l, r]`，相邻不等且任意三连不单调的数组有多少个',
                 '答案对 `10^9+7` 取模',
                 '示例：`n=3, l=1, r=3` → `10`；本视频：`n=4, l=1, r=3`'],
        quote='所以锯齿形数组是一个增减增减交替的数组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不能连增也不能连减 → ==增、减严格交替==',
              '`f[j]`：以 `j` 结尾的方案数；增 → 前缀和，减 → 后缀和',
              '「增减增减」与「减增减增」一一对应（值取反）→ 只算一种再 ×2'],
        summary=['时间 `O(n(r-l))`，空间 `O(r-l)`',
                 '前缀和 / 后缀和边扫边更新：先 `v` 取旧值，再覆盖 `f[j]`，最后并入 `pre`',
                 '优化二用对称性只留一个数组；题解还给了不用对称性的两个数组写法，及为 3700 题铺垫的 reverse 写法',
                 '易错：循环里取模 `pre % MOD`，`pre` 本身可以不取模（Python 大整数）'],
    ),
)
