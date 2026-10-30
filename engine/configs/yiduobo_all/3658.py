CONFIG = dict(
    num=3658, title='奇数和与偶数和的最大公约数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='公式推导',
    tags=['灵神题单', '数学算法', '难度分 1220'],
    code='''
class Solution(object):
    def gcdOfOddEvenSums(self, n):
        
        return n
''',
    call='Solution().gcdOfOddEvenSums(5)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: '前 n 个奇数和：`(1 + 2n - 1) × n / 2 = n²`', size=32),
        dict(type='text', fn=lambda S: '前 n 个偶数和：`(2 + 2n) × n / 2 = n × (n+1)`', size=32),
        dict(type='text', fn=lambda S: f"n = {S['n']}：`{S['n']**2}` 和 `{S['n']*(S['n']+1)}`" if 'n' in S else '', size=32),
        dict(type='text', fn=lambda S: '`n` 与 `n+1` 必然互质 → 最大公约数就是 ==n==', size=32),
    ],
    watch=['n'],
    captions={
        'return n': '两个和的最大公约数就是 `n = {ret}`',
    },
    cards=dict(
        one_liner='n 和 n+1 必然互质，所以公约数就是 n',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['求前 n 个正奇数之和 `sumOdd` 与前 n 个正偶数之和 `sumEven` 的最大公约数',
                 '示例：`n = 5` → `gcd(25, 30) = 5`'],
        quote='由于n和n + 1必然是互质的，因此以上两个值的最大公约数就是n。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数和：`1 + 3 + ... + (2n-1) = n²`',
              '偶数和：`2 + 4 + ... + 2n = n * (n+1)`',
              '两者都含因子 `n`，剩下 `n` 和 `n+1` 互质'],
        after=[dict(heading='验证几个 n', lines=['`n=1`：`1` 和 `2` → gcd `1`', '`n=2`：`4` 和 `6` → gcd `2`', '`n=3`：`9` 和 `12` → gcd `3`', '`n=4`：`16` 和 `20` → gcd `4`', '`n=5`：`25` 和 `30` → gcd `5`', '`n=6`：`36` 和 `42` → gcd `6`', '每一行的答案都等于 ==n=='])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '不用模拟求和，直接用公式',
                 '相邻整数互质是本题的关键',
                 '原文代码已是 Python 3 可运行，未改动'],
    ),
)
