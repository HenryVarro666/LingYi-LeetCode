CONFIG = dict(
    num=3726, title='移除十进制表示中的所有零', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='除 10 模 10 分离数位 · 倒序组装',
    tags=[],
    code='''
class Solution(object):
    def removeZeros(self, n):
        
        digits = []
        while n:
            if n % 10 != 0:
                digits.append(n % 10)
            n //= 10
        
        res = 0
        for v in digits[::-1]:
            res = res * 10 + v
        return res
''',
    call='Solution().removeZeros(1020030)',
    expect=123,
    views=[
        dict(type='text', fn=lambda S: f"n = `{S['n']}`" if 'n' in S else '', size=30),
        dict(type='array', var='digits', label='digits（分离出的非零数位，低位在前）', cell=84,
             color=lambda S, i, v: 'green' if S.get('_line', 0) >= 11 and S.get('res') and i >= len(S['digits']) - len(str(S['res'])) else None),
        dict(type='text', fn=lambda S: f"res = ==`{S['res']}`==" if 'res' in S else '', size=30),
    ],
    watch=['n', 'digits', 'v', ('res', 'res', 'green')],
    captions={
        'digits = []': '`digits` 用来存 n 的所有非零数位',
        'while n': lambda S, B, r: (f'`n = {S.n}` 不为 0，继续分离数位' if S.n else '`n = 0`：数位分离完了'),
        'if n % 10': lambda S, B, r: (f'`n % 10 = {S.n % 10}` ≠ 0 → 是个有效数位' if S.n % 10 else '`n % 10 = 0` → ==这一位是零，丢掉=='),
        'digits.append': '把最低位 `{n % 10}` 记进 digits：`{digits}`',
        'n //= 10': '`n //= 10` 去掉最低位，`n` → {n}',
        'res = 0': '分离完成。因为最低位先进的 digits，要==倒序==遍历来组装',
        'for v in': lambda S, B, r: (f'倒序取出 `v = {S.v}`（当前最高的剩余数位）' if len(str(S.res)) < len(S.digits) else '数位都接完了，遍历结束'),
        'res = res * 10': '`res = {B.res} × 10 + {v} = {res}`：把 v 接在末尾',
        'return res': '数位全部接完，返回 `{res}`',
    },
    cards=dict(
        one_liner='先把非零数位全拆出来，再倒着拼回去',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['给正整数 `n`，把十进制表示里所有的 0 删掉，返回结果',
                 '示例：`1020030` → `123`',
                 '本视频：`n = 1020030`'],
        quote='使用除以10模10的方案分离出n的所有数位，并丢弃掉其中值为0的数位。分离完成后，倒序遍历这些数位，将这些数位组装成答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：`n % 10` 取最低位，非零才进 `digits`，然后 `n //= 10`',
              '最低位先进，所以 `digits` 是反的',
              '第二遍：倒序遍历，`res = res * 10 + v` 逐位接回'],
        summary=['时间 `O(log n)`，空间 `O(log n)`（存了数位列表）',
                 '易错：必须倒序组装，否则数位顺序反了',
                 '原文为 Python 2 风格，这里只删去了类型说明，`//` 原文已是整除',
                 '对比灵神：灵神一遍搞定，用 `pow10` 直接把数位放到对的位置，不需要列表'],
    ),
)
