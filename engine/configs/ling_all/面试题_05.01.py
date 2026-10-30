W = 11


def _bits(x):
    return [int(c) for c in format(x & ((1 << W) - 1), '0%db' % W)]


def _inwin(S, k):
    return S['i'] <= W - 1 - k <= S['j']


def _hi(S, k, v):
    return 'yellow' if _inwin(S, k) else None


def _top(S):
    if 'i' not in S:
        return ''
    return f"下标从右往左数，目标区域：第 `{S['i']}` ~ `{S['j']}` 位（黄色），共 `{S['j'] - S['i'] + 1}` 位"


def _mask(S):
    i, j = S['i'], S['j']
    return ((1 << (j - i + 1)) - 1) << i


CONFIG = dict(
    num='面试题 05.01', title='插入', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='先清零再或上 M',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def insertBits(self, n: int, m: int, i: int, j: int) -> int:
        # 清除 n 的从低到高 i~j 位（i 从 0 开始）
        n &= ~(((1 << (j - i + 1)) - 1) << i)
        # 把 m 填入 n
        return n | (m << i)
''',
    call='Solution().insertBits(1131, 19, 2, 6)',
    expect=1103,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var=lambda S: _bits(S['n']), label='n 的二进制（从高位到低位，11 位）', color=_hi, index=False, cell=64, h=150),
        dict(type='array', var=lambda S: _bits(_mask(S)) if 'i' in S else [], label='掩码 ((1 << (j-i+1)) - 1) << i：区间内全是 1', color=_hi, index=False, cell=64, h=150),
        dict(type='array', var=lambda S: _bits(S['m'] << S['i']), label='m << i：m 的最低位对齐到第 i 位', color=_hi, index=False, cell=64, h=150),
        dict(type='text', fn=lambda S: f"`n = {S['n']}`，`m = {S['m']}`，`m << i = {S['m'] << S['i']}`", size=24),
    ],
    watch=['n', 'm', 'i', 'j'],
    captions={
        'n &= ~': lambda S, B, ret: (f"掩码 `{_mask(S):b}` 取反后，第 {S.i}~{S.j} 位是 ==0==、其余全是 1；`n & 取反掩码`：与 0 得 0，与 1 不变 → 区间被清零：`n` 从 {B.n} 变成 =={S.n}=="),
        'return n |': lambda S, B, ret: (f"`m << i = {S.m << S.i}`（`{S.m:b}` 左移 {S.i} 位）；n 的区间已是 0，或运算就把 m 原样填进去 → ==`{S.n | (S.m << S.i)}`=="),
    },
    cards=dict(
        one_liner='先把 n 的 i~j 位清零，再把 m 左移 i 位或进去',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['把 `M` 的二进制==插入==到 `N` 的第 `i ~ j` 位（从 0 开始），不足补 0',
                 '题目示例：`N = 1024`，`M = 19`，`i = 2`，`j = 6` → `1100`',
                 '本视频换成 `N = 1131`（`10001101011`），区间里原来有 1，更能看清清零这一步',
                 '结果 `1103`（`10001001111`）'],
        quote='把 n 的二进制从低到高第 i 到 j 位清除（置为 0）……任何比特 AND 0 都等于 0，AND 1 都不变。',
        quote_src='—— 灵茶山艾府题解',
        idea=['构造掩码：`1 << (j-i+1)` 再减一得到连续的 1，左移 `i` 位对齐区间',
              '取反后与 n 相与：区间被清零，其他位不变',
              '`m << i` 让 m 最低位落在第 `i` 位，和 n 做或运算即可填入'],
        result='`n` 的 2~6 位被换成 `10011`，返回 `1103` ✓',
        after=[dict(heading='掩码怎么造（以 i=3, j=4 为例）', lines=['① `1 << (j-i+1)` = `100`','② 减一得 `11`，即宽度为 2 的连续 1','③ 左移 `i` 位得 `11000`，正好盖住第 3~4 位','④ 取反得 `...1100111`，和 n 相与就清掉这两位'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错：区间宽度是 `j - i + 1`，不是 `j - i`',
                 '易错：必须先清零再或；直接或会让原来的 1 残留',
                 '同一套「掩码清零 + 或填入」可用于任何定位修改某段比特'],
    ),
)
