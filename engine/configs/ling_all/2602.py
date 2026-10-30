def _col(S, i, v):
    if 'j' in S and 'left' in S:
        return 'blue' if i < S['j'] else 'green'
    return None


def _txt(S):
    if 'left' not in S or 'j' not in S:
        return '排序后，比 q 小的数涨到 q（蓝），比 q 大的数降到 q（绿）'
    q, j, n, s = S['q'], S['j'], len(S['nums']), S['s']
    return (f'`q={q}`：小的 `{j}` 个数涨到 q → `{q}×{j} − {s[j]}` = =={q * j - s[j]}==；'
            f'大的 `{n - j}` 个降到 q → ==' + (str(S['right']) if 'right' in S and S.get('_line', 0) >= 11 else '?') + '==')


CONFIG = dict(
    num=2602, title='使数组元素全部相等的最少操作次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='排序 + 前缀和 + 二分',
    tags=['前缀和', '难度分 1903'],
    code='''
class Solution:
    def minOperations(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)
        nums.sort()
        s = list(accumulate(nums, initial=0))  # 前缀和

        ans = []
        for q in queries:
            j = bisect_left(nums, q)
            left = q * j - s[j]  # 蓝色面积
            right = s[n] - s[j] - q * (n - j)  # 绿色面积
            ans.append(left + right)
        return ans
''',
    call='Solution().minOperations([3,1,6,8], [1,5])',
    expect=[14, 10],
    views=[
        dict(type='array', var='nums', label='nums（排序后；蓝 = 比 q 小，绿 = 不小于 q）', h=170,
             color=lambda S, i, v: _col(S, i, v), pointers={'j': 'pink'}),
        dict(type='array', var='s', label='s：前缀和', h=150, pointers={'j': 'pink'}),
        dict(type='array', var='queries', label='queries', h=130, pointers={'_none': 'blue'}, dim=lambda S, i, v: 'q' in S and v != S['q']),
        dict(type='array', var='ans', label='ans', h=130, pointers={'_none': 'blue'}),
        dict(type='text', fn=_txt, h=60),
    ],
    watch=['q', 'j', ('left', 'left', 'blue'), ('right', 'right', 'green'), ('ans', 'ans', 'green')],
    captions={
        'nums.sort()': '先排序：这样「比 q 小」的数就是一段前缀，`nums = {nums}`',
        's = list(accumulate': '前缀和 `s = {s}`：`s[j]` 是排序后前 j 个数之和',
        'for q in queries': lambda S, B, r: ('查询都处理完了' if 'q' in B and B.q == S.q and B.get('ans') == S.ans and len(S.ans) == 2
                                              else f'处理查询 `q = {S.q}`：每次查询互相独立，数组各自恢复'),
        'bisect_left': '二分找第一个 `≥ {q}` 的位置：`j = {j}`，前 `{j}` 个数比 `{q}` 小',
        'left = ': '比 q 小的 `{j}` 个数都要涨到 q：`{q}×{j} − s[{j}]` = `{q * j} − {s[j]}` = =={left}==（蓝色面积）',
        'right = ': '其余 `{n - j}` 个数都要降到 q：`s[{n}] − s[{j}] − {q}×{n - j}` = =={right}==（绿色面积）',
        'ans.append': '这个查询的答案 `{left} + {right}` = =={left + right}==，放入 ans',
        'return ans': '所有查询答完：`{ans}`',
    },
    cards=dict(
        one_liner='排序后二分切开：小的涨到 q，大的降到 q，前缀和一次算完',
        complexity='时间 `O((n+q)log n)`，空间 `O(n)`',
        problem=['每次查询把 `nums` 中所有数变成 `queries[i]`，每次操作某个数 ±1',
                 '求每个查询的最少操作次数（查询之间互不影响）',
                 '示例：`[3,1,6,8]`，`queries=[1,5]` → `[14,10]`'],
        quote='关于二分查找，请看二分查找红蓝染色法。关于前缀和数组的定义，请看前缀和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['变成 q 的最少操作 = 每个数到 q 的距离之和',
              '排序后 `bisect_left` 把数组切成「小于 q」和「不小于 q」两段',
              '左段：`q×j − 前缀和`；右段：`后缀和 − q×(n−j)`，各 `O(1)`'],
        summary=['排序 `O(n log n)`，每次查询二分 `O(log n)`',
                 '`bisect_left` 返回的 `j` 就是比 q 小的个数，等于 q 的数距离为 0，归哪边都行',
                 '`accumulate(..., initial=0)` 让 `s[0]=0`，`s` 长度是 `n+1`',
                 '易错：`nums.sort()` 会原地修改；yiduobo 把询问也排序，用单调性代替二分'],
    ),
)
