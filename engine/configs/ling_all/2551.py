CONFIG = dict(
    num=2551, title='将珠子放入背包中', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='等价转化 · 相邻和排序',
    tags=['灵神题单', '难度分 2042'],
    code='''
class Solution:
    def putMarbles(self, weights: List[int], k: int) -> int:
        for i in range(len(weights) - 1):
            weights[i] += weights[i + 1]  # 原地求前缀和
        weights.pop()
        weights.sort()
        return sum(weights[len(weights) - k + 1:]) - sum(weights[:k - 1])
''',
    call='Solution().putMarbles([3,1,5,2,4,1], 3)',
    expect=4,
    views=[
        dict(type='text', h=60, fn=lambda S: (
            f"原数组两端 `{S['weights'][0]}` 与最后一个数一定计入分数，最大最小相减抵消" if '_line' in S and 'i' not in S else
            ('每个切点贡献 `weights[i] + weights[i+1]`，现在数组里存的就是这些相邻和' if S.get('i') is not None else ''))),
        dict(type='array', var='weights', pointers={'i': 'blue'}, h=330, label='weights（逐步变成相邻和）'),
        dict(type='text', h=70, fn=lambda S: (
            f"取最大 `k-1 = {S['k']-1}` 个：==大的{S['k']-1}个之和=={sum(S['weights'][len(S['weights'])-S['k']+1:])}；最小 `k-1` 个之和 =={sum(S['weights'][:S['k']-1])}==" if S.get('_line') and 'weights' in S and len(S['weights']) == 5 and S['weights'] == sorted(S['weights']) else '')),
    ],
    watch=['i', 'k', ('weights', 'weights', 'cyan')],
    captions={
        'weights[i] += weights[i + 1]': '第 `{i}` 个位置和下一个位置相加：切在 `{i}` 与 `{i+1}` 之间，要同时算上这两个数 → `weights[{i}] = {weights[i]}`',
        'weights.pop()': '最后一个数没有“下一个”，不是切点和，丢掉；剩下 n-1 个相邻和',
        'weights.sort()': '排序：小的在左，大的在右，排好后 `{weights}`',
        'return': '最大的 `k-1` 个（`weights[n-k+1:]`）之和 减去 最小的 `k-1` 个（`weights[:k-1]`）之和 = =={ret}==',
    },
    cards=dict(
        one_liner='k 个背包 = 切 k-1 刀，每刀贡献相邻两数之和',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['把 `weights` 切成 `k` 个连续的背包，背包价格 = 首 + 尾',
                 '分数 = 所有背包价格之和，求最大分数 − 最小分数',
                 '示例：`[1,3,5,1], k=2` → `4`；本视频：`[3,1,5,2,4,1], k=3` → `4`'],
        quote='`weights[0]` 和 `weights[n-1]` 一定在分数中，最大分数和最小分数相减，抵消了。上一个子数组的末尾和下一个子数组的开头一定同时在分数中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['等价转化：问题变成“选 `k-1` 个切点”，每个切点贡献相邻和 `w[i]+w[i+1]`',
              '最大分数选最大的 `k-1` 个，最小分数选最小的 `k-1` 个',
              '排序后头尾各取 `k-1` 个相减即可'],
        summary=['时间 `O(n log n)`，用快速选择可到 `O(n)`；空间 `O(1)`（原地改数组）',
                 '一共有 `n-1` 个切点和，别忘了 `pop` 掉最后一个多余的数',
                 '`k=1` 时两段切片都为空，答案为 0；注意 `weights[len-k+1:]` 的下标',
                 '原地循环是顺序遍历，`weights[i+1]` 还没被改，所以算出来的是相邻和（注释写“前缀和”是口误）'],
    ),
)
