def _win(S):
    if 'index' not in S or 'length' not in S or '_inner' not in S or 'cnt' not in S['_inner']:
        return None
    return (max(0, S['index'] - S['length'] + 1), S['index'])


def _top(S):
    if 'mid' in S and 'left' in S and 'right' in S:
        s = f"二分答案长度：`left = {S['left']}`，`right = {S['right']}`，当前试 `mid = {S['mid']}`"
        return s
    if 'left' in S and 'right' in S:
        return f"二分答案长度：`left = {S['left']}`，`right = {S['right']}`"
    return ''


def _hl(S):
    w = _win(S)
    return w


CONFIG = dict(
    num=3934, title='最短唯一子数组', difficulty='Hard', category='字符串',
    author='yiduobo', technique='二分长度 + 双哈希滑动窗口',
    tags=['灵神题单', '字符串', '难度分 2163'],
    code='''
class Solution(object):
    def smallestUniqueSubarray(self, nums):
        
        base = 100003
        m1 = 10 ** 9 + 7
        m2 = 2147483647

        def check(length):
            cnt = {}
            v1 = 0
            v2 = 0
            p1 = 1
            p2 = 1
            for index in range(length):
                v1 = (v1 * base + nums[index]) % m1
                v2 = (v2 * base + nums[index]) % m2
                p1 = p1 * base % m1
                p2 = p2 * base % m2

            cnt[(v1, v2)] = 1
            for index in range(length, len(nums)):
                v1 = (v1 * base + nums[index]) % m1
                v1 = (v1 - p1 * nums[index - length] % m1 + m1) % m1
                
                v2 = (v2 * base + nums[index]) % m2
                v2 = (v2 - p2 * nums[index - length] % m2 + m2) % m2
                
                key = (v1, v2)
                cnt[key] = cnt.get(key, 0) + 1
            
            for key in cnt:
                if cnt[key] == 1:
                    return True

            return False

        left = 1
        right = len(nums)
        while left < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().smallestUniqueSubarray([1, 2, 1, 2])',
    expect=2,
    skip=['v1 = 0', 'key = (v1, v2)', 'v2 = ', 'p2 = ', 'cnt = {}', 'base = ', 'm1 = ', 'm2 = '],
    max_steps=100,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='nums', label='nums（蓝框 = 当前长度为 length 的窗口）', cell=84, window=(lambda S: (_win(S) or (None, None))[0], lambda S: (_win(S) or (None, None))[1]),
             pointers={'index': 'pink'}, h=250),
        dict(type='map', var=lambda S: (S.get('_inner') or {}).get('cnt') if 'length' in (S.get('_inner') or {}) else None,
             label='cnt（窗口哈希 → 出现次数，次数为 1 = 唯一）',
             fmt=lambda k, v: f'hash {k[0] % 10000:04d} → {v}', h=300),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'cyan'), ('length', 'length'), ('v1', 'v1')],
    captions={
        'left = 1': '最短唯一长度至少是 1：`left = 1`',
        'right = len(nums)': '整个数组本身一定唯一：`right = len(nums) = {right}`（答案不会超过它）',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，答案还没夹紧，继续二分'
                                               if S.left < S.right else f'`left = right = {S.left}` → ==夹出最小的唯一长度=='),
        'mid = (left + right) // 2': '试 `mid = {mid}`：长度为 {mid} 的子数组里有没有唯一的？',
        'if check(mid)': '调用 `check({mid})`：长度为 {mid} 的窗口里，有没有哈希只出现一次的？',
        'right = mid': '长度越大越容易唯一（单调），所以更短的可能还行：`right = {mid}`',
        'left = mid + 1': '`mid` 不够，答案至少是 `{left}`：`left = mid + 1`',
        'p1 = 1': '`p1` 是 `base^length`，滑动时用来减掉最左边的数',
        'for index in range(length)': lambda S, B, r: ('第一个窗口算完了' if B.get('index') == S.length - 1 and S.index == B.get('index') else '先算第一个窗口 `nums[0:%d]` 的哈希' % S.length),
        15: "把 `nums[{index}] = {nums[index]}` 接到末尾：`v1 = (v1 × base + {nums[index]}) % m1` = {v1}（`v2` 用另一个模数同样算）",
        22: "窗口右移：先乘 base 再加上 `nums[{index}] = {nums[index]}` → `v1 = {v1}`",
        'p1 = p1 * base % m1': '`p1 = base^{index+1}`，之后用它去掉最左边的数',
        'cnt[(v1, v2)] = 1': '第一个窗口的哈希记入 `cnt`，次数 1',
        'for index in range(length, len(nums))': lambda S, B, r: ('窗口滑到末尾了' if B.get('index') == len(S.nums) - 1 and S.index == B.get('index') else f'窗口右端点移到 `index = {S.index}`，每次只更新 O(1)'),
        'v1 = (v1 - p1': lambda S, B, r: f"减去滑出窗口的 `nums[{S.index - S.length}] = {S.nums[S.index - S.length]}`（它乘的是 base^length）→ `v1 = {S.v1}`，现在是 `nums[{S.index - S.length + 1}:{S.index + 1}]` 的哈希",
        'key = (v1, v2)': '用两个哈希组成 `key`，降低冲突概率',
        'cnt[key] = cnt.get': lambda S, B, r: f"窗口 `nums[{S.index - S.length + 1}:{S.index + 1}]` 的 key 出现 `{S.cnt[S.key]}` 次" + ('（==重复==）' if S.cnt[S.key] > 1 else '（暂时唯一）'),
        'for key in cnt': lambda S, B, r: ('所有哈希都看过了，没有唯一的' if 'key' in B and B['key'] == list(S.cnt)[-1] else '遍历所有窗口哈希，找有没有只出现一次的'),
        'if cnt[key] == 1': lambda S, B, r: (f'`cnt[key] = {S.cnt[S.key]}` == 1 → ==这个长度有唯一子数组==' if S.cnt[S.key] == 1
                                              else f'`cnt[key] = {S.cnt[S.key]}` ≥ 2，重复，看下一个'),
        'return True': '存在唯一的 → 返回 `True`',
        'return False': '所有窗口都重复 → 返回 `False`',
        'return left': '`left` 就是最短唯一子数组的长度：`{left}`',
    },
    cards=dict(
        one_liner='长度越大越容易唯一，二分长度，哈希判断有没有唯一窗口',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['找 `nums` 里==只出现一次==的子数组的最小长度',
                 '示例：`[3,3,3]` → `3`；`[2,1,2,3,3]` → `1`',
                 '本视频：`[1,2,1,2]` → `2`（`[1,2]` 出现两次，`[2,1]` 唯一）'],
        quote='若对于某个较短的长度存在独一无二的字符串，那么对于较长的长度必然也存在独一无二的字符串，因此在这里可以二分这个长度length。',
        quote_src='—— yiduobo 题解原文',
        idea=['先证单调：长度 L 的唯一串，两端各加一个元素仍然唯一 → ==可以二分长度==',
              '`check(length)`：滑动窗口算所有长度为 length 的窗口哈希，数出现次数',
              '哈希是 base 进制数取模；右移 = 乘 base、加新元素、减 `nums[i-length] × base^length`',
              '原文用两个模数（双哈希）来降低冲突'],
        result='`check(2)` 为真，`check(1)` 为假 → 答案 2 ✓',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：滑出的元素要乘 `base^length`（`p1`），不是 `base^(length-1)`',
                 '减法后要 `+ m1` 再取模，避免负数',
                 '后缀数组 `O(n)` 也能做，原文选更好写的二分 + 哈希',
                 '原文代码在 Python 3 下无需改动（已使用 `//`）'],
    ),
)
