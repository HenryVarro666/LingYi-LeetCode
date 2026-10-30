def _pal(t):
    return t == t[::-1]


def _txt(S):
    if 'pos' not in S or 'word_len' not in S:
        return '把每个词按长度从小到大处理；两张表：prefix_dict（词本身 → 下标）、suffix_dict（反转词 → 下标）'
    w = S['words'][S['pos']]
    if 'index' in S and S['index'] < S['word_len']:
        i = S['index']
        return f"`{w}`：切点 {i}　前缀 ==`{w[:i + 1]}`==　　剩余 `{w[i + 1:] or '空'}` 要回文才能拼"
    return f"处理 `{w}`（长度 {S['word_len']}）"


def _res_txt(S):
    r = S.get('res')
    if r is None:
        return ''
    if not r:
        return '结果 res：（空）'
    return '结果 res：' + '  '.join(f"[{a},{b}]=`{S['words'][a]}+{S['words'][b]}`" for a, b in r)


CONFIG = dict(
    num=336, title='回文对', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='哈希表前后缀 + 剩余部分回文',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution(object):

    def check(self, s, l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    def palindromePairs(self, words):

        len_list = [[index, len(word)] for index, word in enumerate(words)]
        len_list = sorted(len_list, key=lambda d:d[1])
        res = []

        prefix_dict = {}
        suffix_dict = {}
        for pos, word_len in len_list:
            if word_len == 0:
                for index in range(len(words)):
                    if index != pos and self.check(words[index], 0, len(words[index]) - 1):
                        res.append([pos, index])
                        res.append([index, pos])

            for index in range(word_len):
                if self.check(words[pos], index + 1, word_len - 1):
                    prefix = words[pos][:index + 1]
                    if prefix in suffix_dict:
                        res.append([pos, suffix_dict[prefix]])
                if self.check(words[pos], 0, index - 1):
                    suffix = words[pos][index:][::-1]
                    if suffix in prefix_dict:
                        res.append([prefix_dict[suffix], pos])

            prefix_dict[words[pos]] = pos
            suffix_dict[words[pos][::-1]] = pos

        return res
''',
    call="Solution().palindromePairs(['ab', 'ba', 's', 'ls'])",
    expect=[[0, 1], [1, 0], [2, 3]],
    views=[
        dict(type='array', var='words', pointers={'pos': 'blue'}, label='words（蓝 = 当前处理的词）', cell=110, h=250),
        dict(type='map', var='prefix_dict', label='prefix_dict：词 → 下标（已处理的较短词）', fmt=lambda k, v: f"'{k}': {v}", h=140, font=30),
        dict(type='map', var='suffix_dict', label='suffix_dict：反转词 → 下标', fmt=lambda k, v: f"'{k}': {v}", h=140, font=30),
        dict(type='text', h=80, size=28, fn=_txt),
        dict(type='text', h=70, size=28, fn=_res_txt),
    ],
    watch=[('pos', 'pos', 'blue'), ('word_len', 'word_len'), ('index', 'index', 'orange'), ('prefix', 'prefix', 'cyan'), ('suffix', 'suffix', 'pink')],
    captions={
        'len_list = [[': '先记下每个词的 (下标, 长度)',
        'len_list = sorted': '==按长度从小到大==处理：当前词只和更短（或等长）的已处理词配对，每对只会被发现一次',
        'prefix_dict = {}': '`prefix_dict`：已处理的词 → 下标',
        'suffix_dict = {}': '`suffix_dict`：已处理词的反转 → 下标',
        'for pos, word_len': '取出第 `{pos}` 个词 `{words[pos]!r}`，长度 {word_len}',
        'if word_len == 0': '空串和任意回文串都能配对（本例没有空串）',
        'for index in range(word_len)': '枚举切点 `index = {index}`：把词切成 `[:{index}+1]` 和 `[{index}+1:]`',
        'if self.check(words[pos], index + 1': lambda S, B, r: (
            f"后半段 `{S.words[S.pos][S.index + 1:] or '空'}` 回文 → 前缀 `{S.words[S.pos][:S.index + 1]}` + 回文 + 它的反转 = 回文，去 suffix_dict 查反转词"
            if _pal(S.words[S.pos][S.index + 1:]) else
            f"后半段 `{S.words[S.pos][S.index + 1:]}` 不是回文，这个切法不行"),
        'if prefix in suffix_dict': lambda S, B, r: (f"前缀 `{S.prefix!r}`：`suffix_dict` 里有 → 存在词 `{S.words[S.suffix_dict[S.prefix]]}` 的反转等于前缀 ==可配对==" if S.prefix in S.suffix_dict
                                                     else f"前缀 `{S.prefix!r}`：`suffix_dict` 里没有，没有可配的词"),
        'res.append([pos, suffix_dict[prefix]])': '`{words[pos]}` 在前、`{words[res[-1][1]]}` 在后拼出回文：记录 `{res[-1]}`',
        'if self.check(words[pos], 0, index - 1)': lambda S, B, r: (
            f"前半段 `{S.words[S.pos][:S.index] or '空'}` 回文 → 反转的后缀 + 回文 + 后缀 = 回文，去 prefix_dict 查这个词"
            if _pal(S.words[S.pos][:S.index]) else
            f"前半段 `{S.words[S.pos][:S.index]}` 不是回文，这个切法不行"),
        'if suffix in prefix_dict': lambda S, B, r: (f"反转后缀 `{S.suffix!r}`：`prefix_dict` 里有 → 词 `{S.words[S.prefix_dict[S.suffix]]}` 放前面 ==可配对==" if S.suffix in S.prefix_dict
                                                     else f"反转后缀 `{S.suffix!r}`：`prefix_dict` 里没有，没有可配的词"),
        'res.append([prefix_dict[suffix], pos])': '`{words[res[-1][0]]}` 在前、`{words[pos]}` 在后拼出回文：记录 `{res[-1]}`',
        'prefix_dict[words[pos]] = pos': '当前词处理完，登记进 `prefix_dict`',
        'suffix_dict[words[pos][::-1]] = pos': '把它的反转登记进 `suffix_dict`，供后面更长的词查询',
        'return res': '一共找到 `{len(res)}` 个回文对',
    },
    skip=['while l < r', 'if s[l] != s[r]', 'return False', 'return True', 'l += 1', 'r -= 1', 'if word_len == 0', 'for index in range(word_len)', 'len_list = [[', 'prefix_dict = {}', 'prefix = words', 'suffix = words'],
    max_steps=90,
    cards=dict(
        one_liner='拆成「前缀配反转词 + 剩余部分回文」，哈希表查前后缀',
        complexity='提交版（dict）时间约 `O(n·k²)`，空间 `O(n·k)`',
        problem=['给一组互不相同的单词，找出所有下标对 `(i, j)`，使 `words[i] + words[j]` 是回文串',
                 '示例：`["abcd","dcba","lls","s","sssll"]` → `[[0,1],[1,0],[3,2],[2,4]]`',
                 '本视频：`["ab","ba","s","ls"]` → `[[0,1],[1,0],[2,3]]`'],
        quote='如果s+t能形成回文串，那么s一定是reverse(t)的前缀，且reverse(t)除去s剩下的部分是回文的形式。',
        quote_src='—— yiduobo 题解原文',
        idea=['设 s 不短于 t：s+t 回文 ⇔ s 的一段前缀是 reverse(t)，剩余部分自己回文',
              '所以枚举每个词的切点，用哈希表查「前缀」或「反转后缀」是否是某个词',
              '按长度从小到大处理，较短的词已在表里，每对只记一次'],
        summary=['原文还给了 Manacher + 两棵 trie 的 `O(nk)` 解法，但被注释掉了；视频演示的是实际生效的 dict 版',
                 '视频中删去了被注释的那段和 `import time`，其余代码不变',
                 '易错：空串要单独处理；两个切点方向（前缀配后者、后缀配前者）都要查',
                 '本例 `s + ls = sls`：处理 `ls` 时，前半段 `l` 回文，后缀 `s` 的反转命中词 `s`'],
    ),
)
