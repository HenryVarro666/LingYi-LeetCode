CONFIG = dict(
    num=3783, title='整数的镜像距离', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模 10 拆数位再重组',
    code='''
class Solution(object):
    def mirrorDistance(self, n):
        
        m = n
        digits = []
        while m:
            digits.append(m % 10)
            m //= 10
        
        m = 0
        for d in digits:
            m = m * 10 + d
        return abs(n - m)
''',
    call='Solution().mirrorDistance(1230)',
    expect=909,
    views=[
        dict(type='text', size=32, fn=lambda S: (f"拆出的数位 `{S['digits']}`；已拼出 `m = {S['m']}`" if 'd' in S else f"`m = {S['m']}`，数位 `{S['digits']}`") if 'digits' in S else ''),
        dict(type='array', var='digits', h=220, label='digits（从个位到最高位）'),
    ],
    watch=['n', 'm', 'd'],
    captions={
        'digits.append': '`m % 10 = {m % 10}` 是当前最低位，放进 `digits` → `{digits}`',
        'm //= 10': '`m //= 10` 去掉最低位，`m` 变成 =={m}==',
        'm = m * 10 + d': '把 `{d}` 接到末尾：`m * 10 + d` = =={m}==',
        'return abs': '`abs(n - m) = abs({n} - {m})` = =={ret}==',
    },
    cards=dict(
        one_liner='先拆出数位，再按顺序重新拼成反转数',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['镜像距离是 `n` 与 `reverse(n)` 之差的绝对值',
                 '示例：`n=25` → `|25-52| = 27`；`n=10` → `|10-1| = 9`',
                 '演示用：`n=1230` → `|1230-321| = 909`'],
        quote='那么在这里就可以按模10除以10的方法先将n的数位分离出来，得到数组digits。然后直接正序遍历digits，使用乘以10再加上当前位上元素的方法就能构造出n反转后的整数',
        quote_src='—— yiduobo 题解',
        idea=['`m % 10` 取最低位，`m //= 10` 去掉它，数位按从低到高存入 `digits`',
              '低位先入表，所以正序遍历 `digits` 就是反转后的高位到低位',
              '每次 `m * 10 + d` 把数位接到末尾'],
        summary=['时间 `O(log n)`，空间 `O(log n)`（数位数组）',
                 '末尾是 0 的数：0 最先入 `digits`，重组时落在高位，自动消失',
                 '最后取绝对值，因为反转数可能更大'],
    ),
)
