CONFIG = dict(
    num=2595, title='奇偶位数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='逐位遍历 · i^=1 切换奇偶',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def evenOddBit(self, n: int) -> List[int]:
        ans = [0, 0]
        i = 0
        while n:
            ans[i] += n & 1
            n >>= 1
            i ^= 1  # 切换奇偶
        return ans
''',
    call='Solution().evenOddBit(50)',
    expect=[1, 2],
    views=[
        dict(type='string', var="format(n, 'b') if n else '0'", label='n 还剩的二进制（最右边 = 当前最低位）', h=170, index=False),
        dict(type='array', var='ans', pointers={'i': 'blue'}, label='ans：下标 0 = 偶数位个数，下标 1 = 奇数位个数', h=200),
    ],
    watch=['n', ('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'while n': lambda S, B, r: (f'`n = {S.n}`（二进制 `{bin(S.n)[2:]}`）还没取完，继续' if S.n else '`n = 0`：所有比特都取完了'),
        'ans[i] += n & 1': '最低位是 `{n & 1}`，当前下标 `i = {i}`（{"偶" if i == 0 else "奇"}数位）→ `ans[{i}]` 累加到 =={ans[i]}==',
        'n >>= 1': '右移一位，次低位成为新的最低位：`n` = {n}',
        'i ^= 1': '`i ^= 1` 在 0 和 1 之间切换：下一位是{"偶" if i == 0 else "奇"}数位',
        'return ans': '返回 `[偶数位 1 的个数, 奇数位 1 的个数]` = =={ans}==',
    },
    cards=dict(
        one_liner='从低位到高位取比特，用 i^=1 轮流记到偶、奇两格',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['统计 `n` 的二进制中，偶数下标、奇数下标上 `1` 的个数（下标从右往左，从 0 开始）',
                 '示例：`50 = 110010` → `[1,2]`', '示例：`2 = 10` → `[0,1]`'],
        quote='通过 n & 1 取二进制的最低位，然后把 n 右移一位，继续计算 n & 1，这样可以取到次低位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n & 1` 取最低位，`n >>= 1` 换下一位，直到 `n = 0`', '`i` 只在 0 和 1 间切换，正好对应偶、奇下标',
              '`ans[i] += n & 1`：是 0 就加 0，不用写 if'],
        after=[dict(heading='方法二：位掩码', lines=['`MASK = 0x55555555`（0101…01）取出所有偶数位', '`n & MASK` 与 `n & ~MASK` 各用 `bit_count()` 数 1', '时间 `O(1)`'])],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：下标从右（最低位）往左数，不是从字符串左边数',
                 '`i ^= 1` 可以代替 `i = 1 - i` 或 `i += 1` 再取模',
                 '`bit_count()` 需要 Python 3.10+'],
    ),
)
