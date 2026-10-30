def _cand(S):
    if 'k' not in S:
        return ''
    s, k = S['s'], S['k']
    a, b = s[:k][::-1] + s[k:], s[:-k] + s[-k:][::-1]
    return f"k = {k}：反转前 {k} 个 → ==`{a}`==；反转后 {k} 个 → ==`{b}`=="


def _hl(S, i, v):
    k = S.get('k')
    if k is None:
        return None
    return 'pink' if i < k else None


def _hr(S, i, v):
    k = S.get('k')
    if k is None:
        return None
    return 'cyan' if i >= len(S['s']) - k else None


CONFIG = dict(
    num=3722, title='反转后字典序最小的字符串', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='枚举 k · 暴力比较',
    tags=['灵神题单', '字符串', '字符串哈希', '后缀数组'],
    code='''
class Solution:
    def lexSmallest(self, s: str) -> str:
        ans = s  # k = 1 时，操作不改变 s
        for k in range(2, len(s) + 1):
            ans = min(ans, s[:k][::-1] + s[k:], s[:-k] + s[-k:][::-1])
        return ans
''',
    call='Solution().lexSmallest("dcab")',
    expect='acdb',
    views=[
        dict(type='text', fn=_cand, size=26, h=90),
        dict(type='string', var='s', label='s（粉 = 前 k 个，青 = 后 k 个）', cell=110, h=210,
             color=lambda S, i, v: (_hl(S, i, v) if _hl(S, i, v) else _hr(S, i, v))),
        dict(type='string', var='ans', label='ans：目前最小的结果', cell=110, h=190),
    ],
    watch=[('k', 'k', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = s': '`k = 1` 时反转一个字符，等于没动 → 先让 `ans = "{ans}"`',
        'for k in': lambda S, B, r: (f'枚举反转长度 `k = {S.k}`' if S.k != B.get('k') else 'k 枚举完毕'),
        'ans = min': lambda S, B, r: (f"前缀反转得 `{S.s[:S.k][::-1] + S.s[S.k:]}`，后缀反转得 `{S.s[:-S.k] + S.s[-S.k:][::-1]}`，三者取字典序最小 → `ans` = =={S.ans}=="
                                      + ('（更新了）' if S.ans != B.ans else '（没变）')),
        'return ans': '所有 `k` 都试过了，最小的是 `{ans}`',
    },
    cards=dict(
        one_liner='n 只有 1000，枚举 k，两种反转都试一遍取最小',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['必须恰好操作一次：选 `k`，反转 `s` 的前 `k` 个或后 `k` 个字符',
                 '返回能得到的==字典序最小==的字符串',
                 '示例：`"dcab"` → `"acdb"`（反转前 3 个）'],
        quote='枚举 k=1,2,…,n，反转长为 k 的前缀/后缀，用得到的字符串更新答案的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k = 1` 反转一个字符不变，所以 `ans` 初始为 `s`，循环从 `k = 2` 开始',
              '每个 `k` 构造两个新串：`s[:k][::-1] + s[k:]` 与 `s[:-k] + s[-k:][::-1]`',
              '`min` 一次比较三个字符串，字典序最小的留下'],
        summary=['时间 `O(n^2)`：k 有 n 个，每次拼接比较 `O(n)`',
                 '后缀写法 `s[:-k]` 在 `k = n` 时是空串，没问题；所以 `k` 可到 `len(s)`',
                 '易错：必须恰好操作一次，`k = 1` 的结果就是 `s` 本身，别漏掉',
                 '非暴力：构造 `rev(s) + # + s`，用后缀数组或字符串哈希 + 二分 `O(n log n)` 比较子串'],
    ),
)
