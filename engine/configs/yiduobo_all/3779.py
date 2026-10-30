CONFIG = dict(
    num=3779, title='得到互不相同元素的最少操作次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='倒序找最后一个重复元素',
    tags=['难度分 1444'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        vis = set()
        p = -1
        for index in range(len(nums) - 1, -1, -1):
            if nums[index] in vis:
                p = index
                break
            else:
                vis.add(nums[index])
        
        if p == -1:
            return 0
        
        return p // 3 + 1
''',
    call='Solution().minOperations([5, 1, 2, 3, 3, 8, 9])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue', 'p': 'pink'}, h=260,
             color=lambda S, i, v: 'green' if 'index' in S and i > S['index'] else None, label='nums（绿色 = 倒着看过的）'),
        dict(type='set', var='vis', fmt=lambda x: str(x), h=160),
        dict(type='text', fn=lambda S: (f'要移除 `nums[0..{S["p"]}]` 共 `{S["p"]+1}` 个，每次 3 个 → `{S["p"]} // 3 + 1 = {S["p"]//3+1}` 次') if S.get('p', -1) >= 0 else '', size=28, h=90),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('vis', 'sorted(vis)', 'cyan')],
    captions={
        'vis = set()': '`vis` 记录从后往前已经见过的数',
        'p = -1': '`p` 记最后一个重复元素的下标，`-1` 表示没有重复',
        'for index in': '倒着看 `nums[{index}] = {nums[index]}`',
        'if nums[index] in vis': '`{nums[index]}` 在 `vis` 里吗？{"在：它是重复元素" if nums[index] in vis else "不在：后面没有和它相同的"}',
        'p = index': '找到了：`p = {p}`，`nums[0..{p}]` 必须全部移除',
        'break': '更靠前的不用再看，操作数只由最靠后的重复元素决定',
        'vis.add': '`{nums[index]}` 加入 `vis`',
        'if p == -1': '`p = {p}`：{"一个重复都没有" if p == -1 else "存在重复元素"}',
        'return 0': '数组本来就互不相同，返回 `0`',
        'return p // 3': '移除 `p + 1 = {p+1}` 个元素，每次 3 个：`{p} // 3 + 1` = =={ret}==',
    },
    cards=dict(
        one_liner='操作只由「最靠后的重复元素」的位置决定',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次操作移除前 3 个元素（不足 3 个就全移除）',
                 '重复操作，直到数组为空或没有重复元素',
                 '求操作次数。本视频：`[5,1,2,3,3,8,9]` → `2`'],
        quote='可以统一理解成，将最后一个重复元素从数组中移除后，操作就停止了。',
        quote_src='—— yiduobo 题解原文',
        idea=['空数组也无重复，所以停止条件统一成「重复元素都被移除」',
              '从后往前扫，第一个在 `vis` 里的下标 `p` 就是最后一个重复元素',
              '要移除 `p + 1` 个，每次 3 个，次数 `p // 3 + 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：必须倒着扫，正着扫找到的是第一个重复',
                 '没有重复时 `p = -1`，答案为 `0`',
                 '本题与 3396 相同，灵神题解指向 3396'],
    ),
)
