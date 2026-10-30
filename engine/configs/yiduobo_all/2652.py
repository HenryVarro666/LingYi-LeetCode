_X = lambda S: S['_inner'].get('x')


def _t(S):
    x = _X(S)
    if not x:
        return '先加 3、5、7 的倍数和，再减 15、21、35，最后补 105'
    n = S['n']
    cnt = n // x
    return f'`x = {x}`：`cnt = {n}//{x} = {cnt}`，倍数和 = `(1+{cnt}) × {cnt} / 2 × {x}` = =={(1 + cnt) * cnt // 2 * x}=='


CONFIG = dict(
    num=2652, title='倍数求和', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='容斥原理 · 倍数和公式',
    tags=[],
    code='''
class Solution(object):
    def sumOfMultiples(self, n):

        def calc(x):
            cnt = n // x
            return (1 + cnt) * cnt // 2 * x
        
        return calc(3) + calc(5) + calc(7) - calc(15) - calc(21) - calc(35) + calc(105)
''',
    call='Solution().sumOfMultiples(16)',
    expect=81,
    views=[
        dict(type='text', fn=_t, size=26, h=70),
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='1..n（青 = 当前 x 的倍数）', cell=60, h=190, index=False,
             color=lambda S, i, v: 'cyan' if _X(S) and v % _X(S) == 0 else None),
    ],
    watch=['n', ('x', _X, 'cyan'), ('cnt', lambda S: S['_inner'].get('cnt'), 'green')],
    captions={
        'cnt = n': '`cnt = n // x = {n} // {x}` = =={cnt}==：1 到 n 里 x 的最大倍数是 `cnt × x`',
        'return (1': lambda S, B, ret: f'`x + 2x + … + cnt·x = (1+cnt)×cnt/2 × x` = =={ret}==',
        'return calc(3)': lambda S, B, ret: ('15、21、35 的倍数被算了两次 → 各减一次；105 的倍数被加三次又减三次 → 再加一次。结果 =={}=='.format(ret)
                                             if ret is not None else '分别算出 3、5、7 的倍数和，再按「加、减、补」组合'),
    },
    max_steps=60,
    cards=dict(
        result='81 = 45 + 30 + 21 − 15 − 0 − 0 + 0',
        one_liner='3、5、7 的倍数和相加，重复的减掉，减过头的补回',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['求 `[1, n]` 内能被 `3`、`5`、`7` 之一整除的整数之和',
                 '示例：`n = 10` → `40`',
                 '本视频取 `n = 16`，答案 `81`'],
        quote='对于同时是3和5的倍数，即15的倍数的数，这些数的和在计算3的倍数之和以及5的倍数之和时都会被计算进行，也就是说多计算了一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x` 的倍数最大是 `cnt × x`，和 = `(1+cnt)×cnt/2 × x`',
              '15、21、35 的倍数被算了两次 → 各减一次',
              '105 的倍数：加了 3 次、减了 3 次 → 一次都没剩，要再加一次'],
        summary=['时间、空间都是 `O(1)`；数据很小，暴力也行',
                 '原文为 Python 2 写法，`/` 做整除，已改为 `//`',
                 '易错点：别忘了最后补 `+ calc(105)`',
                 '对比灵神：同一个容斥公式，yiduobo 先讲「为什么会多算」'],
    ),
)
