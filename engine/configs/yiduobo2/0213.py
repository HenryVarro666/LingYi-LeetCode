NUMS = [2, 7, 9, 3, 1]

TRACK = '''
class KList(list):  # 快照用的普通 list（带 cur / seg）
    pass

class TList(list):  # 只用于动画：切片被 for 遍历时，在原数组上记录当前下标 cur 与区间 seg
    root = None
    off = 0
    def __getitem__(self, i):
        if isinstance(i, slice):
            start, stop, _ = i.indices(len(self))
            t = TList(list.__getitem__(self, i))
            t.root, t.off = self, start
            return t
        return list.__getitem__(self, i)

    def __iter__(self):
        r = self.root if self.root is not None else self
        r.seg = (self.off, self.off + len(self))
        for k in range(len(self)):
            r.cur = self.off + k
            yield list.__getitem__(self, k)
        r.cur = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.cur = getattr(self, 'cur', None)
        c.seg = getattr(self, 'seg', None)
        return c
'''

N = len(NUMS)


def _rob(a):
    l2 = l1 = 0
    for x in a:
        l1, l2 = max(l2 + x, l1), l1
    return l1


RES1, RES2 = _rob(NUMS[:-1]), _rob(NUMS[1:])


def _cur(S):
    return getattr(S.get('nums'), 'cur', None)


def _pass(S):
    """第几趟：1 = nums[:-1]，2 = nums[1:]，0 = 还没开始"""
    line = S.get('_line') or 0
    if line >= 15:
        return 2
    if line >= 9:
        return 1
    return 0


def _row(which):
    def color(S, i, v):
        p = _pass(S)
        if p != which:
            return None
        cur = _cur(S)
        if i == cur:
            return 'orange'
        lo = 0 if which == 1 else 1
        if cur is not None and lo <= i < cur:
            return 'blue'
        return None

    def dim(S, i, v):
        return (which == 1 and i == N - 1) or (which == 2 and i == 0)
    return color, dim


def _formula(S, B):
    if S.get('_line') not in (11, 17) or 'num' not in S:
        if _pass(S) == 1 and 'res' not in S:
            return '`last_one`：到上一家为止的最大收益；`last_two`：到上上家为止'
        if 'res' in S:
            return f"第一趟（放弃最后一家）结果 `res = {S['res']}`" + (f"；第二趟当前 `last_one = {S['last_one']}`" if _pass(S) == 2 else '')
        return ''
    a, b = B['last_two'] + S['num'], B['last_one']
    return (f"`last_one = max(last_two + num, last_one)` = `max({B['last_two']} + {S['num']}, {b})` = =={S['last_one']}==")


def _cap_dp(S, B, ret):
    take, skip = B.last_two + S.num, B.last_one
    return (f'选 `{S.num}`：`last_two + {S.num} = {take}`；不选：`last_one = {skip}` → =={"选" if take > skip else "不选"}==，'
            f'`last_one = {S.last_one}`')


c1, d1 = _row(1)
c2, d2 = _row(2)


def _p1(S):
    return _cur(S) if _pass(S) == 1 else None


def _p2(S):
    return _cur(S) if _pass(S) == 2 else None

