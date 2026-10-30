import math

NUMS = [2, 7, 9, 3, 1]

TRACK = '''
class KList(list):  # 快照用的普通 list（带 off / k）
    pass

class TList(list):  # 只用于动画：切片时记住在原数组中的起点 off，for 循环时记录当前下标 k
    off = 0
    def __getitem__(self, i):
        if isinstance(i, slice):
            start = i.indices(len(self))[0]
            t = TList(list.__getitem__(self, i))
            t.off = self.off + start
            return t
        return list.__getitem__(self, i)

    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        c.off = self.off
        return c
'''


def _rob1(a):
    f0 = f1 = 0
    for x in a:
        f0, f1 = f1, max(f1, f0 + x)
    return f1


CASE1 = NUMS[0] + _rob1(NUMS[2:-1])
CASE2 = _rob1(NUMS[1:])


def _info(S):
    """(case, off, length, cur)：case 1 = 偷 nums[0]，2 = 不偷，0 = 还在 rob 里"""
    a = S.get('nums')
    off = getattr(a, 'off', 0)
    if off == 0 or a is None:
        return 0, 0, len(NUMS), None
    k = getattr(a, 'k', None)
    cur = off + k if isinstance(k, int) and k >= 0 else None
    return (1 if off == 2 else 2), off, len(a), cur


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    case, off, ln, cur = _info(S)
    n = len(NUMS)
    title = {0: '房子围成一圈：nums[0] 和 nums[n-1] 相邻',
             1: '情况一：偷 nums[0] → nums[1]、nums[n-1] 不能偷，剩下 nums[2..n-2] 是一排',
             2: '情况二：不偷 nums[0] → 剩下 nums[1..n-1] 是一排'}[case]
    cv.text((x0 + 18, y0 + 4), title, 23, T['muted'], bold=True)
    cx, cy, R = x0 + 260, y0 + 262, 145
    pos = [(cx + R * math.sin(2 * math.pi * i / n), cy - R * math.cos(2 * math.pi * i / n)) for i in range(n)]
    cv.d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=T['border'], width=2)
    for i, (X, Y) in enumerate(pos):
        inseg = case and off <= i < off + ln
        fill, tc, mark = T['panel2'], T['text'], None
        if case == 1 and i == 0:
            fill, tc, mark = T['green'], T['bg'], '偷'
        elif case == 1 and i in (1, n - 1):
            fill, tc, mark = (40, 45, 53), T['dim'], '禁'
        elif case == 2 and i == 0:
            fill, tc, mark = (40, 45, 53), T['dim'], '不偷'
        elif inseg:
            fill = (40, 70, 110)
        if cur == i:
            fill, tc = T['orange'], T['bg']
        cv.rect((X - 38, Y - 38, X + 38, Y + 38), fill=fill, r=12, outline=T['blue'] if inseg else T['border'], width=3 if inseg else 1)
        cv.text((X, Y), NUMS[i], 34, tc, anchor='mm', bold=True)
        ox, oy = (X - cx) / R, (Y - cy) / R
        cv.text((X + ox * 62, Y + oy * 58), f'[{i}]', 19, T['muted'], anchor='mm', mono=True)
        if mark:
            cv.text((X, Y + 56 if oy >= 0 else Y - 58), mark, 20, T['green'] if mark == '偷' else T['red'], anchor='mm', bold=True)
    # 右侧：两种情况的结果
    tx = x0 + 500
    ty = y0 + 70
    cv.text((tx, ty), '两种情况取最大值：', 24, T['text'], bold=True)
    l1 = f'情况一：{NUMS[0]} + rob1({NUMS[2:-1]})'
    l2 = f'情况二：rob1({NUMS[1:]})'
    done1 = case == 2 or S.get('_end')
    cv.text((tx, ty + 50), l1, 22, T['green'] if case == 1 else T['text'], bold=case == 1)
    cv.text((tx + 20, ty + 84), f'= {NUMS[0]} + {CASE1 - NUMS[0]} = {CASE1}' if done1 else '= ?', 24,
            T['yellow'] if done1 else T['dim'], bold=True)
    cv.text((tx, ty + 134), l2, 22, T['green'] if case == 2 else T['text'], bold=case == 2)
    fin = case == 2 and S.get('_line') == 7
    cv.text((tx + 20, ty + 168), f'= {CASE2}' if fin else '= ?', 24, T['yellow'] if fin else T['dim'], bold=True)
    if fin:
        cv.rich(tx, ty + 222, f'答案 `max({CASE1}, {CASE2})` = =={max(CASE1, CASE2)}==', x1 - tx - 20, size=26)


