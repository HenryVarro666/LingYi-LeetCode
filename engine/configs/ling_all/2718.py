Q0 = [[0, 0, 1], [1, 2, 2], [0, 0, 3], [1, 0, 4]]


def _mat(S):
    n = S['n']
    return [[0] * n for _ in range(n)]


def _cell(S, i, j, v):
    if 'vis' not in S:
        return None
    r = i in S['vis'][0]
    c = j in S['vis'][1]
    if r and c:
        return 'purple'
    if r:
        return 'blue'
    if c:
        return 'pink'
    return None


def _fn(S):
    if 'vis' not in S:
        return '倒序处理：越靠后的操作越优先，被覆盖的格子不再计入'
    return f"已定行 `{sorted(S['vis'][0])}`，已定列 `{sorted(S['vis'][1])}`，当前答案 =={S.get('ans', 0)}=="


CONFIG = dict(
    num=2718, title='查询后矩阵的和', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='倒序处理 · 正难则反',
    tags=['灵神题单·贪心与思维', '难度分 1769'],
    code='''
class Solution:
    def matrixSumQueries(self, n: int, queries: List[List[int]]) -> int:
        ans = 0
        vis = [set(), set()]
        for type, index, val in reversed(queries):
            if index not in vis[type]:  # 后面（>i）没有对这一行/列的操作
                # 这一行/列还剩下 n-len(vis[type^1]) 个可以填入的格子
                ans += (n - len(vis[type ^ 1])) * val
                vis[type].add(index)  # 标记操作过
        return ans
''',
    call=f'Solution().matrixSumQueries(3, {Q0})',
    expect=22,
    views=[
        dict(type='table', var=_mat, label='3×3 矩阵（蓝 = 已被后面的行操作定下，粉 = 已被列操作定下，紫 = 两者交叉）', h=300, cell=80,
             values=False, color=_cell),
        dict(type='text', fn=_fn, size=24, h=60),
        dict(type='set', var='vis[0]', label='vis[0]：已操作的行', h=130),
        dict(type='set', var='vis[1]', label='vis[1]：已操作的列', h=130),
    ],
    watch=['type', 'index', 'val', ('ans', 'ans', 'green')],
    captions={
        'vis = [set(), set()]': '`vis[0]` 记被操作过的行号，`vis[1]` 记被操作过的列号',
        'for type, index, val': '==倒序==取一个操作：`type={type}`（' + '0 行 / 1 列），`index={index}`，`val={val}`',
        'if index not in': lambda S, B, r: (f'这' + ('行' if S.type == 0 else '列') + f' `{S.index}` 在后面' + ('已经操作过 → 本次会被完全覆盖，跳过' if S.index in S.vis[S.type] else '没有操作过 → 本次值会留下来')),
        'ans += (n': '这{"行" if type == 0 else "列"}还剩 `n - len(vis[type^1])` = `{n} - {len(vis[type ^ 1])}` = {n - len(vis[type ^ 1])} 个格子可填，贡献 `{n - len(vis[type ^ 1])} × {val}` → ans = =={ans}==',
        'vis[type].add': '标记：这{"行" if type == 0 else "列"}已定，更早的操作对它都不再有效',
        'return ans': '所有操作处理完，矩阵和 = =={ret}==',
    },
    cards=dict(
        one_liner='倒着看：最后一次覆盖才算数，格子数用另一类的已标记数扣掉',
        complexity='时间 `O(q)`，空间 `O(min(q, n))`',
        problem=['`n×n` 全 0 矩阵，每个查询把某一行或某一列整体改成 `val`',
                 '依次执行所有查询，返回最终矩阵所有数之和',
                 '示例：`n=3`，`[[0,0,1],[1,2,2],[0,2,3],[1,0,4]]` → `23`',
                 '本视频：`[[0,0,1],[1,2,2],[0,0,3],[1,0,4]]` → `22`（第 0 行被操作了两次）'],
        quote='如果对同一行反复操作，那么只有最后一次对这行的操作会计入答案。列同理。……正难则反，倒序操作 queries。',
        quote_src='—— 灵茶山艾府题解',
        idea=['倒序遍历：这一行/列之前（后面）没操作过，才有贡献',
              '它还能填的格子 = `n - len(另一类已操作数)`，其余格子被后面的操作覆盖了',
              '用长为 2 的数组 `vis` 统一处理行和列，写法更简洁'],
        summary=['时间 `O(q)`，与 `n` 无关；空间 `O(min(q, n))`',
                 '易错：必须倒序；重复操作的行/列要跳过，且不能再加入 `vis`',
                 '剩余格子数用的是==另一类==的 `vis`：`vis[type^1]`',
                 '相似题：2382. 删除操作后的最大子段和（同样逆向思维）'],
    ),
)
