FIB = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


def _fib_hl(S):
    if 'b' not in S:
        return None
    return FIB.index(S['b']) if S['b'] in FIB else None


CONFIG = dict(
    num=4078, title='连续三项斐波那契数之和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='化简为「n 是否为某项的两倍」', tags=[],
    code='''
class Solution(object):
    def threeFibonacciSum(self, n):
        
        if n % 2 == 1:
            return False
        
        n //= 2
        a, b = 0, 1
        while b < n:
            a, b = b, a + b
        
        return b == n
''',
    call='Solution().threeFibonacciSum(42)',
    expect=True,
    views=[
        dict(type='text', size=32, h=110, fn=lambda S: 'f[i] + f[i+1] + f[i+2] = f[i+2] × 2（前两项之和就是第三项）'),
        dict(type='array', var=lambda S: FIB, label='斐波那契数列（粉 = 当前 b）', h=230,
             color=lambda S, i, v: ('pink' if 'b' in S and v == S['b'] and i == FIB.index(S['b']) else None)),
        dict(type='text', size=34, h=110, fn=lambda S: (f"目标：n 要等于某一项，当前 b = =={S['b']}==，n = =={S['n']}==" if 'b' in S and 'n' in S else (f"n = =={S['n']}==" if 'n' in S else ''))),
    ],
    watch=[('n', 'n', 'orange'), ('a', 'a', 'blue'), ('b', 'b', 'pink')],
    captions={
        'if n % 2 == 1': '连续三项之和 = 某项的两倍，必为偶数。`{n} % 2 = {n % 2}` → {"奇数，直接 False" if n % 2 == 1 else "偶数，继续"}',
        'return False': '奇数不可能是某项的两倍 → `False`',
        'n //= 2': '问题变成：`n` 是不是数列里的某一项？`n` 变为 `{n}`',
        'a, b = 0, 1': '从数列开头 `0, 1` 开始递推：`a = {a}`，`b = {b}`',
        'while b < n': '`b < n`？`{b} < {n}` → {"还没到，继续往后推" if b < n else "到头了，停"}',
        'a, b = b, a + b': '往后推一项：`a = {a}`，`b = {b}`',
        'return b == n': '`b == n`？`{b} == {n}` → ==' + '{b == n}' + '==',
    },
    cards=dict(
        one_liner='三项之和化简成「某一项的两倍」',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给整数 `n`，判断它能否写成斐波那契数列中连续三项之和',
                 '例如 `8 + 13 + 21 = 42` → `True`',
                 '本视频：`n = 42`'],
        quote='对于斐波那契数列中的连续三项f[index]、f[index + 1]以及f[index + 2]，这三者之和可以将前两项合并，那么得到的就是f[index + 2] * 2。换言之，题目问的就是n是否为数列中某一项的两倍。',
        quote_src='—— yiduobo 题解原文',
        idea=['前两项相加正好是第三项，所以三项之和 = 第三项 × 2',
              '于是 `n` 必须是偶数，且 `n / 2` 要出现在数列里',
              '从 `0, 1` 递推到不小于 `n/2`，看是否恰好相等'],
        summary=['时间 `O(log n)`（斐波那契增长很快），空间 `O(1)`',
                 '易错：先判奇偶，奇数直接 `False`；`n / 2` 要用整除',
                 '递推停在第一个 `>= n/2` 的项，用 `b == n` 判等',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
