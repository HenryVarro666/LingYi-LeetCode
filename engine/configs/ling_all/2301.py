def _pairs(S):
    if 'i' not in S:
        return ''
    sub, s, mp, i = S['sub'], S['s'], S['mp'], S['i']
    seg = s[i - len(sub): i]
    parts = []
    for x, y in zip(sub, seg):
        if x == y:
            parts.append(f'{x}={y}')
        elif (x, y) in mp:
            parts.append(f'{x}→{y}')
        else:
            parts.append(f'=={x}≠{y}==')
    return f"`sub` 对 `s[{i - len(sub)}:{i}]`：  " + '   '.join(parts)


def _all(S, B, ret):
    sub, s, mp, i = S.sub, S.s, S.mp, S.i
    seg = s[i - len(sub): i]
    bad = [(x, y) for x, y in zip(sub, seg) if not (x == y or (x, y) in mp)]
    if not bad:
        return f"枚举以 `s[{i - len(sub)}:{i}] = '{seg}'` 为子串：每个字符要么相同，要么在 `mp` 里 → ==全部匹配=="
    x, y = bad[0]
    return f"子串 `'{seg}'`：`'{x}'` 既不等于 `'{y}'`，`('{x}','{y}')` 也不在 `mp` 里 → 不匹配，试下一个"


CONFIG = dict(
    num=2301, title='替换字符后匹配', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='暴力枚举 · 哈希集合查映射',
    tags=[],
    code='''
class Solution:
    def matchReplacement(self, s: str, sub: str, mappings: List[List[str]]) -> bool:
        mp = set((x, y) for x, y in mappings)
        for i in range(len(sub), len(s) + 1):
            if all(x == y or (x, y) in mp for x, y in zip(sub, s[i - len(sub): i])):
                return True
        return False
''',
    call='Solution().matchReplacement("fool3e7b", "leet", [["e","3"],["t","7"],["t","8"]])',
    expect=True,
    views=[
        dict(type='text', fn=_pairs, size=30, h=90),
        dict(type='string', var='s', window=('i - len(sub)', 'i - 1'), h=210, label='s（框 = 当前枚举的子串）'),
        dict(type='string', var='sub', h=170, label='sub'),
        dict(type='set', var='mp', fmt=lambda p: f'{p[0]}→{p[1]}', h=170),
    ],
    watch=[('i', 'i', 'blue'), ('len(sub)', 'len(sub)', 'cyan')],
    captions={
        'mp = set': '把 `mappings` 变成集合 `mp`，“`x` 能否换成 `y`”变成 `O(1)` 的查询；一对多（`t→7`、`t→8`）也没问题',
        'for i in range': '枚举子串右端点 `i = {i}`，子串是 `s[{i - len(sub)}:{i}]`',
        'if all(': _all,
        'return True': '找到一个匹配的子串 → 返回 ==True==',
        'return False': '所有子串都试过了 → ==False==',
    },
    cards=dict(
        one_liner='暴力枚举子串，逐字符看“相同或可替换”',
        complexity='时间 `O(nm)`，空间 `O(k)`（k 为映射数）',
        problem=['`sub` 里的字符可按 `mappings` 替换（每个字符最多换一次），能否变成 `s` 的子串',
                 '示例：`s="fool3e7bar"`，`sub="leet"`，`e→3`、`t→7` → `true`',
                 '本视频：`s="fool3e7b"`，`sub="leet"` → `true`'],
        quote='暴力枚举 s 的所有子串，看与 sub 是否匹配。匹配需要满足对应字符相同，或者 sub 的字符可以通过 mappings 转换到 s 的对应字符上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个起点对应一个长为 `len(sub)` 的子串，`zip` 一一配对',
              '配对 `(x, y)` 合法：`x == y`，或 `(x, y)` 在映射集合里',
              '用 `all(...)` 一次判完，一个子串不合法就换下一个'],
        summary=['时间 `O(nm)`，空间 `O(k)`',
                 '易错：映射有方向，只能 `sub` 的 `old` 换成 `new`，不能反过来（示例 2 的 `0` 不能换回 `o`）',
                 '易错：枚举范围 `i` 从 `len(sub)` 到 `len(s)` 含右端',
                 '字符不能换两次：只查一步 `(x, y)`，不做传递闭包'],
    ),
)
