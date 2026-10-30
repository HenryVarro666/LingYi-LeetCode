CONFIG = dict(
    num=2913, title='子数组不同元素数目的平方和 I', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='枚举左端点 + 集合去重',
    tags=[],
    code='''
class Solution(object):
    def sumCounts(self, nums):

        n = len(nums)
        res = 0
        for i in range(n):
            num_set = set()
            for j in range(i, n):
                num_set.add(nums[j])
                res += len(num_set) ** 2
        
        return res
''',
    call='Solution().sumCounts([1,2,1,3])',
    expect=38,
    views=[
        dict(type='array', var='nums', label='nums（蓝色 = 当前子数组 nums[i..j]）', pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'), h=200,
             color=lambda S, i, v: 'pink' if S.get('j') == i and S['_line'] >= 9 else None),
        dict(type='set', var='num_set', label='num_set（当前子数组里的不同元素）', h=130),
        dict(type='text', size=30, h=60, fn=lambda S: f"不同计数 `{len(S['num_set'])}`，平方 =={len(S['num_set'])**2}==，累计 `res` = =={S['res']}==" if 'num_set' in S and S['_line'] >= 10 else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'num_set = set()': '换新的左端点 `i = {i}`：集合清空，从 `nums[{i}]` 开始向右扩',
        'num_set.add': '把右端点 `nums[{j}] = {nums[j]}` 加入集合；已存在就不变 → 集合 `{sorted(num_set)}`',
        'res += len': '`nums[{i}..{j}]` 有 `{len(num_set)}` 个不同元素 → 加 `{len(num_set)}^2 = {len(num_set)**2}`，`res` = =={res}==',
        'return res': '所有子数组都枚举完，返回 =={res}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='数据小，枚举左端点逐步右扩，集合数不同元素',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['子数组的「不同计数」是里面不同值的个数',
                 '求所有子数组不同计数的平方和',
                 '示例：`[1,2,1]` → `15`；本视频演示 `[1,2,1,3]` → `38`'],
        quote='题目的数据规模比较小，完全可以先枚举子数组的左边界i，然后从i开始向右逐步扩展子数组，同时使用一个集合记录当前子数组中的元素。',
        quote_src='—— yiduobo 题解',
        idea=['固定左端点 i，右端点 j 往右走，每走一步子数组多一个数',
              '用集合记元素，`len(集合)` 就是当前的不同计数',
              '每一步把 `len(集合) ** 2` 累加到答案'],
        summary=['时间 `O(n^2)`，`n ≤ 100` 完全够用',
                 '==换左端点时集合要重新建==，不能沿用上一轮',
                 '先加入 `nums[j]` 再累加平方，别漏掉长度为 1 的子数组',
                 '更大数据的 II 就要用线段树之类的做法'],
    ),
)
