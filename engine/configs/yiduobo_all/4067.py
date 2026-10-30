def _txt(S):
    if 'p' not in S:
        return ''
    if 'index' not in S:
        return '`s`：窗口内两数之和出现的次数；`d`：两数之差（非 0）出现的次数'
    return f'窗口 `[{S["index"]}, {S["p"] - 1}]`（`p` 是第一个还没放进来的位置）：长度 =={S["p"] - S["index"]}==；`res` = =={S["res"]}=='


CONFIG = dict(
    num=4067, title='数对和受限的最长子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='滑动窗口 · 哈希表 s/d 记和与差', tags=[],
    code='''
class Solution(object):
    def maxSubarray(self, nums):
        
        s = {}
        d = {}

        p = 0
        res = 0
        for index, v in enumerate(nums):
            while p < len(nums) and nums[p] not in s and nums[p] not in d:
                for x in nums[index: p]:
                    s[x + nums[p]] = s.get(x + nums[p], 0) + 1
                    diff = abs(x - nums[p])
                    if diff != 0:
                        d[diff] = d.get(diff, 0) + 1

                p += 1
            
            res = max(res, p - index)

            if index < p:
                for x in nums[index + 1: p]:
                    s[x + v] -= 1
                    if s[x + v] == 0:
                        s.pop(x + v)
                    diff = abs(x - v)
                    if diff != 0:
                        d[diff] -= 1
                        if d[diff] == 0:
                            d.pop(diff)
        
        return res
''',
    call='Solution().maxSubarray([2,3,5,3,2,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [index, p-1]）', pointers={'index': 'blue', 'p': 'pink'},
             window=('index', lambda S: S['p'] - 1), h=200),
        dict(type='map', var='s', label='s：窗口内 两数之和 → 对数', fmt=lambda k, v: f'{k}: {v}', h=150, font=28),
        dict(type='map', var='d', label='d：窗口内 两数之差 → 对数', fmt=lambda k, v: f'{k}: {v}', h=150, font=28),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    skip=['for x in nums[index', 'diff = abs', 'if diff != 0', 'if s[x + v] == 0', 'if d[diff] == 0'],
    max_steps=100,
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        's = {}': '`s` 记窗口内「两数之和」出现的次数',
        'd = {}': '`d` 记窗口内「两数之差」出现的次数',
        'p = 0': '`p` 是窗口右边界（开区间）：`nums[p]` 是下一个想放进来的数',
        'for index, v in enumerate': lambda S, B, r: ('左边界都枚举完了，循环结束' if 'index' in B and B['index'] == S['index'] else f'固定左边界 `index = {S.index}`，找它能扩到的最远右边界'),
        'while p < len': lambda S, B, r: (
            '`p` 到头了，不能再扩' if S.p >= len(S.nums) else
            (f'`nums[{S.p}] = {S.nums[S.p]}` 既不在 `s` 也不在 `d`：窗口里凑不出它 → ==可以放进来=='
             if S.nums[S.p] not in S.s and S.nums[S.p] not in S.d else
             f'`nums[{S.p}] = {S.nums[S.p]}` 在 `s` 或 `d` 里：放进来就会出现 i+j=k → ==扩张停止==')),
        's[x + nums[p]] =': '新元素与 `x = {x}` 的和 `{x + nums[p]}` 记入 `s`，次数 {s[x + nums[p]]}',
        'd[diff] = ': '它们的差 `{diff}` 非 0，记入 `d`：`d[{diff}]` = {d[diff]}',
        'p += 1': '`nums[{p - 1}]` 进入窗口，`p` → {p}',
        'res = max': '以 `index = {index}` 为左端点，最长有效长度 `p - index = {p - index}`：`res` = =={res}==',
        'if index < p': '左边界要右移了，先把 `nums[{index}]` 产生的和与差从 `s`、`d` 里减掉',
        's[x + v] -= 1': '`v = {v}` 与 `x = {x}` 的和 `{x + v}` 少一对 → {s.get(x + v, 0)}（减到 0 就删掉这个键）',
        's.pop(x + v)': '次数归零，`s` 里删掉键 `{x + v}`',
        'd[diff] -= 1': '差 `{diff}` 少一对 → {d.get(diff, 0)}',
        'd.pop(diff)': '次数归零，`d` 里删掉键 `{diff}`',
        'return res': '最长有效子数组长度 =={res}==',
    },
    cards=dict(
        one_liner='左边界固定时右边界越远越难合法：用 s、d 两个哈希表判断新数能否入窗',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`（哈希表键数）',
        problem=['子数组中不能有互不相同的下标 `i, j, k` 满足 `nums[i] + nums[j] = nums[k]`',
                 '求最长有效子数组；示例 `[2,3,5,3,2,1]` → `3`'],
        quote='需要考察新加入的元素是否会使得窗口内出现nums[i] + nums[j] = nums[k]的情况。……只需要考察新元素是否可能成为nums[i]或者nums[k]。',
        quote_src='—— yiduobo 题解原文',
        idea=['新元素成为 k：窗口里有两数之和等于它；成为 i/j：窗口里有两数之差等于它',
              '哈希表 `s` 记和、`d` 记差；新数不在 `s`、`d` 里就能放进来',
              '左边界右移时，再把它与窗口其余数的和、差各减一次'],
        summary=['时间 `O(n^2)`：窗口每次进出，维护哈希表花 `O(n)`，`p` 与 `index` 都只前进',
                 '易错：差为 0 时（两个相同的数）不记入 `d`；两个相同的数的和仍要记入 `s`',
                 '次数减到 0 要 `pop`，否则「在不在表里」的判断会出错',
                 '对比灵神：灵神枚举右端点、条件不满足才收缩；这里枚举左端点、尽量向右扩张'],
    ),
)