def _formula(S, B):
    if 'f1' not in S or 'x' not in S or _info(S)[3] is None:
        return '`f0`、`f1` 是 198 题的滚动变量：考虑到上一间、当前这一间时的最大金额' if 'f1' in S else ''
    if S.get('_line') != 6:
        return f"`f0 = {S['f0']}`，`f1 = {S['f1']}`；下一间 `x = {S['x']}`"
    return f"`f0, f1 = {B['f1']}, max({B['f1']}, {B['f0']} + {S['x']})` → `f0 = {S['f0']}`，`f1` = =={S['f1']}=="


def _cap_f(S, B, ret):
    no, yes = B.f1, B.f0 + S.x
    return (f'不偷 `{S.x}`：`f1 = {no}`；偷：`f0 + {S.x} = {yes}` → ==' + ('偷' if yes > no else '不偷') +
            f'==，`f1 = {S.f1}`')


CONFIG = dict(
    num=213, title='打家劫舍 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='分类讨论 nums[0] · 调用 198 题',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    # 198. 打家劫舍
    def rob1(self, nums: List[int]) -> int:
        f0 = f1 = 0
        for x in nums:
            f0, f1 = f1, max(f1, f0 + x)
        return f1

    def rob(self, nums: List[int]) -> int:
        return max(nums[0] + self.rob1(nums[2:-1]), self.rob1(nums[1:]))
''',
    setup=TRACK,
    call=f'Solution().rob(TList({NUMS}))',
    expect=11,
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='text', fn=_formula, size=27, h=90, lines=2),
    ],
    watch=[('x', 'x', 'orange'), ('f0', 'f0', 'blue'), ('f1', 'f1', 'green')],
    captions={
        'return max(nums[0]': '讨论 ==偷不偷 nums[0]==：两种情况各变成一个「排成一排」的 198 题，调用 `rob1` 解决',
        'f0 = f1 = 0': lambda S, B, ret: (f'`rob1({list(S.nums)})`：' +
                                          ('偷了 `nums[0]`，==nums[1] 和 nums[n-1] 都不能偷==' if _info(S)[0] == 1
                                           else '不偷 `nums[0]`，==nums[1..n-1] 随便选==') + '；`f0 = f1 = 0`'),
        'for x in nums': lambda S, B, ret: (f'下一间房 `x = {S.x}`：偷还是不偷？' if _info(S)[3] is not None else '这一排考虑完了'),
        'f0, f1 = f1': _cap_f,
        'return f1': lambda S, B, ret: (
            f'这一排最多偷 `{ret}` → 情况一共 `{NUMS[0]} + {ret}` = =={NUMS[0] + ret}=='
            if _info(S)[0] == 1 else
            f'这一排最多偷 `{ret}` → 情况二 = =={ret}==；取 `max({CASE1}, {ret})` = =={max(CASE1, ret)}=='),
    },
    cards=dict(
        one_liner='讨论偷不偷 nums[0]，环就拆成了两条链，各调用一次 198 题',
        complexity='时间 `O(n)`，空间 `O(1)`（切片除外）',
        problem=['房屋==围成一圈==，`nums[0]` 和 `nums[n-1]` 相邻；相邻两间不能同时偷',
                 '求今晚最多能偷多少钱',
                 '示例：`[2,3,2]` → `3`，`[1,2,3,1]` → `4`',
                 f'本视频：`{NUMS}` → `11`（第 198 题不成环时是 12）'],
        quote='讨论是否偷 nums[0]：如果偷 nums[0]，那么 nums[1] 和 nums[n−1] 不能偷，问题变成从 nums[2] 到 nums[n−2] 的非环形版本……',
        quote_src='—— 灵茶山艾府题解',
        idea=['偷 `nums[0]`：答案 = `nums[0] + rob1(nums[2..n-2])`',
              '不偷 `nums[0]`：答案 = `rob1(nums[1..n-1])`',
              '`nums[0]` 只有偷与不偷两种选择 → 两种方案取最大值',
              '`rob1` 直接复制 198 题：`f0, f1 = f1, max(f1, f0 + x)`'],
        result=f'情况一 `{CASE1}`，情况二 `{CASE2}` → 答案 `{max(CASE1, CASE2)}` ✓',
        summary=['时间 `O(n)`；切片要额外空间，改成下标循环可做到 `O(1)`',
                 '`nums[2:-1]`：n = 1 时是空列表，rob1 返回 0，答案 `nums[0]`，不用特判',
                 '和「去掉首/尾」的拆法相比，按 `nums[0]` 分类更容易说清为什么不重不漏',
                 '套路：环形问题 → ==分类讨论把环拆成链=='],
    ),
)
