N0, BL = 10, [3, 5, 7, 8]


def _col(S, i, v):
    vc = N0 - len(BL)
    pd = S.get('self.pos_dict') or {}
    if i in BL:
        return 'red'
    if i in pd.values():
        return 'green'
    return None


CONFIG = dict(
    num=710, title='黑名单中的随机数', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='黑名单映射到尾部白名单',
    tags=['随机化'],
    code='''
import random

class Solution(object):

    def __init__(self, N, blacklist):
        black_set = set(blacklist)
        self.pos_dict = {}
        self.valid_cnt = N - len(blacklist)
        now = self.valid_cnt
        for num in blacklist:
            if num >= self.valid_cnt:
                continue
            else:
                while now in black_set:
                    now += 1
                self.pos_dict[num] = now
                now += 1

    def pick(self):
        res = random.randint(0, self.valid_cnt - 1)
        return self.pos_dict.get(res, res)
''',
    setup='import random\nrandom.seed(5)',
    call='''s = Solution(10, [3, 5, 7, 8])
out = []
out.append(s.pick())
out.append(s.pick())
out.append(s.pick())
out.append(s.pick())
out''',
    expect=[4, 2, 9, 2],
    views=[
        dict(type='array', var=lambda S: list(range(N0)), label='0 ~ N-1（红 = 黑名单，绿 = 被借来顶替的数；框 = 前 N-k 个）',
             cell=84, h=190, pointers={'now': 'blue'},
             color=_col,
             window=(lambda S: 0, lambda S: N0 - len(BL) - 1)),
        dict(type='map', var='self.pos_dict', label='pos_dict（黑名单数 → 顶替它的白名单数）', fmt=lambda k, v: f'{k} → {v}', h=130, font=34),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=['N', 'valid_cnt', 'now', 'num', 'res'],
    skip=['import random'],
    captions={
        'black_set = set(blacklist)': '黑名单放进集合 `black_set`，查询是否在黑名单是 `O(1)`',
        'self.pos_dict = {}': '`pos_dict`：前半段里的黑名单数 → 后半段里的白名单数',
        'self.valid_cnt = N - len(blacklist)': '白名单一共 `N - k` = `{self.valid_cnt}` 个：只在 `0 ~ {self.valid_cnt - 1}` 里随机，一定不超界',
        'now = self.valid_cnt': '`now` 从 `{now}` 开始，扫描后半段 `[{self.valid_cnt}, N)` 找不在黑名单的数',
        'for num in blacklist': lambda S, B, ret: ('处理黑名单里的 `{}`'.format(S.num) if B.get('num') != S.num or 'num' not in B else '黑名单都处理完了'),
        'if num >= self.valid_cnt': lambda S, B, ret: ('`{} >= {}`：它在后半段，本来就抽不到，不用管'.format(S.num, S['self.valid_cnt']) if S.num >= S['self.valid_cnt']
                                                       else '`{} < {}`：它在前半段，随机会抽到它 → 要找个替身'.format(S.num, S['self.valid_cnt'])),
        'continue': '跳过',
        'while now in black_set': lambda S, B, ret: ('`now = {}` 也在黑名单里，不能当替身，往后找'.format(S.now) if S.now in S.black_set
                                                     else '`now = {}` 不在黑名单：可以当替身'.format(S.now)),
        'now += 1': lambda S, B, ret: '`now` 后移到 `{}`'.format(S.now),
        'self.pos_dict[num] = now': '建立映射：抽到 `{num}` 时改返回 `{now}`',
        'res = random.randint(0, self.valid_cnt - 1)': '在 `0 ~ {self.valid_cnt - 1}` 里等概率随机一个 `res = {res}`',
        'return self.pos_dict.get(res, res)': '`res = {res}` 在映射里就返回替身，否则返回自己 → 返回 `{ret}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='前半段的黑名单数，找后半段的白名单数顶替',
        complexity='构造 `O(k)`，`pick` `O(1)`，空间 `O(k)`（k = 黑名单长度）',
        problem=['给定 `N` 和黑名单 `blacklist`',
                 '`pick()` 从 `[0, N-1]` 中不在黑名单里的数里==等概率==随机返回一个',
                 '示例：`N = 10`，黑名单 `[3, 5, 7, 8]`，白名单是 `0 1 2 4 6 9`'],
        quote='若0到n - 1 - k这n - k个数中有p个数是黑名单中的数，那么反过来，从n - k到n - 1这k个数中就有k - p个数在黑名单中，从而得知恰好也是p个数不在黑名单中。',
        quote_src='—— yiduobo 题解',
        idea=['只在前 `N-k` 个数里随机：个数刚好等于白名单大小',
              '前半段里有 p 个黑名单数，后半段里恰好有 p 个白名单数',
              '一一对应：抽到黑名单数就换成对应的白名单数，返回时概率仍然相等'],
        summary=['构造 `O(k)`，每次 `pick` 只调用一次随机数，`O(1)`',
                 '易错：只给 `< N-k` 的黑名单数建映射；`now` 要跳过黑名单里的数',
                 '原文用了 `random` 却没写 import，演示里补了 `import random`',
                 '同类随机题：381、497、478'],
    ),
)
