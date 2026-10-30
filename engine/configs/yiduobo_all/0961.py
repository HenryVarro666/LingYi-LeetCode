CONFIG = dict(
    num=961, title='在长度 2N 的数组中找出重复 N 次的元素', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='枚举间距 1~3 · 比较相邻',
    tags=['随机算法', '摩尔投票法', '难度分 1162'],
    code='''
class Solution(object):
    def repeatedNTimes(self, A):

        for i in range(1, 4):
            for j in range(len(A) - i):
                if A[j] == A[j + i]:
                    return A[j]
''',
    call='Solution().repeatedNTimes([1,5,2,5,3,5])',
    expect=5,
    views=[
        dict(type='array', var='A', label='A（蓝 = A[j]，粉 = A[j+i]）', h=210, cell=96,
             pointers={'j': 'blue', 'j + i': 'pink'},
             color=lambda S, i, v: ('blue' if i == S.get('j') else 'pink' if 'j' in S and i == S['j'] + S['i'] else None)),
        dict(type='text', h=90, size=30,
             fn=lambda S: f"当前比较间距 `i = {S['i']}`：`A[{S['j']}]` 对 `A[{S['j']+S['i']}]`" if 'j' in S else ''),
    ],
    watch=[('间距 i', 'i', 'yellow'), ('j', 'j', 'blue')],
    captions={
        'for i in range(1, 4)': '枚举答案之间的间距 `i = {i}`（最多到 3，只有 X A B X 这种最挤的情形才要 3）',
        'for j in range(len(A) - i)': lambda S, B, r: (f'`j = {S.j}`：比较 `A[{S.j}]` 和相距 {S.i} 的 `A[{S.j + S.i}]`' if B.get('j') is None or S.j != B.get('j') or B.get('i') != S.i else f'间距 `{S.i}` 的所有 `j` 都比完了，没有相等的 → 换更大的间距'),
        'if A[j] == A[j + i]': lambda S, B, r: (f'`A[{S.j}] = {S.A[S.j]}`，`A[{S.j+S.i}] = {S.A[S.j+S.i]}` → 相等，这就是重复的数' if S.A[S.j] == S.A[S.j + S.i] else f'`{S.A[S.j]}` ≠ `{S.A[S.j+S.i]}` → 不是答案，`j` 往后'),
        'return A[j]': '两个相距 `{i}` 的数相等：它只可能是重复 N 次的数，返回 `{ret}`',
    },
    cards=dict(
        one_liner='答案占一半，所以两个答案之间的距离最多是 2（或 3）',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['长为 `2n` 的数组：`n+1` 个不同元素，其中一个恰好出现 `n` 次',
                 '找出重复了 `n` 次的元素',
                 '本视频：`[1,5,2,5,3,5]` → `5`'],
        quote='答案占所有数字的一半，那么两个连续答案之间的距离的最小值必然是小于等于2的，而这个2也只会出现在最特殊的情况即X A B X这种形式当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案占一半，塞得再松也是 `X A X B X C ...`，相邻两个答案间距 ≤ 2',
              '特殊情况 `X A B X`（`n = 2`）间距是 3，所以枚举间距 `1, 2, 3`',
              '对每个间距比较 `A[j]` 和 `A[j+i]`，相等就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`：外层只循环 3 次',
                 '易错点：间距要枚举到 3（`range(1, 4)`），否则 `[3,1,2,3]` 会漏',
                 '原文还提到：字典计数；或随机抽数（每次命中概率 0.5）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，`range` 本来就是通用写法'],
    ),
)
