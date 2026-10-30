CONFIG = dict(
    num=2869, title='收集元素的最少操作次数', difficulty='Easy', category='模拟',
    author='yiduobo', technique='模拟 + 集合计数',
    tags=[],
    code='''
class Solution(object):
    def minOperations(self, nums, k):

        vis = set()
        res = 0
        while len(vis) < k:
            if nums[-1] <= k:
                vis.add(nums[-1])
            
            nums.pop()
            res += 1
        
        return res
''',
    call='Solution().minOperations([3,1,5,4,2], 2)',
    expect=4,
    views=[
        dict(type='text', size=28, fn=lambda S: f"集合大小 `{len(S['vis'])}`，还差 `{S['k'] - len(S['vis'])}` 个才集齐 1 ~ {S['k']}" if 'vis' in S else ''),
        dict(type='array', var='nums', label='nums（只剩没弹出的部分；最右边 = 下一个被弹出的）', h=200,
             color=lambda S, i, v: ('blue' if i == len(S['nums']) - 1 else None)),
        dict(type='set', var='vis', label='vis（收集到的 ≤ k 的元素）', h=200, fmt=lambda x: str(x)),
    ],
    watch=[('k', 'k'), ('len(vis)', 'len(vis)', 'green'), ('res', 'res', 'orange')],
    captions={
        'vis = set()': '`vis` 记录已经收集到的、`≤ k` 的不同元素',
        'res = 0': '`res` 记录弹出了几次',
        'while len(vis) < k': lambda S, B, r: (f'`len(vis) = {len(S.vis)}` < `k = {S.k}` → 还没集齐，继续弹'
                                               if len(S.vis) < S.k else f'`len(vis) = {len(S.vis)}` = `k = {S.k}` → ==1 到 {S.k} 都有了==，停止'),
        'if nums[-1] <= k': lambda S, B, r: (f'末尾元素 `{S.nums[-1]}` ≤ `{S.k}` → 是要收集的数' if S.nums[-1] <= S.k
                                             else f'末尾元素 `{S.nums[-1]}` > `{S.k}` → 用不上，直接丢掉'),
        'vis.add': '`{nums[-1]}` 加入集合，`vis = {vis}`',
        'nums.pop()': '弹出末尾元素，`nums` 变成 `{nums}`',
        'res += 1': '又操作了一次：`res` → =={res}==',
        'return res': '集齐 1 ~ `{k}`，一共弹出 =={ret}== 次',
    },
    cards=dict(
        one_liner='照题意从后往前弹，集合凑够 k 个就停',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['每次操作弹出数组最后一个元素', '求收集齐 `1, 2, …, k` 的最少操作次数',
                 '示例：`[3,1,5,4,2]`，`k = 2` → `4`'],
        quote='直接按照题目描述进行模拟，从后向前不断将数组的末尾元素弹出，并将小于等于k的元素加入到集合中。若某一时刻集合的大小等于k，说明里面恰好包含了1到k。',
        quote_src='—— yiduobo 题解原文',
        idea=['只有 `≤ k` 的数才可能是目标，其余弹掉不记',
              '集合去重，所以 `len(vis) == k` 就等价于 1 ~ k 全齐',
              '每弹一次 `res += 1`，齐了就返回'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '易错：必须先判断 `nums[-1] <= k` 再加入集合，否则大数会把集合撑大',
                 '代码会真的 `pop` 掉 `nums`，会修改输入数组',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神用位运算整数做集合，`O(1)` 空间；这里用 `set` 计数'],
    ),
)
