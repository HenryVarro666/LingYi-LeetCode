def _win(which):
    def fn(S):
        try:
            if S['_line'] >= 38 or 'f' not in S:
                return None
            idx = S['index']
            if idx >= len(S['f']):
                return None
            r = S['f'][idx]
            return idx - r + 1 if which == 0 else idx + r - 1
        except Exception:
            return None
    return fn


def _top(S):
    ln = S['_line']
    if 'index' not in S:
        return '在 `$` 和 `#` 夹住的字符串上做马拉车：`f[p]` = 以 `s[p]` 为中心的最长奇回文的“半径”（含中心）'
    idx = S['index']
    s = S['s']
    if ln < 22:
        if idx < len(S['f']):
            return f"`f[{idx}] = {S['f'][idx]}`：以 `{s[idx]}` 为中心的最长奇回文长度 = `2×{S['f'][idx]}-1 = {2 * S['f'][idx] - 1}`"
        return f"求 `f[{idx}]`：中心 `{s[idx]}`，已知回文区间的中心 `mid = {S['mid']}`，右端 `right = {S['right']}`"
    if ln < 29:
        return '`l_max[q]`：右端点不超过 `q` 的最长奇回文长度（只看左侧）'
    if ln < 38:
        return '`r_max`：从右往左同理（先倒着存，最后 `reverse`）'
    return '枚举分割线：`l_max[index-1] × r_max[index]`，取最大'


def _cur(S, B, ret):
    return ''


