CONFIG = dict(
    num=2178, title='拆分成最多数目的正偶数之和', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='从小到大贪心拆分',
    tags=['灵神题单', '难度分 1538'],
    code='''
class Solution:
    def maximumEvenSplit(self, finalSum: int) -> List[int]:
        if finalSum % 2:
            return []
        ans = []
        i = 2
        while i <= finalSum:
            ans.append(i)
            finalSum -= i
            i += 2
        ans[-1] += finalSum
        return ans
''',
    call='Solution().maximumEvenSplit(28)',
    expect=[2, 4, 6, 16],
    views=[
        dict(type='text', size=30, fn=lambda S: (f"已拆出 `{S['ans']}`，剩余 `finalSum = {S['finalSum']}`，下一个要拆 `i = {S['i']}`" if 'i' in S and 'ans' in S else '先判断奇偶，再从 2 开始一个个拆')),
        dict(type='array', var='ans', h=260, label='ans（已拆出的偶数）',
             color=lambda S, i, v: 'green' if i == len(S['ans']) - 1 else None),
    ],
    watch=[('finalSum 剩余', 'finalSum', 'cyan'), ('i', 'i', 'blue')],
    captions={
        'if finalSum % 2': lambda S, B, r: ('`finalSum` 是奇数：偶数之和不可能是奇数 → 无解' if S.finalSum % 2 else '`finalSum` 是偶数，可以拆'),
        'ans = []': '准备存放拆出来的偶数',
        'i = 2': '从最小的正偶数 `2` 开始拆：==数越小，能拆出的个数越多==',
        'while i <= finalSum': lambda S, B, r: (f'`i = {S.i} <= finalSum = {S.finalSum}`：剩下的钱够拆 `{S.i}` → 继续' if S.i <= S.finalSum else f'`i = {S.i} > finalSum = {S.finalSum}`：剩下的不够拆下一个 → 停止'),
        'ans.append(i)': '拆出 `{i}`：`ans = {ans}`',
        'finalSum -= i': '`finalSum` 减掉 `{i}`，还剩 =={finalSum}==',
        'i += 2': '下一个偶数 `{i}`（不能重复，所以必须更大）',
        'ans[-1] += finalSum': '剩下的 `{B.finalSum}` 不够再拆，==加到最后一个数上==：它变大后仍然不会和前面重复 → `ans = {ans}`',
        'return ans': '拆成了 `{len(ans)}` 个互不相同的偶数，返回 `{ans}`',
    },
    cards=dict(
        one_liner='从 2 开始一个个拆，剩下的并进最后一个数',
        complexity='时间 `O(√finalSum)`，空间 `O(1)`',
        problem=['把 `finalSum` 拆成若干个互不相同的正偶数之和，个数要最多',
                 '无法拆（奇数）就返回空数组',
                 '示例：`28` → `[2,4,6,16]`，`7` → `[]`'],
        quote='既然要尽量多的分解，且分解出的偶数互不相同，那么可以按照 2,4,6,8,⋯ 的顺序分解，一边分解一边减少 finalSum，直到 finalSum 小于要分解出的数为止。',
        quote_src='—— 灵茶山艾府题解',
        idea=['偶数之和还是偶数，奇数直接无解',
              '要个数最多，就用最小的 `2,4,6,…` 依次拆',
              '剩余的数不够拆下一个时，加到最后一个上，仍然互不相同'],
        summary=['拆出 `x` 个数时 `x(x+1) <= finalSum`，所以循环 `O(√finalSum)` 次',
                 '先判奇偶，奇数必须返回 `[]`',
                 '循环条件 `i <= finalSum` 保证 `ans` 至少有一个数，`ans[-1]` 不会越界',
                 '剩余部分一定 `< i`，加到最后一项后依然是偶数且最大'],
    ),
)
