def _poshow(S):
    if 'pos' not in S:
        return ''
    n = len(S['nums'])
    parts = []
    for x in range(n):
        p = S['pos'][x]
        if p or x < 4:
            parts.append(f"pos[{x}]={list(reversed(p))}")
    s = '　'.join(parts)
    if 'mex' in S and 'start' in S:
        s += f"　｜　这一段 `start={S['start']}`，正在试 `mex={S['mex']}`"
    return s


CONFIG = dict(
    num=3948, title='字典序最大的 MEX 数组', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 每段贪心凑最大 mex',
    tags=['难度分 2122'],
    code='''
class Solution:
    def maximumMEX(self, nums: list[int]) -> list[int]:
        n = len(nums)
        # mex 最大是 n，>= n 的数无需考虑
        pos = [[] for _ in range(n + 1)]  # n 作为哨兵
        for i, x in enumerate(nums):
            if x < n:
                pos[x].append(i)
        for p in pos:
            p.reverse()

        ans = []
        i = 0
        while i < n:
            start = i  # 这一段的起点
            # 枚举这一段的 mex，越大越好（字典序越大）
            mex = 0
            while True:
                # 清理在 start 之前的下标
                q = pos[mex]
                while q and q[-1] < start:
                    q.pop()
                if not q:
                    break
                # 这一段包含剩余元素中的最左边的 mex
                i = max(i, q[-1])
                mex += 1
            ans.append(mex)
            i += 1
        return ans
''',
    call='Solution().maximumMEX([0,1,0,2,0,1,0])',
    expect=[3, 2, 1],
    views=[
        dict(type='array', var='nums', label='nums', h=300, pointers={'start': 'blue', 'i': 'pink'},
             window=('start', 'i'),
             dim=lambda S, k, v: 'start' in S and k < S['start']),
        dict(type='array', var='ans', label='ans', h=170, color=lambda S, k, v: 'green'),
        dict(type='text', fn=_poshow, size=26, h=120),
    ],
    watch=[('start', 'start', 'blue'), ('i', 'i', 'pink'), 'mex', ('ans', 'ans', 'green')],
    skip=['for p in pos', 'p.reverse()', 'if x < n', 'for i, x in', 'while True', 'q = pos[mex]', 'break', 'mex += 1', 'i += 1', 'while i < n:', 'i = 0'],
    captions={
        'pos = [[]': '`pos[x]` 记录数字 `x` 出现的所有下标；mex 最大只会是 `n`，所以 >= n 的数不用记',
        'pos[x].append': '数字 `{x}` 出现在下标 `{i}`：`pos[{x}] = {pos[x]}`',
        'ans = []': '每个 `pos[x]` 已反转（下标降序），`q[-1]` 就是最左边的下标，用 `pop()` 就能 O(1) 删掉最左边',
        'start = i': '新的一段从 `{start}` 开始（外层循环负责准备工作）',
        'mex = 0': '这一段从 `mex = 0` 开始往上试，mex 越大字典序越大',
        'while q and q[-1] < start': lambda S, B, ret: (f"`pos[{S['mex']}]` 最左下标 `{S['q'][-1]}` < `start={S['start']}`：已经在前面的段里，不能用，弹掉" if S['q'] and S['q'][-1] < S['start'] else (f"`pos[{S['mex']}]` 里没有 ≥ {S['start']} 的下标了" if not S['q'] else f"`pos[{S['mex']}]` 最左下标 `{S['q'][-1]}` ≥ `start={S['start']}`，没有要清理的")),
        'if not q': lambda S, B, ret: (f"剩下的元素不含 `{S['mex']}`：这一段的 mex 最多就是 =={S['mex']}==，再延长也不会变大 → 跳出，切一刀" if not S['q'] else f"`pos[{S['mex']}]` 非空：剩余元素里有 `{S['mex']}`，可以继续"),
        'i = max(i, q[-1])': '为了让 mex 更大，这一段必须包含剩余元素里最左边的 `{mex}`（下标 `{q[-1]}`）→ 段尾推进到 `i = {i}`，然后试 `mex = {mex+1}`',
        'ans.append': '这一段切好：mex = =={mex}==，加入答案 → `{ans}`。mex 不再增大时就切，下一段从 `{i+1}` 开始',
    },
    cards=dict(
        one_liner='mex 不会再变大时立刻切一刀，把更多元素留给后面',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `nums` 切成若干段，每段算一个 ==mex==（段内没有的最小非负整数）',
                 '各段 mex 依次组成 `result`，求 ==字典序最大== 的 `result`',
                 '示例：`[0,1,0,2,0,1,0]` → `[3,2,1]`'],
        quote='子数组 mex 的性质是，子数组越长，mex 越大（或者不变）。当 mex 无法再增大时，切一刀是最合适的，因为剩下的元素越多，下一个 mex 的值就越大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用 `pos[x]` 记下每个数的所有下标',
              '每一段枚举 `mex = 0, 1, 2…`：剩余元素里有它，就把最左边那个纳入本段',
              '剩余元素里没有 `mex` 就切断，这是「分组循环」：外层准备/统计，内层找段尾'],
        summary=['时间 `O(n)`：`i` 只增不减，每个下标至多被弹出一次',
                 '`pos[x]` 反转后用列表的 `pop()` 代替队列，题解还给了 deque 写法',
                 '易错点：清理的是 `start` 之前的下标，而不是 `i` 之前的',
                 '分组循环不用特判最后一组，是最不容易出 bug 的写法'],
    ),
)
