def _cmp(S):
    if 'i' not in S or 'j' not in S:
        return ''
    s, sub, i, j = S['s'], S['sub'], S['i'], S['j']
    if i + j >= len(s):
        return ''
    a, b = s[i + j], sub[j]
    if a == b:
        return f"`s[{i+j}] = {a}`  ==相同=="
    if b in S['reverse_mapping'][a]:
        return f"`s[{i+j}] = {a}`，`sub[{j}] = {b}`  ==可替换=={b}→{a}"
    return f"`s[{i+j}] = {a}`，`sub[{j}] = {b}`  ==不匹配=="


CONFIG = dict(
    num=2301, title='替换字符后匹配', difficulty='Hard', category='字符串',
    author='yiduobo', technique='枚举起点 · 反向映射表',
    tags=[],
    code='''
class Solution(object):
    def matchReplacement(self, s, sub, mappings):

        reverse_mapping = {}
        for char in s:
            if char not in reverse_mapping:
                reverse_mapping[char] = set()
        
        for old, new in mappings:
            if new not in reverse_mapping:
                continue
            reverse_mapping[new].add(old)
        
        for i in range(len(s) - len(sub) + 1):
            flag = True
            for j in range(len(sub)):
                if s[i + j] != sub[j] and sub[j] not in reverse_mapping[s[i + j]]:
                    flag = False
                    break
            
            if flag:
                return True
        
        return False
''',
    call='Solution().matchReplacement("fool3e7b", "leet", [["e","3"],["t","7"],["t","8"]])',
    expect=True,
    views=[
        dict(type='text', fn=_cmp, size=30, h=80),
        dict(type='string', var='s', pointers={'i + j': 'blue'}, window=('i', 'i + len(sub) - 1'), h=230, label='s（框 = 起点 i 开始的子串）'),
        dict(type='string', var='sub', pointers={'j': 'pink'}, h=200, label='sub'),
        dict(type='map', var='reverse_mapping', fmt=lambda k, v: k + ' ← {' + ','.join(sorted(v)) + '}', h=240),
    ],
    skip=['if char not in reverse_mapping'],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('flag', 'flag', 'green')],
    captions={
        'reverse_mapping = {}': '`reverse_mapping[c]`：能变成 `c` 的所有原字符（键只需要 `s` 里出现过的字符）',
        'reverse_mapping[char] = set()': '`s` 里的字符 `{char}` 先配一个空集合',
        'if new not in reverse_mapping': lambda S, B, r: (f"`new = {S.new}` 不在 `s` 里，这条映射用不上 → 跳过" if S.new not in S.reverse_mapping
                                                           else f"`new = {S.new}` 在 `s` 里，这条映射可能有用"),
        'reverse_mapping[new].add(old)': '记下：`{old}` 可以变成 `{new}`，`reverse_mapping[{new}]` = {sorted(reverse_mapping[new])}。一对多时同一个 `old` 出现在多个集合里，互不影响',
        'for i in range': '枚举起点 `i = {i}`，对齐 `s[{i}:{i + len(sub)}]`',
        'flag = True': '先假设从 `{i}` 开始能匹配',
        'for j in range': '比较第 `{j}` 个字符',
        'if s[i + j] != sub[j]': lambda S, B, r: (f"`s[{S.i + S.j}] = {S.s[S.i + S.j]}` 等于 `sub[{S.j}] = {S.sub[S.j]}` → 直接匹配" if S.s[S.i + S.j] == S.sub[S.j]
                                                  else (f"`{S.s[S.i + S.j]}` ≠ `{S.sub[S.j]}`，但 `{S.sub[S.j]}` 能变成 `{S.s[S.i + S.j]}`（在 `reverse_mapping[{S.s[S.i + S.j]}]` 里）→ 也算匹配"
                                                        if S.sub[S.j] in S.reverse_mapping[S.s[S.i + S.j]]
                                                        else f"`{S.s[S.i + S.j]}` ≠ `{S.sub[S.j]}`，也换不过去 → ==不匹配==")),
        'flag = False': '这个起点失败：`flag = False`',
        'break': '不用再比后面的字符，换下一个起点',
        'if flag': lambda S, B, r: ('整段都匹配 → 找到了' if S.flag else '这个起点没成功，继续下一个'),
        'return True': '返回 ==True==',
        'return False': '所有起点都失败 → ==False==',
    },
    cards=dict(
        one_liner='枚举起点，用“谁能变成它”的反向表做暴力匹配',
        complexity='时间 `O(nm)`，空间 `O(n + k)`',
        problem=['`sub` 里的字符可按 `mappings` 替换（每个字符最多换一次），能否变成 `s` 的子串',
                 '示例：`s="fool3e7bar"`，`sub="leet"`，`e→3`、`t→7`、`t→8` → `true`',
                 '本视频：`s="fool3e7b"` → `true`'],
        quote='题目的数据规模不大，直接在s中枚举匹配的起点，然后一趟遍历，利用哈希表来进行暴力匹配也是可行的。需要注意题目中的转化是可以一对多的。',
        quote_src='—— yiduobo 题解原文',
        idea=['对 `s` 里每个字符 `c`，记下所有能变成 `c` 的原字符，存成集合',
              '枚举起点 `i`，逐位比 `s[i+j]` 和 `sub[j]`',
              '不等时，只要 `sub[j]` 在 `reverse_mapping[s[i+j]]` 里就还算匹配'],
        summary=['时间最坏 `O(nm)`，空间 `O(n + k)`',
                 '易错：转化是一对多（一个 `old` 可变成多个 `new`），所以按“目标字符”收集原字符更方便',
                 '易错：只能把 `sub` 的字符换成 `s` 的字符，方向不能反',
                 '原文为 Python 2 写法（`class Solution(object)`），Python 3 可直接运行，代码未改动'],
    ),
)
