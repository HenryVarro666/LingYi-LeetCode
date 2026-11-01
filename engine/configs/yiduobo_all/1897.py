CONFIG = dict(
    num=1897, title='重新分配字符使所有字符串都相等', difficulty='Easy', category='字符串',
    author='yiduobo', technique='字典计数 · 是否 n 的倍数',
    tags=[],
    code='''
class Solution(object):
    def makeEqual(self, words):

        cnt_dict = {}
        for word in words:
            for char in word:
                cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        for cnt in cnt_dict.values():
            if cnt % len(words) != 0:
                return False
        
        return True
''',
    call='Solution().makeEqual(["ab","a","bb","ab"])',
    expect=False,
    views=[
        dict(type='array', var='words', h=190, label='words', cell=100,
             color=lambda S, i, v: 'blue' if 'word' in S and 'cnt' not in S and v == S['word'] and i == _first(S) else None),
        dict(type='map', var='cnt_dict', h=270, label='cnt_dict：每种字符的总个数', fmt=lambda k, v: f'{k}:{v}'),
        dict(type='text', size=32, h=90, fn=lambda S: (
            f"字符串总数 `n = {len(S['words'])}`" + (f"；当前字符 `{S['char']}`" if 'char' in S and 'cnt' not in S else '')
            + (f"；检查个数 `{S['cnt']}`" if 'cnt' in S else ''))),
    ],
    watch=[('word', 'word', 'blue'), ('char', 'char', 'cyan'), ('cnt', 'cnt', 'yellow')],
    captions={
        'cnt_dict = {}': '空字典，记录每种字符在所有字符串里一共出现几次',
        'cnt_dict[char] =': '字符 `{char}` 累计出现 =={cnt_dict[char]}== 次（不区分在哪个字符串里）',
        'if cnt % len(words)': lambda S, B, r: (
            f'`{S.cnt} % {len(S.words)} = {S.cnt % len(S.words)}` ≠ 0 → ==这种字符没法平均分给 {len(S.words)} 个字符串=='
            if S.cnt % len(S.words) else f'`{S.cnt} % {len(S.words)} = 0` → 能平均分，继续'),
        'return False': '有一种字符分不匀 → ==False==',
        'return True': '所有字符都能平均分 → True',
    },
    cards=dict(
        one_liner='字符能任意搬，所以只看每种字符的总数能否被 n 整除',
        complexity='时间 `O(L)`，空间 `O(1)`（L 为字符总数）',
        problem=['可以把一个字符串里的任一字符，移到另一个字符串的任意位置',
                 '问能不能让所有字符串都变成同一个',
                 '本视频：`["ab","a","bb","ab"]` → `false`'],
        quote='只需要每种字符出现的次数都是n的倍数，就可以将当前字符平均分配到各个字符串上的同一位置，从而使得所有字符串都相等。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目允许任意调整每个字符串的构成，所以只关心每种字符的总数',
              '用字典数一遍：每种字符总共出现多少次',
              '若某种字符的总数不是 `n` 的倍数，就一定分不匀'],
        summary=['时间 `O(L)`，空间 `O(1)`',
                 '`n` 是字符串个数 `len(words)`，不是字符串长度',
                 '本例 `a` 共 3 个，`3 % 4 != 0`，一发现就提前返回 False；若全部整除则返回 True',
                 '对比灵神：灵神用长度 26 的数组计数，yiduobo 用字典，思路一致'],
    ),
)


def _first(S):
    try:
        return S['words'].index(S['word'])
    except Exception:
        return -1
