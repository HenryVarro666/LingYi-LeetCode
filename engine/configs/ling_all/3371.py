NUMS = [1, -2, -3, -1, 7, -5]


def _cur(S):
    return S['nums'].index(S['y']) if 'y' in S and S['_line'] != 11 else None


def _txt(S):
    if 'total' not in S:
        return '异常值 `x` + 元素和 `y` + 其余 `n − 2` 个数（和也是 `y`）= `total`'
    if 't' not in S:
        return f"==`x + 2y = total = {S['total']}`==：枚举 `y`，异常值就是 `total − 2y`"
    return f"`t = total − 2y = {S['total']} − 2×({S['y']})` = =={S['t']}=="


CONFIG = dict(
    num=3371, title='识别数组中的最大异常值', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='x + 2y = total · 枚举元素和',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1644'],
    code='''
class Solution:
    def getLargestOutlier(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        total = sum(nums)

        ans = -inf
        for y in nums:
            t = total - y * 2
            if t in cnt and (t != y or cnt[t] > 1):
                ans = max(ans, t)
        return ans
''',
    call=f'Solution().getLargestOutlier({NUMS})',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 枚举的元素和 y，绿 = 对应的异常值 t）', h=210,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'y'},
             color=lambda S, i, v: ('blue' if i == _cur(S) else
                                    'green' if 't' in S and _cur(S) is not None and v == S['t'] and S['t'] in S['cnt'] else None)),
        dict(type='map', var='cnt', label='cnt（每个数的出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', h=90, size=30, fn=_txt),
    ],
    watch=['total', ('y', 'y', 'blue'), ('t', 't', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'cnt = Counter': '`cnt` 统计每个数的出现次数，用来 `O(1)` 判断 `t` 在不在数组里',
        'total = sum': '`total = {total}`：==`x + 2y = total`==，变成“两数之和”',
        'ans = -inf': '`ans` 先设为 `-inf`',
        'for y in nums': lambda S, B, r: (f'枚举元素和 `y = {S.y}`' if _cur(S) is not None and B.get('y') != S.y or 't' not in B else '枚举完毕'),
        't = total - y * 2': '异常值只能是 `t = {total} − 2×({y}) = {t}`',
        'if t in cnt and': lambda S, B, r: (f'`{S.t}` 不在数组中 → `y = {S.y}` 不行' if S.t not in S.cnt else
                                           (f'`t = y = {S.t}` 但只出现 1 次：==同一个下标不能既是和又是异常值== → 不行' if S.t == S.y and S.cnt[S.t] <= 1 else
                                            (f'`t = y = {S.t}` 且出现 {S.cnt[S.t]} 次 → 合法' if S.t == S.y else f'`{S.t}` 在数组中且 `≠ y` → 合法的异常值'))),
        'ans = max(ans, t)': '`ans = max({B.ans}, {t})` = =={ans}==',
        'return ans': '最大异常值为 `{ans}`',
    },
    cards=dict(
        one_liner='异常值 x 和元素和 y 满足 x + 2y = total，变成两数之和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n − 2` 个特殊数字，一个是它们的==和==，一个是==异常值==',
                 '求可能的最大异常值（下标要不同，值可以相同）',
                 '示例：`[2,3,5,10]` → `10`；`[-2,-1,-3,-6,4]` → `4`',
                 f'本视频：`{NUMS}` → `7`'],
        quote='设异常值为 x，元素和为 y，那么其余 n−2 个数的和也是 y，所以 ==x+2y 就是整个 nums 数组的元素和 total==。这是我们最熟悉的 1. 两数之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 `y = nums[i]`，异常值就是 `t = total − 2y`',
              '`t` 要在数组中出现；若 `t == y`，它必须==至少出现两次==',
              '所有合法的 `t` 取最大值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`t == y` 时要求 `cnt[t] > 1`，不能复用同一个下标',
                 '方法一（枚举异常值 x）：判断 `(total − x)` 为偶数且 `(total − x) / 2` 在其余数中',
                 '本视频选方法二（枚举元素和），不用判断奇偶'],
    ),
)
