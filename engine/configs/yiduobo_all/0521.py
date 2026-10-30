CONFIG = dict(
    num=521, title='最长特殊序列 Ⅰ', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='子序列关系推导',
    tags=['灵神题单', '贪心算法', '难度分 1400'],
    code='''
class Solution(object):
    def findLUSlength(self, a, b):

        if a == b:
            return -1
        
        return max(len(a), len(b))
''',
    call='Solution().findLUSlength("abc", "ab")',
    expect=3,
    views=[
        dict(type='string', var='a', label='a', h=200),
        dict(type='string', var='b', label='b', h=200),
        dict(type='text', fn=lambda S: f"`len(a) = {len(S['a'])}`，`len(b) = {len(S['b'])}`：较长的那个串不可能是较短串的子序列" if 'a' in S else '', size=28, h=120),
    ],
    watch=[('a', 'a'), ('b', 'b'), ('len(a)', 'len(a)', 'blue'), ('len(b)', 'len(b)', 'pink')],
    captions={
        'if a == b': lambda S, B, r: ('`a == b`：A 是 B 的子序列，B 也是 A 的子序列 → ==没有特殊序列==' if S.a == S.b
                                       else f'`a == b`？不相等 → 往下找较长的那个'),
        'return -1': '互为子序列，A 的任意子序列都是 B 的子序列 → 返回 ==-1==',
        'return max': lambda S, B, ret: f'长度 `{len(S.a)}` 和 `{len(S.b)}` 不同：较长字符串不是较短的子序列，整串就是特殊序列 → ==返回 {ret}==',
    },
    cards=dict(
        one_liner='A 是 B 的子序列，A 的所有子序列就都不特殊',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求两个字符串中「最长的特殊序列」长度：某串独有、不是另一个串的子序列',
                 '本视频示例：`a = "abc"`，`b = "ab"` → `3`',
                 '不存在则返回 `-1`'],
        quote='若A是B的子序列，那么A的任意子序列也一定是B的子序列，换言之，就是A的任意子序列必然不是特殊子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度相等且 `a == b`：互为子序列 → `-1`；不相等，选 A 或 B 都行',
              '长度不等：较长串不可能是较短串的子序列 → 答案就是较长的长度',
              '两种情况合并成：相等 `-1`，否则 `max(len)`'],
        summary=['时间 `O(n)`（比较字符串），空间 `O(1)`',
                 '易错点：长度相等但内容不同，答案仍是该长度，不是 -1',
                 '原文为 Python 2 风格写法（`class Solution(object)`），代码在 Python 3 下无需改动',
                 '延伸 522 题：按长度排序，再逐个用贪心匹配检查子序列'],
        after=[dict(heading='长度不等 vs 长度相等', lines=['长度不等：较长串必然不是较短串的子序列 → 答案是较长的长度',
                                                  '长度相等且 `a == b`：互为子序列 → `-1`',
                                                  '长度相等但 `a != b`：选 A 或 B 都可以 → 答案是该长度'])],
    ),
)
