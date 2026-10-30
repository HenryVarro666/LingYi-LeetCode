CONFIG = dict(
    num=3551, title='数位和排序需要的最小交换次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='目标位置数组 · 沿环走',
    tags=['难度分 1507'],
    code='''
class Solution(object):
    def minSwaps(self, nums):

        n = len(nums)
        digits_sum = [0] * n
        for index, v in enumerate(nums):
            while v:
                digits_sum[index] += v % 10
                v //= 10

        target = [index for index in range(n)]
        target.sort(key=lambda d:(digits_sum[d], nums[d]))

        res = 0
        vis = [False] * n
        for index in range(n):
            if not vis[index]:
                vis[index] = True
                now = index
                while target[now] != index:
                    now = target[now]
                    vis[now] = True
                    res += 1

        return res
''',
    call='Solution().minSwaps([18, 43, 34, 16])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', cell=100, h=170, color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='array', var='digits_sum', label='digits_sum（每个数的数位和）', cell=100, h=170),
        dict(type='array', var='target', label='target[i]：nums[i] 排序后应在的下标', cell=100, h=170,
             color=lambda S, i, v: 'pink' if i == S.get('now') else None),
        dict(type='array', var='vis', label='vis（已走过的位置）', cell=100, h=170,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=['index', 'now', ('res', 'res', 'green')],
    captions={
        'digits_sum = [0] * n': '`digits_sum[i]` 用来存 `nums[i]` 的数位和',
        'for index, v in enumerate(nums)': '算 `nums[{index}] = {nums[index]}` 的数位和',
        'while v:': '`v = {v}`，{"还有数位，继续拆" if v else "拆完了"}',
        'digits_sum[index] += v % 10': '取个位 `{v % 10}`，累加：`digits_sum[{index}] = {digits_sum[index]}`',
        'v //= 10': '去掉个位，`v = {v}`',
        'target = [index': '`target` 先是下标 `0..n-1`：{target}',
        'target.sort': '下标按（数位和，数值）排序 → `target = {target}`：`target[i]` 是 `nums[i]` 排序后的位置',
        'res = 0': '`res` 累计交换次数',
        'vis = [False] * n': '`vis` 记录哪些位置已经被某个环走过',
        'for index in range(n)': '检查位置 `{index}`',
        'if not vis[index]': '位置 `{index}` {"还没走过 → 它是一个新环的起点" if not vis[index] else "走过了 → 跳过"}',
        'vis[index] = True': '标记起点 `{index}` 已走过',
        'now = index': '从 `{now}` 出发，沿着 `target` 走这个环',
        'while target[now] != index': '`target[{now}] = {target[now]}`：{"还没回到起点，继续走" if target[now] != index else "回到起点，环走完了"}',
        'now = target[now]': '走到 `{now}`，这个位置的数要换到那里',
        'vis[now] = True': '标记 `{now}` 已走过',
        'res += 1': '环里多走一步就多一次交换：`res = {res}`（环长 k 需 k−1 次）',
        'return res': '所有环走完，最少交换 ==`{res}`== 次',
    },
    skip=['v //= 10', 'vis[now] = True'],
    max_steps=90,
    cards=dict(
        one_liner='算出每个数的目标位置，沿「位置 → 目标」走环，环长 k 要 k−1 次',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['互不相同的正整数数组 `nums`，按数位和升序排，和相同则数值小的在前',
                 '每次可交换任意两个位置，求排好序的最少交换次数',
                 '示例：`[18,43,34,16]` → `2`',
                 '本视频：`nums = [18,43,34,16]` → `2`'],
        quote='对于当前遍历到的index，如果index刚好就位于target[index]，这种情况下就不需要进行交换了，直接跳过，否则就需要将其交换到target[index]……若这个交换路径的长度为k，那么需要的交换次数就是k - 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用模 10、除 10 算出每个数的数位和 `digits_sum`',
              '下标按（数位和，数值）排序得到 `target`：`nums[i]` 应放到下标 `target[i]`',
              '遍历每个未访问的位置，沿 `target` 走一圈，每多走一步 `res` 加一，不用真的交换'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：`target` 排序的第二关键字是 `nums[d]`，数位和相同按值小的在前',
                 '用 `vis` 标记走过的位置，每个环只统计一次',
                 '环长为 1（已在目标位置）时 `while` 不进入，`res` 不增加',
                 '原文本身可在 Python 3 运行，未做修改'],
    ),
)
