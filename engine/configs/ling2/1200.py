ARR = [9, 4, 11, 1, 6, 3, 10]


def _pairs(S):
    return {tuple(p) for p in (S.get('ans') or [])}


def _in_ans(S, i):
    a = S.get('arr')
    if not a or S.get('_line', 0) <= 3:
        return False
    ps = _pairs(S)
    return (i + 1 < len(a) and (a[i], a[i + 1]) in ps) or (i > 0 and (a[i - 1], a[i]) in ps)


def _diff_line(S):
    if 'x' not in S:
        return '排序后，==最小绝对差只能来自相邻元素==（不相邻的差更大）'
    md = S.get('min_diff')
    md = '∞' if md == float('inf') else md
    return f"相邻对 `({S['x']}, {S['y']})`：`diff = {S['y']} − {S['x']}` = =={S['y'] - S['x']}==，当前 `min_diff = {md}`"


def _cap_if(S, B, ret):
    md = '∞' if B.min_diff == float('inf') else B.min_diff
    if S.diff < B.min_diff:
        return f'`diff = {S.diff} < min_diff = {md}` → 找到==更小==的差，之前的答案全部作废'
    return f'`diff = {S.diff}` 不小于 `min_diff = {md}` → 看看是否相等'


def _cap_elif(S, B, ret):
    if S.diff == S.min_diff:
        return f'`diff = {S.diff} == min_diff` → 并列最小，追加到答案'
    return f'`diff = {S.diff} > min_diff = {S.min_diff}` → 不是最小差，跳过'


CONFIG = dict(
    num=1200, title='最小绝对差', difficulty='Easy', category='普通数组',
    author='灵茶山艾府', technique='排序 + 只看相邻元素',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()
        min_diff = inf
        ans = []
        for x, y in pairwise(arr):
            diff = y - x
            if diff < min_diff:
                min_diff = diff
                ans = [[x, y]]
            elif diff == min_diff:
                ans.append([x, y])
        return ans
''',
    call=f'Solution().minimumAbsDifference({ARR})',
    expect=[[3, 4], [9, 10], [10, 11]],
    views=[
        dict(type='text', fn=_diff_line, size=26, h=70),
        dict(type='array', var='arr', label='arr（排序后；绿 = 当前答案里的数对）', h=230, cell=84,
             pointers={'arr.index(x)': 'blue', 'arr.index(y)': 'pink'},
             pointer_labels={'arr.index(x)': 'x', 'arr.index(y)': 'y'},
             window=('arr.index(x)', 'arr.index(y)'),
             color=lambda S, i, v: 'green' if _in_ans(S, i) else None),
        dict(type='queue', var='ans', label='ans（所有差为 min_diff 的数对）', h=140,
             fmt=lambda p: f'[{p[0]},{p[1]}]'),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'diff', ('min_diff', 'min_diff', 'green')],
    captions={
        'arr.sort()': '先排序：`{arr}`，答案也自然按升序输出',
        'min_diff = inf': '`min_diff` 初始为 ==无穷大==，第一个相邻差一定会更新它',
        'ans = []': '答案列表先置空',
        'for x, y in pairwise': lambda S, B, r: ('相邻对遍历完了 → 结束循环' if B.get('x') == S.x and B.get('y') == S.y
                                               else f'取相邻元素 `(x, y) = ({S.x}, {S.y})`'),
        'diff = y - x': lambda S, B, r: (f'排好序 → `y > x`，绝对差就是 `y − x = {S.diff}`，不用 abs' if S.x == S.arr[0]
                                       else f'`diff = {S.y} − {S.x} = {S.diff}`'),
        'if diff < min_diff': _cap_if,
        'min_diff = diff': '更新 `min_diff = {min_diff}`',
        'ans = [[x, y]]': '答案==重置==为 `[[{x}, {y}]]`（而不是 append）',
        'elif diff == min_diff': _cap_elif,
        'ans.append': '`[{x}, {y}]` 加入答案：现在共 {len(ans)} 对',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='排序后，最小绝对差只能来自相邻元素',
        complexity='时间 `O(n log n)`（排序），空间 `O(1)`（不计排序栈和答案）',
        problem=['给你个==互不相同==的整数数组 `arr`，找出所有绝对差最小的元素对',
                 '每对 `[a,b]` 满足 `a < b`，且所有对按升序输出',
                 '示例：`[4,2,1,3]` → `[[1,2],[2,3],[3,4]]`',
                 f'本视频：`{ARR}` → `[[3,4],[9,10],[10,11]]`'],
        quote='把 arr 排序后，==最小绝对差只能来自相邻元素==（不相邻的元素之差更大）。如果 diff < minDiff，更新答案为 [[x,y]]；如果 diff = minDiff，把 [x,y] 添加到答案中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后 `a < b < c` 时 `c − a > b − a`：只需比较 `n−1` 个相邻差',
              '一趟遍历同时维护 `min_diff` 和答案：==更小就重置，相等就追加==',
              '`pairwise(arr)` 直接给出相邻对 `(x, y)`'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '易错：遇到更小的差要==重置==答案 `ans = [[x, y]]`，不能 append',
                 '`min_diff` 初始为 `inf`，第一对一定会进入 `if` 分支',
                 '也可以两次遍历：先求最小差，再收集差等于它的相邻对'],
    ),
)
