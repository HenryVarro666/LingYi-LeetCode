CONFIG = dict(
    num=3872, title='替换最多一个元素后的最长等差子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='左右两遍扫描 · 三段拼接',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def longestArithmetic(self, nums):
        
        left = [1, 2]
        for index in range(2, len(nums)):
            if nums[index] - nums[index - 1] == nums[index - 1] - nums[index - 2]:
                left.append(left[-1] + 1)
            else:
                left.append(2)
        
        if left[-1] == len(nums):
            return len(nums)

        right = [1, 2]
        for index in range(len(nums) - 3, -1, -1):
            if nums[index] - nums[index + 1] == nums[index + 1] - nums[index + 2]:
                right.append(right[-1] + 1)
            else:
                right.append(2)
        right.reverse()

        res = max(max(left), max(right)) + 1
        for index in range(1, len(nums) - 1):
            s = nums[index - 1] + nums[index + 1]
            if s % 2 == 0:
                v = s // 2
                d = v - nums[index - 1]
                length = 3
                if index > 1 and nums[index - 1] - nums[index - 2] == d:
                    length += left[index - 1] - 1
                if index + 2 < len(nums) and nums[index + 2] - nums[index + 1] == d:
                    length += right[index + 1] - 1
                res = max(res, length)
        
        return res
''',
    call='Solution().longestArithmetic([1,3,8,7,9])',
    expect=5,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=210,
             color=lambda S, i, v: 'yellow' if 's' in S and i == S['index'] and S['_line'] >= 24 else None),
        dict(type='array', var='left', label='left：以 index 结尾的最长等差子数组', h=170),
        dict(type='array', var='right', label='right：以 index 开头的最长等差子数组（反向算完再翻转）', h=170),
        dict(type='text', h=70, size=28, fn=lambda S: (f"改 `nums[{S['index']}]` 为 `{S['v']}`，公差 `d` = =={S['d']}==，拼出 `length` = =={S['length']}==" if 'length' in S and 'v' in S and S['_line'] >= 27 else '')),
    ],
    watch=['index', 's', 'd', ('length', 'length', 'blue'), ('res', 'res', 'green')],
    max_steps=110,
    captions={
        'left = [1, 2]': '`left[0] = 1`，`left[1] = 2`：一个数长 1，两个数一定等差，长 2',
        'if nums[index] - nums[index - 1] ==': lambda S, B, r: (f"`{S.nums[S.index]-S.nums[S.index-1]}` vs `{S.nums[S.index-1]-S.nums[S.index-2]}`：" + ("公差相同 → 接在前一段后面" if S.nums[S.index]-S.nums[S.index-1] == S.nums[S.index-1]-S.nums[S.index-2] else "公差不同 → 重新从 2 开始")) if 'index' in S and S.index >= 2 and 'right' not in S else None,
        'left.append(left[-1] + 1)': '`left[{index}] = left[{index-1}] + 1` = =={left[-1]}==',
        'left.append(2)': '`left[{index}] = 2`：重新开始',
        'if left[-1] == len(nums)': lambda S, B, r: (f"`left[-1] = {S.left[-1]}`，`n = {len(S.nums)}` → 整个数组就是等差，答案 n" if S.left[-1] == len(S.nums) else f"`left[-1] = {S.left[-1]} != n = {len(S.nums)}` → 数组不是等差，需要改一个数"),
        'right = [1, 2]': '反向再扫一遍：先放最后两个位置的长度 `1, 2`（顺序是倒着的）',
        'if nums[index] - nums[index + 1]': lambda S, B, r: f"`{S.nums[S.index]-S.nums[S.index+1]}` vs `{S.nums[S.index+1]-S.nums[S.index+2]}`：" + ("公差相同 → 开头的等差段更长" if S.nums[S.index]-S.nums[S.index+1] == S.nums[S.index+1]-S.nums[S.index+2] else "公差不同 → 从 2 重新开始"),
        'right.append(right[-1] + 1)': '`right` 追加 `{right[-1]}`：`nums[{index}]` 开头的等差段更长了',
        'right.append(2)': '`right` 追加 `2`：公差对不上，重新开始',
        'right.reverse()': '翻转后 `right[i]` = 以 `i` 开头的最长等差长度 → `{right}`',
        'res = max(max(left)': '方案一：把最长等差段的左邻或右邻改成合适的值，能再长 1 → `res = {max(max(left), max(right))} + 1` = =={res}==',
        's = nums[index - 1]': '想改 `nums[{index}]` 来连接两边：左右邻居之和 `s = {nums[index-1]} + {nums[index+1]}` = =={s}==',
        'if s % 2 == 0': lambda S, B, r: (f"`s = {S.s}` 是偶数 → 平均数是整数，可以改" if S.s % 2 == 0 else f"`s = {S.s}` 是奇数 → 平均数不是整数，不能改，跳过"),
        'v = s // 2': '改成两邻居的平均 `v = {v}`',
        'd = v - nums[index - 1]': '这时的公差 `d = {v} - {nums[index-1]}` = =={d}==',
        'length = 3': '先算 `nums[index-1], v, nums[index+1]` 三个数，`length = 3`',
        'if index > 1 and nums[index - 1]': lambda S, B, r: (f"左边 `nums[{S.index-1}] - nums[{S.index-2}]` = {S.nums[S.index-1]-S.nums[S.index-2]} {'==' if False else ''}{'等于' if S.nums[S.index-1]-S.nums[S.index-2] == S.d else '不等于'} `d = {S.d}`" + (" → 能吸纳左段" if S.nums[S.index-1]-S.nums[S.index-2] == S.d else " → 不吸纳")) if S.index > 1 else f"`index = {S.index}`：左边没有 `nums[index-2]` → 不吸纳",
        'length += left[index - 1] - 1': '吸纳左段：加 `left[{index-1}] - 1` = {left[index-1]-1}（`nums[index-1]` 已算过，减 1），`length` → =={length}==',
        'if index + 2 < len(nums)': lambda S, B, r: (f"右边 `nums[{S.index+2}] - nums[{S.index+1}]` = {S.nums[S.index+2]-S.nums[S.index+1]} {'等于' if S.nums[S.index+2]-S.nums[S.index+1] == S.d else '不等于'} `d = {S.d}`" + (" → 能吸纳右段" if S.nums[S.index+2]-S.nums[S.index+1] == S.d else " → 不吸纳")) if S.index + 2 < len(S.nums) else f"`index + 2 = {S.index+2}` 越界：右边没有可吸纳的段",
        'length += right[index + 1] - 1': '吸纳右段：加 `right[{index+1}] - 1` = {right[index+1]-1}，`length` → =={length}==',
        'res = max(res, length)': '`res = max({B.res}, {length})` = =={res}==',
        'return res': '最长等差子数组长度 `{res}`',
    },
    cards=dict(
        one_liner='先算每个位置两侧的最长等差段，再枚举改哪个数把两段拼起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['最多把一个元素改成任意整数，然后选一个等差子数组',
                 '求能得到的最长等差子数组的长度',
                 '本视频：`[1,3,8,7,9]` 把 `8` 改成 `5` → `[1,3,5,7,9]`，`5`'],
        quote='通过修改某个nums[index]来连接nums[index - 1]与nums[index + 1]，构成：以nums[index - 1]结尾的最长等差子数组 <-> nums[index] <-> 以nums[index + 1]开头的最长等差子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left[i]`：以 `i` 结尾的最长等差长度；`right[i]`：以 `i` 开头的',
              '前提：`nums[index-1]` 与 `nums[index+1]` 同奇偶，才能改成平均数',
              '左公差、右公差都等于 `d` 就把两段吸纳进来，各减去重复的 1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '整个数组本来就是等差：`left[-1] == n` 直接返回 n',
                 '`length` 的初值 3 已包含 `nums[index-1]` 和 `nums[index+1]`，所以吸纳时都要 `-1`',
                 '`res` 初值 `max + 1`：改最长段旁边的数，保证两边至少有一侧能改',
                 '对比灵神：灵神 `pre/suf` 加上分三种情况更新，yiduobo 用累加 `length`'],
    ),
)
