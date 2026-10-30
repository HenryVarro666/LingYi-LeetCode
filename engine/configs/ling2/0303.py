NUMS = [-2, 0, 3, -5, 2, -1]
QUERIES = [(0, 2), (2, 5), (0, 5)]


def _s(S):
    return S.get('s') if isinstance(S.get('s'), list) else S.get('self.s')


def _in_query(S):
    return 'left' in S and 'right' in S


W = lambda S: S['i'] + 1 if 'i' in S and not _in_query(S) else None          # noqa: E731
RP = lambda S: S['right'] + 1 if _in_query(S) else None                       # noqa: E731
LP = lambda S: S['left'] if _in_query(S) else None                            # noqa: E731


def _s_color(S, k, v):
    if _in_query(S):
        if k == S['right'] + 1:
            return 'green'
        if k == S['left']:
            return 'red'
        return None
    if 'i' in S and k <= S['i'] + (S.get('_line') == 5):
        return 'cyan'
    return None


def _formula(S):
    s = _s(S)
    if s is None:
        return ''
    if _in_query(S):
        l, r = S['left'], S['right']
        return (f"`[{l}, {r}]` 的和 = `s[{r + 1}] − s[{l}]` = `{s[r + 1]} − ({s[l]})` = =={s[r + 1] - s[l]}==")
    if 'i' in S:
        i = S['i']
        if S.get('_line') == 5:
            return f"`s[{i + 1}] = s[{i}] + nums[{i}]` = `{s[i]} + ({S['x']})` = =={s[i + 1]}=="
        return f"前 `{i}` 个数的和 `s[{i}] = {s[i]}`，再加上 `nums[{i}] = {S['x']}`"
    return '`s[0] = 0`：前 0 个数的和'


CONFIG = dict(
    num=303, title='区域和检索 - 数组不可变', difficulty='Easy', category='子串',
    author='灵茶山艾府', technique='前缀和 · 长度 n+1，s[0] = 0',
    tags=['字节30天'],
    code='''
class NumArray:
    def __init__(self, nums: List[int]):
        s = [0] * (len(nums) + 1)
        for i, x in enumerate(nums):
            s[i + 1] = s[i] + x
        self.s = s

    def sumRange(self, left: int, right: int) -> int:
        return self.s[right + 1] - self.s[left]
''',
    call=f'''na = NumArray({NUMS})
[na.sumRange(l, r) for l, r in {QUERIES}]''',
    expect=[1, -1, -3],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='array', var=lambda S: NUMS, label='nums（nums[k] 夹在 s[k] 和 s[k+1] 之间）', cell=96, h=215, window=('left', 'right'),
             pointers={'i': 'blue', 'left': 'red', 'right': 'green'},
             color=lambda S, k, v: 'blue' if ('i' in S and not _in_query(S) and k == S['i']) else None),
        dict(type='array', var=_s, label='s（s[k] = 前 k 个数的和，长度 n+1）', cell=96, h=230,
             pointers={W: 'blue', LP: 'red', RP: 'green'},
             pointer_labels={W: 'i+1', LP: 'left', RP: 'right+1'}, color=_s_color),
    ],
    watch=['i', 'x', ('left', 'left', 'red'), ('right', 'right', 'green')],
    captions={
        's = [0] * (len(nums) + 1)': '前缀和数组长 `n+1 = {len(s)}`；==`s[0] = 0`== 表示前 0 个数的和',
        'for i, x in enumerate(nums)': lambda S, B, r: (f'`i = {S.i}`：把 `nums[{S.i}] = {S.x}` 加进前缀和'
                                                       if 'i' not in B or B.i != S.i else '所有前缀和都算好了'),
        's[i + 1] = s[i] + x': '前 `{i}` 个数的和加上 `nums[{i}]`，就是前 `{i + 1}` 个数的和：`s[{i + 1}] = {s[i + 1]}`',
        'self.s = s': '保存 `self.s = {s}`：预处理 `O(n)`，之后每次查询 `O(1)`',
        'return self.s[right + 1]': lambda S, B, r: (
            f'`[{S.left}, {S.right}]` = 前缀 `[0, {S.right}]` 去掉前缀 `[0, {S.left - 1}]`：`s[{S.right + 1}] − s[{S.left}]` = =={r}=='
            if S.left else
            f'`[0, {S.right}]` 本身就是前缀：`s[{S.right + 1}] − s[0]` = =={r}==；有 `s[0] = 0`，==left 为 0 也不用特判=='),
    },
    cards=dict(
        one_liner='任意子数组的和，都可以表示为两个前缀和的差',
        complexity='初始化 `O(n)`，`sumRange` `O(1)`；空间 `O(n)`',
        problem=['给定整数数组 `nums`，多次查询下标 `[left, right]`（闭区间）的元素和',
                 '实现 `NumArray(nums)` 和 `sumRange(left, right)`',
                 '示例：`nums = [-2,0,3,-5,2,-1]`',
                 '`sumRange(0,2) = 1`，`sumRange(2,5) = -1`，`sumRange(0,5) = -3`'],
        quote='任意子数组都是一个前缀去掉前缀后的结果。所以==任意子数组的和，都可以表示为两个前缀和的差==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s[i]` = 前 `i` 个数的和，长度 `n+1`，递推 `s[i+1] = s[i] + a[i]`',
              '`[left, right]` 的和 = `s[right+1] − s[left]`',
              '定义 `s[0] = 0`：`left = 0` 时也能套公式，不用特判'],
        result='三次查询依次返回 `[1, -1, -3]` ✓',
        summary=['预处理 `O(n)`，每次查询 `O(1)`：把 `O(n²)` 个子数组和压缩进 `O(n)` 个前缀',
                 '易错：下标是 `s[right + 1] − s[left]`，不是 `s[right] − s[left]`',
                 'Python 库函数写法：`self.s = list(accumulate(nums, initial=0))`',
                 '扩展：560 和为 K 的子数组、304 二维前缀和、307 可修改（树状数组）'],
    ),
)
