CONFIG = dict(
    num=3763, title='Maximum Total Sum With Threshold Constraints', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 最大堆', tags=['贪心', '堆'],
    code='''
class Solution(object):
    def maxSum(self, nums, threshold):
        
        info = sorted(zip(threshold, nums))
        heap = []
        
        res = 0
        p = 0
        for step in range(1, len(nums) + 1):
            while p < len(info) and info[p][0] == step:
                heapq.heappush(heap, -info[p][1])
                p += 1
            
            if not heap:
                break
            else:
                res -= heapq.heappop(heap)
        
        return res
''',
    call='Solution().maxSum([3,9,4,7,5,2], [1,2,2,3,5,9])',
    expect=28,
    views=[
        dict(type='array', var='info', pointers={'p': 'blue'}, label='info = (threshold, nums) 按 threshold 排序', cell=110, h=250,
             color=lambda S, i, v: 'green' if 'p' in S and i < S['p'] else None),
        dict(type='heap', var='heap', fmt=lambda x: str(-x), h=220),
        dict(type='text', fn=lambda S: f"step = ==%s==：能用的下标 threshold ≤ step，累计 `res = %s`" % (S['step'], S['res']) if 'step' in S else '', h=60),
    ],
    watch=['step', 'p', ('res', 'res', 'green')],
    captions={
        'info = sorted': '把 nums 和 threshold 合并，按 threshold 从小到大排序：`{info}`',
        'heap = []': '`heap` 装“当前已解锁”的 nums（取负数，用最小堆模拟最大堆）',
        'p = 0': '`p` 指向 info 里下一个还没解锁的位置',
        'for step': '第 `{step}` 轮：threshold ≤ {step} 的下标都可以选',
        'while p < len': lambda S, B, r: (f'`info[{S.p}][0] = {S.info[S.p][0]}` 等于 step `{S.step}` → 解锁它' if S.p < len(S.info) and S.info[S.p][0] == S.step
                                           else f'没有 threshold 恰好等于 `{S.step}` 的新下标，不再解锁'),
        'heapq.heappush': '把 `nums = {info[p][1]}` 加入候选堆（存负数 `{-info[p][1]}`）',
        'p += 1': '`p` 后移到 {p}，看下一个',
        'if not heap': lambda S, B, r: ('堆为空：这一轮没有下标可选 → 直接结束' if not S.heap else f'堆里还有 `{len(S.heap)}` 个候选，继续'),
        'break': '再往后 step 只会更大但没有新解锁，已无法继续 → 跳出循环',
        'res -= heapq.heappop': '贪心：每轮取候选里 ==最大的 nums==（堆顶 `{-heap_top}`）→ `res = {res}`'.replace('{-heap_top}', '{res - B.res}'),
        'return res': '最大总和 `{res}`',
    },
    cards=dict(
        one_liner='step 一增大就解锁新下标，每轮从候选里挑最大的 nums',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['两个长度为 `n` 的数组 `nums`、`threshold`，从 `step = 1` 开始',
                 '每轮选一个没选过、且 `threshold[index] <= step` 的下标，答案加上 `nums[index]`，`step += 1`',
                 '无法再选时停止，求最大总和',
                 '本视频：`nums=[3,9,4,7,5,2]`，`threshold=[1,2,2,3,5,9]` → `28`'],
        quote='每一轮的候选下标，都相当于在上一轮选择后剩余的候选下标的基础上，额外添加所有threshold恰好等于step的下标，而为了使得最终答案最大，每一轮都应该选择候选下标种对应的nums最大的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['候选集只增不减：step 变大，新解锁的下标加进来',
              '每轮贪心取候选里最大的 nums，用==堆==维护动态最大值',
              '先按 threshold 排序，用指针 `p` 单调地把刚好等于 step 的下标推进堆'],
        summary=['时间 `O(n log n)`（排序 + 堆），空间 `O(n)`',
                 'Python 只有最小堆：存 `-nums`，弹出时用 `res -= ...`',
                 '堆空就 `break`：之后的 step 也没有新下标可解锁（info 中不会有更小的未处理项）',
                 '`while` 要用 `== step` 且循环推进 `p`，同一 threshold 可能有多个下标'],
    ),
)
