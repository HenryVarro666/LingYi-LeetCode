def _groups(S):
    fa = S.get('fa')
    if not fa:
        return ''
    def root(c):
        while fa[c] != c:
            c = fa[c]
        return c
    g = {}
    for c in range(26):
        g.setdefault(root(c), []).append(chr(97 + c))
    parts = [f"[{chr(97 + r)}: {''.join(m)}]" for r, m in sorted(g.items()) if len(m) > 1]
    return '等价小组（代表元：成员）  ' + ('　'.join(parts) if parts else '（还没有合并）')


CONFIG = dict(
    num=1061, title='按字典序排列最小的等效字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='并查集 · 小的并到大的前面',
    tags=[],
    code='''
class Solution(object):
    def smallestEquivalentString(self, s1, s2, baseStr):

        fa = list(range(26))

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for char1, char2 in zip(s1, s2):
            x = ord(char1) - 97
            y = ord(char2) - 97

            fa_x = find(x)
            fa_y = find(y)
            if fa_x != fa_y:
                if fa_x < fa_y:
                    fa[fa_y] = fa_x
                else:
                    fa[fa_x] = fa_y

        return ''.join([chr(find(ord(char) - 97) + 97) for char in baseStr])
''',
    call='Solution().smallestEquivalentString("abc", "cde", "eed")',
    expect='aab',
    views=[
        dict(type='text', fn=lambda S: '等价对：' + '　'.join(f'{a}={b}' for a, b in zip(S['s1'], S['s2'])) + f"　　baseStr = {S['baseStr']}", size=28, h=70),
        dict(type='array', var='fa[:8]', label='fa[i]：字母 i 的父节点（只显示前 8 个：0=a … 7=h）',
             pointers={'x': 'blue', 'y': 'pink'}, h=230,
             color=lambda S, i, v: 'green' if v != i else None),
        dict(type='text', fn=_groups, size=24, h=60),
        dict(type='calls', h=110),
    ],
    watch=[('x', lambda S: S.get('x') if 'fa_x' in S or S['_line'] in (13, 14) else None, 'blue'),
           ('y', lambda S: S.get('y') if 'y' in S else None, 'pink'),
           ('fa_x', lambda S: S.get('fa_x'), 'green'), ('fa_y', lambda S: S.get('fa_y'), 'orange')],
    captions={
        'fa = list(range(26))': '26 个字母编号 0–25，`fa[i] = i`：每个字母自成一组、自己是自己的代表元',
        'if fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] = {S.fa[S.x]}` ≠ {S.x} → 还不是代表元，向上找' if S.fa[S.x] != S.x else f'`fa[{S.x}] = {S.x}`：{S.x} 就是代表元'),
        'fa[x] = find': '找到根后路径压缩：让 `x` 直接指向代表元',
        'return fa[x]': '`find` 返回代表元 `{ret}`',
        'for char1, char2': lambda S, B, r: (f'取下一对等价字母 `{S.char1}` 和 `{S.char2}`' if B.get('char1') != S.char1 or B.get('char2') != S.char2 else '所有等价对处理完，接着给 `baseStr` 的每个字母找代表元'),
        'x = ord': '把字母 `{char1}` 换成编号：`x = {x}`',
        'y = ord': '把字母 `{char2}` 换成编号：`y = {y}`',
        'fa_x = find': '调用 `find({x})`：求 `{x}` 所在组的代表元',
        'fa_y = find': '调用 `find({y})`：求 `{y}` 所在组的代表元',
        'if fa_x != fa_y': lambda S, B, r: (f'代表元 {S.fa_x} ≠ {S.fa_y} → 两组不同，需要合并' if S.fa_x != S.fa_y else f'代表元相同（都是 {S.fa_x}）→ 已在同一组，不用合并'),
        'if fa_x < fa_y': lambda S, B, r: (f'`{S.fa_x} < {S.fa_y}`：字典序小的 {chr(97 + S.fa_x)} 当代表元' if S.fa_x < S.fa_y else f'`{S.fa_x} > {S.fa_y}`：字典序小的 {chr(97 + S.fa_y)} 当代表元'),
        'fa[fa_y] = fa_x': '大的并到小的：`fa[{fa_y}] = {fa_x}`',
        'fa[fa_x] = fa_y': '大的并到小的：`fa[{fa_x}] = {fa_y}`',
        'return ': '每个字母 `find` 一下得到该组最小字母，拼成 `baseStr` 的答案',
    },
    cards=dict(
        one_liner='字母是点、等价是边：合并时让字典序小的做代表元',
        complexity='时间 `O(n + m)`，空间 `O(1)`（26 个字母）',
        problem=['`s1[i]` 与 `s2[i]` 等价，等价关系可传递',
                 '求 `baseStr` 在这些等价关系下字典序最小的字符串',
                 '本视频：`s1 = "abc"`，`s2 = "cde"`，`baseStr = "eed"` → `"aab"`'],
        quote='如果将单个字母视为图中的点，那么字母间的等价关系就可以视为无向图中的边，在同一个连通分量间的字符则可以互相替换。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每一对等价关系，用并查集维护字符间的连通性',
              '合并时把字典序较大的代表元并到较小的下面',
              '这样每个字符 `find` 一次，直接得到可替换的最小字符'],
        summary=['时间 `O(n + m)`：字母只有 26 个，`find` 近似 `O(1)`',
                 '判断 `fa_x != fa_y` 再合并，同组的不用重复处理',
                 '最后别忘了把编号转回字母：`chr(… + 97)`',
                 '原文 `fa = range(26)` 是 Python 2 写法（返回列表），Python 3 的 range 不能赋值，已改为 `list(range(26))`',
                 '对比灵神：灵神用字母当字典的键并 `sorted` 比较代表元，这里用编号和 if/else'],
    ),
)
