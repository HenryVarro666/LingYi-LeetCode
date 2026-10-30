CONFIG = dict(
    num=665, title='非递减数列', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心：一趟扫描，只改一次',
    code='''
class Solution(object):
    def checkPossibility(self, nums):

        now = nums[0]
        change = True
        for index in range(1, len(nums)):
            if nums[index] >= now:
                now = nums[index]
            elif change:
                if index == 1 or nums[index - 2] <= nums[index]:
                    now = nums[index]
                change = False
            else:
                return False

        return True
''',
    call='Solution().checkPossibility([2,3,3,2,4])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前 index）', pointers={'index': 'blue'}, h=260),
        dict(type='text', size=32, fn=lambda S: (
            f"前一个有效值 `now = {S['now']}`，还能修改一次：=={'是' if S['change'] else '否'}==" if 'now' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'green'), ('change', 'change（还能改）', 'orange')],
    captions={
        'now = nums[0]': '`now` 表示「修改之后」前一个位置的值，先取 `nums[0] = {now}`',
        'change = True': '`change = True`：还有 ==一次修改机会==',
        'if nums[index] >= now': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` ≥ `now = {B.now}` → 没有逆序，`now` 更新为它' if S.nums[S.index] >= B.now
                                                  else f'`nums[{S.index}] = {S.nums[S.index]}` < `now = {B.now}` → 出现逆序，必须改一个数'),
        'elif change': lambda S, B, r: ('还有修改机会 → 动手修改' if S.change else '已经用过一次修改 → 第二次逆序，不可能了'),
        'if index == 1 or': lambda S, B, r: (
            '`index == 1`：前面没有 nums[index-2]，降低前一个不会冲突 → 改前一个' if S.index == 1 else
            (f'`nums[{S.index-2}] = {S.nums[S.index-2]}` ≤ `nums[{S.index}] = {S.nums[S.index]}`：降低前一个不冲突 → 改前一个，当前数原样保留'
             if S.nums[S.index-2] <= S.nums[S.index] else
             f'`nums[{S.index-2}] = {S.nums[S.index-2]}` > `nums[{S.index}] = {S.nums[S.index]}`：降低前一个会与更前面冲突 → 只能把 nums[index] 抬到 `now = {B.now}`，`now` 不变')),
        8: '没有逆序：`now` → {now}，当前数成为新的前值',
        11: '`now` → {now}：当前数原样保留，成为新的前值',
        'change = False': '修改机会用掉了：`change = False`',
        'return False': '再次出现逆序，已经没有修改机会 → 返回 ==False==',
        'return True': '整条数组扫完，最多改了一次 → 返回 True',
    },
    cards=dict(
        one_liner='遇到逆序，尽量改前一个数，让后面的数更容易接上',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定数组 `nums`，最多修改 ==一个元素==，能否变成非递减数列（`nums[i] <= nums[i+1]`）',
                 '示例：`[4,2,3]` → `true`（把 4 改成 1）',
                 '本视频：`[2,3,3,2,4]` → `true`（把第二个 3 之后的 2 抬成 3）'],
        quote='为了改变后满足nums[index + 1]大于等于nums[index]，因此我们在这里希望nums[index]尽量小。',
        quote_src='—— yiduobo 题解原文',
        idea=['出现 `nums[index] < now`：必须改 `nums[index-1]` 或 `nums[index]` 之一',
              '优先改前一个（降低它），这样 `nums[index]` 原样保留、后面更好接',
              '若 `nums[index-2] > nums[index]`，降前一个会冲突，只能把 `nums[index]` 抬高到前值',
              '有标记 `change`：第二次逆序直接返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`index == 1` 时没有 `nums[index-2]`，要单独判断',
                 '易错：`now` 表示「修改后」的前一个值，不是原数组的前一个',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