CONFIG = dict(
    num=1960, title='两个回文子字符串长度的最大乘积', difficulty='Hard', category='字符串',
    author='yiduobo', technique='马拉车 + 左右最长回文预处理',
    tags=['灵神题单', '字符串', '难度分 2691'],
    code='''
class Solution(object):
    def maxProduct(self, s):

        s = '$' + s + '#'
        mid = 0
        right = 0
        f = [0]
        for index in range(1, len(s) - 1):
            if index <= right:
                f.append(min(right - index, f[mid + mid - index]))
            else:
                f.append(1)
            
            while s[index + f[index]] == s[index - f[index]]:
                f[index] += 1
            
            if right < f[index] + index:
                right = f[index] + index
                mid = index
        
        l_max = [0]
        pos = 0
        for index in range(1, len(s) - 1):
            while pos < index + f[index] - 1:
                pos += 1
                l_max.append(max(l_max[-1], (pos - index) * 2 + 1))
        
        r_max = [0]
        pos = len(s) - 1
        for index in range(len(s) - 2, 0, -1):
            while pos > index - f[index] + 1:
                pos -= 1
                r_max.append(max(r_max[-1], (index - pos) * 2 + 1))
        r_max.append(0)
        r_max.reverse()

        res = l_max[1] * r_max[2]
        for index in range(2, len(s) - 1):
            res = max(res, l_max[index - 1] * r_max[index])

        return res
''',
    call='Solution().maxProduct("abab")',
    expect=3,
    skip=['else:', 'pos += 1', 'pos -= 1', 'f.append(1)', 'right = f[index] + index', 'r_max.append(0)', 'pos = 0', 'pos = len(s) - 1', 'mid = 0', 'right = 0', 23, 30, 38, 'f.append(min', 'f = [0]', 'l_max = [0]', 'r_max = [0]'],
    max_steps=110,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='string', var='s', label='s（首尾加了哨兵 $ 和 #；蓝框 = 以 index 为中心的回文）',
             pointers={'index': 'blue', 'mid': 'cyan', 'right': 'pink', 'pos': 'orange'},
             window=(_win(0), _win(1)), dim=lambda S, i, v: v in ('$', '#'), h=240),
        dict(type='array', var='f', label='f（回文半径，含中心；蓝 = index 位置）', h=150,
             color=lambda S, i, v: 'blue' if S.get('index') == i and S['_line'] < 38 else None),
        dict(type='array', var='l_max', label='l_max（左侧最长奇回文）', h=150),
        dict(type='array', var='r_max', label='r_max（右侧最长奇回文；倒着存，reverse 后对齐下标）', h=150),
    ],
    watch=[('index', 'index', 'blue'), ('mid', 'mid', 'cyan'), ('right', 'right', 'pink'), ('pos', 'pos', 'orange'), ('res', 'res', 'green')],
    captions={
        "s = '$'": '两端加哨兵 `$`、`#`：扩展回文时碰到哨兵必然不等，不用判越界。`f[p]` 是以 `s[p]` 为中心的回文半径（含中心）',
        'f = [0]': '`f[p]` = 以 `s[p]` 为中心的最长奇回文半径（含中心），回文长度 = `2f - 1`；`mid`、`right` 记==最靠右的回文==的中心和右端',
        8: lambda S, B, ret: (f"求 `f[{S.index}]`：中心 `{S.s[S.index]}`" if S.index != B.get('index') or len(S.f) == 1 else '第一趟结束，`f` 全部算完'),
        'if index <= right': lambda S, B, ret: (
            f'`index = {S.index} <= right = {S.right}`：在 `mid = {S.mid}` 的回文里 → 镜像位置 `{S.mid + S.mid - S.index}` 的半径 `{S.f[S.mid + S.mid - S.index]}`，且不能超出 `right - index = {S.right - S.index}` → ==取较小者== `f[{S.index}] = {min(S.right - S.index, S.f[S.mid + S.mid - S.index])}`'
            if S.index <= S.right else f'`index = {S.index} > right = {S.right}`：没有可借用的信息，`f[{S.index}]` 从 1 开始'),
        'f.append(1)': '先假定半径 1（只有中心自己），再向两边扩',
        'while s[index + f[index]]': lambda S, B, ret: (
            (f"半径是 0：先拿中心 `s[{S.index}]` 和自己比，必然相等，半径变 1" if S.f[S.index] == 0 else
             f"比 `s[{S.index + S.f[S.index]}] = {S.s[S.index + S.f[S.index]]}` 和 `s[{S.index - S.f[S.index]}] = {S.s[S.index - S.f[S.index]]}` → ==相等==，半径再加 1")
            if S.s[S.index + S.f[S.index]] == S.s[S.index - S.f[S.index]]
            else f"比 `s[{S.index + S.f[S.index]}] = {S.s[S.index + S.f[S.index]]}` 和 `s[{S.index - S.f[S.index]}] = {S.s[S.index - S.f[S.index]]}` → ==不等==，停止，`f[{S.index}] = {S.f[S.index]}`"),
        'f[index] += 1': '半径 → `f[{index}] = {f[index]}`',
        'if right < f[index] + index': lambda S, B, ret: (f'`f[{S.index}] + index = {S.f[S.index] + S.index}` > `right = {S.right}`：这个回文伸得更靠右 → 更新 `mid`、`right`'
                                                          if S.right < S.f[S.index] + S.index else f'`f[{S.index}] + index = {S.f[S.index] + S.index}` <= `right`：没伸得更远，不更新'),
        'right = f[index] + index': '`right` → {right}',
        'mid = index': '更新：`mid = {mid}`，`right = {right}`',
        'l_max = [0]': '第二趟：`l_max[q]` = 右端不超过 `q` 的最长奇回文长度',
        'pos = 0': '`pos` = 已经处理到的右端位置',
        'while pos < index + f[index] - 1': lambda S, B, ret: (
            f'中心 `{S.s[S.index]}` 的回文右端到 `{S.index + S.f[S.index] - 1}`，`pos = {S.pos}` 还没到 → ==继续记录新的右端=='
            if S.pos < S.index + S.f[S.index] - 1 else
            f'中心 `{S.s[S.index]}` 的回文右端 `{S.index + S.f[S.index] - 1}` 已经记录过（`pos = {S.pos}`）→ 换下一个中心'),
        'l_max.append': '右端为 `{pos}` 的回文长 `({pos} - {index}) × 2 + 1 = {(pos - index) * 2 + 1}`，和前一个比取大 → `l_max` 末尾 =={l_max[-1]}==',
        'r_max = [0]': '第三趟：从右往左，同样的做法求 `r_max`',
        'pos = len(s) - 1': '`pos` 从最右边开始往左',
        'while pos > index - f[index] + 1': lambda S, B, ret: (
            f'从右往左：中心 `{S.s[S.index]}` 的回文左端到 `{S.index - S.f[S.index] + 1}`，`pos = {S.pos}` 还没到 → ==继续=='
            if S.pos > S.index - S.f[S.index] + 1 else
            f'中心 `{S.s[S.index]}` 的回文左端 `{S.index - S.f[S.index] + 1}` 已经记录过（`pos = {S.pos}`）→ 换下一个中心'),
        'r_max.append(max': '左端为 `{pos}` 的回文长 `({index} - {pos}) × 2 + 1 = {(index - pos) * 2 + 1}`，取大 → =={r_max[-1]}==',
        'r_max.append(0)': '补一个 0，下标对齐',
        'r_max.reverse()': '补一个 0 并倒过来，`r_max[q]` = 左端不小于 `q` 的最长奇回文长度',
        'res = l_max[1]': '`res` 初值，先取第一条分割线（1 与 2 之间）：`l_max[1] × r_max[2] = {l_max[1]} × {r_max[2]}` = =={res}==',
        'res = max(res': lambda S, B, ret: (f'分割线在 `{S.index - 1}` | `{S.index}`：`l_max[{S.index - 1}] × r_max[{S.index}] = {S.l_max[S.index - 1]} × {S.r_max[S.index]} = {S.l_max[S.index - 1] * S.r_max[S.index]}`，`res` = =={S.res}=='
                                            + ('（和初值是同一条线）' if S.index == 2 else '')),
        'return res': '两个回文长度的最大乘积是 =={ret}==',
    },
    cards=dict(
        one_liner='枚举分割线，左右两边各取最长奇回文；马拉车预处理',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在字符串里选两个==不重叠==、==长度为奇数==的回文子串',
                 '求两个长度乘积的最大值',
                 '示例：`ababbb` → `aba` 和 `bbb`，`3 × 3 = 9`；本视频用 `abab` → `aba` 和 `b`，`3 × 1 = 3`'],
        quote='一般做法就是枚举中间的分割线，在分割线的左侧和右侧分别找出最长的回文子串，然后使用这两个串长度的乘积来更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`l_max[q]` / `r_max[q]`：分割线左 / 右的最长奇回文；分割线两边相乘取最大',
              '先马拉车算出每个中心的半径 `f`，只有奇回文所以不必插分隔符',
              '回文 `[p-k, p+k]` 的右端是 `p+k`：用一个 `pos` 只往右走，每个右端位置只算一次，整体线性'],
        result='`l_max`、`r_max` 对齐后，分割线处 `3 × 1 = 3` 最大 ✓',
        summary=['时间 `O(n)`，空间 `O(n)`；`n` 最大 10^5，不能 `O(n^2)`',
                 '哨兵 `$`、`#` 让扩展时不用判越界；`f` 是半径，回文长度是 `2f - 1`',
                 '`pos` 只增不减：被更靠前中心盖住的回文不会产生新的更长答案',
                 '原文本来就能在 Python 3 运行，代码未改动（没有整数除法）'],
    ),
)
