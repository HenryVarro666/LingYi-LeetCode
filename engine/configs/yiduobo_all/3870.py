CONFIG = dict(
    num=3870, title='统计范围内的逗号', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='按位数分段计数',
    code='''
class Solution(object):
    def countCommas(self, n):
        
        length = 1
        p10 = 1
        res = 0
        while p10 * 10 - 1 < n:
            res += (length - 1) // 3 * p10 * 9
            p10 *= 10
            length += 1
        
        return res + (length - 1) // 3 * (n - p10 + 1)
''',
    call='Solution().countCommas(12345)',
    expect=11346,
    views=[
        dict(type='text', size=34, fn=lambda S: (
            f"`{S['length']}` 位数：每个有 `({S['length']}-1)//3 = {(S['length']-1)//3}` 个逗号，区间 `{10**(S['length']-1)} ~ {min(10**S['length']-1, S['n'])}`"
            if 'length' in S else '')),
        dict(type='text', size=34, fn=lambda S: (f"目前累计逗号 `res = {S['res']}`" if 'res' in S else '')),
    ],
    watch=[('n', 'n', 'blue'), ('length', 'length', 'orange'), ('p10', 'p10', 'pink'), ('res', 'res', 'green')],
    captions={
        'length = 1': '`length` 表示当前处理的数位数，从 1 位数开始',
        'p10 = 1': '`p10` 是当前位数的最小值：1、10、100……',
        'res = 0': '`res` 累计逗号总数',
        'while p10 * 10 - 1 < n': lambda S, B, r: (
            f'`{S.p10}×10-1 = {S.p10*10-1} < {S.n}`：{S.length} 位数全部在范围内 → 整段计算' if S.p10 * 10 - 1 < S.n
            else f'`{S.p10*10-1} >= {S.n}`：{S.length} 位数只算到 n，停止整段计算'),
        'res += (length - 1)': '共 `9×{p10}` = {p10*9} 个 {length} 位数，每个 `{(length-1)//3}` 个逗号 → `res = {res}`',
        'p10 *= 10': '`p10` → {p10}，进入下一个位数',
        'length += 1': '`length` → {length}',
        'return res': '最后一段只到 n：`{n} - {p10} + 1 = {n-p10+1}` 个数，各 `{(length-1)//3}` 个逗号 → 总共 =={ret}==',
    },
    cards=dict(
        one_liner='逗号数只和位数有关：按 10 的幂次分段，一段一段数',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['把 `1..n` 都写成标准格式（每三位一个逗号），求逗号总数',
                 '不足四位的数没有逗号',
                 '示例：`n = 1002` → `3`（1,000 / 1,001 / 1,002）'],
        quote='对于一个length位数，其具有(length - 1) // 3个逗号，同时一共有从10^(length - 1)到10^length - 1，这一共有9 * 10^(length - 1)个length位数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`length` 位数每个有 `(length-1)//3` 个逗号',
              '`p10` 从 1 开始每次乘 10，整段 `9 × p10` 个数一起加',
              '最后一段只到 n：`(n - p10 + 1)` 个数，单独算'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '循环条件 `p10 * 10 - 1 < n`：整段完全在 n 以内才整段加',
                 '原文用 `//` 本来就是整数除法，无需修改',
                 '第二题 n 可达 10^15，同样的做法直接适用'],
    ),
)
