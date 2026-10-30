X0, Y0 = 29, 6
W = 5  # 显示的二进制位数


def _bits(v):
    return [int(c) for c in format(v, f'0{W}b')]


def _low(v):
    """最低位 1 在显示数组里的下标"""
    if not v:
        return None
    return W - 1 - ((v & -v).bit_length() - 1)


def _info(S):
    if 'res' not in S and S.get('_line') != 3:
        return '两个数的二进制==不同位置的数目==：先异或，再数 1 的个数'
    x = S['x']
    return f"`x = {x}`（`{x:0{W}b}`）还剩 `{bin(x).count('1')}` 个 1；已数 `res = {S.get('res', 0)}`"


CONFIG = dict(
    num=461, title='汉明距离', difficulty='Easy', category='技巧',
    author='yiduobo', technique='异或 + x & (x-1) 逐个消掉最低位的 1',
    tags=['热题173'],
    code='''
class Solution(object):
    def hammingDistance(self, x, y):
        x ^= y
        res = 0
        while x:
            x &= x - 1
            res += 1
        return res
''',
    call=f'Solution().hammingDistance({X0}, {Y0})',
    expect=4,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var=lambda S: _bits(X0), label=f'原来的 x = {X0}', cell=90, h=140, index=False,
             color=lambda S, i, v: 'pink' if v != _bits(Y0)[i] else None),
        dict(type='array', var=lambda S: _bits(Y0), label=f'y = {Y0}（粉 = 和 x 不同的位）', cell=90, h=140, index=False,
             color=lambda S, i, v: 'pink' if v != _bits(X0)[i] else None),
        dict(type='array', var=lambda S: _bits(S['x']) if 'res' in S or S.get('_line') == 3 else None,
             label='当前 x（异或结果；粉 = 最低位的 1，下一步要消掉它）', cell=90, h=140, index=False,
             color=lambda S, i, v: 'pink' if i == _low(S['x']) else ('blue' if v else None)),
        dict(type='array', var=lambda S: _bits(S['x'] - 1) if S.get('x') else None,
             label='x - 1（最低位的 1 变 0，它右边的 0 全变 1）', cell=90, h=140, index=False,
             color=lambda S, i, v: 'orange' if _low(S['x']) is not None and i >= _low(S['x']) else None),
    ],
    watch=[('x', 'x', 'blue'), ('x 二进制', lambda S: format(S['x'], f'0{W}b') if 'x' in S else None, 'blue'),
           ('y', 'y'), ('res', 'res', 'green')],
    captions={
        'x ^= y': '异或：==相同位得 0、不同位得 1== → `x = {B.x} ^ {y} = {x}`（`{x:05b}`）',
        'res = 0': '汉明距离 = 异或结果里 1 的个数，`res` 用来计数',
        'while x': lambda S, B, r: (f'`x = {B.x}`（`{B.x:05b}`）≠ 0 → 还有 1 没数' if B.x
                                    else '`x = 0`：所有的 1 都被消掉了 → 结束'),
        'x &= x - 1': '`{B.x:05b} & {B.x - 1:05b} = {x:05b}`：`x & (x-1)` ==消掉了最低位的 1==',
        'res += 1': '消掉一个 1，计数 `res = {res}`',
        'return res': lambda S, B, r: f'`{X0}` 和 `{Y0}` 的二进制有 =={r}== 位不同 → 汉明距离 `{r}`',
    },
    cards=dict(
        one_liner='x ^ y 把不同的位变成 1，再用 x & (x-1) 一个个数出来',
        complexity='时间 `O(1)`（至多 31 次循环），空间 `O(1)`',
        problem=['两个整数之间的==汉明距离==：它们二进制表示中==不同位置==的数目',
                 '给你 `x` 和 `y`，返回它们的汉明距离',
                 '示例：`x = 1, y = 4` → `2`（`0001` 和 `0100`）',
                 f'本视频：`x = {X0}, y = {Y0}` → `4`'],
        quote='很自然就想到对两个数取异或，==异或结果中1的个数就是汉明距离==。而对于统计1的个数，则可以通过x & x - 1这个操作逐个分离出x的最低位的1。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`x ^ y`：相同位为 0，不同位为 1 → 问题变成数 1 的个数',
              '`x - 1`：最低位的 1 变成 0，它右边的 0 全变成 1',
              '`x & (x-1)`：正好==只消掉最低位的 1==；循环次数 = 1 的个数'],
        result=f'返回 `4`：`{X0}`（`11101`）和 `{Y0}`（`00110`）有 4 位不同 ✓',
        summary=['循环次数等于 1 的个数，比逐位右移检查更快',
                 '`x & x - 1` 中 `-` 优先级高于 `&`，等价于 `x & (x - 1)`',
                 'Python 3.10+ 也可以直接 `(x ^ y).bit_count()`',
                 '同类：191 位1的个数、338 比特位计数、231 2 的幂',
                 '原文为 Python 2 风格：删去了文档字符串，代码未改'],
    ),
)
