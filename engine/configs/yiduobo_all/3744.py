T = 'abbccc dee'
K0 = 9


def _consumed(S):
    k = S.get('k')
    return 0 if k is None else K0 - k


CONFIG = dict(
    num=3744, title='在展开字符串中查找第 K 个字符', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按单词长度跳过 + 逐字符扣减 k',
    code='''
class Solution(object):
    def kthCharacter(self, s, k):

        k += 1
        for w in s.split():
            word_length = len(w)
            exp_length = (word_length + 1) * word_length // 2
            if k <= exp_length:
                for index, c in enumerate(w):
                    if k <= index + 1:
                        return c
                    k -= index + 1
            else:
                k -= exp_length
                if k == 1:
                    return " "
                k -= 1
''',
    call="Solution().kthCharacter('abc de', 8)",
    expect='e',
    skip=['word_length = len'],
    views=[
        dict(type='string', var=lambda S: T, label="展开后的 t（灰色 = 已被跳过的部分，第 k 个字符就在后面）", h=170, cell=70,
             dim=lambda S, i, v: 'k' in S and i < _consumed(S),
             color=lambda S, i, v: 'blue' if 'k' in S and i == _consumed(S) else None),
        dict(type='text', size=26, h=60, fn=lambda S: (f"当前单词 `{S['w']}`，展开后长度 `exp_length = {S['exp_length']}`；剩余 `k = {S['k']}`" if 'exp_length' in S else '')),
    ],
    watch=[('k', 'k', 'yellow'), ('w', 'w', 'blue'), 'exp_length', ('index', 'index', 'pink'), ('c', 'c', 'green')],
    captions={
        'k += 1': '下标从 0 开始，先 `k += 1` 变成“第 k 个字符”：`k = {k}`，更好理解',
        'for w in s.split': '看单词 `{w!r}`',
        'exp_length = (': '长度 {len(w)} 的单词展开后：`1 + 2 + … + {len(w)}` = `({len(w)} + 1) × {len(w)} // 2` = =={exp_length}==',
        'if k <= exp_length': lambda S, B, r: (f'`k = {S.k} <= {S.exp_length}`：答案在这个单词里' if S.k <= S.exp_length
                                                else f'`k = {S.k} > {S.exp_length}`：答案在后面的单词，整个单词跳过'),
        'for index, c': '逐个字符看：`{c}` 在 t 里占 `{index + 1}` 格',
        'if k <= index + 1': lambda S, B, r: (f'`k = {S.k} <= {S.index + 1}`：第 k 个字符就落在字符 `{S.c}` 的重复段里' if S.k <= S.index + 1
                                              else f'`k = {S.k} > {S.index + 1}`：不在 `{S.c}` 里，要继续往后'),
        'return c': '找到了：答案是 `{ret}`',
        'k -= index + 1': '跳过字符 `{c}` 的 {index + 1} 格：`k` = {k}',
        'k -= exp_length': '跳过整个单词：`k -= {exp_length}` → {k}',
        'if k == 1': lambda S, B, r: ('`k = 1`：正好是单词后面的空格 → 返回空格' if S.k == 1 else f'`k = {S.k}`，不是空格，空格也占一格，下面扣掉'),
        'return " "': '答案就是空格',
        'k -= 1': '跳过单词之间的空格：`k` = {k}',
    },
    cards=dict(
        one_liner='不真的展开：按单词、再按字符，一段段扣减 k',
        complexity='时间 `O(n)`，空间 `O(n)`（`split` 的结果）',
        problem=['把每个单词的第 i 个字符重复 i 次（i 从 1 开始），得到展开串 `t`',
                 '求 `t` 中下标为 `k` 的字符，`s` 长度可达 `10^5`',
                 '本视频：`s = "abc de"`，展开为 `"abbccc dee"`，`k = 8` → `"e"`'],
        quote='对于一个长度为length的单词，其扩展后的长度就是1 + 2 + ... + length = (length + 1) * lenght // 2。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 `k += 1`，把“下标”变成“第几个”',
              '单词展开长度 `(len + 1) * len // 2`：`k` 更大就整段跳过，再扣掉 1 个空格',
              '落在当前单词里，就逐字符扣 `index + 1`，直到 `k <= index + 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：空格也占一格——跳过单词后 `k == 1` 说明答案是空格，否则还要 `k -= 1`',
                 '`k` 是下标，先加 1 再比较，否则会差 1',
                 '原文已是 Python 3 可直接运行的写法（整除本来就是 `//`），代码未改动'],
    ),
)
