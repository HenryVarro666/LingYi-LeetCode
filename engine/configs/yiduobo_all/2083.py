CONFIG = dict(
    num=2083, title='求以相同字母开头和结尾的子串总数', difficulty='Medium', category='字符串',
    author='yiduobo', technique='哈希表计数 · n(n+1)/2',
    code='''
class Solution(object):
    def numberOfSubstrings(self, s):

        cnt = {}
        for char in s:
            cnt[char] = cnt.get(char, 0) + 1
        
        res = 0
        for v in cnt.values():
            res += v * (v + 1) // 2
        
        return res
''',
    call='Solution().numberOfSubstrings("abcab")',
    expect=7,
    views=[
        dict(type='string', var='s', h=170, label='s'),
        dict(type='map', var='cnt', h=200, label='cnt（每个字母出现次数）'),
        dict(type='text', fn=lambda S: f"`{S['v']}` 个相同字母 → `{S['v']} × {S['v']+1} ÷ 2` = =={S['v']*(S['v']+1)//2}==" if 'v' in S else '', size=32),
    ],
    watch=['char', ('v', 'v', 'cyan'), ('res', 'res', 'green')],
    captions={
        'cnt = {}': '`cnt` 记录每种字符出现的次数',
        'for char': '读到字符 `{char!r}`',
        'cnt[char] =': '`cnt[{char!r}]` → =={cnt[char]}==',
        'res = 0': '`res` 累计合法子串数',
        'for v in': '字符出现 `{v}` 次',
        'res +=': '选两端：下标不同 `C({v},2)={v*(v-1)//2}`，再加单字符 `{v}` 个 = `{v*(v+1)//2}`：`res` → =={res}==（原文 `/` 已改为 `//`）',
        'return res': '总数 `{res}`',
    },
    cards=dict(
        one_liner='同一字母出现 n 次，就有 n(n+1)/2 个合法子串',
        complexity='时间 `O(n)`，空间 `O(1)`（字母表大小）',
        problem=['给字符串 `s`，统计以==相同字母开头和结尾==的子串个数',
                 '单个字符本身也算一个子串',
                 '示例：`"abcab"` → `7`（a:3，b:3，c:1）'],
        quote='若整个字符串中有n个s[index]，那么以s[index]为两端的子串就一共有n * (n +1) / 2个。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，用哈希表数出每个字母的个数',
              '以某字母为结尾，前面有 `k` 个相同的（含自己），就有 `k` 个合法子串',
              '累加 `1+2+...+n = n(n+1)/2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '单个字符也算一个子串，所以是 `n(n+1)/2` 而不是 `n(n-1)/2`',
                 '答案可能很大，Python 不会溢出'],
    ),
)
