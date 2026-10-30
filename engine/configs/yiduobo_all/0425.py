def _square(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    w1, w4 = S.get('word1'), S.get('word4')
    cv.text((x0 + 18, y0 + 4), '方块的外圈由 word1、word4 决定；中间只剩 ? 要找', 24, T['muted'], bold=True)
    if not (isinstance(w1, str) and isinstance(w4, str) and len(w1) == 4 and len(w4) == 4):
        cv.text((x0 + 18, y0 + 60), '（还没开始枚举 word1 / word4）', 22, T['dim'])
        return
    c = S.get('word2_mid')
    w2, w3 = S.get('word2'), S.get('word3')
    ch = chr(c + 97) if isinstance(c, int) else None
    found = ('word2_remove1' in S and S['word2_remove1'] in S.get('remove1_words', {}) and
             S.get('word3_remove2') in S.get('remove2_words', {}))
    g = [[None] * 4 for _ in range(4)]
    for k in range(4):
        g[0][k], g[k][0] = w1[k], w1[k]
        g[3][k], g[k][3] = w4[k], w4[k]
    kind = {}
    for k in range(4):
        for (r, q) in ((0, k), (k, 0)):
            kind[(r, q)] = 'w1'
        for (r, q) in ((3, k), (k, 3)):
            kind[(r, q)] = 'w4'
    if ch:
        g[1][2] = g[2][1] = ch
        kind[(1, 2)] = kind[(2, 1)] = 'mid'
    if found and isinstance(w2, str) and isinstance(w3, str):
        g[1][1], g[2][2] = w2[1], w3[2]
        kind[(1, 1)] = kind[(2, 2)] = 'new'
    cell = min(110, (y1 - y0 - 120) / 4)
    sx, sy = x0 + 60, y0 + 70
    col = {'w1': T['blue'], 'w4': T['pink'], 'mid': T['yellow'], 'new': T['green']}
    for r in range(4):
        for q in range(4):
            X, Y = sx + q * cell, sy + r * cell
            k = kind.get((r, q))
            v = g[r][q]
            fill = col[k] if k else T['panel2']
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=10)
            cv.text((X + cell / 2, Y + cell / 2), v if v else '?', 36, T['bg'] if k else T['dim'], anchor='mm', bold=True, mono=True)
    tx = sx + 4 * cell + 50
    lines = [('word1 = ' + w1, T['blue']), ('word4 = ' + w4, T['pink'])]
    if ch:
        lines.append((f'中间字符 = {ch}（第 {c} 个字母）', T['yellow']))
        lines.append((f"word2 去掉下标1 = {S.get('word2_remove1')}", T['text']))
        lines.append((f"word3 去掉下标2 = {S.get('word3_remove2')}", T['text']))
    for i, (t, cc) in enumerate(lines):
        cv.text((tx, sy + 10 + i * 38), t, 24, cc, anchor='lm', mono=True, bold=True)
    if found:
        cv.text((tx, sy + 10 + len(lines) * 38), '两个键都命中 → 方块凑齐', 24, T['green'], anchor='lm', bold=True)


def _hit(S, B, ret):
    a, b = S.word2_remove1 in S.remove1_words, S.word3_remove2 in S.remove2_words
    if a and b:
        return f'两个键都在哈希表里 → `{S.remove1_words[S.word2_remove1]}` 和 `{S.remove2_words[S.word3_remove2]}` 配成 ==word2 / word3=='
    return '两张表没有同时命中 → 这个字母不行'


