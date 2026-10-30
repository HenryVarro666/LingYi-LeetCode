def _cost(S):
    k = S['k']
    return [m - 1 + (k - 1) // m for m in range(1, k + 1)]


def _col(S, i, v):
    if 'rt' in S and i + 1 in (S['rt'], S['rt'] + 1):
        return 'green' if v == min(_cost(S)) else 'yellow'
    return None


def _text(S):
    k = S['k']
    if 'rt' not in S:
        return f'`k = {k}`：先加一 `m-1` 次，再复制 `(k-1)//m` 次；下面是每个 `m` 的总操作数'
    rt = S['rt']
    a = rt - 1 + (k - 1) // rt
    b = rt + (k - 1) // (rt + 1)
    return f'`m = {rt}` → ==`{a}`==　`m = {rt + 1}` → ==`{b}`==　柱子最低处就在 `rt` 附近'


CONFIG = dict(
    num=3091, title='执行操作使数据元素之和大于等于 K', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='先加一再复制 · 对勾函数',
    tags=['灵神题单', '难度分 1522'],
    code='''
class Solution:
    def minOperations(self, k: int) -> int:
        rt = max(isqrt(k - 1), 1)
        return min(rt - 1 + (k - 1) // rt, rt + (k - 1) // (rt + 1))
''',
    call='Solution().minOperations(11)',
    expect=5,
    views=[
        dict(type='text', fn=_text, h=90, lines=2),
        dict(type='bars', var=_cost, label='总操作数 m - 1 + (k-1)//m（下标 0 对应 m = 1）',
             pointers={'rt - 1': 'blue', 'rt': 'pink'}, pointer_labels={'rt - 1': 'm=rt', 'rt': 'm=rt+1'},
             color=_col, h=420),
    ],
    watch=[('k', 'k', 'blue'), ('rt', 'rt', 'pink')],
    captions={
        'rt = max': '开平方取整 `isqrt({k} - 1)`，和 1 取最大防止 `m = 0` → `rt` = =={rt}==；最小值就在 `m = rt` 或 `rt + 1`',
        'return min': '`m = {rt}`：`{rt-1} + {(k-1)//rt} = {rt - 1 + (k - 1) // rt}`；`m = {rt+1}`：`{rt} + {(k-1)//(rt+1)} = {rt + (k - 1) // (rt + 1)}` → 取小的 ==`{ret}`==',
    },
    cards=dict(
        one_liner='先把数加到 m，再复制 ⌊(k-1)/m⌋ 次',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`nums = [1]`，可以把某个元素加一，或复制某个元素追加到末尾',
                 '求让元素和 `≥ k` 的最少操作数',
                 '示例：`k = 11` → `5`（加到 4，再复制两次，和为 12）'],
        quote='先加一再复制更优。所以，加一操作都应当在复制操作之前。',
        quote_src='—— 灵茶山艾府题解',
        before=[dict(heading='贪心：先加一，再复制', lines=[
            '先复制 `m` 再加一，和只多 `m + 1`',
            '先加一再复制 `m + 1`，和多 `m + 2`',
            '所以加一都放在前面：枚举 `m = 1 + add`',
            '还需复制 `ceil(k/m) - 1 = (k-1)//m` 次',
            '答案 `min(m - 1 + (k-1)//m)`，方法一枚举 `m`，`O(k)`'])],
        idea=['`m - 1 + (k-1)//m` 是「对勾函数」：先降后升',
              '最低点在 `√(k-1)` 附近 → 只试 `rt` 和 `rt + 1` 两个 `m`',
              '`rt = max(isqrt(k-1), 1)`：`k = 1` 时 `isqrt(0) = 0`，必须保底为 1'],
        summary=['方法二时间 `O(1)`，方法一枚举 `m` 为 `O(k)`',
                 '易错：`k = 1` 时 `rt = 0` 会除零，所以和 1 取最大',
                 '`(k-1)//m` 等于 `ceil(k/m) - 1`，不用写上取整',
                 '主视频演示方法二，方法一是 `min(m - 1 + (k - 1) // m for m in range(1, k + 1))`'],
    ),
)
