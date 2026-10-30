CONFIG = dict(
    num=3712, title='出现次数能被 K 整除的元素总和', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数',
    tags=[],
    code='''
class Solution:
    def sumDivisibleByK(self, nums: List[int], k: int) -> int:
        cnt = Counter(nums)
        ans = 0
        for x, c in cnt.items():
            if c % k == 0:
                ans += x * c
        return ans
''',
    call='Solution().sumDivisibleByK([1,2,2,3,3,3,3,4], 2)',
    expect=16,
    views=[
        dict(type='array', var='nums', label='nums', cell=80, h=170),
        dict(type='map', var='cnt', label='cnt（元素 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=190, font=34),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"当前 `x={S['x']}`，出现 `c={S['c']}` 次，`{S['c']} % {S['k']} = {S['c'] % S['k']}`" if 'x' in S and 'c' in S else '')),
    ],
    watch=['k', 'x', 'c', ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '一次遍历统计每个数的出现次数：`cnt = {cnt}`',
        'ans = 0': '`ans` 累计满足条件的元素之和',
        'for x, c': '取出键值对：元素 `x = {x}`，出现次数 `c = {c}`',
        'if c % k': '`c % k = {c} % {k} = {c % k}` → ' + '{"整除，要加" if c % k == 0 else "不整除，跳过"}',
        'ans += x * c': '`x` 出现了 `c` 次，每次都要加：`{B.ans} + {x} × {c}` → `ans` = =={ans}==',
        'return ans': '遍历完哈希表，返回 `{ans}`',
    },
    cards=dict(
        one_liner='先数每个元素出现几次，次数是 k 的倍数就把 c 个 x 都加上',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `nums` 和整数 `k`',
                 '出现次数能被 `k` 整除的元素，==每次出现都要计入总和==',
                 '示例：`[1,2,2,3,3,3,3,4]`，`k=2` → `16`'],
        quote='用哈希表（或者数组）统计每个元素的出现次数。遍历哈希表中的键值对 (x,c)，如果 c 是 k 的倍数，那么把 c 个 x 加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`Counter` 一次遍历得到 `元素 → 次数`',
              '再遍历键值对：`c % k == 0` 就加 `x * c`',
              '次数不整除的元素直接跳过'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '加的是 `x * c`，不是 `x`：出现几次就加几次',
                 '另一种写法：用一行 `sum(x * c for ... if c % k == 0)` 生成器表达式',
                 '值域只有 1~100，也可以用数组代替哈希表'],
    ),
)
