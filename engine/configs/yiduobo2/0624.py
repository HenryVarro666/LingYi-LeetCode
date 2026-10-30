ARR = [[3, 5], [1, 4, 9], [2, 6], [4, 7]]


def _cur(S):
    a = S.get('arr')
    if a is None:
        return 0 if 'mi' in S else -1
    return ARR.index(a) if a in ARR else -1


def _color(S, i, j, v):
    c = _cur(S)
    row = S['arrays'][i]
    if c < 0:
        return None
    if i == c and c > 0:
        if j == 0:
            return 'cyan'
        if j == len(row) - 1:
            return 'orange'
        return None
    if i < c or (i == 0 and c == 0):
        upto = max(c, 1)
        firsts = [ARR[k][0] for k in range(upto)]
        lasts = [ARR[k][-1] for k in range(upto)]
        if j == 0 and v == min(firsts) and firsts.index(v) == i:
            return 'blue'
        if j == len(row) - 1 and v == max(lasts) and lasts.index(v) == i:
            return 'pink'
    return None


def _formula(S, B):
    if S.get('_line') == 8 and 'arr' in S:
        a = S['arr']
        r = B['res']
        rs = '-∞' if r == float('-inf') else str(r)
        return (f"`res = max({rs}, {a[-1]} − {B['mi']}, {B['ma']} − {a[0]})` = =={S['res']}==")
    return '最大距离 = ==某个数组的最大值 − 另一个数组的最小值=='


CONFIG = dict(
    num=624, title='数组列表中的最大距离', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='一趟遍历 · 维护已遍历数组的最小值和最大值',
    tags=['字节30天'],
    code='''
class Solution(object):
    def maxDistance(self, arrays):
        res = float('-inf')
        mi = arrays[0][0]
        ma = arrays[0][-1]

        for arr in arrays[1:]:
            res = max(res, arr[-1] - mi, ma - arr[0])
            mi = min(mi, arr[0])
            ma = max(ma, arr[-1])

        return res
''',
    call=f'Solution().maxDistance({ARR})',
    expect=7,
    views=[
        dict(type='text', fn=_formula, size=26, h=70),
        dict(type='grid', var='arrays', label='arrays（青/橙 = 当前 arr 的首/尾；蓝 = mi 来自哪，粉 = ma 来自哪）',
             rows=['0', '1', '2', '3'], cell=92, h=440, color=_color),
    ],
    watch=[('mi', 'mi', 'blue'), ('ma', 'ma', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = float': '`res = -∞`：原文是 `res = None`，==依赖 Python 2 里 None 比任何数都小==',
        'mi = arrays[0][0]': '升序 → 最小值是数组的==头一个元素==：`mi = arrays[0][0] = {mi}`',
        'ma = arrays[0][-1]': '最大值是数组的==最后一个元素==：`ma = arrays[0][-1] = {ma}`',
        'for arr in arrays[1:]': lambda S, B, ret: (f'遍历到 `arr = {S.arr}`' if S.get('arr') is not None and S.arr != B.get('arr')
                                                    else '遍历结束'),
        'res = max': lambda S, B, ret: (f'`arr[-1] − mi = {S.arr[-1]} − {B.mi} = {S.arr[-1] - B.mi}`，'
                                        f'`ma − arr[0] = {B.ma} − {S.arr[0]} = {B.ma - S.arr[0]}` → `res = {S.res}`'),
        'mi = min': lambda S, B, ret: (f'==然后==再用 `arr[0] = {S.arr[0]}` 更新 `mi = {S.mi}`'
                                       if S.arr == ARR[1] else f'`mi = min({B.mi}, {S.arr[0]}) = {S.mi}`'),
        'ma = max': lambda S, B, ret: (f'`ma = max({B.ma}, {S.arr[-1]}) = {S.ma}`'
                                       + ('：mi、ma 都来自这个数组，但之后每次只和其中一个相减，==不会选到同一个数组=='
                                          if S.arr[0] == S.mi and S.arr[-1] == S.ma else '')),
        'return res': '最大距离 =={ret}==',
    },
    cards=dict(
        one_liner='先用当前数组和之前的 mi/ma 更新答案，再更新 mi/ma',
        complexity='时间 `O(m)`，空间 `O(1)`',
        problem=['给定 `m` 个==升序==数组，从==两个不同的==数组中各选一个整数',
                 '距离定义为差的绝对值 `|a-b|`，返回最大距离',
                 '示例：`[[1,2,3],[4,5],[1,2,3]]` → `4`；本视频 `[[3,5],[1,4,9],[2,6],[4,7]]` → `7`'],
        quote='对于遍历到的arrays[index]，==首先使用arrays[index][-1] - mi以及ma - arrays[index][0]来更新最终答案==，然后再使用arrays[index][0]来更新mi，arrays[index][-1]来更新ma即可。',
        quote_src='—— yiduobo 题解',
        idea=['最大距离 = 某个数组的最大值 − 另一个数组的最小值',
              '数组有序：最小值是头一个元素，最大值是最后一个元素',
              '`mi`、`ma` 初始化为第 0 个数组的首尾，从第 1 个数组开始遍历'],
        result='运行结束：返回 `7` ✓',
        summary=['时间 `O(m)`，空间 `O(1)`',
                 '先更新答案再更新 `mi`/`ma`：保证两个数来自==不同==数组',
                 '原文 `res = None`（Python 2 中 None 小于任何数），这里改为 `float(\'-inf\')`；并删去 docstring',
                 '对比灵神：灵神用 `inf/-inf` 初始化并从第 0 个数组遍历，yiduobo 从第 1 个开始'],
    ),
)
