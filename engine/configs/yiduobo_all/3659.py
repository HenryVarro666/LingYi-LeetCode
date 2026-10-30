NUMS, K = [3, 5, 2, 2], 2

CONFIG = dict(
    num=3659, title='数组元素分组', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='鸽笼原理 · 哈希计数',
    tags=['灵神题单', '贪心与思维', '难度分 1440'],
    code='''
class Solution(object):
    def partitionArray(self, nums, k):
        
        n = len(nums)
        if n % k != 0:
            return False
        
        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            if cnt[v] > n // k:
                return False
        return True
''',
    call=f'Solution().partitionArray({NUMS}, {K})',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: 'blue' if S.get('v') == v else None),
        dict(type='map', var='cnt', label='cnt（元素 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=180, font=34),
        dict(type='text', size=30, h=90, fn=lambda S: f"组数 `n // k = {S['n'] // S['k']}`：每个元素至多出现这么多次" if 'n' in S else ''),
    ],
    watch=['n', 'k', 'v'],
    captions={
        'if n % k': '`{n} % {k} != 0`？：不是 `k` 的倍数就一定有剩余 → ' + '本例 `{n} % {k} = {n % k}`，继续',
        'cnt = {}': '`cnt` 用哈希表统计每个元素的次数',
        'for v in nums': '取下一个元素 `v = {v}`',
        'cnt[v] = cnt.get': '`{v}` 出现了 `{cnt[v]}` 次',
        'if cnt[v] > n // k': lambda S, B, r: f'`cnt[{S.v}] = {S.cnt[S.v]}` 对比组数 `n // k = {S.n // S.k}` → ' + ('==鸽笼原理：必有一组出现两个相同的，返回 False==' if S.cnt[S.v] > S.n // S.k else '没超，继续'),
        'return True': '两个条件都满足，按排序依次分配即可 → ==True==',
    },
    cards=dict(
        one_liner='鸽笼原理：同一元素出现次数不能超过组数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `nums` 分成若干组，每组恰好 `k` 个==互不相同==的元素，所有元素都要用上',
                 '判断能否做到',
                 f'示例：`nums={NUMS}`，`k={K}` → `True`'],
        quote='根据鸽笼原理，单个元素出现的次数也不能大于n // k，否则必然有至少一组中有两个相同的元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['条件一：总数 `n` 是 `k` 的倍数，组数为 `n // k`',
              '条件二：每个元素出现次数 ≤ 组数（鸽笼原理）',
              '两条件够用：把元素排序后依次发到各组，同一元素不会进同一组'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：别漏掉 `n % k != 0` 的判断',
                 '充分性靠构造：排序后按轮流分配',
                 '对比灵神：灵神用数组计数并提前把 `n` 改成 `n//k`；yiduobo 用哈希表，循环里算 `n // k`'],
    ),
)
