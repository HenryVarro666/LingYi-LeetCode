_last = [None]
_inner = {'a': 'b', 'b': 'c', 'c': 'd', 'd': 'if'}


def _mark(tag, fn):
    def f(S, B, ret):
        _last[0] = tag
        return fn(S, B, ret)
    return f


def _loop(var, outer, fresh, done):
    def f(S, B, ret):
        prev = _last[0]
        _last[0] = var
        if prev == _inner[var] and S[var] == B[var]:
            return done
        return fresh.format(S[var])
    return f


def _txt(S):
    if 'd' not in S:
        return '找 `a < b < c < d`，满足 `nums[a] + nums[b] + nums[c] == nums[d]`'
    n = S['nums']
    a, b, c, d = S['a'], S['b'], S['c'], S['d']
    t = n[a] + n[b] + n[c]
    ok = '==相等，计数==' if t == n[d] else '不相等'
    return f'`({a},{b},{c},{d})`：`{n[a]} + {n[b]} + {n[c]} = {t}`，`nums[d] = {n[d]}` → {ok}'


def _col(S, i, v):
    for k, c in (('d', 'green'), ('c', 'purple'), ('b', 'pink'), ('a', 'blue')):
        if k in S and S[k] == i:
            return c
    return None


def _if(S, B, ret):
    n, a, b, c, d = S.nums, S.a, S.b, S.c, S.d
    t = n[a] + n[b] + n[c]
    if t == n[d]:
        return f'`{n[a]} + {n[b]} + {n[c]} = {t}` 恰好等于 `nums[{d}] = {n[d]}` → 是特殊四元组'
    return f'`{n[a]} + {n[b]} + {n[c]} = {t} ≠ nums[{d}] = {n[d]}`，不是'


CONFIG = dict(
    num=1995, title='统计特殊四元组', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='四重循环暴力枚举',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def countQuadruplets(self, nums):

        n = len(nums)
        res = 0

        for a in range(n - 3):
            for b in range(a + 1, n - 2):
                for c in range(b + 1, n - 1):
                    for d in range(c + 1, n):
                        if nums[a] + nums[b] + nums[c] == nums[d]:
                            res += 1

        return res
''',
    call='Solution().countQuadruplets([1,1,1,3,5])',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'a': 'blue', 'b': 'pink', 'c': 'purple', 'd': 'green'},
             color=_col, cell=110, h=300),
        dict(type='text', fn=_txt, size=30, h=120),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'pink'), ('c', 'c', 'purple'), ('d', 'd', 'green'), ('res', 'res', 'orange')],
    captions={
        'n = len': '`n = {n}`',
        'res = 0': '`res` 记录特殊四元组的个数',
        'for a in range': _loop('a', None, '第一个数 `a = {}`（最多到 `n − 4`，后面要留 3 个位置）', '`a` 枚举完 → 结束'),
        'for b in range': _loop('b', 'a', '第二个数 `b = {}`，从 `a + 1` 开始保证 `a < b`', '`b` 走到头，回到外层换 `a`'),
        'for c in range': _loop('c', 'b', '第三个数 `c = {}`', '`c` 走到头，回到外层换 `b`'),
        'for d in range': _loop('d', 'c', '第四个数 `d = {}`：看它是否等于前三数之和', '`d` 走到头，回到外层换 `c`'),
        'if nums[a]': _mark('if', _if),
        'res += 1': _mark('if', lambda S, B, ret: f'计数加一 → `res = {S.res}`'),
        'return res': '一共 =={ret}== 个特殊四元组',
    },
    cards=dict(
        one_liner='数据范围很小，直接四重循环暴力枚举',
        complexity='时间 `O(n^4)`，空间 `O(1)`',
        problem=['统计满足 `a < b < c < d` 且 `nums[a] + nums[b] + nums[c] == nums[d]` 的四元组个数',
                 '`4 <= nums.length <= 50`，`1 <= nums[i] <= 100`',
                 '示例：`[1,1,1,3,5]` → `4`：(0,1,2,3)、(0,1,3,4)、(0,2,3,4)、(1,2,3,4)'],
        quote='稍微转化一下就是四数之和问题，可以使用之前相同的方法来处理……我在这里偷懒，==直接使用了四次方的暴力算法==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 50` 时 `C(50,4)` 约 23 万组，四重循环完全够用',
              '下一层从上一层 `+ 1` 开始，自然保证 `a < b < c < d`',
              '每组判断前三个数之和是否等于第四个数'],
        summary=['时间 `O(n^4)`，空间 `O(1)`，`n ≤ 50` 可过',
                 '循环上界 `n − 3`、`n − 2`、`n − 1`：给后面的下标留位置',
                 '易错：`d` 必须在最右边，不能交换顺序',
                 '原文为 Python 2 风格写法，代码可直接在 Python 3 运行，未作改动',
                 '更快：移项成 `nums[a] + nums[b] = nums[d] − nums[c]`，枚举 b 用哈希表可做到 `O(n^2)`'],
    ),
)
