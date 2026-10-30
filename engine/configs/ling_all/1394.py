CONFIG = dict(
    num=1394, title='找出数组中的幸运数', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表计数',
    code='''
class Solution:
    def findLucky(self, arr: List[int]) -> int:
        cnt = Counter(arr)
        ans = -1
        for x, c in cnt.items():
            if x == c:
                ans = max(ans, x)
        return ans
''',
    call='Solution().findLucky([1,2,2,3,3,3])',
    expect=3,
    views=[
        dict(type='array', var='arr', label='arr', h=130),
        dict(type='map', var='cnt', fmt=lambda k, v: f'{k} 出现 {v} 次', h=190, label='cnt'),
        dict(type='text', h=60, fn=lambda S: (f"当前 `x = {S['x']}`，`c = {S['c']}`" if 'x' in S else '')),
    ],
    watch=['x', 'c', ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '统计每个数的出现次数：`{dict(cnt)}`',
        'ans = -1': '先假设没有幸运数，`ans = -1`',
        'if x == c': lambda S, B, r: f'数值 `{S.x}`，次数 `{S.c}` → ' + ('==相等，是幸运数==' if S.x == S.c else '不相等，不是'),
        'ans = max': '幸运数取最大：`ans = max({B.ans}, {x})` = =={ans}==',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='数一数每个数出现几次，次数等于数值的取最大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['幸运数：出现次数恰好等于自身数值的整数',
                 '返回最大的幸运数，没有则返回 `-1`',
                 '示例：`[1,2,2,3,3,3]` → `3`'],
        quote='用哈希表统计每个元素的出现次数。然后遍历哈希表，其中 key 等于 value 的元素即为幸运数，取其最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`Counter` 得到 数值 → 次数',
              '遍历哈希表，`key == value` 就是幸运数',
              '用 `ans` 记录最大值，初值 `-1`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：没有幸运数时要返回 `-1`，所以 `ans` 初值是 `-1`',
                 '写法二：`max(..., default=-1)` 一行搞定',
                 '方法二：次数不会超过 n，用长为 n+1 的数组计数、从大到小找'],
    ),
)
