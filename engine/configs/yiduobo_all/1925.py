CONFIG = dict(
    num=1925, title='统计平方和三元组的数目', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='平方集合 + 双层枚举',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def countTriples(self, n):

        pow_set = set()
        for c in range(1, n + 1):
            pow_set.add(c * c)
        
        res = 0
        for a in range(1, n + 1):
            for b in range(a + 1, n + 1):
                if a * a + b * b in pow_set:
                    res += 2
        
        return res
''',
    call='Solution().countTriples(6)',
    expect=2,
    views=[
        dict(type='set', var='pow_set', label='pow_set：1..n 的平方', fmt=lambda x: str(x), h=190, font=30),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"a=={S['a']}==, b=={S['b']}==：a²+b² = =={S['a']**2+S['b']**2}=={'，在集合里！' if S['a']**2+S['b']**2 in S['pow_set'] else '，不在集合里'}" if 'b' in S and 'a' in S and S.get('res') is not None
                           else '先把所有 c² 放进集合，之后判断 a²+b² 是否在里面')),
        dict(type='text', h=90, size=30, fn=lambda S: f"已找到的三元组个数 res = =={S['res']}==" if S.get('res') is not None else ''),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), ('c', 'c'), ('res', 'res', 'green')],
    captions={
        'pow_set = set()': '`pow_set` 存放 `1..n` 每个数的平方',
        'pow_set.add': '`{c}² = {c*c}` 加入集合',
        'res = 0': '`res` 统计三元组个数',
        'for a in range(1, n + 1)': lambda S, B, r: (f'枚举 `a = {S.a}`' if 'a' not in B or S.a != B.a else '枚举结束'),
        'for b in range(a + 1, n + 1)': lambda S, B, r: (f'枚举 `b = {S.b}`（从 a+1 开始，保证 a < b）' if ('b' in S and ('b' not in B or S.b != B.b or S.a != B.a))
                                                       else '这个 a 的 b 都枚举完了'),
        'if a * a + b * b in pow_set': lambda S, B, r: (f'`{S.a}² + {S.b}² = {S.a**2 + S.b**2}`：是平方数 → ==(a,b,c) 成立==' if S.a**2+S.b**2 in S.pow_set
                                                         else f'`{S.a}² + {S.b}² = {S.a**2 + S.b**2}`：不是 1..n 里的平方数'),
        'res += 2': '`(a,b,c)` 和 `(b,a,c)` 各算一次，`res` += 2 → {res}',
        'return res': '一共 `{res}` 个平方和三元组',
    },
    max_steps=80,
    cards=dict(
        one_liner='数据范围小：平方存进集合，两层循环查一下',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['数出满足 `a²+b²=c²` 且 `1 <= a,b,c <= n` 的整数三元组 `(a,b,c)`',
                 '`(3,4,5)` 和 `(4,3,5)` 算两个',
                 '示例：`n=10` → `4`；本视频 `n=6` → `2`'],
        quote='题目要求寻找一定范围内所有的勾股数对，感觉应该有数学方法来构造，不过没有什么思路。题目的范围很小，直接使用平方枚举加哈希表，甚至三次方枚举都可以。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n <= 250`，不必找公式：枚举 `a < b` 就够',
              '把 `1..n` 的平方放进集合，`a²+b²` 在集合里就说明有对应的 c',
              '`b` 从 `a+1` 开始，每找到一个就加 2（交换 a、b 也成立）'],
        summary=['时间 `O(n²)`，空间 `O(n)`，`n=250` 完全够用',
                 '`b` 从 `a+1` 开始避免重复，再用 `res += 2` 补回交换的那个',
                 '`a = b` 不会成立（`2a²` 不是完全平方数）',
                 '原文无需改动 Python 3'],
    ),
)
