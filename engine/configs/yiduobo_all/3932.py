def _pv(S):
    try:
        return S['v'] ** S['k']
    except Exception:
        return None


def _in_p(S):
    return 'x' in S.get('_inner', {})


def _txt(S):
    if 'v' not in S or 'l' not in S:
        return ''
    if _in_p(S):
        return f"进入 `p(x)`：循环乘 `k = {S['k']}` 次，算出 `x^k`"
    pv = _pv(S)
    return f"`v = {S['v']}`：`v^{S['k']} = {pv}`，区间 `[{S['l']}, {S['r']}]`，已数到 =={S.get('res', 0)}== 个"


CONFIG = dict(
    num=3932, title='统计区间内的完全 K 次幂数量', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举底数 v，按 v^k 与区间比较计数',
    tags=[],
    code='''
class Solution(object):
    def countKthRoots(self, l, r, k):
        
        if k == 1:
            return r - l + 1
        
        def p(x):
            v = 1
            for _ in range(k):
                v *= x
            return v

        v = 0
        res = 0
        while p(v) < l:
            v += 1
        while p(v) <= r:
            res += 1
            v += 1
        
        return res
''',
    call='Solution().countKthRoots(8, 30, 2)',
    expect=3,
    views=[
        dict(type='text', size=36, h=130, fn=_txt),
        dict(type='text', size=34, h=130, fn=lambda S: (
            f"第一段：找首个 `v^k ≥ l`" if S.get('_line') in (15, 16) else
            f"第二段：`v^k ≤ r` 就计数" if S.get('_line') in (17, 18, 19) else '')),
    ],
    watch=['l', 'r', 'k', 'v', ('res', 'res', 'green')],
    skip=['v = 1', 'v *= x', 'for _ in range(k)'],
    captions={
        'if k == 1': '`k = {k}`：k 为 1 时每个数都是自己的 1 次幂，答案直接是 `r - l + 1`；这里 k = 2，往下走',
        'v = 0': '`v` 从 0 开始，枚举底数',
        'res = 0': '`res` 记录完全 k 次幂的个数',
        'while p(v) < l': lambda S, B, ret: f'`p({B.v}) = {_pv(B)}`，和 `l = {B.l}` 比：{"==小于 l，还没进入区间，v 再加一==" if _pv(B) < B.l else "==不小于 l，找到首个落进区间的 v=="}',
        'v += 1': '`v` → {v}',
        'while p(v) <= r': lambda S, B, ret: f'`p({B.v}) = {_pv(B)}`，和 `r = {B.r}` 比：{"==≤ r，在区间里，计一个==" if _pv(B) <= B.r else "==超过 r，后面的更大，停止=="}',
        'return v': '`p` 返回 `x^k = {ret}`',
        'res += 1': '`v^k = {v * v}` 落在 `[l, r]` 内，`res` → {res}',
        'return res': '一共 =={res}== 个完全 k 次幂',
        'return r - l + 1': 'k = 1：直接返回 `r - l + 1`',
    },
    cards=dict(
        one_liner='k 次根号下 r 个数量级很小，直接从小到大枚举底数 v',
        complexity='时间 `O(r^(1/k) · k)`，空间 `O(1)`',
        problem=['给 `l`、`r`、`k`，数 `[l, r]` 内满足 `y = x^k` 的整数 `y` 个数',
                 '示例：`l=8, r=30, k=2` → `3`（9、16、25）'],
        quote='可以使用一个变量v从0开始向上枚举，直到v^k >= l的元素v。接下来再从v开始向上枚举，直到v^k > r为止',
        quote_src='—— yiduobo 题解原文',
        idea=['`k = 1` 单独处理：答案 `r − l + 1`',
              '`k ≥ 2` 时底数最多 `10^(9/k)` 量级，直接枚举 v 就够快',
              '先跳过 `v^k < l` 的，再数 `v^k ≤ r` 的，边枚举边计数'],
        summary=['时间 `O(r^(1/k) · k)`，`k = 2` 时约 3 万次，空间 `O(1)`',
                 '易错点：`k = 1` 要单独判断，否则要枚举到 `10^9`',
                 '`p(x)` 用循环乘出 `x^k`，不会有浮点误差',
                 '对比灵神：他用 `n^(1/k)` 直接开根 + 前缀差，yiduobo 用枚举'],
    ),
)
