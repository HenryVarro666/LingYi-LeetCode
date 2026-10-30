_J = lambda S: (S['_inner']['j'] - 1) if 'j' in S['_inner'] else None


CONFIG = dict(
    num='LCR 080', title='组合', difficulty='Medium', category='二叉树与回溯',
    author='灵茶山艾府', technique='回溯：枚举下一个数选哪个（倒着选 + 剪枝）',
    tags=[],
    code='''
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        ans = []
        path = []
        def dfs(i: int) -> None:
            d = k - len(path)  # 还要选 d 个数
            if d == 0:
                ans.append(path.copy())
                return
            for j in range(i, d - 1, -1):
                path.append(j)
                dfs(j - 1)
                path.pop()
        dfs(n)
        return ans
''',
    call='Solution().combine(4, 2)',
    expect=[[4, 3], [4, 2], [4, 1], [3, 2], [3, 1], [2, 1]],
    views=[
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='1 ~ n（j = 当前枚举的数）', cell=64, h=130,
             pointers={_J: 'pink'}, pointer_labels={_J: 'j'}),
        dict(type='stack', var='path', label='path（已选的数）', h=100),
        dict(type='calls', h=170),
        dict(type='stack', var='ans', label='ans', h=130),
    ],
    watch=[('i', 'i', 'blue'), ('d', lambda S: S['_inner'].get('d'), 'yellow'), ('j', lambda S: S['_inner'].get('j'), 'pink'), 'path'],
    skip=['ans = []', 'path = []'],
    captions={
        'd = k': '已选 `{len(path)}` 个，还要选 `d = {k} - {len(path)} = =={d}==` 个',
        'if d == 0': lambda S, B, ret: ('`d == 0`：==凑够 k 个== → 记录答案' if S['d'] == 0 else f'`d = {S["d"]} > 0`：还没选够，继续枚举'),
        'ans.append': '复制 `path = {path}` 加入答案（共 `{len(ans)}` 个）',
        'for j in range': '枚举下一个数 `j`，范围 `{i}` 到 `{d}`；==j < d 时剩下的数不够选，所以到 d 为止==',
        'path.append': '选 `{j}` → `path = {path}`',
        'dfs(j - 1)': '递归 `dfs({j - 1})`：下一个数只能比 j ==小==，保证组合不重复',
        'path.pop': '恢复现场：弹出 `{B.path[-1]}`',
        'dfs(n)': '从 `dfs({n})` 开始：第一个数从 n 往下选',
        'return ans': '共 `{len(ret)}` 个组合 = `C(4,2)`',
    },
    max_steps=90,
    cards=dict(
        one_liner='倒着选：还要选 d 个，下一个数至少是 d，否则凑不够',
        complexity='时间 `O(k·C(n,k))`，空间 `O(k)`',
        problem=['给定 `n` 和 `k`，返回 `1 ... n` 中所有 `k` 个数的组合',
                 '示例：`n = 4, k = 2` → `[[2,4],[3,4],[2,3],[1,2],[1,3],[1,4]]`',
                 '顺序任意'],
        quote='分析回溯问题的时间复杂度，有一个通用公式：路径长度 × 搜索树的叶子数。对于本题，它等于 O(k·C(n,k))。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`d = k - len(path)` 表示还要选几个数',
              '枚举 `j` 从 `i` 到 `d`：比 d 小的数不够选满，不必枚举（剪枝）',
              '选了 `j` 就递归 `j - 1`，保证组合里的数递减、不重复'],
        summary=['时间 `O(k·C(n,k))`：叶子数 × 路径长度；空间 `O(k)`',
                 '易错点：`range(i, d - 1, -1)` 的终点是 `d - 1`，包含 d',
                 '易错点：加入答案要 `path.copy()`',
                 '题解方法二是选或不选：不选 `i` 要求 `i > d`，思路相同'],
    ),
)
