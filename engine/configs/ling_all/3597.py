CONFIG = dict(
    num=3597, title='分割字符串', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='字典树（嵌套字典）',
    tags=[],
    code='''
class Solution:
    def partitionString(self, s: str) -> List[str]:
        ans = []
        cur = root = {}
        left = 0
        for i, c in enumerate(s):
            if c not in cur:  # 无路可走？
                cur[c] = {}  # 那就造路！
                ans.append(s[left: i + 1])
                left = i + 1
                cur = root  # 重置
            else:
                cur = cur[c]
        return ans
''',
    call='Solution().partitionString("abbccccd")',
    expect=["a", "b", "bc", "c", "cc", "d"],
    views=[
        dict(type='string', var='s', pointers={'left': 'blue', 'i': 'pink'}, window=('left', 'i'), h=190,
             label='s（蓝 = 当前段起点 left，粉 = 正在看的字符 i）'),
        dict(type='custom', h=270, draw=lambda cv, S, B, box, T: _trie(cv, S, B, box, T)),
        dict(type='text', h=70, fn=lambda S: '已分出的段：' + ' , '.join(f'`{x}`' for x in S.get('ans', [])) if S.get('ans') else '已分出的段：（空）'),
    ],
    watch=[('left', 'left', 'blue'), ('i', 'i', 'pink'), ('c', 'c', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'cur = root = {}': '`root` 是字典树的根：一个空字典。`cur` 表示当前走到的节点',
        'left = 0': '`left` 是当前段的起点',
        'for i, c': lambda S, B, r: ('字符都看完了，循环结束' if B.get('i') == S.i and B.get('c') == S.c and S.i == len(S.s) - 1 else f'看第 `{S.i}` 个字符 `{S.c}`'),
        'if c not in cur': lambda S, B, r: (
            f'`{S.c}` 在当前节点的孩子里吗？' + ('==不在==：无路可走，说明当前段是新串' if S.c not in S.cur else '在：这条路以前走过，当前段还是旧串，继续扩展')),
        'cur[c] = {}': '造路：给当前节点加孩子 `{c}`，这个段从此"出现过"',
        'ans.append': '当前段 `s[{left}:{i + 1}]` = =={ans[-1]}== 是新的，加入答案',
        'left = i + 1': '下一段从 `{left}` 开始',
        'cur = root': '回到根，从头开始匹配新段',
        'cur = cur[c]': '沿着已有的路往下走一格，段还要继续变长',
        'return ans': '返回所有段：`{ret}`',
    },
    cards=dict(
        one_liner='段是否出现过 = 字典树里有没有路，没路就造一条',
        complexity='时间 `O(n)`（哈希表实现），空间 `O(n)`',
        problem=['按规则分割 `s`：从当前位置逐字符扩展，直到这个段之前没出现过，就切出来',
                 '返回所有段，例如 `"aaaa"` → `["a", "aa"]`',
                 '本视频：`"abbccccd"` → `["a","b","bc","c","cc","d"]`'],
        quote='if c not in cur:  # 无路可走？\n    cur[c] = {}  # 那就造路！',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['用嵌套字典当字典树：每个节点是 `{字符: 子节点}`',
              '走得通 → 当前段还是以前出现过的前缀，继续扩展',
              '走不通 → 当前段是新的：造路、记下答案、回到根开始下一段'],
        summary=['时间 `O(n)`，空间 `O(n)`；方法一用哈希集合存段，字符串比较使总时间为 `O(n√n)`',
                 '字典树的路径正好是"段的所有前缀"：新段 = 旧段多一个字符，所以只会多造一格',
                 '易错：造路后要 `cur = root` 重置，且 `left = i + 1`',
                 '同类题：208. 实现 Trie'],
    ),
)


def _trie(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '字典树 root（黄 = 当前所在节点 cur）', 24, T['muted'], bold=True)
    root = S.get('root')
    if root is None:
        return
    cur = S.get('cur')
    # 布局：叶子数决定宽度
    def leaves(n):
        return max(1, sum(leaves(c) for c in n.values())) if n else 1
    total = leaves(root)
    W = x1 - x0 - 60
    unit = min(120, W / total)
    pos = {}
    def place(n, lo, depth, label):
        w = leaves(n) * unit
        x = x0 + 30 + lo + w / 2
        y = y0 + 120 + depth * 70
        pos[id(n)] = (x, y)
        off = lo
        for ch, c in n.items():
            cw = leaves(c) * unit
            place(c, off, depth + 1, ch)
            off += cw
    place(root, 0, 0, '')
    def draw(n, label):
        x, y = pos[id(n)]
        off = None
        for ch, c in n.items():
            cx, cy = pos[id(c)]
            cv.line([(x, y), (cx, cy)], T['muted'], 2)
            cv.text(((x + cx) / 2 + 10, (y + cy) / 2), ch, 22, T['cyan'], anchor='lm', bold=True)
            draw(c, ch)
    draw(root, '')
    for k, (x, y) in [(None, pos[id(root)])]:
        pass
    for n_id, (x, y) in pos.items():
        is_cur = cur is not None and id(cur) == n_id
        cv.rect((x - 16, y - 16, x + 16, y + 16), fill=T['yellow'] if is_cur else T['border'], r=16,
                outline=T['yellow'] if is_cur else T['muted'], width=2)
    cv.text((pos[id(root)][0] - 30, pos[id(root)][1]), 'root', 20, T['dim'], anchor='rm')
