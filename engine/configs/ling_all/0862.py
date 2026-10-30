_S = [0, 2, 1, 3, 1, 2, 5]


CONFIG = dict(
    num=862, title='和至少为 K 的最短子数组', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 + 单调队列',
    tags=['单调队列', '前缀和', '难度分 2307'],
    code='''
class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        ans = inf
        s = list(accumulate(nums, initial=0))  # 计算前缀和
        q = deque()
        for i, cur_s in enumerate(s):
            while q and cur_s - s[q[0]] >= k:
                ans = min(ans, i - q.popleft())  # 优化一
            while q and s[q[-1]] >= cur_s:
                q.pop()  # 优化二
            q.append(i)
        return ans if ans < inf else -1
''',
    call='Solution().shortestSubarray([2,-1,2,-2,1,3], 4)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', h=190, pointers={}),
        dict(type='array', var='s', label='前缀和 s（蓝 = 在队列里，粉箭头 = 当前 i）', pointers={'i': 'pink'}, h=220,
             color=lambda S, i, v: 'blue' if i in (S.get('q') or []) and i != S.get('i') else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='queue', var='q', label='单调队列 q（下标:前缀和，队首最小、从左到右递增）', fmt=lambda i: f'{i}:{_S[i]}', h=130),
        dict(type='text', fn=lambda S: (f"当前 `s[{S['i']}] = {S['cur_s']}`，队首 `s[{S['q'][0]}] = {S['s'][S['q'][0]]}`：差 = =={S['cur_s'] - S['s'][S['q'][0]]}== （k = {S['k']}）"
                                        if 'cur_s' in S and S.get('q') else ''), h=60),
    ],
    watch=[('i', 'i', 'pink'), ('cur_s', 'cur_s', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = inf': '`ans = inf`：还没找到合法子数组',
        'accumulate(nums, initial=0)': '前缀和 `s = {s}`：子数组 `[j, i)` 的和 = `s[i] − s[j]`',
        'q = deque()': '队列里存==前缀和的下标==，队首是最靠左（最早）的候选左端点',
        'for i, cur_s': '枚举右端点：`i = {i}`，`cur_s = s[{i}] = {cur_s}`',
        'while q and cur_s - s[q[0]] >= k': lambda S, B, r: (
            f'`{S.cur_s} − {S.s[S.q[0]]} = {S.cur_s - S.s[S.q[0]]} ≥ {S.k}`：队首当左端点够用了' if S.q and S.cur_s - S.s[S.q[0]] >= S.k
            else ('队列空了，停止' if not S.q else f'`{S.cur_s} − {S.s[S.q[0]]} = {S.cur_s - S.s[S.q[0]]} < {S.k}`：不够，停止')),
        'ans = min(ans, i - q.popleft())': '队首出队，更新答案：长度 `i − 队首下标`，`ans` = =={ans}==。==出队后不会再用==：以后的右端点只会更远、更长',
        'while q and s[q[-1]] >= cur_s': lambda S, B, r: (
            f'队尾 `s[{S.q[-1]}] = {S.s[S.q[-1]]} ≥ {S.cur_s}`：又靠左又更大，比新来的差 → ==没用了==' if S.q and S.s[S.q[-1]] >= S.cur_s
            else '队尾比 `cur_s` 小（或队列空）→ 保留，停止'),
        'q.pop()': '弹掉队尾：以它为左端点，差永远不如 `cur_s`，而且更长',
        'q.append(i)': '`{i}` 入队：队列里的前缀和保持==严格递增==',
        'return ans if ans < inf else -1': '`ans = {ans}`，有合法子数组 → 返回 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='及时移除没用的前缀和，让队列保持递增',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找和 ==至少为 `k`== 的最短非空子数组，没有则 `-1`',
                 '`nums` 有负数，不能直接用双指针',
                 '本视频：`[2,-1,2,-2,1,3]`，`k = 4` → `2`（`1+3`）'],
        quote='遍历 s，同时用某个合适的数据结构来维护遍历过的 s[i]，并及时移除无用的 s[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['优化一：队首 `s[j]` 已满足 `s[i] − s[j] ≥ k`，==出队==，后面的右端点只会更长',
              '优化二：队尾 `s[j] ≥ s[i]`，==出队==，以 `i` 为左端点既更近又更小',
              '队列因此严格递增：左边弹队首，右边弹队尾，右边入队 → 双端队列'],
        summary=['时间 `O(n)`：每个下标至多入队、出队各一次',
                 '前缀和多一个 0：`s` 长度 n+1，子数组是左闭右开 `[j, i)`',
                 '另一种写法：边遍历边算前缀和，队列里存 `(cur_s, i)`，初始放 `(0, -1)`，适用于数据流',
                 '`nums` 全非负时可以用双指针（209 题）'],
    ),
)
