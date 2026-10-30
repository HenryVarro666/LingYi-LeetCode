CONFIG = dict(
    num=2826, title='将三个组排序', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='正难则反 · 最长非递减子序列', tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1721'],
    code='''
class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        g = []
        for x in nums:
            j = bisect_right(g, x)
            if j == len(g):
                g.append(x)
            else:
                g[j] = x
        return len(nums) - len(g)
''',
    call='Solution().minimumOperations([2,1,3,2,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=200, label='nums'),
        dict(type='array', var='g', h=200, label='g：长为 j+1 的非递减子序列的最小结尾', pointers={'j': 'pink'}),
        dict(type='text', fn=lambda S: f"最多保留 `len(g) = {len(S['g'])}` 个，要删 `{len(S['nums'])} − {len(S['g'])} = {len(S['nums']) - len(S['g'])}` 个" if 'g' in S else ''),
    ],
    watch=[('x', 'x', 'yellow'), ('j', 'j', 'pink'), ('g', 'g', 'cyan')],
    captions={
        'g = []': '正难则反：算最多==保留==多少个数，保留的必须非递减；`g` 记录各长度的最小结尾',
        'j = bisect_right': '`bisect_right` 找第一个 `> {x}` 的位置：`j = {j}`（相等的数可以接在后面，所以用 right）',
        'if j == len': lambda S, B, r: (f'`j = {S.j} = len(g)`：没有比 `{S.x}` 大的结尾 → `{S.x}` 可接在最长序列后' if S.j == len(S.g)
                                        else f'`g[{S.j}] = {S.g[S.j]} > {S.x}`：可以被 `{S.x}` 替换'),
        'g.append': '`g` 末尾加入 `{x}`：最长非递减子序列变长到 =={len(g)}==',
        'g[j] = x': '`g[{j}]` 换成更小的 `{x}`：长度不变，后面更容易接上',
        'return len': '保留 `{len(g)}` 个，删除 `{len(nums)} − {len(g)}` = =={len(nums) - len(g)}== 个',
    },
    cards=dict(
        one_liner='正难则反：删得最少 = 留得最多 = 最长非递减子序列',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`nums` 每个元素是 1、2 或 3，每次可删一个元素',
                 '求让 `nums` 变成非递减所需的最少删除次数',
                 '示例：`[2,1,3,2,1]` → `3`'],
        quote='正难则反，计算最多保留多少个数。这些保留的数必须是非递减的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['问题等价于求 `nums` 的最长非递减子序列长度 `L`，答案 `n − L`',
              '`g[j]` 存长度 `j+1` 的子序列最小结尾，用二分维护',
              '非递减允许相等，所以二分用 `bisect_right`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '严格递增用 `bisect_left`，非递减用 `bisect_right`',
                 '题解另给两种写法：值域只有 3 的多维 DP（`O(nU)`，`f[x] += 1` 再传递），以及合法子序列 DP',
                 '`g` 不是真实的子序列，长度才是答案'],
    ),
)
