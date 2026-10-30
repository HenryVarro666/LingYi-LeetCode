A1 = [1, 2, 2, 6, 6, 6, 6, 7, 10]
A2 = [1, 2, 3, 4, 5, 6, 7, 7, 7]


def _color(S, k, v):
    if 'm' not in S:
        return None
    m = S['m']
    if 'x' in S and S['_line'] >= 6 and 'i' in S:
        if v == S['x']:
            return 'blue'
    if k in (m, 2 * m + 1, 3 * m + 2):
        return 'yellow' if S['_line'] < 6 else None
    return None


def _top(S):
    if 'm' not in S:
        return '有序数组：相同元素==连续==；出现次数 > 25% ⇔ 至少 `floor(n/4) + 1` 次'
    m, n = S['m'], len(S['arr'])
    if 'j' in S and S['_line'] >= 7 and 'x' in S:
        j = S['j']
        if j + m < n:
            return f"最左边的 `{S['x']}` 在 `j = {j}`；如果它出现 `> {m}` 次，`arr[j + m] = arr[{j + m}]` 也一定是 `{S['x']}`"
    return f"`n = {n}`，`m = n // 4 = {m}`：只需检查下标 `m, 2m+1, 3m+2` = `{m}, {2*m+1}, {3*m+2}`"


def _if(S, B, ret):
    j, m, x = S.j, S.m, S.x
    y = S.arr[j + m]
    if y == x:
        return f'`arr[{j} + {m}] = arr[{j + m}] = {y} == {x}`：从 `{j}` 到 `{j + m}` 全是 `{x}`，共 `> {m}` 个 → ==找到答案=='
    return f'`arr[{j + m}] = {y} ≠ {x}`：`{x}` 不足 `{m + 1}` 个 → 检查下一个候选'


CONFIG = dict(
    num=1287, title='有序数组中出现次数超过25%的元素', difficulty='Easy', category='二分算法',
    author='灵茶山艾府', technique='检查三个候选下标 + 二分',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution:
    def findSpecialInteger(self, arr: List[int]) -> int:
        m = len(arr) // 4
        for i in (m, m * 2 + 1):
            x = arr[i]
            j = bisect_left(arr, x)
            if arr[j + m] == x:
                return x
        return arr[m * 3 + 2]
''',
    call=f'''s = Solution()
[s.findSpecialInteger({A1}), s.findSpecialInteger({A2})]''',
    expect=[6, 7],
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var='arr', label='arr（黄 = 候选下标 m, 2m+1, 3m+2；蓝 = 等于 x 的段）', cell=90, color=_color,
             pointers={'i': 'yellow', 'j': 'blue', 'j + m if "j" in _inner and _line >= 7 else None': 'pink'},
             pointer_labels={'j + m if "j" in _inner and _line >= 7 else None': 'j+m'}, h=300),
    ],
    watch=[('m', 'm', 'cyan'), ('i', 'i', 'yellow'), ('x', 'x', 'blue'), ('j', 'j', 'blue')],
    captions={
        'm = len(arr) // 4': '`m = {len(arr)} // 4 = {m}`：答案至少出现 `m + 1 = {m + 1}` 次',
        'for i in (m': lambda S, B, r: (f'检查候选下标 `i = {S.i}`' if S.get('i') != B.get('i') else '两个候选都不是'),
        'x = arr[i]': '`x = arr[{i}] = {x}`',
        'j = bisect_left': '二分找最左边的 `{x}`：`j = {j}`',
        'if arr[j + m] == x': _if,
        'return x': '返回 =={ret}==',
        'return arr[m * 3 + 2]': '答案存在，又不是 `arr[m]`、`arr[2m+1]` → 只能是 `arr[{3*m+2}]` = =={ret}==',
    },
    cards=dict(
        one_liner='网孔不能比鱼大：只检查 m、2m+1、3m+2 三个下标',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['非递减数组 `arr` 中恰好有一个整数出现次数 ==超过 25%==，返回它',
                 '示例：`[1,2,2,6,6,6,6,7,10]` → `6`',
                 '本视频再跑一个答案在末尾的例子：`[1,2,3,4,5,6,7,7,7]` → `7`'],
        quote='好比用网去捕鱼，如果网孔比鱼还大，那么就会出现漏网之鱼。……我们至多检查 3 个下标 m, 2m+1, 3m+2，其中一定有一个 arr[i] 的出现次数至少为 m+1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案是一段长度 `>= m + 1` 的连续区间，相邻检查点之间只隔 `m` 个数 → 一定被「网」住',
              '二分出最左边的 `x` 的下标 `j`，只需看 `arr[j + m]` 是否还等于 `x`',
              '前两个都不是，答案就一定是 `arr[3m + 2]`，不用再二分'],
        summary=['时间 `O(log n)`：最多两次二分；空间 `O(1)`',
                 '优化前：`bisect_right − bisect_left > m` 直接算个数，要四次二分',
                 '`j + m` 不会越界：越界说明没有符合要求的数，与题意矛盾',
                 '`n = 1` 时 `m = 0`，第一次检查就返回，不会访问 `2m + 1`'],
    ),
)
