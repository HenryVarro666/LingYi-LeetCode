def _phase2(S):
    return 'c' in S


def _ptr_j(S):
    j = S.get('j')
    return j if isinstance(j, int) and 0 <= j < len(S['t']) else None


def _s_color(S, k, v):
    ans, t = S.get('ans'), S['t']
    if ans and k in ans:
        pos = ans.index(k)
        return 'orange' if S['s'][k] != t[pos] else 'green'
    return None


def _t_color(S, k, v):
    if 'j' not in S:
        return None
    j = S['j']
    if not _phase2(S):
        return 'orange' if k > j else None
    if k < j:
        ans = S.get('ans') or []
        return 'orange' if (k < len(ans) and S['s'][ans[k]] != S['t'][k]) else 'green'
    return None


def _top(S):
    if 'i' not in S:
        return ''
    if not _phase2(S):
        return '第一阶段：从右往左，算 `suf[i]`：`t[suf[i]:]` 是 `s[i:]` 的子序列'
    return f"第二阶段：从左往右贪心，已改过 = {'是' if S['changed'] else '否'}；答案下标 = {S['ans']}"


CONFIG = dict(
    num=3302, title='字典序最小的合法序列', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前后缀分解 · 贪心匹配',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·动态规划', '难度分 2474'],
    code='''
class Solution:
    def validSequence(self, s: str, t: str) -> List[int]:
        n, m = len(s), len(t)
        suf = [0] * (n + 1)
        suf[n] = m
        j = m - 1
        for i in range(n - 1, -1, -1):
            if j >= 0 and s[i] == t[j]:
                j -= 1
            suf[i] = j + 1

        ans = []
        changed = False  # 是否修改过
        j = 0
        for i, c in enumerate(s):
            if c == t[j] or not changed and suf[i + 1] <= j + 1:
                if c != t[j]:
                    changed = True
                ans.append(i)
                j += 1
                if j == m:
                    return ans
        return []
''',
    call="Solution().validSequence('bacdc', 'abc')",
    expect=[1, 2, 4],
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='string', var='s', label='s = word1（绿 = 直接匹配的下标，橙 = 改一个字母后匹配的下标）', cell=84, h=190,
             pointers={'i': 'pink'}, color=_s_color),
        dict(type='string', var='t', label='t = word2（橙 = suf 阶段已匹配的后缀，绿 = 已匹配的前缀）', cell=84, h=190,
             pointers={_ptr_j: 'blue'}, pointer_labels={_ptr_j: 'j'}, color=_t_color),
        dict(type='array', var='suf', label='suf[i]：t[suf[i]:] 是 s[i:] 的子序列（suf[i] 尽量小）', cell=84, h=140, pointers={'i': 'pink'}),
    ],
    watch=[('i', 'i', 'pink'), ('j', 'j', 'blue'), ('suf', 'suf', 'orange'), ('changed', 'changed', 'red'), ('ans', 'ans', 'green')],
    captions={
        'n, m = len': '`s = "{s}"`，`t = "{t}"`：选 s 的一个下标序列，改至多一个字母后等于 t，要字典序最小',
        'suf = [0] * (n + 1)': '`suf[i]`：`s[i:]` 能匹配 ==t 的最长后缀== 的起点（越小匹配得越长）',
        'suf[n] = m': '`s[n:]` 是空串，只能匹配空后缀，起点是 `m`',
        'j = m - 1': '`j` 指向 t 的末尾，从后往前匹配：`j = {j}`',
        'for i in range(n - 1, -1, -1)': lambda S, B, r: ('第一阶段结束，`suf` 算完了' if S.get('i') == B.get('i') and 'i' in B else f'`i` 从后往前：`i = {S.i}`'),
        'if j >= 0 and s[i] == t[j]': lambda S, B, r: (
            f"`s[{S.i}] = '{S.s[S.i]}'` == `t[{B.j}] = '{S.t[B.j]}'` → 匹配，后缀变长" if B.j >= 0 and S.s[S.i] == S.t[B.j]
            else (f"`s[{S.i}] = '{S.s[S.i]}'` ≠ `t[{B.j}] = '{S.t[B.j]}'` → 匹配不上，`j` 不动" if B.j >= 0 else "`j < 0`：t 已经匹配完了")),
        'j -= 1': '`j` → {j}',
        'suf[i] = j + 1': '`suf[{i}] = {j + 1}`：`t[{j + 1}:]` 是 `s[{i}:]` 的子序列',
        'ans = []': '第二阶段：从左往右扫 s，把选中的下标放进 `ans`',
        'changed = False': '`changed` 记录有没有用掉那次修改机会',
        'j = 0': '`j` 指向 t 里下一个要匹配的字母，从 `0` 开始',
        'for i, c in enumerate(s)': lambda S, B, r: ('s 扫完了还没匹配完 → 没有合法序列' if S.get('i') == B.get('i') and S.get('c') == B.get('c') else f"扫描 `s[{S.i}] = '{S.c}'`"),
        'if c == t[j] or': lambda S, B, r: (
            f"`'{S.c}'` == `t[{S.j}] = '{S.t[S.j]}'` → 能匹配就==立刻匹配==，否则第 `{S.j}` 个下标只会更大" if S.c == S.t[S.j]
            else (f"`'{S.c}'` ≠ `t[{S.j}] = '{S.t[S.j]}'`，但还没改过，且 `suf[{S.i+1}] = {S.suf[S.i+1]} ≤ j+1 = {S.j+1}` → 改它，后面仍能匹配 → ==必须改=="
                  if (not S.changed and S.suf[S.i + 1] <= S.j + 1) else
                  f"`'{S.c}'` ≠ `t[{S.j}] = '{S.t[S.j]}'`" + (f'，`suf[{S.i+1}] = {S.suf[S.i+1]} > j+1 = {S.j+1}`：改了后面也匹配不完 → 跳过' if not S.changed else '，已经改过了 → 跳过'))),
        'if c != t[j]': lambda S, B, r: ('不相等，这次要用掉修改机会' if S.c != S.t[S.j] else '本来就相等，不用改'),
        'changed = True': '修改机会用掉了：`changed = True`',
        'ans.append(i)': '`ans` 加入下标 `{i}`：`{ans}`',
        'j += 1': '`t` 匹配到下一位：`j` → {j}',
        'if j == m': lambda S, B, r: (f'`j == m = {S.m}`：t 全匹配完 → 返回 `ans`' if S.j == S.m else f'`j = {S.j} < m = {S.m}`，继续'),
        'return ans': '找到了字典序最小的合法下标序列 `{ans}`',
        'return []': 's 扫完仍未匹配完 → 返回空数组',
    },
    cards=dict(
        one_liner='前后缀分解：能匹配就匹配；不能匹配时，能改就必须改',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选 `word1` 的升序下标序列，对应字母改==至多一个==后等于 `word2`，求字典序最小的下标序列',
                 '示例：`word1 = "bacdc"`，`word2 = "abc"` → `[1,2,4]`',
                 '`word1 = "aaaaaa"`，`word2 = "aaabc"` → `[]`'],
        quote='如果 s[i]=t[j]，既然能匹配上，那么就立刻匹配……如果 s[i]≠t[j] 且 suf[i+1]≤j+1，说明修改 s[i] 为 t[j] 后，t[j+1:] 是 s[i+1:] 的子序列。此时一定要修改。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先倒着算 `suf[i]`：`t` 最长的后缀，能当 `s[i:]` 的子序列（和 2565 一样的前后缀分解）',
              '再从左往右贪心：==能匹配就匹配==，这样每个下标都最小',
              '不匹配时，如果还没改过，且改完后面仍能匹配（`suf[i+1] ≤ j+1`），就==立刻改=='],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '第一阶段 `j` 可能减到 `-1`，所以条件里要先判 `j >= 0`',
                 '`changed` 只能用一次；改了之后只能靠直接匹配',
                 '`j == m` 立刻返回，避免下一轮 `t[j]` 越界',
                 '无解时循环结束，返回 `[]`；不修改版本见 2565'],
    ),
)
