def _xi(S):
    """当前 x 在 s 中的下标（pairwise 没有下标，用 vis 的大小推出来：vis 里每个子串对应一次循环）"""
    if 'x' not in S:
        return None
    n = len(S['vis'])
    return n if S['_line'] == 4 else n - 1


def _color(S, i, v):
    k = _xi(S)
    if k is None or S['_line'] == 7:
        return None
    if i == k:
        return 'blue'
    if i == k + 1:
        return 'pink'
    return None


def _txt(S):
    if 'x' not in S or S['_line'] < 5:
        return '`vis` 记录遇到过的长为 2 的子串'
    x, y = S['x'], S['y']
    return f"当前子串 `{x}{y}`；它在反转串里出现 ⇔ `{y}{x}` 在 s 中出现过"


CONFIG = dict(
    num=3083, title='字符串及其反转中是否存在同一子字符串', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='哈希集合 · 边遍历边查反向子串',
    tags=[],
    code='''
class Solution:
    def isSubstringPresent(self, s: str) -> bool:
        vis = set()
        for x, y in pairwise(s):
            vis.add(x + y)
            if y + x in vis:
                return True
        return False
''',
    call="Solution().isSubstringPresent('abcdefgdc')",
    expect=True,
    views=[
        dict(type='string', var='s', h=200, cell=70, color=_color),
        dict(type='text', h=100, size=40, fn=_txt),
        dict(type='set', var='vis', h=240, label='vis'),
    ],
    watch=['x', 'y', ('vis', 'sorted(vis)', 'blue')],
    captions={
        'vis = set': '`vis` 用来存已经遇到过的长为 2 的子串',
        'for x, y in pairwise': '相邻两个字符：`x = {x}`，`y = {y}`，子串是 `{x+y}`',
        'vis.add': '把 `{x+y}` 记进集合：`vis = {sorted(vis)}`',
        'if y + x in vis': '反转串里有 `{x+y}` ⇔ `s` 里有反过来的 `{y+x}`。`{y+x}` 在 `vis` 里吗？→ {"==在，找到了==" if (y+x in vis) else "不在"}',
        'return True': '`{y+x}` 早就出现过，而 `{x+y}` 刚出现 → ==反转后同一个子串==，返回 True',
        'return False': '所有子串都没有反向版本，返回 False',
    },
    cards=dict(
        one_liner='x+y 在反转串里 ⇔ y+x 在原串里',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`（至多 26×26 个子串）',
        problem=['判断 `s` 是否有一个长为 2 的子串，在 `s` 反转后的字符串里也出现',
                 '示例：`leetcode` → `True`（`ee`），`abcd` → `False`',
                 '本例演示：`abcdefgdc`，`cd` 与 `dc` 互为反向'],
        quote='核心思路：x+y 在反转串 reverse(s) 中，等价于 y+x 在 s 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不用真的反转：只需判断「反过来的子串」有没有出现过',
              '边遍历边记录 `x+y`；若 `y+x` 已在集合里，立刻返回',
              '一次遍历就够：两个互为反向的子串，后出现的那个会命中前面的'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '==回文式的两个相同字母（如 `ee`）==：`y+x == x+y`，先加入再判断，所以也能命中',
                 '==先 add 再判断==，顺序不能反',
                 '题解还给了位运算写法：`vis[x]` 用二进制数压缩第二维，思路相同']),
)
