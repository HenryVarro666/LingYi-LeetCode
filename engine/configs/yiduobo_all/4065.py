CONFIG = dict(
    num=4065, title='移除不同值重排数组', difficulty='Easy', category='模拟',
    author='yiduobo', technique='下标数组计数 + 按题意模拟', tags=[],
    code='''
class Solution(object):
    def rearrangeArray(self, nums):
        
        cnt = [0] * 101
        for v in nums:
            cnt[v] += 1
        
        res = []
        while len(res) < len(nums):
            for v in range(1, 101):
                if cnt[v] > 0:
                    res.append(v)
                    cnt[v] -= 1
        
        return res
''',
    call='Solution().rearrangeArray([3,1,3,2,1,3])',
    expect=[1, 2, 3, 1, 3, 3],
    views=[
        dict(type='array', var='nums', label='nums', pointers={}, h=150),
        dict(type='array', var=lambda S: S['cnt'][:8], label='cnt 前 8 格（cnt 共 101 格，后面全是 0）',
             pointers={'v': 'blue'}, h=220, color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='array', var='res', label='res', h=170),
    ],
    skip=['for v in range(1, 101)', 'if cnt[v] > 0'],
    watch=[('v', 'v', 'blue'), ('len(res)', 'len(res)', 'green')],
    captions={
        'cnt[v] += 1': '`cnt[{v}]` 记下 {v} 的个数 → =={cnt[v]}==',
        'while len(res) < len(nums)': lambda S, B, r: (f'`res` 长 {len(S.res)} < `nums` 长 {len(S.nums)}：还没取完，再来一轮' if len(S.res) < len(S.nums) else f'`res` 长 {len(S.res)} = `nums` 长 {len(S.nums)}：取完了，退出循环'),
        'for v in range(1, 101)': '这一轮从 1 扫到 100，只在 `cnt[v] > 0` 时动手',
        'if cnt[v] > 0': lambda S, B, r: (f'`cnt[{S.v}] > 0`：{S.v} 还没移除完 → 本轮取一个' if S.cnt[S.v] > 0
                                          else f'`cnt[{S.v}] = 0`：没有 {S.v}，跳过'),
        'res.append(v)': '从 1 往上扫到 `v = {v}`：`cnt[{v}] > 0`（中间的 0 都跳过）→ 追加到 `res` → {res}',
        'cnt[v] -= 1': '移除一个：`cnt[{v}]` → =={cnt[v]}==',
        'return res': '`res` 长度等于 `nums`，返回 `{res}`',
    },
    cards=dict(
        one_liner='值域只有 100，直接开下标数组，按题意一轮轮模拟',
        complexity='时间 `O(100 × n)`，空间 `O(100)`',
        problem=['每轮把 `nums` 中每种值各移除一个，升序追加到 `ans`，直到 `nums` 为空',
                 '示例：`[3,1,3,2,1,3]` → `[1,2,3,1,3,3]`'],
        quote='题目中nums的长度以及其中元素的大小都不大，因此可以使用一个下标数组cnt记录每种元素出现的次数，然后按照题目描述不断执行操作，直到ans的长度等于nums的长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['每一轮都从 1 遍历到 100：对当前的 `v`，`cnt[v] > 0` 就加入 `res` 并减一',
              '值从小到大遍历，所以每轮追加的内容自然升序'],
        summary=['时间 `O(100n)`（轮数 ≤ n），空间 `O(100)`',
                 '值域从 1 开始，`cnt` 开 101 格，`range(1, 101)` 不要写成 `range(1, 100)`',
                 '视频只画了 `cnt` 前 8 格，其余全为 0；第一轮之后每轮都要重新扫满 100 个值',
                 '对比灵神：灵神用 `max(nums) + 1` 开数组，只扫到最大值'],
    ),
)
