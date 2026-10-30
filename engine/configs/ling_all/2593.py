def _picked(nums):
    n = len(nums)
    vis = [False] * n
    res = set()
    for x, i in sorted((x, i) for i, x in enumerate(nums)):
        if not vis[i]:
            res.add(i)
            for k in (i - 1, i, i + 1):
                if 0 <= k < n:
                    vis[k] = True
    return res


def _green(S, i, v):
    if 'i' not in S:
        return False
    P = _picked(S['nums'])
    if i not in P:
        return False
    L = S['_line']
    if L == 12:
        return True
    if L in (5, 6):
        return i < S['i']
    if i < S['i0']:
        return True
    if L in (9, 10, 11) and 'j' in S:
        return S['i0'] <= i <= S['i'] and i >= S['j']
    return False


def _info(S):
    if 'i' not in S:
        return ''
    L = S['_line']
    if L in (9, 10, 11) and 'j' in S and S['i0'] <= S['j'] <= S['i']:
        return f"下坡段 `[{S['i0']}, {S['i']}]`：从坡底往左隔一个取，当前取 `nums[{S['j']}]` = =={S['nums'][S['j']]}=="
    if L in (7, 8) and 'i0' in S:
        return f"找下坡的坡底：从 `{S['i0']}` 往右，只要递减就继续"
    return ''


CONFIG = dict(
    num=2593, title='标记所有元素后数组的分数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 严格递减段隔一个取',
    tags=['灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def findScore(self, nums: List[int]) -> int:
        ans = 0
        i, n = 0, len(nums)
        while i < n:
            i0 = i
            while i + 1 < n and nums[i] > nums[i + 1]:  # 找到下坡的坡底
                i += 1
            for j in range(i, i0 - 1, -2):  # 从坡底 i 到坡顶 i0，每隔一个累加
                ans += nums[j]
            i += 2  # i 选了 i+1 不能选
        return ans
''',
    call='Solution().findScore([6,5,4,3,7,2])',
    expect=10,
    views=[
        dict(type='array', var='nums', pointers={'i0': 'blue', 'i': 'pink', 'j': 'cyan'}, window=('i0', 'i'), h=300,
             color=lambda S, i, v: 'green' if _green(S, i, v) else None),
        dict(type='text', h=90, size=30, fn=_info),
    ],
    watch=[('i0', 'i0', 'blue'), ('i', 'i', 'pink'), 'j', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans = 0`：累计分数',
        'i, n = 0': '`i` 从左往右扫，只增不减；`n = {n}`',
        'while i < n': lambda S, B, r: (f"`i = {S.i} < {S.n}`：还有没处理的元素，开始新的一组" if S.i < S.n else f"`i = {S.i} >= {S.n}`：全部处理完 → 结束"),
        'i0 = i': '这一组从 `i0 = {i0}` 开始：把数组看成若干个==严格递减段==',
        'while i + 1 < n and': lambda S, B, r: (f"`nums[{S.i}] > nums[{S.i+1}]`（{S.nums[S.i]} > {S.nums[S.i+1]}）→ 还在下坡" if S.i + 1 < S.n and S.nums[S.i] > S.nums[S.i+1] else (f"`nums[{S.i}] > nums[{S.i+1}]` 不成立（{S.nums[S.i]} ≤ {S.nums[S.i+1]}）→ 到坡底了" if S.i + 1 < S.n else "已经是最后一个元素 → 到坡底了")),
        'i += 1': '继续下坡：`i` → {i}',
        'for j in range': lambda S, B, r: ("这一段取完了（`range` 里没有更多的 j）" if B.get('j') == S.j else f"先取坡底 `j = {S.j}`：`nums[{S.j}]` = {S.nums[S.j]} 比左边小、不超过右边，一定能选" if S.j == S.i else f"往左隔一个：`j = {S.j}`（`nums[{S.j+1}]` 被右边的已选数标记了，跳过）"),
        'ans += nums[j]': '选中 `nums[{j}]` = {nums[j]}，`ans = {B.ans} + {nums[j]}` = =={ans}==',
        'i += 2': '坡底 `{B.i}` 被选，右边 `{B.i + 1}` 被标记不能选 → 下一组从 `i = {i}` 开始',
        'return ans': '总分 `{ans}`',
    },
    cards=dict(
        one_liner='把数组切成严格递减的下坡段，每段从坡底往左隔一个取',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选最小的未标记数（相等取下标小的）加到分数，并标记它和左右邻居',
                 '重复到全部被标记，求总分',
                 '示例：`[2,1,3,4,5,2]` → `7`；本视频：`[6,5,4,3,7,2]` → `10`'],
        quote='严格递减子段的最小值 nums[i] 一定可以选，因为它比 nums[i-1] 小，且不会超过 nums[i+1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数组 = 若干严格递减段，例如 `[2,1] [3] [4] [5,2]`',
              '坡底先被选，右邻居被标记；左边 `i-2, i-4, …` 也轮到被选',
              '`i` 只增不减，一趟扫完不需要排序'],
        after=[dict(heading='另一种写法', lines=['方法一：带着下标排序，按值从小到大模拟，用 `vis` 标记', '时间 `O(n log n)`，空间 `O(n)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '坡底 `i` 选完后 `i += 2`：`i+1` 已被标记，不能选',
                 '相等时靠"从左往右"遍历保证选到下标更小的',
                 '分组循环：外层记起点，内层找终点，最后一组不用特判'],
    ),
)
