def _row(S):
    n = S.get('n')
    if not n:
        return None
    return [i | (n - 1) for i in range(n)]


def _fml(S):
    if 'pair' not in S or not S.get('n'):
        return '目标：`A` 的元素和 = `pair[n] × n × (n-1) // 2`，不超过 `s`'
    n = S['n']
    return (f'n = =={n}==：`pair = {S["pair"]}`，元素和 `now = {S["pair"]} × {n} × {n - 1} // 2` = =={S["now"]}==（s = {S["s"]}）')


CONFIG = dict(
    num=3344, title='最大尺寸数组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举 n + 递推 pair[n]',
    tags=['二分算法', '位运算'],
    code='''
class Solution(object):
    def maxSizedArray(self, s):
        
        now = 0
        n = 0
        pair = 0
        while now <= s:
            n += 1
            t = 0
            for i in range(n):
                t += (i | (n - 1))
            pair += t + t - (n - 1)
            now = pair * n * (n - 1) // 2

        return n - 1
''',
    call='Solution().maxSizedArray(100)',
    expect=3,
    skip=['now = 0', 'n = 0', 'pair = 0', 'for i in range(n)'],
    views=[
        dict(type='text', fn=_fml, size=26, h=90),
        dict(type='array', var=_row, label='本轮的 t = (0|n-1) + (1|n-1) + … + (n-1|n-1)，每格是 i | (n-1)',
             pointers={'i': 'blue'}, cell=96, h=260),
        dict(type='text', fn=lambda S: (f'`pair[n] = pair[n-1] + 2t − (n−1)`：多出来的项成对出现（交换律），(n-1)|(n-1) 只有一个，所以减掉一个 `n-1`'
                                         if 't' in S and S.get('n') else ''), size=24, h=110),
    ],
    watch=[('n', 'n', 'blue'), ('t', 't', 'orange'), ('pair', 'pair', 'purple'), ('now', 'now', 'green'), ('s', 's')],
    captions={
        'while now <= s': lambda S, B, r: (f'`now = {B.now} <= s = {B.s}`：这个 n 还放得下，继续试更大的 n' if B.now <= B.s
                                           else f'`now = {B.now} > s = {B.s}`：超了，上一个 n 就是答案'),
        'n += 1': '尝试更大的数组，`n` → =={n}==，把 `A` 的元素和算出来',
        't += (i | (n - 1))': '新增的 `n-1` 与 `i = {i}` 做按位或：`{i} | {n-1}` = {i | (n-1)}，累加到 `t` = {t}',
        'pair += t + t - (n - 1)': ('`pair[n]` 比 `pair[n-1]` 多出第 `n-1` 行和第 `n-1` 列：`t` 算两遍，'
                                    '中间 `(n-1)|(n-1)` 重复了一次要减掉 → `pair` = =={pair}=='),
        'now = pair * n * (n - 1) // 2': ('每个 `i` 对应 `i × pair`，i 从 0 到 n-1 求和 = `pair × n(n-1)/2` → `now` = =={now}=='),
        'return n - 1': '循环停下时 `n` 已经超了，最大合法尺寸是 `n - 1` = =={n - 1}=='
    },
    cards=dict(
        one_liner='把三维求和化成 pair[n] × n(n-1)/2，从小到大枚举 n',
        complexity='时间 `O(n^2)`（n 很小），空间 `O(1)`',
        problem=['给正整数 `s`，`A` 是 `n×n×n` 数组，`A[i][j][k] = i × (j | k)`',
                 '求最大的 `n`，使 `A` 所有元素之和 ≤ `s`',
                 '示例：`s = 100` → `3`（n=3 时和为 45，n=4 时和为 216）'],
        quote='手动跑几个n可以发现A数组元素之和的增长速度还是可以的，因此在这里直接从1开始向上枚举n，在过程中计算数组和now。',
        quote_src='—— yiduobo 题解原文',
        idea=['`i` 可以提出来：同一个 `i` 的所有项和 = `i × pair[n]`',
              '总和 = `pair[n] × (0+1+…+n-1)` = `pair[n] × n(n-1)/2`',
              '`pair[n]` 在 `pair[n-1]` 上只多出 `n-1` 参与的项，暴力 O(n) 算 `t`'],
        summary=['时间 `O(n^2)`：和增长很快，n 不会大，所以直接枚举',
                 '易错：`t` 要算两遍再减掉 `n-1`，对角项 `(n-1)|(n-1)` 只能算一次',
                 '循环结束时 `n` 是第一个超标的，答案要返回 `n - 1`',
                 '也可以对 n 二分（和随 n 单调增）；原文直接枚举，整数除法本来就是 `//`，代码未改'],
    ),
)
