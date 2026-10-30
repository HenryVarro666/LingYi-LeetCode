U = 1 << 20


def _u(x):
    return f'{x / U:g}'


def _info(S):
    if 'half' not in S:
        return '每个数先乘 `2^20`，用整数模拟「减半」，不用浮点数'
    return f"还需要再减掉 `half` = =={_u(S['half'])}== 才算减掉一半（图中数字都已除回 `2^20`）"


CONFIG = dict(
    num=2208, title='将数组和减半的最少操作次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='最大堆模拟 + 整数放大',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1550'],
    code='''
class Solution:
    def halveArray(self, nums: List[int]) -> int:
        for i in range(len(nums)):
            nums[i] <<= 20
        heapify_max(nums)

        ans = 0
        half = sum(nums) // 2
        while half > 0:
            half -= nums[0] // 2
            heapreplace_max(nums, nums[0] // 2)
            ans += 1
        return ans
''',
    # Python 3.14 才自带 heapify_max / heapreplace_max；这里用 heapq 的内部函数补上（不被追踪）
    setup='''
def heapify_max(heap):
    heapq._heapify_max(heap)

def heapreplace_max(heap, item):
    ret = heap[0]
    heap[0] = item
    heapq._siftup_max(heap, 0)
    return ret
''',
    call='Solution().halveArray([5, 19, 8, 1])',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='heap', var='nums', label='nums：最大堆（数值已除回 2^20，橙色 = 堆顶 = 当前最大）', top_color='orange', fmt=_u, h=260),
        dict(type='text', fn=lambda S: (f"已经操作 `{S['ans']}` 次，堆里的和 = =={_u(sum(S['nums']))}==" if 'ans' in S else ''), size=26, h=60),
    ],
    watch=[('ans', lambda S: S.get('ans'), 'green'), ('half（原单位）', lambda S: S['half'] / U if 'half' in S else None, 'orange'),
           ('堆顶', lambda S: S['nums'][0] / U, 'pink')],
    captions={
        'nums[i] <<= 20': '`nums[{i}]` 乘 `2^20`：这样减半 20 次内都还是整数（证明见原文链接）',
        'heapify_max(nums)': '原地堆化成==最大堆==，堆顶 = 当前最大的数，`O(n)`',
        'ans = 0': '`ans` 记操作次数',
        'half = sum': lambda S, B, r: f'总和 {_u(sum(S.nums))}，要减掉一半：`half` = =={_u(S.half)}==（放大后是 `{S.half}`）',
        'while half > 0': lambda S, B, r: (f'`half` 还剩 =={_u(S.half)}== > 0，还没减掉一半，继续操作' if S.half > 0
                                          else '`half <= 0`：已经减掉至少一半，结束'),
        'half -= nums[0] // 2': lambda S, B, r: f'贪心：每次选==最大的数== `{_u(B.nums[0])}` 减半，能减掉最多的 `{_u(B.nums[0] // 2)}` → `half` 变成 =={_u(S.half)}==',
        'heapreplace_max': lambda S, B, r: f'把堆顶 `{_u(B.nums[0])}` 换成它的一半 `{_u(B.nums[0] // 2)}`，再向下调整：新的堆顶是 =={_u(S.nums[0])}==',
        'ans += 1': '操作次数 `ans` = =={ans}==',
        'return ans': '返回 =={ret}==',
    },
    skip=['for i in range'],
    max_steps=70,
    cards=dict(
        one_liner='每次把最大的数减半，直到总和减掉一半',
        complexity='时间 `O(n log n)`，空间 `O(1)`（原地）',
        problem=['每次可以选数组中任意一个数，把它减到==恰好一半==',
                 '求让数组和==至少减少一半==的最少操作数',
                 '本视频：`nums = [5,19,8,1]`，和 33 → 答案 `3`'],
        quote='思路是用最大堆来模拟，每次将堆顶减半，累加每次减半的值，直到不低于总和的一半。……将每个数都乘上一个 2 的幂次（比如 2^20）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['减半能减掉「这个数的一半」，所以==每次选最大的数==收益最大：贪心',
              '「取最大 + 放回减半后的值」就是最大堆的 `heapreplace`',
              '为避免浮点误差，每个数先乘 `2^20`：一个数最多减半 20 次，全程都是整数'],
        summary=['每个数最多减半约 20 次，堆操作 `O(log n)`；整体 `O(n log n)`',
                 '易错：`half` 是要减掉的总量，减到 `<= 0` 就停；不是堆里的和',
                 '放大 `2^20` 后用整除 `// 2` 是精确的，不会丢精度',
                 '`heapify_max` / `heapreplace_max` 是 Python 3.14 新增的；旧版本可存相反数'],
    ),
)
