COST = [[1, 3, 5], [4, 1, 1], [1, 5, 3]]


def _bits(S):
    return [format(i, f'0{len(S["cost"][0])}b') for i in range(len(S['f']))]


def _phase(S):
    return 'row' in S and 'f' in S


def _fcol(S, r, c, v):
    if not _phase(S):
        if 'bit' in S and 'mask' in S and c in (S['bit'] | S['mask'], S['mask']) and S.get('_line') == 7:
            return 'yellow' if c == (S['bit'] | S['mask']) else 'blue'
        return None
    j = S.get('j')
    if j is None or S.get('_line') != 10:
        return None
    m = len(S['cost'][0])
    if c == j:
        return 'yellow'
    if c in {j & ~(1 << k) for k in range(m)}:
        return 'blue'
    return None


def _gcell(S, r, c, v):
    if _phase(S) and S.get('_line') == 10:
        return 'yellow' if S['cost'][r] is S['row'] else None
    return None


def _txt(S):
    line = S.get('_line')
    bits = lambda x: format(x, f'0{len(S["cost"][0])}b')
    if _phase(S) and line == 10 and 'j' in S:
        j, row = S['j'], S['row']
        items = ' ，'.join(f'连{k}→`{bits(j & ~(1 << k))}`+{row[k]}' for k in range(len(row)))
        return f'`f[{bits(j)}]` = min( {items} )'
    if line == 7 and 'mask' in S and 'bit' in S:
        return f'`f[{bits(S["bit"] | S["mask"])}] = f[{bits(S["mask"])}] + minCost[{S["j"]}]({S["mn"]})`'
    return '`f[j]`：第二组还没连上的点集合是 `j`（二进制第 k 位 = 点 k），最小成本'


CONFIG = dict(
    num=1595, title='连通两组点的最小成本', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状压 DP（一维滚动 + 子集递推初始化）',
    tags=['状压 DP', '其他状压 DP', '难度分 2538'],
    code='''
class Solution:
    def connectTwoGroups(self, cost: List[List[int]]) -> int:
        f = [0] * (1 << len(cost[0]))
        for j, mn in enumerate(map(min, zip(*cost))):
            bit = 1 << j
            for mask in range(bit):
                f[bit | mask] = f[mask] + mn
        for row in cost:
            for j in range(len(f) - 1, -1, -1):
                f[j] = min(f[j & ~(1 << k)] + c for k, c in enumerate(row))
        return f[-1]
''',
    call=f'Solution().connectTwoGroups({COST})',
    expect=4,
    setup='',
    views=[
        dict(type='grid', var='cost', label='cost（黄 = 当前处理的第一组点 i 这一行）', h=210, cell=60, color=_gcell),
        dict(type='table', var='[f]', label='f[j]（列名 = 集合 j 的二进制；黄 = 正在算，蓝 = 它依赖的状态）', h=230, cell=70,
             rows=lambda S: ['f'], cols=_bits, color=_fcol),
        dict(type='text', fn=_txt, size=24, h=80),
    ],
    watch=[('j', 'j', 'blue'), ('mn', 'mn', 'cyan'), ('bit', 'bit', 'pink'), ('mask', 'mask', 'yellow')],
    skip=['for j, mn in', 'for mask in', 'for row in cost', 'for j in range(len(f)'],
    captions={
        'f = [0] *': '`f[j]` 有 `2^m = {len(f)}` 项：`j` 的第 k 位为 1 表示第二组的点 k ==还没被连接==',
        'f[bit | mask] = f[mask] + mn': '`f[{bit | mask}] = f[{mask}] + {mn}`：新加的点 `{j}` 只能找一个最便宜的连 → ==初始值 = 各未连点的最小成本之和==',
        'f[j] = min(': lambda S, B, r: f'第一组的点 `{S.cost.index(S.row)}` 连第二组的哪个点？`f[{S.j}]` = 各 `f[j 去掉 k] + cost[i][k]` 的最小值 = =={S.f[S.j]}==',
        'return f[-1]': '`f[-1]` = `f[(1 << m) - 1]`：第二组全部还没连、第一组全部处理完 → =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='枚举第一组每个点连谁，第二组剩下的点各自找最便宜的连',
        complexity='时间 `O(nm·2^m)`，空间 `O(2^m)`',
        problem=['两组点，`cost[i][j]` 是第一组点 `i` 与第二组点 `j` 的连接成本，`size1 >= size2`',
                 '要求==每个点至少连一条边==，求最小总成本',
                 '示例：`[[1,3,5],[4,1,1],[1,5,3]]` → `4`'],
        quote='第一组的点全部连完后，第二组的某些点可能未被连接，这些点可以去第一组找个成本最小的点连上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「枚举选哪个」：第一组的点 `i` 连第二组的点 `k`，把 `k` 从未连集合 `j` 里去掉',
              '递归边界：第一组连完后，未连的点各取所在列最小值 `minCost`',
              '1:1 翻译成递推，再==去掉第一维==；初始值用 `f[bit|mask] = f[mask] + mn` 在 `O(2^m)` 内算出'],
        result='最小成本 4',
        summary=['时间 `O(nm·2^m)`：状态 `n·2^m`，每个状态枚举 `m` 个点',
                 '易错：`j` 要==倒序==枚举，滚动数组才不会用到本行已更新的值',
                 '易错：`j & ~(1 << k)` —— k 不在 j 中时 j 不变',
                 '`n >= m` 所以压缩第二组（点数少的一组）',
                 '题解还给了记忆化搜索和二维递推写法；同类题：1434. 每个人戴不同帽子的方案数'],
    ),
)
