
SETUP = """
class _Snap(list):
    pos = -1


class _Track(list):
    pos = -1

    def __iter__(self):
        for i in range(len(self)):
            self.pos = i
            yield self[i]
        self.pos = len(self)

    def __deepcopy__(self, memo):
        c = _Snap(list.__iter__(self))
        c.pos = self.pos
        return c
"""
NUMS = [5, 2, 7, 4, 4, 1, 10]
K = 3


def _cur(S):
    nums = S.get('nums')
    if nums is None or 'length' not in S:
        return None
    p = getattr(nums, 'pos', None)
    if p is None or p < 0 or p >= len(nums):
        return None
    return p


def _wl(S):
    p = _cur(S)
    if p is None:
        return None
    return p - S['length'] + 1


def _color(S, i, v):
    p = _cur(S)
    if p is None or 'length' not in S:
        return None
    if p - S['length'] < i <= p:
        return 'green' if S['s'] == S['r'] and S['length'] > 1 else 'yellow'
    return None


def _mods(S):
    if 'k' not in S:
        return None
    p = _cur(S)
    cells = []
    for i, x in enumerate(S['nums']):
        m = x % S['k']
        cells.append(f'==[{m}]==' if i == p else f'{m}')
    return '各数对 `k = ' + str(S['k']) + '` 取模：' + ' '.join(cells)


def _info(S):
    if 'r' not in S or S['r'] == -1:
        return '`res` 是目前最长的有韧性子数组长度，至少为 1'
    ok = '==满足==' if (S['s'] == S['r'] and S['length'] > 1) else '不满足'
    return f'当前段：余数 `r = {S["r"]}`，长度 `length = {S["length"]}`，和模 k `s = {S["s"]}` → {ok} `s == r`'


CONFIG = dict(
    num=4075, title='最长有韧性的子数组I', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按余数分段 · 一趟遍历',
    tags=[],
    code='''
class Solution(object):
    def resilientSubarray(self, nums, k):
        
        res = 1
        r = -1
        s = 0
        length = 0
        for v in nums:
            v %= k
            if v == r:
                s += v
                length += 1
                s %= k
                if s == v:
                    res = max(res, length)
            else:
                s = v
                length = 1
                r = v

        
        return res
''',
    setup=SETUP,
    call='Solution().resilientSubarray(_Track([5, 2, 7, 4, 4, 1, 10]), 3)',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（框内 = 当前同余数段；绿 = 满足 s == r）', cell=84, h=210,
             color=_color, window=(_wl, lambda S: _cur(S))),
        dict(type='text', h=80, size=28, fn=_mods),
        dict(type='text', h=110, size=30, fn=_info),
    ],
    watch=['v', ('r', 'r', 'blue'), ('s', 's', 'orange'), ('length', 'length', 'pink'), ('res', 'res', 'green')],
    skip=['res = 1', 'r = -1', 's = 0', 'length = 0', 's += v', 'length += 1', 's = v', 'length = 1', 'r = v'],
    captions={
        'for v in nums': lambda S, B, ret: ('遍历结束' if _cur(S) is None and 'length' in B and B.get('length') == S.length and 'v' in B and B.v == S.v and S['nums'].pos >= len(S['nums'])
                                              else f'取 `nums[{S["nums"].pos}]`，下面先对 k 取模'),
        'v %= k': '余数 `v = {v}`，当前段的余数 `r = {r}`',
        'if v == r': lambda S, B, ret: (f'`v = {S.v}` 和 `r = {S.r}` 相同 → ==延长当前段=='
                                        if S.v == S.r else f'`v = {S.v}` ≠ `r = {S.r}` → 换了一种余数，==开新的一段=='),
        'else': '换新段：`s = v = {v}`，`length = 1`，`r = {v}`',
        's %= k': '段内和 `s` 对 `k` 取模：`s = {s}`（段长 `length = {length}`）',
        'if s == v': lambda S, B, ret: (f'`s = {S.s} == v = {S.v}`：删掉任意一个数，剩下的和都被 k 整除 → ==有韧性=='
                                        if S.s == S.v else f'`s = {S.s} ≠ v = {S.v}`：整段不满足，但后面还可能再满足'),
        'res = max(res, length)': '`res = max({B.res}, {length}) = {res}`',
        'return res': '最长有韧性子数组长度为 `{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='有韧性 ⇔ 全是同一个余数，且整段的和模 k 等于它',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子数组里每个元素删掉后，剩余元素的和都能被 `k` 整除，就称它有韧性（长度 1 总是有韧性）',
                 '求最长的有韧性子数组长度',
                 '本视频：`nums = [5,2,7,4,4,1,10]`，`k = 3` → `4`（`[7,4,4,1]`，和 16，删 7 剩 9）'],
        quote='如果将这个子数组中的所有元素都相对k取模，那么子数组中所有的元素将全部是同一种元素，而这些元素之和模k的结果也刚好就是这种元素自身。',
        quote_src='—— yiduobo 题解原文',
        idea=['设和为 `s`，任意两个元素 `a、b` 都有 `s − a ≡ s − b ≡ 0`，所以 `a ≡ b (mod k)`',
              '于是有韧性子数组里余数全相同，且 `s mod k` 就等于这个余数',
              '把数组按相同余数分段，段内一路累加，`s == v` 时更新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`，本题 n 较小，同一份代码也能过 II',
                 '易错：单个元素总是有韧性，所以 `res` 初值是 1',
                 '易错：`s` 每步取模后才和 `v` 比较；余数中断（`v != r`）要重新开段',
                 '`r` 初值 -1，保证第一个元素一定开新段',
                 '原文已是 Python 3 可运行写法，代码未改动；视频里为了画出当前位置，用 list 子类包了一下输入（演示用）'],
    ),
)
