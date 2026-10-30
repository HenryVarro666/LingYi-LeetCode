def _info(S):
    if 't' not in S:
        return '`s` 里的 `0` 只能向左移 → 对每个 `t`，让 `s` 的第 k 个 0 不能在 `t` 的第 k 个 0 的左边'
    t = ''.join(S['t'])
    return f"当前检查 `t = {t}`"


CONFIG = dict(
    num=3998, title='使用子序列排序转换二进制字符串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='双序列双指针 · 0 只能左移，逐个比下标',
    tags=['灵神题单', '难度分 1862'],
    code='''
class Solution:
    def transformStr(self, s: str, strs: list[str]) -> list[bool]:
        total0 = s.count('0')

        def check(t: str) -> bool:
            cnt0 = t.count('0')
            cnt_q = t.count('?')
            # t 中的 '0' 的个数在闭区间 [cnt0, cnt0+cnt_q] 中，total0 必须在这个范围内
            if not cnt0 <= total0 <= cnt0 + cnt_q:
                return False

            # 把前 total0-cnt0 个 '?' 改成 '0'
            t = list(t)
            for i, ch in enumerate(t):
                if cnt0 == total0:
                    break
                if ch == '?':
                    t[i] = '0'
                    cnt0 += 1

            # 判断能否把 s 变成 t
            i = j = 0
            for _ in range(total0):
                # 找下一个 s[i] = '0'
                while s[i] != '0':
                    i += 1

                # 找下一个 t[j] = '0'
                while t[j] != '0':
                    j += 1

                # s 中的 '0' 无法右移，所以无法把 s 变成 t
                if i < j:
                    return False

                i += 1
                j += 1

            return True

        return list(map(check, strs))
''',
    call='Solution().transformStr("0101", ["0?1?", "1?0?"])',
    expect=[True, False],
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='string', var='s', label='s', pointers={'(i if _line >= 22 else None)': 'blue'}, pointer_labels={'(i if _line >= 22 else None)': 'i'}, h=170,
             color=lambda S, idx, v: ('blue' if S.get('_line', 0) >= 22 and idx == S.get('i') and v == '0' else None),
             dim=lambda S, idx, v: S.get('_line', 0) >= 22 and v == '0' and idx < S.get('i', 0)),
        dict(type='string', var='t', label='t', pointers={'(i if _line < 22 else j)': 'pink'}, pointer_labels={'(i if _line < 22 else j)': 'i / j'}, h=170,
             color=lambda S, idx, v: ('green' if v == '0' and S.get('_line', 0) < 22 else
                                      'pink' if S.get('_line', 0) >= 22 and idx == S.get('j') and v == '0' else None),
             dim=lambda S, idx, v: S.get('_line', 0) >= 22 and v == '0' and idx < S.get('j', 0)),
    ],
    watch=['total0', 'cnt0', 'cnt_q', ('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'total0 = s.count': '`s` 里有 `{total0}` 个 `0`，转换后 `t` 里也必须恰好有这么多个 `0`',
        'cnt0 = t.count': '`t` 里已经有 `{cnt0}` 个确定的 `0`',
        'cnt_q = t.count': '还有 `{cnt_q}` 个 `?` 可以变成 `0` 或 `1`',
        'if not cnt0 <= total0': lambda S, B, r: (f"`total0 = {S.total0}` 在 `[{S.cnt0}, {S.cnt0 + S.cnt_q}]` 内 → 个数能凑上" if S.cnt0 <= S.total0 <= S.cnt0 + S.cnt_q else f"`total0 = {S.total0}` 不在 `[{S.cnt0}, {S.cnt0 + S.cnt_q}]` 内 → 0 的个数凑不出 → ==False=="),
        't = list(t)': '转成列表，方便把 `?` 改成 `0`',
        'for i, ch in enumerate(t)': lambda S, B, r: f"从左到右扫 `t`：`t[{S.i}] = '{S.ch}'`" if 'ch' in S and 'i' in S else '从左到右扫 `t`',
        'if cnt0 == total0': lambda S, B, r: (f"`cnt0 = {S.cnt0}` 已等于 `total0` → 0 的个数够了，停" if S.cnt0 == S.total0 else f"`cnt0 = {S.cnt0} < total0 = {S.total0}` → 还要补 0"),
        "if ch == '?'": lambda S, B, r: (f"`t[{S.i}]` 是 `?`" if S.ch == '?' else f"`t[{S.i}]` 不是 `?`，跳过"),
        "t[i] = '0'": '靠左的 `?` 变 `0`：==0 越靠左，越容易被 s 的 0 左移到达==，`t[{i}] = 0`',
        'cnt0 += 1': '`cnt0` → {cnt0}',
        'i = j = 0': '`i` 指向 `s` 的 0，`j` 指向 `t` 的 0，从头开始配对',
        'for _ in range': lambda S, B, r: ("配对下一对 0（第 k 个对第 k 个）" if B.get('_') is None or B.get('_') != S.get('_') else "所有 0 配对完毕"),
        's[i] != ': lambda S, B, r: (f"`s[{S.i}] = '{S.s[S.i]}'` 不是 0 → `i` 右移" if S.s[S.i] != '0' else f"`s[{S.i}]` 是 0 → 这就是 `s` 的下一个 0（位置 {S.i}）"),
        't[j] != ': lambda S, B, r: (f"`t[{S.j}] = '{S.t[S.j]}'` 不是 0 → `j` 右移" if S.t[S.j] != '0' else f"`t[{S.j}]` 是 0 → 这是 `t` 的下一个 0（位置 {S.j}）"),
        'if i < j': lambda S, B, r: (f"`i = {S.i} < j = {S.j}`：`s` 的 0 在 `t` 的 0 的左边，而 0 只能左移 → ==False==" if S.i < S.j else f"`i = {S.i} >= j = {S.j}`：`s` 的 0 能左移到 `t` 的位置 → 这一对没问题"),
        'i += 1': lambda S, B, r: (f"`i` → {S.i}" if S._line == 26 else f"这一对配好：`i` → {S.i}"),
        'j += 1': lambda S, B, r: (f"`j` → {S.j}" if S._line == 30 else f"`j` → {S.j}：这一对配好，找下一对"),
        'return True': '所有 0 都能左移到位 → ==True==',
        'return False': lambda S, B, r: ('这个 `t` 不可能 → `False`'),
        'return list(map': lambda S, B, r: ('对每个 `t` 调用 `check`，收集成布尔列表' if r is None or not isinstance(r, list) else f'每个 `t` 的结果：`{r}`'),
    },
    skip=['t = list(t)'],
    cards=dict(
        one_liner='s 里的 0 只能向左移：逐个对比 0 的下标',
        complexity='时间 `O(nm)`，空间 `O(1)`（写法三）；本视频用写法一，空间 `O(n)`',
        problem=['对 `s` 的任意子序列升序排序，可以做任意多次',
                 '`strs[i]` 里的 `?` 可以换成 `0` 或 `1`',
                 '判断每个 `strs[i]` 能否由 `s` 变出来',
                 '本视频：`s = 0101`，`strs = ["0?1?", "1?0?"]` → `[true, false]`'],
        quote='这意味着，`s` 中的 `0` 只能向左移动。……每个 `P[j]` 都要 `>= Q[j]`，才能保证我们能把 `s` 变成 `t`。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子序列排序 = 反复把「左 1 右 0」换成「左 0 右 1」，所以 0 只会向左',
              '`?` 靠左的变 `0`、靠右的变 `1`：0 越靠左越好达成，还要保证 0 的个数相等',
              '`P` 是 s 的 0 的下标，`Q` 是 t 的：必须逐个有 `P[k] >= Q[k]`'],
        summary=['时间 `O(nm)`；写法一空间 `O(n)`',
                 '先判断 0 的个数能否凑上，再把靠左的 `?` 变 0',
                 '`?` 全变 0 的数量只补到刚好够，其余 `?` 视作 1',
                 '题解另有写法二（把补 0 并入双指针）、写法三（前缀 1 的个数，`s` 的 1 不能少于 `t` 的 1，空间 O(1)）'],
    ),
)
