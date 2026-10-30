def _formula(S):
    if 'i' not in S or 'j' not in S or 'f' not in S:
        return '`f[i]` = 跳到 i 时的最大跳跃次数，`-1` 表示到不了'
    i, j, n = S['i'], S['j'], S['nums']
    if S.get('_line') in (7, 8, 9) and j < i:
        d = abs(n[i] - n[j])
        return f'`|{n[i]} − {n[j]}|` = {d}，{"≤" if d <= S["target"] else ">"} `target = {S["target"]}`'
    return f'`f[{i}]` = 到 {i} 号位置最多跳几次'


def _color(S, k, v):
    if 'i' not in S or 'f' not in S:
        return None
    if k == S['i']:
        return 'blue'
    if S.get('_line') in (7, 8, 9) and 'j' in S and k == S['j'] and S['j'] < S['i']:
        ok = S['f'][S['j']] != -1 and abs(S['nums'][S['i']] - S['nums'][S['j']]) <= S['target']
        return 'green' if ok else 'pink'
    return None


CONFIG = dict(
    num=2770, title='达到末尾下标所需的最大跳跃次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='O(n²) 动态规划：枚举上一跳',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def maximumJumps(self, nums, target):

        f = [0]
        for i in range(1, len(nums)):
            f.append(-1)
            for j in range(i):
                if f[j] != -1 and abs(nums[i] - nums[j]) <= target:
                    f[i] = max(f[i], f[j] + 1)
        
        return f[-1]
''',
    call='Solution().maximumJumps([1,3,6,4,1,2], 2)',
    expect=3,
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='nums', label='nums（蓝 = 要到达的 i，绿 = 能跳过来的 j，粉 = 不行）', h=200, cell=100,
             pointers={'i': 'blue', 'j if _line in (7, 8, 9) else None': 'pink'}, pointer_labels={'j if _line in (7, 8, 9) else None': 'j'}, color=_color),
        dict(type='array', var='f', label='f：跳到每个位置的最大次数（-1 = 到不了）', h=200, cell=100,
             pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if 'i' in S and k == S['i'] else ('green' if S.get('_line') in (8, 9) and k == S.get('j') and S['f'][k] != -1 else None)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[i]', 'f[i] if "i" in locals() else None', 'green')],
    captions={
        'f = [0]': '`f[0] = 0`：起点不用跳，已经在 0 号位置',
        'f.append(-1)': '先假设到不了：`f[{i}] = -1`',
        'if f[j] != -1': lambda S, B, r: (
            f'`f[{S.j}] = -1`：根本到不了 {S.j} → 不能从它出发' if S.f[S.j] == -1 else
            (f'`|{S.nums[S.i]} − {S.nums[S.j]}| = {abs(S.nums[S.i] - S.nums[S.j])} ≤ {S.target}`：能从 {S.j} 跳到 {S.i}' if abs(S.nums[S.i] - S.nums[S.j]) <= S.target
             else f'`|{S.nums[S.i]} − {S.nums[S.j]}| = {abs(S.nums[S.i] - S.nums[S.j])} > {S.target}`：差太大，跳不了')),
        'f[i] = max': '`f[{i}] = max({B.f[i]}, f[{j}] + 1)` = =={f[i]}==：多一个中转点就多跳一次，要的是最大',
        'return f[-1]': '`f[-1] = {f[-1]}`：最后一个位置最多跳 =={f[-1]}== 次（`-1` 表示到不了）',
    },
    cards=dict(
        one_liner='f[i] 表示跳到 i 的最大次数，-1 表示到不了',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['从下标 `0` 出发，每次只能向右跳到 `j`，要求 `|nums[j] − nums[i]| <= target`',
                 '求到达最后一个下标的==最大==跳跃次数，到不了返回 `-1`',
                 '示例：`nums = [1,3,6,4,1,2]`，`target = 2` → `3`'],
        quote='令f[i]表示跳到位置i时的最大跳跃次数，那么对于f[i]，首先初始化f[i] = -1，表示无法到达。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` 先设成 `-1`，再从 `0..i-1` 枚举上一跳的终点 `j`',
              '`j` 自己能到达，且 `abs(nums[i] - nums[j]) <= target`，就可以 `f[i] = max(f[i], f[j] + 1)`',
              '全部算完，`f[-1]` 就是答案'],
        summary=['时间 `O(n^2)`，空间 `O(n)`，`n <= 1000` 刚好够用',
                 '必须判断 `f[j] != -1`：到不了的位置不能当中转，否则会把 `-1 + 1 = 0` 当成可达',
                 '要求的是最大次数，所以用 `max`，不是最短路',
                 '原文本身是 Python 3 可运行的写法，代码未做修改',
                 '对比灵神：灵神把 `-inf` 当不可达，并给出线段树优化到 `O(n log n)`'],
    ),
)
