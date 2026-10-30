def _cand(S, B):
    if 'a' not in B or S.get('_line') != 9:
        return '更新窗口时，用旧的 a b c d 算四个候选'
    a, b, c, d, e = B['a'], B['b'], B['c'], B['d'], B['e']
    return f"候选：`{d}×2={d*2}`（3 步×2）  `{c}×3={c*3}`（4 步×3）  `{b}×4={b*4}`  `{a}×5={a*5}` → 取最大 ==" + str(max(d*2, c*3, b*4, a*5)) + "=="


CONFIG = dict(
    num=651, title='4键键盘', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='递推 · 滚动 6 个变量',
    tags=[],
    code='''
class Solution(object):
    def maxA(self, n):

        if n <= 6:
            return n
        else:
            a, b, c, d, e, f = 1, 2, 3, 4, 5, 6
            for index in range(7, n + 1):
                a, b, c, d, e, f = b, c, d, e, f, max(d * 2, c * 3, b * 4, a * 5)
            
            return f
''',
    call='Solution().maxA(10)',
    expect=20,
    views=[
        dict(type='text', fn=lambda S: f"现在算 ==f[{S['index']}]==（共 {S['n']} 步）" if 'index' in S else f"n = {S['n']}", size=28, h=70),
        dict(type='array', var=lambda S: [S['a'], S['b'], S['c'], S['d'], S['e'], S['f']] if 'a' in S else [], label='滚动窗口：a b c d e f = 最近 6 个 f 值', h=250, cell=110,
             color=lambda S, i, v: 'green' if i == 5 else None),
        dict(type='text', fn=_cand, size=26, h=90),
    ],
    watch=['n', 'index', ('f', 'f', 'green')],
    captions={
        'if n <= 6': '`n = {n}`：`n ≤ 6` 时全按 A 最划算，`f[n] = n`' ,
        'return n': '直接返回 `{n}`',
        'a, b, c, d, e, f = 1': '`f[1..6] = 1..6`：前 6 步只按 A 最优，窗口里存这 6 个值',
        'for index': lambda S, B, r: ('`range` 走完，循环结束' if B.get('index') == S.index else '下一个要算 `f[{}]`'.format(S.index)),
        'a, b, c, d, e, f = b': '`f[i] = max(f[i-3]×2, f[i-4]×3, f[i-5]×4, f[i-6]×5)` = =={f}==：窗口整体左移一格，`f` 换成新值',
        'return f': '`f[{n}] = {f}`：屏幕上最多出现 {f} 个 A',
    },
    cards=dict(
        one_liner='先加后乘：全选-复制-粘贴 N 次，相当于乘以 N−1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['键盘 4 个键：`A`、全选、复制、粘贴',
                 '恰好按 `n` 次，屏幕上最多能有多少个 `A`',
                 '示例：`n = 7` → `9`；本视频：`n = 10` → `20`'],
        quote='当 1 <= i <= 6 时，有 f[i] = i；当 i > 6 时，有 f[i] = max(f[i - 3] * 2, f[i - 4] * 3, f[i - 5] * 4, f[i - 6] * 5)。',
        quote_src='—— yiduobo 题解原文',
        idea=['全选-复制-粘贴 3 步 ==×2==，再多粘一次就 4 步 ×3，依此类推',
              '连续粘贴超过 6 步不划算：不如拆成两轮，剪贴板更大',
              '加 `A` 只会出现在最开头：先加后乘，加的部分会被放大'],
        summary=['时间 `O(n)`，空间 `O(1)`：只保留最近 6 个 `f`',
                 '易错：`n ≤ 6` 要单独返回 `n`，窗口初值是 `f[1..6]`',
                 '元组赋值右侧先整体求值，所以 `max` 用的是旧的 a、b、c、d',
                 '原文为 Python 2 写法，在 Python 3 下原样可运行'],
    ),
)
