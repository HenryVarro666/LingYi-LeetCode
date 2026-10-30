def _layout(node, depth, pos, out, ch=''):
    """列表节点 [children_dict, count]：叶子按顺序占列，父节点居中"""
    kids = list(node[0].items())
    if not kids:
        x = pos[0]
        pos[0] += 1
        out.append((id(node), ch, node, depth, x, None))
        return x
    xs = [_layout(c, depth + 1, pos, out, k) for k, c in kids]
    x = (xs[0] + xs[-1]) / 2
    out.append((id(node), ch, node, depth, x, [(id(c), k) for k, c in kids]))
    return x


def _trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    root = S.get('root')
    cv.text((x0 + 18, y0 + 4), '当前组的前缀树（节点里的数字 = 经过该节点的单词数，黄 = 当前位置）', 22, T['muted'], bold=True)
    if not (isinstance(root, list) and len(root) == 2 and isinstance(root[0], dict)):
        cv.text((x0 + 18, y0 + 60), '（这一组只有 1 个单词，或还没建树）', 24, T['dim'])
        return
    out = []
    pos = [0]
    _layout(root, 0, pos, out)
    maxd = max(o[3] for o in out)
    cols = max(pos[0], 1)
    gx = min(150, (x1 - x0 - 120) / cols)
    gy = min(70, (y1 - y0 - 110) / max(maxd, 1))
    P = {o[0]: (x0 + 70 + o[4] * gx + (x1 - x0 - 140 - gx * (cols - 1)) / 2, y0 + 70 + o[3] * gy) for o in out}
    cur = S.get('now')
    for nid, ch, node, d, x, kids in out:
        for cid, k in (kids or []):
            a, b = P[nid], P[cid]
            cv.line([(a[0], a[1] + 18), (b[0], b[1] - 18)], T['muted'], 2)
            cv.text(((a[0] + b[0]) / 2 + 12, (a[1] + b[1]) / 2), k, 22, T['cyan'], anchor='mm', bold=True, mono=True)
    for nid, ch, node, d, x, kids in out:
        X, Y = P[nid]
        on = node is cur
        cv.rect((X - 18, Y - 18, X + 18, Y + 18), fill=T['yellow'] if on else T['panel2'],
                outline=T['yellow'] if on else T['border'], width=2, r=18)
        cv.text((X, Y), 'root' if d == 0 else node[1], 18 if d == 0 else 22, T['bg'] if on else T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=527, title='单词缩写', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='分组 + 前缀树',
    tags=['前缀树'],
    code='''
class Solution(object):
    def wordsAbbreviation(self, words):

        res = words[:]

        word_dict = {}
        for index in range(len(words)):
            word = words[index]
            key = (word[0], word[-1], len(word))
            if key not in word_dict:
                word_dict[key] = []
            word_dict[key].append(index)

        for group in word_dict.values():
            if len(group) == 1:
                word = words[group[0]]
                abbr = word[0] + str(len(word) - 2) + word[-1]
                if len(abbr) < len(word):
                    res[group[0]] = abbr
                continue
                
            root = [{}, 0]
            for index in group:
                word = words[index]
                now = root
                n = len(word)
                for p in range(1, n - 1):
                    char = word[p]
                    if char not in now[0]:
                        now[0][char] = [{}, 0]
                    now = now[0][char]
                    now[1] += 1
            
            for index in group:
                word = words[index]
                now = root
                n = len(word)
                abbr = None
                for p in range(1, n - 1):
                    char = word[p]
                    now = now[0][char]
                    if now[1] == 1:
                        abbr = word[:p + 1] + str(len(word) - p - 2) + word[-1]
                        break

                if abbr is not None and len(abbr) < len(word):
                    res[index] = abbr

        return res
''',
    call="Solution().wordsAbbreviation(['like','god','abcdef','abxdef'])",
    expect=['l2e', 'god', 'abc2f', 'abx2f'],
    views=[
        dict(type='map', var='word_dict', label='word_dict：(首, 尾, 长度) → 下标列表', fmt=lambda k, v: f'{k[0]}…{k[1]} 长{k[2]} → {v}', font=22, h=120),
        dict(type='custom', draw=_trie, h=380),
        dict(type='array', var='res', label='res（答案）', cell=110, h=165,
             color=lambda S, i, v: 'green' if v != S['words'][i] else None),
    ],
    watch=['index', 'word', 'p', 'char', ('abbr', 'abbr', 'green')],
    skip=['word_dict[key] = []', 'break', 'abbr = None', 'continue', 'res = words[:]', 'n = len(word)', 'char = word[p]', 'if char not in now[0]', 'if key not in word_dict', 'n = len(word)', 'word = words[index]', 'word = words[group[0]]'],
    max_steps=130,
    captions={
        'key = (': '分组依据：`(首字母, 尾字母, 长度)` = `{key}`。==只有这三样都相同的单词才可能缩写冲突==',
        'word_dict[key].append': '`{word}` 的下标 {index} 放进组 `{key}`',
        'for group in': '逐组处理：本组下标 `{group}`',
        'if len(group) == 1': '组里有 `{len(group)}` 个单词：' + '{"只有一个 → 不可能冲突，直接用最短缩写" if len(group) == 1 else "不止一个 → 可能冲突，要建前缀树"}',
        'abbr = word[0] + str(len(word) - 2)': '孤零零的单词：首字母 + 中间长度 + 尾字母 = `{abbr}`',
        'if len(abbr) < len(word)': '缩写 `{abbr}`（{len(abbr)}）要比原词（{len(word)}）更短才算数 → {"成立" if len(abbr) < len(word) else "不成立，保持原词"}',
        'root = [{}, 0]': '新建这一组的前缀树：节点 = [孩子字典, 经过次数]',
        'now = root': '从根出发',
        'now[0][char] = [{}, 0]': '`{char}` 还没有这条边 → 新建节点',
        'now = now[0][char]': '沿 `{char}` 往下走一格',
        'now[1] += 1': '==经过次数 +1==：现在有 `{now[1]}` 个单词共用这个前缀',
        'if now[1] == 1': '次数 = `{now[1]}`' + '：' + '{"只有自己走过 → 这就是唯一的最短前缀" if now[1] == 1 else "还有别的单词共用 → 继续往下"}',
        'abbr = word[:p + 1]': '前缀 `{word[:p+1]}` + 省略 `{len(word)-p-2}` 个 + 尾字母 = ==`{abbr}`==',
        'break': '找到最短唯一前缀，不用再往下',
        'res[index] = abbr': '`res[{index}] = {abbr}`',
        'return res': '全部缩写完成：`{res}`',
    },
    cards=dict(
        one_liner='先按「首尾字母 + 长度」分组，组内用前缀树找最短唯一前缀',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['给一组不同的单词，给每个单词一个最短缩写：首字母 + 省略个数 + 尾字母',
                 '若多个单词缩写相同，就==延长前缀==直到各不相同；缩写不比原词短就保留原词',
                 '本视频：`[like, god, abcdef, abxdef]`'],
        quote='只有长度相同，且首尾字符相同的单词才可能出现冲突，因此可以使用这三个元素做key，在一开始就使用哈希表将所有单词分组。',
        quote_src='—— yiduobo 题解原文',
        idea=['缩写 = 前缀 + 省略数 + 尾字母；同组的长度和尾字母一样，唯一性只取决于==前缀==',
              '第一遍把组内单词插入前缀树，每个节点记经过次数 `now[1]`',
              '第二遍沿路径走，第一个次数为 1 的节点，对应的前缀就是最短唯一前缀'],
        summary=['时间 `O(总字符数)`，空间同阶；不同组互不干扰',
                 '循环范围是 `range(1, n-1)`：首尾字母不进树，只考察中间字符',
                 '易错：缩写长度不短于原词时==必须保留原词==（`len(abbr) < len(word)`）',
                 '原文为 Python 2 风格，本题代码无需改动，可直接用 Python 3 运行'],
    ),
)
