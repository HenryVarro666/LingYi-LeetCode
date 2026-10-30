def _prune_text(S):
    inner = S.get('_inner', {})
    if 'i' not in inner or 'path' not in S:
        return '倒着枚举：`dfs(i, left_sum)` 表示还能从 `1..i` 里选，还差 `left_sum`'
    i, d, ls = inner['i'], S['k'] - len(S['path']), inner['left_sum']
    mx = (i * 2 - d + 1) * d // 2
    top = ' + '.join(str(i - t) for t in range(d)) if d else '0'
    return f'从 `1..{i}` 再选 `d = {d}` 个，最大和 `{top} = {mx}`，还差 `left_sum = {ls}`'


def _prune(S, B, ret):
    i, d, ls = S.i, S.d, S.left_sum
    mx = (i * 2 - d + 1) * d // 2
    if ls < 0:
        return f'`d = {d}`，`left_sum = {ls} < 0`：选多了 → ==剪枝，返回=='
    if ls > mx:
        return f'`left_sum = {ls}` > 从 `1..{i}` 选 `{d}` 个的最大和 `{mx}`，凑不够 → ==剪枝，返回=='
    return f'还要选 `d = {d}` 个：`0 ≤ left_sum = {ls} ≤ {mx}`，还有希望，继续'


def _digit_color(S, idx, v):
    path = S.get('path') or []
    if v in path:
        return 'green'
    inner = S.get('_inner', {})
    if 'i' in inner and v > inner['i']:
        return None
    return None


def _digit_dim(S, idx, v):
    inner = S.get('_inner', {})
    path = S.get('path') or []
    return 'i' in inner and v > inner['i'] and v not in path


_I = lambda S: S['_inner']['i'] - 1 if 'i' in S.get('_inner', {}) and S['_inner']['i'] >= 1 else None


CONFIG = dict(
    num=216, title='组合总和 III', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='组合型回溯 · 倒序枚举 + 上下界剪枝',
    tags=['labuladong', '灵神核心路线'],
    code='''
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        ans = []
        path = []

        def dfs(i: int, left_sum: int) -> None:
            d = k - len(path)  # 还要选 d 个数
            if left_sum < 0 or left_sum > (i * 2 - d + 1) * d // 2:  # 剪枝
                return
            if d == 0:  # 找到一个合法组合
                ans.append(path.copy())
                return
            # 枚举的数不能太小，否则后面没有数可以选
            for j in range(i, d - 1, -1):
                path.append(j)
                dfs(j - 1, left_sum - j)
                path.pop()  # 恢复现场

        dfs(9, n)  # 从 i=9 开始倒着枚举
        return ans
''',
    call='Solution().combinationSum3(2, 16)',
    expect=[[9, 7]],
    views=[
        dict(type='text', fn=_prune_text, h=60, size=24),
        dict(type='array', var=lambda S: list(range(1, 10)), label='数字 1..9（暗 = 大于 i，不能再选；绿 = 已在 path 中）',
             cell=80, index=False, color=_digit_color, dim=_digit_dim, h=150,
             pointers={_I: 'blue'},
             pointer_labels={_I: 'i'}),
        dict(type='array', var='path', label='path（已选的数，从大到小）', cell=80, h=140),
        dict(type='calls', h=230),
        dict(type='stack', var='ans', label='ans', h=100),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('left_sum', lambda S: S['_inner'].get('left_sum'), 'pink'),
           ('d', lambda S: S['k'] - len(S['path']) if 'path' in S else None, 'yellow')],
    skip=['ans = []', 'path = []', 'd = k - len(path)', '                return'],
    captions={
        'd = k - len(path)': '还要选 `d = {k} - {len(path)} = {d}` 个数',
        'if left_sum < 0 or': _prune,
        '                return': lambda S, B, ret: ('剪掉这棵子树，回到上一层' if B.d else '记录完毕，回到上一层'),
        'if d == 0': lambda S, B, ret: ('`d == 0` 且没被剪枝（`0 ≤ left_sum ≤ 0`）→ ==找到一个合法组合==' if S.d == 0
                                        else f'`d = {S.d}`，还没选够'),
        'ans.append(path.copy())': '记录答案 `{ans[-1]}`（要复制 path）',
        'for j in range(i, d - 1, -1)': lambda S, B, ret: (
            f'枚举这一个数选 `j = {S.j}`（`j` 至少是 `d = {S.d}`，否则后面不够选）' if S.get('j') is not None and S.j != B.get('j')
            else f'`j` 已经枚举到 `d = {S.d}`，这一层结束'),
        'path.append(j)': '选 `{j}`：`path = {path}`',
        'dfs(j - 1, left_sum - j)': lambda S, B, ret: f'递归 `dfs({B.j - 1}, {B.left_sum} - {B.j} = {B.left_sum - B.j})`：下一个数只能更小',
        'path.pop()': '恢复现场：弹出 `{B.path[-1]}`，试下一个更小的 `j`',
        'dfs(9, n)': '从 `i = 9` 开始==倒着枚举==：`dfs(9, {n})`',
        'return ans': '搜索结束，返回 `{ret}`',
    },
    max_steps=54,
    cards=dict(
        one_liner='倒着枚举选哪个数，用剩余和的上下界剪枝',
        complexity='时间 `O(k·C(9,k))`，空间 `O(k)`',
        problem=['从 `1..9` 中选 `k` 个==不同==的数，使它们的和为 `n`，返回所有组合',
                 '示例：`k = 3, n = 9` → `[[1,2,6],[1,3,5],[2,3,4]]`',
                 '本视频：`k = 2, n = 16` → `[[9,7]]`（倒序枚举，组合内从大到小）'],
        quote='这题如果改成求方案个数（而不是具体方案），就是==恰好装满型 0-1 背包==。为方便大家与后续 DP 课程内容直接对应上，我们倒着枚举。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, left_sum)`：从 `1..i` 里再选 `d` 个数，凑出 `left_sum`',
              '剪枝一：`left_sum < 0`，选多了；剪枝二：`left_sum` 比 `i, i-1, …, i-d+1` 之和还大',
              '那 `d` 个最大数之和是等差数列：`(i + i-d+1)·d / 2`'],
        summary=['时间 `O(k·C(9,k))`：路径长 `k` × 叶子数 `C(9,k)`；空间 `O(k)`',
                 '`for j in range(i, d - 1, -1)`：`j` 不能小于 `d`，否则剩下的数不够选',
                 '`ans.append(path.copy())`，不能直接放 `path`',
                 '题解还给了「选或不选」写法：不选 `i` 时要求 `i > d`，剪枝条件相同',
                 '去掉和的限制就是 77. 组合；求方案数就是 0-1 背包'],
    ),
)
