def _set(m, n=3):
    return '{' + ', '.join(str(i) for i in range(1, n + 1) if m >> i & 1) + '}'


def _info(S):
    if 'x' not in S:
        return ''
    s = f'A 的前缀 `x = {_set(S["x"])}`，B 的前缀 `y = {_set(S["y"])}`'
    if 't' in S and S['_line'] >= 11:
        s += f'；`t = x & y = {bin(S["t"])[2:]}`，已数出 ==%d== 个 1' % S['cnt']
    return s


CONFIG = dict(
    num=2657, title='找到两个数组的前缀公共数组', difficulty='Medium', category='位运算',
    author='yiduobo', technique='位掩码 · lowbit 数 1',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def findThePrefixCommonArray(self, A, B):

        x = y = 0
        res = []
        for a, b in zip(A, B):
            x |= (1 << a)
            y |= (1 << b)
            
            t = x & y
            cnt = 0
            while t:
                t -= t & -t
                cnt += 1
            
            res.append(cnt)
        
        return res
''',
    call='Solution().findThePrefixCommonArray([2,3,1], [3,1,2])',
    expect=[0, 1, 3],
    views=[
        dict(type='array', var='A', label='A', pointers={'A.index(a)': 'blue'}, pointer_labels={'A.index(a)': 'a'}, h=170, cell=90),
        dict(type='array', var='B', label='B', pointers={'B.index(b)': 'pink'}, pointer_labels={'B.index(b)': 'b'}, h=170, cell=90),
        dict(type='array', var='res', label='res', min_slots=3, h=170, cell=90,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
        dict(type='text', fn=_info, h=90),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), ('x', "bin(x)[2:]", 'cyan'), ('y', "bin(y)[2:]", 'orange'),
           ('t', 't', 'yellow'), ('cnt', 'cnt', 'green')],
    captions={
        'x = y = 0': '`x`、`y` 各是一个二进制数：第 k 位为 1 表示 k 已经在 A（或 B）的前缀里',
        'x |= (1 << a)': '`a = {a}` 加入 A 的前缀：`x = {bin(x)[2:]}`',
        'y |= (1 << b)': '`b = {b}` 加入 B 的前缀：`y = {bin(y)[2:]}`',
        't = x & y': '两个前缀同时出现的数：`x & y = {bin(t)[2:]}`，它里面 1 的个数就是答案',
        'cnt = 0': '`cnt` 准备数 `t` 里有几个 1',
        'while t': lambda S, B, r: (f'`t = {bin(S.t)[2:]}` 还有 1 → 继续数' if S.t else '`t = 0`，1 都数完了'),
        't -= t & -t': '`t & -t` 是最低位的 1；减掉它：`t = {bin(t)[2:] if t else 0}`',
        'cnt += 1': '去掉了一个 1，`cnt = {cnt}`',
        'res.append': '这个前缀有 `{cnt}` 个公共数 → `res = {res}`',
        'return res': '前缀公共数组 `{res}`',
    },
    cards=dict(
        one_liner='用 50 位二进制数当集合，AND 后数 1 的个数',
        complexity='时间 `O(n·n)`，空间 `O(1)`（返回值不计）',
        problem=['`A`、`B` 是长度为 n 的排列，`C[i]` 是两数组下标 0..i 的前缀里 ==公共元素的个数==',
                 '示例：`A=[2,3,1]`，`B=[3,1,2]` → `[0,1,3]`',
                 '本视频用的就是这个示例'],
        quote='由于数组中的数都不超过50，因此可以分别使用两个50位的二进制数来表示A和B的当前前缀中是否包含某个数，那么同时出现的数字个数就是这两个二进制数按位与的结果中1的个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模很小，每个前缀直接算一次公共个数即可',
              '`x`、`y` 的第 k 位记录 k 是否出现过，`x & y` 里的 1 就是公共数',
              '数 1 的个数用 `t -= t & -t` 逐个去掉最低位的 1'],
        summary=['时间 `O(n^2)`：每个前缀最多数 n 个 1；空间 `O(1)`',
                 '`t & -t` 取最低位的 1，减掉后 1 的个数少一',
                 '数 1 也可以直接用 `bin(t).count("1")`',
                 '对比灵神：灵神用 `bit_count()` 一步数出，整体是 `O(n)`'],
    ),
)
