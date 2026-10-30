def _txt(S):
    if 'ans' in S and 'cur_r' in S and 'nxt_r' in S and 'max_jump' in S:
        return f"已建的桥通到 `cur_r = {S['cur_r']}`；目前最远能到 `nxt_r = {S['nxt_r']}`；已用段数 `ans = {S['ans']}`"
    if 'max_jumps' in S and 'z' in S and 'm' in S:
        return '`max_jumps[i]`：从 `target[i]` 开始，最长能匹配某个 word 前缀的长度'
    return '先求每个位置能匹配的最长前缀 `max_jumps`，再当成「跳跃游戏」求最少跳数'


def _zs(S):
    """word + '#' + target"""
    w = S.get('word')
    return None if w is None else w + '#' + S['target']


CONFIG = dict(
    num=3292, title='形成目标字符串需要的最少字符串数 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='Z 函数 + 跳跃游戏 II（建桥）',
    tags=['字符串', '难度分 2662'],
    code='''
class Solution:
    def calc_z(self, s: str) -> List[int]:
        n = len(s)
        z = [0] * n
        box_l = box_r = 0  # z-box 左右边界（闭区间）
        for i in range(1, n):
            if i <= box_r:
                z[i] = min(z[i - box_l], box_r - i + 1)
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                box_l, box_r = i, i + z[i]
                z[i] += 1
        return z

    # 桥的概念，见我在 45 或 1326 题下的题解
    def jump(self, max_jumps: List[int]) -> int:
        ans = 0
        cur_r = 0  # 已建造的桥的右端点
        nxt_r = 0  # 下一座桥的右端点的最大值
        for i, max_jump in enumerate(max_jumps):  # 如果走到 n-1 时没有返回 -1，那么必然可以到达 n
            nxt_r = max(nxt_r, i + max_jump)
            if i == cur_r:  # 到达已建造的桥的右端点
                if i == nxt_r:  # 无论怎么造桥，都无法从 i 到 i+1
                    return -1
                cur_r = nxt_r  # 造一座桥
                ans += 1
        return ans

    def minValidStrings(self, words: List[str], target: str) -> int:
        n = len(target)
        max_jumps = [0] * n
        for word in words:
            z = self.calc_z(word + "#" + target)
            m = len(word) + 1
            for i in range(n):
                max_jumps[i] = max(max_jumps[i], z[m + i])
        return self.jump(max_jumps)
''',
    call="Solution().minValidStrings(['abc', 'ba'], 'abab')",
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=28, h=50),
        dict(type='string', var='target', label='target', h=170, window=('i if cur_r is not None else None', 'i + max_jump - 1 if max_jump else i')),
        dict(type='array', var='max_jumps', label='max_jumps[i]：从 i 出发最远跳几格', h=250,
             pointers={'i': 'blue', 'cur_r': 'orange', 'nxt_r': 'green'}),
        dict(type='array', var=lambda S: [] if 'cur_r' in S else S.get('z'), label='z：Z 数组（word + # + target），z[m+i] 对应 target[i]', h=150),
    ],
    watch=[('i', 'i', 'blue'), ('cur_r', 'cur_r', 'orange'), ('nxt_r', 'nxt_r', 'green'), ('ans', 'ans', 'pink')],
    captions={
        'z = self.calc_z': lambda S, B, r: f"拼成 `{S.word}#{S.target}` 求 Z 数组：`z[k]` = 后缀 `s[k:]` 与 `s` 的最长公共前缀；中间的 `#` 保证匹配不会越过 word",
        'm = len(word)': '`m = {m}`：`target[i]` 在拼接串里的下标是 `m + i`，所以 `z[m + i]` 就是 `target[i:]` 与 `{word}` 的最长公共前缀',
        'max_jumps[i] = max': '`max_jumps[{i}] = max({B.max_jumps[i]}, z[{m}+{i}] = {z[m + i]})` = =={max_jumps[i]}==：从 `target[{i}]` 起，最长能匹配 words 前缀 {max_jumps[i]} 个字符',
        'return self.jump': '前缀的前缀还是前缀：从 `i` 出发可以跳到 `[i+1, i+max_jumps[i]]` 内任意位置 → 最少几跳到 `n`？就是 ==跳跃游戏 II==',
        'for i, max_jump in': lambda S, B, r: ('都走完了，返回段数' if B.get('i') == S.i and B.get('max_jump') == S.max_jump and S.i == len(S.max_jumps) - 1
                                               else f'走到 `i = {S.i}`，它最多能跳 `{S.max_jump}` 格'),
        'nxt_r = max': '从 `{i}` 出发最远到 `{i} + {max_jump} = {i + max_jump}` → 下一座桥最远通到 `nxt_r = {nxt_r}`',
        'if i == cur_r': lambda S, B, r: (f'`i = cur_r = {S.cur_r}`：走到已建桥的右端，==必须再建一座桥==' if S.i == S.cur_r
                                          else f'`i = {S.i}` 还没走到桥端 `{S.cur_r}`：继续走，同时记录更远的桥端'),
        'if i == nxt_r': lambda S, B, r: (f'`i = nxt_r = {S.nxt_r}`：无论怎么造桥都到不了 `{S.i + 1}` → 返回 `-1`' if S.i == S.nxt_r
                                          else f'`nxt_r = {S.nxt_r} > i`：还能往前造桥'),
        'cur_r = nxt_r': '造桥：`cur_r = {cur_r}`，已建的桥通到这里',
        'ans += 1': '用了一段前缀：`ans = {ans}`',
        'return ans': '`ans = {ans}`：最少需要连接的有效字符串数',
    },
    skip=['n = len(s)', 'z = [0] * n', 'box_l = box_r = 0', 'for i in range(1, n)', 'if i <= box_r', 'z[i] = min', 'while i + z[i]', 'box_l, box_r', 'z[i] += 1', 'return z',
          'n = len(target)', 'max_jumps = [0] * n', 'for i in range(n)', 'ans = 0', 'cur_r = 0', 'nxt_r = 0', 'for word in words'],
    max_steps=100,
    cards=dict(
        one_liner='先算出每个位置最长能匹配的前缀，再当「跳跃游戏 II」',
        complexity='时间 `O(L + nm)`，空间 `O(l + n)`',
        problem=['把 `target` 划分成若干段，每段都是某个 `words[i]` 的前缀，求最少划分几段',
                 '无法划分返回 `-1`',
                 '本视频：`words = [abc, ba]`，`target = abab` → `2`（`ab` + `ab`）'],
        quote='注意 words[i] 前缀的前缀还是 words[i] 的前缀……如果从 target[2] 开始的段，最长可以是 3，那么这个段的长度也可以是 1 或者 2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每段越长越好：只需知道从 `target[i]` 开始最长能匹配多长 → `max_jumps[i]`',
              '前缀的前缀仍是前缀，所以能跳到 `[i+1, i+max_jumps[i]]` 内任意位置：就是跳跃游戏 II',
              '`max_jumps` 用 Z 函数：对每个 word 求 `word + # + target` 的 Z 数组，`z[m+i]` 就是 LCP；跳跃用「建桥」贪心 `O(n)`'],
        summary=['时间 `O(L + nm)`：`L` 是 words 总长，`m = len(words)`，空间 `O(l + n)`',
                 '`#` 是分隔符，让 `z[i]` 不会超过 word 长度',
                 '`i == nxt_r` 说明连下一格都到不了，返回 `-1`',
                 'Z 函数内部（z-box 维护）本视频略过，直接看每个 word 的结果',
                 '题解还有：字符串哈希 + 二分 / 双指针（`O(n log n)` / `O(L+n)`）、AC 自动机 `O(L|Σ|+n)`'],
    ),
)
