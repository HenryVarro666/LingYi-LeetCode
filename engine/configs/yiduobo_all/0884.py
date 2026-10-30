CONFIG = dict(
    num=884, title='两句话中的不常见单词', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表统计词频',
    tags=[],
    code='''
class Solution(object):
    def uncommonFromSentences(self, A, B):

        word_dict = {}
        for word in A.split(' '):
            word_dict[word] = word_dict.get(word, 0) + 1
        for word in B.split(' '):
            word_dict[word] = word_dict.get(word, 0) + 1
        
        res = []
        for word, freq in word_dict.items():
            if freq == 1:
                res.append(word)
                
        return res
''',
    call="Solution().uncommonFromSentences('this apple is sweet apple', 'this is sour')",
    expect=['sweet', 'sour'],
    views=[
        dict(type='map', var='word_dict', h=330, font=26),
        dict(type='array', var='res', label='res', h=120),
    ],
    watch=['word', 'freq', ('res', 'res', 'green')],
    captions={
        'word_dict = {}': '`word_dict` 统计每个单词在==两句话合计==出现的次数',
        'for word in A.split': '遍历句子 A 的单词，当前 `{word!r}`',
        'for word in B.split': '遍历句子 B 的单词，当前 `{word!r}`',
        'word_dict[word] = word_dict.get': '`{word!r}` 的次数：`{B.word_dict.get(word, 0)} + 1` = =={word_dict[word]}==',
        'res = []': '`res` 收集只出现一次的单词',
        'for word, freq': '检查 `{word!r}`：合计出现 `{freq}` 次',
        'if freq == 1': '`freq = {freq}`，{"==等于 1== → 在其中一句出现一次、另一句没有，是不常见单词" if freq == 1 else "不是 1：出现多次或两句都有 → 不算"}',
        'res.append': '`{word!r}` 加入答案：`res = {res}`',
        'return res': '不常见单词：`{ret}`',
    },
    cards=dict(
        one_liner='「只在一句出现」等价于「两句合计只出现一次」',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['句子是用空格隔开的单词；单词在一句中出现一次、在另一句中没出现，就是不常见单词',
                 '返回所有不常见单词，顺序不限',
                 '本视频：`A="this apple is sweet apple"`，`B="this is sour"` → `["sweet","sour"]`'],
        quote='综合起来就是，在两个句子中总共只出现了一次。于是可以遍历两个句子中的所有单词并统计每个单词出现的次数，然后找出那些只出现了一次的单词。',
        quote_src='—— yiduobo 题解原文',
        idea=['A 中一次且 B 中没有，或 B 中一次且 A 中没有',
              '两种情况合并：两句话==总次数 = 1==',
              '把两个句子的单词全部计入同一张哈希表，再挑出次数为 1 的'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：A 内部重复的词（如 `apple`）也不算，因为次数 ≥ 2',
                 '不能只看 A、B 各自的次数，要==合并统计==',
                 '原文代码已是 Python 3 写法，未做修改'],
    ),
)
