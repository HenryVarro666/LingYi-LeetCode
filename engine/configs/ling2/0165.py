import copy as _copy

V1, V2 = '1.01.3', '1.001.3.0.2'


def _left(it):
    try:
        return len(list(_copy.deepcopy(it)))
    except Exception:
        return None


def _index(S):
    """当前比较到第几个修订号：从 map 迭代器剩余的元素个数反推（zip_longest 每轮各取一个）"""
    if 'ver1' not in S or 'a' not in S:
        return None
    p1, p2 = S['version1'].split('.'), S['version2'].split('.')
    ra, rb = _left(S['a']), _left(S['b'])
    if ra is None or rb is None:
        return None
    return max(len(p1) - ra, len(p2) - rb) - 1


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '按 . 分割 → 转成整数 → 短的末尾补 0 → 从左到右比较', 24, T['muted'], bold=True)
    if 'version1' not in S:
        return
    p1, p2 = S['version1'].split('.'), S['version2'].split('.')
    n = max(len(p1), len(p2))
    k = _index(S)
    done = k is not None and S.get('_line') == 6 and S['ver1'] != S['ver2']
    cell = min(150, (x1 - x0 - 200) / n)
    sx = x0 + 170
    for r, (name, parts) in enumerate((('version1', p1), ('version2', p2))):
        Y = y0 + 80 + r * 190
        cv.text((x0 + 20, Y + 40), name, 24, T['text'], bold=True, mono=True)
        cv.text((x0 + 20, Y + 74), f"'{S[name]}'", 20, T['dim'], mono=True)
        for i in range(n):
            X = sx + i * cell
            miss = i >= len(parts)
            raw = '' if miss else parts[i]
            val = 0 if miss else int(parts[i])
            fill = T['panel2']
            if k is not None and i < k:
                fill = (40, 80, 55)
            if k is not None and i == k:
                fill = (110, 50, 50) if S['ver1'] != S['ver2'] else (70, 64, 30)
            if miss:
                cv.dashed((X + 6, Y + 10), (X + cell - 6, Y + 10), T['dim'], 2)
                cv.dashed((X + 6, Y + 110), (X + cell - 6, Y + 110), T['dim'], 2)
                cv.dashed((X + 6, Y + 10), (X + 6, Y + 110), T['dim'], 2)
                cv.dashed((X + cell - 6, Y + 10), (X + cell - 6, Y + 110), T['dim'], 2)
                if k is not None and i <= k:
                    cv.rect((X + 9, Y + 13, X + cell - 9, Y + 107), fill=fill, r=8)
                cv.text((X + cell / 2, Y + 40), '缺失', 22, T['dim'], anchor='mm', bold=True)
                cv.text((X + cell / 2, Y + 82), '补 0', 30, T['orange'], anchor='mm', bold=True, mono=True)
            else:
                cv.rect((X + 6, Y + 10, X + cell - 6, Y + 110), fill=fill, r=10,
                        outline=T['yellow'] if (k is not None and i == k) else T['border'], width=3 if (k is not None and i == k) else 1)
                cv.text((X + cell / 2, Y + 40), f"'{raw}'", 24, T['muted'], anchor='mm', mono=True)
                cv.text((X + cell / 2, Y + 82), val, 34, T['text'], anchor='mm', bold=True, mono=True)
            if r == 0:
                cv.text((X + cell / 2, Y - 6), f'第 {i} 个', 18, T['dim'], anchor='mb')
    if k is not None:
        X = sx + k * cell + cell / 2
        a, b = S['ver1'], S['ver2']
        op = '=' if a == b else ('<' if a < b else '>')
        c = T['green'] if a == b else T['red']
        cv.text((X, y0 + 80 + 150), op, 44, c, anchor='mm', bold=True, mono=True)


CONFIG = dict(
    num=165, title='比较版本号', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='split + map(int) + zip_longest 比较字典序',
    tags=['字节30天', '热题173'],
    code='''
class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        a = map(int, version1.split('.'))
        b = map(int, version2.split('.'))
        for ver1, ver2 in zip_longest(a, b, fillvalue=0):
            if ver1 != ver2:
                return -1 if ver1 < ver2 else 1
        return 0
''',
    call=f'Solution().compareVersion({V1!r}, {V2!r})',
    expect=-1,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', h=70, size=26, fn=lambda S: (
            f"列表 `a = {[int(x) for x in S['version1'].split('.')]}`，`b = {[int(x) for x in S['version2'].split('.')]}`：比较它们的==字典序=="
            if 'version1' in S else '')),
    ],
    watch=[('ver1', 'ver1', 'blue'), ('ver2', 'ver2', 'pink')],
    captions={
        'a = map(int, version1': "`version1.split('.')` = `{version1.split('.')}`，`int` 会==自动忽略前导零==（`'01'` → 1）",
        'b = map(int, version2': "`version2.split('.')` = `{version2.split('.')}`，同样转成整数",
        'for ver1, ver2 in zip_longest': lambda S, B, ret: (
            f'`zip_longest` 取出一对：`ver1 = {S.ver1}`，`ver2 = {S.ver2}`'
            + ('（version1 已经没有修订号了，==用 fillvalue=0 补==）' if 'ver1' in S and S.ver1 == 0 and _left(B.a) == 0 and _index(S) is not None and _index(S) >= len(S.version1.split('.')) else '')),
        'if ver1 != ver2': lambda S, B, ret: (f'`{S.ver1} == {S.ver2}`：这一位相同，==继续比下一位==' if S.ver1 == S.ver2
                                              else f'`{S.ver1} != {S.ver2}`：第一个不同的修订号，==由它决定大小=='),
        'return -1 if': lambda S, B, ret: f'`{S.ver1} < {S.ver2}` → version1 更小，返回 `{ret}`' if S.ver1 < S.ver2 else f'`{S.ver1} > {S.ver2}` → 返回 `{ret}`',
        'return 0': '所有修订号都相同，返回 `0`',
    },
    cards=dict(
        one_liner='按点分割转成整数列表，短的补 0，比较字典序',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['版本号由 `.` 分隔的修订号组成，修订号的值是==转成整数==后的值（忽略前导零）',
                 '从左到右比较修订号；某个版本修订号较少时，==缺失的视为 0==',
                 '`v1 < v2` 返回 `-1`，`v1 > v2` 返回 `1`，否则返回 `0`',
                 '示例：`"1.2"` vs `"1.10"` → `-1`；`"1.0"` vs `"1.0.0.0"` → `0`'],
        quote='把字符串按照 . 分割，分割出的子串转成整数，我们可以得到两个整数列表。……问题相当于比较这两个列表的字典序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`map(int, s.split(\'.\'))`：`int(\'001\') = 1`，前导零自动消失',
              '`zip_longest(a, b, fillvalue=0)`：短的那个==末尾补 0==，正好就是题目的规则',
              '找到第一个不同的位置就能返回；全部相同返回 0'],
        result='下标 4 处 `0 < 2` → 返回 `-1`：`"1.01.3" < "1.001.3.0.2"`',
        summary=['时间 `O(n + m)`，空间 `O(n + m)`（split 出的列表）',
                 '易错：修订号要按==整数==比较，`"10" > "2"`，不能按字符串比',
                 '易错：不要忘了补 0 的情况：`"1.0"` 和 `"1.0.0.0"` 相等',
                 '想要 `O(1)` 空间：双指针边扫边算每段的整数值'],
    ),
)
