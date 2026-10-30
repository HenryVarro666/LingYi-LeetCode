CONFIG = dict(
    num=2522, title='将字符串分割成值不超过 K 的子字符串', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='划分型贪心 · 每段尽量长',
    tags=['灵神题单', '贪心算法', '难度分 1605'],
    code='''
class Solution:
    def minimumPartition(self, s: str, k: int) -> int:
        ans, x = 1, 0
        for v in map(int, s):
            if v > k: return -1
            x = x * 10 + v
            if x > k:
                ans += 1
                x = v
        return ans
''',
    call="Solution().minimumPartition('165462', 60)",
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"当前这一段的值 `x = {S['x']}`，上限 `k = {S['k']}`" if 'x' in S else ''), size=34, h=90),
        dict(type='string', var='s', h=300, label='s（当前这一段高亮）',
             color=lambda S, i, v: 'blue' if _inseg(S, i) else None,
             dim=lambda S, i, v: 'ans' in S and _pos(S) is not None and i > _pos(S)),
    ],
    watch=[('v', 'v', 'blue'), ('x', 'x', 'pink'), ('k', 'k'), ('ans', 'ans', 'green')],
    captions={
        'ans, x = 1': '至少有 1 段，当前这一段的值 `x = 0`',
        'for v in map': lambda S, B, r: ('所有数位都处理完，结束循环' if B.get('v') == S.get('v') and B.get('x') == S.get('x') else f"取下一个数位 `v = {S.v}`"),
        'if v > k': '`v = {v}`，`k = {k}`：{\'单个数位就超过 k，怎么分都不行 → 返回 -1\' if v > k else \'单个数位不超过 k，至少能单独成段\'}',
        'x = x * 10 + v': '把 `{v}` 接在当前段末尾：`x = {B.x}×10 + {v}` = =={x}==',
        'if x > k': '`x = {x}` {\'>\' if x > k else \'<=\'} `k = {k}` → {\'接上去超了，这一段到此为止\' if x > k else \'没超，这一段还能更长（越长越好）\'}',
        'ans += 1': '在 `{v}` 前面切开，新开一段：`ans` = =={ans}==',
        'x = v': '新的一段从 `{v}` 开始：`x = {x}`',
        'return ans': '一共 `{ans}` 段',
    },
    cards=dict(
        one_liner='第一段越长越好：给后面留得越短，答案不会变大',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 每位是 1~9，把它分成若干子串，每个子串的数值 `≤ k`',
                 '返回最少的段数；分不了返回 `-1`',
                 '示例：`s = "165462", k = 60` → `4`（16 | 54 | 6 | 2）'],
        quote='如果给后面留下的字符串越短，答案显然不会变大，因此第一个字符串越长越好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左往右一位位接：能接就接，接不下才切一刀',
              '`x` 保存当前段的值，超过 `k` 就把当前数位作为新一段的开头',
              '单个数位 `> k` 时无解，直接返回 `-1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ans` 从 1 开始（至少一段）',
                 '易错：切开后 `x = v`，不是 0',
                 '同类：划分型贪心，每段尽量长'],
    ),
)


def _segs(S):
    """按代码规则重放，得到每个下标所属段的起点；返回 (起点列表)"""
    s, k = S['s'], S['k']
    starts, x, st = [], 0, 0
    for i, ch in enumerate(s):
        v = int(ch)
        x2 = x * 10 + v
        if x2 > k and i > 0:
            st, x2 = i, v
        starts.append(st)
        x = x2
    return starts


def _pos(S):
    """当前处理到的下标：v 前缀匹配无法唯一，用 (v, ans, x) 对重放结果找"""
    if 'v' not in S or 'x' not in S:
        return None
    s, k = S['s'], S['k']
    ans, x = 1, 0
    ln = S['_line']
    cands = []
    for i, ch in enumerate(s):
        v = int(ch)
        pre = (v, ans, x)
        x2 = x * 10 + v
        a2 = ans
        mid = (v, ans, x2)
        if x2 > k:
            a2, x2 = ans + 1, v
        post = (v, a2, x2)
        cut = (v, ans + 1, x * 10 + v) if x2 != x * 10 + v or a2 != ans else mid
        cands.append((pre, mid, cut, post))
        ans, x = a2, x2
    t = (S['v'], S['ans'], S['x'])
    kk = 0 if ln <= 5 else (1 if ln <= 7 else (2 if ln == 8 else 3))
    for i, c in enumerate(cands):
        if c[kk] == t:
            return i
    return None


def _inseg(S, i):
    p = _pos(S)
    if p is None or i > p:
        return False
    st = _segs(S)
    return st[i] == st[p]
