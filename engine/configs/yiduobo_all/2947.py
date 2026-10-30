def _col(S, i, v):
    return 'purple' if v in 'aeiou' else None



CONFIG = dict(
    num=2947, title='统计美丽子字符串 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='暴力枚举起点终点',
    code='''
class Solution(object):
    def beautifulSubstrings(self, s, k):

        vowel_set = set(['a', 'e', 'i', 'o', 'u'])

        res = 0
        for i in range(len(s)):
            vowel = consonants = 0
            for j in range(i, len(s)):
                if s[j] in vowel_set:
                    vowel += 1
                else:
                    consonants += 1

                if vowel == consonants and vowel * consonants % k == 0:
                    res += 1
        
        return res
''',
    call='Solution().beautifulSubstrings("baeyh", 2)',
    expect=2,
    max_steps=110,
    views=[
        dict(type='string', var='s', label='s（紫 = 元音；蓝窗口 = 子串 [i, j]）', pointers={'i': 'blue', 'j': 'pink'},
             window=('i', 'j'), color=_col, h=230),
        dict(type='text', fn=lambda S: f"元音 `{S['vowel']}`　辅音 `{S['consonants']}`　美丽子串 `res` = =={S['res']}==" if 'vowel' in S else '', h=80),
    ],
    watch=['i', 'j', ('vowel', 'vowel', 'purple'), 'consonants', ('res', 'res', 'green')],
    captions={
        'vowel_set = set': '用集合存元音，判断更方便',
        'res = 0': '`res` 统计美丽子字符串个数',
        'for i in range': '枚举子串起点 `i = {i}`',
        'vowel = consonants = 0': '新起点，元音和辅音计数清零',
        'for j in range(i': '枚举终点 `j = {j}`，子串 `s[{i}..{j}]`',
        'if s[j] in vowel_set': lambda S, B, r: (f"`'{S.s[S.j]}'` 是元音" if S.s[S.j] in 'aeiou' else f"`'{S.s[S.j]}'` 不是元音，是辅音"),
        'vowel += 1': '元音 +1：`vowel` = {vowel}',
        'consonants += 1': '辅音 +1：`consonants` = {consonants}',
        'if vowel == consonants and': lambda S, B, r: (f"`{S.vowel} == {S.consonants}` 且 `{S.vowel}×{S.consonants} % {S.k}` = {S.vowel * S.consonants % S.k} → ==美丽=="
                                                       if (S.vowel == S.consonants and S.vowel * S.consonants % S.k == 0)
                                                       else (f"元音 {S.vowel} ≠ 辅音 {S.consonants} → 不美丽" if S.vowel != S.consonants
                                                             else f"数量相等，但 `{S.vowel * S.consonants} % {S.k}` ≠ 0 → 不美丽")),
        'res += 1': '又找到一个美丽子串：`res` = =={res}==',
        'return res': '枚举完毕，共 ==`{res}`== 个',
    },
    cards=dict(
        one_liner='数据范围小，起点终点双重循环直接数',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['元音数 == 辅音数，且乘积能被 `k` 整除的非空子串叫美丽子串，求个数',
                 '示例：`"baeyh"`，`k = 2` → `2`'],
        quote='题目的数据规模不大，因此可以直接暴力计算。枚举子字符串的起点i，然后从i开始不断向后枚举子字符串的终点j，同时计算子字符串中元音和辅音的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 1000`，`O(n²)` 够用', '固定起点 `i`，终点 `j` 右移时增量更新元音/辅音数',
              '每次 `vowel == consonants` 且乘积被 `k` 整除就 `res += 1`'],
        summary=['时间 `O(n²)`，空间 `O(1)`', '增量更新计数，不必每个子串重新数',
                 '对比灵神：灵神用前缀和 + 哈希表做到 `O(n)`，适用于更大数据（II）',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
