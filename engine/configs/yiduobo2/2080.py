ARR = [3, 1, 3, 2, 3]
QUERIES = [(1, 4, 3), (0, 2, 2)]


def _pos_list(S):
    d = S.get('self.num_dict')
    v = S.get('value')
    if d is None or v is None or v not in d:
        return None
    return d[v]


def _draw_bs(cv, S, B, box, T):
    """在 value 的位置列表上二分：找 ≤ pos 的最后一个"""
    x0, y0, x1, y1 = box
    a = _pos_list(S)
    if 'pos' not in S or 'value' not in S:
        cv.text((x0 + 18, y0 + 4), 'binary_search(value, pos)：位置列表中 ≤ pos 的数有几个', 23, T['muted'], bold=True)
        return
    pos, v = S['pos'], S['value']
    cv.text((x0 + 18, y0 + 4), f'num_dict[{v}] 中 ≤ pos = {pos} 的有几个？（青 = 已确定 ≤ pos）', 23, T['muted'], bold=True)
    if a is None:
        cv.text((x0 + 30, y0 + 70), f'{v} 没出现过 → 0', 28, T['text'], bold=True)
        return
    cell = 100
    sx = x0 + (x1 - x0 - cell * len(a)) / 2
    y = y0 + 50
    l, r, mid = S.get('l'), S.get('r'), S.get('mid')
    for k, p in enumerate(a):
        X = sx + k * cell
        fill = T['panel2']
        if isinstance(l, int) and k <= l and a[k] <= pos:
            fill = (24, 110, 104)
        if isinstance(l, int) and isinstance(r, int) and not (l <= k <= r):
            fill = (40, 45, 53) if fill == T['panel2'] else fill
        cv.rect((X + 4, y, X + cell - 4, y + 70), fill=fill, r=10,
                outline=T['yellow'] if k == mid and S['_line'] in (20, 21, 22, 23, 24) else T['border'],
                width=4 if k == mid and S['_line'] in (20, 21, 22, 23, 24) else 1)
        cv.text((X + cell / 2, y + 35), p, 32, T['text'], anchor='mm', mono=True, bold=True)
        cv.text((X + cell / 2, y + 82), k, 18, T['dim'], anchor='mt')
    marks = []
    if isinstance(l, int):
        marks.append(('l', l, T['blue']))
    if isinstance(r, int):
        marks.append(('r', r, T['pink']))
    if isinstance(mid, int) and S['_line'] in (20, 21, 22, 23, 24):
        marks.append(('mid', mid, T['yellow']))
    seen = {}
    for name, idx, c in marks:
        row = seen.get(idx, 0)
        seen[idx] = row + 1
        X = sx + idx * cell + cell / 2
        cv.tri_up(X, y + 108, 9, c)
        cv.text((X, y + 128 + row * 26), f'{name}={idx}', 21, c, anchor='mt', bold=True)


def _arr_color(S, k, v):
    if 'value' in S and v == S['value']:
        if 'pos' in S and k <= S['pos']:
            return 'cyan'
        return 'purple'
    if 'index' in S and 'value' not in S and k == S['index']:
        return 'yellow'
    return None


_st = {'n': 0}   # 第几次执行"for num in self.num_dict"（字幕按步骤顺序各求值一次）


def _sort_for(S, B, ret):
    _st['n'] += 1
    if _st['n'] <= len(set(ARR)):
        return f'把 `{S.num}` 的位置从小到大排序'
    return '排序完毕'


def _early(S, B, ret):
    v, pos, d = S.value, S.pos, S['self.num_dict']
    if v not in d:
        return f'`{v}` 没出现过 → 返回 0'
    if pos < d[v][0]:
        return f'`pos = {pos}` < 最小位置 `{d[v][0]}`：`[0, {pos}]` 里一个 `{v}` 都没有 → 返回 0'
    return f'`pos = {pos}` ≥ 最小位置 `{d[v][0]}`，二分找 ≤ pos 的最后一个'


def _while(S, B, ret):
    if B.l < B.r:
        return f'`l = {B.l} < r = {B.r}`：继续二分'
    return f'`l = r = {B.l}`：`num_dict[{S.value}][{B.l}]` 就是 ≤ pos 的最后一个'


def _ifmid(S, B, ret):
    a = S['self.num_dict'][S.value]
    m = S.mid
    if a[m] <= S.pos:
        return f'`num_dict[{S.value}][{m}] = {a[m]}` ≤ `{S.pos}` → 答案在 `mid` 或右边'
    return f'`num_dict[{S.value}][{m}] = {a[m]}` > `{S.pos}` → 答案在 `mid` 左边'


