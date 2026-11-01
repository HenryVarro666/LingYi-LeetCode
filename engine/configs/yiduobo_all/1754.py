def _top(S):
    if 'p1' not in S:
        return ''
    a, b = S['word1'][S['p1']:], S['word2'][S['p2']:]
    return f"word1[p1:] = `{a}`　word2[p2:] = `{b}`"


CONFIG = dict(
    num=1754, title='构造字典序最大的合并字符串', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='双指针归并 · 拼接后比较',
    tags=['贪心与思维', '字符串', '难度分 1829'],
    code='''
class Solution(object):
    def largestMerge(self, word1, word2):
        n1 = len(word1)
        n2 = len(word2)
        p1 = p2 = 0
        res = []
        while p1 < n1 and p2 < n2:
            if word1[p1:] + word2[p2:] > word2[p2:] + word1[p1:]:
                res.append(word1[p1])
                p1 += 1
            else:
                res.append(word2[p2])
                p2 += 1
        
        if p1 == n1:
            return ''.join(res) + word2[p2:]
        else:
            return ''.join(res) + word1[p1:]
''',
    call='Solution().largestMerge("abab", "abcab")',
    expect='abcababab',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='word1', label='word1', cell=70, pointers={'p1': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('p1') else None, dim=lambda S, k, v: k < S.get('p1', 0)),
        dict(type='string', var='word2', label='word2', cell=70, pointers={'p2': 'pink'},
             color=lambda S, k, v: 'pink' if k == S.get('p2') else None, dim=lambda S, k, v: k < S.get('p2', 0)),
        dict(type='array', var='res', label='res（已合并）', cell=70, color=lambda S, k, v: 'green'),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink')],
    captions={
        'n1 = len': '`word1` 长度 `n1 = {n1}`',
        'n2 = len': '`word2` 长度 `n2 = {n2}`',
        'p1 = p2 = 0': '两个指针 `p1`、`p2` 分别指向两串的起点，像归并排序一样往后走',
        'res = []': '`res` 存合并结果',
        'while p1 < n1': lambda S, B, r: ('两边都还有字符，继续比较' if S.p1 < S.n1 and S.p2 < S.n2
                                           else '有一边用完了，跳出循环，把另一边剩下的接上'),
        'if word1[p1:]': lambda S, B, r: (
            f"`word1[p1:] + word2[p2:]` = `{S.word1[S.p1:] + S.word2[S.p2:]}`，"
            f"`word2[p2:] + word1[p1:]` = `{S.word2[S.p2:] + S.word1[S.p1:]}`：" +
            ('前者更大 → ==取 word1 的字符==' if S.word1[S.p1:] + S.word2[S.p2:] > S.word2[S.p2:] + S.word1[S.p1:]
             else '前者不更大 → ==取 word2 的字符==')),
        'res.append(word1[p1])': '取出 `word1[{p1}] = {word1[p1]}`，`res` = `{"".join(res)}`',
        'p1 += 1': '`p1` → {p1}',
        'res.append(word2[p2])': '取出 `word2[{p2}] = {word2[p2]}`，`res` = `{"".join(res)}`',
        'p2 += 1': '`p2` → {p2}',
        'if p1 == n1': lambda S, B, r: ('`p1 == n1`，word1 用完了 → 接上 word2 剩下的部分' if S.p1 == S.n1
                                         else '`p2 == n2`，word2 用完了 → 接上 word1 剩下的部分'),
        'return': '返回 `"{ret}"`',
    },
    cards=dict(
        one_liner='谁拼在前面更大就取谁：比较两种拼接顺序',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['每次从 `word1` 或 `word2` 头部取一个字符拼到 `merge` 末尾',
                 '求字典序==最大==的 `merge`',
                 '本视频：`"abab"`、`"abcab"` → `"abcababab"`'],
        quote='若当前的word1[p1:] + word2[p2:] > word2[p2:] + word1[p1:]，那么此时就应该合并word1[p1]，否则合并word2[p2]。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个指针做归并，但不能只比较当前字符：字符相同时不知道谁更优',
              '把另一个串拼在后面，从 p1、p2 起逐字符比较，相同就一直比下去',
              '拼接还保证一方走到末尾时，会自然去比较另一方的字符'],
        summary=['时间 `O(n^2)`：每步切片拼接比较，数据规模小所以够用',
                 '循环结束后一定有一个串已用完，把另一个剩下部分直接接上',
                 '原文说也可以用后缀数组做，会更快',
                 '原文是 Python 2 写法，只删去了开头的类型说明文档字符串，其余不变'],
    ),
)
