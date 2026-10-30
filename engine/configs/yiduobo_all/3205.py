CONFIG = dict(
    num=3205, title='最大数组跳跃得分 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='倒序扫描 · 后缀最大值链',
    tags=[],
    code='''
class Solution(object):
    def maxScore(self, nums):

        n = len(nums)
        p = n - 1
        res = 0

        for index in range(n - 2, 0, -1):
            if nums[index] > nums[p]:
                res += (p - index) * nums[p]
                p = index
        
        res += p * nums[p]
        return res
''',
    call='Solution().maxScore([4,5,2,8,9,1,3])',
    expect=42,
    skip=['n = len(nums)'],
    views=[
        dict(type='text', fn=lambda S: (f"`p = {S['p']}`：已确定的下一个落点，值 `{S['nums'][S['p']]}`" if 'p' in S else ''), size=28, h=60),
        dict(type='array', var='nums', label='nums（粉 = 落点 p，蓝 = 正在检查的 index）', cell=84,
             pointers={'p': 'pink', 'index': 'blue'}, h=260,
             color=lambda S, i, v: ('pink' if i == S.get('p') else 'blue' if i == S.get('index') else None) if 'p' in S else None),
        dict(type='text', fn=lambda S: f"累计得分 `res = {S['res']}`" if 'res' in S else '', size=30, h=60),
    ],
    watch=[('p', 'p', 'pink'), ('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'p = n - 1': '终点必须到达：先让落点 `p = {p}`（最后一个元素）',
        'res = 0': '`res` 累计得分',
        'for index': lambda S, B, r: (f'倒着看 `index = {S.index}`，`nums[{S.index}] = {S.nums[S.index]}`' if 'index' in S and S.get('index') != B.get('index')
                                      else '倒序遍历结束，只剩从 0 跳到 p 的一跳'),
        'if nums[index] > nums[p]': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]} > nums[{S.p}] = {S.nums[S.p]}`：它比落点大 → ==值得作为中继点=='
                                                      if S.nums[S.index] > S.nums[S.p]
                                                      else f'`nums[{S.index}] = {S.nums[S.index]} ≤ nums[{S.p}] = {S.nums[S.p]}`：不比落点大，直接跨过它'),
        'res += (p - index)': '从 `{index}` 跳到 `{p}`：`({p} − {index}) × nums[{p}] = {(p - index) * nums[p]}` → `res = {res}`',
        'p = index': '新的落点 `p = {p}`：它是后缀里目前的最大值',
        'res += p * nums[p]': '最后从下标 0 直接跳到 `p`：`{p} × nums[{p}] = {p * nums[p]}` → `res = {res}`',
        'return res': '最大得分 `{res}`',
    },
    cards=dict(
        one_liner='最大值必是落点，从后往前挑出递增的“后缀最大值”链',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['从下标 0 出发，每次从 `i` 跳到某个 `j > i`，得分 `(j - i) * nums[j]`',
                 '求跳到最后一个元素时的最大总得分',
                 '本视频：`[4,5,2,8,9,1,3]` → `42`'],
        quote='距离总和是一定的，那么为了得分最大，就应该尽量放大后续的nums[j]。……最大值nums[ma]是必然会被作为某次跳跃的终点。',
        quote_src='—— yiduobo 题解原文',
        idea=['若跳跃 p→q 越过了最大值 ma，改成 p→ma→q 得分更大，所以最大值必是落点',
              '从 0 出发，直接跳到 ma 优于经过中间点；ma 之后的部分是同样的子问题',
              '倒序扫描：遇到比当前落点大的就加入链，累加这一跳的得分'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环到 `index = 1` 为止：下标 0 是起点，不能当落点，最后单独加 `p * nums[p]`',
                 '得分用的是==落点的值== `nums[p]`，不是起点的值',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
