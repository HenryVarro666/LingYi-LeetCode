def _num_inner(S):
    return S['_inner'].get('num')


def _if(S, B, ret):
    num = S.num
    c = B.nums_count[num]
    if c > 0 and not B.now and num != next(iter(B.nums_count)):
        return f'第 1 轮的下一个键是 `{num}`：==两个 1 只占了一个键，第一位不会再试一次 1== → 选 `{num}`'
    if c > 0:
        return f'`{num}` 还剩 `{c}` 次 → 选它'
    return f'`{num}` 剩余 `0` 次 → 跳过'


def _rest(S, B, ret):
    if S.rest_flag:
        return '`rest_flag` 仍为 True：==每个数字可用次数都为 0== → 生成一个可行解'
    return '`rest_flag` 为 False → 不记录，返回'


CONFIG = dict(
    num=47, title='全排列 II', difficulty='Medium', category='回溯',
    author='yiduobo', technique='计数字典 · 同一轮只试不同的数字',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def permuteUnique(self, nums):
        nums_count = {}
        for num in nums:
            nums_count[num] = nums_count.get(num, 0) + 1

        res = []

        self.dfs(nums_count, [], res)
        return res

    def dfs(self, nums_count, now, res):
        rest_flag = True

        for num in nums_count:
            if nums_count[num] > 0:
                now.append(num)
                nums_count[num] -= 1
                self.dfs(nums_count, now, res)
                nums_count[num] += 1
                now.pop()
                rest_flag = False

        if rest_flag:
            res.append(now[:])
''',
    call='Solution().permuteUnique([1, 1, 2])',
    expect=[[1, 1, 2], [1, 2, 1], [2, 1, 1]],
    views=[
        dict(type='map', var='nums_count', label='nums_count（数字 → 剩余可用次数）', h=120,
             fmt=lambda k, v: f'{k} 剩 {v} 次'),
        dict(type='stack', var='now', label='now（当前生成的排列）', h=110),
        dict(type='calls', h=190, hide=('nums_count', 'res', 'now')),
        dict(type='stack', var='res', label='res', h=110),
    ],
    watch=[('num', _num_inner, 'pink'), ('rest_flag', lambda S: S['_inner'].get('rest_flag'), 'orange')],
    skip=['for num in nums_count', 'for num in nums:', 'nums_count[num] = nums_count.get', 'self.dfs(nums_count, now, res)', 'rest_flag = False'],
    captions={
        'nums_count = {}': '`nums_count` 字典：每个数字==剩余的可用次数==',
        'res = []': '统计好每个数字出现的次数：`{nums_count}`',
        'self.dfs(nums_count, [], res)': '开始迭代：`now` 为空，每一轮在末尾放一个数字',
        'rest_flag = True': lambda S, B, ret: f'第 {len(S.now) + 1} 轮：先设 `rest_flag = True`',
        'if nums_count[num] > 0': _if,
        'now.append(num)': '`now` 末尾放入 `{num}`',
        'nums_count[num] -= 1': '`{num}` 次数减 1 → `{nums_count[num]}`，进行下一轮',
        'nums_count[num] += 1': '返回：`{num}` 的次数还回去 → `{nums_count[num]}`',
        'now.pop()': lambda S, B, ret: (f'弹出 `{B.now[-1]}`，接着试==下一个不同的数字==（选过数字，`rest_flag = False`）'
                                        if len(S.now) == 0 and S.num == 1 else f'弹出 `{B.now[-1]}`，`rest_flag = False`'),
        'if rest_flag': _rest,
        'res.append(now[:])': '把 `now` 的副本 `{res[-1]}` 加入 res，然后返回',
        'return res': '全部迭代完：共 `{len(ret)}` 个不重复的排列',
    },
    max_steps=80,
    cards=dict(
        one_liner='同一轮迭代里，相同的数字只试一次',
        complexity='时间 `O(n·n!)`，空间 `O(n)`（不计返回值）',
        problem=['给定一个==可包含重复数字==的序列 `nums`，按任意顺序返回所有==不重复==的全排列',
                 '示例：`[1,1,2]` → `[[1,1,2],[1,2,1],[2,1,1]]`'],
        quote='要想不重复的话就必须保证==同一轮的迭代中不能选择相同的数字==，于是我们可以统计出每个数字出现的次数，然后每轮检查每个不同的数字。',
        quote_src='—— yiduobo 题解',
        idea=['`nums_count` 的键是==不同的数字==，值是剩余可用次数',
              '每一轮遍历字典：次数 > 0 就选它，递归后再把次数还回去',
              '所有数字次数都为 0（`rest_flag` 仍为 True）→ 得到一个解'],
        result='3 个不重复的排列全部找到 ✓',
        summary=['时间 `O(n·n!)`，空间 `O(n)`；不需要排序',
                 '去重原理：每一轮只遍历==不同的数字==，两个 1 不会在同一位置各试一次',
                 '`rest_flag` 代替 `len(now) == n` 判断是否用完',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改',
                 '对比灵神：灵神排序后跳过“前一个相同数没填”的情况，yiduobo 用计数'],
    ),
)
