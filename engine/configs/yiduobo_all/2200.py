NUMS, KEY, KK = [9, 2, 9, 4, 1, 6, 9, 5], 9, 1


def _color(S, i, v):
    if i in (S.get('res') or []):
        return 'green'
    if v == S['key']:
        return 'yellow'
    return None


def _ivs(S):
    iv = S.get('intervals')
    if not iv:
        return '`intervals`：每个 key 下标 `index` 影响的区间 `[index−k, index+k]`（截到数组边界）'
    parts = []
    cur = (S.get('x'), S.get('y')) if S['_line'] in (15, 16, 17, 18, 19, 20) else None
    for a, b in iv:
        s = f'[{a},{b}]'
        parts.append(f'=={s}==' if cur and (a, b) == cur else f'`{s}`')
    return 'intervals：' + ' '.join(parts)


def _cur(S):
    if 'nowx' not in S:
        return ''
    return f"正在合并的区间 `[nowx, nowy] = [{S['nowx']}, {S['nowy']}]`（框）"


CONFIG = dict(
    num=2200, title='找出数组中的所有 K 近邻下标', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='key 的影响区间 · 区间合并',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def findKDistantIndices(self, nums, key, k):

        n = len(nums)
        intervals = []
        for index, num in enumerate(nums):
            if num == key:
                intervals.append([max(0, index - k), min(n - 1, index + k)])

        if not intervals:
            return []

        res = []
        nowx, nowy = intervals[0]
        for x, y in intervals[1:]:
            if nowy >= x:
                nowy = y
            else:
                res.extend(range(nowx, nowy + 1))
                nowx, nowy = x, y

        res.extend(range(nowx, nowy + 1))
        return res
''',
    call=f'Solution().findKDistantIndices({NUMS}, {KEY}, {KK})',
    expect=[0, 1, 2, 3, 5, 6, 7],
    views=[
        dict(type='array', var='nums', label=f'nums（key = {KEY}，k = {KK}；黄 = key，绿 = 已加入 res）', h=250,
             pointers={'index': 'blue'}, window=('nowx', 'nowy'), color=_color),
        dict(type='text', h=80, size=28, fn=_ivs),
        dict(type='text', h=70, size=26, fn=_cur),
        dict(type='array', var='res', label='res', h=170, color=lambda S, i, v: 'green'),
    ],
    watch=[('index', 'index', 'blue'), ('x', 'x'), ('y', 'y'), ('nowx', 'nowx', 'cyan'), ('nowy', 'nowy', 'cyan')],
    captions={
        'n = len(nums)': '`n = {n}`，区间不能越过 `0` 和 `n − 1 = {n - 1}`',
        'intervals = []': '反过来想：每个 key 能影响哪些下标？',
        'for index, num in': lambda S, B, r: ('第一趟扫描结束' if B.get('index') == S.index else f'`nums[{S.index}] = {S.num}`'),
        'if num == key': lambda S, B, r: (f'`{S.num} == key`：它影响 `[{S.index}−{S.k}, {S.index}+{S.k}]`' if S.num == S.key
                                          else f'`{S.num} ≠ key`，不影响任何下标'),
        'intervals.append': '加入区间 `[max(0, {index - k}), min({n - 1}, {index + k})]` = `{intervals[-1]}`',
        'if not intervals': '有 key 存在，区间不为空',
        'res = []': '这些区间==天然按左端点排好序==，一趟遍历就能合并',
        'nowx, nowy = intervals[0]': '当前区间先取第一个：`[{nowx}, {nowy}]`',
        'for x, y in': lambda S, B, r: ('区间遍历结束' if (B.get('x'), B.get('y')) == (S.x, S.y) and 'x' in B
                                        else f'看下一个区间 `[{S.x}, {S.y}]`'),
        'if nowy >= x': lambda S, B, r: (f'`nowy = {S.nowy} ≥ x = {S.x}`：两个区间==有重叠==，可以合并' if S.nowy >= S.x
                                         else f'`nowy = {S.nowy} < x = {S.x}`：==不相交==，当前区间结束'),
        'nowy = y': '右端点延长到 `{nowy}`，当前区间变成 `[{nowx}, {nowy}]`',
        19: '把 `[{nowx}, {nowy}]` 的下标全部加入 `res` → `{res}`',
        'nowx, nowy = x, y': '当前区间换成新的 `[{nowx}, {nowy}]`',
        22: '最后一个区间还没加：`[{nowx}, {nowy}]` → `res = {res}`',
        'return res': '返回 `{res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='每个 key 影响一段区间，把区间合并起来就是答案',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找出所有下标 `i`：存在 `j` 满足 `|i − j| ≤ k` 且 `nums[j] == key`，按递增返回',
                 '示例：`nums = [3,4,9,1,3,9,5], key = 9, k = 1` → `[1,2,3,4,5,6]`',
                 '本视频：`nums = [9,2,9,4,1,6,9,5], key = 9, k = 1` → `[0,1,2,3,5,6,7]`'],
        quote='不妨反过来思考，对于nums中所有值等于key的数影响到的范围是哪些，然后将这些范围合并起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：每个 key 的下标 `index` 产生区间 `[index−k, index+k]`，==截到数组边界==',
              '区间已按左端点有序 → 一趟遍历，`nowy ≥ x` 就合并',
              '不相交时把当前区间的下标全部加入 `res`'],
        summary=['时间 `O(n)`：区间个数 ≤ n，每个下标只加入一次',
                 '易错：循环结束后==最后一个区间==还要再加一次',
                 '易错：区间左右端点要和 `0`、`n − 1` 取 max / min',
                 '原文的 Python 2 风格代码可直接在 Python 3 运行，未做改动',
                 '对比灵神：灵神用指针 `j` 边走边加，不需要存区间'],
    ),
)
