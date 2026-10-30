def _txt(S):
    if 'cnt1' not in S:
        return ''
    if 'now1' in S and 'i' in S and 'j' in S and S['i'] != S['j'] and S['cnt1'][S['i']] and S['cnt2'][S['j']]:
        return f"交换 `{chr(97 + S['i'])}` 换 `{chr(97 + S['j'])}` 后：word1 种类 `now1 = {S['now1']}`，word2 种类 `now2 = {S['now2']}`"
    if 'tot1' in S:
        return f"原本 word1 有 `tot1 = {S['tot1']}` 种字母，word2 有 `tot2 = {S['tot2']}` 种"
    return ''


CONFIG = dict(
    num=2531, title='使字符串中不同字符的数目相等', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举两种字母 + 数组计数', tags=[],
    code='''
class Solution(object):
    def isItPossible(self, word1, word2):

        cnt1 = [0] * 26
        for char in word1:
            cnt1[ord(char) - 97] += 1
        
        cnt2 = [0] * 26
        for char in word2:
            cnt2[ord(char) - 97] += 1
        
        tot1 = tot2 = 0
        for i in range(26):
            if cnt1[i] > 0:
                tot1 += 1
            if cnt2[i] > 0:
                tot2 += 1
        
        for i in range(26):
            for j in range(26):
                if cnt1[i] == 0 or cnt2[j] == 0:
                    continue

                if i == j:
                    if tot1 == tot2:
                        return True
                    continue

                now1, now2 = tot1, tot2
                if cnt1[i] == 1:
                    now1 -= 1
                if cnt2[j] == 1:
                    now2 -= 1
                
                if cnt2[i] == 0:
                    now2 += 1
                if cnt1[j] == 0:
                    now1 += 1
                
                if now1 == now2:
                    return True

        return False
''',
    call="Solution().isItPossible('abcc', 'aab')",
    expect=True,
    views=[
        dict(type='string', var='word1', label='word1', cell=70, h=150),
        dict(type='array', var='cnt1', label='cnt1（word1 各字母个数，下标 0 = a）', pointers={'i': 'blue'}, cell=48, h=190,
             dim=lambda S, i, v: v == 0),
        dict(type='string', var='word2', label='word2', cell=70, h=150),
        dict(type='array', var='cnt2', label='cnt2（word2 各字母个数）', pointers={'j': 'pink'}, cell=48, h=190,
             dim=lambda S, i, v: v == 0),
        dict(type='text', fn=_txt, size=26, h=100),
    ],
    skip=['continue', 'for char in', 'cnt1[ord(char)', 'cnt2[ord(char)', 13, 14, 16, 20, 21],
    watch=[('tot1', 'tot1', 'blue'), ('tot2', 'tot2', 'pink'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), 'now1', 'now2'],
    captions={
        'cnt1 = [0]': '`cnt1[c]`：word1 里字母 `c` 出现的次数，共 26 个格子',
        'cnt2 = [0]': '`cnt2` 同理，统计 word2',
        'tot1 = tot2': '`tot1`、`tot2`：两个字符串一开始各有几种不同字母',
        'if cnt1[i] > 0': '`cnt1[{i}] = {cnt1[i]}`：{"出现过，`tot1` 要计入" if cnt1[i] > 0 else "没出现"}',
        'tot1 += 1': '字母 `{chr(97 + i)}` 在 word1 出现过：`tot1` → {tot1}',
        'if cnt2[i] > 0': '`cnt2[{i}] = {cnt2[i]}`：{"出现过，`tot2` 要计入" if cnt2[i] > 0 else "没出现"}',
        'tot2 += 1': '字母 `{chr(97 + i)}` 在 word2 出现过：`tot2` → {tot2}',
        'for i in range(26)': lambda S, B, r: ('开始枚举：用来换出去的字母 `i`' if 'j' not in S else f'换出 word1 的字母 `{chr(97 + S.i)}`'),
        'for j in range(26)': '换入 word2 的字母 `{chr(97 + j)}`',
        'if cnt1[i] == 0 or': lambda S, B, r: (f'`{chr(97 + S.i)}`、`{chr(97 + S.j)}` 必须分别在 word1、word2 里出现过：'
                                              f'{"满足" if S.cnt1[S.i] and S.cnt2[S.j] else "不满足，跳过这一对"}'),
        'if i == j': lambda S, B, r: (f'换出 `{chr(97 + S.i)}`、换入 `{chr(97 + S.j)}`（两个字符串里都有）。' + f'`i == j`：两边换的是同一种字母，等于没换；只看 `tot1 = {S.tot1}` 与 `tot2 = {S.tot2}`'
                                      if S.i == S.j else f'换出 `{chr(97 + S.i)}`、换入 `{chr(97 + S.j)}`（两个字符串里都有）。`i ≠ j`，会改变种类数，要具体算'),
        'if tot1 == tot2': '`tot1 = {tot1}`、`tot2 = {tot2}`：=={"相等 → 可行" if tot1 == tot2 else "不等 → 这种换法不行"}=='.replace('"', "'"),
        'now1, now2 = ': '先拷贝种类数，不真的修改 cnt：`now1 = {now1}`，`now2 = {now2}`',
        'if cnt1[i] == 1': '`cnt1[{i}] = {cnt1[i]}`：{"只有 1 个，换走后 word1 少一种 → now1 减 1" if cnt1[i] == 1 else "还有剩，种类不减"}',
        'now1 -= 1': '`now1` → {now1}',
        'if cnt2[j] == 1': '`cnt2[{j}] = {cnt2[j]}`：{"只有 1 个，换走后 word2 少一种 → now2 减 1" if cnt2[j] == 1 else "还有剩，种类不减"}',
        'now2 -= 1': '`now2` → {now2}',
        'if cnt2[i] == 0': '`{chr(97 + i)}` 换到 word2：{"word2 本来没有 → 多一种" if cnt2[i] == 0 else "word2 本来就有，种类不变"}',
        'now2 += 1': '`now2` → {now2}',
        'if cnt1[j] == 0': '`{chr(97 + j)}` 换到 word1：{"word1 本来没有 → 多一种" if cnt1[j] == 0 else "word1 本来就有，种类不变"}',
        'now1 += 1': '`now1` → {now1}',
        'if now1 == now2': '`now1 = {now1}`，`now2 = {now2}`：=={"相等，找到可行的交换" if now1 == now2 else "不等，试下一对"}==',
        'return True': '找到可行方案，返回 ==True==',
        'return False': '所有交换方案都不行 → `False`',
    },
    cards=dict(
        one_liner='字符串很长，但字母只有 26 种：枚举换哪两种',
        complexity='时间 `O(n+m+26²)`，空间 `O(26)`',
        problem=['在 `word1`、`word2` 各挑一个位置，交换这两个字符，==恰好一次==',
                 '问交换后两个字符串的不同字符数能否相等',
                 '示例：`abcc`、`aab` → `true`'],
        quote='字符串长度很长，因此不能直接枚举具体的交换位置。……可以改为枚举交换了哪两种字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt1`、`cnt2` 统计次数，`tot1`、`tot2` 是原有的种类数',
              '`i == j`：相当于没换，`tot1 == tot2` 才可行',
              '`i != j`：`cnt1[i]` 从 1 变 0 则 word1 少一种；`cnt1[j]` 从 0 变 1 则多一种；word2 对称',
              '不真的改数组，只看次数是 0 还是 1'],
        summary=['时间 `O(n+m+26²)`，空间 `O(26)`',
                 '`cnt1[i] == 0 or cnt2[j] == 0` 要跳过：这个字母在该字符串里不存在，换不出去',
                 '`i == j` 也是一次合法交换，别漏掉',
                 '原文 `range(26)` 等已是 Python 3 可运行写法，仅 `class` 保持原样',
                 '对比灵神：灵神用 `Counter` 只枚举真实存在的字母；这里用定长数组枚举 26×26 再跳过'],
    ),
)
