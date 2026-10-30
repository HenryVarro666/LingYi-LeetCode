NUMS, K = [1, 2, 1, 1, 3], 2


def _fs_table(S):
    fs = S.get('fs') or {}
    return [list(v) for v in fs.values()] or [[0] * (S['k'] + 1)]


def _fs_rows(S):
    fs = S.get('fs') or {}
    return [f'x={key}' for key in fs] or ['']


def _cell(S, r, c, v):
    fs = S.get('fs') or {}
    x, j = S.get('x'), S.get('j')
    if x is None or j is None or S.get('_line', 0) < 10:
        return None
    keys = list(fs)
    if r < len(keys) and keys[r] == x and c == j:
        return 'yellow'
    if r < len(keys) and keys[r] == x:
        return 'blue'
    return None


def _formula(S):
    x, j = S.get('x'), S.get('j')
    if x is None or j is None or 'f' not in S:
        return '`f[x][j]` = 以 x 结尾、至多 j 个相邻不同对的最长子序列；`mx[j+1]` = 所有 x 里 `f[x][j]` 的最大值'
    return (f'`f[{j}] = max(f[{j}], mx[{j}]) + 1`：接在 {x} 后面（相同）或接在别的数后面（用 `mx[{j}]`，多一个不同对）')


CONFIG = dict(
    num=3177, title='求出最长好子序列 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='DP + 全局最大值数组 mx',
    tags=['其他线性 DP', '难度分 2365'],
    code='''
class Solution:
    def maximumLength(self, nums: List[int], k: int) -> int:
        fs = {}
        mx = [0] * (k + 2)
        for x in nums:
            if x not in fs:
                fs[x] = [0] * (k + 1)
            f = fs[x]
            for j in range(k, -1, -1):
                f[j] = max(f[j], mx[j]) + 1
                mx[j + 1] = max(mx[j + 1], f[j])
        return mx[-1]
''',
    call=f'Solution().maximumLength({NUMS!r}, {K})',
    expect=4,
    skip=['mx = [0]', 'for j in range', 'for x in nums'],
    max_steps=70,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 和当前 x 相同的位置）', h=170, cell=80,
             color=lambda S, i, v: 'blue' if S.get('x') == v else None),
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='table', var=_fs_table, label='fs[x][j]：以 x 结尾、至多 j 个相邻不同对的最长长度（黄 = 正在更新）', h=250, cell=80,
             rows=_fs_rows, cols=lambda S: [f'j={t}' for t in range(S['k'] + 1)], color=_cell),
        dict(type='array', var='mx', label='mx[j+1] = 所有结尾里 f[·][j] 的最大值（mx[0] 恒为 0）', h=170, cell=80,
             pointers={'j': 'pink'}),
    ],
    watch=[('x', 'x', 'blue'), ('j', 'j', 'pink'), ('f[j]', 'f[j]', 'green')],
    captions={
        'fs = {}': '`fs[x]` 记录「以 x 结尾」的各种长度，按需创建',
        'mx = [0]': '`mx` 长 `k+2`：往左多放一个 0，`mx[j]` 就表示 `f[·][j-1]` 的最大值，省去判断 `j>0`',
        'if x not in fs': lambda S, B, r: (f'取下一个数 `x = {S.x}`：第一次出现 → 新建长为 `k+1` 的全 0 数组' if S.x not in B.fs else f'取下一个数 `x = {S.x}`：以前出现过，沿用 `fs[{S.x}]`'),
        'f = fs[x]': '`f = fs[{x}] = {f}`',
        'f[j] = max(': lambda S, B, r: (f'`j = {S.j}`：`f[{S.j}] = max(f[{S.j}], mx[{S.j}]) + 1` = `max({B.f[S.j]}, {S.mx[S.j]}) + 1` = =={S.f[S.j]}==（接相同 vs 接别的数）'),
        'mx[j + 1] = max': '`mx[{j+1}] = max({B.mx[j+1]}, f[{j}]) = {mx[j+1]}`：更新 `j` 个不同对时的全局最大',
        'return mx[-1]': '`mx[k+1]` 就是至多 `k` 个不同对的最长好子序列：=={ret}==',
    },
    cards=dict(
        one_liner='f[x][j] 记结尾；mx[j] 记所有结尾里的最大',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['`nums` 的子序列中，相邻不同的位置 `seq[i] != seq[i+1]` ==不超过 k 个==就是好序列',
                 '求最长好子序列的长度',
                 '示例：`nums=[1,2,1,1,3], k=2` → `4`；`nums=[1,2,3,4,5,1], k=0` → `2`'],
        quote='只需要维护 mx，无需判断 x 和子序列的最后一个数是否相等……用 f[x][j-1] + 1 更新 f[x][j] 的最大值其实不会改变 f[x][j]。',
        quote_src='—— 灵茶山艾府题解（进一步优化）',
        idea=['`f[x][j]`：以 `x` 结尾、至多 `j` 个相邻不同对的最长子序列',
              '接在相同的数后面：`f[x][j] + 1`；接在不同的数后面：`mx[j] + 1`（`j` 少一个）',
              '用 `mx` 取代枚举结尾；`mx` 左边补 0，`j` 倒序枚举避免用到刚覆盖的值'],
        summary=['时间 `O(nk)`，空间 `O(nk)`（哈希表里每个不同的数一行）',
                 '易错：`j` ==必须倒序==，否则 `mx[j]` 已被本轮的 `x` 更新',
                 '前一版本维护最大 + 次大 + 结尾数，处理 `x == num` 的情况；本版证明可以省掉',
                 '相似题：CF264C Choosing Balls'],
    ),
)
