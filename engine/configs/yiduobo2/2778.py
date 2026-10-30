def _color(S, i, v):
    if 'index' not in S:
        return None
    n, cur, ln = len(S['nums']), S['index'], S.get('_line')
    a = S['nums']
    upto = sum(x * x for j, x in enumerate(a[:cur + 1]) if n % (j + 1) == 0)
    if n % (i + 1) == 0 and (i < cur or (i == cur and S.get('res') == upto)):
        return 'green'
    if i == cur and ln == 5:
        return 'blue'
    return None


def _dim(S, i, v):
    if 'index' not in S:
        return False
    n, cur, ln = len(S['nums']), S['index'], S.get('_line')
    return n % (i + 1) != 0 and (i < cur or (i == cur and ln == 5))


def show(S):
    if 'index' not in S:
        return '一趟遍历：下标 `index` 对应题目里的第 `index + 1` 个数'
    n, i = len(S['nums']), S['index']
    ok = n % (i + 1) == 0
    return (f"`len(nums) % (index + 1)` = `{n} % {i + 1}` = `{n % (i + 1)}` → "
            + ('==特殊元素==' if ok else '不是特殊元素'))


CONFIG = dict(
    num=2778, title='特殊元素平方和', difficulty='Easy', category='数学',
    author='yiduobo', technique='一趟遍历 · 下标 + 1 判断整除',
    tags=['字节30天'],
    code='''
class Solution(object):
    def sumOfSquares(self, nums):
        res = 0
        for index, v in enumerate(nums):
            if len(nums) % (index + 1) == 0:
                res += v * v

        return res
''',
    call='Solution().sumOfSquares([2,7,1,19,18,3])',
    expect=63,
    views=[
        dict(type='array', var='nums', label='nums（下标 index 从 0 开始；绿 = 特殊元素，暗 = 不是）', cell=110,
             pointers={'index': 'blue'}, color=_color, dim=_dim, h=220),
        dict(type='text', fn=show, size=28, h=70),
        dict(type='text', fn=lambda S: (f"`res = {S['res']}`" if 'res' in S else ''), size=30, h=70),
    ],
    watch=[('index', 'index', 'blue'), ('index + 1', lambda S: S['index'] + 1 if 'index' in S else None),
           ('v', 'v'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累加特殊元素的平方',
        'for index, v in enumerate(nums)': lambda S, B, ret: (f'`index = {S.index}`：题目里的第 `{S.index + 1}` 个数 `v = {S.v}`'
                                                              if S.index != B.get('index') else '遍历结束'),
        'if len(nums) % (index + 1) == 0': lambda S, B, ret: (
            f'`{len(S.nums)} % {S.index + 1} == 0` → 第 `{S.index + 1}` 个数是==特殊元素=='
            if len(S.nums) % (S.index + 1) == 0 else
            f'`{len(S.nums)} % {S.index + 1} = {len(S.nums) % (S.index + 1)}` → 不是，跳过'),
        'res += v * v': '`res += {v} × {v}` → `{res}`',
        'return res': '一趟遍历结束，返回 =={ret}==',
    },
    cards=dict(
        one_liner='按题意一趟遍历：长度能被 index + 1 整除，就累加 v²',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组 `nums` ==下标从 1 开始==，长度为 `n`',
                 '若 `n % i == 0`，则 `nums[i]` 是特殊元素；返回所有特殊元素的==平方和==',
                 '示例：`[2,7,1,19,18,3]` → `2² + 7² + 1² + 3² = 63`'],
        quote='按照题目要求直接一趟遍历，对于当前遍历到的下标index，若其满足index + 1可以被数组长度整除，那么就将==nums[index] * nums[index]累加到答案中==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['Python 的下标从 0 开始，题目从 1 开始：判断时用 `index + 1`',
              '条件其实是==数组长度能被 `index + 1` 整除==：`len(nums) % (index + 1) == 0`',
              '满足就 `res += v * v`'],
        result='特殊元素是第 1、2、3、6 个：`4 + 49 + 1 + 9 = 63` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：下标偏移，判断的是 `index + 1` 而不是 `index`（`index = 0` 时还会除零）',
                 '原文叙述「index + 1 可以被数组长度整除」说反了，以代码为准',
                 '原文为 Python 2 风格：删去了文档字符串，逻辑未改',
                 '灵神的优化：只枚举 `√n` 以内的因子 `i`，同时统计 `n / i`'],
    ),
)
