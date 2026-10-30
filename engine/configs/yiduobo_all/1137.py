def _win(S):
    if 'a' not in S:
        return '`T(0)=0, T(1)=1, T(2)=1`，之后 `T(n) = T(n-1)+T(n-2)+T(n-3)`'
    return f"窗口 `[a, b, c]` = `[{S['a']}, {S['b']}, {S['c']}]`，下一项 = `{S['a']}+{S['b']}+{S['c']}` = =={S['a']+S['b']+S['c']}=="


CONFIG = dict(
    num=1137, title='第 N 个泰波那契数', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='按定义逐项递推',
    tags=['动态规划'],
    code='''
class Solution(object):
    def tribonacci(self, n):

        if n == 0:
            return 0

        a, b, c = 0, 1, 1
        for index in range(3, n + 1):
            a, b, c = b, c, a + b + c
        
        return c
''',
    call='Solution().tribonacci(8)',
    expect=44,
    views=[
        dict(type='text', fn=_win, size=28, h=90),
        dict(type='array', var=lambda S: [S['a'], S['b'], S['c']] if 'a' in S else [0, 1, 1], label='[a, b, c]（滑动的三个数）', cell=150, h=260,
             color=lambda S, i, v: ('blue', 'pink', 'green')[i] if 'a' in S else None),
        dict(type='array', var=lambda S: [0, 1, 1, 2, 4, 7, 13, 24, 44], label='T(0..8) 参考：0 1 1 2 4 7 13 24 44', cell=90, h=200,
             pointers={'index': 'yellow'}),
    ],
    watch=[('n', 'n'), ('index', 'index', 'yellow'), ('a', 'a', 'blue'), ('b', 'b', 'pink'), ('c', 'c', 'green')],
    captions={
        'if n == 0': lambda S, B, r: '`n = 0`：直接返回 0（因为下面 `c` 初值是 `T(2)=1`）' if S.n == 0 else '`n = {}` 不是 0，往下走'.format(S.n),
        'a, b, c = 0, 1, 1': '`a, b, c` = `T(0), T(1), T(2)` = ==0, 1, 1==，所以 `n ≤ 2` 时 `c` 已经是答案',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：现在要算 `T({S.index})`' if 'index' in S and S.index != B.get('index')
                                              else 'N 不超过 37，逐项算完即可，不用矩阵快速幂'),
        'a, b, c = b, c, a + b + c': '新 `c` = `{B.a} + {B.b} + {B.c}` = =={c}==，三个数整体向右滑一格：`a, b, c = {a}, {b}, {c}`',
        'return c': '`c` 就是 `T({n})` = =={ret}==',
    },
    cards=dict(
        one_liner='N 很小，按定义逐项算：每次滑动三个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['泰波那契序列：`T0=0, T1=1, T2=1`，且 `Tn+3 = Tn + Tn+1 + Tn+2`',
                 '给定 `n`，求 `Tn` 的值（`0 ≤ n ≤ 37`）',
                 '示例：`n = 4` → `4`；本视频：`n = 8` → `44`'],
        quote='由于这里的N不超过37，因此没必要使用矩阵快速幂之类的东西，根据定义逐个计算就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['只保留最近三项 `a, b, c`，其余都不用存',
              '每一轮：新 `c = a + b + c`，同时 `a, b` 顺次后移',
              '`c` 初始就是 `T(2)`，循环从 `T(3)` 开始，跑 `n-2` 轮'],
        summary=['时间 `O(n)`，空间 `O(1)`；`n` 大时可改矩阵快速幂 `O(log n)`',
                 '易错：`n = 0` 要单独返回 0；`n = 1, 2` 靠 `c` 初值 1 自然得到',
                 '`a, b, c = b, c, a + b + c` 是元组同时赋值，右边先全部算好',
                 '原文已是 Python 3 可运行写法，无修改'],
    ),
)
