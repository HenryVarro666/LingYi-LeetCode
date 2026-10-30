def _txt(S):
    if 'x' not in S or 'j' not in S or S.get('_line') not in (8, 9):
        return '`f[i+1]` = 只考虑 `a[0..i]` 这些不同数值时的最大总伤害；`j` = 第一个不与 `x` 冲突的位置'
    x, j, i, f, a, cnt = S['x'], S['j'], S['i'], S['f'], S['a'], S['cnt']
    if S.get('_line') == 8:
        return f'`x = {x}`：`a[j] = {a[j]}` 要 ≥ `{x}-2 = {x-2}` 才不冲突，`j` = =={j}=='
    return f'`f[{i+1}] = max(f[{i}], f[{j}] + {x}×{cnt[x]})` = =={f[i+1]}=='


CONFIG = dict(
    num=3186, title='施咒的最大总伤害', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='值域打家劫舍 + 双指针',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1841'],
    code='''
class Solution:
    def maximumTotalDamage(self, power: List[int]) -> int:
        cnt = Counter(power)
        a = sorted(cnt)
        f = [0] * (len(a) + 1)
        j = 0
        for i, x in enumerate(a):
            while a[j] < x - 2:
                j += 1
            f[i + 1] = max(f[i], f[j] + x * cnt[x])
        return f[-1]
''',
    call='Solution().maximumTotalDamage([1,1,3,4,7,6,6])',
    expect=15,
    views=[
        dict(type='map', var='cnt', label='cnt：每种伤害值出现的次数', h=100, fmt=lambda k, v: f'{k}: ×{v}'),
        dict(type='array', var='a', label='a：去重后从小到大（蓝 = i，粉 = j，j 之前的和 x 冲突）', h=200, cell=90,
             pointers={'i': 'blue', 'j': 'pink'}, window=('j', 'i'),
             dim=lambda S, i, v: S.get('j') is not None and i < S['j']),
        dict(type='array', var='f', label='f（f[i+1] 由 f[i] 和 f[j] 转移）', h=190, cell=90,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_txt, size=24, h=70),
    ],
    watch=['x', ('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'cnt = Counter': '统计每个伤害值的次数：选一个就能把同值的全选，所以按「值」做决策',
        'a = sorted(cnt)': '`a = {a}`：不同伤害值，从小到大',
        'f = [0]': '`f[0] = 0`：一个数都没得选，伤害为 0（把递归边界 `dfs(-1)` 挪到下标 0）',
        'while a[j] < x - 2': lambda S, B, r: (f'`a[{S.j}] = {S.a[S.j]}` < `{S.x}-2`，和 `x` 不冲突的数还在右边 → 继续' if S.a[S.j] < S.x - 2
                                               else f'`a[{S.j}] = {S.a[S.j]}` ≥ `{S.x}-2`：它离 `x` 太近，`j` 停在这里'),
        'j += 1': '`a[j]` 比 `x-2` 还小，肯定不冲突，`j` 右移到 {j}',
        'f[i + 1] = max': '不选 `x`：`f[{i}] = {f[i]}`；选 `x`：`f[{j}] + {x}×{cnt[x]} = {f[j] + x * cnt[x]}` → `f[{i+1}] = {f[i+1]}`',
        'return f[-1]': '全部 `a` 都考虑完：最大总伤害 = =={ret}==',
    },
    cards=dict(
        one_liner='和 740 一样是值域打家劫舍，只是不能选相差 ≤ 2 的数',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['用伤害 `power[i]` 的咒语后，不能再用伤害 `±1`、`±2` 的咒语',
                 '同伤害值可以重复使用，求总伤害最大值',
                 '示例：`[7,1,6,6]` → `13`'],
        quote='本题和 740. 删除并获得点数 几乎一样，都是在值域上的 198. 打家劫舍。……双指针最快且适用性更广（把题目的 2 改成 k 也可以过）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`Counter` 统计次数，key 排序成 `a`；选 `a[i]` 就是 `x × cnt[x]`',
              '`f[i+1] = max(f[i], f[j] + x×cnt[x])`，`j` 是第一个 `a[j] ≥ x-2` 的位置',
              '`x` 递增，`j` 只会右移，所以双指针一遍扫完'],
        after=[dict(heading='另一种写法', lines=['题解先给了记忆化搜索 `dfs(i)`', '再 1:1 翻译成递推，这里演示的是递推 + 双指针'])],
        summary=['时间 `O(n log n)`，瓶颈在排序；双指针本身 `O(n)`',
                 '`f` 左边多插一个 0，所以写成 `f[i+1]`，`a` 的下标不用改',
                 '值域大到 10^9 也不怕，只对出现过的数做 DP'],
    ),
)
