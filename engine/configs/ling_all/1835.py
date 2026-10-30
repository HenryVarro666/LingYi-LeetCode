import functools, operator


def _x(l):
    return functools.reduce(operator.xor, l)


CONFIG = dict(
    num=1835, title='所有数对按位与结果的异或和', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='分配律 (a&b)^(a&c)=a&(b^c)',
    tags=['灵神题单', '难度分 1825'],
    code='''
class Solution:
    def getXORSum(self, a: List[int], b: List[int]) -> int:
        return reduce(xor, a) & reduce(xor, b)
''',
    call='Solution().getXORSum([1,2,4], [6,5])',
    expect=3,
    views=[
        dict(type='array', var='a', label='a', h=150),
        dict(type='array', var='b', label='b', h=150),
        dict(type='text', h=60, size=34, fn=lambda S: f"`xor(a)` = `{_x(S['a']):03b}` = {_x(S['a'])}" if 'a' in S else ''),
        dict(type='text', h=60, size=34, fn=lambda S: f"`xor(b)` = `{_x(S['b']):03b}` = {_x(S['b'])}" if 'b' in S else ''),
        dict(type='text', h=60, size=34, fn=lambda S: f"相与 = `{_x(S['a']) & _x(S['b']):03b}` = =={_x(S['a']) & _x(S['b'])}==" if 'a' in S else ''),
    ],
    watch=[],
    captions={
        'return reduce': lambda S, B, r: f'`xor(a) = {_x(S.a)}`，`xor(b) = {_x(S.b)}`；因为 `(a&b)^(a&c) == a&(b^c)`，答案 = 两个异或和相与 = =={r}==',
    },
    cards=dict(
        after=[dict(heading='为什么能拆开：逐位看', lines=[
            '枚举某一位：`a` 里有 `p` 个数这位是 1，`b` 里有 `q` 个',
            '相与后这一位是 1 的数对有 `p × q` 个，异或看奇偶',
            '`p×q` 为奇 ⇔ `p`、`q` 都奇 ⇔ 两个异或和这位都是 1'])],
        one_liner='与对异或有分配律：两个数组各自异或，再相与',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['对所有数对 `(i, j)` 算 `a[i] & b[j]`，再把这些结果全部异或',
                 '数组长度到 `10^5`，不能两两枚举',
                 '示例：`a=[1,2,3], b=[6,5]` → `0`；本视频用 `[1,2,4]`、`[6,5]` → `3`'],
        quote='由于 (a&b)^(a&c) == a&(b^c)，将两个数组的异或和求出，两个异或和的与就是答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['固定 `a[i]`：它与 `b` 里每个数相与再异或 = `a[i] & xor(b)`',
              '再把所有 `a[i]` 的结果异或 = `xor(a) & xor(b)`',
              '一行代码，不用枚举数对'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '分配律：`&` 对 `^` 满足 `a&(b^c) = (a&b)^(a&c)`，位上看就是 GF(2) 的乘法对加法分配',
                 '`reduce`、`xor` 在 LeetCode 环境里已预置'],
    ),
)
