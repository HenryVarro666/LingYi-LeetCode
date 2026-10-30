CONFIG = dict(
    num=2972, title='统计移除递增子数组的数目 II', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='枚举保留的后缀 + 前缀指针单调左移',
    tags=['灵神题单', '难度分 2153'],
    code='''
class Solution:
    def incremovableSubarrayCount(self, a: List[int]) -> int:
        n = len(a)
        i = 0
        while i < n - 1 and a[i] < a[i + 1]:
            i += 1
        if i == n - 1:  # 每个非空子数组都可以移除
            return n * (n + 1) // 2

        ans = i + 2  # 不保留后缀的情况，一共 i+2 个
        # 枚举保留的后缀为 a[j:]
        j = n - 1
        while j == n - 1 or a[j] < a[j + 1]:
            while i >= 0 and a[i] >= a[j]:
                i -= 1
            # 可以保留前缀 a[:i+1], a[:i], ..., a[:0] 一共 i+2 个
            ans += i + 2
            j -= 1
        return ans
''',
    call='Solution().incremovableSubarrayCount([1,3,4,1,2])',
    expect=7,
    views=[
        dict(type='text', fn=lambda S: (f"保留后缀 `a[{S['j']}:]`，前缀最多留到 `a[{S['i']}]`，能删的方案数 = `i + 2` = =={S['i']+2}==" if 'j' in S and 'i' in S and S['j'] < len(S['a']) else '先找最长严格递增前缀，再枚举保留的后缀'), size=30, h=90),
        dict(type='array', var='a', h=200, label='a（蓝 = 保留的前缀 a[:i+1]，粉 = 保留的后缀 a[j:]）',
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: ('pink' if 'j' in S and k >= S['j'] else 'blue' if 'i' in S and 0 <= k <= S['i'] else None)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'while i < n - 1 and a[i] < a[i + 1]': lambda S, B, r: (f"`a[{S.i}] = {S.a[S.i]} < a[{S.i+1}] = {S.a[S.i+1]}` 成立 → 前缀还能延长" if S.i < len(S.a) - 1 and S.a[S.i] < S.a[S.i+1] else f"`a[{S.i}] = {S.a[S.i]}` 之后不再变大 → 最长严格递增前缀到 `i` = =={S.i}== 为止"),
        'i += 1': '前缀还在递增，`i` → {i}',
        'if i == n - 1': '`i == n-1` 吗（{i} vs {n-1}）？不成立：数组不是整体递增，要继续数',
        'ans = i + 2': '先算不保留后缀（删到末尾）的情况：删掉 `a[k:]`，k 取 `i+1 … 0`，共 `i + 2` = =={ans}== 种',
        'j = n - 1': '开始枚举保留的后缀 `a[j:]`，从只留最后一个数开始：`j` = {j}',
        'while j == n - 1': lambda S, B, r: (f"`j = {S.j}` 是最后一位，一个数的后缀必然递增 → 进入循环" if S.j == len(S.a) - 1 else (f"`a[{S.j}] = {S.a[S.j]} < a[{S.j+1}] = {S.a[S.j+1]}` 成立 → 后缀 `a[{S.j}:]` 仍严格递增" if S.a[S.j] < S.a[S.j+1] else f"`a[{S.j}] = {S.a[S.j]} < a[{S.j+1}] = {S.a[S.j+1]}` 不成立 → 后缀不再递增，==停止枚举==")),
        'while i >= 0 and a[i] >= a[j]': '前缀末尾 `a[i]` 必须 `< a[j]`：判断 `a[i] >= a[j]`（i={i}）；不满足就继续左移',
        'i -= 1': '`a[i]` 太大，前缀只能再缩短：`i` → {i}。j 变小后 i 只会往左，所以 ==i 和 j 都不回头==',
        'ans += i + 2': '保留后缀 `a[{j}:]` 时，前缀可留 `a[:i+1]` … `a[:0]`，共 `i+2` = {i+2} 种 → `ans` = =={ans}==',
        'j -= 1': '后缀再加长一位：`j` → {j}，回去检查还严格递增吗',
        'return ans': '没有更长的递增后缀了，一共 =={ans}== 种',
    },
    cards=dict(
        one_liner='删掉中间一段，剩下的是「递增前缀 + 递增后缀」，枚举后缀、前缀指针只左移',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删掉 `nums` 的一个非空子数组，若剩下的元素严格递增，就算一种',
                 '求这样的子数组共有多少个（剩下空数组也算递增）',
                 '本视频：`[1,3,4,1,2]` → `7`'],
        quote='设后缀的第一个数为 a[j]……枚举 j 的同时，维护最长前缀的最后一个数的下标 i（满足 a[i] < a[j]）……由于 j 越小，a[j] 越小，a[i] 也越小，有单调性。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先数「只留前缀」的情况：最长递增前缀末位是 `i`，共 `i+2` 种',
              '再枚举保留后缀 `a[j:]`：前缀末尾必须 `< a[j]`，由 `i` 向左找',
              '`j` 左移时 `a[j]` 变小，`i` 只会更靠左，所以像滑动窗口一样双指针'],
        summary=['时间 `O(n)`：`i` 和 `j` 都只减不增（`i` 先右移一遍，再只左移）',
                 '`i = -1` 时前缀为空，只有 1 种，正好是 `i + 2`',
                 '整个数组严格递增要先特判，答案是 `n(n+1)/2`',
                 '思考题：1574 删除最短的子数组使剩余数组有序'],
    ),
)
