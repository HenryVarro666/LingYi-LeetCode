CONFIG = dict(
    num=46, title='全排列', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='排列型回溯（on_path 标记）',
    code='''
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        path = [0] * n  # 所有排列的长度都是一样的 n
        on_path = [False] * n
        ans = []

        # 枚举 path[i] 填 nums 的哪个数
        def dfs(i: int) -> None:
            if i == n:
                ans.append(path.copy())  # 也可以写 path[:]
                return
            for j, on in enumerate(on_path):
                if not on:
                    path[i] = nums[j]  # 从没有选的数字中选一个
                    on_path[j] = True  # 已选上
                    dfs(i + 1)
                    on_path[j] = False  # 恢复现场
                    # 注意 path 无需恢复现场，因为排列长度固定，直接覆盖就行

        dfs(0)
        return ans
''',
    call='Solution().permute([1, 2, 3])',
    expect=[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
    views=[
        dict(type='array', var='nums', label='nums（绿 = 已在 path 上）', cell=64, h=150, pointers={'j': 'pink'},
             color=lambda S, i, v: 'green' if S['on_path'][i] else None),
        dict(type='array', var='path', label='path（暗 = 旧值）', cell=64, h=150, pointers={'i': 'blue'},
             dim=lambda S, i, v: i > S['i'] or (i == S['i'] and S['path'][i] != S['nums'][S['j']])),
        dict(type='calls', h=218),
        dict(type='stack', var='ans', label='ans', h=108),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'on_path'],
    skip=['for j, on in enumerate'],
    captions={
        'dfs(0)': '从 `dfs(0)` 开始：先决定 `path[0]` 填哪个数',
        'if i == n': lambda S, B, ret: (f'`i == n`（{S.i} == {S.n}）→ ==成立==：path 填满了，得到一个排列'
                                        if S.i == S.n else
                                        f'`i = {S.i} < n`：还没填满，枚举 `path[{S.i}]` 填哪个数'),
        'if not on': lambda S, B, ret: (f'`nums[{S.j}] = {S.nums[S.j]}` 还没用过 → 可以填进 `path[{S.i}]`'
                                        if not S.on else
                                        f'`nums[{S.j}] = {S.nums[S.j]}` ==已在 path 上== → 跳过'),
        'path[i] = nums[j]': '从没有选的数字中选一个：`path[{i}] = {nums[j]}`，直接覆盖旧值',
        'on_path[j] = True': '已选上：`on_path[{j}] = True`，下面几层不能再选 `{nums[j]}`',
        'dfs(i + 1)': '递归 `dfs({i})`：`path[{i - 1}]` 定好了，去填下一个位置 `path[{i}]`',
        'ans.append': lambda S, B, ret: (
            f'记录答案 `{S.ans[-1]}`：==必须 copy==，否则 path 之后被覆盖，ans 里的也会变'
            if len(S.ans) == 1 else f'记录答案 `{S.ans[-1]}`（复制一份 path）'),
        '                return': '这条分支到底了 → 返回上一层，换下一个数试试',
        'on_path[j] = False': lambda S, B, ret: (
            f'`dfs({S.i + 1})` 返回，恢复现场：`on_path[{S.j}] = False`'
            + ('；==path 不用恢复==，下次直接覆盖' if len(S.ans) <= 1 else '')),
        'return ans': '所有分支都试完了，返回全部 `{len(ret)}` 个排列',
    },
    max_steps=56,
    cards=dict(
        one_liner='排列型回溯：每层枚举「这一位填哪个没用过的数」',
        complexity='时间 `O(n·n!)`，空间 `O(n)`（不计返回值）',
        problem=['给一个==不含重复数字==的数组 `nums`，返回它的所有全排列',
                 '示例：`[1,2,3]` → `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`'],
        quote='枚举 `path[i]` 填 `nums` 的哪个数。`on_path[j] = False` 恢复现场；==注意 path 无需恢复现场，因为排列长度固定，直接覆盖就行==。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`dfs(i)`：前 `i` 位已经填好，现在决定 `path[i]`',
              '`on_path[j]` 记录 `nums[j]` 是否已在 path 上，只从没选的数里挑',
              '`i == n` 时 path 填满 → 复制一份加入答案'],
        result='6 个排列全部找到 ✓（中间分支已快进，过程同理）',
        summary=['搜索树节点数精确值为 `e·n!` 向下取整，叶子 `n!` 个，每个复制 `O(n)` → `O(n·n!)`',
                 '易错：`ans.append(path)` 不 copy，最后 ans 里全是同一个数组',
                 '易错：`on_path[j]` 必须恢复为 `False`；path 定长可直接覆盖',
                 '另一种写法：传 `remain` 集合，`dfs(i + 1, remain - {x})`'],
    ),
)
