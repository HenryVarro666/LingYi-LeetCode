def _cap_if(S, B, ret):
    if S.i == S.n:
        return f'`i == n`：每个数都决定完了 → 得到一个子集 `{S.path}`'
    return f'`i = {S.i}`：考虑 `nums[{S.i}] = {S.nums[S.i]}` 选还是不选'


def _cap_skip(S, B, ret):
    i, n, x = S.i, S.n, S.x
    if i < n and S.nums[i] == x:
        return f'`nums[{i}] = {x}` 和 x ==相同==：既然不选 x，后面等于 x 的也都不选 → 跳过'
    if i < n:
        return f'`nums[{i}] = {S.nums[i]}` ≠ `{x}`：跳完了，下一个要决定的是 `nums[{i}]`'
    return f'`i = {i} = n`：后面没有数了'


CONFIG = dict(
    num=90, title='子集 II', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='选或不选 · 不选时跳过所有相同的数',
    tags=['字节30天'],
    code='''
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        ans = []
        path = []

        def dfs(i: int) -> None:
            if i == n:
                ans.append(path.copy())  # 也可以写 path[:]
                return

            # 选 x
            x = nums[i]
            path.append(x)
            dfs(i + 1)
            path.pop()  # 恢复现场

            # 不选 x，那么后面所有等于 x 的数都不选
            # 如果不跳过这些数，会导致「选 x 不选 x'」和「不选 x 选 x'」这两种情况都会加到 ans 中，这就重复了
            i += 1
            while i < n and nums[i] == x:
                i += 1
            dfs(i)

        dfs(0)
        return ans
''',
    call='Solution().subsetsWithDup([2, 1, 2])',
    expect=[[1, 2, 2], [1, 2], [1], [2, 2], [2], []],
    views=[
        dict(type='array', var='nums', label='nums（排序后；i = 正在决定选不选的数）', cell=80, h=200,
             pointers={'i': 'blue'}, dim=lambda S, i, v: 'i' in S and i < S['i']),
        dict(type='stack', var='path', label='path（当前选了哪些数）', h=100),
        dict(type='calls', h=200),
        dict(type='stack', var='ans', label='ans', h=110, fmt=lambda p: str(p).replace(' ', '')),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'orange'), ('path', 'path', 'yellow'), ('len(ans)', 'len(ans)', 'green')],
    skip=['n = len(nums)', 'ans = []', 'path = []', 'x = nums[i]', 11],
    captions={
        'nums.sort()': '先排序 `[2,1,2]` → `{nums}`：==相同的数挨在一起==，方便跳过',
        'if i == n': _cap_if,
        'ans.append': '复制 path 加入答案：`{ans[-1]}`',
        'path.append(x)': '==选== `x = nums[{i}] = {x}`：path → `{path}`',
        16: '选了 `{x}` 之后，递归去决定 `nums[{i}]`',
        'path.pop()': '恢复现场：撤销选 `{B.path[-1]}`，path → `{path}`',
        21: '==不选== `x = {x}`：`i` 先移到 `{i}`，再看后面有没有和 x 相同的数',
        'while i < n and nums[i] == x': _cap_skip,
        '                i += 1': '跳过一个和 `{x}` 相同的数：`i` → {i}',
        24: lambda S, B, ret: (f'==不选== `{S.x}`（以及它后面的同值数），递归 `dfs({S.i})`' if S.i < S.n
                               else f'==不选== `{S.x}`，同值的也都跳过 → `dfs({S.i})` 直接到叶子'),
        'dfs(0)': '从 `dfs(0)` 开始：依次决定每个数选或不选',
        'return ans': '共 `{len(ret)}` 个子集，==没有重复==',
    },
    max_steps=70,
    cards=dict(
        one_liner='和 78 题一样选或不选；不选 x 时，把后面所有等于 x 的数也一起跳过',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['整数数组 `nums` ==可能包含重复元素==，返回所有可能的子集（幂集）',
                 '解集==不能包含重复的子集==',
                 '示例：`[1,2,2]` → `[[],[1],[1,2],[1,2,2],[2],[2,2]]`',
                 '本视频：`[2,1,2]`（排序后同示例）'],
        quote='在不选 nums[i] 时，要==跳过后续所有等于 nums[i] 的数==。如果不跳过这些数……「选第一个 2 不选第二个 2」和「不选第一个 2 选第二个 2」这两种情况都相当于「选了一个 2」，这就重复了。',
        quote_src='—— 灵茶山艾府题解「方法一：选或不选」',
        idea=['先排序，让相同的数挨在一起',
              '选 x：`path.append(x)` → `dfs(i + 1)` → `path.pop()` 恢复现场',
              '不选 x：`i` 跳过所有等于 x 的数，再 `dfs(i)`',
              '这样「选了几个 2」只由「从第一个 2 起连续选了几个」决定，不会重复'],
        result='6 个子集，无重复 ✓',
        summary=['时间 `O(n·2^n)`，空间 `O(n)`（递归栈 + path）',
                 '易错：忘记排序，相同的数不挨着就跳不干净',
                 '方法二「枚举选哪个」：`for j in range(i, n)`，`j > i and nums[j] == nums[j-1]` 时跳过',
                 '同类：40 组合总和 II、47 全排列 II，都是「排序 + 跳过相同」'],
    ),
)
