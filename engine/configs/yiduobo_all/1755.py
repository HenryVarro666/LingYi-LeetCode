def _li(S):
    if 'num' in S and 'left_list' in S and S['num'] in S['left_list']:
        return S['left_list'].index(S['num'])
    return None


CONFIG = dict(
    num=1755, title='最接近目标值的子序列和', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='折半枚举 + 排序后双指针',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def minAbsDifference(self, nums, goal):

        n = len(nums)
        if n == 1:
            return min(abs(nums[0] - goal), abs(goal))
        
        cut_pos = n // 2
        left_sum = set([0])
        for num in nums[:cut_pos]:
            left_sum = left_sum.union(set([x + num for x in left_sum]))
        
        right_sum = set([0])
        for num in nums[cut_pos:]:
            right_sum = right_sum.union(set([x + num for x in right_sum]))
        
        left_list = sorted(left_sum)
        right_list = sorted(right_sum)

        p = len(right_list) - 1
        res = abs(goal)
        for num in left_list:
            while p >= 0 and num + right_list[p] > goal:
                p -= 1
            
            if p >= 0:
                res = min(res, abs(num + right_list[p] - goal))
            if p < len(right_list) - 1:
                res = min(res, abs(num + right_list[p + 1] - goal))
        
        return res
''',
    call='Solution().minAbsDifference([5,-7,3,5], 6)',
    expect=0,
    views=[
        dict(type='array', var='nums', label='nums（从中间切成两半）', cell=90, h=180, pointers={'cut_pos': 'pink'}),
        dict(type='array', var='left_list', label='left_list（左半，蓝=当前 num）', cell=80, h=185, color=lambda S, i, v: 'blue' if S['_line'] >= 22 and v == S.get('num') else None),
        dict(type='array', var='right_list', label='right_list（右半，升序）', cell=80, h=185, pointers={'p': 'orange'}),
        dict(type='text', h=90, size=28, fn=lambda S: (
            f'`num + right_list[p] = {S["num"]} + {S["right_list"][S["p"]]} = {S["num"] + S["right_list"][S["p"]]}`，目标 `goal = {S["goal"]}`'
            if S['_line'] >= 22 and 'p' in S and 'num' in S and 'right_list' in S and 0 <= S['p'] < len(S['right_list'])
            else '目标：从两个有序列表各取一个数，使和最接近 `goal`')),
    ],
    watch=[('goal', 'goal', 'cyan'), ('num', 'num', 'blue'), ('p', 'p', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '共 `{n}` 个数，数据范围小到可以折半枚举',
        'cut_pos = n // 2': '从中间切开：左半 `nums[:{cut_pos}]`，右半 `nums[{cut_pos}:]`，各自只有 `2^{cut_pos}` 左右种子集和',
        'left_sum = set': '`left_sum` 记录左半所有子集和，初始只有空集 `0`',
        'right_sum = set': '`right_sum` 记录右半所有子集和，初始只有空集 `0`',
        'for num in nums[:cut_pos]': '左半取下一个数 `num`',
        'for num in nums[cut_pos:]': '右半取下一个数 `num`',
        'left_sum = left_sum.union': '已有的每个和都可以再加上 `{num}`：`left_sum` = `{sorted(left_sum)}`',
        'right_sum = right_sum.union': '已有的每个和都可以再加上 `{num}`：`right_sum` = `{sorted(right_sum)}`',
        'left_list = sorted': '左半子集和排序：从小到大',
        'right_list = sorted': '右半子集和排序：`p` 从最大的那个开始往前找',
        'p = len(right_list) - 1': '`p` 指向 `right_list` 最后一个（最大）',
        'res = abs(goal)': '什么都不选时差距是 `|goal| = {res}`，作为初始答案',
        'for num in left_list': '从小到大枚举左半的和 `num`，`num` 变大，合适的 `p` 只会往左走',
        'while p >= 0 and': lambda S, B, r: (
            '`p < 0`：右边已经没有更小的了，停' if S.p < 0 else
            (f'`{S.num} + {S.right_list[S.p]} = {S.num + S.right_list[S.p]} > goal = {S.goal}`：超过目标了 → `p` 要左移'
             if S.num + S.right_list[S.p] > S.goal else
             f'`{S.num} + {S.right_list[S.p]} = {S.num + S.right_list[S.p]} <= goal = {S.goal}`：`p` 停在不超过 goal 的最大位置')),
        'p -= 1': '`p` 左移 → {p}',
        'if p >= 0': lambda S, B, r: (f'`p = {S.p}` 有效：和 `<= goal` 的最接近候选是 `{S.right_list[S.p]}`' if S.p >= 0
                                      else '`p < 0`：没有不超过 goal 的搭配，跳过这一侧'),
        'res = min(res, abs(num + right_list[p] - goal))': '差距 `|{num} + {right_list[p]} − {goal}| = {abs(num + right_list[p] - goal)}`，和旧答案 `{B.res}` 取小 → `res = {res}`',
        'if p < len(right_list) - 1': lambda S, B, r: (f'`p + 1 = {S.p + 1}` 还在范围内：再看刚好超过 goal 的候选' if S.p < len(S.right_list) - 1
                                                       else '`p` 已在最后：没有超过 goal 的候选'),
        'res = min(res, abs(num + right_list[p + 1] - goal))': '差距 `|{num} + {right_list[p + 1]} − {goal}| = {abs(num + right_list[p + 1] - goal)}`，和旧答案 `{B.res}` 取小 → `res = {res}`',
        'return res': '最小的差距 `{res}`',
    },
    max_steps=75,
    cards=dict(
        one_liner='40 个数拆成两个 20，各自暴力，再用双指针配对',
        complexity='时间 `O(2^(n/2)·n)`，空间 `O(2^(n/2))`',
        problem=['从 `nums` 选一个子序列（可为空），使元素和与 `goal` 的差的绝对值最小',
                 '返回这个最小值，`n <= 40`',
                 '本视频：`nums = [5,-7,3,5]`，`goal = 6` → `0`'],
        quote='题目非常取巧地给了一个40的数据范围。一个常见的数据范围是2^20 = 1048576，也就是百万规模。',
        quote_src='—— yiduobo 题解原文',
        idea=['把数组切成两半，各自枚举出所有子集和，排序',
              '枚举左边的和 `num`，右边指针 `p` 从尾部向前，找刚好不超过 `goal` 的位置',
              '`num` 增大，合适的 `p` 只会变小，所以指针只回退不前进，均摊 `O(1)`'],
        summary=['时间约 `O(2^(n/2)·n)`（含排序），空间 `O(2^(n/2))`',
                 '每个 `num` 要看两个候选：`right_list[p]` 和 `right_list[p+1]`',
                 '`res` 初始为 `|goal|`，对应一个数都不选',
                 '原文为 Python 2 写法，`n / 2` 整数除法已改为 `n // 2`'],
    ),
)
