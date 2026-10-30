S0 = '2560'
SEG_COLORS = ['blue', 'pink', 'purple', 'cyan']


def _inner(S, k):
    return (S.get('_inner') or {}).get(k)


def _seg_of(S):
    """当前分支里 s 的每个字符属于第几段（只看 path[:j]）"""
    j, path = _inner(S, 'j'), S.get('path')
    if j is None or path is None:
        return {}
    out, p = {}, 0
    for k in range(j):
        for _ in path[k]:
            out[p] = k
            p += 1
    return out


def _s_color(S, idx, v):
    seg = _seg_of(S).get(idx)
    return SEG_COLORS[seg] if seg is not None else None


def _s_dim(S, idx, v):
    i, r = _inner(S, 'i'), _inner(S, 'right')
    return i is not None and idx >= i and (r is None or idx > r)


def _prune_text(S):
    i, j = _inner(S, 'i'), _inner(S, 'j')
    if i is None:
        return '每段颜色 = 第几段；框 = 当前这一段 `s[i..right]`'
    n = S['n']
    rem, seg = n - i, 4 - j
    ok = seg <= rem <= seg * 3
    return (f'剩 `{rem}` 个字符分 `{seg}` 段：`{seg} ≤ {rem} ≤ {seg * 3}`？' +
            ('==可以==' if ok else '==剪枝=='))


def _cap_prune(S, B, ret):
    i, j, n = S.i, S.j, S.n
    rem, seg = n - i, 4 - j
    if seg <= rem <= seg * 3:
        return f'剩 `{rem}` 个字符分 `{seg}` 段：`{seg} ≤ {rem} ≤ {seg * 3}` ✓'
    why = '太少了（每段至少 1 个）' if rem < seg else '太多了（每段至多 3 个）'
    return f'剩 `{rem}` 个字符分 `{seg}` 段：{why} → ==剪枝=='


def _cap_for(S, B, ret):
    if 'right' not in B or B.get('i') != S.i or S.right != B.right:
        return f"第 `{S.j}` 段：右端点试 `right = {S.right}`"
    return f'第 `{S.j}` 段的右端点都试过了 → 返回上一层'


def _cap_gt(S, B, ret):
    if S.ip_val > 255:
        return f'`{S.ip_val} > 255`：不合法，再往右只会更大 → ==break=='
    return f'`{S.ip_val} ≤ 255`，合法'


def _cap_zero(S, B, ret):
    if S.ip_val == 0:
        return f"这一段是 `'0'`：再往右取会有==前导零== → break"
    return f'`ip_val = {S.ip_val}` 不是 0，可以继续往右延长这一段'


