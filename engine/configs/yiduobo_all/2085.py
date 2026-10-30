CONFIG = dict(
    num=2085, title='统计出现过一次的公共字符串', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='两个哈希表计数',
    code='''
class Solution(object):
    def countWords(self, words1, words2):

        cnt1 = {}
        cnt2 = {}
        for word in words1:
            cnt1[word] = cnt1.get(word, 0) + 1
        for word in words2:
            cnt2[word] = cnt2.get(word, 0) + 1
        
        res = 0
        for word, cnt in cnt1.items():
            if cnt == 1 and cnt2.get(word, 0) == 1:
                res += 1
        
        return res
''',
    call='Solution().countWords(["leetcode","is","amazing","as","is"], ["amazing","leetcode","is"])',
    expect=2,
    views=[
        dict(type='map', var='cnt1', h=230, label='cnt1（words1 计数）'),
        dict(type='map', var='cnt2', h=230, label='cnt2（words2 计数）'),
        dict(type='text', fn=lambda S: f"当前 `{S['word']}`：cnt1=`{S['cnt']}`，cnt2=`{S['cnt2'].get(S['word'], 0)}`" if 'cnt' in S and 'word' in S and 'res' in S else '', size=30),
    ],
    watch=['word', ('res', 'res', 'green')],
    captions={
        'cnt1 = {}': '`cnt1` 统计 words1 里每个字符串出现几次',
        'cnt2 = {}': '`cnt2` 统计 words2 的',
        'cnt1[word] =': '`cnt1[{word!r}]` → =={cnt1[word]}==',
        'cnt2[word] =': '`cnt2[{word!r}]` → =={cnt2[word]}==',
        'res = 0': '`res` 统计满足条件的字符串数',
        'for word, cnt': '看 words1 里的 `{word!r}`，出现 `{cnt}` 次',
        'if cnt == 1': '`{word!r}`：words1 出现 `{cnt}` 次，words2 出现 `{cnt2.get(word, 0)}` 次 → {"两边都恰好一次，计入" if cnt == 1 and cnt2.get(word, 0) == 1 else "不满足，跳过"}',
        'res += 1': '`res` → =={res}==',
        'return res': '一共 `{res}` 个',
    },
    cards=dict(
        one_liner='两个哈希表数次数，两边都恰好 1 次才算',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['给两个字符串数组 `words1`、`words2`',
                 '统计在两个数组中==都恰好出现一次==的字符串个数',
                 '示例：`["leetcode","is","amazing","as","is"]` 与 `["amazing","leetcode","is"]` → `2`'],
        quote='使用哈希表统计words1和words2中每个字符串出现的次数，然后统计在word1和word2中都出现了一次的字符串的数目即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['分别给两个数组建计数表 `cnt1`、`cnt2`',
              '遍历 `cnt1`，要求自己次数为 1 且 `cnt2` 里也为 1',
              '`cnt2.get(word, 0)` 处理 words2 里没有的情况'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '`is` 在 words1 出现两次，所以不算',
                 '用 `.get(word, 0)`，避免 KeyError',
                 '原文已是 Python 3 可运行的写法，无需修改'],
    ),
)
