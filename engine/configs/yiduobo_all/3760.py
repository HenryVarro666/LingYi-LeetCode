CONFIG = dict(
    num=3760, title='不同首字母的子字符串数目', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='集合统计字符种数',
    tags=['灵神题单', '难度分 1364'],
    code='''
class Solution(object):
    def maxDistinct(self, s):
        
        char = set()
        for c in s:
            char.add(c)
        return len(char)
''',
    call='Solution().maxDistinct("abacbd")',
    expect=4,
    views=[
        dict(type='string', var='s', h=200, label='s（绿色 = 该字母已进集合）',
             color=lambda S, i, v: 'green' if 'char' in S and v in S['char'] else None),
        dict(type='set', var='char', h=200, fmt=lambda x: str(x)),
    ],
    watch=['c', ('种数', 'len(char)', 'green')],
    captions={
        'char = set()': '准备一个集合 `char`，专门记录出现过的字符',
        'char.add': '把 `{c}` 加入集合；已有的字符不会重复 → 现有 `{len(char)}` 种',
        'return len': '遍历完，集合大小 = 字符种数 = =={ret}==，这就是最多能划分的子串数',
    },
    cards=dict(
        one_liner='最多划分数 = 字符的种数，一趟遍历数出来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把字符串 `s` 拆成若干子串，每个子串开头字符都不同',
                 '问最多能拆出多少个',
                 '示例：`"abab"` → `2`'],
        quote='最终结果的上限是s中不同字符的种数，因为最好的情况就是以每种字符开头的子串都有一个，而构造这种情况是很容易的。',
        quote_src='—— yiduobo 题解原文',
        idea=['设有 k 种字符，首次出现的位置依次为 p[0]…p[k-1]',
              '按这些位置切开：s[p[0]:p[1]]、s[p[1]:p[2]]…最后一段到结尾',
              '这样恰好得到 k 段且首字符各不相同，所以答案就是 k'],
        summary=['时间 `O(n)`，空间 `O(1)`（字符集只有 26 个）',
                 '关键是先证上限，再构造能取到',
                 '原文只多了一个空行，代码未改动'],
    ),
)