CONFIG = dict(
    num=2080, title='区间内查询数字的频率', difficulty='Medium', category='二分查找',
    author='yiduobo', technique='前缀相减 + 位置列表二分',
    tags=['字节30天'],
    code='''
class RangeFreqQuery(object):

    def __init__(self, arr):
        self.num_dict = {}
        for index, num in enumerate(arr):
            if num not in self.num_dict:
                self.num_dict[num] = []
            self.num_dict[num].append(index)

        for num in self.num_dict:
            self.num_dict[num] = sorted(self.num_dict[num])

    def binary_search(self, value, pos):
        if value not in self.num_dict or pos < self.num_dict[value][0]:
            return 0

        l = 0
        r = len(self.num_dict[value]) - 1
        while l < r:
            mid = (l + r + 1) >> 1
            if self.num_dict[value][mid] <= pos:
                l = mid
            else:
                r = mid - 1

        return l + 1

    def query(self, left, right, value):

        return self.binary_search(value, right) - self.binary_search(value, left - 1)
''',
    call=f'''obj = RangeFreqQuery({ARR})
[obj.query(*q) for q in {QUERIES}]''',
    expect=[2, 0],
    skip=['self.num_dict = {}', 'if num not in self.num_dict'],
    views=[
        dict(type='array', var=lambda S: ARR, label='arr（青 = [0, pos] 内的 value，紫 = pos 右边的 value）', h=170, cell=90,
             pointers={'index': 'yellow', 'pos': 'pink'}, color=_arr_color),
        dict(type='map', var=lambda S: S.get('self.num_dict'), label='num_dict：数字 → 出现的所有位置', h=110,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='custom', draw=_draw_bs, h=220),
        dict(type='calls', h=100),
    ],
    watch=[('left', 'left'), ('right', 'right'), ('value', 'value', 'green'), ('pos', 'pos', 'pink'),
           ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow')],
    captions={
        'for index, num in enumerate(arr)': lambda S, B, ret: (f'`arr[{S.index}] = {S.num}`' if B.get('index') != S.index or 'index' not in B
                                                               else '位置记录完毕'),
        'self.num_dict[num] = []': '`{num}` 第一次出现，建一个空列表',
        'self.num_dict[num].append(index)': '记录 `{num}` 出现在位置 `{index}`',
        'for num in self.num_dict': _sort_for,
        'self.num_dict[num] = sorted': '`num_dict[{num}] = {self.num_dict[num]}`',
        'return self.binary_search(value, right)': lambda S, B, ret: (
            f'`query({B.left}, {B.right}, {B.value})` = `[0, {B.right}]` 中的个数 − `[0, {B.left - 1}]` 中的个数' if ret is None
            else f'`query({S.left}, {S.right}, {S.value})` = =={ret}=='),
        'if value not in self.num_dict or': _early,
        'return 0': '返回 `0`',
        'l = 0': '在 `num_dict[{value}]` 上二分：找==最后一个 ≤ pos== 的位置',
        'r = len(self.num_dict[value]) - 1': '`r = {r}`（闭区间 `[l, r]`）',
        'while l < r': _while,
        'mid = (l + r + 1) >> 1': '`mid = (l + r + 1) >> 1 = {mid}`（==上取整==，防止 `l = mid` 死循环）',
        'if self.num_dict[value][mid] <= pos': _ifmid,
        'l = mid': '`l` → {l}',
        'r = mid - 1': '`r` → {r}',
        'return l + 1': '下标 `0..{l}` 都 ≤ pos → 有 `{ret}` 个',
    },
    max_steps=70,
    cards=dict(
        one_liner='区间转前缀：[0, r] 的个数减 [0, l−1] 的个数，各用一次二分',
        complexity='初始化 `O(n log n)`（含排序），每次 `query` `O(log n)`；空间 `O(n)`',
        problem=['设计 `RangeFreqQuery(arr)`：`query(left, right, value)` 返回 `value` 在 `arr[left..right]` 中出现几次',
                 '示例：`arr = [12,33,4,56,22,2,34,33,22,12,34,56]`，`query(1,2,4) = 1`，`query(0,11,33) = 2`',
                 '本视频：`arr = [3,1,3,2,3]`，查询 `(1,4,3) → 2`、`(0,2,2) → 0`'],
        quote='一个自然的想法就是==将区间问题转化为前缀问题==……num_dict[value]中小于等于r的数有多少个，区间[0, r]中value的数量就有多少个。',
        quote_src='—— yiduobo 题解原文',
        idea=['`query(l, r, v)` = `[0, r]` 中 v 的个数 − `[0, l−1]` 中 v 的个数',
              'value 范围太大，不能给每个前缀都存计数 → 折中：只记每个数出现的位置',
              '`[0, pos]` 中 v 的个数 = 位置列表里 `≤ pos` 的个数 → 二分'],
        result='两次查询返回 `[2, 0]` ✓',
        summary=['每次查询两次二分 `O(log n)`',
                 '二分找"最后一个 ≤ pos"：`mid` 要上取整 `(l + r + 1) >> 1`',
                 '`pos` 比最小位置还小时提前返回 0（包括 `left − 1 = −1`）',
                 '原文为 Python 2 风格，删去了文档字符串和 LeetCode 模板注释；位置本就有序，`sorted` 只是保险',
                 '对比灵神：灵神直接 `bisect_right(a, right) - bisect_left(a, left)`'],
    ),
)
