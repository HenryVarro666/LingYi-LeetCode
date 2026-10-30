def _txt(S):
    s, k = S['s'], S['k']
    w = s.split(' ')
    return f"`split(' ')` 得到 {len(w)} 个单词；取前 `{k}` 个：==" + ' '.join(w[:k]) + '=='


CONFIG = dict(
    num=1816, title='截断句子', difficulty='Easy', category='字符串',
    author='yiduobo', technique='split + join',
    tags=[],
    code='''
class Solution(object):
    def truncateSentence(self, s, k):

        return ' '.join(s.split(' ')[:k])
''',
    call='Solution().truncateSentence("Hello how are you Contestant", 4)',
    expect='Hello how are you',
    views=[
        dict(type='text', fn=lambda S: f"`k = {S['k']}`：只保留前 {S['k']} 个单词", size=30, h=60),
        dict(type='array', var=lambda S: S['s'].split(' '), label='s.split(" ")（按空格切开）', h=230, cell=170,
             color=lambda S, i, v: 'green' if i < S['k'] else None,
             dim=lambda S, i, v: i >= S['k']),
        dict(type='text', fn=_txt, size=28),
    ],
    watch=['s', 'k'],
    captions={
        'return': "先 `split(' ')` 按空格切成单词，`[:{k}]` 取前 {k} 个，再用空格 `join` 拼回去 → =={ret}==",
    },
    cards=dict(
        one_liner='按空格切开，取前 k 个单词，再拼回去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['句子 `s` 是用单个空格分隔的单词，没有首尾空格',
                 '截断：只保留前 `k` 个单词',
                 '示例：`s = "Hello how are you Contestant"`，`k = 4` → `"Hello how are you"`'],
        quote='比较基础的题目，我这里直接用了python的split和join，不过个人感觉更好的写法应该一趟遍历，尝试去找句子中第k个空格。',
        quote_src='—— yiduobo 题解原文',
        idea=['Python 里 `split` + 切片 + `join` 一行搞定',
              '更省空间的写法：一趟遍历，数到第 `k` 个空格就返回它前面的内容',
              '找不到第 `k` 个空格，说明句子正好 `k` 个单词，返回整个句子'],
        after=[dict(heading='作者提到的另一种写法', lines=[
            '从左到右扫描 `s`，数空格的个数',
            '数到第 `k` 个空格：返回 `s[:i]`（空格前面的内容）',
            '一直没数到：句子单词数 ≤ `k`，返回整个 `s`',
            '这样不用建单词列表，额外空间 `O(1)`（不计结果）'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`split(" ")` 的切片 `[:k]` 即使 `k` 超过单词数也不会越界',
                 '题目保证单词间只有一个空格，所以 `join` 后与原文一致',
                 '原文为 Python 2 风格，本题无需改动，代码照搬原文'],
    ),
)
