_cnt = {}


def _forcap(var, n, key):
    def f(S, B, r):
        c = _cnt.get(key, 0) + 1
        _cnt[key] = c
        if c > n:
            return '遍历完所有元素，退出循环'
        return f'第 {c} 个元素，取到 `{var} = {S.nums[c - 1]}`' 
    return f


CONFIG = dict(
    num=3397, title='执行操作后不同元素的最大数量', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 每个人尽量往左挪',
    tags=['灵神题单', '难度分 1687'],
    code='''
class Solution:
    def maxDistinctElements(self, nums: List[int], k: int) -> int:
        if k * 2 + 1 >= len(nums):
            return len(nums)

        nums.sort()
        ans = 0
        pre = -inf  # 记录每个人左边的人的位置
        for x in nums:
            x = min(max(x - k, pre + 1), x + k)
            if x > pre:
                ans += 1
                pre = x
        return ans
''',
    call='Solution().maxDistinctElements([4,4,4,4,4,5,9], 1)',
    expect=5,
    views=[
        dict(type='array', var='nums', h=190, label='nums（排序后）'),
        dict(type='text', h=130, fn=lambda S: ('左边的人移动后的位置 `pre = %s`；下一个人最理想的位置 `pre + 1` 是 ==%s==' % (S['pre'], S['pre'] + 1)) if 'pre' in S else ''),
        dict(type='text', h=130, fn=lambda S: ('已经得到 ==%d== 个互不相同的位置' % S['ans']) if 'ans' in S else ''),
    ],
    watch=['x', 'k', ('pre', 'pre', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'for x in nums': _forcap('x', 7, 'l'),
        'if k * 2 + 1': '一个数能变成 `[x-k, x+k]` 里 `2k+1 = {k*2+1}` 个值；这里 `{k*2+1} < n = {len(nums)}`，不能保证全不同，继续',
        'nums.sort': '排序：就像同学们按位置从左到右排成一排，从最左边的人开始安排',
        'pre = -inf': '`pre` 记录左边那个人移动后的位置，一开始左边没人，是 `-inf`',
        'x = min(max': '`x` 尽量往左挪但要紧挨着 `pre`：`min(max(x-k, pre+1), x+k)`，即让 `pre+1` 落进 `[x-k, x+k]`，越界就修正：`min(max({B.x}-{k}, {B.pre+1}), {B.x}+{k})` = `{x}`',
        'if x > pre': lambda S, B, r: (f'新位置 `{S.x}` > `pre = {S.pre}`：没和左边的人撞位置' if S.x > S.pre else f'新位置 `{S.x}` 没超过 `pre = {S.pre}`：这个人被迫和左边重复，不计数'),
        'ans += 1': '又多了一个不同的值：`ans` → {ans}',
        'pre = x': '更新 `pre = {pre}`：下一个人从 `{pre + 1}` 起放',
        'return ans': '最多有 =={ret}== 个不同元素',
    },
    max_steps=70,
    cards=dict(
        one_liner='排好队，每个人尽量往左挪，紧挨着左边的人',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每个元素可以加上一个 `[-k, k]` 内的整数，也可以不动',
                 '求操作后数组里 ==不同元素== 的最大数量',
                 '本视频：`[4,4,4,4,4,5,9]`、`k=1` → `5`'],
        quote='对于最靠左的同学 A，他需要尽量往左移动，给其他同学腾出位置。A 旁边的同学，可以紧挨着 A。依此类推。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `nums` 看成数轴上的同学，从最小的开始，尽量往左：`x-k`',
              '后面的人不能和左边重复，所以变成 `max(x-k, pre+1)`；又不能超过 `x+k`，再取 `min`',
              '新位置比 `pre` 大就是新的不同值，`ans` 加一；不然不计数、`pre` 不动'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '优化：若 `2k+1 >= n`，所有数都能互不相同，直接返回 `n`',
                 '没挪成功的人（`x <= pre`）不更新 `pre`',
                 '题解先给出不带优化的写法，视频演示的是带 `2k+1 >= n` 提前返回的优化版'],
    ),
)