CONFIG = dict(
    num=213, title='打家劫舍 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='环拆成两条链 · 198 题跑两次',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def rob(self, nums):
        if not nums:
            return 0

        if len(nums) <= 2:
            return max(nums)

        last_two = last_one = 0
        for num in nums[:-1]:
            last_one, last_two = max(last_two + num, last_one), last_one

        res = last_one

        last_two = last_one = 0
        for num in nums[1:]:
            last_one, last_two = max(last_two + num, last_one), last_one

        return max(res, last_one)
''',
    setup=TRACK,
    call=f'Solution().rob(TList({NUMS}))',
    expect=11,
    views=[
        dict(type='text', fn=_formula, size=26, h=90, lines=2),
        dict(type='array', var=lambda S: list(S['nums']) if 'nums' in S else None,
             label='第一趟 nums[:-1]：放弃最后一家（灰），蓝 = 已考虑', cell=96, h=190,
             pointers={_p1: 'orange'}, pointer_labels={_p1: 'num'}, color=c1, dim=d1),
        dict(type='array', var=lambda S: list(S['nums']) if 'nums' in S else None,
             label='第二趟 nums[1:]：放弃第一家（灰）', cell=96, h=190,
             pointers={_p2: 'orange'}, pointer_labels={_p2: 'num'}, color=c2, dim=d2),
    ],
    watch=[('num', 'num', 'orange'), ('last_two', 'last_two', 'blue'), ('last_one', 'last_one', 'green'), ('res', 'res', 'pink')],
    captions={
        'if not nums': '空数组直接返回 0；这里 `nums` 不空',
        'if len(nums) <= 2': lambda S, B, ret: (f'`len(nums) = {len(S.nums)} > 2`：首尾两家不是同一家，正常处理'),
        'return max(nums)': '只有 1~2 家：只能偷一家，偷最多的',
        'for num in nums[:-1]': lambda S, B, ret: (f'考虑第 `{_cur(S)}` 家 `num = {S.num}`' if _cur(S) is not None
                                                   else f'第一趟结束：不偷最后一家时最多偷 `{S.last_one}`'),
        'res = last_one': '记下第一趟的答案 `res = {res}`',
        'last_two = last_one = 0': lambda S, B, ret: ('第二趟：==放弃第一家==，滚动变量清零' if 'res' in S
                                                      else '第一趟：==放弃最后一家==，在 `nums[:-1]` 上跑 198 题；`last_two = last_one = 0`'),
        'for num in nums[1:]': lambda S, B, ret: (f'考虑第 `{_cur(S)}` 家 `num = {S.num}`' if _cur(S) is not None
                                                  else f'第二趟结束：不偷第一家时最多偷 `{S.last_one}`'),
        'last_one, last_two = max': _cap_dp,
        'return max(res, last_one)': '两种放弃方式取较大值：`max({res}, {last_one})` = =={ret}==',
    },
    cards=dict(
        one_liner='第一家和最后一家不能同时选：分别放弃其中一家，跑两遍 198 题取较大值',
        complexity='时间 `O(n)`，空间 `O(1)`（切片除外）',
        problem=['房屋==围成一圈==，第一家和最后一家相邻；相邻两家不能同时偷',
                 '求今晚最多能偷多少钱',
                 '示例：`[2,3,2]` → `3`，`[1,2,3,1]` → `4`',
                 f'本视频：`{NUMS}` → `11`'],
        quote='第一家与最后一家就不能同时选取，于是可以==选择放弃第一家==，计算第二家到最后一家的最大收益，然后==选择放弃最后一家==，计算第一家到倒数第二家的最大收益，最后取其中较大的值作为答案。',
        quote_src='—— yiduobo 题解',
        idea=['放弃最后一家：`nums[:-1]` 变成普通的一排，跑 198 题',
              '放弃第一家：`nums[1:]` 同理',
              '首尾不能同时偷 → 最优解一定落在两种情况之一',
              '198 题做法：`last_one = max(last_two + num, last_one)`'],
        result=f'放弃最后一家 `{RES1}`，放弃第一家 `{RES2}` → 答案 `{max(RES1, RES2)}` ✓',
        summary=['时间 `O(n)`，滚动变量 `O(1)`',
                 '`len(nums) <= 2` 要特判：只有一家时 `nums[:-1]`、`nums[1:]` 都是空的',
                 '两趟之间别忘了把 `last_two`、`last_one` 清零',
                 '原文为 Python 2 风格，仅删去文档字符串，代码未改',
                 '对比灵神：按「偷不偷 nums[0]」分类，不用特判长度'],
    ),
)
