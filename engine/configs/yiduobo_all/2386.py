def _info(S):
    if 'heap' not in S:
        return '先把 0 剔掉（每个 0 让每个和翻倍），负数取相反数，只剩「减去一个正数」'
    t = f"最大和 `s = {S['s']}`；堆里存 `(-和, 下一个可用下标)`，下面显示的是真实的和（大根）"
    if 'now' in S and S.get('_line', 0) >= 34:
        t = f"刚弹出的和 `{-S['now']}`：它占了 `same_cnt = {S['same_cnt']}` 个名次（0 带来的重复）→ 还剩 `k = {S['k']}`"
    return t


CONFIG = dict(
    num=2386, title='找出数组的第 K 大和', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='从最大和往下构造 + 堆（零的重复数）',
    tags=['常用数据结构', '难度分 2648'],
    code='''
class Solution(object):
    def kSum(self, nums, k):

        non_zero_list = []
        zero_cnt = 0
        s = 0
        for num in nums:
            if num > 0:
                non_zero_list.append(num)
                s += num
            elif num < 0:
                non_zero_list.append(-num)
            else:
                zero_cnt += 1
        
        non_zero_list.sort()

        same_cnt = 1
        for _ in range(zero_cnt):
            same_cnt += same_cnt
            if same_cnt >= k:
                break

        k -= same_cnt
        heap = [[-s, 0]]
        while k > 0:
            now, pos = heapq.heappop(heap)
            if pos < len(non_zero_list):
                heapq.heappush(heap, [now + non_zero_list[pos], pos + 1])
                
                if pos > 0:
                    heapq.heappush(heap, [now - non_zero_list[pos - 1] + non_zero_list[pos], pos + 1])
        
            k -= same_cnt

        return -heap[0][0]
''',
    call='Solution().kSum([2, 4, -2, 0], 7)',
    expect=2,
    views=[
        dict(type='array', var='non_zero_list', label='non_zero_list：非零数取绝对值后排序', h=120, cell=80,
             color=lambda S, i, v: ('blue' if i == S.get('pos') else 'pink' if i == S.get('pos', 0) - 1 else None) if 'now' in S else None),
        dict(type='heap', var='heap', h=240, fmt=lambda x: f'{-x[0]}|{x[1]}'),
        dict(type='text', fn=_info, size=26, h=110),
    ],
    watch=[('s', 's', 'green'), 'zero_cnt', 'same_cnt', 'k', 'now', 'pos'],
    skip=['for num in nums', 'if num > 0', 'elif num < 0', 'else:', 'non_zero_list.append(num)', 'non_zero_list.append(-num)', 'while k > 0', 'if pos < len', 'if pos > 0', 'for _ in range(zero_cnt)'],
    captions={
        's += num': '正数 `{num}` 全选：`s` = {s}（最大和）',
        'zero_cnt += 1': '遇到 0：不改变和，只记数 `zero_cnt = {zero_cnt}`',
        'non_zero_list.sort()': '非零数排好序 `{non_zero_list}`：负数已取相反数，之后每一步都是「减去一个数」',
        'same_cnt += same_cnt': '每个 0 可选可不选 → 每个和重复出现 `{same_cnt}` 次',
        'if same_cnt >= k': lambda S, B, r: (f'`same_cnt = {S.same_cnt} ≥ k = {S.k}`：最大的和重复次数已经够 k 次，不用再翻倍了' if S.same_cnt >= S.k
                                              else f'`same_cnt = {S.same_cnt} < k = {S.k}`，继续'),
        24: '最大和（连同 0 的各种选法）占掉前 `{same_cnt}` 个名次 → `k = {k}`',
        'heap = [[-s, 0]]': '堆里放 `[-s, 0]`：Python 是小根堆，取负就变成大根；下一个可用的下标是 `0`',
        'heapq.heappop(heap)': '弹出最大的和 `{-now}`，它下次可以「减去」的下标是 `pos = {pos}`',
        'heapq.heappush(heap, [now + non_zero_list[pos]': '想继续往下构造：再==减去== `{non_zero_list[pos]}` → 新和 `{-now} − {non_zero_list[pos]} = {-(now + non_zero_list[pos])}`，下标 {pos + 1}',
        'heapq.heappush(heap, [now - non_zero_list[pos - 1]': '或者把上次减去的 `{non_zero_list[pos - 1]}` ==换成== `{non_zero_list[pos]}`：新和 `{-now} + {non_zero_list[pos - 1]} − {non_zero_list[pos]} = {-(now - non_zero_list[pos - 1] + non_zero_list[pos])}`',
        34: '刚弹出的和占了 `{same_cnt}` 个名次 → `k = {k}`' ,
        'return -heap[0][0]': '`k ≤ 0`：此时堆顶就是第 k 大的和 =={-heap[0][0]}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='从最大和出发，用堆一个个往下数，0 当作重复倍数',
        complexity='时间 `O(n log n + k log k)`，空间 `O(k)`',
        problem=['任选 `nums` 的子序列求和（空序列和为 0），求第 `k` 大的和',
                 '`n` 很大，但 `k` 不超过 2000',
                 '本视频：`[2,4,-2,0], k=7` → `2`'],
        quote='题目中n非常大，处理起来会比较麻烦，但是k相对是比较小的，那么不妨从最大的组合开始逐个向下找，直到找到第k大和为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['最大和 = 所有正数之和；负数取相反数后，每次操作都是「从当前和减去一个数」',
              '为了不重复：规定每次只能减比上一次下标更大的数，用堆记录 `(和, 下一个下标)`',
              '0 单独处理：有 `cnt` 个 0 时，每个和都重复 `2^cnt` 次，每次出堆扣 `2^cnt` 个名次'],
        summary=['堆里存相反数，小根堆就当大根堆用',
                 '一个和出堆后，派生两个：再减一个 `nums[pos]`；或把上一次减的 `nums[pos-1]` 换成 `nums[pos]`',
                 '`same_cnt` 翻倍时遇到 `≥ k` 就提前停，避免 `2^zero_cnt` 溢出',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神把负数取绝对值后转成「第 k 小的减数和」；yiduobo 思路相同，但单独拆出 0 的倍数'],
    ),
)
