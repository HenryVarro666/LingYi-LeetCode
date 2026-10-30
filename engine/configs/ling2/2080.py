ARR = [1, 2, 1, 1, 2, 2]
QUERIES = [(3, 5, 2), (1, 3, 1), (0, 5, 7)]


def _q(S):
    """当前查询 (left, right, value)"""
    if 'value' in S and 'left' in S:
        return S['left'], S['right'], S['value']
    return None


def _arr_color(S, k, v):
    q = _q(S)
    if q:
        l, r, val = q
        if v == val and l <= k <= r:
            return 'green'
        if v == val:
            return 'purple'
        return None
    if 'i' in S and k == S['i']:
        return 'yellow'
    return None


def _draw_a(cv, S, B, box, T):
    """下标列表 a 上的两次二分：p = 第一个 ≥ left，q = 第一个 > right（红蓝染色）"""
    x0, y0, x1, y1 = box
    q = _q(S)
    if not q or 'a' not in S:
        cv.text((x0 + 18, y0 + 4), 'query 时：在 value 的下标列表 a 上二分', 23, T['muted'], bold=True)
        return
    l, r, val = q
    a = S['a']
    p, qq = bisect_left(a, l), bisect_right(a, r)
    cv.text((x0 + 18, y0 + 4), f'a = pos[{val}]（有序！）：p = 第一个 ≥ {l}，q = 第一个 > {r}', 23, T['muted'], bold=True)
    cell = 96
    n = max(1, len(a))
    sx = x0 + (x1 - x0 - cell * (n + 1)) / 2
    y = y0 + 52
    if not a:
        cv.text((x0 + (x1 - x0) / 2, y + 40), f'{val} 没出现过：a = []，p = q = 0', 28, T['text'], anchor='mm', bold=True)
        return
    for k, v in enumerate(a):
        X = sx + k * cell
        inside = p <= k < qq
        fill = T['green'] if inside else T['panel2']
        cv.rect((X + 4, y, X + cell - 4, y + 70), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, y + 35), v, 32, T['bg'] if inside else T['text'], anchor='mm', mono=True, bold=True)
        cv.text((X + cell / 2, y + 82), k, 18, T['dim'], anchor='mt')
    for name, idx, c, dy in (('p', p, T['blue'], 0), ('q', qq, T['pink'], 28 if p == qq else 0)):
        X = sx + idx * cell + cell / 2
        cv.tri_up(X, y + 110, 9, c)
        cv.text((X, y + 122 + dy), f'{name}={idx}', 22, c, anchor='mt', bold=True)


CONFIG = dict(
    num=2080, title='区间内查询数字的频率', difficulty='Medium', category='二分查找',
    author='灵茶山艾府', technique='统计位置 + 二分查找',
    tags=['字节30天'],
    code='''
class RangeFreqQuery:
    def __init__(self, arr: List[int]):
        pos = defaultdict(list)
        for i, x in enumerate(arr):
            pos[x].append(i)
        self.pos = pos

    def query(self, left: int, right: int, value: int) -> int:
        a = self.pos[value]
        return bisect_right(a, right) - bisect_left(a, left)
''',
    call=f'''obj = RangeFreqQuery({ARR})
[obj.query(*q) for q in {QUERIES}]''',
    expect=[2, 2, 0],
    views=[
        dict(type='array', var=lambda S: ARR, label='arr（query 时：框 = [left, right]，绿 = 区间内的 value，紫 = 区间外的）', h=190, cell=90,
             pointers={'i': 'yellow'}, window=('left', 'right'), color=_arr_color),
        dict(type='map', var=lambda S: S.get('pos') or S.get('self.pos'), label='pos：数字 → 出现的下标列表', h=120,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='custom', draw=_draw_a, h=230),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('value', 'value', 'green')],
    captions={
        'pos = defaultdict(list)': '`pos[x]`：数字 `x` 在 `arr` 中的==所有出现位置==',
        'for i, x in enumerate(arr)': lambda S, B, ret: (f'`arr[{S.i}] = {S.x}`' if B.get('i') != S.i or 'i' not in B else '统计完毕'),
        'pos[x].append(i)': '`{x}` 出现在下标 `{i}`：`pos[{x}] = {pos[x]}`（从左到右追加，天然==有序==）',
        'self.pos = pos': '保存下来，之后每次 `query` 都用它',
        'a = self.pos[value]': lambda S, B, ret: (f'`query({S.left}, {S.right}, {S.value})`：`{S.value}` 的下标列表 `a = {S.a}`'
                                                  + ('' if S.a else '（没出现过，空列表）')),
        'return bisect_right': lambda S, B, ret: (f'`a` 中落在 `[{S.left}, {S.right}]` 的下标个数 = `q − p` = '
                                                  f'`{bisect_right(S.a, S.right)} − {bisect_left(S.a, S.left)}` = =={ret}=='),
    },
    cards=dict(
        one_liner='记下每个数的出现位置，查询变成在有序下标列表上二分',
        complexity='初始化 `O(n)`，每次 `query` `O(log n)`；空间 `O(n)`',
        problem=['设计 `RangeFreqQuery(arr)`：`query(left, right, value)` 返回 `value` 在 `arr[left..right]` 中出现几次',
                 '示例：`arr = [12,33,4,56,22,2,34,33,22,12,34,56]`',
                 '`query(1,2,4) = 1`，`query(0,11,33) = 2`',
                 '本视频：`arr = [1,2,1,1,2,2]`，查询 `(3,5,2)`、`(1,3,1)`、`(0,5,7)`'],
        quote='知道了下标，那么对于 query 来说，问题就变成了：下标列表中，==满足 left ≤ i ≤ right 的下标 i 的个数==。……由于 a 是有序数组，我们可以用二分查找快速求出。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`p`：`a` 中第一个 `≥ left` 的数的下标（`bisect_left`）',
              '`q`：`a` 中第一个 `> right` 的数的下标（`bisect_right`）',
              '`a[p..q-1]` 都满足要求，共 `q − p` 个；没有满足的也是 `0`，仍然正确'],
        result='三次查询返回 `[2, 2, 0]` ✓',
        summary=['初始化 `O(n)`，每次查询 `O(log n)`，空间 `O(n)`',
                 '下标按顺序追加，列表天然有序，不用再排序',
                 '`defaultdict` 查不存在的 `value` 会插入一个空列表，不影响答案',
                 '`bisect_right(a, right)` = `≤ right` 的个数；`bisect_left(a, left)` = `< left` 的个数',
                 '二分原理：红蓝染色法（基础算法精讲 04）'],
    ),
)
