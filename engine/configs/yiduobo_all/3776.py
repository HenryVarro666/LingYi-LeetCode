def _color(S, i, v):
    if 'p' not in S or S['p'] >= len(S['balance']):
        return None
    if i == S['p']:
        return 'pink'
    if 'left' in S and i == S['left']:
        return 'blue'
    if 'right' in S and i == S['right']:
        return 'orange'
    return None


def _txt(S):
    if 'v' not in S:
        return ''
    s = f"欠款 `v` = =={S['v']}==，已花 `res` = =={S['res']}=="
    if 'dis' in S:
        s += f"，当前距离 `dis` = {S['dis']}"
    return s


CONFIG = dict(
    num=3776, title='使循环数组余额非负的最少移动次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='左右指针 · 向两侧扩张',
    tags=['灵神题单', '难度分 1740'],
    code='''
class Solution(object):
    def minMoves(self, balance):

        if sum(balance) < 0:
            return -1

        p = 0
        n = len(balance)
        while p < n and balance[p] >= 0:
            p += 1

        if p == n:
            return 0

        left = (p - 1 + n) % n
        right = (p + 1) % n

        v = -balance[p]
        dis = 1
        res = 0
        while v:
            if balance[left] + balance[right] >= v:
                res += v * dis
                break
            else:
                res += (balance[left] + balance[right]) * dis
                v -= balance[left]
                v -= balance[right]
                left = (left - 1 + n) % n
                right = (right + 1) % n
                dis += 1

        return res
''',
    call='Solution().minMoves([3,1,-6,0,2])',
    expect=11,
    views=[
        dict(type='text', fn=_txt, size=30, h=70),
        dict(type='array', var='balance', pointers={'p': 'pink', 'left': 'blue', 'right': 'orange'}, color=_color,
             h=330, cell=110, label='balance（粉 = 负数 p，蓝 = left，橙 = right，环形）'),
    ],
    watch=[('p', 'p', 'pink'), ('left', 'left', 'blue'), ('right', 'right', 'orange'), ('v', 'v', 'orange'),
           ('dis', 'dis', 'cyan'), ('res', 'res', 'green')],
    captions={
        'sum(balance) < 0': lambda S, B, r: (f'总和 `{sum(S.balance)}` < 0：负的人负得太多，别人全给也不够 → -1' if sum(S.balance) < 0
                                             else f'总和 `{sum(S.balance)}` ≥ 0：够补，继续'),
        'while p < n': lambda S, B, r: (f'`balance[{S.p}] = {S.balance[S.p]}` 不是负数，往后找' if S.p < len(S.balance) and S.balance[S.p] >= 0
                                        else ('找到负数，`p` 停在 {}'.format(S.p) if S.p < len(S.balance) else '一路没遇到负数')),
        'p += 1': '`p` → {p}',
        'if p == n': lambda S, B, r: ('没有负数，无需操作 → 0' if S.p == len(S.balance) else '有负数，继续'),
        'left = (p': '`left` 是 p 左边相邻的人（环形，要 `+ n` 再取模）：`left = {left}`',
        'right = (p': '`right` 是 p 右边相邻的人：`right = {right}`',
        'v = -balance': '`p` 欠 `{v}`，需要别人给 `{v}` 个单位：`v = {v}`',
        'dis = 1': '最近的人距离是 `1`，每个单位转 `1` 次',
        'while v': lambda S, B, r: (f'还欠 `{S.v}`，继续' if S.v else '不欠了，结束'),
        'if balance[left] + balance[right] >= v': lambda S, B, r: (
            f'`balance[{S.left}] + balance[{S.right}] = {S.balance[S.left] + S.balance[S.right]}` ≥ `v = {S.v}` → 足够，只给 `v` 个'
            if S.balance[S.left] + S.balance[S.right] >= S.v else
            f'`balance[{S.left}] + balance[{S.right}] = {S.balance[S.left] + S.balance[S.right]}` < `v = {S.v}` → 不够，两人全给'),
        'res += v * dis': '只需 `{v}` 个单位，每个走 `{dis}` 步：`res` = {B.res} + {v}×{dis} = =={res}==',
        'break': '欠款补齐，跳出循环',
        'res += (balance': '两人全给：`res` = {B.res} + {balance[left] + balance[right]}×{dis} = =={res}==',
        'v -= balance[left]': '欠款减去左边给的：`v` = {v}',
        'v -= balance[right]': '再减去右边给的：`v` = =={v}==',
        'left = (left': '`left` 再往左一格 → {left}',
        'right = (right': '`right` 再往右一格 → {right}',
        'dis += 1': '更远一圈，每个单位多走一步：`dis` = {dis}',
        'return res': '最少移动 `{res}` 次',
    },
    cards=dict(
        one_liner='先让离负数最近的人给钱，左右各一格向外扩',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['环形数组，`balance[i]` 是净余额，一次可以向左或右邻居转 1 个单位',
                 '至多一个人为负，求让所有人非负的最少移动次数，不可能返回 `-1`',
                 '本视频：`[3,1,-6,0,2]` → `11`'],
        quote='为了使得移动的次数最少，就应该尽可能先移动与其距离最近的人的余额。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理边界：总和为负返回 `-1`，没有负数返回 `0`',
              '`p` 是负数的位置，`left`、`right` 从它两侧相邻处出发',
              '够就只给 `v` 个并停下；不够就两人全给，`left`、`right` 各往外挪一格，`dis` 加 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '环形取下标：`(left - 1 + n) % n` 与 `(right + 1) % n`',
                 '判断是否足够用 `>= v`，等于时恰好补平',
                 '原文本身是 Python 3 可运行的写法，只去掉了空行和多余缩进'],
    ),
)
