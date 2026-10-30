# setup 里的 Nums 只是普通 list，额外记下 for 循环当前走到的下标 pos（仅用于画图，不影响代码逻辑）
SETUP = '''
class Nums(list):
    def __init__(self, it):
        super().__init__(it)
        self.live = True
    def __iter__(self):
        return self._walk() if self.live else list.__iter__(self)
    def _walk(self):
        for i in range(len(self)):
            self.pos = i
            yield list.__getitem__(self, i)
        self.pos = len(self)
    def __deepcopy__(self, memo):
        c = Nums(list.__iter__(self))
        c.__dict__.update(self.__dict__)
        c.live = False
        return c
'''

NUMS = [1, 1, 0, 1, 0, 1, 1, 1]


def _cur(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return p if p is not None and p < len(nums) else None


def _done(S):
    """now 已经统计到的最后一个下标：for 行之后、if 行时还没处理当前元素"""
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    if p is None:
        return None
    if p >= len(nums):
        return len(nums) - 1
    return p if S.get('_line') in (7, 9, 10) else p - 1


def _color(S, i, v):
    p = _done(S)
    if p is None or 'now' not in S:
        return None
    if S['now'] and p - S['now'] < i <= p:
        return 'blue'          # 正在统计的这一段 1
    if i == p and v == 0:
        return 'red'
    return None


def _dim(S, i, v):
    p = _cur(S)
    return p is not None and i > p


def _seg(S):
    p = _done(S)
    if p is None or p < 0 or 'now' not in S:
        return '蓝色 = 正在统计的这一段连续 1（`now`）'
    if S.get('_line') == 11:
        return f'扫描结束时还有一段 `now = {S["now"]}` ==没结算==，最后要和 `res = {S["res"]}` 再比一次'
    if S['now'] == 0:
        return f'`nums[{p}] = 0`：上一段已结算进 `res = {S["res"]}`，`now` 归零'
    return f'正在统计的段 `nums[{p - S["now"] + 1}..{p}]`：`now = {S["now"]}`；已结算的最大 `res = {S["res"]}`'


CONFIG = dict(
    num=485, title='最大连续 1 的个数', difficulty='Easy', category='普通数组',
    author='yiduobo', technique='一趟扫描 · 遇 0 结算',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        res = 0
        now = 0
        for num in nums:
            if num == 1:
                now += 1
            else:
                res = max(now, res)
                now = 0
        return max(now, res)
''',
    setup=SETUP,
    call=f'Solution().findMaxConsecutiveOnes(Nums({NUMS}))',
    expect=3,
    views=[
        dict(type='text', fn=_seg, size=28, h=90),
        dict(type='array', var='nums', label='nums（蓝 = 正在统计的这段 1）', cell=100, h=300,
             pointers={_cur: 'pink'}, pointer_labels={_cur: 'num'}, color=_color, dim=_dim),
    ],
    watch=[('num', 'num', 'pink'), ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res`：==已经结算==的最长连续 1',
        4: '`now`：当前这一段连续 1 的长度',
        'for num in nums': lambda S, B, r: (f'扫到 `nums[{_cur(S)}] = {S.num}`' if _cur(S) is not None else '一趟扫描结束'),
        'if num == 1': lambda S, B, r: ('`num == 1` → 当前段继续变长' if S.num == 1 else '`num == 0` → 当前段==到头了==，要结算'),
        'now += 1': '`now` → =={now}==（这里先不更新 res）',
        'res = max(now, res)': '一段 1 结束才结算：`max({now}, {B.res})` = =={res}==',
        10: '`now` 清零，准备统计下一段',
        'return max(now, res)': lambda S, B, r: (f'数组以 1 结尾，最后一段 `now = {S.now}` 没遇到 0 ==还没结算== → `max({S.now}, {S.res})` = =={r}=='),
    },
    cards=dict(
        one_liner='一趟扫描数连续的 1，遇到 0 时结算，最后别忘了收尾',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定只含 0 和 1 的数组 `nums`，求==最长的连续 1== 有多少个',
                 '示例：`[1,1,0,1,1,1]` → `3`',
                 f'本视频：`{NUMS}` → `3`（最长段在末尾）'],
        quote='比较基础的题目，一趟扫描统计1连续出现的次数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 数当前这一段 1；==遇到 0 才把 now 结算进 res==，然后清零',
              '末尾的那段 1 后面没有 0 → 循环里结算不到',
              '所以返回 `max(now, res)`，把最后一段补上'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：==只在遇 0 时结算==，返回前必须再 `max(now, res)` 一次，否则末尾的段会丢',
                 '对比灵神：灵神每次 `cnt += 1` 都立刻更新答案，就不需要收尾',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