CONFIG = dict(
    num=425, title='单词方块', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举首尾单词 + 去字符哈希表',
    tags=[],
    code='''
class Solution(object):
    def wordSquares(self, words):

        n = len(words[0])
        
        res = []

        if n == 1:
            for word in words:
                res.append([word])
        elif n == 2:
            for word1 in words:
                for word2 in words:
                    if word2[0] == word1[1]:
                        res.append([word1, word2])
        elif n == 3:
            words_set = set(words)
            for word1 in words:
                for word3 in words:
                    if word3[0] == word1[2]:
                        for word2_mid in range(26):
                            word2 = word1[1] + chr(word2_mid + 97) + word3[1]
                            if word2 in words_set:
                                res.append([word1, word2, word3])
        else:
            remove1_words = {}
            remove2_words = {}
            for word in words:
                remove1 = word[0] + word[2] + word[3]
                remove2 = word[0] + word[1] + word[3]
                if remove1 not in remove1_words:
                    remove1_words[remove1] = set()
                if remove2 not in remove2_words:
                    remove2_words[remove2] = set()

                remove1_words[remove1].add(word)
                remove2_words[remove2].add(word)

            for word1 in words:
                for word4 in words:
                    if word4[0] == word1[3]:
                        for word2_mid in range(26):
                            word2_remove1 = word1[1] + chr(word2_mid + 97) + word4[1]
                            word3_remove2 = word1[2] + chr(word2_mid + 97) + word4[2]
                            if word2_remove1 in remove1_words and word3_remove2 in remove2_words:
                                for word2 in remove1_words[word2_remove1]:
                                    for word3 in remove2_words[word3_remove2]:
                                        res.append([word1, word2, word3, word4])
        
        return res
''',
    call='Solution().wordSquares(["ball", "lady", "area", "lead"])',
    expect=[['ball', 'area', 'lead', 'lady']],
    skip=['remove2_words = {}', 'n = len(words[0])', 'res = []', 'for word2_mid in range(26)', 'word2_remove1 = word1[1]',
          'remove1 = word[0]', 'remove2 = word[0]', 'if remove1 not in', 'remove1_words[remove1] = set()',
          'if remove2 not in', 'remove2_words[remove2] = set()', 'remove1_words[remove1].add'],
    views=[
        dict(type='array', var='words', label='words', h=170,
             color=lambda S, i, v: 'blue' if v == S.get('word1') else ('pink' if v == S.get('word4') else None)),
        dict(type='custom', draw=_square, h=330),
        dict(type='map', var='remove1_words', label='remove1_words（去掉下标 1 的字母 → 单词）', fmt=lambda k, v: f'{k} → {sorted(v)}', font=22, h=120),
        dict(type='map', var='remove2_words', label='remove2_words（去掉下标 2 的字母 → 单词）', fmt=lambda k, v: f'{k} → {sorted(v)}', font=22, h=120),
    ],
    watch=['word1', 'word4', ('mid', lambda S: chr(S['word2_mid'] + 97) if 'word2_mid' in S else None, 'yellow'), 'word2_remove1', 'word3_remove2', ('res', 'res', 'green')],
    captions={
        'remove1_words = {}': '预处理：给每个单词==去掉下标 1 / 下标 2 的字母==，剩下的部分当 key 聚合单词',
        'for word in words': lambda S, B, r: ('预处理完成：两张表都建好了' if 'word' in B and B['word'] == S['word'] else f"处理单词 `{S['word']!r}`：它既属于 remove1 表，也属于 remove2 表"),
        'remove2_words[remove2].add': '`{word!r}` 去掉下标 1 → `{remove1}`，去掉下标 2 → `{remove2}`，分别登记进两张表',
        'for word1 in words': lambda S, B, r: ('枚举完所有 word1' if 'word1' in B and B['word1'] == S['word1'] else f"枚举第一个单词 `word1 = {S['word1']!r}`"),
        'for word4 in words': lambda S, B, r: ('word4 枚举完了' if 'word4' in B and B['word4'] == S['word4'] else f"枚举第四个单词 `word4 = {S['word4']!r}`"),
        'if word4[0] == word1[3]': lambda S, B, r: (f"右上角 `word1[3] = {S.word1[3]}`、左下角 `word4[0] = {S.word4[0]}` " + ('相等 → 外圈可以闭合，继续' if S.word4[0] == S.word1[3] else '不相等 → ==对称性不满足==，跳过')),
        'word3_remove2 = word1[2]': '中间字符 `{chr(word2_mid + 97)}`：要找 `word2` 去掉下标 1 = `{word2_remove1}`，`word3` 去掉下标 2 = `{word3_remove2}`',
        'if word2_remove1 in remove1_words': _hit,
        'for word2 in remove1_words': '候选 word2：`{word2}`',
        'for word3 in remove2_words': '候选 word3：`{word3}`',
        'res.append([word1, word2, word3, word4])': '四个单词凑齐：`{[word1, word2, word3, word4]}` 加入答案',
        'return res': '一共 `{len(res)}` 个单词方块',
    },
    max_steps=50,
    cards=dict(
        one_liner='枚举首尾两个单词，对称性把外圈钉死，中间靠哈希表一步查出',
        complexity='时间约 `O(n^2 · 26)`（`n` 为单词数），空间 `O(n)`',
        problem=['给一组等长单词（长度 1–4），找出所有单词方块：==第 k 行和第 k 列读出同一个单词==',
                 '同一个单词可以重复使用，返回所有方块（顺序任意）',
                 '本视频：`["ball","lady","area","lead"]` → `[["ball","area","lead","lady"]]`'],
        quote='接下来，根据单词对称的关系，就可以将方块的外层完全填充好……更好的做法应该是在一开始就进行预处理，对于单词集合中的每个单词，分别去除掉下标位置为1和下标位置为2的字符，将剩余的部分作为key，使用哈希表将各个单词聚合起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度 ≤ 2 直接枚举；长度 3 枚举两个单词，再枚举唯一的空格字母',
              '长度 4：枚举 `word1`、`word4`，要求 `word1[3] == word4[0]`（右上角 = 左下角）',
              '外圈定了，剩 `@ # *` 三格，`#` 受对称约束 → 枚举这一个字母，其余用哈希表按「去掉某位的剩余部分」直接查'],
        summary=['这份代码按单词长度 `n` 分四种情况，视频只演示 `n = 4`（最难的一支）',
                 '关键：中间字符 `#` 同时出现在 word2 和 word3 里，枚举它就能把两个 key 都拼出来',
                 '先判 `word4[0] == word1[3]`，不满足的整支剪掉，避免白枚举 26 个字母',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
