CONFIG = dict(
    num=2444, title='统计定界子数组的数目', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='分段 + 位置列表双指针', tags=['三指针', '难度分 2093'],
    code='''
class Solution(object):
    def countSubarrays(self, nums, minK, maxK):
        n = len(nums)
        left = 0
        right = 0
        res = 0
        while left < n:
            while left < n and (nums[left] < minK or nums[left] > maxK):
                left += 1

            if left == n:
                break

            right = left
            minK_list = []
            maxK_list = []
            while right < n and minK <= nums[right] <= maxK:
                if nums[right] == minK:
                    minK_list.append(right)
                if nums[right] == maxK:
                    maxK_list.append(right)
                right += 1

            minK_pos = maxK_pos = 0
            while minK_pos != len(minK_list) and maxK_pos != len(maxK_list):
                res += right - max(minK_list[minK_pos], maxK_list[maxK_pos])
                if nums[left] == minK:
                    minK_pos += 1
                if nums[left] == maxK:
                    maxK_pos += 1

                left += 1

            left = right

        return res
''',
    call='Solution().countSubarrays([1,3,5,2,7,5,1,5,4], 1, 5)',
    expect=7,
    max_steps=110, skip=[3, 5],
    views=[
        dict(type='text', size=28, fn=lambda S: (f"本段 `[{S['left']}, {S['right']})`：minK 位置 `{S['minK_list']}`，maxK 位置 `{S['maxK_list']}`" if 'minK_list' in S and 'right' in S else f"minK=`{S['minK']}`，maxK=`{S['maxK']}`：先切出全部在范围内的段")),
        dict(type='array', var='nums', h=300, pointers={'left': 'blue', 'right': 'pink'},
             color=lambda S, idx, v: ('red' if not S['minK'] <= v <= S['maxK'] else 'cyan' if v == S['minK'] else 'orange' if v == S['maxK'] else None) if 'minK' in S else None),
        dict(type='text', size=26, fn=lambda S: (f"以 left=`{S['left']}` 为左端点：右端点从 `max(minK 位置, maxK 位置)` 到 `{S['right'] - 1}`，共 `{S['right']} − max(…)` 个" if 'minK_pos' in S and 24 <= S['_line'] <= 32 else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('minK_list', 'minK_list', 'cyan'), ('maxK_list', 'maxK_list', 'orange'), ('res', 'res', 'green')],
    captions={
        'while left < n:': lambda S, B, r: (f'`left = {S.left} < {S.n}`：还有没处理的位置，开始找下一段' if S.left < S.n else '`left == n`：处理完了'),
        'while left < n and (nums[left] < minK': lambda S, B, r: (f'`nums[{S.left}] = {S.nums[S.left]}` 在 `[{S.minK}, {S.maxK}]` 外 → 不能做左端点，跳过' if S.left < S.n and (S.nums[S.left] < S.minK or S.nums[S.left] > S.maxK) else f'`left` 停在 {S.left}：这里是新一段的起点'),
        9: '`left` → {left}',
        32: '`left` 右移 → {left}：看下一个左端点',
        15: '新建 `minK_list`，记录本段里 minK 出现的位置',
        16: '新建 `maxK_list`，记录本段里 maxK 出现的位置',
        'if left == n': lambda S, B, r: ('`left == n`：后面没有合法段了 → 结束' if S.left == S.n else '还有合法段，继续'),
        'right = left': '从 `left` 开始向右找这一段的右边界：`right = {right}`',
        'while right < n and minK': lambda S, B, r: (f'`nums[{S.right}] = {S.nums[S.right]}` 在范围内 → 属于本段' if S.right < S.n and S.minK <= S.nums[S.right] <= S.maxK else f'`right = {S.right}`：到头或遇到范围外的数，本段是 `[{S.left}, {S.right})`'),
        'if nums[right] == minK': lambda S, B, r: (f'`{S.nums[S.right]} == minK` → 记下 minK 的位置 {S.right}' if S.nums[S.right] == S.minK else f'`{S.nums[S.right]}` 不是 minK'),
        'minK_list.append': '`minK_list` = {minK_list}',
        'if nums[right] == maxK': lambda S, B, r: (f'`{S.nums[S.right]} == maxK` → 记下 maxK 的位置 {S.right}' if S.nums[S.right] == S.maxK else f'`{S.nums[S.right]}` 不是 maxK'),
        'maxK_list.append': '`maxK_list` = {maxK_list}',
        'right += 1': '`right` → {right}',
        'minK_pos = maxK_pos = 0': '`minK_pos`、`maxK_pos`：左端点右侧第一个 minK / maxK 在列表里的下标',
        'while minK_pos != len': lambda S, B, r: ('两个列表里都还有位置 → 当前 left 右侧 minK、maxK 都出现过' if S.minK_pos != len(S.minK_list) and S.maxK_pos != len(S.maxK_list) else '某个列表用完了：left 右侧凑不齐 → 本段结束'),
        'res += right - max': '最短右端点 `max({minK_list[minK_pos]}, {maxK_list[maxK_pos]})`，最长到 `right-1`：`{right} - max(…)` → `res` = =={res}==',
        'if nums[left] == minK': lambda S, B, r: (f'`nums[{S.left}]` 是 minK：left 右移后，它不在窗口里 → `minK_pos` 后移' if S.nums[S.left] == S.minK else '不是 minK，`minK_pos` 不动'),
        'minK_pos += 1': '`minK_pos` → {minK_pos}',
        'if nums[left] == maxK': lambda S, B, r: (f'`nums[{S.left}]` 是 maxK → `maxK_pos` 后移' if S.nums[S.left] == S.maxK else '不是 maxK，`maxK_pos` 不动'),
        'maxK_pos += 1': '`maxK_pos` → {maxK_pos}',
        'left = right': '这一段处理完，`left` 跳到 `right` = {left}，找下一段',
        'return res': '共 `{res}` 个定界子数组',
    },
    cards=dict(
        one_liner='先切出范围内的段，再用位置列表数每个左端点的右端点个数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组最小值 `== minK` 且最大值 `== maxK` 叫定界子数组，求个数',
                 '示例：`[1,3,5,2,7,5]`，`minK=1, maxK=5` → `2`',
                 '本视频：`[1,3,5,2,7,5,1,5,4]` → `7`'],
        quote='可以拆分成两个部分：找出所有数组值都在 minK 到 maxK 之间的子数组；对于这些子数组，找出 minK 和 maxK 都至少出现过一次的子数组的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['先找一段全在 `[minK, maxK]` 内的区间，顺便记下 minK、maxK 的位置列表',
              '枚举左端点 left：右侧第一个 minK、maxK 位置的较大者就是最短右端点',
              '右端点最远到 `right-1`，个数 `right - max(…)`；left 右移时用两个下标追位置'],
        summary=['时间 `O(n)`，空间 `O(n)`（两个位置列表）',
                 '易错：越过 minK 或 maxK 所在位置后，对应下标要后移',
                 '`left = right`：这一段处理完就跳到下一段起点',
                 '原文为 Python 2 风格，只删去了函数开头及若干空白行',
                 '对比灵神：灵神一趟遍历只记三个位置，空间 `O(1)`'],
    ),
)
