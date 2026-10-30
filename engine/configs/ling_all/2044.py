def _txt(S):
    if 'subset_or' not in S:
        return ''
    t, s = S['total_or'], S['subset_or']
    w = max(t.bit_length(), 3)
    return f'`subset_or = {s:0{w}b}`（{s}），`total_or = {t:0{w}b}`（{t}）' + ('  ==已达到最大值==' if s == t else '')


def _cap_if(S, B, ret):
    s, t, i, n = S.subset_or, S.total_or, S.i, S.n
    if s == t:
        return (f'`subset_or = {s}` 已等于 `total_or`：再选什么 OR 都不会变大 → 剩下 `{n - i}` 个数选不选都行，'
                f'一共 `2^{n - i} = {1 << (n - i)}` 种，一次加进答案')
    return f'`subset_or = {s}` 还没到 `total_or = {t}` → 继续往下选'


CONFIG = dict(
    num=2044, title='统计按位或能得到最大值的子集数目', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='子集型回溯 + 提前计数剪枝',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution:
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        total_or = reduce(or_, nums)
        n = len(nums)
        ans = 0

        def dfs(i: int, subset_or: int) -> None:
            if subset_or == total_or:
                nonlocal ans
                ans += 1 << (n - i)
                return
            if i == n:
                return
            dfs(i + 1, subset_or) # 不选 nums[i]
            dfs(i + 1, subset_or | nums[i])  # 选 nums[i]

        dfs(0, 0)
        return ans
''',
    setup='from operator import or_',
    call='Solution().countMaxOrSubsets([3, 5, 1])',
    expect=2,
    views=[
        dict(type='text', h=70, fn=_txt, size=26),
        dict(type='array', var='nums', label='nums（箭头 = 当前决定选不选的数）', h=140, cell=80, pointers={'i': 'blue'},
             dim=lambda S, i, v: i < S.get('i', 0) and False),
        dict(type='calls', h=300),
        dict(type='text', h=60, fn=lambda S: f'答案 `ans = {S["ans"]}`' if 'ans' in S else '', size=26),
    ],
    watch=[('i', 'i', 'blue'), ('subset_or', 'subset_or', 'cyan'), ('total_or', 'total_or', 'green'), ('ans', 'ans', 'yellow')],
    skip=['n = len(nums)', 'ans = 0', 'nonlocal ans', '                return'],
    captions={
        'total_or = reduce': 'OR 的参与者越多结果越大 → 最大值就是全部 OR：`total_or = {total_or}`',
        'dfs(0, 0)': '从 `dfs(0, 0)` 开始：枚举 `nums` 的每个子集，`subset_or` 记录子集的 OR',
        'if subset_or == total_or': _cap_if,
        'ans += 1 <<': '`ans += 2^({n} - {i})` → `{ans}`',
        'if i == n': lambda S, B, r: (f'`i = {S.i} = n`：所有数都决定完了，OR 没达到最大值 → 这个子集不算' if S.i == S.n else f'`i = {S.i} < n`：还有数没决定'),
        '# 不选': '不选 `nums[{i-1}]`：`subset_or` 保持 `{subset_or}`',
        '# 选': '选 `nums[{i-1}]`：`subset_or = {subset_or}`（OR 上它）；`subset_or` 是参数，不用恢复现场',
        'return ans': '搜完：共 `{ret}` 个子集的 OR 等于最大值 `{total_or}`',
    },
    max_steps=100,
    cards=dict(
        one_liner='枚举子集；OR 一旦到顶，剩下的数随便选，直接加 2^(n−i)',
        complexity='时间 `O(2^n)`，空间 `O(n)`',
        problem=['求 `nums` 的所有子集 ==按位或== 能得到的最大值，返回得到最大值的非空子集个数',
                 '下标不同视为不同子集',
                 '本视频：`[3,5,1]` → `2`（最大 OR 是 `7`）'],
        quote='子集 OR 已经等于 totalOr，那么 subsetOr 不可能再变大。所以下标在 [i, n-1] 中的每个数无论是选还是不选，对应的子集 OR 值都等于 totalOr。',
        quote_src='—— 灵茶山艾府题解',
        idea=['OR 越选越大，所以最大值 = 全部 OR = `total_or`',
              '`dfs(i, subset_or)`：枚举每个数选或不选（子集型回溯）',
              '`subset_or` 已经等于 `total_or`：后面 `n−i` 个数随便选，直接 `ans += 2^(n−i)`'],
        result='共 2 个子集的 OR 等于 7 ✓',
        summary=['时间 `O(2^n)`，空间 `O(n)`；最坏仍是指数级（本题可归约为 set cover 计数）',
                 '`subset_or` 是 `int` 参数，每层各持一份，==不用恢复现场==',
                 '先判 `subset_or == total_or`，再判 `i == n`：顺序不能反（`i == n` 时 `2^0 = 1` 也要算）',
                 '原文先给了不剪枝的写法（到叶子再比较），这里选剪枝优化版'],
    ),
)
