def _if(S, B, ret):
    j, nums, on = S.j, S.nums, B.on_path
    if on[j]:
        return f'`nums[{j}] = {nums[j]}` ==已填入排列== → continue'
    if j > 0 and nums[j] == nums[j - 1] and not on[j - 1]:
        return (f'`nums[{j}] = nums[{j - 1}] = {nums[j]}`，且 `nums[{j - 1}]` ==没填入排列== → continue，'
                f'否则会和填 `nums[{j - 1}]` 的分支重复')
    if j > 0 and nums[j] == nums[j - 1]:
        return f'`nums[{j}] = nums[{j - 1}]`，但 `nums[{j - 1}]` 已填 → 它是剩余数中第一个 `{nums[j]}`，可以填'
    return f'`nums[{j}] = {nums[j]}` 没填过，也不和前一个数重复 → 可以填入 `path[{S.i}]`'


_J = lambda S: S['_inner'].get('j')  # 只看最内层的 j（刚进入下一层时还没有 j）


CONFIG = dict(
    num=47, title='全排列 II', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='排序 + 排列型回溯（相同数按顺序填）',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        nums.sort()

        n = len(nums)
        path = [0] * n  # 所有排列的长度都是 n
        on_path = [False] * n  # on_path[j] 表示 nums[j] 是否已经填入排列
        ans = []

        # i 表示当前要填排列的第几个数
        def dfs(i: int) -> None:
            if i == n:  # 填完了
                ans.append(path.copy())  # 也可以写 path[:]
                return

            # 枚举 nums[j] 填入 path[i]
            for j, on in enumerate(on_path):
                # 如果 nums[j] 已填入排列，continue
                # 如果 nums[j] 和前一个数 nums[j-1] 相等，且 nums[j-1] 没填入排列，continue
                if on or j > 0 and nums[j] == nums[j - 1] and not on_path[j - 1]:
                    continue
                path[i] = nums[j]  # 填入排列
                on_path[j] = True  # nums[j] 已填入排列（注意标记的是下标，不是值）
                dfs(i + 1)  # 填排列的下一个数
                on_path[j] = False  # 恢复现场
                # 注意 path 无需恢复现场，因为排列长度固定，直接覆盖 path[i] 就行

        dfs(0)
        return ans
''',
    call='Solution().permuteUnique([1, 2, 1])',
    expect=[[1, 1, 2], [1, 2, 1], [2, 1, 1]],
    views=[
        dict(type='array', var='nums', label='nums（排序后；绿 = 已填入排列）', cell=64, h=150, pointers={_J: 'pink'}, pointer_labels={_J: 'j'},
             color=lambda S, i, v: 'green' if S['on_path'][i] else None),
        dict(type='array', var='path', label='path（暗 = 还没填 / 旧值）', cell=64, h=150, pointers={'i': 'blue'},
             dim=lambda S, i, v: i >= S['i'] and not (i == S['i'] and 'j' in S and S['on_path'][S['j']] and S['path'][i] == S['nums'][S['j']])),
        dict(type='calls', h=190),
        dict(type='stack', var='ans', label='ans', h=108),
    ],
    watch=[('i', 'i', 'blue'), ('j', _J, 'pink'), 'on_path'],
    skip=['for j, on in enumerate', '                    continue', 'n = len(nums)', 'ans = []'],
    captions={
        'nums.sort()': '先排序：==相同的数挨在一起==，才能用 `nums[j] == nums[j-1]` 判断重复 → `{nums}`',
        'path = [0] * n': '`path` 长度固定为 `n`，填的时候直接覆盖',
        'on_path = [False] * n': '`on_path[j]` 标记的是==下标== j 是否已填入（两个 1 要区分开）',
        'dfs(0)': '从 `dfs(0)` 开始：先决定 `path[0]` 填什么',
        'if i == n': lambda S, B, ret: ('`i == n` → ==填完了==，得到一个排列' if S.i == S.n
                                        else f'`i = {S.i} < n`：枚举 `nums[j]` 填入 `path[{S.i}]`'),
        'if on or j > 0': _if,
        'path[i] = nums[j]': '填入排列：`path[{i}] = nums[{j}] = {nums[j]}`',
        'on_path[j] = True': '`on_path[{j}] = True`：下标 {j} 已用，下面几层不能再选它',
        'dfs(i + 1)': '递归 `dfs({i})`：填排列的下一个数',
        'ans.append': lambda S, B, ret: f'记录答案 `{S.ans[-1]}`（==复制== path，否则之后会被覆盖）',
        '                return': '这条分支到底了 → 回到上一层',
        'on_path[j] = False': '恢复现场：`on_path[{j}] = False`；path 不用恢复，下次直接覆盖',
        'return ans': '枚举结束：共 `{len(ret)}` 个==不重复==的排列',
    },
    max_steps=60,
    cards=dict(
        one_liner='排序后规定：相同的数只能按下标顺序填入排列',
        complexity='时间 `O(n·n!)`，空间 `O(n)`（不计返回值）',
        problem=['给定一个==可包含重复数字==的序列 `nums`，按任意顺序返回所有==不重复==的全排列',
                 '示例：`[1,1,2]` → `[[1,1,2],[1,2,1],[2,1,1]]`',
                 '本视频：`[1,2,1]`（排序后就是 `[1,1,2]`）'],
        quote='如果 `nums[i] = nums[i-1]`，且 `nums[i-1]` 没有填入排列，为了避免生成重复的排列，==绝对不能填 nums[i]==，直接 continue。',
        quote_src='—— 灵茶山艾府题解',
        idea=['重复来自：两个 1 交换填的位置，得到同一个排列',
              '排序后，相同的数里==只有“剩余的第一个”能填==当前位置',
              '其余写法和 46 题完全一样：`on_path` 标记 + 恢复现场'],
        result='3 个不重复的排列全部找到 ✓',
        summary=['时间 `O(n·n!)`，空间 `O(n)`；返回值不计入',
                 '必须先 `sort`：相同的数相邻，才能和 `nums[j-1]` 比较',
                 '`on_path` 标记==下标==而不是值，两个相等的数要区分',
                 '判断顺序：`on` 或（等于前一个 且 前一个没填）→ continue',
                 '同类题：40. 组合总和 II、90. 子集 II（有重复元素的回溯）'],
    ),
)
