def _wt(x):
    s = 0
    while x != 1:
        x = x // 2 if x % 2 == 0 else x * 3 + 1
        s += 1
    return s


LO, HI = 7, 11
WT = {x: _wt(x) for x in range(LO, HI + 1)}


def _tbl(S):
    order = sorted(WT, key=lambda x: (WT[x], x))
    a = '  '.join(f'`{x}`:{WT[x]}' for x in range(LO, HI + 1))
    b = ' → '.join(str(x) for x in order)
    return f'权重（`数:权重`）：{a}\n按权重排序：==[{b}]==，第 4 个是 ==7=='


def _cur(S):
    if 'i' not in S:
        return '`dfs(i)` = 从 `i` 变到 `1` 的步数（权重）'
    i = S['i']
    if i == 1:
        return '`i = 1`：已经是 1，权重 ==0=='
    if i % 2:
        return f'`i = {i}` 是奇数：`3i+1` 必为偶数，一次走两步到 `{(i * 3 + 1) // 2}`'
    return f'`i = {i}` 是偶数：除以 2 到 `{i // 2}`，走 1 步'


CONFIG = dict(
    num=1387, title='将整数按权重排序', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索 + 稳定排序',
    tags=['灵神题单·动态规划', '难度分 1507'],
    code='''
@cache  # 缓存装饰器，避免重复计算 dfs 的结果（记忆化）
def dfs(i: int) -> int:
    if i == 1:
        return 0
    if i % 2:
        return dfs((i * 3 + 1) // 2) + 2
    return dfs(i // 2) + 1

class Solution:
    def getKth(self, lo: int, hi: int, k: int) -> int:
        # sorted 是稳定排序，我们只需比较 dfs 的返回值
        return sorted(range(lo, hi + 1), key=dfs)[k - 1]
''',
    call='Solution().getKth(7, 11, 4)',
    expect=7,
    views=[
        dict(type='text', h=110, fn=_cur),
        dict(type='calls', h=470),
        dict(type='text', h=120, fn=_tbl),
    ],
    watch=[('i', 'i', 'blue'), ('lo', 'lo'), ('hi', 'hi'), ('k', 'k')],
    max_steps=90,
    captions={
        'if i == 1': lambda S, B, r: ('`i = 1`：递归边界，权重 0' if S.i == 1 else f'`i = {S.i}` 还不是 1，继续往下'),
        'if i % 2': lambda S, B, r: (f'`{S.i} % 2` 余 1 → ==奇数==，走 `3i+1`' if S.i % 2 else f'`{S.i}` 是偶数，走 `i / 2`'),
        'return 0': '到 1 了，==权重 0==。往回「归」时每层按奇偶加 2 或加 1，并被缓存',
        'return dfs((i * 3 + 1)': lambda S, B, r: (f'`dfs({B["i"]})` 是奇数：`(3×{B["i"]}+1)//2 = {S.i}`，先去求 `dfs({S.i})`，回来再 `+2`' if r is None
                                                   else f'奇数：`dfs({S.i})` = 下一个状态 + 2 = =={r}=='),
        'return dfs(i // 2)': lambda S, B, r: (f'`dfs({B["i"]})` 是偶数：`{B["i"]}//2 = {S.i}`，先去求 `dfs({S.i})`，回来再 `+1`' if r is None
                                               else f'偶数：`dfs({S.i})` = 下一个状态 + 1 = =={r}=='),
        'return sorted': lambda S, B, r: (f'`sorted(range({S.lo}, {S.hi + 1}), key=dfs)[{S.k - 1}]`：按 dfs 权重稳定排序，取第 `k` 个 → =={r}==' if r is not None
                                          else '对每个数调用 `dfs` 作 key，已缓存的状态直接命中'),
    },
    cards=dict(
        one_liner='3n+1 猜想：dfs 求权重，缓存共享，稳定排序后取第 k 个',
        complexity='时间 `O(n log n + C)`，空间 `O(n)`',
        problem=['权重 = 把 `x` 变成 `1` 的步数：偶数 `x/2`，奇数 `3x+1`',
                 '把 `[lo, hi]` 按权重升序排序，权重相同按数值升序，返回第 `k` 个',
                 '示例：`lo=7, hi=11, k=4`，权重 `[16,3,19,6,14]` → 排序后第 4 个是 `7`'],
        quote='由于 i 是奇数，3i+1 一定是偶数，所以也可以直接走两步，写成 dfs(i) = dfs((3i+1)/2)+2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i)`：从 `i` 到 `1` 的权重；偶数 `+1`，奇数合并两步 `+2`',
              '链条会汇到重复状态，`@cache` 记忆化；`dfs` 写在类外，多组数据共享缓存',
              '`sorted` 是稳定排序，只用 `key=dfs`，相同权重自然保持数值升序'],
        summary=['时间 `O(n log n + C)`，`C ≤ 1625` 是记忆化状态数；快速选择可做到 `O(n + C)`',
                 '奇数一步合并两步：`(3i+1)//2` 后加 2，别忘了是整除',
                 '`range` 本来就升序，靠稳定排序处理同权重，不用写二元 key',
                 '递归边界 `dfs(1) = 0`；缓存装饰器 `@cache` 来自 `functools`'],
    ),
)
