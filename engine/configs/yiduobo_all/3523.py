NUMS = [4, 2, 6, 3, 5, 7, 1]


def _cur(S):
    if 'v' not in S:
        return None
    return S['nums'].index(S['v'])


def _kept(a, i):
    return i == 0 or a[i] >= max(a[:i])


def _color(S, i, v):
    c = _cur(S)
    if c is None or i > c:
        return None
    if i == c and S['_line'] in (6, 7):
        return 'blue'
    return 'green' if _kept(S['nums'], i) else 'red'


def _dim(S, i, v):
    c = _cur(S)
    return c is not None and i < c and not _kept(S['nums'], i)


def _txt(S):
    if 'v' not in S:
        return '被消除的元素不会留下，`ma` 始终是剩余数组的最后一个元素'
    return f"当前 `v = {S['v']}`，剩余数组最后一个元素 `ma = {S['ma']}`，当前长度 ==`{S['res']}`=="


CONFIG = dict(
    num=3523, title='非递减数组的最大长度', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='一趟遍历 · 小于前一个就消除',
    tags=['灵神题单', '贪心与思维', '难度分 1435'],
    code='''
class Solution(object):
    def maximumPossibleSize(self, nums):
        
        ma = nums[0]
        res = len(nums)
        for v in nums[1:]:
            if v < ma:
                res -= 1
            else:
                ma = v
        
        return res
''',
    call=f'Solution().maximumPossibleSize({NUMS})',
    expect=3,
    views=[
        dict(type='text', fn=_txt),
        dict(type='array', var='nums', color=_color, dim=_dim, h=300),
    ],
    watch=[('ma', 'ma', 'cyan'), ('res', 'res', 'green')],
    captions={
        'ma = nums[0]': '`ma` 记录剩余数组最后一个元素；第一个元素前面没有东西，必定保留：`ma = {ma}`',
        'res = len': '先假设一个都不删，`res = {res}`，每消除一个就减 1',
        'for v in nums': lambda S, B, r: ('`nums[1:]` 遍历完了，退出循环' if B.get('v') == S.v and S.nums.index(S.v) == len(S.nums) - 1 and 'v' in B else f'检查下一个元素 `v = {S.v}`'),
        'if v < ma': lambda S, B, r: (
            f'`v = {S.v}` < 前一个 `ma = {S.ma}`：前面是非递减的不能动 → ==v 必须被消除=='
            if S.v < S.ma else f'`v = {S.v}` ≥ `ma = {S.ma}`：不用消除'),
        'res -= 1': '消除 `v`，不管具体怎么操作它都会被合并掉，`res` → {res}；`ma` 不变',
        'ma = v': '`v` 保留，成为新的最后一个元素：`ma = {ma}`',
        'return res': '最大长度 `{res}`',
    },
    cards=dict(
        one_liner='比前一个小的元素必被消除，数一数被消除了几个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作：把一个子数组替换成它的最大值',
                 '操作若干次后数组要非递减，求最大可能长度',
                 '示例：`[4,2,5,3,5]` → `3`；本视频用 `[4,2,6,3,5,7,1]`'],
        quote='若v小于其前一个元素，在这里就必须通过操作将v消除掉。在这里不能消除掉v的前一个元素，因为前面的部分是非递减的。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，逐个和「剩余数组的最后一个元素」比较',
              '`v < ma`：`v` 无论和谁合并自己都会消失，答案减 1',
              '被消除后下一个元素要和它的前一个比，所以用变量 `ma` 记录最后一个'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ma` 只在 `v >= ma` 时更新，被消除的元素不改它',
                 '从 `nums[1:]` 开始遍历，首元素直接保留',
                 '对比灵神：他数「保留」的，yiduobo 数「消除」的，用 `len(nums)` 倒着减'],
    ),
)
