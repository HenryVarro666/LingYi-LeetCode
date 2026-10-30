CONFIG = dict(
    num=3536, title='两个数字的最大乘积', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='模 10 分离数位 · 记录最大两位',
    code='''
class Solution(object):
    def maxProduct(self, n):
        
        first, second = None, None
        while n:
            digit = n % 10
            n //= 10

            if first is None or first < digit:
                first, second = digit, first
            elif second is None or second < digit:
                second = digit

        return first * second
''',
    call='Solution().maxProduct(41927)',
    expect=63,
    views=[
        dict(type='text', h=120, size=34, fn=lambda S: f"剩余 `n = {S['n']}`，取出数位 `digit = {S['digit']}`" if 'digit' in S else f"剩余 `n = {S['n']}`"),
        dict(type='text', h=120, size=34, fn=lambda S: f"最大 `first` = =={S['first']}==　次大 `second` = =={S['second']}==" if 'first' in S else ''),
    ],
    watch=['n', 'digit', ('first', 'first', 'green'), ('second', 'second', 'cyan')],
    captions={
        'first, second = None': '`first`、`second` 先设为 `None`：还没见过任何数位',
        'while n': lambda S, B, r: (f'`n = {S.n}` 不为 0，继续分离数位' if S.n else '`n = 0`，数位分离完了'),
        'digit = n % 10': '`n % 10` 取出最低位 `digit = {digit}`',
        'n //= 10': '去掉最低位，`n = {n}`',
        'if first is None': lambda S, B, r: (f'`first` 还是空，直接成为最大' if B.first is None
                                              else (f'`first = {B.first} < digit = {S.digit}`：比最大还大 → 更新' if B.first < S.digit
                                                    else f'`first = {B.first} ≥ digit = {S.digit}`，不是新的最大')),
        'first, second = digit, first': '新数位当最大，旧最大降为次大：`first = {first}`，`second = {second}`',
        'elif second is None': lambda S, B, r: (f'`second` 还是空，直接成为次大' if B.second is None
                                                 else (f'`second = {B.second} < digit = {S.digit}`：比次大大 → 更新' if B.second < S.digit
                                                       else f'`second = {B.second} ≥ digit = {S.digit}`，忽略')),
        'second = digit': '`second` 更新为 `{second}`',
        'return first * second': '最大 `{first}` × 次大 `{second}` = =={first * second}==',
    },
    cards=dict(
        one_liner='乘积最大就用最大的两个数位，边分离边记录',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给出不小于 10 的正整数 `n`，从各位数字中任取两位相乘',
                 '求能得到的最大乘积',
                 '示例：`n = 124` → `8`；本视频：`41927` → `63`'],
        quote='为了使得乘积最大，使用的两个数位就应该是最大的两个，于是只需不断通过模10除10的方法分离n的所有数位，在这个过程中记录最大的两个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n % 10` 取最低位，`n //= 10` 丢掉它，直到 `n` 为 0',
              '用 `first`、`second` 保存目前最大、次大的数位',
              '分离完成后两者相乘即为答案'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：更新最大时旧最大要降为次大，用一次元组赋值完成',
                 '`first`、`second` 初值为 `None`，所以要先判空再比较',
                 '原文为 Python 2 写法，`n //= 10` 本来就是整除，仅删去类型说明；代码未改',
                 '对比灵神：灵神用 `divmod` 且初值为 0，省掉判空'],
    ),
)
