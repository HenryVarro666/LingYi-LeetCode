CONFIG = dict(
    num=1437, title='是否所有 1 都至少相隔 k 个元素', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟扫描 · 计数距离', tags=[],
    code='''
class Solution(object):
    def kLengthApart(self, nums, k):

        cnt = k
        for index, num in enumerate(nums):
            if num == 1:
                if cnt < k:
                    return False
                cnt = 0
            else:
                cnt += 1
        
        return True
''',
    call='Solution().kLengthApart([1,0,0,1,0,0,0,1,0,1], 2)',
    expect=False,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=260,
             color=lambda S, i, v: ('yellow' if i == S.get('index') and v == 1 else 'blue' if i == S.get('index') else None) if 'index' in S else None),
        dict(type='text', fn=lambda S: f"距离上一个 1 已经隔了 `cnt = {S['cnt']}` 个 0，要求 `>= {S['k']}`" if 'cnt' in S else '', size=30),
    ],
    watch=[('index', 'index', 'blue'), 'num', ('cnt', 'cnt', 'orange'), 'k'],
    captions={
        'cnt = k': '`cnt` 是距上一个 1 的间隔数；==初始设为 k==，让第一个 1 直接通过',
        'if num == 1': lambda S, B, r: (f'`nums[{S.index}] = 1`，要看它离上一个 1 有多远' if S.num == 1 else f'`nums[{S.index}] = 0`，不是 1'),
        'if cnt < k': lambda S, B, r: (f'`cnt = {S.cnt} < k = {S.k}`：间隔不够 → ==返回 False==' if S.cnt < S.k else f'`cnt = {S.cnt} >= k = {S.k}`：间隔够了'),
        'return False': '出现间隔小于 `k` 的两个 1，直接 `False`',
        'cnt = 0': '遇到 1，间隔计数清零，重新数',
        'cnt += 1': '又隔了一个 0：`cnt` → {cnt}',
        'return True': '所有 1 的间隔都不小于 `k` → `True`',
    },
    cards=dict(
        one_liner='一趟扫描，数每个 1 和上一个 1 之间隔了几个 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['0/1 数组 `nums` 与整数 `k`，所有 1 是否都至少相隔 `k` 个元素',
                 '本视频：`[1,0,0,1,0,0,0,1,0,1]`，`k = 2`'],
        quote='直接一趟扫描，计算每个1距离上一个1出现的距离，若其中有小于k的，那么就返回false，否则返回true。',
        quote_src='—— yiduobo 题解原文',
        idea=['遇到 0，`cnt` 加 1；遇到 1，先检查 `cnt < k`，再清零',
              '`cnt` 初始为 `k`，相当于第一个 1 前面已经有足够的空位'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`cnt` 数的是两个 1 之间的 0 的个数，所以和 `k` 直接比较',
                 '初始值必须是 `k`（不能是 0），否则开头的 1 会被误判',
                 '对比灵神：灵神记下标差，yiduobo 数间隔个数；原文为 Python 2 风格，本题无需改动'],
    ),
)
