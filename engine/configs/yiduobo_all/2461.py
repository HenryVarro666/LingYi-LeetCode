def _win(S):
    if 'cnt' not in S:
        return None
    if 'res' not in S:
        n = sum(S['cnt'].values())
        return (0, n - 1) if n else None
    idx = S.get('index')
    if idx is None:
        return (0, S['k'] - 1)
    line = S.get('_line')
    if line in (16, 17):                       # 新元素已进、旧元素未出：窗口暂时是 k+1 个
        return (idx - S['k'], idx)
    return (idx - S['k'] + 1, idx)


def _ok(S, B, ret):
    if len(S.cnt) == S.k:
        return f'`len(cnt) = {S.k} = k`：每种数字==恰好出现一次==，窗口合法'
    return f'`len(cnt) = {len(S.cnt)} ≠ k`：有数字重复，窗口不合法'


CONFIG = dict(
    num=2461, title='长度为 K 子数组中的最大和', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='滑动窗口 + 哈希表长度判重',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1553'],
    code='''
class Solution(object):
    def maximumSubarraySum(self, nums, k):

        cnt = {}
        s = 0
        for num in nums[:k]:
            cnt[num] = cnt.get(num, 0) + 1
            s += num
        
        if len(cnt) == k:
            res = s
        else:
            res = 0
        
        for index in range(k, len(nums)):
            cnt[nums[index]] = cnt.get(nums[index], 0) + 1
            s += nums[index]

            cnt[nums[index - k]] -= 1
            if cnt[nums[index - k]] == 0:
                cnt.pop(nums[index - k])
            s -= nums[index - k]

            if len(cnt) == k:
                res = max(res, s)
        
        return res
''',
    call='Solution().maximumSubarraySum([1,2,1,3,4,3], 3)',
    expect=8,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前窗口）', h=240, cell=100,
             pointers={'index': 'blue'},
             window=(lambda S: (_win(S) or (None,))[0], lambda S: (_win(S) or (None, None))[1])),
        dict(type='map', var='cnt', label='cnt（数字 → 窗口内出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"窗口和 `s = {S['s']}`，`len(cnt) = {len(S['cnt'])}`，`k = {S['k']}`" if 'cnt' in S and 's' in S
                           else '==哈希表长度为 k== ⇔ 每种数字恰好一次')),
    ],
    watch=[('num', 'num'), ('index', 'index', 'blue'), ('s', 's', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = s': '初始窗口合法：`res = {res}`',
        'res = 0': '初始窗口不合法：`res` 先置 0',
        'cnt = {}': '`cnt` 维护窗口中每种数字出现的次数',
        's = 0': '`s` 维护窗口中的数字和',
        'for num in nums[:k]': lambda S, B, r: ('初始窗口 `nums[:k]` 建好了' if 'num' in B and S.num == B.num and S.s == B.s + 0 and S._line == B._line and sum(S.cnt.values()) == S.k
                                                else f'把 `{S.num}` 放进初始窗口'),
        'cnt[num] = cnt.get': '`cnt[{num}]` → {cnt[num]}',
        's += num': '`s` → {s}',
        'if len(cnt) == k:': _ok,
        'for index in range(k, len(nums))': lambda S, B, r: (f'窗口右移：`nums[{S.index}]` 进，`nums[{S.index - S.k}]` 出'
                                                             if 'index' not in B or S.index != B.index else '窗口滑到末尾'),
        'cnt[nums[index]] = cnt.get': '新元素 `{nums[index]}` 计数 → {cnt[nums[index]]}',
        's += nums[index]': '`s += {nums[index]}` → {s}',
        'cnt[nums[index - k]] -= 1': '左边界 `{nums[index - k]}` 移出：计数 → {cnt[nums[index - k]]}',
        'if cnt[nums[index - k]] == 0': lambda S, B, r: (f'`{S.nums[S.index - S.k]}` 计数为 0：==必须删掉 key==，否则长度不对'
                                                         if S.nums[S.index - S.k] in S.cnt and S.cnt[S.nums[S.index - S.k]] == 0
                                                         else f'`{S.nums[S.index - S.k]}` 窗口里还有，保留'),
        'cnt.pop(': '`cnt.pop({nums[index - k]})`，`len(cnt)` → {len(cnt)}',
        's -= nums[index - k]': '`s -= {nums[index - k]}` → {s}',
        'res = max(res, s)': '`res = max({B.res}, {s}) = {res}`',
        'return res': '最大和 `{res}`',
    },
    cards=dict(
        one_liner='哈希表长度恰好为 k，就说明窗口里没有重复',
        complexity='时间 `O(n)`，空间 `O(k)`',
        problem=['求长度为 `k` 且元素==各不相同==的子数组最大和，没有则返回 `0`',
                 '示例：`nums = [1,5,4,2,9,9,9], k = 3` → `15`',
                 '本视频：`nums = [1,2,1,3,4,3], k = 3` → `8`（`[1,3,4]`）'],
        quote='将这个条件对应到哈希表的长度为k，这样每种数字出现的次数就是恰好一次了。……哈希表的计数为0时，需要将这个数对应的key从哈希表中移除，才能保证哈希表的长度正确。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用 `nums[:k]` 建好初始窗口的 `cnt` 和 `s`',
              '右移：先加入 `nums[index]`，再移出 `nums[index − k]`',
              '`len(cnt) == k` 时用 `s` 更新 `res`'],
        summary=['时间 `O(n)`，空间 `O(k)`',
                 '易错：计数减到 0 不 `pop`，`len(cnt)` 偏大会误判为合法',
                 '原文为 Python 2 风格，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神用 `defaultdict` + `del`，套「入-更新-出」一个循环'],
    ),
)
