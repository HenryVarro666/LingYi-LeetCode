CONFIG = dict(
    num=266, title='回文排列', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='集合配对 · 统计落单字符',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def canPermutePalindrome(self, s):

        char_set = set()
        for char in s:
            if char not in char_set:
                char_set.add(char)
            else:
                char_set.remove(char)
        
        return len(char_set) <= 1
''',
    call='Solution().canPermutePalindrome("carerac")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（黄 = 当前读到的字符）', cell=84,
             color=lambda S, i, v: 'yellow' if S.get('char') == v else None),
        dict(type='set', var='char_set', label='char_set（里面都是“落单”的字符）', fmt=lambda x: f"'{x}'"),
        dict(type='text', fn=lambda S: f"落单字符数 = ==`{len(S['char_set'])}`==（回文串最多允许 1 个）" if 'char_set' in S else '', size=28),
    ],
    watch=['char', ('落单数', 'len(char_set)', 'green')],
    captions={
        'char_set = set()': '空集合：记录当前==落单==的字符',
        'for char in s': lambda S, B, r: (f"读到字符 `{S.char}`" if S.get('char') != B.get('char') else '遍历完了'),
        'if char not in char_set': lambda S, B, r: (f"`'{S.char}'` 不在集合里 → 它目前落单" if S.char not in B.char_set
                                                    else f"`'{S.char}'` 已在集合里 → 凑成一对"),
        'char_set.add': '第一次见（或配对被消掉后再见）：`{char}` 加入集合，成为落单字符',
        'char_set.remove': '`{char}` 又出现一次，和集合里的那个凑成一对 → ==移出集合==',
        'return': lambda S, B, r: f"落单字符 `{len(S.char_set)}` 个，≤ 1 → `{r}`",
    },
    cards=dict(
        one_liner='成对的字符互相抵消，最后落单的不超过 1 个就行',
        complexity='时间 `O(n)`，空间 `O(k)`，`k` 为字符种类数',
        problem=['给定字符串 `s`，判断它的某个排列能否成为==回文串==',
                 '示例：`"code"` → `false`，`"aab"` → `true`',
                 '本视频：`"carerac"` → `true`'],
        quote='对于一个回文串，除中心字符外的所有字符都是成对出现的，换言之，回文串中落单的字符数量只能是0个或者1个。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历 `s`：字符不在集合就加入，在集合就移出',
              '遍历完，集合里剩下的就是出现奇数次的字符',
              '剩余个数 `<= 1`，奇数长度时它放中间，即可组成回文'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '空串、偶数长度时集合应为空；奇数长度时恰好剩 1 个',
                 '原文为 Python 2 风格，本题代码无需改动',
                 '同类思路：用异或或奇偶计数判断出现次数的奇偶'],
    ),
)
