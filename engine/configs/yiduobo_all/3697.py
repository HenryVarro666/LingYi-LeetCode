def _txt(S):
    if 'p' not in S:
        return ''
    return f"当前位权 `p = {S['p']}`，剩余 `n = {S['n']}`，个位 `n % 10 = {S['n'] % 10}`"


CONFIG = dict(
    num=3697, title='计算十进制表示', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模 10 逐位分离', tags=[],
    code='''
class Solution(object):
    def decimalRepresentation(self, n):
        
        res = []
        p = 1
        while n:
            if n % 10 != 0:
                res.append(n % 10 * p)
            n //= 10
            p *= 10
        
        return res[::-1]
''',
    call='Solution().decimalRepresentation(5072)',
    expect=[5000, 70, 2],
    views=[
        dict(type='text', h=70, size=34, fn=_txt),
        dict(type='array', var='res', label='res（从低位到高位）', cell=130, h=200),
    ],
    watch=[('n', 'n', 'blue'), ('p', 'p', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 存放分离出的 10 进制分量',
        'p = 1': '`p` 记录当前数位对应的 10 的幂次，个位是 1',
        'while n': lambda S, B, r: (f'`n = {S.n}` 不为 0，还有数位没分离' if S.n else '`n = 0`：所有数位都处理完'),
        'if n % 10 != 0': lambda S, B, r: (f'个位 `{S.n % 10}` 非零 → 它和 `p` 的乘积是一个分量' if S.n % 10 else '个位是 0 → 这一位没有分量，跳过'),
        'res.append': '个位 × 位权：`{n % 10} × {p}` = =={n % 10 * p}==，加入 `res`',
        'n //= 10': '去掉个位：`n` → {n}',
        'p *= 10': '位权升一位：`p` → {p}',
        'return': '低位在前，倒序成降序：`{ret}`',
    },
    cards=dict(
        one_liner='模 10 取个位，除 10 去个位，位权同步 ×10',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['把正整数 `n` 拆成最少个 10 进制分量（一位数字 × 10 的幂）之和',
                 '结果按大小降序返回',
                 '本视频：`5072` → `[5000,70,2]`'],
        quote='题目实际上就是要将n中非零的个位、整十、整百、整千等拆分出来，于是只需使用模10除以10的方法逐位分离n的数位，同时使用一个变量p记录当前分离出来的位对应的10的幂次。',
        quote_src='—— yiduobo 题解原文',
        idea=['最少个数 = ==非零数位的个数==，每个非零数位单独成一个分量',
              '`n % 10` 取个位，`n //= 10` 丢掉个位，`p` 跟着乘 10',
              '低位先进 `res`，最后 `res[::-1]` 变降序'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：`n % 10 * p` 先取模再乘位权；个位为 0 时不加入',
                 '易错：`n //= 10` 与 `p *= 10` 要在每一轮都执行，即使该位为 0',
                 '原文已是 Python 3 写法的整除 `//`，无需修改'],
    ),
)
