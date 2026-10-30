
CONFIG = dict(
    num=3999, title='字符串变换后的最少分组数', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='最小表示法 · 哈希集合去重',
    tags=['灵神题单·字符串', '难度分 2162'],
    code='''
# 返回 s 的字典序最小的循环同构串
# 时间复杂度 O(|s|)，证明见代码末尾的注释
def smallestRepresentation(s: str) -> str:
    n = len(s)
    s += s
    i = 0  # 始终指向当前最小子串的首字母下标
    j = 1  # 指向需要和 i 比较的子串的首字母下标
    while j < n:
        # 暴力比较：是 i 开头的字典序小，还是 j 开头的字典序小？
        k = 0
        while k < n and s[i + k] == s[j + k]:
            k += 1
        if k >= n:
            # s 是个周期字符串，周期为 j-i
            # j+d 开头的子串等于 i+d 开头的子串，而这些子串我们之前已经排除了，继续遍历不会找到更小的
            break

        if s[i + k] < s[j + k]:  # 注：如果求字典序最大，改成 >
            # 比如从 i 开始是 "aaab"，从 j 开始是 "aaac"
            # 从 i 开始比从 j 开始更小（排除 j）
            # 此外：
            # 从 i+1 开始比从 j+1 开始更小，所以从 j+1 开始不可能是答案，排除
            # 从 i+2 开始比从 j+2 开始更小，所以从 j+2 开始不可能是答案，排除
            # ……
            # 从 i+k 开始比从 j+k 开始更小，所以从 j+k 开始不可能是答案，排除
            # 所以下一个「可能是答案」的开始位置是 j+k+1
            j += k + 1
        else:
            # 从 j 开始比从 i 开始更小，更新 i=j（也意味着我们排除了 i）
            # 此外：
            # 从 j+1 开始比从 i+1 开始更小，所以从 i+1 开始不可能是答案，排除
            # 从 j+2 开始比从 i+2 开始更小，所以从 i+2 开始不可能是答案，排除
            # ……
            # 从 j+k 开始比从 i+k 开始更小，所以从 i+k 开始不可能是答案，排除
            # 所以把 j 跳到 i+k+1，不过这可能比 j+1 小，所以与 j+1 取 max
            # 综上所述，下一个「可能是答案」的开始位置是 max(j+1, i+k+1)
            i, j = j, max(j, i + k) + 1

        # 每次要么排除 k+1 个与 i 相关的位置（这样的位置至多 n 个），要么排除 k+1 个与 j 相关的位置（这样的位置至多 n 个）
        # 所以上面关于 k 的循环，∑k <= 2n，所以二重循环的总循环次数是 O(n) 的

    return s[i: i + n]

class Solution:
    def minimumGroups(self, words: list[str]) -> int:
        st = {smallestRepresentation(word[::2]) + smallestRepresentation(word[1::2]) for word in words}
        return len(st)
''',
    call='Solution().minimumGroups(["bbaab","aabbb","bbaaa"])',
    expect=2,
    views=[
        dict(type='string', var='s', label='s + s（循环展开）：i 蓝 = 当前最小起点，j 粉 = 挑战者', pointers={'i': 'blue', 'j': 'pink'}, h=230, cell=64,
             color=lambda S, idx, v: ('blue' if idx == S.get('i') else 'pink' if idx == S.get('j') else None) if 'j' in S else None),
        dict(type='text', fn=lambda S: (f"比较起点 `i={S['i']}` 与 `j={S['j']}`：已相同 `k={S['k']}` 个字符" if 'k' in S and 'j' in S else ''), h=70),
        dict(type='set', var='st', label='st（每个字符串的最小表示拼成的规范形）', h=120),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'k', 'n', ('len(st)', 'len(st)', 'green')],
    captions={
        'n = len(s)': '`n = {n}`：循环同构只有 `n` 种起点',
        's += s': '把 `s` 拼成 `s+s`，任意起点截 `n` 个字符就是一种循环移位',
        'i = 0': '`i` 记录当前最小候选起点',
        'j = 1': '`j` 是挑战者起点，从 1 开始',
        'while j < n': lambda S, B, r: f'`j = {S.j} < n = {S.n}`：还有候选起点没排除' if S.j < S.n else f'`j = {S.j} >= n = {S.n}`：所有起点都比较完',
        'k = 0': '暴力比较 `i`、`j` 开头的两个子串，`k` 记录已经相同的长度',
        'while k < n and': lambda S, B, r: (f"`s[{S.i}+{S.k}] = '{S.s[S.i+S.k]}'` 与 `s[{S.j}+{S.k}] = '{S.s[S.j+S.k]}'` 相同 → 继续比下一位" if (S.k < S.n and S.s[S.i+S.k] == S.s[S.j+S.k]) else '遇到不同字符或比满 `n` 位 → 停止比较'),
        'k += 1': '相同，`k` 增到 `{k}`',
        'if k >= n': lambda S, B, r: (f'`k = {S.k} >= n`：整个串是周期串，后面不会再有更小的 → ==break==' if S.k >= S.n else f'`k = {S.k} < n`：找到第一个不同位置，要分出胜负'),
        'if s[i + k] < s[j + k]': lambda S, B, r: (f"`'{S.s[S.i+S.k]}' < '{S.s[S.j+S.k]}'` → ==i 开头更小==，j 到 j+k 都可以排除" if S.s[S.i+S.k] < S.s[S.j+S.k] else f"`'{S.s[S.i+S.k]}' > '{S.s[S.j+S.k]}'` → ==j 开头更小==，i 到 i+k 都可以排除"),
        'j += k + 1': 'i 更小：`j` 到 `j+k` 全部排除，`j` 直接跳到 {j}',
        'i, j = j, max': 'j 更小：`i` 换成原来的 `j`；`j` 跳到 `max(j+1, i+k+1)` = {j}',
        'return s[i: i + n]': '从 `i` 起截 `n` 位 = 最小循环同构串 `{ret}`',
        'st = {': '偶数下标、奇数下标各自取最小表示再拼起来，放进集合：`{st}`',
        'return len(st)': '集合大小就是最少分组数 `{ret}`',
    },
    cards=dict(
        one_liner='每个串的奇偶两半各取最小表示，规范形相同就是一组',
        complexity='时间 `O(L)`，空间 `O(L)`，`L` 为所有字符串长度之和',
        problem=['一次变换：偶数下标子序列、奇数下标子序列分别循环右移任意位',
                 '能互相变成的字符串等价，求最少分成几组',
                 '本视频：`["bbaab","aabbb","bbaaa"]` → `2`'],
        quote='把每个字符串的偶数下标子序列 a 变成其「最小表示」：在 a 的所有循环同构字符串中，字典序最小的字符串。奇数下标子序列同理。然后把得到的字符串插入哈希集合中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['等价 = 偶数位循环同构 + 奇数位循环同构',
              '每个循环同构类选一个代表：==字典序最小的那个==',
              '最小表示用 `i`、`j` 双指针：比较失败的一方，一整段起点一起排除，总共 `O(n)`'],
        summary=['时间 `O(L)`，空间 `O(L)`',
                 '`k >= n` 表示周期串，直接 break 是正确的',
                 '`j` 跳到 `max(j+1, i+k+1)`，不取 max 会往回走',
                 '写法一是把最小表示分别放回偶、奇下标；写法二直接拼接，本视频用写法二',
                 '同类题：1163 按字典序排在最后的子串（同一套双指针）'],
    ),
)
