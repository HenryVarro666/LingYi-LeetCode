def _L(m):
    return ''.join(chr(97 + k) for k in range(26) if m >> k & 1) or '∅'


def _cand_new(S):
    return None


def _text(S):
    if 'puzzle' not in S:
        return '把每个字符串编码成 26 位二进制：第 k 位 = 有没有字母 k（下面用字母集合表示）'
    p = S['puzzle']
    return f'`puzzle = "{p}"`：必须含 `{p[0]}`，其余 `{p[1:]}` 可有可无 → 候选集合 `2^{len(p) - 1}` 种'


def _wtxt(S):
    return ''


CONFIG = dict(
    num=1178, title='猜字谜', difficulty='Hard', category='位运算',
    author='yiduobo', technique='位掩码 · 枚举 puzzle 子集',
    code='''
class Solution(object):
    def findNumOfValidWords(self, words, puzzles):

        word_dict = {}
        for word in words:
            cnt = 0
            num = 0
            for char in word:
                p = 1 << (ord(char) - 97)
                if num & p:
                    continue
                cnt += 1
                num |= p
                if cnt > 7:
                    break
            
            if cnt <= 7:
                word_dict[num] = word_dict.get(num, 0) + 1

        res = []
        for puzzle in puzzles:
            candidate = set([1 << (ord(puzzle[0]) - 97)])
            for char in puzzle[1:]:
                candidate.update([x | (1 << ord(char) - 97) for x in candidate])
            res.append(sum([word_dict.get(x, 0) for x in candidate]))

        return res
''',
    call='Solution().findNumOfValidWords(["ab", "aab", "bc"], ["abc", "bcx"])',
    expect=[2, 1],
    views=[
        dict(type='text', fn=_text, h=60, size=24),
        dict(type='map', var='word_dict', label='word_dict：字母集合 → 出现次数（原代码里 key 是整数掩码）',
             fmt=lambda k, v: f'{_L(k)} : {v}', font=28, h=190),
        dict(type='set', var='candidate', label='candidate：puzzle 的合法子集（黄 = 刚加入）', fmt=_L, font=26, h=240),
        dict(type='array', var='res', label='res', cell=90, h=150),
    ],
    watch=[('cnt', 'cnt', 'pink'), ('num', 'num', 'blue'), ('word', 'word'), ('puzzle', 'puzzle', 'yellow')],
    skip=['p = 1 <<', 'cnt = 0', 'num = 0', 'for char in word', 'cnt += 1', 'continue', 'for char in puzzle[1:]'],
    max_steps=75,
    captions={
        'word_dict = {}': '`word_dict` 统计每种编码（字母集合）有几个单词',
        'for word in words': lambda S, B, r: (f'处理单词 `"{S.word}"`：编码它含有的字母' if B.get('word') != S.word
                                              else '单词都登记完了'),
        'for char in word': lambda S, B, r: (f"看字母 `'{S.char}'`" if S.get('char') is not None else ''),
        'if num & p': lambda S, B, r: (f"字母 `'{S.char}'` 已经在 `num` 里 → 重复字母，==不重复计数==，跳过" if S.num & S.p
                                       else f"字母 `'{S.char}'` 是新字母：`cnt` 加一，位置 1"),
        'num |= p': lambda S, B, r: f"`num |= p`：`{S.char}` 对应的位置 1，字母集合 → `{_L(S.num)}`，不同字母数 `cnt = {S.cnt}`",
        'if cnt > 7': '`cnt = {cnt}`：超过 7 个不同字母就不可能是谜底，提前停止（这里没超过）',
        'if cnt <= 7': lambda S, B, r: f'`cnt = {S.cnt} ≤ 7`：保留，登记编码 `{_L(S.num)}`',
        'word_dict[num]': lambda S, B, r: f'编码 `{_L(S.num)}` 的单词数 → `{S.word_dict[S.num]}`',
        'res = []': '接下来对每个 puzzle，数有多少个编码在候选集合里',
        'for puzzle in puzzles': lambda S, B, r: (f'处理 `puzzle = "{S.puzzle}"`' if B.get('puzzle') != S.puzzle
                                                  else 'puzzle 都处理完了'),
        'candidate = set': lambda S, B, r: f'谜底必须含首字母 `{S.puzzle[0]}`：候选集合先只有 `{_L(1 << (ord(S.puzzle[0]) - 97))}`',
        'candidate.update': "字母 `'{char}'` 可有可无：给每个候选都加上它再并入，旧的保留 → 候选翻倍，共 `{len(candidate)}` 个",
        'res.append': '候选里在 `word_dict` 中的次数之和 = `{res[-1]}`，就是该 puzzle 的谜底数',
        'return res': '每个 puzzle 的谜底数：`{ret}`',
    },
    cards=dict(
        one_liner='单词压成位掩码，枚举 puzzle 的子集去字典里查',
        complexity='时间 `O(Σ|word| + m · 2^6)`，空间 `O(n)`',
        problem=['`puzzle` 长为 7 且字母不重复；单词 `word` 是它的谜底需满足：',
                 '`word` 含有 `puzzle` 的==第一个字母==，且 `word` 的每个字母都在 `puzzle` 里',
                 '对每个 puzzle 返回谜底单词数',
                 '本视频为了简短，用 `["abc","aab","bcd"]` 和 4 个字母的 puzzle'],
        quote='由于puzzle[1:]只有6个字符，因此实际上最多只有32种不同的情况。得到答案候选集之后，我们只需要看看其中有多少个编码出现在word编码的dict中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['字母 a–z 对应 26 位二进制，单词和 puzzle 都编码成整数',
              '不同字母超过 7 个的单词不可能是谜底，直接忽略',
              '枚举 `puzzle[1:]` 的每个子集（必含首字母），在 `word_dict` 里查数量求和'],
        summary=['时间约 `O(Σ|word| + m · 2^6)`，空间 `O(n)`',
                 '易错：首字母必须在掩码里，其余 6 个才枚举「选或不选」',
                 '单词里重复字母只算一次，所以用 `num & p` 判重',
                 '`candidate.update` 里列表推导先用旧集合算完，再并入，不会边遍历边改',
                 '视频演示用了更短的 puzzle（4 位），代码和原文一致'],
    ),
)
