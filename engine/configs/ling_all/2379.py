# blocks 用一个“带下标的字符串”传入：行为与 str 完全相同，只是遍历出的字符记得自己的下标，方便画窗口
SETUP = '''
class _Ch(str):
    pass

class _Blocks(str):
    def __new__(cls, s, off=0):
        o = super().__new__(cls, s)
        o.off = off
        return o
    def __getitem__(self, key):
        r = str.__getitem__(self, key)
        if isinstance(key, slice):
            start = key.start or 0
            return _Blocks(r, self.off + start)
        return r
    def __iter__(self):
        for j, c in enumerate(str.__iter__(self)):
            ch = _Ch(c)
            ch.idx = self.off + j
            yield ch
'''


def _r(S):
    """index of in_ (window right end) or None"""
    c = S.get('in_')
    if c is not None and hasattr(c, 'idx'):
        return c.idx
    if 'ans' in S and 'in_' not in S:
        return S['k'] - 1
    return None


def _l(S):
    r = _r(S)
    return None if r is None else r - S['k'] + 1


def _out(S):
    c = S.get('out')
    return getattr(c, 'idx', None) if c is not None else None


CONFIG = dict(
    num=2379, title='得到 K 个黑块的最少涂色次数', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长滑窗 · 统计白块',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1360'],
    setup=SETUP,
    code='''
class Solution:
    def minimumRecolors(self, blocks: str, k: int) -> int:
        ans = cnt_w = blocks[:k].count('W')
        for in_, out in zip(blocks[k:], blocks):
            cnt_w += (in_ == 'W') - (out == 'W')
            ans = min(ans, cnt_w)
        return ans
''',
    call='Solution().minimumRecolors(_Blocks("WBBWWBBWBW"), 4)',
    expect=1,
    views=[
        dict(type='string', var=lambda S: str(S['blocks']) if 'blocks' in S else None,
             label='blocks（框 = 长 k 的窗口；白块 W 是要涂的）', cell=96, h=270,
             pointers={_r: 'blue', _out: 'pink'}, pointer_labels={_r: 'in_', _out: 'out'}, window=(_l, _r),
             color=lambda S, i, v: 'yellow' if v == 'W' else None),
        dict(type='text', h=110, size=32,
             fn=lambda S: (f"窗口 `{str(S['blocks'])[_l(S):_r(S) + 1]}` 里白块 `cnt_w = {S['cnt_w']}`，最少 `ans = {S['ans']}`"
                           if _r(S) is not None and 'cnt_w' in S else '窗口里有几个 ==W==，就要涂几次')),
    ],
    watch=[('in_', lambda S: str(S['in_']) if 'in_' in S else None, 'blue'),
           ('out', lambda S: str(S['out']) if 'out' in S else None, 'pink'),
           ('cnt_w', 'cnt_w', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt_w = blocks[:k]': '初始窗口是前 k 个 `{str(blocks[:k])!r}`：白块 `cnt_w = {cnt_w}`，`ans` 也初始化为它',
        'for in_, out in zip': lambda S, B, r: (f'窗口右移：`blocks[{S.in_.idx}] = {str(S.in_)!r}` 进入，`blocks[{S.out.idx}] = {str(S.out)!r}` 离开'
                                                if 'in_' in S and ('in_' not in B or S.in_.idx != B.in_.idx) else '窗口已到末尾'),
        'cnt_w += (in_': lambda S, B, r: (f"`({str(S.in_)!r} == 'W') − ({str(S.out)!r} == 'W')` = `{int(S.in_ == 'W')} − {int(S.out == 'W')}`"
                                          f" → `cnt_w = {S.cnt_w}`"),
        'ans = min(ans, cnt_w)': lambda S, B, r: (f'白块更少了！`ans = min({B.ans}, {S.cnt_w}) = {S.ans}`' if S.ans < B.ans
                                                  else f'`ans = min({B.ans}, {S.cnt_w}) = {S.ans}`，不变'),
        'return ans': '最少涂 `{ans}` 次',
    },
    cards=dict(
        one_liner='要涂的次数 = 窗口里的白块数，求它的最小值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`blocks` 由 `W`（白）和 `B`（黑）组成，每次可把一个白块涂黑',
                 '求得到==连续 k 个黑块==的最少操作次数',
                 '示例：`"WBBWWBBWBW", k = 7` → `3`；本视频 `k = 4` → `1`'],
        quote='本题可以看成一个长度固定为 k 的滑动窗口，我们需要计算窗口内 W 的出现次数的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['初始窗口是长为 k 的前缀，`cnt_w` = 其中 W 的个数',
              '`zip(blocks[k:], blocks)` 同时拿到==进入的 in_ 和离开的 out==',
              '布尔值当整数用：`cnt_w += (in_ == W) − (out == W)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`zip` 会在较短的 `blocks[k:]` 用完时停下，正好对齐',
                 '题解还给了 `s[i] & 1` 的无分支写法：W 的 ASCII 最低位是 1，B 是 0',
                 '动画里 blocks 用带下标的字符串传入以便画窗口，代码与原文一致'],
    ),
)
