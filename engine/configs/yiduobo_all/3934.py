_NUMS = [1, 1, 2, 2]
_B, _M1, _M2 = 100003, 10 ** 9 + 7, 2147483647


def _h(w):
    v1 = v2 = 0
    for x in w:
        v1 = (v1 * _B + x) % _M1
        v2 = (v2 * _B + x) % _M2
    return (v1, v2)


_WIN = {_h(_NUMS[i:i + L]): str(_NUMS[i:i + L]).replace(' ', '') for L in range(1, len(_NUMS) + 1) for i in range(len(_NUMS) - L + 1)}


def _cnt_fmt(k, v):
    return f'{_WIN.get(k, "?")} × {v}'


def _top(S):
    if 'length' in S and S['_line'] >= 9:
        return f'检查长度 `length = {S["length"]}`：窗口的哈希值有没有只出现一次的？'
    if 'left' in S:
        return f'二分长度：答案在 `[{S["left"]}, {S["right"]}]` 里，`check(mid)` 为真就往小找'
    return ''


def _win(S):
    if 'length' in S and 'index' in S:
        return ('window', S['index'] - S['length'] + 1 if S['index'] >= S['length'] else 0, S['index'])
    return None


CONFIG = dict(
    num=3934, title='最短唯一子数组', difficulty='Hard', category='字符串',
    author='yiduobo', technique='二分长度 + 滑动窗口双哈希',
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
    call='Solution().smallestUniqueSubarray([1, 1, 2, 2])',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var='nums', label='nums（蓝箭头 = 窗口右端 index，框 = 当前窗口）', cell=84, h=220,
             pointers={'index': 'blue'}, window=('max(0, index - length + 1)', 'index')),
        dict(type='map', var='cnt', label='cnt：窗口哈希 → 出现次数（黄框 = 刚改动）', fmt=_cnt_fmt, h=150, font=30),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'cyan'), ('length', 'length', 'orange'), ('v1', 'v1', 'green')],
    skip=['m1 = ', 'm2 = ', 'base = ', 'v1 = 0', 'v2 = 0', 'p1 = 1', 'p2 = 1', 'v2 = (', 'p2 = p2', 'cnt = {}', 'return False\n', 'def check'],
    captions={
        'left = 1': '`left = 1`：长度至少为 1',
        'right = len(nums)': '`right = {right}`：整个数组一定是唯一的，所以答案不超过它',
        'while left < right': lambda S, B, ret: (f'`left = {S.left} < right = {S.right}`：还没夹到，继续二分' if S.left < S.right else f'`left == right = {S.left}`：二分结束'),
        'mid = (left + right) // 2': '试长度 `mid = {mid}`：有没有哪个长度为 {mid} 的子数组独一无二？',
        'right = mid': '有 → 更长的也一定有（左右加一个数仍唯一），所以收缩上界：`right = {right}`',
        'left = mid + 1': '没有 → 更短的也不可能有，所以 `left = {left}`',
        14: lambda S, B, ret: ('第一个窗口的哈希算好了' if 'index' in B and B.get('index') == S.index else '先算第一个窗口 `nums[0:' + str(S.length) + ']` 的哈希：按 base 进制逐位累加'),
        15: '窗口哈希 `v1 = v1 × base + nums[{index}]`，取模：`{v1}`',
        'p1 = p1 * base % m1': '`p1` = `base^{length}` 的累积，滑窗时用来减掉最左边的数',
        'cnt[(v1, v2)] = 1': '第一个窗口入表：`cnt` 里记 1 次',
        21: lambda S, B, ret: ('窗口都滑完了，`cnt` 里是每个哈希的出现次数' if 'index' in B and B.get('index') == S.index and S['_line'] == 21 else f'窗口右移：右端进 `nums[{S.index}]`，左端出 `nums[{S.index - S.length}]`'),
        22: '窗口整体 ×base 再加右端新数 `nums[{index}]`',
        'v1 = (v1 - p1': '再减去左端 `nums[{index - length}] × base^length`：得到新窗口的哈希 `{v1}`',
        'key = (v1, v2)': '两个模数的哈希组成 `key`，降低冲突概率',
        'cnt[key] = cnt.get': '这个窗口的哈希出现次数 +1 → `{cnt[key]}` 次',
        31: '逐个看哈希计数：有没有只出现一次的？',
        'if check(mid)': '调用 `check({mid})`：长度为 {mid} 的子数组里有没有唯一的？',
        'if cnt[key] == 1': lambda S, B, ret: (f'`{_WIN.get(S.key, "?")}` 只出现 1 次 → ==找到唯一子数组==' if S.cnt[S.key] == 1 else f'`{_WIN.get(S.key, "?")}` 出现 {S.cnt[S.key]} 次，不唯一'),
        'return True': '存在唯一窗口 → `check` 返回 `True`',
        'return False': '没有任何唯一窗口 → `check` 返回 `False`',
        'return left': '最短唯一子数组长度 `{left}`',
    },
    max_steps=120,
    cards=dict(
        one_liner='长度越大越容易唯一，二分长度 + 滑窗哈希计数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['求 `nums` 里 ==只出现一次== 的子数组的最小长度',
                 '示例：`[3,3,3]` → `3`；`[2,1,2,3,3]` → `1`',
                 '本视频：`[1,1,2,2]` → `2`'],
        quote='若对于某个较短的长度存在独一无二的字符串，那么对于较长的长度必然也存在独一无二的字符串',
        quote_src='—— yiduobo 题解原文',
        idea=['单调性：长度 `L` 有唯一子数组，往两边加一个数仍唯一 → 可以二分 `L`',
              '`check(L)`：滑动窗口算所有长度 `L` 窗口的 base 进制哈希，字典计数',
              '有计数为 1 的哈希就成功；用两个模数合成 `key` 降低冲突'],
        result='长度 1 都重复，长度 2 有唯一窗口 → 返回 `2` ✓',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '滑窗：先 `×base` 加新数，再减去 `旧数 × base^length`',
                 '减法后要 `+ m` 再取模，防止出现负数',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比灵神：灵神用后缀数组 `O(n)` 求每个后缀的最短唯一前缀；yiduobo 用哈希 + 二分，写起来更短'],
    ),
)
