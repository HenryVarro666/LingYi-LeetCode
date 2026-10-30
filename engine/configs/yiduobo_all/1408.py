def _hs(S):
    n = S.get('n')
    hl = S.get('hash_list')
    if n is None or hl is None:
        return set()
    return hl[n]


def _top(S):
    if 'word' not in S:
        return ''
    n = len(S['word'])
    return f"当前 `word = \"{S['word']}\"`，长度 `{n}`；答案 res = `{S.get('res')}`"


CONFIG = dict(
    num=1408, title='数组中的字符串匹配', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按长度排序 · 前缀哈希（类 RK）',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def stringMatching(self, words):

        mod = 10 ** 9 + 7
        p = [1]
        for index in range(30):
            p.append(p[-1] * 29 % mod)

        hash_list = [set() for _ in range(31)]
        res = []
        for word in sorted(words, key=lambda d:-len(d)):
            v = [ord(word[0]) - 97]
            for char in word[1:]:
                v.append((v[-1] * 29 + ord(char) - 97) % mod)

            n = len(word)
            if v[-1] in hash_list[n]:
                res.append(word)
            else:
                hash_list[n].add(v[-1])
                for l in range(1, n):
                    hash_list[l].add(v[l - 1])
                    for index in range(l, n):
                        hash_list[l].add((v[index] - (v[index - l] * p[l] % mod) + mod) % mod)

        return res
''',
    call='Solution().stringMatching(["abcd", "bc", "d"])',
    expect=['bc', 'd'],
    views=[
        dict(type='text', fn=_top, size=26, h=60),
        dict(type='array', var='words', label='words（按长度从大到小处理）', h=190),
        dict(type='array', var='v', label='v：word 各前缀的 29 进制哈希', h=210),
        dict(type='set', var=_hs, label='hash_list[n]：长度为 n 的子串哈希', fmt=lambda x: str(x), h=190),
        dict(type='array', var='res', label='res（答案）', h=170),
    ],
    watch=[('n', 'n', 'blue'), ('l', 'l', 'pink'), ('res', 'res', 'green')],
    captions={
        'mod = 10': '哈希取模 `mod = 10^9 + 7`，防止 29 进制编码过大',
        'p = [1]': '预处理 `p[i] = 29^i`（求子串哈希用）；`hash_list[k]` 存长度为 k 的子串哈希',
        'hash_list = [': '`hash_list[k]`：存==长度为 k 的子串==的哈希，先建 31 个空集合',
        'for word in sorted': '==从长到短==处理：长串先入表，短串才能查到自己是不是它的子串',
        'v = [ord': '`v[0]` = 首字母编码 `{v[0]}`（a=0, b=1, ...）',
        'v.append': '29 进制往后推：`v[-1] * 29 + 新字母` → 前缀哈希 `{v[-1]}`',
        'n = len(word)': '`word = "{word}"` 长度 `n = {n}`',
        'if v[-1] in hash_list[n]': lambda S, B, r: (
            f"整串哈希 `{S.v[-1]}` ==已在== hash_list[{S.n}] → 它是更长串的子串" if S.v[-1] in S.hash_list[S.n]
            else f"整串哈希 `{S.v[-1]}` 不在 hash_list[{S.n}] → 目前没见过，不是子串"),
        'res.append(word)': '`"{word}"` 是别的串的子串，加入 `res = {res}`；它的子串也必然是子串，不用再展开',
        'hash_list[n].add': '把整串哈希 `{v[-1]}` 记入 hash_list[{n}]',
        'hash_list[l].add(v[l - 1])': '长度 `{l}` 的前缀哈希 `v[{l-1}] = {v[l-1]}` 入 hash_list[{l}]',
        'hash_list[l].add((v[index]': '滑窗哈希：`v[{index}] - v[{index-l}] * 29^{l}` 得到 `word[{index-l+1}..{index}]`（长 {l}）的哈希，入 hash_list[{l}]',
        'return res': '返回所有==是别的字符串子串==的串：`{res}`',
    },
    skip=['mod = 10', 'for index in range(30)', 'p.append', 'hash_list = [set'],
    max_steps=90,
    cards=dict(
        one_liner='长串先入表，短串查哈希，查到就是子串',
        complexity='时间约 `O(L^2)`（L 为总长度），空间 `O(L^2)`',
        problem=['给一个字符串数组 `words`，返回其中==是其他单词子串==的所有单词（顺序任意）',
                 '示例：`["mass","as","hero","superhero"]` → `["as","hero"]`',
                 '本视频：`["abcd","bc","d"]` → `["bc","d"]`'],
        quote='先将字符串按长度从大到小进行排序，然后对于每个字符串，先将其按照29进制编码。由于这个编码很大，因此要将其对10^9 + 7取模。',
        quote_src='—— yiduobo 题解原文',
        idea=['当前串的哈希==出现过== → 是某个更长串的子串，加入答案，无需再展开它的子串',
              '没出现过 → 把它所有子串的哈希按长度存进 `hash_list`',
              '子串哈希用前缀哈希相减得到，类似 RK 算法'],
        summary=['字符串很短，直接暴力 `in` 判断也能过',
                 '易错：必须按长度从大到小，否则短串查不到',
                 '哈希取模有极小概率冲突；`hash_list[k]` 只放长度为 k 的哈希',
                 '原文为 Python 2 风格（`class Solution(object)`），无需改动即可在 Python 3 运行'],
    ),
)
