CONFIG = dict(
    num='LCR 033', title='字母异位词分组', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='排序后的字符串作 key 分组',
    tags=[],
    code='''
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d = defaultdict(list)
        for s in strs:
            d[''.join(sorted(s))].append(s)  # sorted(s) 相同的字符串分到同一组
        return list(d.values())
''',
    call="Solution().groupAnagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])",
    expect=[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']],
    views=[
        dict(type='array', var='strs', label='strs（黄 = 当前处理的 s）', cell=130, h=170,
             color=lambda S, i, v: 'yellow' if 's' in S and S['s'] == v else None),
        dict(type='text', size=30, h=70,
             fn=lambda S: f"`sorted({S['s']!r})` → ==`{''.join(sorted(S['s']))}`==" if 's' in S else ''),
        dict(type='map', var='d', label='d（排序后的字符串 → 同一组的原字符串）', fmt=lambda k, v: f"'{k}': {v}", h=300, font=30),
    ],
    watch=[('s', 's', 'blue'), ('key', lambda S: ''.join(sorted(S['s'])) if 's' in S else None, 'orange'), ('组数', lambda S: len(S['d']) if 'd' in S else 0, 'green')],
    captions={
        'd = defaultdict': '哈希表 `d`：==排序后的字符串== 当 key，原字符串组成的列表当 value',
        'for s in strs': lambda S, B, r: (f'取出 `{S.s!r}`' if 's' not in B or S.s != B.s else '所有字符串都分好组了'),
        'd[': lambda S, B, r: (
            f"`sorted({S.s!r})` = `{''.join(sorted(S.s))!r}`：key 已存在 → `{S.s!r}` ==加入这一组=="
            if ''.join(sorted(S.s)) in B['d']
            else f"`sorted({S.s!r})` = `{''.join(sorted(S.s))!r}`：新的 key → 新开一组，放入 `{S.s!r}`"),
        'return list(d.values())': '每个 value 就是一组异位词，把所有 value 放进列表返回：`{ret}`',
    },
    cards=dict(
        one_liner='字母次数相同 ⇔ 排序后一样：拿排序结果当 key 分组',
        complexity='时间 `O(nm log m)`，空间 `O(nm)`',
        problem=['把每种字母出现次数都相同的字符串（变位词）分到同一组，组的顺序不限',
                 '示例：`["eat","tea","tan","ate","nat","bat"]`',
                 '→ `[["bat"],["nat","tan"],["ate","eat","tea"]]`'],
        quote='当且仅当两个字符串排序后一样，这两个字符串才能分到同一组。……把排序后的字符串当作 key，原字符串组成的列表（即答案）当作 value。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`aab`、`aba`、`baa` 排序后都是 `aab`；`abb` 排序后是 `abb`，不同',
              '所以排序结果能当“组号”：用哈希表按组号收集原字符串',
              '`defaultdict(list)`：新 key 自动得到空列表，直接 `append`'],
        summary=['时间 `O(nm log m)`：n 个字符串，每个排序 `O(m log m)`；空间 `O(nm)`',
                 '`sorted(s)` 返回列表，不能直接当 key，要 `\'\'.join(...)` 变成字符串（或转 tuple）',
                 '返回 `list(d.values())`，组的先后顺序不限',
                 '注意空字符串 `""`：排序后还是 `""`，自成一组'],
    ),
)
