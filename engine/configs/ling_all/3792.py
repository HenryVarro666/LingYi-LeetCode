CONFIG = dict(
    num=3792, title='递增乘积块之和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='暴力模拟 + 中途取模',
    code='''
class Solution:
    def sumOfBlocks(self, n: int) -> int:
        MOD = 1_000_000_007
        ans = 0
        begin = 1
        for i in range(1, n + 1):
            m = 1
            for j in range(begin, begin + i):
                m = m * j % MOD
            ans += m
            begin += i
        return ans % MOD
''',
    call='Solution().sumOfBlocks(4)',
    expect=5167,
    views=[
        dict(type='text', size=34, fn=lambda S: (f"第 `{S['i']}` 块：从 `{S['begin']}` 起连乘 {S['i']} 个数，当前乘积 `m = {S['m']}`" if 'm' in S and 'begin' in S else '块 1 = 1，块 2 = 2×3，块 3 = 4×5×6，…') if 'i' in S else '块 1 = 1，块 2 = 2×3，块 3 = 4×5×6，…'),
        dict(type='text', size=30, fn=lambda S: f"已累加的块之和 `ans = {S['ans']}`" if 'ans' in S else ''),
    ],
    watch=['i', 'begin', 'j', 'm', ('ans', 'ans', 'green')],
    captions={
        'MOD =': '答案要对 `10^9 + 7` 取模',
        'm = 1': '第 `{i}` 块：从 `begin={begin}` 开始，连乘 `{i}` 个数，先把乘积 `m` 置为 1',
        'm = m * j': '`m = m * {j} % MOD` = =={m}==，==每乘一次就取模==，数字不会变大',
        'ans += m': '第 {i} 块乘积 =={m}==，累加进答案：`ans = {ans}`',
        'begin += i': '下一块从 `begin + i` 开始：`begin` → {begin}',
        'return ans': '最后再对 `MOD` 取一次模，返回 =={ret}==',
    },
    cards=dict(
        one_liner='n 很小，逐块连乘，边乘边取模',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['数列分块：第 1 块是 `1`，第 2 块是 `2×3`，第 3 块是 `4×5×6`，……第 i 块是接下来连续 i 个整数的乘积',
                 '求前 n 块乘积之和，对 `10^9 + 7` 取模',
                 '演示用：`n=4` → `1 + 6 + 120 + 5040 = 5167`'],
        quote='n 很小，O(n^2) 暴力即可。代码实现时，注意取模。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`begin` 记录当前块的起点，第 i 块的数是 `begin ... begin+i-1`',
              '内层循环连乘，每一步都 `% MOD`',
              '外层用 `begin += i` 跳到下一块'],
        summary=['时间 `O(n^2)`：共约 n^2/2 次乘法',
                 '为什么能中途取模：乘法和加法对模运算封闭',
                 '易错点：`ans` 累加后最后要再取模',
                 '起点 `begin` 每块增加的是 i，不是 1'],
    ),
)
