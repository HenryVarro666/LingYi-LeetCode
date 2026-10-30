def _txt(S):
    if 'q' not in S or 'l' not in S:
        return '`f[i]` = 以 `nums[i]` 结尾的最大子序列和；`q[l:]` 是 f 递减的候选'
    q, l = S['q'], S['l']
    if l >= len(q):
        return '候选队列为空：只能自己单独作为子序列'
    return f"候选 `q[l:] = {q[l:]}`，队首 `q[{l}] = {q[l]}` 的 f 最大 = {S['f'][q[l]]}"


CONFIG = dict(
    num=1425, title='带限制的子序列和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='单调递减队列优化 DP',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def constrainedSubsetSum(self, nums, k):

        q = []
        l = r = 0
        res = -10000
        f = []
        for index, num in enumerate(nums):
            while l < r and index - q[l] > k:
                l += 1
            
            f.append(num)
            if r > l:
                f[-1] += f[q[l]]
            res = max(res, f[-1])
            if f[-1] > 0:
                while r > l and f[q[-1]] <= f[-1]:
                    q.pop()
                    r -= 1
        
                q.append(index)
                r += 1

        return res
''',
    call='Solution().constrainedSubsetSum([10,-2,-10,-5,20], 2)',
    expect=23,
    skip=['f = []'],
    views=[
        dict(type='array', var='nums', label='nums', h=190, cell=84, pointers={'index': 'blue'}),
        dict(type='array', var='f', label='f（以 nums[i] 结尾的最大和，逐个追加）', h=130, cell=84),
        dict(type='array', var='q', label='q（候选位置，从 l 开始有效）', h=190, cell=84,
             pointers={'l': 'pink'}, window=('l', 'r - 1'),
             dim=lambda S, i, v: i < S.get('l', 0)),
        dict(type='text', fn=_txt, size=24, h=50),
    ],
    watch=[('index', 'index', 'blue'), ('l', 'l', 'pink'), ('r', 'r', 'cyan'), 'k', ('res', 'res', 'green')],
    captions={
        'q = []': '`q` 存候选位置（f 值递减）',
        'l = r = 0': '`l` 是队首、`r` 是队尾后一格：有效候选是 `q[l:r]`',
        'res = -10000': '`res` 记录答案，初始为很小的数',
        'for index, num in enumerate': lambda S, B, r: ('全部位置处理完' if S.get('index') == B.get('index') else f'`index = {S.index}`，`num = {S.num}`'),
        'while l < r and index': lambda S, B, r: (
            f'`index - q[l] = {S.index - S.q[S.l]} > k = {S.k}`：队首距离太远，不能再接 → ==过期=='
            if S.l < S.r and S.index - S.q[S.l] > S.k
            else ('队列为空' if S.l >= S.r else f'`index - q[l] = {S.index - S.q[S.l]} ≤ k = {S.k}`：队首仍在范围内')),
        'l += 1': '队首过期，`l` → {l}',
        'f.append(num)': '先让 `nums[{index}]` 单独成为子序列：`f[{index}] = {num}`',
        'if r > l:': lambda S, B, r: ('队列非空，看看要不要接在队首后面' if S.r > S.l else '队列空，没有可接的前驱'),
        'f[-1] += f[q[l]]': '队首 f 最大（{f[q[l]]} > 0）：接上它，`f[{index}] = {num} + {f[q[l]]}` = =={f[-1]}==',
        'res = max(res': '`res = max({B.res}, {f[-1]})` = =={res}==',
        'if f[-1] > 0': lambda S, B, r: (f'`f[{S.index}] = {S.f[-1]} > 0`：对后面有帮助 → 要入队' if S.f[-1] > 0
                                         else f'`f[{S.index}] = {S.f[-1]} ≤ 0`：接上它只会变小 → ==不入队=='),
        'while r > l and f[q[-1]]': lambda S, B, r: (
            f'`f[{S.q[-1]}] = {S.f[S.q[-1]]} ≤ f[{S.index}] = {S.f[-1]}`：更早又不更大 → ==淘汰==，弹出队尾'
            if S.r > S.l and S.f[S.q[-1]] <= S.f[-1]
            else '队尾比它大（或队列空），停止弹出'),
        'q.pop()': '弹出队尾',
        'r -= 1': '`r` → {r}',
        'q.append(index)': '`index = {index}` 入队：`q = {q}`',
        'r += 1': '`r` → {r}',
        'return res': '最大的受限子序列和 =={ret}==',
    },
    cards=dict(
        one_liner='f 取前 k 个里的最大正值，队列里只留又晚又大的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和整数 `k`，选一个非空子序列',
                 '子序列里相邻两个数的下标差必须 `<= k`',
                 '求这样的子序列的最大和',
                 '示例：`[10,-2,-10,-5,20]`，`k = 2` → `23`'],
        quote='若存在一组j1和j2，满足j1 < j2且f[j1] <= f[j2]，那么对于后续的计算，我们是不可能再用到f[j1]来更新答案的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` = 以 `nums[i]` 结尾的最大和：自己单独一个，或接在前 k 个里最大的 `f[j]` 后面（只有它为正才接）',
              '前 k 个取最大：`j1 < j2` 且 `f[j1] <= f[j2]`，j1 永远没用',
              '队列里 f 递减，队首最大；过期就右移 `l`；`f <= 0` 的位置根本不入队'],
        summary=['时间 `O(n)`，每个位置最多入队、出队一次；暴力是 `O(nk)`',
                 '`f[i]` 初始化为 `nums[i]`：可以什么都不接',
                 '只让 `f > 0` 的位置入队：接上负数前驱只会更小',
                 '答案是所有 `f[i]` 的最大值，不是 `f[n-1]`',
                 '题解还提到可以用堆代替队列，但要处理过期，单调队列更简洁'],
    ),
)
