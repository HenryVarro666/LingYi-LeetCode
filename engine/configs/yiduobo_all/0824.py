CONFIG = dict(
    num=824, title='山羊拉丁文', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按规则模拟',
    code='''
class Solution(object):
    def toGoatLatin(self, S):

        words = S.split(' ')
        res = []
        for index, word in enumerate(words):
            if word[0] in ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'):
                res.append(word + 'ma' + 'a' * (index + 1))
            else:
                res.append(word[1:] + word[0] + 'ma' + 'a' * (index + 1))
        
        return ' '.join(res)
''',
    call='Solution().toGoatLatin("I speak Goat Latin")',
    expect='Imaa peaksmaaa oatGmaaaa atinLmaaaaa',
    views=[
        dict(type='array', var='words', label='words（蓝 = 当前单词）', cell=150, pointers={'index': 'blue'}, h=300,
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='text', size=26, h=70, fn=lambda S: ('res：' + ' ｜ '.join(f'==%s==' % w if k == len(S['res']) - 1 else w for k, w in enumerate(S['res']))) if S.get('res') else 'res：（空）'),
        dict(type='text', size=26, fn=lambda S: (
            f"当前单词 `{S['word']}`：{'元音开头，保持原样' if S['word'][0] in 'aeiouAEIOU' else '辅音开头，首字母移到末尾'}，再加 `ma` 和 `{S['index'] + 1}` 个 `a`"
            if 'word' in S and 'index' in S else '')),
    ],
    watch=['index', 'word', ('res', 'res', 'green')],
    captions={
        'words = S.split': '按空格拆成单词：`{words}`',
        'res = []': '`res` 存放变换后的单词',
        'for index, word': lambda S, B, r: ('所有单词都处理完了，退出循环' if len(S.res) == len(S.words) else
                                            f'第 `{S.index}` 个单词 `{S.word}`，后面要补 `index + 1 = {S.index + 1}` 个 `a`'),
        "if word[0] in": lambda S, B, r: (f"首字母 `{S.word[0]}` 是元音 → ==成立=="
                                            if S.word[0] in 'aeiouAEIOU' else f"首字母 `{S.word[0]}` 不是元音 → 走 else"),
        "res.append(word + 'ma'": '元音开头：直接加 `ma` 和 `{index + 1}` 个 `a` → `{res[-1]}`',
        'res.append(word[1:]': '辅音开头：去掉首字母 `{word[0]}` 放到末尾，再加 `ma` 和 `{index + 1}` 个 `a` → `{res[-1]}`',
        'return': '用空格把 `res` 拼回去：`{ret}`',
    },
    cards=dict(
        one_liner='不用想算法，照着规则逐个单词变换',
        complexity='时间 `O(n^2)`（第 k 个单词补 k 个 a），空间 `O(n^2)`',
        problem=['把句子转成“山羊拉丁文”：元音开头的单词后面加 `ma`；辅音开头先把首字母移到末尾再加 `ma`',
                 '第 `i`（从 1 开始）个单词末尾再加 `i` 个 `a`',
                 '示例：`I speak Goat Latin` → `Imaa peaksmaaa oatGmaaaa atinLmaaaaa`'],
        quote='比较基础的题目，直接按照题目要求进行字符串变换即可。',
        quote_src='—— yiduobo 题解',
        idea=['`split(\' \')` 拆单词，`enumerate` 同时拿到下标和单词',
              '首字母在元音集合里（大小写都要列）就不动，否则 `word[1:] + word[0]`',
              '`index` 从 0 开始，所以补 `index + 1` 个 `a`'],
        summary=['时间、空间都是 `O(n^2)`：最后一个单词要补很多个 `a`',
                 '易错：元音要同时包含大写 `AEIOU`；下标从 0 开始要 `+1`',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
