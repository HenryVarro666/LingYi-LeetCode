def _text(S):
    if 'p' not in S:
        return ''
    n = len(S['nums'])
    if S['p'] >= n:
        return '数组里没有 1' 
    if 'q' in S and S['q'] < n and S['nums'][S['q']] == 1 and S['_line'] >= 17:
        return f"`p={S['p']}`、`q={S['q']}` 之间有 `{S['q'] - S['p'] - 1}` 个 0：左 0 右 k … 左 k 右 0，共 =={S['q'] - S['p']}== 种"
    return f"`res = {S.get('res', 1)}`"


CONFIG = dict(
    num=2750, title='将数组划分成若干好子数组的方式', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='找相邻的 1 · 累乘 k+1',
    tags=['灵神题单', '难度分 1598'],
    code='''
class Solution(object):
    def numberOfGoodSubarraySplits(self, nums):

        mod = 10 ** 9 + 7
        p = 0
        while p < len(nums) and nums[p] == 0:
            p += 1
        
        if p == len(nums):
            return 0
        
        res = 1
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] == 0:
                q += 1
            
            if q == len(nums):
                break
                
            res = res * (q - p) % mod
            p = q
        
        return res
''',
    call='Solution().numberOfGoodSubarraySplits([0,1,0,0,1,0,0,0,1,0])',
    expect=12,
    views=[
        dict(type='text', fn=_text, h=90),
        dict(type='array', var='nums', pointers={'p': 'pink', 'q': 'blue'}, h=300,
             color=lambda S, i, v: 'green' if v == 1 else None),
    ],
    watch=[('p', 'p', 'pink'), ('q', 'q', 'blue'), ('res', 'res', 'green')],
    captions={
        'while p < len(nums) and nums[p] == 0': lambda S, B, r: (f'`nums[{S.p}] = 0`，前导 0 只能归首个 1 的子数组，`p` 继续右移' if S.p < len(S.nums) and S.nums[S.p] == 0
                                                                else '`p` 停在首个 1 上'),
        'if p == len(nums)': lambda S, B, r: '`p` 走到末尾：全是 0，不存在合法划分 → 返回 0' if S.p == len(S.nums) else '`p` 没越界，说明至少有一个 1，继续',
        'res = 1': '初始 `res = 1`，后面按乘法原理累乘',
        'while p < len(nums):': '以 `p` 位置的 1 为左端，去找右边的下一个 1',
        'q = p + 1': '从 `p + 1` 开始找下一个 1',
        'while q < len': lambda S, B, r: (f'`nums[{S.q}] = 0`，两个 1 之间的 0，`q` 右移' if S.q < len(S.nums) and S.nums[S.q] == 0
                                          else '`q` 停下：越界或碰到 1'),
        'if q == len(nums)': lambda S, B, r: ('`q` 越界：`p` 右边没有 1 了，后缀 0 归最后一个 1，结束' if S.q == len(S.nums)
                                              else '`q` 指向下一个 1，可以结算这一段'),
        'res = res *': '`p = {p}` 和 `q = {q}` 之间 `{q - p - 1}` 个 0，左 0 右 k … 左 k 右 0 共 `{q - p}` 种 → `res = {B.res} × {q - p} = {res}`',
        'p = q': '`p` 跳到下一个 1：`p = {p}`',
        'return res': '所有相邻 1 的方案数累乘完：`{res}`',
    },
    cards=dict(
        one_liner='前导、后缀 0 归端点的 1；两个 1 之间的 k 个 0 有 k+1 种分法',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二元数组，恰好含一个 `1` 的子数组叫好子数组',
                 '求划分成若干好子数组的方法数，结果对 `10^9 + 7` 取余',
                 '示例：`[0,1,0,0,1]` → `3`；本视频：`[0,1,0,0,1,0,0,0,1,0]` → `12`'],
        quote='数组中的前导0必然只能被划分到数组的首个1所在的子数组，而后缀0则只能被划分到数组中最后那个1所在的子数组，而在两个1之间的连续0，则可以将前半段划分到左侧的子数组，将后半段划分到右侧的子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['先跳过前导 0，找到首个 1；全是 0 直接返回 0',
              '两个 1 之间长度为 `k` 的 0：左 0 右 `k`、…、左 `k` 右 0，共 `k + 1` 种',
              '`p` 在当前 1，`q` 找下一个 1，累乘 `q - p`，再令 `p = q`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`q` 越界（右边没有 1）时必须 `break`，后缀 0 不产生新方案',
                 '示例里首尾的 0 不影响答案，只看相邻 1 的间距',
                 '对比灵神：灵神一次遍历用 `pre` 记上一个 1；yiduobo 用 `p`、`q` 双指针找相邻两个 1'],
    ),
)
