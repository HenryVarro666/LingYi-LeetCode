def _in2(S):
    return S['_line'] >= 25 and 'sr' in S and 'r' in S and 'last_x2' in S


def _wl(S):
    if _in2(S) and 'l' in S and S['_line'] >= 31:
        return S['l']
    return None


def _wr(S):
    return S['r'] - 1


def _txt(S):
    if not _in2(S) or S['_line'] < 31 or 'sl' not in S:
        return ''
    k = S['k']
    need = (S['sr'] - S['sl']) % k
    j = S['last_x2'][need]
    return (f"`s[r]%k = {S['sr']}`，`s[l]%k = {S['sl']}`：需要 `2·nums[i] % k = ({S['sr']}−{S['sl']}) % {k} = {need}`，"
            f"最近出现位置 `j = {j}`，l = {S['first_pos'][S['sl']]}")


CONFIG = dict(
    num=4064, title='至多一次取反能被 K 整除的最长子数组 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举 s[r]、s[l]，无需二分',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution:
    def longestSubarray(self, nums: list[int], k: int) -> int:
        first_sum = [0]
        first_pos = [-1] * k  # 前缀和 % k 首次出现的位置
        last_pos = [-1] * k  # 前缀和 % k 最后一次出现的位置
        first_pos[0] = last_pos[0] = 0
        s = 0  # 前缀和
        ans = 0

        for i, x in enumerate(nums):
            s = (s + x) % k
            r = i + 1
            l = first_pos[s]
            if l < 0:
                first_pos[s] = r
                first_sum.append(s)
            else:
                # 不取反时的最大长度
                ans = max(ans, r - l)
            last_pos[s] = r

        last_x2 = [-1] * k
        sr = 0

        # 枚举 s[r]%k 和 s[l]%k，判断是否存在满足要求的 i
        for i, x in enumerate(nums):
            last_x2[x * 2 % k] = i
            sr = (sr + x) % k
            r = i + 1
            if last_pos[sr] != r:  # 只考虑 s[r]%k 最后一次出现的位置
                continue
            for sl in first_sum:
                l = first_pos[sl]
                if r - l <= ans:  # 最优性优化：ans 无法增大
                    break
                j = last_x2[(sr - sl) % k]
                if j >= l:
                    ans = r - l

        return ans
''',
    call='Solution().longestSubarray([2,2,5], 6)',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=190, label='nums（框 = 当前检查的 [l, r)）',
             window=(_wl, _wr)),
        dict(type='array', var='first_pos', label='first_pos[s%k]', h=130, cell=70, pointers={}),
        dict(type='array', var='last_pos', label='last_pos[s%k]', h=130, cell=70, pointers={}),
        dict(type='array', var='last_x2', label='last_x2[2·x%k]', h=130, cell=70, pointers={}),
        dict(type='text', size=24, h=80, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('r', 'r', 'pink'), ('l', 'l', 'cyan'), ('ans', 'ans', 'green')],
    skip=['s = 0  #', 'ans = 0', 'first_sum.append', 'last_pos[s] = r', 'break', 'r = i + 1'],
    captions={
        'first_sum = [0]': '`first_sum`：按首次出现的先后保存不同的 `s[l]%k`，枚举时不用扫不存在的余数',
        'first_pos = [-1]': '`first_pos[v]`：前缀和 %k = v 第一次出现的下标，越靠左子数组越长',
        'last_pos = [-1]': '`last_pos[v]`：前缀和 %k = v 最后一次出现的下标，越靠右越长',
        'first_pos[0] = last_pos[0] = 0': '空前缀 `s[0] = 0`，位置记 0（`[l,r)` 左闭右开）',
        's = 0': '`s` 是前缀和（%k）',
        'ans = 0': '`ans` 是最长长度',
        's = (s + x) % k': '`s = ({B.s} + {x}) % {k} = {s}`',
        'r = i + 1': '`r = {r}`：前缀和下标，子数组 [l, r)',
        'l = first_pos[s]': '`first_pos[{s}] = {l}`：前缀和 %k 同值的最早位置（-1 表示第一次出现）',
        'if l < 0': lambda S, B, r: (f'`l = {S.l} < 0`：{S.s} 第一次出现' if S.l < 0 else f'`l = {S.l} ≥ 0`：之前出现过 → 中间那段和 %k = 0，不取反就合法'),
        'first_pos[s] = r': '记下首次位置 `first_pos[{s}] = {r}`',
        'first_sum.append': '`first_sum` = {first_sum}',
        'ans = max(ans, r - l)': '不取反：长度 `{r} − {l}`，`ans` = =={ans}==',
        'last_pos[s] = r': '更新最后位置 `last_pos[{s}] = {r}`（不断覆盖，最后留下最右）',
        'last_x2 = [-1]': '`last_x2[v]`：`2·nums[i] % k = v` 最近出现的下标 i',
        'sr = 0': '`sr` 重新累计前缀和 %k',
        'last_x2[x * 2 % k] = i': '`2·{x} % {k} = {x*2%k}`，`last_x2[{x*2%k}] = {i}`',
        'sr = (sr + x) % k': '`sr = {sr}`',
        'if last_pos[sr] != r': lambda S, B, rr: (f'`last_pos[{S.sr}] = {S.last_pos[S.sr]} ≠ r = {S.r}`：不是该余数最后一次出现 → 更靠右的 r 更优，跳过' if S.last_pos[S.sr] != S.r else f'`last_pos[{S.sr}] = r = {S.r}`：这是 `s[r]%k` 最后一次出现，枚举 `s[l]%k`'),
        'for sl in first_sum': '枚举 `s[l]%k = {sl}`',
        'l = first_pos[sl]': '对应最左位置 `l = {l}`',
        'if r - l <= ans': lambda S, B, rr: (f'`{S.r} − {S.l} = {S.r - S.l} ≤ ans = {S.ans}`：后面的 l 更大、更短 → 直接 break' if S.r - S.l <= S.ans else f'`{S.r} − {S.l} = {S.r - S.l} > ans = {S.ans}`：有机会变长，继续检查'),
        'j = last_x2': '需要 `2·nums[i] % k = (sr−sl) % k = {(sr - sl) % k}`，最近出现下标 `j = {j}`',
        'if j >= l': lambda S, B, rr: (f'`j = {S.j} ≥ l = {S.l}`：取反 nums[{S.j}] 刚好落在 [l, r) 内 → 合法' if S.j >= S.l else f'`j = {S.j} < l = {S.l}`：满足同余的元素在区间外 → 不行'),
        'ans = r - l': '`ans = {r} − {l} = {ans}`',
        'return ans': '最长有效子数组长度 `{ans}`',
    },
    cards=dict(
        one_liner='枚举前缀和的余数而不是下标，用 last_x2 代替二分',
        complexity='时间 `O(n + k + min(n,k)^2)`，空间 `O(k)`',
        problem=['子数组和能被 `k` 整除，或取反其中一个元素后能被 `k` 整除，就是==有效==',
                 '求最长有效子数组的长度，没有则为 0',
                 '示例：`nums=[2,2,5], k=6` → `2`（`[2,2]` 取反一个得 0）'],
        quote='本题 k ≤ 3000，我们可以枚举前缀和的值（而不是下标）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['取反 `nums[i]` 后：`s[r] − s[l] ≡ 2·nums[i] (mod k)`',
              '相同的 `s[l]%k` 取最左 l，相同的 `s[r]%k` 取最右 r',
              '遍历时维护 `2·x%k` 最近出现位置 j，`j ≥ l` 就说明 i 在区间内，不用二分'],
        after=[dict(heading='另外两种写法', lines=['优化前：把 `2·nums[i]%k` 的所有位置存数组，再二分查第一个 ≥ l 的',
                                                  '附：枚举取反元素 i，用 `ptr` 双指针避免重复枚举 l'])],
        summary=['时间 `O(n + k + min(n,k)^2)`，空间 `O(k)`',
                 '区间是左闭右开 `[l, r)`，所以空前缀位置记 0',
                 '先不取反更新 ans，再处理取反的情况',
                 '`r - l <= ans` 提前 break：first_sum 按 l 升序，后面只会更短'],
    ),
)
