_GROUP_COLORS = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _grp_color(S, i, v):
    d = S.get('d')
    if not d:
        return None
    key = ''.join(sorted(v))
    if key in d and v in d[key]:
        return _GROUP_COLORS[list(d).index(key) % len(_GROUP_COLORS)]
    return None


def _cur(S):
    if 's' not in S:
        return None
    return S['strs'].index(S['s'])


def _sort_text(S):
    if 'sorted_s' not in S or 's' not in S:
        return '每个字符串排序后作为 key'
    return f"`\"{S['s']}\"` 排序 → `\"{S['sorted_s']}\"`（作为哈希表的 key）"


def _check(S, B, ret):
    k = S.sorted_s
    if k not in S.d:
        return f'首次遇到 `"{k}"`：哈希表里还没有这一组'
    return f'`"{k}"` 已经有一组了：`{S.d[k]}` → 直接追加'


CONFIG = dict(
    num=49, title='字母异位词分组', difficulty='Medium', category='哈希',
    author='灵茶山艾府', technique='排序后的字符串作 key · 哈希表分组',
    code='''
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d = {}  # 用 defaultdict 的写法见【Python3 写法二】
        for s in strs:
            sorted_s = ''.join(sorted(s))  # 把 s 排序，作为 dict 的 key
            if sorted_s not in d:  # 首次遇到 sorted_s
                d[sorted_s] = []  # 创建列表
            d[sorted_s].append(s)  # 排序后相同的字符串，保存到同一组中
        return list(d.values())  # 哈希表的所有 value 就是分组结果
''',
    call='Solution().groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])',
    expect=[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']],
    views=[
        dict(type='text', fn=_sort_text),
        dict(type='array', var='strs', pointers={_cur: 'yellow'}, pointer_labels={_cur: 's'}, color=_grp_color, h=230,
             label='strs（同色 = 已分到同一组）'),
        dict(type='map', var='d', font=28, h=290,
             fmt=lambda k, v: f'"{k}" → [{", ".join(v)}]',
             label='d：排序后的字符串 → 这一组的原字符串'),
    ],
    watch=[('s', 's', 'yellow'), ('sorted_s', 'sorted_s', 'cyan'), ('组数', lambda S: len(S['d']) if 'd' in S else None)],
    captions={
        'd = {}': '`d`：==key== 是排序后的字符串，==value== 是这一组的原字符串列表',
        'for s in strs': lambda S, B, r: (f'取下一个字符串 `s = "{S.s}"`' if 's' not in B or B.s != S.s else 'for 循环结束：所有字符串都分好组了'),
        'sorted_s = ': lambda S, B, r: (f'`"{S.s}"` 排序后是 `"{S.sorted_s}"`：==互为异位词 ⇔ 排序后相等=='
                                         if S.s == S.strs[0] else f'`"{S.s}"` 排序 → `"{S.sorted_s}"`'),
        'if sorted_s not in d': _check,
        'd[sorted_s] = []': '创建列表：`d["{sorted_s}"] = []`',
        'append(s)': '`"{s}"` 放进 `"{sorted_s}"` 这一组 → `{d[sorted_s]}`',
        'return list(': '哈希表的所有 value 就是分组结果：共 =={len(d)} 组==',
    },
    cards=dict(
        one_liner='排序后相同的字符串，扔进哈希表的同一个桶',
        complexity='时间 `O(nm log m)`，空间 `O(nm)`',
        problem=['把==字母异位词==（字母相同、只是顺序不同）分到同一组，组的顺序随意',
                 '示例：`["eat","tea","tan","ate","nat","bat"]`',
                 '→ `[["bat"],["nat","tan"],["ate","eat","tea"]]`'],
        quote='如果两个字符串从小到大排序后相等，那么两个字符串就互为字母异位词，否则不是。……用哈希表分组，==把排序后的字符串当作哈希表的 key==，排序前的字符串加到对应的列表中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`eat`、`tea`、`ate` 排序后都是 `aet` → 同一个 key',
              'key 第一次出现时建空列表，之后往里追加原字符串',
              '最后把哈希表的所有 value 收集起来就是答案'],
        summary=['时间 `O(nm log m)`：n 个字符串，每个排序 `O(m log m)`；空间 `O(nm)`',
                 '`sorted(s)` 返回字符列表，要 `"".join` 成字符串才能当 key',
                 '写法二：`defaultdict(list)`，省掉"首次遇到就建空列表"的判断',
                 '`d.values()` 不是 list，返回前要包一层 `list(...)`'],
    ),
)
