CONFIG = dict(
    num=771, title='宝石与石头', difficulty='Easy', category='位运算',
    author='yiduobo', technique='哈希集合',
    code='''
class Solution(object):
    def numJewelsInStones(self, J, S):

        j_set = set()
        for char in J:
            j_set.add(char)
        
        res = 0
        for char in S:
            if char in j_set:
                res += 1
        
        return res
''',
    call='Solution().numJewelsInStones("aA", "aAAbbbb")',
    expect=3,
    views=[
        dict(type='string', var='J', label='J（宝石类型）', h=160),
        dict(type='set', var='j_set', fmt=lambda x: str(x), h=160),
        dict(type='string', var='S', label='S（我拥有的石头）', h=220,
             color=lambda S, i, v: ('green' if v in S['j_set'] else None) if 'res' in S else None),
    ],
    watch=['char', ('res', 'res', 'green')],
    captions={
        'j_set = set()': '建一个空集合，存放宝石类型',
        'for char in J': '取宝石 `{char}`',
        'j_set.add': '`{char}` 加入集合，现在是 `{sorted(j_set)}`',
        'res = 0': '`res` 统计石头里的宝石数',
        'for char in S': '检查石头 `{char}`',
        'if char in j_set': lambda S, B, r: (f'`{S.char}` 在集合里 → ==是宝石==' if S.char in S.j_set else f'`{S.char}` 不在集合里 → 普通石头'),
        'res += 1': '`res` → {res}',
        'return res': '一共 `{res}` 块宝石',
    },
    cards=dict(
        one_liner='用哈希集合记下宝石，逐个查石头',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['`J` 的每个字符是一种宝石类型，`S` 的每个字符是一块石头',
                 '数一数 `S` 里有多少块是宝石，区分大小写',
                 '示例：`J="aA"`，`S="aAAbbbb"` → `3`'],
        quote='比较基础的题目，使用哈希表统计J中出现的所有字符，然后遍历S，若当前字符在哈希表中则将答案加一即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `J` 里的字符全放进集合，查询是 `O(1)`',
              '再扫一遍 `S`，在集合里就答案加一'],
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '大小写是不同类型，`a` 和 `A` 各算各的',
                 '对比灵神：用位运算 mask 代替哈希集合，空间降到 `O(1)`'],
    ),
)
