CONFIG = dict(
    num=3445, title='奇偶频次间的最大差值 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举 a,b + 前缀和 + 状态压缩',
    tags=['前缀和', '难度分 2694'],
    code='''
class Solution(object):
    def maxDifference(self, s, k):
        
        def calc(a, b):
            val = [0] * len(s)
            for index, char in enumerate(s):
                if char == a:
                    val[index] = 1
                elif char == b:
                    val[index] = -1
                else:
                    val[index] = 0
            
            f = [0]
            state = [0]
            pre_first_b = None
            pre_second_b = None
            left = 0
            state_a = 0
            state_b = 0
            best = [None] * 4
            res = -len(s)
            for index, v in enumerate(val):
                f.append(f[-1] + v)
                if v == 1:
                    state_a ^= 1
                elif v == -1:
                    state_b ^= 1
                    pre_first_b, pre_second_b = index + 1, pre_first_b
                
                state.append(state_a << 1 | state_b)

                while index - left + 1 >= k and pre_second_b is not None and left < pre_second_b:
                    if best[state[left]] is None or best[state[left]] > f[left]:
                        best[state[left]] = f[left]
                    left += 1
            
                pre_state = (state_a ^ 1) << 1 | state_b
                if best[pre_state] is not None:
                    res = max(res, f[-1] - best[pre_state])

            return res

        char_set = set(s)
        res = -len(s)
        for a in char_set:
            for b in char_set:
                if a == b:
                    continue
                res = max(res, calc(a, b))
        
        return res
''',
    call='Solution().maxDifference("00110", 4)',
    expect=1,
    setup='_set = set\nset = lambda it: sorted(_set(it))  # 让枚举 (a, b) 的顺序固定，视频可复现',
    views=[
        dict(type='array', var='val', label='val：a→1，b→−1，其余→0', h=190, pointers={'index': 'blue', 'left': 'pink'},
             color=lambda S, i, v: 'green' if v == 1 else 'orange' if v == -1 else None),
        dict(type='array', var='f', label='f：前缀和', h=190, pointers={'left': 'pink'}),
        dict(type='array', var='state', label='state：a奇偶×2 + b奇偶', h=190),
        dict(type='array', var='best', label='best[state]：可用前缀里 f 的最小值', h=190),
    ],
    watch=['a', 'b', 'index', 'left', 'state_a', 'state_b', ('res', 'res', 'green')],
    max_steps=57,
    skip=['val = [0]', 'f = [0]', 'state = [0]', 'pre_first_b = None', 'pre_second_b = None', 'state_a = 0', 'state_b = 0', 'best = [None]', 'else:', 'val[index] = 0', 'if char == a', 'elif char == b', 'if a == b', 'continue', 'if v == 1', 'elif v == -1', 'if best[state[left]] is None', 'state.append', 'pre_state = ', 'for index, char', 'f.append'],
    captions={
        'val[index] = 1': '`s[{index}] = {char}` 就是 a → 记 `1`',
        'val[index] = -1': '`s[{index}] = {char}` 就是 b → 记 `−1`',
        'res = -len(s)': '`res` 初值 `−len(s)`（比任何合法答案都小）',
        'left = 0': '`left`：可用前缀的右边界。`left` 之前的前缀已经记进 `best`',
        'f.append': '读到 `val = {v}`，`f` 末尾加入前缀和 `{f[-1]}`',
        'state_a ^= 1': 'a 的奇偶翻转，`state_a = {state_a}`；当前前缀的状态 `state = {state_a << 1 | state_b}`',
        'state_b ^= 1': 'b 的奇偶翻转，`state_b = {state_b}`；当前前缀的状态 `state = {state_a << 1 | state_b}`',
        'pre_first_b, pre_second_b': '记下 b 最近两次出现的位置：`pre_first_b = {pre_first_b}`，`pre_second_b = {pre_second_b}`（保证子串里至少两个 b）',
        'while index - left + 1 >= k': lambda S, B, r: (
            f'长度够：`{S.index} − {S.left} + 1 = {S.index - S.left + 1}` ≥ `k = {S.k}`'
            + (f'，且 `left = {S.left}` < `pre_second_b = {S.pre_second_b}` → ==这个前缀可用==' if S.pre_second_b is not None and S.left < S.pre_second_b else '，但 b 还不到两个 → 不能用')
            if S.index - S.left + 1 >= S.k else f'长度 `{S.index - S.left + 1}` < `k = {S.k}` → 前缀还不能用'),
        'if best[state[left]] is None': '前缀 `left = {left}`：状态 `{state[left]}`，`f = {f[left]}`；比 `best` 里记录的更小就更新',
        'best[state[left]] = f[left]': '`best[{state[left]}] = {f[left]}`：这个状态下目前最小的前缀和',
        'left += 1': '`left → {left}`：可用前缀右边界右移',
        'if best[pre_state] is not None': '要 a 奇偶相反、b 相同的前缀：`pre_state = ({state_a} ^ 1) << 1 | {state_b} = {pre_state}`；`best[{pre_state}]` {"有记录 → 更新答案" if best[pre_state] is not None else "还没有 → 跳过"}',
        'res = max(res, f[-1]': '`f[-1] − best[{pre_state}] = {f[-1]} − {best[pre_state]}`，`res = {res}`',
        42: '`calc({a}, {b})` 的结果 `{res}`',
        52: '所有 `(a, b)` 枚举完，答案 `{res}`',
    },
    cards=dict(
        one_liner='枚举 a、b 变成 1/−1 数组，前缀和 + 两位奇偶状态找最小前缀',
        complexity='时间 `O(n·|Σ|²)`，空间 `O(n)`',
        problem=['找子串里 `freq[a] − freq[b]` 的最大值：`a` 出现奇数次，`b` 出现非 0 偶数次，长度 `≥ k`',
                 '`s` 只含 `0` 到 `4`',
                 '示例：`s="1122211", k=3` → `1`；本视频用 `"00110", k=4`'],
        quote='s中仅包含\'0\'到\'4\'最多5种不同的数字，那么在这里就可以先暴力枚举所有a和b的组合，接下来将s中所有的\'a\'都变为1，\'b\'都变为-1，其余元素都变为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a→1`、`b→−1`：子串和就是 `freq[a] − freq[b]`，转成「长度 ≥ k 的最大子段和」',
              '前缀和相减；`state` 两位二进制记 a、b 出现次数的奇偶，需要的前缀状态是 `(state_a^1)<<1 | state_b`',
              '`best[state]` 存可用前缀的最小 `f`；用 `pre_second_b` 保证子串里至少有两个 b'],
        summary=['时间 `O(n·|Σ|²)`，每对 `(a, b)` 扫一遍',
                 'b 的偶数次不能是 0：靠 `left < pre_second_b` 保证至少两个 b',
                 '原文为 Python 2 写法，`left < pre_second_b` 在 `pre_second_b` 为 None 时 Py2 恒为假，已改为先判断 `is not None`',
                 '`char_set` 是 set，枚举 `(a, b)` 的顺序不影响结果（视频里为了可复现把它排了序）',
                 '对比灵神：灵神用 `cur_s/pre_s` 次数数组与 `min_s[p][q]`，yiduobo 用 `f`、`state`、`best`'],
    ),
)
