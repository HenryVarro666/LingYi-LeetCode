NUMS = [1, 5, 3, 4, 2]


def _sums(S):
    n = S['nums']
    return [n[i] + n[i + 1] for i in range(len(n) - 1)]


def _t1(S):
    s = _sums(S)
    return '相邻两数之和（共 n−1 = ' + str(len(s)) + ' 个）：`' + ', '.join(f'{S["nums"][i]}+{S["nums"][i+1]}={v}' for i, v in enumerate(s)) + '`'


def _t2(S):
    s = _sums(S)
    d = len(set(s))
    return f'去重后 `{sorted(set(s))}`，共 `{d}` 个；`{d} < {len(s)}` → ==有重复，存在和相等的子数组=='


CONFIG = dict(
    num=2395, title='和相等的子数组', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='相邻和 + 哈希集合去重',
    tags=[],
    code='''
class Solution:
    def findSubarrays(self, nums: List[int]) -> bool:
        return len(set(map(sum, pairwise(nums)))) < len(nums) - 1
''',
    call=f'Solution().findSubarrays({NUMS!r})',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums', cell=100, h=190),
        dict(type='text', fn=_t1, size=28, h=110),
        dict(type='text', fn=_t2, size=28, h=110),
    ],
    watch=[('n-1', 'len(nums) - 1', 'blue')],
    captions={
        'return len(set': lambda S, B, ret: (
            f'`pairwise(nums)` 给出全部 {len(S.nums) - 1} 个相邻对，`map(sum, …)` 求和得 `{_sums(S)}`；'
            f'`set` 去重剩 {len(set(_sums(S)))} 个，`{len(set(_sums(S)))} < {len(S.nums) - 1}` → 有重复，返回 =={ret}=='),
    },
    cards=dict(
        one_liner='n−1 个相邻和去重，个数不足 n−1 就有重复',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断是否存在==两个==长为 2 的子数组，和相等，且起始下标不同',
                 '示例：`[4,2,4]` → `true`（`4+2 = 2+4 = 6`）',
                 '本视频：`[1,5,3,4,2]`，`1+5 = 4+2 = 6` → `true`'],
        quote='统计相邻数字的和，加入哈希表中。一共有 n-1 个相邻数字的和。如果去重后，个数不足 n-1 个，则说明和相等的子数组存在。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长为 2 的子数组恰好有 `n-1` 个，每个起始下标对应一个和',
              '把这些和放进集合：若全不相同，集合大小仍是 `n-1`',
              '集合更小 ⇔ 至少两个和相等 ⇔ 答案为真'],
        result='相邻和 `[6, 8, 7, 6]` 去重后只剩 3 个，3 < 4 → True ✓',
        after=[dict(heading='一行代码拆开看', lines=[
            '`pairwise(nums)`：依次给出 `(nums[0], nums[1])`、`(nums[1], nums[2])`……共 n−1 对',
            '`map(sum, …)`：每一对求和，得到 n−1 个相邻和',
            '`set(…)`：去重；`len(…) < len(nums) - 1` 就说明有重复'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：比较的是个数 `n-1`，不是 `n`',
                 '也可以边遍历边判断，遇到见过的和就提前返回',
                 '思考题：子数组长度改成 k → 用滑窗维护和；改成子序列 → 需要换思路'],
    ),
)
