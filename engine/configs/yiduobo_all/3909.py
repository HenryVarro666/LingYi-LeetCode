def _peak(a):
    return a.index(max(a))


CONFIG = dict(
    num=3909, title='比较双调部分的和', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='先加递增段，再减递减段',
    code='''
class Solution(object):
    def compareBitonicSums(self, nums):
        
        n = len(nums)
        s = nums[0]
        p = 0
        while p + 1 < n and nums[p + 1] > nums[p]:
            p += 1
            s += nums[p]
        
        s -= nums[p]
        while p + 1 < n:
            p += 1
            s -= nums[p]
        
        if s > 0:
            return 0
        elif s < 0:
            return 1
        else:
            return -1
''',
    call='Solution().compareBitonicSums([2,4,7,9,6,3,1])',
    expect=0,
    views=[
        dict(type='text', size=32, fn=lambda S: (f"s = 递增部分和 − 已减去的递减部分 = ==​{S['s']}==" if 's' in S else '')),
        dict(type='array', var='nums', label='nums（p 先走上升段，再走下降段）', h=260, cell=100, pointers={'p': 'blue'},
             color=lambda S, i, v: None if 'p' not in S else ('green' if i <= S['p'] and S['_line'] <= 10 else 'pink' if i <= S['p'] and S['_line'] > 10 and i > _peak(S['nums']) else 'green' if i <= S['p'] else None)),
    ],
    watch=['p', ('s', 's', 'green'), 'n'],
    captions={
        's = nums[0]': '递增部分之和从 `nums[0] = {nums[0]}` 开始，`s = {s}`',
        'p = 0': '`p` 从下标 0 出发，向后找峰顶',
        'while p + 1 < n and': lambda S, B, r: (f'`nums[{S.p+1}] = {S.nums[S.p+1]} > nums[{S.p}] = {S.nums[S.p]}` → 仍在上升，继续' if S.p + 1 < S.n and S.nums[S.p+1] > S.nums[S.p] else (f'`p + 1 = {S.p+1}` 已到末尾，没有下降段' if S.p + 1 >= S.n else f'`nums[{S.p+1}] = {S.nums[S.p+1]} < nums[{S.p}] = {S.nums[S.p]}` → 上升结束，`p = {S.p}` 是峰顶')),
        'p += 1': '`p` 右移到 {p}',
        's += nums[p]': '`nums[{p}] = {nums[p]}` 属于递增部分：`s` → =={s}==',
        's -= nums[p]': lambda S, B, r: (f'峰顶 `{S.nums[S.p]}` 同时属于两部分，已加过，现在也要减一次：`s` → =={S.s}==' if S['_line'] == 11 else f'`nums[{S.p}] = {S.nums[S.p]}` 属于递减部分，从 `s` 里减掉 → =={S.s}=='),
        'if s > 0': '`s = {s}` > 0？ → ==递增部分更大==时返回 0',
        'elif s < 0': '`s = {s}` < 0？ → 递减部分更大时返回 1',
        'return': '`s = {s}`，返回 =={ret}==',
    },
    cards=dict(
        one_liner='先加上递增部分，再把递减部分全减掉，看差的正负',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['长度为 `n` 的双调数组：先递增到峰值，再递减',
                 '比较递增部分之和与递减部分之和',
                 '递增更大 → `0`，递减更大 → `1`，相等 → `-1`',
                 '本视频：`[2,4,7,9,6,3,1]` → `0`'],
        quote='先计算递增部分之和，再减去递减部分的所有元素，这样一来就得到了递增部分与递减部分和的差，最后判断这个差与0的大小关系即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s` 初始为 `nums[0]`，`p` 往后走，只要还在上升就把 `nums[p]` 加进 `s`',
              '`p` 停下的位置就是峰值；峰值在两部分里都有，所以要再减一次',
              '`p` 继续走到末尾，把剩下的元素都减掉'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：峰值要被减一次（`s -= nums[p]`），否则递减部分少算了峰值',
                 '三个分支对应 `s` 的正、负、零',
                 '对比灵神：灵神一次遍历用 `inc` 标志，峰顶两边抵消；这里分两个 while 循环'],
    ),
)
