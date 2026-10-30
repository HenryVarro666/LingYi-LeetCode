CONFIG = dict(
    num=3658, title='奇数和与偶数和的最大公约数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='等差数列求和 + 互质',
    tags=['灵神题单', '数学算法', '难度分 1220'],
    code='''
class Solution:
    def gcdOfOddEvenSums(self, n: int) -> int:
        return n
''',
    call='Solution().gcdOfOddEvenSums(4)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: '`sumOdd = 1+3+...+(2n-1) = n²`', size=34),
        dict(type='text', fn=lambda S: '`sumEven = 2+4+...+2n = n(n+1)`', size=34),
        dict(type='text', fn=lambda S: f"n = {S['n']}：`sumOdd = {S['n']**2}`，`sumEven = {S['n']*(S['n']+1)}`" if 'n' in S else '', size=34),
        dict(type='text', fn=lambda S: f"提出公因数 n 后剩 `n` 和 `n+1`：==相邻整数互质==，所以 gcd = `n`", size=34),
    ],
    watch=['n'],
    captions={
        'return n': '`gcd(n², n(n+1)) = n × gcd(n, n+1) = n × 1`，直接返回 `n = {ret}`',
    },
    cards=dict(
        one_liner='两个和分别是 n² 和 n(n+1)，公因数就是 n',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`sumOdd`：最小 n 个正奇数之和；`sumEven`：最小 n 个正偶数之和',
                 '返回两者的最大公约数',
                 '示例：`n = 4` → `gcd(16, 20) = 4`'],
        quote='提取公约数 n 后，sumOdd 剩下 n，sumEven 剩下 n+1，这两个数一定互质。',
        quote_src='—— 灵茶山艾府题解',
        idea=['等差数列求和：`sumOdd = (1 + 2n - 1) * n / 2 = n²`',
              '`sumEven = (2 + 2n) * n / 2 = n(n+1)`',
              '反证法：`n` 与 `n+1` 若有公因数 `x > 1`，两数至少差 `x`，与差 1 矛盾'],
        after=[dict(heading='验证几个 n', lines=['`n=1`：`1` 和 `2` → gcd `1`', '`n=2`：`4` 和 `6` → gcd `2`', '`n=3`：`9` 和 `12` → gcd `3`', '`n=4`：`16` 和 `20` → gcd `4`', '每一行的答案都等于 ==n=='])],
        summary=['时间、空间都是 `O(1)`',
                 '不需要真的求和再算 gcd，推出公式后答案就是 `n`',
                 '关键是证明 `n` 和 `n+1` 互质',
                 '代码只有一行 `return n`，动画重点在推导'],
    ),
)
