CONFIG = dict(
    num=3347, title='执行操作后元素的最高频率 II', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='同向三指针 + 同向双指针', tags=['三指针', '难度分 2156'],
    code='''
class Solution:
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        nums.sort()

        n = len(nums)
        ans = cnt = left = right = left2 = 0
        for i, x in enumerate(nums):
            while nums[left2] < x - k * 2:
                left2 += 1
            ans = max(ans, min(i - left2 + 1, numOperations))

            cnt += 1
            # 循环直到连续相同段的末尾，这样可以统计出 x 的出现次数
            if i < n - 1 and x == nums[i + 1]:
                continue
            while nums[left] < x - k:
                left += 1
            while right < n and nums[right] <= x + k:
                right += 1
            ans = max(ans, min(right - left, cnt + numOperations))
            cnt = 0

        return ans
''',
    call='Solution().maxFrequency([1,2,4,4,7], 2, 2)',
    expect=3,
    max_steps=110, skip=[5, 21],
    views=[
        dict(type='text', size=28, fn=lambda S: (f"x=`{S['x']}`：[x−k, x+k] = `[{S['x'] - S['k']}, {S['x'] + S['k']}]` 内有 `right − left = {S['right'] - S['left']}` 个数" if 'x' in S and 'right' in S and 16 <= S['_line'] <= 21 else (f"x=`{S['x']}`：[x−2k, x] = `[{S['x'] - 2 * S['k']}, {S['x']}]` 内 `{S['i'] - S['left2'] + 1}` 个数能变成同一个数" if 'x' in S and 8 <= S['_line'] <= 10 else f"k=`{S['k']}`，操作数 `{S['numOperations']}`：每个数能变成 [x−k, x+k] 里的任意整数"))),
        dict(type='array', var='nums', h=330, pointers={'left': 'blue', 'right - 1': 'pink', 'left2': 'cyan', 'i': 'green'},
             pointer_labels={'right - 1': 'right-1'},
             window=('left', 'right - 1'),
             color=lambda S, idx, v: ('green' if 'i' in S and idx == S['i'] else None)),
    ],
    watch=[('i', 'i', 'green'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('left2', 'left2', 'cyan'), ('cnt', 'cnt', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '先排序：这样“能变成 x 的数”是一段连续区间',
        'ans = cnt = left': '`ans`、`cnt`（x 的出现次数）和三个左右指针都从 0 开始',
        'for i, x in enumerate': '枚举 `x = nums[{i}] = {x}`',
        'while nums[left2] < x - k * 2': lambda S, B, r: (f'`nums[left2] = {S.nums[S.left2]} < x - 2k = {S.x - 2 * S.k}`：离 x 太远，不可能和 x 变成同一个数 → left2 右移' if S.nums[S.left2] < S.x - S.k * 2 else f'`nums[left2] = {S.nums[S.left2]} >= {S.x - 2 * S.k}`，left2 停下'),
        'left2 += 1': '`left2` → {left2}',
        'ans = max(ans, min(i - left2': '`[left2, i]` 有 `{i - left2 + 1}` 个数能一起变成 `x-k`（变成不在 nums 里的数）：最多改 `{numOperations}` 个 → `ans` = =={ans}==',
        'cnt += 1': '`x` 的出现次数 `cnt` → {cnt}',
        'if i < n - 1 and x == nums[i + 1]': lambda S, B, r: ('下一个还是 x → 继续数，等到相同段末尾再算' if S.i < S.n - 1 and S.x == S.nums[S.i + 1] else '`x` 的相同段到头了，开始算以 x 为目标的最高频率'),
        'continue': '跳到下一个下标继续数 `cnt`',
        'while nums[left] < x - k': lambda S, B, r: (f'`nums[left] = {S.nums[S.left]} < x - k = {S.x - S.k}`：变不成 x → left 右移' if S.nums[S.left] < S.x - S.k else f'`nums[left] = {S.nums[S.left]} >= {S.x - S.k}`：left 停在能变成 x 的最左元素'),
        'left += 1': '`left` → {left}',
        'while right < n and nums[right] <= x + k': lambda S, B, r: (f'`nums[right] = {S.nums[S.right]} <= x + k = {S.x + S.k}`：能变成 x → right 右移' if S.right < S.n and S.nums[S.right] <= S.x + S.k else f'`right = {S.right}`：到头或 `nums[right] > x + k`，区间是 `[left, right)`'),
        'right += 1': '`right` → {right}',
        'ans = max(ans, min(right - left, cnt': '能变成 x 的有 `{right - left}` 个，其中 `{cnt}` 个本来就是 x，其余最多改 `{numOperations}` 个 → `min({right - left}, {cnt} + {numOperations}) = {min(right - left, cnt + numOperations)}`，`ans` = =={ans}==',
        'cnt = 0': '这个 x 算完，`cnt` 清零',
        'return ans': '最高频率 `{ans}`',
    },
    cards=dict(
        one_liner='排序后，能变成同一个数的元素是一段连续区间',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每次操作选一个没选过的下标，把它加上 `[-k, k]` 内一个整数，共 `numOperations` 次',
                 '求操作后出现次数最多的元素的频率',
                 '本视频：`[1,2,4,4,7]`，`k=2`，`numOperations=2` → `3`'],
        quote='同向三指针没有考虑「变成不在 nums 中的数」这种情况。然而，不在 nums 中的数太多了！怎么减少计算量？',
        quote_src='—— 灵茶山艾府题解',
        idea=['三指针：x 在 nums 中时，`[left, right)` 是能变成 x 的元素，答案 `min(right-left, cnt+numOperations)`',
              '双指针：变成不在 nums 的数 y，只需考虑 `y+k` 在 nums 中，窗口 `[x-2k, x]`',
              '这种情况最多改 `numOperations` 个，所以和它取最小值'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '统计 x 的出现次数要走到相同段末尾，所以有 `continue`',
                 '目标是 x 时，x 自己不用操作：`cnt + numOperations`',
                 '灵神还给了差分写法（方法一）和两个 for 分开写的版本',
                 '这里选的是把两个循环合并的写法'],
    ),
)
