def _dist(S, i):
    """环上 i 到 neg_idx 的距离（取较短一边）"""
    n = len(S['balance'])
    d = (i - S['neg_idx']) % n
    return min(d, n - d)


def _color(S, i, v):
    if 'neg_idx' not in S or S['neg_idx'] < 0:
        return None
    if i == S['neg_idx']:
        return 'pink'
    if 'dis' not in S:
        return None
    d = _dist(S, i)
    if d == S['dis']:
        return 'blue'
    if d < S['dis']:
        return 'green'
    return None


def _dim(S, i, v):
    return 'dis' in S and 'neg_idx' in S and _dist(S, i) > S['dis']


def _txt(S):
    if 'need' not in S:
        return ''
    s = f"还缺 `need` = =={S['need']}==，已用 `ans` = =={S['ans']}== 次移动"
    if 'dis' in S and 's' in S:
        s += f"  ｜ 距离 {S['dis']} 的两个数之和 `s` = {S['s']}"
    return s


CONFIG = dict(
    num=3776, title='使循环数组余额非负的最少移动次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='从负数向两边由近到远',
    tags=['灵神题单', '难度分 1740'],
    code='''
class Solution:
    def minMoves(self, balance: List[int]) -> int:
        if sum(balance) < 0:  # 总和必须非负
            return -1

        neg_idx = next((i for i, x in enumerate(balance) if x < 0), -1)
        if neg_idx < 0:  # 没有负数，无需操作
            return 0

        n = len(balance)
        need = -balance[neg_idx]
        ans = 0
        for dis in count(1):  # 把与 neg_idx 相距 dis 的数移到 neg_idx
            s = balance[neg_idx - dis] + balance[(neg_idx + dis) % n]
            if s >= need:
                ans += need * dis  # need 个 1 移动 dis 次
                return ans
            ans += s * dis  # s 个 1 移动 dis 次
            need -= s
''',
    setup='from itertools import count',
    call='Solution().minMoves([3,1,-6,0,2])',
    expect=11,
    views=[
        dict(type='text', fn=_txt, size=30, h=70),
        dict(type='array', var='balance', pointers={'neg_idx': 'pink'}, color=_color, dim=_dim, h=330, cell=110,
             label='balance（粉 = 负数位置，蓝 = 这一圈要搬的数，绿 = 已搬过）'),
    ],
    watch=[('neg_idx', 'neg_idx', 'pink'), ('need', 'need', 'orange'), ('dis', 'dis', 'blue'), 's', ('ans', 'ans', 'green')],
    captions={
        'sum(balance) < 0': lambda S, B, r: (f'总和 `{sum(S.balance)}` < 0：全部给它也补不平 → 无解' if sum(S.balance) < 0
                                             else f'总和 `{sum(S.balance)}` ≥ 0：钱够，有解'),
        'neg_idx = next': lambda S, B, r: f'找到唯一的负数下标 `neg_idx = {S.neg_idx}`（题目保证至多一个负数）',
        'neg_idx < 0': lambda S, B, r: '有负数，继续' if S.neg_idx >= 0 else '没有负数，无需操作 → 返回 0',
        'need = ': '它欠 `{need}`，需要别人搬 `{need}` 个 1 过来：`need = {need}`',
        'for dis in count': '==离得越近每个 1 花的步数越少==：先搬距离 `{dis}` 的两个数',
        's = balance': '距离 `{dis}` 的两个数：`balance[{(neg_idx - dis) % n}] + balance[{(neg_idx + dis) % n}]` = ==`{s}`==',
        's >= need': lambda S, B, r: (f'`s = {S.s} ≥ need = {S.need}`：这一圈就够了，只搬 `need` 个 → 成立'
                                      if S.s >= S.need else f'`s = {S.s} < need = {S.need}`：不够，这一圈全搬，再往外找'),
        'ans += need * dis': '只需 `{need}` 个 1，每个走 `{dis}` 步：`ans` = {B.ans} + {need}×{dis} = =={ans}==',
        'return ans': '欠的补齐了，最少移动 `{ans}` 次',
        'ans += s * dis': '`{s}` 个 1 各走 `{dis}` 步：`ans` = {B.ans} + {s}×{dis} = =={ans}==',
        'need -= s': '欠款减少 `{s}`：`need` = {B.need} − {s} = =={need}==',
        'return -1': '返回 -1',
        'return 0': '返回 0',
    },
    cards=dict(
        one_liner='负数只有一个：由近到远，先搬近的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['环形数组 `balance`，每次可以把 1 个单位转给左/右邻居',
                 '至多有一个负数，求让所有数非负的最少移动次数，不可能返回 `-1`',
                 '示例：`[1,2,-5,2]` → `6`；本视频用 `[3,1,-6,0,2]` → `11`'],
        quote='贪心地，移动离 i 近的数，操作次数更少：先把离 i 最近的 balance[i-1] 和 balance[i+1] 移到 i，每个 1 移动 1 次；再把离 i 为 2 的…',
        quote_src='—— 灵茶山艾府题解',
        idea=['只有一个负数，别人搬 1 个单位过去，花的步数就是==环上的距离==',
              '距离越近越省，所以按 `dis = 1, 2, 3...` 一圈一圈往外搬',
              '某一圈的和 `s ≥ need`，只搬 `need` 个，结束；否则整圈搬完继续'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先判总和 `< 0` 返回 `-1`，再判无负数返回 `0`',
                 '右边下标要 `% n` 绕回来；左边 `neg_idx - dis` 靠 Python 负下标自动绕回',
                 '`count` 来自 itertools，视频里在 setup 中导入'],
    ),
)
