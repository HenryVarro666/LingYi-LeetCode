CONFIG = dict(
    num=819, title='最常见的单词', difficulty='Easy', category='字符串',
    author='yiduobo', technique='逐字符分词 + 哈希计数',
    code='''
class Solution(object):
    def mostCommonWord(self, paragraph, banned):

        ban_set = set(banned)
        count_dict = {}
        now = ''
        max_cnt = 0
        max_word = None
        for char in paragraph + ' ':
            if char >= 'a' and char <= 'z':
                now += char
            elif char >= 'A' and char <= 'Z':
                now += chr(ord(char) + 32)
            else:
                if now != '' and now not in banned:
                    count_dict[now] = count_dict.get(now, 0) + 1
                    if count_dict[now] > max_cnt:
                        max_cnt = count_dict[now]
                        max_word = now
                now = ''

        return max_word
''',
    call='Solution().mostCommonWord("Bob hit a ball, the hit BALL", ["hit"])',
    expect='ball',
    views=[
        dict(type='text', fn=lambda S: f"当前字符 `{S['char']}` · 正在拼的单词 `{S.get('now') or '（空）'}`" if 'char' in S else '', size=30, h=70),
        dict(type='set', var='ban_set', h=130, label='ban_set（禁用词）'),
        dict(type='map', var='count_dict', h=330, label='count_dict（单词出现次数）'),
    ],
    watch=[('char', 'char', 'blue'), ('now', 'now', 'cyan'), ('max_word', 'max_word', 'green'), ('max_cnt', 'max_cnt', 'orange')],
    captions={
        'ban_set = set': '禁用词放进集合：`{ban_set}`',
        'count_dict = {}': '`count_dict` 统计每个单词出现几次',
        'for char in paragraph': '逐个字符扫描，末尾补的空格保证最后一个单词也会被结算',
        "if char >= 'a'": lambda S, B, r: (f'`{S.char}` 是小写字母 → 接到 `now` 后面' if 'a' <= S.char <= 'z' else f'`{S.char}` 不是小写字母，看看是不是大写'),
        'now += char': '`now = {now}`',
        "elif char >= 'A'": lambda S, B, r: (f'`{S.char}` 是大写字母 → 转成小写再接上' if 'A' <= S.char <= 'Z' else f'`{S.char}` 是标点或空格 → 一个单词结束了'),
        'now += chr': '加 32 就是转小写：`now = {now}`',
        "if now != ''": lambda S, B, r: (f'单词 `{S.now}` 不为空且不在 banned 里 → 计数' if S.now != '' and S.now not in S.banned else (f'`{S.now}` 是禁用词 → 不计数' if S.now != '' else '`now` 为空（连续标点或空格）→ 没有单词要结算')),
        'count_dict[now] = ': '`count_dict[{now}] = {count_dict[now]}`',
        'if count_dict[now] > max_cnt': '`{count_dict[now]}` 比当前最多 `{max_cnt}` 大吗 → {"是，更新答案" if count_dict[now] > max_cnt else "否"}',
        'max_cnt = count_dict': '最多次数更新为 `{max_cnt}`',
        'max_word = now': '答案暂定 `{max_word}`',
        "now = ''": '清空 `now`，准备拼下一个单词',
        'return max_word': '出现次数最多的非禁用词：`{max_word}`（{max_cnt} 次）',
    },
    cards=dict(
        one_liner='边分词边计数，禁用词直接不统计',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`（n 为段落长，m 为禁用词数）',
        problem=['给一段文字 `paragraph` 和禁用词列表 `banned`',
                 '返回出现次数最多、且不在禁用词里的单词；不区分大小写，答案用小写，保证唯一',
                 '示例：`"Bob hit a ball, the hit BALL"`，`banned=["hit"]` → `"ball"`'],
        quote='将每个单词转换成小写，若其未出现在banned中那么就统计出现次数，选择出现最多的单词即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['一个字符一个字符扫：字母拼进 `now`，大写字母加 32 变小写',
              '遇到非字母，说明一个单词结束：不在禁用词里就计数',
              '计数后顺手和历史最大值比较，不用再遍历一遍哈希表'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：末尾补一个空格，否则最后一个单词不会结算',
                 '`now != \'\'` 要判断：连续标点会产生空单词',
                 '代码里直接用 `now not in banned`（列表），用 `ban_set` 会更快'],
    ),
)
