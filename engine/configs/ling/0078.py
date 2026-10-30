CONFIG = dict(
    num=78, title='子集', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='子集型回溯 · 选或不选（输入的视角）',
    code='''
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        ans = []
        path = []

        # 选或不选：讨论 nums[i] 是否加入 path
        def dfs(i: int) -> None:
            if i == n:  # 子集构造完毕
                ans.append(path.copy())  # 复制 path，也可以写 path[:]
                return

            # 不选 nums[i]
            dfs(i + 1)  # 考虑下一个数 nums[i+1] 选或不选

            # 选 nums[i]
            path.append(nums[i])
            dfs(i + 1)  # 考虑下一个数 nums[i+1] 选或不选
            path.pop()  # 恢复现场，撤销 path.append(nums[i])

        dfs(0)
        return ans
''',
    call='Solution().subsets([1, 2, 3])',
    expect=[[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]],
    views=[
        dict(type='array', var='nums', label='nums（指针 i = 正在讨论选不选的数）', cell=64, h=150,
             pointers={'i': 'blue'}, dim=lambda S, i, v: i < S['i']),
        dict(type='stack', var='path', label='path', h=108),
        dict(type='calls', h=218),
        dict(type='stack', var='ans', label='ans', h=108),
    ],
    watch=[('i', 'i', 'blue'), ('path', 'path', 'yellow'), ('len(ans)', 'len(ans)', 'green')],
    captions={
        14: '==不选== `nums[{B.i}] = {nums[B.i]}`：path 不变，递归 `dfs({i})` 去讨论下一个数',
        18: '==选了== `nums[{B.i}]` 之后，递归 `dfs({i})` 去讨论下一个数',
        'dfs(0)': '从 `dfs(0)` 开始：依次讨论每个 `nums[i]` 选还是不选',
        'if i == n': lambda S, B, ret: (
            f'`i == n`（{S.i} == {S.n}）→ 子集构造完毕：每个数都讨论过了'
            if S.i == S.n else
            f'`i = {S.i} < n`：讨论 `nums[{S.i}] = {S.nums[S.i]}` 选还是不选'),
        'ans.append': lambda S, B, ret: (
            f'复制 path 加入答案：`{S.ans[-1]}`' + ('（==要复制==，path 之后还会变）' if len(S.ans) == 1 else '')),
        '                return': '这是搜索树的一个叶子 → 返回上一层',
        17: '==选== `nums[{i}] = {nums[i]}`：加入 path → `{path}`',
        'path.pop()': lambda S, B, ret: (
            f'恢复现场：撤销 `path.append({B.path[-1]})`，path 回到 `{S.path}`'
            + ('；==不恢复会多出残留的数==' if len(S.ans) <= 2 else '')),
        'return ans': '每个数都选或不选过，共 `2^3 = {len(ret)}` 个子集',
    },
    max_steps=64,
    cards=dict(
        one_liner='每个数只有两种命运：选，或不选',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['数组 `nums` 的元素==互不相同==，返回它的所有子集（幂集）',
                 '示例：`[1,2,3]` → `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`'],
        quote='对于输入的 `nums`，考虑每个 `nums[i]` 是==选还是不选==，由此组合出 `2^n` 个不同的子集。`dfs` 中的 `i` 表示当前考虑到 `nums[i]` 选或不选。',
        quote_src='—— 灵茶山艾府题解「方法一：选或不选」',
        idea=['先走「不选」分支：直接 `dfs(i + 1)`',
              '再走「选」分支：`append` → `dfs(i + 1)` → `pop` 恢复现场',
              '`i == n` 是叶子：搜索树恰好 `2^n` 个叶子，每个叶子一个子集'],
        result='8 个子集全部找到 ✓（中间分支已快进）',
        summary=['`2^n` 个叶子，每个复制 path `O(n)` → `O(n·2^n)`',
                 '为什么恢复现场？不 `pop` 的话，`[1,2]` 会算出 `[2,1,2]` 这种错答案',
                 '方法二「枚举选哪个」：每个节点都是答案，`for j in range(i, n)`',
                 '方法三「二进制枚举」：`for i in range(1 << n)`，看 `i >> j & 1`'],
    ),
)
