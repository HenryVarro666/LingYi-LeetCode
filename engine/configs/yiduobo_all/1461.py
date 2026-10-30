S0, K0 = '0001110100', 3
# 本例中 8 个长为 3 的窗口两两不同，所以可以由 now 的值反推出窗口位置（代码里没有下标变量）
_POS = {int(S0[j:j + K0], 2): j for j in range(len(S0) - K0 + 1)}


def _wl(S):
    if 'num_set' not in S or 'now' not in S:
        return None
    if not S['num_set']:
        return 0
    return _POS.get(S['now'] % (1 << K0))


def _wr(S):
    l = _wl(S)
    return None if l is None else l + K0 - 1


def _txt(S):
    if 'now' not in S:
        return '用整数 `now` 表示窗口里的二进制串，`now + now` 就是左移一位'
    k, now = S['k'], S['now']
    if now >= S['p']:
        return f"`now = {now}` = `{now:b}`：多出了第 {k + 1} 位，==要减去 p = {S['p']}=="
    return f"`now = {now}` = `{now:0{k}b}`　集合里已有 `{len(S['num_set'])}` / `{S['p']}` 种"


CONFIG = dict(
    num=1461, title='检查一个字符串是否包含所有长度为 K 的二进制子串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='先判数量 · 滑窗二进制编码',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def hasAllCodes(self, s, k):

        p = 1 << k
        if len(s) - k + 1 < p:
            return False

        num_set = set()
        now = 0
        for char in s[:k]:
            now = now + now + int(char)

        num_set.add(now)
        for char in s[k:]:
            now = now + now + int(char)
            if now >= p:
                now -= p
            num_set.add(now)

        return len(num_set) == p
''',
    call=f'Solution().hasAllCodes({S0!r}, {K0})',
    expect=True,
    views=[
        dict(type='string', var='s', label=f's（框 = 当前长为 k = {K0} 的窗口）', h=230, cell=96,
             window=(_wl, _wr)),
        dict(type='text', h=90, size=28, fn=_txt),
        dict(type='set', var='num_set', label='num_set（窗口编码）', h=170, font=34,
             fmt=lambda v: f'{v:0{K0}b} ({v})'),
    ],
    watch=[('char', 'char'), ('now', 'now', 'orange'), ('p', 'p'), ('len(num_set)', 'len(num_set)', 'green')],
    captions={
        'p = 1 << k': '长为 k 的二进制串一共 `p = 2^{k} = {p}` 种',
        'if len(s) - k + 1 < p': '`s` 只有 `{len(s)} − {k} + 1 = {len(s) - k + 1}` 个长为 k 的子串，`≥ p`，==数量上==还有可能',
        'num_set = set()': '`num_set` 存出现过的窗口编码',
        'now = 0': '`now`：当前窗口的二进制数',
        'for char in s[:k]': '先把前 k 个字符 `{s[:k]}` 读进 `now`，得到第一个窗口',
        11: '`now = now × 2 + {char}` → `{now}`',
        13: '第一个窗口 `{now:0{k}b}` 加入集合',
        'for char in s[k:]': '窗口继续右移：从 `s[k:]` 取下一个字符（取完就结束）',
        15: '`now + now + {char}`：整体左移一位、末尾补上新字符 → `{now}`（`{now:b}`）',
        'if now >= p': lambda S, B, r: (f'`now = {S.now} ≥ p = {S.p}`：最高位是窗口==最左边要离开的 1==' if S.now >= S.p
                                        else f'`now = {S.now} < p`：离开的最左位是 0，不用处理'),
        'now -= p': '减去 `p` 去掉最高位 → `now = {now}`（`{now:0{k}b}`）',
        18: lambda S, B, r: (f'`{S.now:0{S.k}b}` 是==新的==子串，加入集合（共 {len(S.num_set)} 种）' if len(S.num_set) > len(B.num_set)
                             else f'`{S.now:0{S.k}b}` 已经出现过'),
        'return len(num_set)': '`len(num_set) = {len(num_set)}`，等于 `p = {p}` → `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='先比数量：子串个数都不够 2^k，就不可能全覆盖',
        complexity='时间 `O(n)`，空间 `O(min(n, 2^k))`',
        problem=['二进制串 `s`，判断==所有==长为 `k` 的二进制串是否都是 `s` 的子串',
                 '示例：`s = "00110110", k = 2` → `true`；`s = "0110", k = 2` → `false`',
                 '本视频：`s = "0001110100", k = 3` → `true`'],
        quote='一个长度为l的字符串中所包含的长度为k的子串数目则一共是l - k + 1个，那么可以先检测这个总数与目标子串数目的大小，若数目不足，那么答案必然为false。',
        quote_src='—— yiduobo 题解原文',
        idea=['剪枝：`len(s) − k + 1 < 2^k` 直接返回 False',
              '滑动窗口：`now + now + 新位` 入窗，`now ≥ p` 时减 `p` 让最高位出窗',
              '集合大小恰好为 `2^k` 就是 True'],
        summary=['时间 `O(n)`：每个字符只做常数次运算',
                 '易错：先读满前 k 个字符得到第一个窗口，再开始滑动',
                 '`now -= p` 等价于灵神的 `& MASK`：去掉超出 k 的最高位',
                 '原文的 Python 2 风格代码可直接在 Python 3 运行，未做改动'],
    ),
)
