def _formula(S):
    if 'i' not in S or 'j' not in S:
        return '`f[i]` = i 对人的握手方案数，`f[0] = 1`'
    i, j = S['i'], S['j']
    return f'`f[{i}] += f[{j}] × f[{i - j - 1}]`：第一对握手把其余人分成 =={j}== 对和 =={i - j - 1}== 对两块'


def _color(S, k, v):
    if 'i' not in S or 'j' not in S or S.get('_line', 0) not in (11, 12):
        return None
    i, j = S['i'], S['j']
    if k == i:
        return 'yellow'
    if k == j:
        return 'blue'
    if k == i - j - 1:
        return 'pink'
    return None


CONFIG = dict(
    num=1259, title='不相交的握手', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='卡特兰数递推 · 枚举切分出去的握手对数',
    tags=[],
    code='''
class Solution(object):
    def numberOfWays(self, numPeople):

        mod = 10 ** 9 + 7
        n = numPeople // 2

        f = [0] * (n + 1)
        f[0] = 1
        for i in range(1, n + 1):
            for j in range(i):
                f[i] += f[j] * f[i - j - 1]
                f[i] %= mod
        
        return f[n]
''',
    call='Solution().numberOfWays(8)',
    expect=14,
    skip=['mod = 10', 'for j in range'],
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var='f', label='f（黄 = 正在算的 f[i]，蓝 = f[j]，粉 = f[i-j-1]）', cell=100,
             pointers={'i': 'yellow'}, color=_color, h=260),
        dict(type='text', fn=lambda S: f"`numPeople = {S['numPeople']}` → 一共 `n = {S['n']}` 对人" if 'n' in S else '', size=26, h=50),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'blue')],
    captions={
        'n = numPeople': '`numPeople = {numPeople}`，人两两握手，只看==对数== `n = {n}`（原文 `/` 在 Python 3 要写 `//`）',
        'f = [0] * (n + 1)': '`f[i]` 表示 i 对人的合法握手方案数',
        'f[0] = 1': '0 对人：什么也不做，算 `1` 种方案（边界）',
        'for i in range': lambda S, B, r: (f'计算 `f[{S.i}]`：枚举切分出去的握手对数 `j`' if 'i' in S and S.get('i') != B.get('i') else '`f` 全部算完'),
        'f[i] += f[j] * f[i - j - 1]': '一对握手把剩下的人分成 `j = {j}` 对和 `{i - j - 1}` 对两块，互不相交 → 加上 `f[{j}] × f[{i - j - 1}] = {f[j] * f[i - j - 1]}`，`f[{i}] = {f[i]}`',
        'f[i] %= mod': '取模防止溢出：`f[{i}] = {f[i]}`',
        'return f[n]': '`n = {n}` 对人的方案数 `{f[n]}`',
    },
    cards=dict(
        one_liner='一次握手把人分成两块独立子问题，递推式就是卡特兰数',
        complexity='时间 `O(n²)`（n = numPeople/2），空间 `O(n)`',
        problem=['偶数个人围成一圈，每人恰好和另一人握手，所有握手的手臂两两不相交',
                 '求不同的握手方案数，对 `10^9 + 7` 取模',
                 '本视频：`numPeople = 8` → `14`'],
        quote='当一次握手发生后，这些人将被分为不相交的两个部分，也就是说转化成了两个子问题，因此在这里可以使用规划来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数个人方案数为 0，所以只看握手的==对数== `i`，边界 `f[0] = 1`',
              '枚举被切分出去的握手对数 `j`：`f[i] = sum(f[j] × f[i - j - 1])`',
              '这正是标准的卡特兰数递推，也可以用组合数直接求'],
        summary=['时间 `O(n²)`，空间 `O(n)`',
                 '易错：`f[0] = 1` 不能写 0；乘法后记得 `% mod`',
                 '原文为 Python 2 写法，`numPeople / 2` 已改为 `numPeople // 2`',
                 '同类：卡特兰数问题（括号生成、不同的二叉搜索树）'],
    ),
)
