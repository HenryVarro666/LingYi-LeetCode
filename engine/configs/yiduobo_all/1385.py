def _c1(S, i, v):
    if 'num' in S and 'p' in S and v == S['num']:
        return 'yellow'
    return None


def _top(S):
    if 'p' in S and 'num' in S:
        m, p, x = S['merged'], S['p'], S['num']
        if p < len(m):
            return f'`num = {x}`，`p = {p}` 指向合并区间 `[{m[p][0]}, {m[p][1]}]`'
        return f'`num = {x}`：`p = {p}` 已越过所有合并区间'
    if 'nowy' in S:
        return f"正在合并：当前大区间 ==[{S['nowx']}, {S['nowy']}]=="
    if S.get('intervals'):
        return '每个 `arr2[j]` 变成区间 `[arr2[j] − d, arr2[j] + d]`：落进区间的 arr1 元素不合格'
    return '先把 arr2 的每个数==转化为区间=='


def _if_merge(S, B, ret):
    x, y, ny = S.x, S.y, S.nowy
    if x <= ny:
        return f'`[{x}, {y}]` 的起点 `{x} ≤ {ny}`：和当前大区间==有重叠== → 合并'
    return f'`[{x}, {y}]` 的起点 `{x} > {ny}`：不相交 → 当前大区间 `[{S.nowx}, {ny}]` 定型'


def _while(S, B, ret):
    p, m, x = S.p, S.merged, S.num
    if p < len(m) and x > m[p][1]:
        return f'`{x} > {m[p][1]}`：num 在区间 `[{m[p][0]}, {m[p][1]}]` 右边 → 这个区间以后都用不上，`p` 右移'
    if p == len(m):
        return f'`p = {p}`：后面没有区间了'
    return f'`{x} ≤ {m[p][1]}`：`[{m[p][0]}, {m[p][1]}]` 是第一个右端点 ≥ num 的区间，停下'


def _if(S, B, ret):
    p, m, x = S.p, S.merged, S.num
    if p == len(m):
        return f'没有区间能盖住 `{x}` → ==符合距离要求=='
    if x < m[p][0]:
        return f'`{x} < {m[p][0]}`：num 落在两个区间的==空隙==里 → 符合距离要求'
    return f'`{m[p][0]} ≤ {x} ≤ {m[p][1]}`：被区间盖住 → 存在 `|num − arr2[j]| ≤ d`，不符合'


CONFIG = dict(
    num=1385, title='两个数组间的距离值', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='区间合并 + 双指针',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1235'],
    code='''
class Solution(object):
    def findTheDistanceValue(self, arr1, arr2, d):

        intervals = []
        for num in arr2:
            intervals.append([num - d, num + d])

        intervals = sorted(intervals, key=lambda d:d[0])
        merged = []
        nowx, nowy = intervals[0]
        for x, y in intervals[1:]:
            if x <= nowy:
                nowy = y
            else:
                merged.append([nowx, nowy])
                nowx, nowy = x, y

        merged.append([nowx, nowy])

        res = 0
        p = 0
        for num in sorted(arr1):
            while p < len(merged) and num > merged[p][1]:
                p += 1
            if p == len(merged) or num < merged[p][0]:
                res += 1

        return res
''',
    call='Solution().findTheDistanceValue([8,4,13,5], [10,9,1,8,0], 2)',
    expect=3,
    skip=['res = 0'],
    views=[
        dict(type='text', fn=_top, size=26, h=90),
        dict(type='intervals', var='intervals', out='merged',
             label='蓝 = arr2 生成的区间，绿 = 合并后的区间', h=380),
        dict(type='array', var=lambda S: sorted(S['arr1']), label='sorted(arr1)（黄 = 当前 num）',
             color=_c1, cell=90, h=170),
    ],
    watch=['d', ('nowx', 'nowx', 'cyan'), ('nowy', 'nowy', 'cyan'), ('p', 'p', 'blue'),
           ('num', lambda S: S['num'] if 'p' in S else None, 'yellow'), ('res', 'res', 'green')],
    captions={
        'intervals = []': '`intervals` 存放 arr2 转化出的区间',
        'for num in arr2': lambda S, B, r: ('arr2 转化完毕' if 'num' in B and B.num == S.num and len(S.intervals) == len(S.arr2)
                                            else f'`arr2` 中的 `{S.num}`'),
        'intervals.append': '`{num}` → 区间 `[{num} − {d}, {num} + {d}]` = `[{num - d}, {num + d}]`：落在里面的数离它 ==≤ d==',
        'intervals = sorted': '区间==按起点排序==：`{intervals}`',
        'merged = []': '`merged` 存放合并后互不相交的区间',
        'nowx, nowy = intervals[0]': '从第一个区间 `[{nowx}, {nowy}]` 开始合并',
        'for x, y in': lambda S, B, r: ('区间都看完了' if 'x' in B and (B.x, B.y) == (S.x, S.y)
                                        else f'下一个区间 `[{S.x}, {S.y}]`'),
        'if x <= nowy': _if_merge,
        'nowy = y': '右端点延伸到 `{nowy}`：大区间变成 `[{nowx}, {nowy}]`',
        15: '把定型的 `[{merged[-1][0]}, {merged[-1][1]}]` 放进 `merged`',
        18: '最后一个大区间也要放进去：`merged = {merged}`',
        'nowx, nowy = x, y': '以 `[{nowx}, {nowy}]` 开始新的大区间',
        'p = 0': '`res = 0` 计数；`p = 0` 指向第一个合并区间',
        'for num in sorted': lambda S, B, r: ('arr1 检测完毕' if 'num' in B and B.num == S.num and 'p' in B
                                              else f'按从小到大检测 `num = {S.num}`'),
        'while p < len': _while,
        'p += 1': '`p` → {p}',
        'if p == len': _if,
        'res += 1': '`res` → =={res}==',
        'return res': '距离值 = =={ret}==',
    },
    cards=dict(
        one_liner='把 arr2 的数变成区间并合并，再让排序后的 arr1 逐个检查是否落在区间里',
        complexity='时间 `O(n log n + m log m)`，空间 `O(m)`',
        problem=['对 `arr1` 中的元素 x，若 `arr2` 中==不存在== `|x − y| ≤ d` 的 y，就计数一次',
                 '返回计数（距离值）；示例：`[4,5,8], [10,9,1,8], d = 2` → `2`',
                 '本视频：`[8,4,13,5], [10,9,1,8,0], d = 2` → `3`'],
        quote='先将arr2中的元素转化为区间，然后将区间按起点排序，再将有重叠部分的区间合并成一个区间。这样一来，我们就得到了一些==单调递增，且互不相交的区间==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`arr2[j]` 对应「禁区」`[arr2[j] − d, arr2[j] + d]`，x 落进任何禁区就不合格',
              '禁区按起点排序后合并，得到有序且互不相交的区间',
              'arr1 排序后，指针 `p` 跟着往右走：两边都单调，一趟扫完'],
        summary=['时间瓶颈在排序 `O(n log n + m log m)`，空间 `O(m)` 存区间',
                 '合并时直接 `nowy = y`：所有区间长度都是 `2d`，起点有序则终点也有序，不必取 max',
                 '`while` 跳过右端点 `< num` 的区间；再看 num 是否 `< 起点`（落在空隙里）',
                 '对比灵神：灵神不建区间，直接让指针在排序后的 arr2 上找 `≥ x − d` 的最小数'],
    ),
)
