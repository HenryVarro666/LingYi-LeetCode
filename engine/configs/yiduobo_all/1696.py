def _txt(S):
    if 'stack' not in S or 'l' not in S:
        return '`f[i]` = 跳到 i 的最大得分；`stack[l:]` 是还能用的候选位置，f 递减'
    st, l = S['stack'], S['l']
    if l >= len(st):
        return '候选队列已空'
    return f"候选 `stack[l:] = {st[l:]}`，队首 `stack[{l}] = {st[l]}` 的 f 最大"


CONFIG = dict(
    num=1696, title='跳跃游戏 VI', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='单调递减队列（list + 头指针 l）',
    tags=['灵神题单·动态规划', '难度分 1954'],
    code='''
class Solution(object):
    def maxResult(self, nums, k):

        stack = [0]
        f = [nums[0]]
        l = 0

        for index in range(1, len(nums)):
            num = nums[index]
            while l < len(stack) and index - stack[l] > k:
                l += 1
            
            f.append(f[-1] + num)
            if l < len(stack):
                f[-1] = max(f[-1], f[stack[l]] + num)
            
            while len(stack) > l and f[stack[-1]] <= f[-1]:
                stack.pop()
            
            stack.append(index)
        
        return f[-1]
''',
    call='Solution().maxResult([1,-1,-2,4,-7,3], 2)',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums', h=190, cell=84, pointers={'index': 'blue'}),
        dict(type='array', var='f', label='f（跳到每个位置的最大得分，逐个追加）', h=130, cell=84),
        dict(type='array', var='stack', label='stack（候选位置，从 l 开始有效）', h=190, cell=84,
             pointers={'l': 'pink'}, window=('l', 'len(stack) - 1'),
             dim=lambda S, i, v: i < S.get('l', 0)),
        dict(type='text', fn=_txt, size=24, h=50),
    ],
    watch=[('index', 'index', 'blue'), ('l', 'l', 'pink'), 'k', ('f[-1]', lambda S: S['f'][-1] if S.get('f') else None, 'green')],
    skip=['num = nums[index]'],
    captions={
        'stack = [0]': '`stack` 存候选位置，先放起点 `0`',
        'f = [nums[0]]': '起点得分 `f[0] = {nums[0]}`',
        'l = 0': '`l` 是队首指针：不真的删除，只是右移',
        'for index in range': lambda S, B, r: ('全部位置算完' if S.get('index') == B.get('index') else f'`index = {S.index}`：算 `f[{S.index}]`'),
        'while l < len(stack) and': lambda S, B, r: (
            f'`index - stack[l] = {S.index - S.stack[S.l]} > k = {S.k}`：队首跳不到这里 → ==左边界过期=='
            if S.l < len(S.stack) and S.index - S.stack[S.l] > S.k
            else ('队列空了' if S.l >= len(S.stack) else f'`index - stack[l] = {S.index - S.stack[S.l]} ≤ k = {S.k}`：队首仍可用')),
        'l += 1': '队首过期，`l` → {l}',
        'f.append(f[-1] + num)': '先用 `f[index-1] + num` 作候选：`f[{index}] = {f[-1]}`',
        'if l < len(stack):': lambda S, B, r: ('队列里还有候选，可以从队首转移' if S.l < len(S.stack) else '队列空，只能从上一格来'),
        'f[-1] = max(': '队首 f 最大：`max(上一个, f[{stack[l]}] + {num})` → `f[{index}] = {f[-1]}`',
        'while len(stack) > l and': lambda S, B, r: (
            f'`f[{S.stack[-1]}] = {S.f[S.stack[-1]]} ≤ f[{S.index}] = {S.f[-1]}`：位置更靠前又不更大 → ==没用了，弹出=='
            if len(S.stack) > S.l and S.f[S.stack[-1]] <= S.f[-1]
            else '队尾比新值大（或没有候选），停止弹出'),
        'stack.pop()': '弹出队尾：`stack = {stack}`',
        'stack.append(index)': '`index = {index}` 入队：`stack = {stack}`',
        'return f[-1]': '到达最后位置的最大得分 =={ret}==',
    },
    cards=dict(
        one_liner='区间最大值：留下又晚又大的位置，其余淘汰',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从下标 0 出发，每次最多往前跳 `k` 步，到最后一个位置',
                 '得分是经过的数字之和，求最大值',
                 '示例：`[1,-1,-2,4,-7,3]`，`k = 2` → `7`'],
        quote='对于两个位置j和k，不妨设j < k且f[j] <= f[k]，那么对于任意大于k的位置i：……此时没有必要继续保留j了',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i] = max(f[j]) + nums[i]`，`j` 在 `[i-k, i-1]`，直接枚举是 `O(n^2)`',
              '`j < k` 且 `f[j] <= f[k]`：k 更晚过期、值又不小，j 永远不用',
              '队列里 f 单调递减，队首最大；队首过期就右移 `l`'],
        summary=['时间 `O(n)`：每个位置最多入队、出队一次',
                 '用列表加头指针 `l` 代替 deque，弹队首只是 `l += 1`',
                 '`stack` 前面 `l` 个是已过期的残留，没有真的删除；易错：先弹过期队首再取最大值；入队前弹掉 `f` 不大于新值的队尾',
                 '代码中 `max(f[-1], ...)` 先用上一格兜底，队列空时也有值',
                 '对比灵神：他直接取 `q[0]`，靠 `k >= 1` 保证队列非空'],
    ),
)
