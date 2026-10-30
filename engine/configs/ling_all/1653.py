S0 = 'abababa'


def _pos(S):
    """当前处理到 S0 的哪个下标（用 (c, f, cnt_b) 在小例子上唯一反推）"""
    if 'c' not in S:
        return -1
    f = cb = 0
    for p, ch in enumerate(S0):
        x = 1 if ch == 'b' else 0
        states = {(f, cb), (f, cb + x)}
        cb += x
        f = min(f + (x ^ 1), cb)
        states.add((f, cb))
        if ch == S['c'] and (S['f'], S['cnt_b']) in states:
            return p
    return -1


def _fml(S):
    if 'c' not in S or _pos(S) < 0:
        return '`f` = 当前前缀变平衡的最少删除数；`cnt_b` = 前缀里 `b` 的个数'
    x = 1 if S['c'] == 'b' else 0
    if S['_line'] == 4:
        return f"取到字母 `{S['c']}`"
    if S['_line'] == 5:
        return f"当前字母 `{S['c']}`：`x = {x}`（`b` 为 1，`a` 为 0）"
    if S['_line'] == 6:
        return f"`cnt_b` += `x`：`b` 才会增加，现在前缀共有 `{S['cnt_b']}` 个 `b`"
    return f"`f = min(f + (x ^ 1), cnt_b)`：删掉这个 `a`（+1），或保留它而删光前面所有 `b`（`{S['cnt_b']}`）"


CONFIG = dict(
    num=1653, title='使字符串平衡的最少删除次数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='动态规划（一次遍历，空间 O(1)）',
    tags=['灵神题单·动态规划', '难度分 1794'],
    code='''
class Solution:
    def minimumDeletions(self, s: str) -> int:
        f = cnt_b = 0
        for c in s:
            x = ord(c) - ord('a')  # ord 很慢
            cnt_b += x
            f = min(f + (x ^ 1), cnt_b)
        return f
''',
    call=f'Solution().minimumDeletions({S0!r})',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（蓝 = 正在处理，灰 = 已处理）', h=210, cell=80,
             color=lambda S, i, v: 'blue' if i == _pos(S) else None,
             dim=lambda S, i, v: i < _pos(S)),
        dict(type='text', fn=_fml, size=26, h=90),
    ],
    watch=[('c', 'c', 'blue'), ('x', 'x', 'orange'), ('cnt_b', 'cnt_b', 'pink'), ('f', 'f', 'green')],
    captions={
        'f = cnt_b = 0': '`f`：前缀的最少删除次数；`cnt_b`：前缀里 `b` 的个数；空前缀都是 0',
        'for c in s': lambda S, B, r: ('字符串扫完了，循环结束' if _pos(S) == len(S0) - 1 and S.f == 3 else f'看下一个字母 `{S.c}`'),
        'x = ord': '`x = {x}`：==`b` 记 1，`a` 记 0==，用算术代替 if-else',
        'cnt_b += x': '`cnt_b` += `{x}` → =={cnt_b}==（只有 `b` 会让它增加）',
        'f = min': lambda S, B, r: (f'`{S.c}` 是 `a`：删它（`f+1 = {B.f + 1}`）或保留它而删光前面的 `b`（`cnt_b = {S.cnt_b}`）取小 → `f` = =={S.f}=='
                                    if S.x == 0 else
                                    f'`{S.c}` 是 `b`：放在末尾无需删，`f` 不超过 `cnt_b`（全删 `b`）：`min({B.f}, {S.cnt_b})` → `f` = =={S.f}=='),
        'return f': '整个字符串变平衡的最少删除次数 `f` = =={ret}==',
    },
    cards=dict(
        one_liner='看最后一个字母：是 b 不用管，是 a 就在“删 a”和“删光前面的 b”里选小的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 只含 `a` 和 `b`，可以删任意字符',
                 '平衡：不存在 `i < j` 使得 `s[i] = b` 且 `s[j] = a`',
                 '返回最少删除次数；示例：`"aababbab"` → `2`，本视频用 `"abababa"` → `3`'],
        quote='如果它是 a：删除它，则答案为「使 s 的前 n-1 个字母平衡的最少删除次数」加上 1；保留它，那么前面的所有 b 都要删除。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`f[i]`：前 `i` 个字母平衡的最少删除次数，只依赖 `f[i-1]`，滚动成一个变量 `f`',
              '最后一个字母是 `b`：`f` 不变，`cnt_b` 加 1',
              '最后一个字母是 `a`：`f = min(f + 1, cnt_b)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：遇到 `b` 时 `f` 不变，但要同步增加 `cnt_b`',
                 '无分支版本：`x = ord(c) - ord(\'a\')`，`b` 时 `f` 取 `min(f, cnt_b)`，等价于全删 `b`',
                 '灵神还给了方法一：前后缀分解（枚举分界线，删前面的 `b` 和后面的 `a`），一次遍历版本是它的优化',
                 '去掉 `if-else` 是为了避免 CPU 分支预测失败，业务代码不建议这样写'],
    ),
)
