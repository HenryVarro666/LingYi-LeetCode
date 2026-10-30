def _letters(x):
    return ''.join(chr(97 + i) for i in range(26) if x >> i & 1)


def _top(S):
    if 'word' not in S or 'now' not in S:
        return '用 26 位二进制数表示单词里有哪些字母'
    return f"`{S['word']!r}` 的二进制表示 `now` = {S['now']}，对应字母 =={_letters(S['now'])}=="


CONFIG = dict(
    num=2135, title='统计追加字母可以获得的单词数', difficulty='Medium', category='位运算',
    author='yiduobo', technique='26 位二进制表示字母集合 · 集合查找',
    tags=[],
    code='''
class Solution(object):
    def wordCount(self, startWords, targetWords):

        num_set = set()
        for word in startWords:
            now = 0
            for char in word:
                now += (1 << (ord(char) - 97))
            num_set.add(now)
        
        res = 0
        for word in targetWords:
            now = 0
            for char in word:
                now += (1 << (ord(char) - 97))
            for char in word:
                if (now ^ (1 << (ord(char) - 97))) in num_set:
                    res += 1
                    break
        
        return res
''',
    call='Solution().wordCount(["ab","a","bcd"], ["abc","bcd","ba"])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=28, h=60),
        dict(type='array', var='startWords', label='startWords', cell=110, h=190),
        dict(type='array', var='targetWords', label='targetWords', cell=110, h=190),
        dict(type='set', var='num_set', label='num_set（start 单词的字母集）', fmt=lambda x: f'{_letters(x)}', h=130, font=34),
    ],
    watch=[('word', 'word', 'blue'), ('char', 'char'), ('now', 'now', 'purple'), ('res', 'res', 'green')],
    captions={
        'num_set = set()': '`num_set` 收集 startWords 每个单词的二进制表示',
        'now = 0': '`now = 0`：一个字母都还没有',
        'now += (1 <<': '字母 `{char}` 占第 `{ord(char) - 97}` 位 → `now` = {now}',
        'num_set.add': '`{word}` 的字母集 =={_letters(now)}== 放进 `num_set`',
        'res = 0': '再来遍历 targetWords',
        'for word in targetWords': lambda S, B, ret: (f'考察目标单词 `{S.word}`' if 'word' in S and S.word != B.get('word') else '全部考察完'),
        'if (now ^': lambda S, B, ret: (f"去掉 `{S.char}` → =={_letters(S.now ^ (1 << (ord(S.char) - 97)))}==，在 `num_set` 中 → ==能由它追加 {S.char} 得到=="
                                        if S.now ^ (1 << (ord(S.char) - 97)) in S.num_set
                                        else f"去掉 `{S.char}` → =={_letters(S.now ^ (1 << (ord(S.char) - 97)))}==，不在 `num_set` 中"),
        'res += 1': '`{word}` 可以转换得到：`res` → {res}',
        'break': '已经可以转换，考察下一个单词',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='目标单词的字母集，恰好比某个起始单词多一个字母',
        complexity='时间 `O(L)`，空间 `O(n)`',
        problem=['起始单词追加一个没出现过的字母，再任意重排，能否得到目标单词',
                 '统计 targetWords 中能得到的单词个数',
                 '本视频：`["ab","a","bcd"]`，`["abc","bcd","ba"]` → `2`'],
        quote='对于targetWords中的某个单词而言，只要其包含的字母集比startWords中某个单词包含的字母集恰好多出一个字母，就可以从startWords中的这个单词完成转换。',
        quote_src='—— yiduobo 题解原文',
        idea=['重排可任意，每个字母只出现一次 → 只需比较字母集',
              '用 26 位二进制数表示字母集，start 的都收进 `num_set`',
              '对目标单词逐个字母去掉，结果出现在 `num_set` 就答案加一'],
        summary=['时间 `O(L)`，空间 `O(n)`',
                 '`ba` 去掉 b 得 `a`，在集合里 → 可转换；`bcd` 本身在集合里，但去掉任一字母都不在 → 不行',
                 '用 `+=` 累加二进制位，因为单词内无重复字母，效果等同 `|=`',
                 '对比灵神：同样的掩码思路；灵神用 `|=`，本文用 `+=`'],
    ),
)
