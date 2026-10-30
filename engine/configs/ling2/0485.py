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

NUMS = [1, 1, 0, 1, 1, 1, 0, 1]


def _cur(S):
    nums = S.get('nums')
    p = getattr(nums, 'pos', None)
    return p if p is not None and p < len(nums) else None


def _done(S):
    """cnt 已经统计到的最后一个下标：执行完第 6/9 行才算处理完当前元素"""
    p = _cur(S)
    if p is None:
        return None
    return p if S.get('_line') in (6, 7, 9) else p - 1


def _color(S, i, v):
    p = _done(S)
    if p is None or 'cnt' not in S:
        return None
    if S['cnt'] and p - S['cnt'] < i <= p:
        return 'blue'          # 当前这一段连续 1
    if i == p and v == 0:
        return 'red'
    return None


def _dim(S, i, v):
    p = _cur(S)
    return p is not None and i > p


def _seg(S):
    p = _done(S)
    if p is None or p < 0 or 'cnt' not in S:
        return '蓝色 = 以当前元素结尾的那一段连续 1'
    if S['cnt'] == 0:
        return f'`nums[{p}] = 0`：连续段被打断，`cnt` 归零'
    return f'当前连续段 `nums[{p - S["cnt"] + 1}..{p}]`，长度 `cnt = {S["cnt"]}`，历史最长 `ans = {S.get("ans", 0)}`'


CONFIG = dict(
    num=485, title='最大连续 1 的个数', difficulty='Easy', category='普通数组',
    author='灵茶山艾府', technique='一次遍历 · 维护连续 1 的个数',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        ans = cnt = 0
        for x in nums:
            if x:
                cnt += 1  # 连续 1 的个数增加
                ans = max(ans, cnt)  # 更新答案的最大值
            else:
                cnt = 0  # 重置
        return ans
''',
    setup=SETUP,
    call=f'Solution().findMaxConsecutiveOnes(Nums({NUMS}))',
    expect=3,
    views=[
        dict(type='text', fn=_seg, size=28, h=90),
        dict(type='array', var='nums', label='nums（蓝 = 当前这段连续 1）', cell=100, h=300,
             pointers={_cur: 'pink'}, pointer_labels={_cur: 'x'}, color=_color, dim=_dim),
    ],
    watch=[('x', 'x', 'pink'), ('cnt', 'cnt', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt = 0': '`cnt`：目前连续 1 的个数；`ans`：答案，都从 `0` 开始',
        'for x in nums': lambda S, B, r: (f'看 `nums[{_cur(S)}] = {S.x}`' if _cur(S) is not None else '遍历结束'),
        'if x:': lambda S, B, r: (f'`x = 1` → 连续段可以==延长==' if S.x else f'`x = 0` → 连续段==断了=='),
        'cnt += 1': '连续 1 的个数增加：`cnt` → =={cnt}==',
        'ans = max': '更新答案的最大值：`max({B.ans}, {cnt})` = =={ans}==',
        'cnt = 0': '遇到 0，下一段要从头数：`cnt` 重置为 `0`',
        'return ans': '最大连续 1 的个数 = =={ans}==',
    },
    cards=dict(
        one_liner='遇 1 计数加一并更新答案，遇 0 计数清零',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定只含 0 和 1 的数组 `nums`，求==最长的连续 1== 有多少个',
                 '示例：`[1,1,0,1,1,1]` → `3`（最后三位）',
                 f'本视频：`{NUMS}` → `3`'],
        quote='遍历 nums，同时维护目前连续 1 的个数 cnt。如果 nums[i]=0，把 cnt 重置为 0。如果 nums[i]=1，把 cnt 加一，然后用 cnt 更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`cnt` 始终表示：==以当前元素结尾==的连续 1 的长度',
              '每次 `cnt` 变大就立刻更新 `ans`，所以末尾那段 1 也不会漏掉'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ans = max(ans, cnt)` 放在 `x == 1` 分支里：==数组以 1 结尾也能统计到==',
                 '`if x:` 利用 0/1 本身当布尔值，简洁',
                 '思考题：允许删一个数 → 1493. 删掉一个元素以后全为 1 的最长子数组'],
    ),
)
