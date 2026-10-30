def _t(S):
    if 'now' not in S:
        return ''
    m, k = S['modulo'], S['k']
    if S['now'] >= k:
        t = (S['now'] - k) % m
        return f"前缀和 `now = {S['now']}`：要找之前余数为 `({S['now']} − {k}) % {m}` = =={t}=={'' if 'cnt' not in S else '，已出现 `' + str(S['cnt'].get(t, 0)) + '` 次'}"
    return f"前缀和 `now = {S['now']} < k = {k}`：较长前缀必须 ≥ k，跳过"


CONFIG = dict(
    num=2845, title='统计趣味子数组的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='01 数组 + 前缀和余数计数',
    tags=['前缀和与哈希表', '难度分 2073'],
    code='''
class Solution(object):
    def countInterestingSubarrays(self, nums, modulo, k):

        score = [1 if v % modulo == k else 0 for v in nums]
        cnt = {0 : 1}
        res = 0
        now = 0
        for v in score:
            now += v
            if now >= k:
                res += cnt.get((now - k) % modulo, 0)
            
            cnt[now % modulo] = cnt.get(now % modulo, 0) + 1
        
        return res
''',
    call='Solution().countInterestingSubarrays([3,2,4,5,7], 2, 1)',
    expect=8,
    views=[
        dict(type='array', var='score', label='score（nums 变成 01 数组）', h=190, cell=100,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='map', var='cnt', label='cnt：前缀和 % modulo → 出现次数', fmt=lambda k, v: f'{k}: {v}', h=200, font=32),
        dict(type='text', h=110, size=28, fn=_t),
    ],
    watch=[('v', 'v', 'blue'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'score = [': '先变形：`nums[i] % modulo == k` 记 1，否则 0 → `score = {score}`',
        'cnt = {0 : 1}': '哈希表记各余数的前缀个数；空前缀（和 0）先算 1 个',
        'res = 0': '`res` 累计趣味子数组个数',
        'now = 0': '`now`：当前前缀和（1 的个数）',
        'for v in score': lambda S, B, r: (f'看 `score` 的下一个值 `v = {S.v}`' if sum(S.cnt.values()) <= len(S.score) else '扫描结束'),
        'now += v': '`now = {B.now} + {v} = {now}`',
        'if now >= k': lambda S, B, r: (f'`now = {S.now} ≥ k = {S.k}`：较长前缀够大，可以和旧前缀相减' if S.now >= S.k
                                        else f'`now = {S.now} < k = {S.k}`：差不可能等于 k，跳过'),
        'res += cnt.get': '要找余数 `({now} − {k}) % {modulo} = {(now - k) % modulo}` 的旧前缀，有 `{cnt.get((now - k) % modulo, 0)}` 个 → `res = {res}`',
        'cnt[now % modulo] =': '把当前前缀的余数 `{now % modulo}` 记入哈希表：`cnt = {cnt}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先变 01 数组：1 的个数就是区间和，再用前缀和差',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组中满足 `nums[i] % modulo == k` 的下标个数为 `cnt`',
                 '`cnt % modulo == k` 的子数组叫趣味子数组，求个数',
                 '示例：`[3,2,4,5,7], modulo = 2, k = 1`'],
        quote='先根据nums中每个元素对modulo取模的结果是否为k将其变形为一个新的01数组score，接下来的任务就是找出score中1的个数模modulo等于k的子数组数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['`score` 是 01 数组，子数组 1 的个数 = 区间和 → 前缀和',
              '区间和模 modulo 为 k ⇒ 两个前缀和差模 modulo 为 k，==较长的前缀必须 ≥ k==',
              '一趟扫描：哈希表记旧前缀的余数次数，边算边累加'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`now >= k` 的判断不能漏，否则 `(now − k) % modulo` 会错配',
                 '`cnt = {0: 1}` 表示空前缀',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神用定长数组做计数；这里用字典 + `get`，并显式先生成 `score`'],
    ),
)
