def _b(S):
    return [x - 1 - i for i, x in enumerate(S['arr'])]


def _info(S):
    if 'left' not in S:
        return '`b[i] = arr[i] - 1 - i`：`arr[i]` 之前缺了多少个正整数'
    b = _b(S)
    return f'`b = {b}`（递增），找第一个 `b[i] >= k = {S["k"]}` 的下标'


CONFIG = dict(
    num=1539, title='第 k 个缺失的正整数', difficulty='Easy', category='二分算法',
    author='灵茶山艾府', technique='二分 arr[i]-1-i · 红蓝染色',
    tags=['灵神题单'],
    code='''
class Solution:
    def findKthPositive(self, arr: list[int], k: int) -> int:
        left = -1
        right = len(arr)
        while left + 1 < right:
            mid = (left + right) // 2
            if arr[mid] - 1 - mid >= k:
                right = mid
            else:
                left = mid
        return right + k  # 推导过程见题解
''',
    call='Solution().findKthPositive([2, 3, 4, 7, 11], 5)',
    expect=9,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='arr', pointers={'left': 'blue', 'mid': 'yellow', 'right': 'pink'}, cell=96, h=260,
             color=lambda S, i, v: ('green' if 'mid' in S and i == S['mid'] and v - 1 - i >= S['k'] else
                                    'blue' if 'mid' in S and i == S['mid'] else None)),
        dict(type='array', var=lambda S: [x - 1 - i for i, x in enumerate(S['arr'])], label='b[i] = arr[i] - 1 - i（缺失个数）',
             cell=96, h=200,
             color=lambda S, i, v: 'green' if v >= S.get('k', 10 ** 9) else None),
    ],
    watch=[('left', 'left', 'blue'), ('mid', 'mid', 'yellow'), ('right', 'right', 'pink'), ('k', 'k', 'green')],
    captions={
        'left = -1': '红蓝染色：`left = -1` 视为蓝（`b < k`）',
        'right = len': '`right = {right}` 视为红（`b >= k`），开区间 `({left}, {right})`',
        'while left + 1 < right': lambda S, B, r: (f'`{S.left} + 1 < {S.right}`，开区间里还有数' if S.left + 1 < S.right
                                                   else f'`{S.left} + 1 >= {S.right}`，区间空了：`right` 就是第一个 `b >= k` 的下标'),
        'mid = (left + right)': '`mid = ({left} + {right}) // 2 = {mid}`',
        'if arr[mid] - 1 - mid >= k': lambda S, B, r: (
            f'`arr[{S.mid}] - 1 - {S.mid} = {S.arr[S.mid] - 1 - S.mid}` >= `k = {S.k}` → ==红色==，缺的数已经够 k 个了'
            if S.arr[S.mid] - 1 - S.mid >= S.k else
            f'`arr[{S.mid}] - 1 - {S.mid} = {S.arr[S.mid] - 1 - S.mid}` < `k = {S.k}` → ==蓝色==，缺的数还不够 k 个'),
        'right = mid': '`mid` 是红的 → `right = {right}`',
        'left = mid': '`mid` 是蓝的 → `left = {left}`',
        'return right + k': '`right = {right}`：答案 = `right + k = {right} + {k}` = =={ret}==（推导：`arr[i]-1-(arr[i]-1-i-k) = i+k`）',
    },
    cards=dict(
        one_liner='arr[i]-1-i 是 arr[i] 之前缺的个数，它递增 → 二分',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['严格升序的正整数数组 `arr`，求第 `k` 个缺失的正整数',
                 '示例：`arr=[2,3,4,7,11]`，`k=5` → 缺失 `1,5,6,8,9,...` → `9`',
                 '进阶：做到小于 `O(n)`'],
        quote='在 arr[i] 之前缺失的正整数个数：arr[i] - 1 - i。设 b[i] = arr[i] - 1 - i，b 是（非严格）递增数组。',
        quote_src='—— 灵茶山艾府题解（节选）',
        idea=['`arr[i]` 之前有 `arr[i]-1` 个正整数，其中 `i` 个在数组里，缺 `arr[i]-1-i` 个',
              '`b` 递增 → 二分找第一个 `b[i] >= k` 的 `i`',
              '从 `arr[i]-1` 往前数几个，化简后答案恰好是 `i + k`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '二分的是 `b[i] = arr[i]-1-i`，不要真的建数组 b',
                 '答案 `right + k`：`right` 可以等于 `n`（所有缺失都在 arr 之后），也成立',
                 '题解还给了 `bisect_left(range(n), True, key=...)` 的库函数写法'],
    ),
)
