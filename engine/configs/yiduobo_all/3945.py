def _fq(S):
    f = S.get('freq')
    if f is None:
        return '输入 `n = 1223`'
    return f"剩下的 n = ==`{S.get('n')}`=="


CONFIG = dict(
    num=3945, title='计算数字频率得分', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='哈希表统计频率 + 按定义求和',
    code='''
class Solution(object):
    def digitFrequencyScore(self, n):
        
        freq = {}
        while n:
            d = n % 10
            n //= 10
            freq[d] = freq.get(d, 0) + 1
        
        res = 0
        for d in freq:
            res += d * freq[d]
        
        return res
''',
    call='Solution().digitFrequencyScore(1223)',
    expect=8,
    views=[
        dict(type='text', h=110, size=38, fn=lambda S: f"剩下的 n = ==`{S['n']}`==" if 'n' in S else ''),
        dict(type='map', var='freq', label='freq（数字 d → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=36),
        dict(type='text', h=110, size=32, fn=lambda S: f"得分 res = ==`{S['res']}`==" if 'res' in S else ''),
    ],
    watch=[('n', 'n', 'blue'), ('d', 'd', 'pink'), ('res', 'res', 'green')],
    captions={
        'freq = {}': '`freq` 记录每种数字出现的次数',
        'while n': lambda S, B, r: (f'`n = {S.n}` 非 0，继续分离数位' if S.n else '`n = 0`：数位分离完 → 结束'),
        'd = n % 10': '模 10 取出个位 `d = {d}`',
        'n //= 10': '除以 10 去掉个位：`n` = =={n}==',
        'freq[d] =': '`freq[{d}]` 计数加一 → =={freq[d]}==',
        'res = 0': '接下来遍历 `freq`，按定义累加 `d * freq[d]`',
        'for d in freq': '取一种数字 `d = {d}`',
        'res += d * freq[d]': '贡献 `{d} * {freq[d]}` = {d * freq[d]} → `res` = =={res}==',
        'return res': '得分 `{res}`',
    },
    cards=dict(
        one_liner='用哈希表统计每个数位的频率，再按定义求和',
        complexity='时间 `O(log n)`，空间 `O(1)`（最多 10 种数字）',
        problem=['得分 = 对每个不同数字 `d`，累加 `d * freq(d)`',
                 '示例：`n = 122` → `1×1 + 2×2 = 5`',
                 '本视频：`n = 1223` → `8`'],
        quote='按照题目描述直接模拟计算即可。使用模10除以10的方法分离n的所有数位d，并使用哈希表freq记录其中每种d出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先分离数位：`n % 10` 取个位，`n //= 10` 去掉个位',
              '`freq` 记每种数字的次数',
              '再遍历 `freq`，把 `d * freq[d]` 累加进答案'],
        summary=['时间 `O(log n)`，空间 `O(1)`：数字只有 0–9',
                 '数字 0 也会进 `freq`，但贡献为 0，不影响答案',
                 '对比灵神：其实 `d * freq[d]` 之和就是数位和，可省掉哈希表',
                 '原文为 Python 2 写法，整数除法已是 `//`，无需改动'],
    ),
)
