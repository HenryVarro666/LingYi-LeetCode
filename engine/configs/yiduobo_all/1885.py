CONFIG = dict(
    num=1885, title='统计数对', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差值数组 + 树状数组',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def countPairs(self, nums1, nums2):
        n = len(nums1)
        d = [nums1[index] - nums2[index] + 100000 for index in range(n)]
        res = 0

        f = [0] * 200000

        def get(x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s
        
        def add(x):
            while x < 200000:
                f[x] += 1
                x += x & -x

        for index in range(n - 1, -1, -1):
            res += (n - index - 1) - get(200000 - d[index])
            add(d[index])
        
        return res
''',
    call='Solution().countPairs([1, 10, 6, 2], [1, 4, 1, 5])',
    expect=5,
    skip=['n = len(nums1)', 'res = 0', 'f = [0]', 's = 0', 'return s', 'x -= x & -x', 'x += x & -x', 'while x > 0', 'while x < 200000', 's += f[x]', 'f[x] += 1'],
    max_steps=110,
    views=[
        dict(type='text', fn=lambda S: (f"i = `{S['index']}`：`d[i] = {S['d'][S['index']] - 100000}`（加偏移后 {S['d'][S['index']]}）。找右边满足 d[j] + d[i] > 0 的 j" if 'index' in S and 'd' in S and 'f' in S else ''), h=60),
        dict(type='array', var=lambda S: [v - 100000 for v in S['d']], label='d[i] = nums1[i] − nums2[i]（程序里再加 100000 当下标；绿 = 已加入树状数组）', pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and i > S['index'] else None, h=190),
        dict(type='map', var=lambda S: {i: v for i, v in enumerate(S['f']) if v}, label='树状数组 f（只列出非 0 的位置：下标 → 计数）', fmt=lambda k, v: f'f[{k}] = {v}', h=190),
    ],
    watch=[('index', 'index', 'blue'), 'x', 's', ('res', 'res', 'green')],
    captions={
        'd = [': '`d[i] = nums1[i] − nums2[i]`，条件变成 `d[i] + d[j] > 0`；加偏移 100000 让下标为正：`d = {d}`',
        'f = [0]': '树状数组 `f`：下标 `1..199999`，记录“出现过的 d 值”的个数',
        'for index in range(n - 1, -1, -1)': lambda S, B, r: (f'`index = {S.index}`：从后往前，右边的 d 都已加入树状数组' if B.get('index') != S.index or 'res' not in B else '所有 i 都处理完了'),
        'res += (n - index - 1) - get(': lambda S, B, r: (lambda q, hops: f'右边共 `{len(S.nums1) - S.index - 1}` 个数；`get({q})` 沿 lowbit 向前跳 `{hops}` 步，数出右边 `d[j] <= {q}` 的个数（配不上的），其余才满足 `d[j] > {q}`')(200000 - S.d[S.index], bin(200000 - S.d[S.index]).count('1')),
        'add(d[index])': lambda S, B, r: (lambda nodes: f'把 `d[{S.index}] = {S.d[S.index]}` 加入树状数组：沿 lowbit 向后更新 `{len(nodes)}` 个节点 `{nodes[:4]}…`，供更左边的 i 查询；此时 `res = {S.res}`')(list(__import__("itertools").takewhile(lambda v: v < 200000, __import__("itertools").accumulate([S.d[S.index]] + [0]*40, lambda a_, _: a_ + (a_ & -a_))))),
        'return res': '满足条件的数对一共 `{res}` 个',
    },
    cards=dict(
        one_liner='移项成 d[i]+d[j]>0，从后往前用树状数组数个数',
        complexity='时间 `O(n log C)`，空间 `O(C)`（`C = 2×10^5`）',
        problem=['给两个等长数组 `nums1`、`nums2`，数对 `(i, j)` 满足 `i < j`',
                 '且 `nums1[i] + nums1[j] > nums2[i] + nums2[j]`，求数对个数',
                 '示例：`[1,10,6,2]`、`[1,4,1,5]` → `5`'],
        quote='题目中数对的计算方法是nums1[i] + nums1[j] > nums2[i] + nums2[j]，移项后就是(nums1[i] - nums2[i]) + (nums1[j] - nums2[j]) > 0，那么就可以预处理出一个数组d。',
        quote_src='—— yiduobo 题解原文',
        idea=['`d[i] = nums1[i] − nums2[i]`，问题变成：数 `i < j` 且 `d[i] + d[j] > 0` 的对数',
              '`d` 在 `[-99999, 99999]`，加 `100000` 变成正数，才能当树状数组下标',
              '从后往前：右边满足 `d[j] > 200000 − d[i]` 的个数 = 右边总数 − `d[j] <= 200000 − d[i]` 的个数',
              '后者就是树状数组的前缀和'],
        summary=['时间 `O(n log C)`，空间 `O(C)`',
                 '易错点：偏移后条件是 `d[i] + d[j] > 200000`，两个数各加了 100000',
                 '树状数组下标从 1 开始，所以偏移还保证了 `d >= 1`',
                 '原文为 Python 2 风格，代码未改动（已使用 `range`，无整数除法）',
                 '也可以排序 + 双指针做到 `O(n log n)`'],
    ),
)
