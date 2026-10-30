def _idx(s, t, k):
    out, p = [], 0
    for i, ch in enumerate(s):
        if p < k and ch == t[p]:
            out.append(i)
            p += 1
    return out


def _s_color(S, i, v):
    if 'j' not in S:
        return None
    return 'green' if i in _idx(S['s'], S['t'], S['j']) else None


def _top(S):
    if 'j' not in S:
        return ''
    t, j, m = S['t'], S['j'], S['m']
    if j >= m:
        return f'`j = {j} = m`：t 已全部匹配，无需追加'
    head = f"已匹配 t 的前 =={j}== 个字母，下一个要找 `t[{j}] = {t[j]}`"
    if 'c' in S and S['_line'] >= 5:
        return head + f"；当前扫到 `s` 里的 `{S['c']}`"
    return head + f'；还差 =={m - j}== 个'


def _if(S, B, ret):
    c, t, j = S.c, S.t, S.j
    if c == t[j]:
        return f"`{c}` == `t[{j}] = {t[j]}` → ==匹配上了==，立刻吃掉，别留到后面"
    return f"`{c}` ≠ `t[{j}] = {t[j]}` → 这个字母用不上，只让 s 往后走"


CONFIG = dict(
    num=2486, title='追加字符以获得子序列', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='双序列双指针 · 贪心匹配',
    tags=['灵神题单', '难度分 1363'],
    code='''
class Solution:
    def appendCharacters(self, s: str, t: str) -> int:
        j, m = 0, len(t)
        for c in s:
            if c == t[j]:
                j += 1
                if j == m: return 0
        return m - j
''',
    call="Solution().appendCharacters('coaching', 'coding')",
    expect=4,
    views=[
        dict(type='text', fn=_top, h=60),
        dict(type='string', var='s', color=_s_color, label='s（绿 = 已匹配上 t 前缀的字母）', h=180),
        dict(type='string', var='t', pointers={'j': 'blue'}, color=lambda S, i, v: 'green' if 'j' in S and i < S['j'] else None,
             dim=lambda S, i, v: False, label='t（箭头 j = 下一个要匹配的字母）', h=200),
    ],
    watch=[('j', 'j', 'blue'), 'm', 'c'],
    captions={
        'j, m = 0': '`j = 0`：t 里下一个要匹配的位置；`m = {m}` 是 t 的长度',
        'for c in s': '遍历 s 的每个字母 `c`（只能在 s 末尾追加，所以只看 s 能匹配 t 的==前缀==多长）',
        'if c == t[j]': _if,
        'j += 1': '匹配成功，`j` → {j}：t 的前 {j} 个字母已经是 s 的子序列',
        'if j == m': lambda S, B, r: (f'`j = {S.j} == m`：t 整个都匹配完 → 返回 0' if S.j == S.m else f'`j = {S.j} < m = {S.m}`：还没匹配完，继续往后找'),
        'return m - j': '扫完 s 还剩 `m - j = {m} − {j}` = =={m - j}== 个字母没匹配，全部追加到末尾',
    },
    cards=dict(
        one_liner='t[j] 应匹配 s 里尽量靠前的位置，剩下的全部追加',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['给小写字符串 `s` 和 `t`，只能在 `s` ==末尾==追加字符',
                 '让 `t` 成为 `s` 的子序列，求最少追加几个字符',
                 '示例：`s = coaching`，`t = coding` → `4`（追加 `ding`）'],
        quote='贪心，双指针遍历 s 和 t，t[j] 应匹配 i 尽量小（但大于上一个的匹配的位置）的 s[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['追加只发生在末尾，所以问题等价于：==s 的子序列最多能匹配 t 的多长前缀==',
              '贪心：每个 `t[j]` 都选最靠前的匹配位置，给后面留足空间',
              '遍历 s，`c == t[j]` 就 `j += 1`；最后答案是 `m - j`'],
        summary=['时间 `O(n+m)`，空间 `O(1)`',
                 '第二种写法（本视频）按 s 枚举，`j == m` 时提前返回 0，避免 `t[j]` 越界',
                 '第一种写法按 t 枚举，用 while 在 s 里找 `t[j]`，找不到返回 `len(t) - j`',
                 '同类题：392 判断子序列、2825'],
    ),
)