CONFIG = dict(
    num=93, title='复原 IP 地址', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='划分型回溯 · 枚举右端点 + 剪枝',
    tags=['热题173'],
    code='''
class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        n = len(s)
        ans = []
        path = [''] * 4

        # 分割 s[i] 到 s[n-1]，现在在第 j 段（j 从 0 开始）
        def dfs(i: int, j: int) -> None:
            # 剪枝：还剩下 n-i 个字符，需要分成 4-j 段，每段至少 1 个字符，至多 3 个字符，所以 4-j <= n-i <= (4-j)*3
            if not 4 - j <= n - i <= (4 - j) * 3:
                return

            if i == n:  # s 分割完毕
                ans.append('.'.join(path))
                return

            # 子串左端点为 i
            # 枚举子串右端点 right
            ip_val = 0
            for right in range(i, n):
                ip_val = ip_val * 10 + int(s[right])
                if ip_val > 255:  # 不合法
                    break
                path[j] = s[i: right + 1]  # 直接覆盖 path[j]，无需恢复现场
                dfs(right + 1, j + 1)
                if ip_val == 0:  # 前导零，对于后续循环不合法
                    break

        dfs(0, 0)
        return ans
''',
    call=f"Solution().restoreIpAddresses('{S0}')",
    expect=['2.5.6.0'],
    skip=['n = len(s)', 'ans = []', 'ip_val = 0'],
    views=[
        dict(type='string', var='s', label='s（颜色 = 已切好的段，框 = 当前段 s[i..right]）', cell=76, h=150,
             window=(lambda S: _inner(S, 'i'), lambda S: _inner(S, 'right')), color=_s_color, dim=_s_dim),
        dict(type='text', fn=_prune_text, h=50, size=24),
        dict(type='array', var='path', label='path（固定 4 段，直接覆盖）', cell=76, h=180, pointers={'j': 'yellow'},
             color=lambda S, k, v: SEG_COLORS[k] if _inner(S, 'j') is not None and k < _inner(S, 'j') else None),
        dict(type='calls', h=160),
        dict(type='stack', var='ans', label='ans', h=90),
    ],
    watch=[('i', "_inner['i'] if 'i' in _inner else None", 'blue'), ('j', "_inner['j'] if 'j' in _inner else None", 'yellow'),
           ('right', "_inner['right'] if 'right' in _inner else None", 'cyan'),
           ('ip_val', "_inner['ip_val'] if 'ip_val' in _inner else None", 'green')],
    captions={
        "path = [''] * 4": '`path` 长度固定为 4：每次==直接覆盖 path[j]==，不用恢复现场',
        'dfs(0, 0)': '`dfs(0, 0)`：从 `s[0]` 开始切第 0 段',
        'if not 4 - j <= n - i': _cap_prune,
        11: '剪掉这个分支，返回',
        'if i == n': lambda S, B, r: ('`i == n`：s 分割完毕（剪枝保证此时==恰好 4 段==）' if S.i == S.n
                                      else f'`i = {S.i}`：第 `{S.j}` 段的左端点是 `s[{S.i}]`'),
        "ans.append('.'.join(path))": '找到一个合法 IP：`{ans[-1]}`',
        15: '返回上一层',
        'for right in range': _cap_for,
        'ip_val = ip_val * 10': lambda S, B, r: (
            f'`ip_val = {B.ip_val}×10 + {S.s[S.right]} = {S.ip_val}`' + ('：手动把字符串转成整数，严格 `O(1)`' if S.right == 0 else '')),
        'if ip_val > 255': _cap_gt,
        'path[j] = s[i: right + 1]': lambda S, B, r: (
            f"`path[{S.j}] = '{S.path[S.j]}'`" + ('：直接覆盖，==无需恢复现场==' if S.right == 0 else '')),
        'dfs(right + 1, j + 1)': '递归切下一段：`dfs({B.right + 1}, {B.j + 1})`',
        23: '跳出循环：右端点再往右，数值只会更大',
        27: '跳出循环（`0` 后面不能再接数字）',
        'if ip_val == 0': _cap_zero,
        'return ans': '搜索结束，返回 `{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='把 s 切成恰好 4 段：枚举每段的右端点，剩余长度不对就剪枝',
        complexity='时间 `O(m^4)`，`m = min(n, 12)`；空间 `O(1)`（不计返回值）',
        problem=['有效 IP：恰好 4 个 `0`–`255` 的整数，用 `.` 分隔，==不能有前导 0==',
                 '给只含数字的字符串 `s`，返回所有能通过插入 `.` 得到的有效 IP（不能重排或删除数字）',
                 '示例：`"25525511135"` → `["255.255.11.135","255.255.111.35"]`',
                 '本视频：`"2560"` → `["2.5.6.0"]`'],
        quote='剪枝：还剩下 n−i 个字符，需要分成 4−j 段，每段至少 1 个字符，至多 3 个字符，所以必须满足 ==4−j ≤ n−i ≤ (4−j)·3==，若不满足则返回。',
        quote_src='—— 灵茶山艾府题解「方法二 · 写法二：枚举选哪个」',
        idea=['`dfs(i, j)`：剩余 `s[i..n-1]`，现在切第 `j` 段；枚举这一段的右端点 `right`',
              '边枚举边维护 `ip_val`：`> 255` 就 break；==这一段是 0 时也 break==（前导零）',
              '剪枝保证到 `i == n` 时恰好切了 4 段'],
        result='`["2.5.6.0"]` ✓：`256 > 255` 和前导零都被正确排除',
        summary=['递归 `O(m^3)` 次（`m−1` 个空隙选 3 个放点号），生成答案 `O(m)` → `O(m^4)`',
                 '`n > 12` 一定无解，已经包含在剪枝里',
                 '`path` 长度固定，直接覆盖 `path[j]`；若用空列表 `append` 就要恢复现场',
                 '方法一：三重循环枚举三个点号的位置；写法一：选或不选（是否在 s[i] 后分割）'],
    ),
)
