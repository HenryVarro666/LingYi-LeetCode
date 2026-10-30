NUMS = [1, 5, 2, 9, 4]


def _pairs(S):
    a = S['nums'] + [S['nums'][0]]
    return [(a[k], a[k + 1]) for k in range(len(a) - 1)]


def _diffs(S):
    return [abs(x - y) for x, y in _pairs(S)]


def _fn(S):
    ds = _diffs(S)
    ps = _pairs(S)
    seg = '　'.join(f'|{x}−{y}|=={d}==' if d == max(ds) else f'|{x}−{y}|={d}' for (x, y), d in zip(ps, ds))
    return seg


CONFIG = dict(
    num=3423, title='循环数组中相邻元素的最大差值', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='pairwise + 首尾补一项',
    code='''
class Solution:
    def maxAdjacentDistance(self, nums: List[int]) -> int:
        return max(abs(x - y) for x, y in pairwise(nums + [nums[0]]))
''',
    call=f'Solution().maxAdjacentDistance({NUMS})',
    expect=7,
    views=[
        dict(type='array', var=lambda S: S['nums'] + [S['nums'][0]], label='nums + [nums[0]]（末尾补上首项，把环拉直）', cell=90, h=200,
             color=lambda S, k, v: 'yellow' if k == len(S['nums']) else None),
        dict(type='text', fn=_fn, size=26),
        dict(type='text', fn=lambda S: f'相邻差的最大值 = =={max(_diffs(S))}==', size=34),
    ],
    watch=[],
    captions={
        'return max': lambda S, B, ret: ('把 `nums` 末尾补一个 `nums[0]`，相邻两项一对对看：' + '，'.join(f'`|{x}−{y}|={abs(x-y)}`' for x, y in _pairs(S))
                                          + f'。其中最大的是 ==`{ret}`==，返回'),
    },
    cards=dict(
        one_liner='末尾补一个首项，把环拉直，再看相邻差',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['循环数组 `nums`，==首尾也相邻==',
                 '求所有相邻元素绝对差的最大值',
                 '示例：`[1,2,4]` → `3`（首尾 `|4-1|`）',
                 '本视频：`[1,5,2,9,4]` → `7`（`|9-2|`）'],
        quote='遍历数组，计算相邻元素之差的最大值。由于数组是环形的，需额外考虑首尾两项之差。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums + [nums[0]]` 末尾再放一份首项',
              '`pairwise` 生成相邻对，其中最后一对 `(nums[-1], nums[0])` 正好是首尾',
              '对每一对取 `abs(x - y)`，再取 `max`，不用单独特判'],
        before=[dict(heading='先看一个环', lines=[
            '把数组首尾接起来成一个圈：`1 → 5 → 2 → 9 → 4 → 1`',
            '一共 `n` 对相邻元素，而不是普通数组的 `n-1` 对',
            '多出来的那一对，就是==最后一项和第一项=='])],
        after=[dict(heading='为什么补一项就够了', lines=[
            '补上 `nums[0]` 后，数组变成 `n + 1` 项，`pairwise` 恰好给出 `n` 对',
            '前 `n-1` 对是普通相邻，最后一对是 `(nums[-1], nums[0])`',
            '这样循环的特殊性被“拉直”了，代码只剩一行'])],
        summary=['时间 `O(n)`，空间 `O(1)`（拼接数组与生成器的开销忽略不计）',
                 '易错：别漏了首尾这一对；差值要取绝对值',
                 '本例首尾 `|1-4|=3`，最大差在中间 `|2-9|=7`，说明首尾不一定是答案'],
    ),
)
