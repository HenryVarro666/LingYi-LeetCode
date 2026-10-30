A0 = [1, 3, 1, 2, 3]
B0 = [3, 1, 1, 2, 3]


def _col(S, r, c, v):
    i = S.get('i')
    if i is None or S.get('_line') not in (6, 7):
        return None
    cur = 0 if S['_line'] == 6 else 1
    if (r, c) == (i + 2, cur):
        return 'yellow'
    if (r, c) == (i + 1, cur):
        return 'green'
    if (r, c) == (i, cur ^ 1):
        return 'blue'
    return None


def _txt(S):
    i = S.get('i')
    if i is None:
        return '`f[i+2][0]`：最后喝 A；`f[i+2][1]`：最后喝 B（黄 = 正在算，绿 = 接着喝同一种，蓝 = 隔一小时换过来）'
    if S.get('_line') not in (6, 7):
        return f'第 `{i}` 小时：A 给 `{S["x"]}`，B 给 `{S["y"]}`'
    j = 0 if S['_line'] == 6 else 1
    c = S['x'] if j == 0 else S['y']
    return f'`f[{i+2}][{j}] = max(f[{i+1}][{j}], f[{i}][{1-j}]) + {c}` = =={S["f"][i+2][j]}=='


CONFIG = dict(
    num=3259, title='超级饮料的最大强化能量', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP（1:1 翻译成递推）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1484'],
    code='''
class Solution:
    def maxEnergyBoost(self, a: List[int], b: List[int]) -> int:
        n = len(a)
        f = [[0, 0] for _ in range(n + 2)]
        for i, (x, y) in enumerate(zip(a, b)):
            f[i + 2][0] = max(f[i + 1][0], f[i][1]) + x
            f[i + 2][1] = max(f[i + 1][1], f[i][0]) + y
        return max(f[-1])
''',
    call=f'Solution().maxEnergyBoost({A0}, {B0})',
    expect=10,
    views=[
        dict(type='array', var='a', label='a（A 饮料）', h=150, cell=80,
             color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='array', var='b', label='b（B 饮料）', h=150, cell=80,
             color=lambda S, i, v: 'pink' if S.get('i') == i else None),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='table', var='f', label='f 表（左 A 右 B）', h=420, cell=60,
             rows=lambda S: ['空', '空'] + [f'第{k}时' for k in range(len(S['a']))], cols=['A', 'B'],
             color=_col),
    ],
    watch=[('i', 'i', 'blue'), 'x', 'y'],
    captions={
        'n = len(a)': '`n = {n}`',
        'f = [[0, 0]': '`f[i+2][j]` 对应 `dfs(i, j)`；前两行是边界（还没喝），值为 0',
        'for i, (x, y)': lambda S, B, r: (f"第 `{S['i']}` 小时：A 能给 `{S['x']}`，B 能给 `{S['y']}`" if S.get('i') != B.get('i') or 'i' not in B else '所有小时都算完了'),
        'f[i + 2][0] =': '最后喝 A：接着喝 A（`f[{i+1}][0] = {f[i+1][0]}`）或前一小时空着、换自 B（`f[{i}][1] = {f[i][1]}`），取大再加 `{x}` = =={f[i+2][0]}==',
        'f[i + 2][1] =': '最后喝 B：接着喝 B（`f[{i+1}][1] = {f[i+1][1]}`）或前一小时空着、换自 A（`f[{i}][0] = {f[i][0]}`），取大再加 `{y}` = =={f[i+2][1]}==',
        'return max': '最后一小时喝 A 还是 B 取大：`max({f[-1]})` = =={ret}==',
    },
    cards=dict(
        one_liner='当前小时一定喝，换饮料就跳过上一小时',
        complexity='时间 `O(n)`，空间 `O(n)`（可滚动成 `O(1)`）',
        problem=['两个数组 `a`、`b` 是 A、B 饮料每小时的能量，每小时喝一种',
                 '从一种换到另一种，要空等一小时，那一小时没有能量',
                 '示例：`a=[1,3,1], b=[3,1,1]` → `5`；`a=[4,1,1], b=[1,1,3]` → `7`'],
        quote='如果当前选了 a 中的元素，接下来要么继续选 a 中的元素，要么不继续选 a 中的元素，也就是选 b 中的元素。',
        quote_src='—— 灵茶山艾府题解（「选或不选」思考方式）',
        idea=['状态 `dfs(i, j)`：从下标 `[0,i]` 里选，最后选的是 `c[j][i]` 时的最大和',
              '继续选同一个数组 → `dfs(i-1, j)`；换到另一个数组 → 跳过 `i-1`，即 `dfs(i-2, j^1)`',
              '记忆化搜索 1:1 翻译成递推，`f[i+2][j]` 的 `+2` 是为了放下 `dfs(-2)`、`dfs(-1)` 两个边界'],
        summary=['时间 `O(n)`，空间 `O(n)`；用滚动变量可降到 `O(1)`',
                 '易错：`f` 下标整体 `+2`，答案取 `max(f[-1])`',
                 '题解还给出了记忆化搜索写法（`@cache`），这里演示递推',
                 '同类：198 打家劫舍'],
    ),
)
