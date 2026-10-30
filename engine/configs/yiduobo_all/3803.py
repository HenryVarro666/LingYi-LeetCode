CONFIG = dict(
    num=3803, title='统计残差前缀', difficulty='Easy', category='字符串',
    author='yiduobo', technique='集合逐前缀累加',
    tags=[],
    code='''
class Solution(object):
    def residuePrefixes(self, s):
        
        cnt = set()
        res = 0
        for index, c in enumerate(s):
            cnt.add(c)
            if len(cnt) == (index + 1) % 3:
                res += 1
        
        return res
''',
    call="Solution().residuePrefixes('abbaac')",
    expect=3,
    views=[
        dict(type='string', var='s', h=200, cell=90, pointers={'index': 'pink'},
             window=('0', 'index'), label='s（框 = 前缀 s[:index+1]）'),
        dict(type='set', var='cnt', h=200, fmt=lambda x: str(x), label='cnt：当前前缀的字符集'),
        dict(type='text', size=32, fn=lambda S: (f"字符数 `{len(S['cnt'])}`  vs  前缀长度 `{S['index'] + 1}` % 3 = `{(S['index'] + 1) % 3}`" if 'index' in S and S.get('cnt') else '')),
    ],
    watch=[('index', 'index', 'pink'), ('len(cnt)', 'len(cnt)', 'cyan'), ('res', 'res', 'green')],
    captions={
        'cnt = set()': '`cnt` 记录前缀里的不同字符',
        'cnt.add(c)': '前缀 `s[:{index + 1}]` 比上一个前缀多了 `{c}`：直接加入，`cnt` 有 =={len(cnt)}== 个字符',
        'if len(cnt)': lambda S, B, r: (f'字符数 `{len(S.cnt)}` == 长度 `{S.index + 1}` % 3 = `{(S.index + 1) % 3}` → 是残差前缀' if len(S.cnt) == (S.index + 1) % 3
                                        else f'字符数 `{len(S.cnt)}` != `{(S.index + 1) % 3}` → 不是'),
        'res += 1': '统计这个前缀：`res` = =={res}==',
        'return res': '全部前缀看完，残差前缀共 `{res}` 个',
    },
    cards=dict(
        one_liner='后一个前缀 = 前一个前缀 + 一个字符，集合可以直接沿用',
        complexity='时间 `O(n)`，空间 `O(26)`',
        problem=['前缀中不同字符的数量 == `len(prefix) % 3` → 残差前缀',
                 '求 `s` 中残差前缀的数量',
                 '本视频：`abbaac` → `3`'],
        quote='对于当前的前缀s[:index + 1]，是在上一个前缀s[:index]的基础上，新增字符s[index]得到的，因此可以在上一个前缀字符集的基础上，加入s[index]得到当前前缀的字符集。',
        quote_src='—— yiduobo 题解原文',
        idea=['这是题目里的「隐藏条件」：前缀逐个变长，只多一个字符',
              '所以一趟遍历、一个集合，不用对每个前缀重新数',
              '第 `index` 个字符对应的前缀长度是 `index + 1`，用它模 3 去比较'],
        summary=['时间 `O(n)`，空间 `O(26)`',
                 '易错：前缀长度是 `index + 1`，不是 `index`',
                 '原文为 Python 2 风格 `class Solution(object)`，代码无需改动',
                 '对比灵神：灵神在集合大小到 3 时提前 `break`，这里一直遍历到结尾'],
    ),
)
