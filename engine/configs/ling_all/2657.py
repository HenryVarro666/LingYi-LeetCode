def _set(m, n=4):
    return '{' + ', '.join(str(i) for i in range(1, n + 1) if m >> i & 1) + '}'


def _info(S):
    if 'p' not in S:
        return ''
    p, q = S['p'], S['q']
    s = f'A 前缀集合 `p = {_set(p)}`，B 前缀集合 `q = {_set(q)}`'
    if S['_line'] >= 8:
        s += f'；交集 `p & q = {_set(p & q)}`，大小 ==%d==' % (p & q).bit_count()
    return s


CONFIG = dict(
    num=2657, title='找到两个数组的前缀公共数组', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='二进制表示集合 · AND 求交集',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def findThePrefixCommonArray(self, a: List[int], b: List[int]) -> List[int]:
        ans = []
        p = q = 0
        for x, y in zip(a, b):
            p |= 1 << x
            q |= 1 << y
            ans.append((p & q).bit_count())
        return ans
''',
    call='Solution().findThePrefixCommonArray([1,3,2,4], [3,1,2,4])',
    expect=[0, 2, 3, 4],
    views=[
        dict(type='array', var='a', label='a', pointers={'a.index(x)': 'blue'}, pointer_labels={'a.index(x)': 'x'}, h=170, cell=80),
        dict(type='array', var='b', label='b', pointers={'b.index(y)': 'pink'}, pointer_labels={'b.index(y)': 'y'}, h=170, cell=80),
        dict(type='array', var='ans', label='ans（前缀公共数组）', min_slots=4, h=170, cell=80,
             color=lambda S, i, v: 'green' if i == len(S['ans']) - 1 else None),
        dict(type='text', fn=_info, h=90),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('p', "bin(p)[2:]", 'cyan'), ('q', "bin(q)[2:]", 'orange')],
    captions={
        'p = q = 0': 'p、q 是两个二进制数，各表示一个集合，初始都是空集 `0`',
        'p |= 1 << x': lambda S, B, r: f'把 `x = {S.x}` 加入集合 A：第 `{S.x}` 位置 1 → `p = {bin(S.p)[2:]}` = {_set(S.p)}',
        'q |= 1 << y': lambda S, B, r: f'把 `y = {S.y}` 加入集合 B：第 `{S.y}` 位置 1 → `q = {bin(S.q)[2:]}` = {_set(S.q)}',
        'ans.append': '`p & q = {bin(p & q)[2:]}`，AND 就是集合交集；`bit_count()` 数出 1 的个数 → ==`{ans[-1]}`== 个公共元素',
        'return ans': '前缀公共数组 `{ans}`',
    },
    cards=dict(
        one_liner='二进制数当集合：AND 是交集，1 的个数是交集大小',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['`A`、`B` 是长度为 n 的排列，`C[i]` 是两数组下标 0..i 的前缀里 ==公共元素的个数==',
                 '示例：`A=[1,3,2,4]`，`B=[3,1,2,4]` → `[0,2,3,4]`',
                 '本视频用的就是这个示例'],
        quote='用二进制数表示集合，两个二进制数的 AND 就是集合的交集，二进制数中 1 的个数就是交集的大小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`p` 的第 x 位为 1 表示 x 已在 A 的前缀里，`q` 同理',
              '每走一步把 `a[i]`、`b[i]` 分别加入集合',
              '`(p & q).bit_count()` 就是前缀公共元素个数，不需要哈希表'],
        summary=['时间 `O(n)`，空间 `O(1)`（n ≤ 50，一个整数装得下）',
                 '`1 << x` 而不是 `1 << (x-1)`：元素 1..n 用第 1..n 位，第 0 位空着没关系',
                 '`int.bit_count()` 需要 Python 3.10+，旧版本可用 `bin(v).count("1")`',
                 '同类：用位掩码表示集合，见灵神位运算题单'],
    ),
)
