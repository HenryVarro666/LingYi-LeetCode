CONFIG = dict(
    num=2970, title='统计移除递增子数组的数目 I', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前缀 + 后缀双指针',
    tags=[],
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
        dict(type='text', size=26, fn=lambda S: (
            f"保留前缀 `a[:{S['i']+1}]`，后缀 `a[{S['j']}:]` → 可移除 `{S['i']}+2 = {S['i']+2}` 个" if 'j' in S and S['i'] >= -1 and S['_line'] in (14, 15, 17)
            else '先找最长严格递增前缀，再枚举保留的后缀' )),
        dict(type='array', var='a', pointers={'i': 'blue', 'j': 'pink'}, cell=96, h=260,
             color=lambda S, k, v: ('green' if (k <= S['i']) else ('purple' if ('j' in S and k >= S['j']) else None)) if 'j' in S else ('green' if k <= S.get('i', -1) else None)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'n = len(a)': '`n = {n}`',
        'i = 0': '`i` 指向最长严格递增前缀的最后一个数',
        'while i < n - 1 and a[i] < a[i + 1]': lambda S, B, r: (f'`a[{S.i}] < a[{S.i+1}]`（{S.a[S.i]} < {S.a[S.i+1]}）→ 前缀还能继续延长' if S.i < S.n - 1 and S.a[S.i] < S.a[S.i+1] else f'`a[{S.i}] >= a[{S.i+1}]` 或到头了 → 最长递增前缀到 `i = {S.i}` 为止' if S.i < S.n - 1 else '`i` 到了末尾 → 整个数组严格递增'),
        'i += 1': '前缀延长一位：`i` → `{i}`',
        'if i == n - 1': lambda S, B, r: ('`i == n - 1`：整个数组递增，任何非空子数组移除后都递增' if S.i == S.n - 1 else f'`i = {S.i} != n - 1 = {S.n-1}`：不是严格递增数组，继续一般情况'),
        'return n * (n + 1) // 2': '非空子数组个数 `{n}×{n+1}/2` = =={ret}==',
        'ans = i + 2': '后缀全部移除：可保留前缀 `a[:i+1], ..., a[:0]`，共 `i+2 = {ans}` 个',
        'j = n - 1': '从最右开始枚举保留的后缀 `a[j:]`，`j = {j}`',
        'while j == n - 1 or': lambda S, B, r: ('`j == n - 1`：只保留最后一个数，必然递增，可以枚举' if S.j == S.n - 1 else (f'`a[{S.j}] < a[{S.j+1}]`（{S.a[S.j]} < {S.a[S.j+1]}）→ 后缀 `a[{S.j}:]` 仍严格递增，继续' if S.a[S.j] < S.a[S.j+1] else f'`a[{S.j}] >= a[{S.j+1}]`（{S.a[S.j]} >= {S.a[S.j+1]}）→ 后缀不再递增，停止枚举')),
        'while i >= 0 and a[i] >= a[j]': lambda S, B, r: (f'前缀末尾 `a[{S.i}] = {S.a[S.i]}` >= 后缀开头 `a[{S.j}] = {S.a[S.j]}` → 拼不起来，前缀缩短，`i` 左移' if S.i >= 0 and S.a[S.i] >= S.a[S.j] else ('`i = -1`：前缀已空，只能移除 `a[:j]`' if S.i < 0 else f'`a[{S.i}] = {S.a[S.i]} < a[{S.j}] = {S.a[S.j]}` → 前缀合法，停止左移')),
        'i -= 1': '`i` → `{i}`（j 变小后 a[j] 更小，所以 i 只会左移不会回头）',
        'ans += i + 2': '固定 `j = {j}`：可保留前缀 `a[:{i+1}] ... a[:0]` 共 `{i}+2` 个，`ans` → =={ans}==',
        'j -= 1': '后缀向左扩一位：`j` → `{j}`',
        'return ans': '一共 `{ans}` 个移除递增子数组',
    },
    cards=dict(
        one_liner='剩下的是递增前缀 + 递增后缀：枚举后缀，前缀只会越缩越短',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['移除一个非空子数组后，剩余元素要==严格递增==（空数组也算）',
                 '求这样的子数组总数',
                 '示例：`[1,3,4,1,2]` → `7`'],
        quote='移除子数组后，剩下的部分是一个前缀加一个后缀，需要满足：前缀是严格递增的；后缀是严格递增的；前缀的最后一个数严格小于后缀的第一个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先数「移除后缀」的情况：最长递增前缀末尾是 `i`，共 `i+2` 个',
              '枚举保留的后缀 `a[j:]`（必须递增），前缀末尾 `i` 满足 `a[i] < a[j]`，可保留 `i+2` 种前缀',
              'j 越小 a[j] 越小，`i` 只会左移 → 像滑动窗口一样总共 `O(n)`'],
        summary=['时间 `O(n)`，空间 `O(1)`：i、j 都只减小',
                 '整个数组严格递增时要特判，答案是 `n(n+1)/2`',
                 '`i = -1` 时 `i+2 = 1`，正好对应移除 `a[:j]`，不用特判',
                 '变形：1574 删除最短的子数组使剩余数组有序'],
    ),
)
