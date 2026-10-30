def _ops(l, r):
    return [(x.bit_length() + 1) // 2 for x in range(l, r + 1)]


def _ops_var(S):
    n = S.get('n')
    if n is None or n < 1:
        return None
    return _ops(1, n)


def _col(S, i, v):
    return {1: 'blue', 2: 'pink', 3: 'green', 4: 'orange'}.get(v)


def _top(S):
    return '询问 `[l, r]`：`tot = f(r) - f(l-1)` = 区间内每个数的操作次数之和，答案 `ceil(tot / 2)`'


def _f_txt(S):
    I = S.get('_inner', {})
    if 'm' not in I:
        return ''
    m = I['m']
    s = f"`n = {I['n']}` 的二进制长度 `m = {m}`"
    if 'k' in I:
        s += f"，小于 m 的最大偶数 `k = {I['k']}`"
    return s


CONFIG = dict(
    num=3495, title='使数组元素都变为零的最少操作次数', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='数学公式 · 前缀和 O(1)',
    tags=['灵神题单', '难度分 2206'],
    code='''
def f(n: int) -> int:
    if n == 0:
        return 0
    m = n.bit_length()
    k = (m - 1) // 2 * 2
    res = (k << k >> 1) - (1 << k) // 3  # -1 可以省略
    return res + (m + 1) // 2 * (n + 1 - (1 << k))

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        return sum((f(r) - f(l - 1) + 1) // 2 for l, r in queries)
''',
    call='Solution().minOperations([[1,2],[2,6]])',
    expect=5,
    views=[
        dict(type='text', fn=_top, h=70),
        dict(type='array', var='queries', label='queries', h=190, cell=110),
        dict(type='array', var=_ops_var, color=_col, label='ops：1..n 每个数单独操作到 0 的次数（f(n) = 它们的和）', h=230, cell=80),
        dict(type='text', fn=_f_txt, h=70),
    ],
    watch=['n', 'm', 'k', 'res'],
    captions={
        'if n == 0': '`n = {n}`：f(n) 是 [1, n] 里每个数单独操作次数的总和；`n = 0` 时总和为 0',
        'return 0': '空区间，返回 0',
        'm = n.bit_length()': '`n = {n}` 的二进制长度 `m = {m}`：每操作一次右移 2 位，变成 0 要 `ceil(m/2)` 次',
        'k = (m - 1)': '`k` = 小于 m 的最大偶数 = =={k}==：长度 1..k 的数两个一组（长 1、2 各 1 次，长 3、4 各 2 次……）',
        'res = (k << k': '前面完整的几组之和 `k·2^(k-1) - (2^k-1)/3` = =={res}==（错位相减化简）',
        'return res + (m + 1)': '再加上长度 k+1..m 的数：共 `n + 1 - 2^k` = {n + 1 - (1 << k)} 个，每个 `ceil(m/2) = {(m + 1) // 2}` 次 → `f({n}) = {ret}`',
        'return sum(': '每个询问 `[l, r]`：`tot = f(r) - f(l-1)`，一次操作处理两个数，所以加上 `(tot + 1) // 2`（向上取整）。先算 f(r)，再算 f(l-1)',
    },
    cards=dict(
        one_liner='右移 2 位 = 除以 4：只算总次数，答案是总数的一半',
        complexity='时间 `O(q)`，空间 `O(1)`',
        problem=['对每个 `[l, r]`，数组是 `l, l+1, ..., r`；每次选两个数 `a, b`，都换成下取整的 `a/4`',
                 '求全部变 0 的最少操作次数，所有询问的结果相加',
                 '示例：`[[1,2],[2,4]]` → `3`；本视频：`[[1,2],[2,6]]` → `5`'],
        quote='a 除以 4 下取整等价于 a 右移 2 位。所以把一个长为 m 的二进制数变成 0，需要操作 ⌈m/2⌉ 次。……算出了 tot，就算出了答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个数单独需要 `ceil(m/2)` 次，一次操作能同时推进两个数',
              '连续整数的 ops 相邻至多差 1，所以最大值不会卡住：答案 = `ceil(tot / 2)`',
              '`tot = f(r) - f(l-1)`，`f(n)` 按二进制长度分组求和，化简成 `O(1)` 公式'],
        summary=['时间 `O(q)`，空间 `O(1)`',
                 '`f(0)` 要特判（`bit_length` 为 0 时 `k - 1` 会出问题）',
                 '`ceil(x/2)` 写成 `(x + 1) // 2`',
                 '优化前的写法用循环对每个长度分组求和，时间 `O(q log U)`；这里是化简后的 `O(1)` 版本'],
    ),
)
