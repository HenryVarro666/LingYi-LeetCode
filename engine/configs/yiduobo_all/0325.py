CONFIG = dict(
    num=325, title='和等于 k 的最长子数组长度', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 哈希表记首次位置',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution(object):
    def maxSubArrayLen(self, nums, k):

        first_pos = {}
        first_pos[0] = -1
        now = 0
        res = 0
        for index, num in enumerate(nums):
            now += num
            if now - k in first_pos:
                res = max(res, index - first_pos[now - k])
            
            if now not in first_pos:
                first_pos[now] = index
        
        return res
''',
    call='Solution().maxSubArrayLen([1,-1,5,-2,3], 3)',
    expect=4,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=210, label='nums',
             window=(lambda S: (first_pos_of(S)), 'index')),
        dict(type='map', var='first_pos', fmt=lambda k, v: f'前缀和 {k} → 首次下标 {v}', h=230, font=28),
        dict(type='text', size=30, h=90, fn=lambda S: (
            f"需要的前缀和 `now − k = {S['now'] - S['k']}`" + (f"，首次出现在下标 {S['first_pos'][S['now'] - S['k']]} → 长度 ==`{S['index'] - S['first_pos'][S['now'] - S['k']]}`==" if S['now'] - S['k'] in S['first_pos'] else '，之前没出现过')
        ) if 'index' in S and 'now' in S and S['_line'] >= 8 else ''),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    setup='''
def first_pos_of(S):
    if 'index' not in S or 'now' not in S:
        return None
    t = S['now'] - S['k']
    if t in S['first_pos']:
        return S['first_pos'][t] + 1
    return None
''',
    captions={
        'first_pos = {}': '`first_pos`：记录每个前缀和==第一次==出现的下标，越靠左子数组越长',
        'first_pos[0] = -1': '空前缀和为 0，下标记 `-1`：这样从头开始的子数组长度才是 `index - (-1)`',
        'now = 0': '`now` 是当前前缀和',
        'now += num': '累加 `{num}`，前缀和 `now = {now}`',
        'if now - k in first_pos': lambda S, B, r: (f'要找前缀和 `now − k = {S.now - S.k}`：它在表里 → 区间 (它的下标, index] 的和恰为 k' if S.now - S.k in S.first_pos else f'要找前缀和 `now − k = {S.now - S.k}`：表里没有 → 以 index 结尾没有合法子数组'),
        'res = max': '长度 `{index} − ({first_pos[now - k]})`，`res` 取最大 → =={res}==',
        'if now not in first_pos': lambda S, B, r: (f'`now = {S.now}` 还没出现过 → 记下首次位置' if S.now not in S.first_pos else f'`now = {S.now}` 已经出现过 → ==不覆盖==，保留更靠左的下标'),
        'first_pos[now] = index': '`first_pos[{now}] = {index}`',
        'return res': '最长长度 `{res}`',
    },
    cards=dict(
        one_liner='区间和变成前缀和之差，哈希表只记首次出现位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和整数 `k`，求和恰好等于 `k` 的==最长连续子数组==的长度',
                 '没有则返回 0',
                 '示例：`nums=[1,-1,5,-2,3], k=3` → `4`（`[1,-1,5,-2]`）'],
        quote='若right左侧存在某个left满足s[left - 1] = s[right] - k，那么(left, right)就是一个满足条件的子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举右端点，累加前缀和 `now`',
              '只要之前出现过前缀和 `now − k`，中间那段的和就是 `k`',
              '要最长，所以只存==首次==下标：已有的不覆盖'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`first_pos[0] = -1` 不能漏，否则从下标 0 开始的子数组会丢',
                 '`now` 已存在时不能覆盖，否则长度变短',
                 '原文为 Python 2 风格，本题代码无需修改即可在 Python 3 运行'],
    ),
)
