CONFIG = dict(
    num=3913, title='按频率对元音排序', difficulty='Medium', category='字符串',
    author='yiduobo', technique='哈希表记次数与首位 + 双关键字排序',
    code='''
class Solution(object):
    def sortVowels(self, s):

        vowel = {
            'a': [0, None],
            'e': [0, None],
            'i': [0, None],
            'o': [0, None],
            'u': [0, None]
        }

        for index, c in enumerate(s):
            if c in vowel:
                if vowel[c][0] == 0:
                    vowel[c][1] = index
                vowel[c][0] += 1
        
        v = sorted(vowel.keys(), key=lambda d:(-vowel[d][0], vowel[d][1]))
        res = []
        p = 0
        for c in s:
            if c in vowel:
                res.append(v[p])
                vowel[v[p]][0] -= 1
                if vowel[v[p]][0] == 0:
                    p += 1
            else:
                res.append(c)

        return ''.join(res)
''',
    call='Solution().sortVowels("dienaeoaei")',
    expect='deeneiiaao',
    views=[
        dict(type='string', var='s', label='s（原串）', h=150, cell=70, pointers={'index': 'blue'}),
        dict(type='map', var='vowel', label='vowel（元音 → [次数, 首次出现下标]）', fmt=lambda k, v: f"'{k}': 次数 {v[0]}，首位 {v[1]}", h=220, font=26),
        dict(type='array', var='v', label='v（排序后的元音顺序）', h=160, cell=70, pointers={'p': 'pink'}),
        dict(type='string', var='res', label='res（已生成的结果）', h=160, cell=70),
    ],
    watch=['c', ('p', 'p', 'pink'), ('v', 'v', 'cyan')],
    skip=['for index, c in enumerate(s)', 'for c in s', "'a': [0", "'e': [0", "'i': [0", "'o': [0", "'u': [0"],
    max_steps=90,
    captions={
        'vowel = {': '`vowel` 为每个元音记录 ==[出现次数, 首次出现的下标]==',
        'if c in vowel': lambda S, B, r: (f"下标 `{S.index}` 是 `'{S.c}'`，是元音 → 要统计" if S.c in S.vowel and S['_line'] < 20 else (f"扫到 `'{S.c}'`，是元音 → 要用排好的元音替换" if S.c in S.vowel else f"`'{S.c}'` 不是元音 → 原样放进答案")),
        'if vowel[c][0] == 0': lambda S, B, r: (f"`'{S.c}'` 次数为 0，是第一次出现 → 记下首次下标" if S.vowel[S.c][0] == 0 else f"`'{S.c}'` 之前出现过，首次下标已记录"),
        'vowel[c][1] = index': "记下 `'{c}'` 首次出现的下标 `{index}`（同频次时靠它排序）",
        'vowel[c][0] += 1': "`'{c}'` 次数 → {vowel[c][0]}",
        'v = sorted': '排序：第一关键字 ==次数从大到小==，第二关键字 ==首次下标从小到大==；得到 `v = {v}`',
        'res = []': '`res` 保存答案',
        'p = 0': '`p` 指向 `v` 中当前要填的元音',
        'res.append(v[p])': "元音位置：填入 `v[{p}] = '{v[p]}'`",
        'vowel[v[p]][0] -= 1': "`'{v[p]}'` 还剩 {vowel[v[p]][0]} 个没填",
        'if vowel[v[p]][0] == 0': lambda S, B, r: (f"`'{S.v[S.p]}'` 填完了 → `p` 后移" if S.vowel[S.v[S.p]][0] == 0 else f"`'{S.v[S.p]}'` 还没填完，继续用它"),
        'p += 1': '`p` → {p}，换下一种元音',
        'res.append(c)': "辅音 `'{c}'` 原样放入 `res`",
        'return': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='哈希表记下次数和首位，双关键字排序，再扫一遍替换',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `s` 里的元音按==出现频率从高到低==重排，辅音不动',
                 '频率相同的，按在 `s` 中首次出现的位置排',
                 '示例：`"leetcode"` → `"leetcedo"`'],
        quote='使用哈希表记录每种元音字母出现的次数以及首次出现的下标。接下来对哈希表的key，按照以出现次数为第一关键字，首次出现的位置为第二关键字进行排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['`vowel[c] = [次数, 首次下标]`，第一趟遍历填表',
              '排序键 `(-次数, 首次下标)`：一次写清两个关键字',
              '第二趟遍历：元音位置依次取 `v[p]`，用完 `p += 1`'],
        summary=['时间 `O(n)`（排序只对 5 个元音），空间 `O(n)`',
                 '易错：次数为 0 时才记首次下标；没出现过的元音次数 0 排在最后，不会被用到',
                 '对比灵神：灵神靠稳定排序省掉首次下标；这里显式写出第二关键字',
                 '本视频输入：`"dienaeoaei"`'],
    ),
)
