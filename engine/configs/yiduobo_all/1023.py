def _kids(nd):
    return list(nd[0].items())


def draw_trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S.get('trie')
    if root is None:
        cv.text((x0 + 20, y0 + 30), '（先统计大写字母，再建 trie）', 24, T['dim'])
        return
    pat = S.get('pattern', '')
    cur = S.get('now')
    pos = S.get('pos')
    # 顶部：pattern 与匹配进度
    if pos is not None and pat:
        cv.text((x0 + 20, y0 + 22), 'pattern', 22, T['muted'], anchor='lm')
        for k, ch in enumerate(pat):
            X = x0 + 110 + k * 50
            c = T['green'] if k < pos else (T['yellow'] if k == pos else T['panel2'])
            cv.rect((X, y0 + 4, X + 44, y0 + 40), fill=c, r=8)
            cv.text((X + 22, y0 + 22), ch, 26, T['bg'] if c != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((x0 + 130 + len(pat) * 50, y0 + 22), '绿 = 已匹配，黄 = 下一个要匹配', 19, T['dim'], anchor='lm')
    layout, cnt, maxd = {}, [0], [0]

    def lay(nd, d):
        maxd[0] = max(maxd[0], d)
        ks = _kids(nd)
        if not ks:
            layout[id(nd)] = (float(cnt[0]), d)
            cnt[0] += 1
            return layout[id(nd)][0]
        xs = [lay(ch, d + 1) for _, ch in ks]
        layout[id(nd)] = ((xs[0] + xs[-1]) / 2, d)
        return layout[id(nd)][0]

    lay(root, 0)
    n = max(cnt[0], 1)
    gx = min(110, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - gx * (n - 1)) / 2
    top = y0 + 80
    gy = min(80, (y1 - top - 70) / max(maxd[0], 1))

    def xy(nd):
        a, d = layout[id(nd)]
        return sx + a * gx, top + d * gy

    def edges(nd):
        px, py = xy(nd)
        for ch, c in _kids(nd):
            qx, qy = xy(c)
            cv.line([(px, py + 18), (qx, qy - 18)], T['border'], 2)
            edges(c)
    edges(root)

    def nodes(nd, label):
        X, Y = xy(nd)
        c = T['yellow'] if nd is cur else (T['panel2'])
        cv.rect((X - 20, Y - 18, X + 20, Y + 18), fill=c, r=8)
        up = label.isupper()
        tc = T['bg'] if nd is cur else (T['pink'] if up else T['text'])
        cv.text((X, Y), label, 24, tc, anchor='mm', bold=True, mono=True)
        if nd[1]:
            cv.text((X + 24, Y + 20), str(nd[1]), 16, T['cyan'], anchor='lm')
        for ch, c2 in _kids(nd):
            nodes(c2, ch)
    nodes(root, '·')
    cv.text((x0 + 20, y1 - 12), '粉 = 大写字母（必须匹配），白 = 小写字母（可跳过）；青色列表 = 经过此节点的 query 下标', 18, T['dim'], anchor='lm')


CONFIG = dict(
    num=1023, title='驼峰式匹配', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='Trie 树 + DFS 跳过小写',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def camelMatch(self, queries, pattern):

        up_cnt = 0
        for char in pattern:
            if 'A' <= char <= 'Z':
                up_cnt += 1

        trie = [{}, []]
        for index, query in enumerate(queries):
            tmp = 0
            for char in query:
                if 'A' <= char <='Z':
                    tmp += 1
            if tmp != up_cnt:
                continue

            now = trie
            for char in query:
                if char not in now[0]:
                    now[0][char] = [{}, [index]]
                else:
                    now[0][char][1].append(index)
                now = now[0][char]

        res = [False] * len(queries)

        self.dfs(trie, pattern, 0, res)
        return res
    
    def dfs(self, now, pattern, pos, res):
        if pos == len(pattern):
            for index in now[1]:
                res[index] = True
            return
        
        for next_char in now[0]:
            if next_char == pattern[pos]:
                self.dfs(now[0][next_char], pattern, pos + 1, res)
            elif 'a' <= next_char <= 'z':
                self.dfs(now[0][next_char], pattern, pos, res)
''',
    call="Solution().camelMatch(['FoB', 'Fa', 'FB'], 'FB')",
    expect=[True, False, True],
    views=[
        dict(type='text', fn=lambda S: '`queries = ' + str(S.get('queries', '')) + '`，`pattern = ' + repr(S.get('pattern', '')) + '`', size=26, h=60),
        dict(type='custom', draw=draw_trie, h=480),
        dict(type='calls', h=170, hide=('res',)),
    ],
    watch=[('up_cnt', 'up_cnt', 'pink'), ('pos', 'pos', 'yellow'), ('res', 'res', 'green')],
    captions={
        'up_cnt = 0': '`up_cnt` 统计 pattern 里的大写字母个数：大写字母只能匹配，不能跳过',
        'up_cnt += 1': '`up_cnt` → {up_cnt}',
        'trie = [{}, []]': 'trie 的节点是 `[子节点字典, 经过它的 query 下标列表]`',
        'for index, query': lambda S, B, r: ('所有 query 都处理完了，trie 建好' if B.get('index') == S.index else f'处理 `queries[{S.index}] = {S.query!r}`'),
        'tmp += 1': '`tmp` 数 query 的大写字母 → {tmp}',
        'if tmp != up_cnt': lambda S, B, r: (f'`tmp = {S.tmp}` ≠ `up_cnt = {S.up_cnt}` → 大写字母数量不同，必然匹配不上 → ==直接忽略==' if S.tmp != S.up_cnt
                                              else f'`tmp = {S.tmp}` == `up_cnt = {S.up_cnt}` → 可能匹配，插入 trie'),
        'continue': '这条 query 不进 trie，下一条',
        'now = trie': '从根节点开始插入',
        'if char not in now[0]': lambda S, B, r: (f'字母 `{S.char}` 还没有子节点 → 新建节点' if S.char not in S.now[0] else f'字母 `{S.char}` 已有节点 → 只追加下标'),
        'now[0][char] = [{}, [index]]': '新建节点，下标列表 `[{index}]`',
        '[1].append(index)': '该节点已存在，下标 `{index}` 追加进列表',
        'now = now[0][char]': '沿着 `{char}` 往下走一层',
        'res = [False]': '`res` 先全部置为 False，只有匹配上的才改成 True',
        'self.dfs(trie': '从 trie 根节点、pattern 下标 0 开始 dfs。小写字母可跳过，所以不能逐字符直接比对',
        'if pos == len(pattern)': lambda S, B, r: (f'`pos = {S.pos} == len(pattern)`：pattern 匹配完了 → 这个节点下的 query 都匹配上' if S.pos == len(S.pattern)
                                                    else f'`pos = {S.pos}` < {len(S.pattern)}，pattern 还没匹配完，继续往下走'),
        'for index in now[1]': '取节点列表里的下一个下标（取完则结束）：`index = {index}`',
        'res[index] = True': '`res[{index}] = True`',
        'return': '这一支完成，回到上一层',
        'for next_char in now[0]': lambda S, B, r: (f"取下一个子节点 `{S.next_char}`（没有了就返回上一层）" if 'next_char' in S else '枚举当前节点的所有子字母'),
        'if next_char == pattern[pos]': lambda S, B, r: (f"`{S.next_char}` == `pattern[{S.pos}] = {S.pattern[S.pos]}` → ==pattern 往前匹配一位==，进入这个子树，`pos + 1`" if S.next_char == S.pattern[S.pos]
                                                         else f"`{S.next_char}` ≠ `pattern[{S.pos}] = {S.pattern[S.pos]}`，不能当作匹配，看是不是小写"),
        'elif': lambda S, B, r: (f"`{S.next_char}` 是小写字母 → ==可以跳过==：进入子树，但 `pos` 不变" if 'a' <= S.next_char <= 'z'
                                 else f"`{S.next_char}` 是不匹配的大写字母 → 这一支走不通，不进入"),
        'self.dfs(now[0][next_char], pattern, pos + 1': '匹配上 `{next_char}`，进入子树，`pos` = {pos}',
        'self.dfs(now[0][next_char], pattern, pos, res)': '跳过小写 `{next_char}`，进入子树，`pos` 仍是 {pos}',
        'return res': '返回结果 `{res}`',
    },
    cards=dict(
        one_liner='大写字母数量先筛一遍，再在 Trie 上 DFS，小写字母可跳过',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['给 `queries` 和 `pattern`：可以在 pattern 的任意位置插入小写字母，得到 query 就算匹配',
                 '返回每个 query 是否匹配的布尔数组',
                 '视频示例：`["FoB","Fa","FB"]`，`pattern = "FB"` → `[True, False, True]`'],
        quote='若queries中字符串的大写字母数量与pattern中大写字母的数量不一致，那么这条query必然是无法匹配的，可以直接忽略掉。……这里不能直接一个个字符匹配，而需要执行dfs，因为trie树中的小写字母是可以被跳过的。',
        quote_src='—— yiduobo 题解原文',
        idea=['大写字母不能多也不能少，数量不同的 query 先排除',
              '剩下的 query 建 Trie，每个节点记下经过它的 query 下标',
              'DFS：子字母等于 `pattern[pos]` 就匹配并 `pos + 1`；小写字母可以跳过，`pos` 不变',
              '`pos` 走到 pattern 末尾，节点里的下标全部置 True'],
        summary=['时间、空间都是 `O(所有 query 的字符总数)`',
                 '大写字母既不能被跳过也不能多出来：数量筛选和 DFS 里只跳小写共同保证',
                 '示例里 `Fa` 只有 1 个大写字母，被数量筛选直接排除',
                 '对比灵神：灵神的题单把它归在同向双指针（子序列判断），这里用 Trie 一次批量匹配',
                 '原文为 Python 2 风格，本题无需改动，可直接在 Python 3 运行'],
    ),
    skip=[6, 7, 12, 13, 19],
    max_steps=110,
)
