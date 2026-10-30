def _rule(S):
    inn = S['_inner']
    if 'now' not in inn:
        return ''
    now, flag = inn['now'], inn.get('flag')
    if flag is None:
        return ''
    if flag:
        return f'正序 `f({now})` = `2 × g({now // 2})`：删奇数项，剩下的除以 2'
    if now % 2:
        return f'逆序 `g({now})`，`{now}` 是奇数 = `2 × f({now // 2})`：剩偶数项'
    return f'逆序 `g({now})`，`{now}` 是偶数 = `2 × f({now // 2}) - 1`：剩奇数项'


CONFIG = dict(
    num=390, title='消除游戏', difficulty='Medium', category='位运算',
    author='yiduobo', technique='找规律 · f/g 互相递归',
    tags=['位运算', '数学算法', '难度分 3782'],
    code='''
class Solution(object):
    def lastRemaining(self, n):

        return self.calc(n, True)

    def calc(self, now, flag):
        if now == 1:
            return 1

        if flag:
            return 2 * self.calc(now // 2, False)
        else:
            return 2 * self.calc(now // 2, True) - 1 + now % 2
''',
    call='Solution().lastRemaining(9)',
    expect=6,
    views=[
        dict(type='text', fn=_rule, size=28, h=80),
        dict(type='calls', h=420),
        dict(type='text', fn=lambda S: '`f(n)`：从左往右开始；`g(n)`：从右往左开始', size=26, h=60),
    ],
    watch=[],
    captions={
        'return self.calc(n, True)': '题目求 `f(n)`：第一轮是正序，所以 `flag = True`',
        'if now == 1': lambda S, B, r: (f'`now = {S._inner["now"]}`：只剩 1 个数，答案就是 1' if S._inner['now'] == 1
                                        else f'`now = {S._inner["now"]} > 1`，还要继续消除'),
        'if flag': lambda S, B, r: ('`flag = True`：这一轮从左往右（正序）' if S._inner['flag'] else '`flag = False`：这一轮从右往左（逆序）'),
        'return 2 * self.calc(now // 2, False)': '`now = {B.now}`，正序删掉奇数项，剩 `2,4,6...`，除以 2 就是子问题 `g({B.now // 2})`：`f({B.now}) = 2 × g({B.now // 2})`',
        'return 2 * self.calc(now // 2, True)': lambda S, B, r: (
            f'逆序：`now = {B.now}` 是奇数，剩下偶数项 `2,4,...,now-1`，`g({B.now}) = 2 × f({B.now // 2})`' if B.now % 2
            else f'逆序：`now = {B.now}` 是偶数，剩下奇数项 `1,3,...,now-1`，加一再除以 2，`g({B.now}) = 2 × f({B.now // 2}) - 1`'),
    },
    cards=dict(
        one_liner='f(n) 和 g(n) 互相递归：每轮规模减半',
        complexity='时间 `O(log n)`，空间 `O(log n)`（递归栈）',
        problem=['`1..n` 先正序删、再逆序删，交替进行，直到剩一个数',
                 '每轮：删第一个，之后隔一个删一个',
                 '示例：`n = 9` → `6`'],
        quote='如果将剩下的数都除以2，那么就可以得到f[n] = g[n/2] * 2',
        quote_src='—— yiduobo 题解原文',
        idea=['`f(n)`：第一步正序；`g(n)`：第一步逆序',
              '`f(n) = 2 × g(n//2)`：正序删完剩 `2,4,6...`，除以 2 变回子问题',
              '`g(n)`：`n` 奇数 `= 2 × f(n//2)`；偶数 `= 2 × f(n//2) - 1`'],
        summary=['时间 `O(log n)`，递归深度约 `log n`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错点：逆序时 `n` 的奇偶决定剩下偶数项还是奇数项',
                 '对比灵神：他直接维护等差数列的首项和公差，这里是 f/g 公式递推'],
    ),
)
