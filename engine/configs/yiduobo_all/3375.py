CONFIG = dict(
    num=3375, title='使数组的值全部为 K 的最少操作次数', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='每轮降次大值 · 数不同元素',
    tags=['灵神题单', '难度分 1383'],
    code='''
class Solution(object):
    def minOperations(self, nums, k):
        
        mi = min(nums)
        if mi < k:
            return -1

        res = len(set(nums)) - 1
        if k < mi:
            res += 1
        return res
''',
    call='Solution().minOperations([9,7,5,3,7], 1)',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums', h=240,
             color=lambda S, i, v: 'green' if 'mi' in S and v == S['mi'] else None),
        dict(type='set', var=lambda S: set(S['nums']), h=170, fmt=lambda x: str(x), label='set(nums)'),
        dict(type='text', fn=lambda S: (f"最小值 `{S['mi']}` 与 k = `{S['k']}`" + ('：最小值已经小于 k，变不成 → ==-1==' if S['mi'] < S['k'] else '')) if 'mi' in S else f"目标 k = `{S['k']}`", size=30),
        dict(type='text', fn=lambda S: f"res = `{S['res']}`" + ('（m 种不同值，m-1 轮降到最小值）' if 'res' in S else ''), size=30),
    ],
    watch=[('k', 'k', 'pink'), ('mi', 'mi', 'green'), ('res', 'res', 'orange')],
    captions={
        'mi = min': '`mi = min(nums) = {mi}`：最小的数只会被压低，不会被抬高',
        'if mi < k': lambda S, B, r: (f'`mi = {S.mi} < k = {S.k}`：这个数永远变不成 k → 无解' if S.mi < S.k else f'`mi = {S.mi} >= k = {S.k}`：k 不大于最小值，有办法'),
        'return -1': '返回 `-1`',
        'res = len': '有 `m = {len(set(nums))}` 种不同的值：每轮选次大值作 h，`m-1` 轮把所有数降到最小值 → `res = {res}`',
        'if k < mi': lambda S, B, r: (f'`k = {S.k} < mi = {S.mi}`：还差一步，要再降到 k' if S.k < S.mi else f'`k = {S.k} == mi = {S.mi}`：已经全是 k，无需额外操作'),
        'res += 1': '多一次操作把整个数组降到 k：`res = {res}`',
        'return res': '最少操作次数 =={res}==',
    },
    cards=dict(
        one_liner='先判无解，再按「次大值」逐轮降低，最后看要不要多降一步',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`h` 合法：所有严格大于 `h` 的元素都相等；操作把所有大于 `h` 的元素变成 `h`',
                 '求把全部元素变成 `k` 的最少操作次数，不行返回 `-1`',
                 '本视频：`[9,7,5,3,7], k=1` → `4`'],
        quote='若nums中有m种不同的元素，那么可以在m - 1轮操作后将nums中的所有元素都变为nums中的最小值。接下来，若k小于这个最小值，那么还需要一次操作……',
        quote_src='—— yiduobo 题解原文',
        idea=['特殊情况：最小值 `< k`，这个值变不成 `k` → 返回 `-1`',
              '一般情况：每轮选次大值作 `h`，把最大的元素降一档，轮数最少',
              '`m` 种不同元素 → `m-1` 轮降到最小值；`k` 更小再加 1 轮'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`mi < k` 返回 -1（不是 `mi > k`）',
                 '`k == mi` 时不用再加 1',
                 '对比灵神：yiduobo 用 `res` 加 `if` 分步，灵神一句 `- (k == mn)` 合并',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
