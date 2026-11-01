CONFIG = dict(
    num=1968, title='构造元素不等于两相邻元素平均值的数组', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='排序后小大交替 隔位填充（Go 原文转写）',
    tags=['贪心与思维', '难度分 1499'],
    code='''
class Solution:
    def rearrangeArray(self, a: List[int]) -> List[int]:
        a.sort()
        i, n = 0, len(a)
        ans = [0] * n
        for v in a:
            ans[i] = v
            i += 2
            if i >= n:
                i = 1
        return ans
''',
    call='Solution().rearrangeArray([5,1,8,3,9,2,7])',
    expect=[1, 7, 2, 8, 3, 9, 5],
    views=[
        dict(type='array', var='a', label='排序后的 a（蓝 = 当前要放的 v）', h=230,
             color=lambda S, i, v: 'blue' if 'v' in S and v == S['v'] else None,
             dim=lambda S, i, v: 'v' in S and v < S['v']),
        dict(type='array', var='ans', label='ans（先填偶数下标，再填奇数下标）', pointers={'i': 'pink'}, h=260,
             color=lambda S, i, v: ('green' if i % 2 == 0 else 'cyan') if v != 0 else None),
    ],
    watch=['n', ('i', 'i', 'pink'), ('v', 'v', 'blue')],
    captions={
        'a.sort()': '先排序：`a = {a}`，后面小的放偶数位、大的放奇数位',
        'i, n = 0, len': '`i` 是下一个要填的位置，`n = {n}`',
        'ans = [0] * n': '`ans` 先放 `{n}` 个占位的 0',
        'for v in a': '按从小到大取下一个数 `v = {v}`',
        'ans[i] = v': '把 `{v}` 放到 `ans[{i}]`',
        'i += 2': '隔一位填：`i` → {i}',
        'if i >= n': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还没越界，继续隔一位填' if S.i < S.n else (f'`i = {S.i} >= n = {S.n}`：越界了，偶数位已经填满 → 成立，转去填奇数位' if 0 in S.ans else f'`i = {S.i} >= n = {S.n}`：越界了，但所有数都已放好')),
        'i = 1': lambda S, B, r: ('偶数位都是较小的数，从 `i = 1` 开始填奇数位（较大的数）' if 0 in S.ans else '`i = 1`：所有数都已放好，循环马上结束'),
        'return ans': '偶数位 `ans` 全是小数，奇数位全是大数 → 每个奇数位比左右邻居都大，返回 `{ans}`',
    },
    cards=dict(
        one_liner='排序后，小的数放偶数位，大的数放奇数位',
        complexity='时间 `O(n log n)`，空间 `O(n)`（排序之外）',
        problem=['把 `nums` 里互不相同的整数重排，使每个数都不等于左右两数的平均值',
                 '返回任意一种合法重排',
                 '本视频：`[5,1,8,3,9,2,7]`'],
        quote='排序后，把小的一半放到偶数下标，大的一半放到奇数下标（代码用 i += 2，越界后改成 i = 1）。',
        quote_src='—— 灵茶山艾府题解代码（Go）',
        idea=['偶数下标装较小的数，奇数下标装较大的数',
              '奇数位上的数比左右邻居都大 → 不可能是平均值',
              '偶数位上的数比左右邻居都小，同理'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`if i += 2; i >= n` 拆成两行）',
                 '时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错点：数组元素互不相同，才能保证严格大于、严格小于',
                 '`i >= n` 之后从 1 开始，不是从 0 重新开始'],
    ),
)
