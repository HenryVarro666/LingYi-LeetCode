ARR = [13, 2, 9, 6, 14, 8]


def _in_res(S, i):
    a = S.get('arr')
    if not a or 'res' not in S:
        return False
    ps = {tuple(p) for p in S['res']}
    return (i + 1 < len(a) and (a[i], a[i + 1]) in ps) or (i > 0 and (a[i - 1], a[i]) in ps)


def _line(S):
    if 'index' in S:
        a, k = S['arr'], S['index']
        return f"`arr[{k}] − arr[{k-1}] = {a[k]} − {a[k-1]}` = =={a[k] - a[k-1]}==，`min_diff = {S['min_diff']}`"
    if 'min_diff' in S:
        return f"第一对 `[{S['arr'][0]}, {S['arr'][1]}]` 先当作答案，`min_diff = {S['min_diff']}`"
    return '最小绝对差==必然出现在相邻的两个元素之间=='


def _cap_if(S, B, ret):
    a, k = S.arr, S.index
    d = a[k] - a[k - 1]
    if d < B.min_diff:
        return f'`{d} < min_diff = {B.min_diff}` → 更小的差出现了'
    return f'`{d}` 不小于 `min_diff = {B.min_diff}`'


def _cap_elif(S, B, ret):
    a, k = S.arr, S.index
    d = a[k] - a[k - 1]
    if d == S.min_diff:
        return f'`{d} == min_diff` → 同样是最小差，也要输出'
    return f'`{d} > min_diff` → 跳过这一对'


CONFIG = dict(
    num=1200, title='最小绝对差', difficulty='Easy', category='普通数组',
    author='yiduobo', technique='排序后一趟扫描相邻元素',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def minimumAbsDifference(self, arr):

        arr = sorted(arr)
        res = [[arr[0], arr[1]]]
        min_diff = arr[1] - arr[0]
        for index in range(2, len(arr)):
            if arr[index] - arr[index - 1] < min_diff:
                min_diff = arr[index] - arr[index - 1]
                res = [[arr[index - 1], arr[index]]]
            elif arr[index] - arr[index - 1] == min_diff:
                res.append([arr[index - 1], arr[index]])

        return res
''',
    call=f'Solution().minimumAbsDifference({ARR})',
    expect=[[8, 9], [13, 14]],
    views=[
        dict(type='text', fn=_line, size=26, h=70),
        dict(type='array', var='arr', label='arr（从小到大排序后；绿 = res 里的数对）', h=230, cell=90,
             pointers={'index - 1': 'purple', 'index': 'cyan'},
             window=('index - 1', 'index'),
             color=lambda S, i, v: 'green' if _in_res(S, i) else None),
        dict(type='queue', var='res', label='res（具有最小绝对差的元素对）', h=150,
             fmt=lambda p: f'[{p[0]},{p[1]}]'),
    ],
    watch=['index', ('min_diff', 'min_diff', 'green')],
    captions={
        'arr = sorted(arr)': '先从小到大排序：`{arr}`，输出自然是升序',
        'res = [[arr[0], arr[1]]]': '先把第一对 `[{arr[0]}, {arr[1]}]` 放进答案（数组长度 ≥ 2）',
        'min_diff = arr[1] - arr[0]': '`min_diff` 用第一对的差初始化：`{arr[1]} − {arr[0]} = {min_diff}`',
        'for index in range': lambda S, B, r: ('扫描结束' if B.get('index') == S.index
                                               else f'看相邻对 `arr[{S.index-1}], arr[{S.index}]` = `{S.arr[S.index-1]}, {S.arr[S.index]}`'),
        'if arr[index] - arr[index - 1] < min_diff': _cap_if,
        'min_diff = arr[index]': '更新 `min_diff = {min_diff}`',
        'res = [[arr[index - 1]': '之前的数对差更大，==全部丢弃==，`res = {res}`',
        'elif arr[index]': _cap_elif,
        'res.append': '追加 `[{arr[index-1]}, {arr[index]}]`，`res = {res}`',
        'return res': '一趟扫描完成，返回 `{res}`',
    },
    cards=dict(
        one_liner='排好序后，最小绝对差必然出现在相邻两个元素之间',
        complexity='时间 `O(n log n)`，空间 `O(n)`（`sorted` 复制了一份）',
        problem=['给你个==互不相同==的整数数组 `arr`，找出所有绝对差最小的元素对',
                 '每对 `[a,b]` 满足 `a < b`，所有对按升序输出',
                 '示例：`[4,2,1,3]` → `[[1,2],[2,3],[3,4]]`',
                 f'本视频：`{ARR}` → `[[8,9],[13,14]]`'],
        quote='题目要求按照升序输出，那么我们可以将数组从小到大进行排序。完成排序后，可以明确的是==最小绝对差必然出现在相邻的两个元素之间==，因此可以一趟扫描求解最小绝对差以及对应的元素对。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序一举两得：==输出升序== + 只需比较相邻元素',
              '用第一对初始化 `res` 和 `min_diff`，从 `index = 2` 开始扫',
              '更小 → 重置 `res`；相等 → 追加；更大 → 跳过'],
        summary=['时间 `O(n log n)`，瓶颈在排序',
                 '易错：差更小时要==整体替换== `res`，而不是追加',
                 '用第一对初始化依赖 `len(arr) ≥ 2`（题目保证）',
                 '原文为 Python 2 写法，仅删去了类型注释的文档字符串'],
    ),
)
