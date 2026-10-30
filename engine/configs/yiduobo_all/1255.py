CONFIG = dict(
    num=1255, title='得分最高的单词集合', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='预处理 + DFS 枚举子集',
    tags=['灵神题单', '链表树与回溯', '难度分 1882'],
    setup='''
SC = [0] * 26
for ch, v in zip('abxz', (4, 4, 5, 10)):
    SC[ord(ch) - 97] = v
''',
    code='''
class Solution(object):
    def maxScoreWords(self, words, letters, score):

        words_letter = []
        words_score = []
        for word in words:
            words_letter.append({})
            words_score.append(0)
            for char in word:
                words_letter[-1][char] = words_letter[-1].get(char, 0) + 1
                words_score[-1] += score[ord(char) - 97]

        letter_dict = {}
        for letter in letters:
            letter_dict[letter] = letter_dict.get(letter, 0) + 1

        n = len(words)
        self.res = 0
        self.dfs(0, n, letter_dict, 0, words_letter, words_score)
        return self.res

    def dfs(self, level, n, letter_dict, now, words_letter, words_score):
        if level == n:
            self.res = max(self.res, now)
            return

        self.dfs(level + 1, n, letter_dict, now, words_letter, words_score)

        flag = True
        for char, num in words_letter[level].items():
            if num > letter_dict.get(char, 0):
                flag = False
                break

        if flag:
            for char, num in words_letter[level].items():
                letter_dict[char] -= num
            self.dfs(level + 1, n, letter_dict, now + words_score[level], words_letter, words_score)
            for char, num in words_letter[level].items():
                letter_dict[char] += num
''',
    call='Solution().maxScoreWords(["ax", "xxz"], ["z", "a", "x", "x"], SC)',
    expect=20,
    views=[
        dict(type='array', var='words', label='words（蓝 = 当前 level 的单词）', cell=110, h=150, pointers={'level': 'blue'}),
        dict(type='map', var='letter_dict', label='letter_dict（剩余字母）', h=110, font=26),
        dict(type='map', var='words_score', label='words_score', h=90, font=26) if False else dict(type='array', var='words_score', label='words_score（每个单词的总分）', cell=70, h=130),
        dict(type='calls', h=150, hide=('words_letter', 'words_score', 'letter_dict', 'n', 'words', 'letters', 'score')),
        dict(type='text', h=50, fn=lambda S: f"本条路径得分 `now` = =={S['_inner'].get('now', 0)}==，最高 `res` = =={S.get('self.res', 0)}=="),
    ],
    watch=[('level', lambda S: S['_inner'].get('level'), 'blue'), ('now', lambda S: S['_inner'].get('now'), 'yellow'), ('flag', lambda S: S['_inner'].get('flag')),
           ('res', 'self.res', 'green')],
    skip=['words_letter.append', 'words_score.append', 'for word in words', 'for char in word', 'for letter in letters',
          'letter_dict = {}', 'words_letter = []', 'words_score = []', 'n = len(words)', 'for char, num in words_letter[level].items()'],
    max_steps=90,
    captions={
        'words_letter[-1][char] =': '统计 `{char}` 的个数，同时把它的分数累加进这个单词的总分',
        'words_score[-1] +=': '`{word}` 的总分累加到 `{words_score[-1]}`',
        'letter_dict[letter] =': '统计字母表里每个字母的个数：`letter_dict = {letter_dict}`',
        'self.res = 0': '预处理完成：每个单词需要的字母 `words_letter` 与得分 `words_score` 都备好了，开始 dfs',
        'self.dfs(0, n': '从第 0 个单词开始 dfs，当前得分 0',
        'if level == n': lambda S, B, ret: ('`level == n` → ==所有单词都决定完了==，到达叶子' if S['_inner'].get('level') == S['_inner'].get('n')
                                            else f"`level = {S['_inner'].get('level')}`：决定第 {S['_inner'].get('level')} 个单词要不要加入"),
        25: '叶子处理完了 → 返回上一层',
        'self.res = max': lambda S, B, ret: f"更新答案：`res = max({B['self.res']}, {S['now']})` = =={S['self.res']}==",
        'self.dfs(level + 1, n, letter_dict, now, ': '先试「不加入」当前单词：得分不变，进入下一层',
        'flag = True': '再试「加入」：先检查字母够不够，默认 `flag = True`',
        'if num > letter_dict': '需要 `{char}` ×`{num}`，剩余 `{letter_dict.get(char, 0)}` → {"==不够，这个单词不能选==" if num > letter_dict.get(char, 0) else "够用"}',
        'flag = False': '字母不够 → `flag = False`，跳出检查',
        'break': '不用再查了，直接跳出',
        'if flag': lambda S, B, ret: '`flag = True` → 字母足够，可以加入这个单词' if S['_inner'].get('flag') else '`flag = False` → 这个单词放弃，回到上一层',
        'letter_dict[char] -= num': '加入单词：扣掉 `{char}` ×`{num}`，`letter_dict[{char!r}]` = {letter_dict[char]}',
        'now + words_score[level]': '递归：这个单词选上，得分加 `words_score[{B.level}]`，进入下一层',
        'letter_dict[char] += num': '回溯：把 `{char}` ×`{num}` 还回字母表，不影响其他分支',
        'return self.res': '全部 `2^n` 种选法试完，最高得分 ==`{ret}`==',
    },
    cards=dict(
        one_liner='先预处理每个单词的字母与得分，再 dfs 枚举取舍',
        complexity='时间 `O(2^n · L)`，空间 `O(n)`',
        problem=['单词表 `words`、字母表 `letters`、字母得分 `score`',
                 '每个字母、每个单词最多用一次，求最高总分',
                 '本视频：`["ax","xxz"]`，字母 `z a x x`，a=4, x=5, z=10 → 20'],
        quote='由于题目中的单词最多就14个，因此可以先预处理出每个单词需要消耗的字母集合以及其对应的得分。接下来直接进行dfs，每一轮都可以选择是否将当前单词加入到最后答案当中',
        quote_src='—— yiduobo 题解',
        idea=['单词最多 14 个，最坏 `2^14` 种状态，直接暴力 dfs',
              '预处理：每个单词要消耗的字母计数 + 单词总分',
              'dfs 到第 `level` 个单词：先不选；字母够就扣掉、递归、再还回'],
        result='所有取舍试完，最高得分 20',
        summary=['时间 `O(2^n · L)`，空间 `O(n)`，n ≤ 14 可接受',
                 '预处理后，每次判断单词能否选只需比较字母计数',
                 '易错：选完递归返回后，必须把扣掉的字母加回 `letter_dict`',
                 '不选分支放在最前，选的分支才需要扣/还字母',
                 '与灵神写法对比：灵神逐字母扣并回撤，这里按字母计数一次扣整个单词'],
    ),
)
