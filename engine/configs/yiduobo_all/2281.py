def _txt(S):
    ln = S.get('_line', 0)
    if 'res' in S and 'l' in S and ln >= 37:
        i, l, r = S['index'], S['l'], S['r']
        return f"以 `strength[{i}]={S['strength'][i]}` 为最弱：左右第一个更弱的在 `{l}`、`{r}`，管辖 `[{l+1}, {r-1}]`"
    if 'g' in S and 'res' not in S:
        return '预处理完毕：f 是前缀和，g 是 f 的前缀和'
    if 'res' in S:
        return '第四步：枚举每个巫师当最弱者，用 g 算贡献'
    if 'left' in S:
        return '第二步：从右往左的单调栈，求左边第一个更弱的位置'
    return '第一步：从左往右的单调栈，求右边第一个不大于它的位置'


CONFIG = dict(
    num=2281, title='巫师的总力量和', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='枚举最弱者 + 两层前缀和 + 单调栈',
    tags=['单调栈', '难度分 2621'],
    code='''
class Solution(object):
    def totalStrength(self, strength):

        n = len(strength)

        stack = [0]
        right = [n] * n
        for index in range(1, n):
            while stack and strength[stack[-1]] >= strength[index]:
                right[stack[-1]] = index
                stack.pop()
            
            stack.append(index)

        stack = [n - 1]
        left = [-1] * n
        for index in range(n - 2, -1, -1):
            while stack and strength[stack[-1]] > strength[index]:
                left[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        f = [strength[0]]
        g = [strength[0]]
        mod = 10 ** 9 + 7
        for index in range(1, n):
            f.append((f[-1] + strength[index]) % mod)
            g.append((g[-1] + f[-1]) % mod)

        res = 0
        for index in range(n):
            l = left[index]
            r = right[index]
            now = g[r - 1] * (index - l) % mod
            if index > 0:
                now += g[index - 1] * (l - r)
                now %= mod
                if l > 0:
                    now += g[l - 1] * (r - index)
                    now %= mod
            res = (res + now * strength[index]) % mod

        return res
''',
    call='Solution().totalStrength([3,1,2,1])',
    expect=42,
    views=[
        dict(type='text', h=44, fn=_txt),
        dict(type='array', var='strength', h=100, pointers={'index': 'blue'},
             window=(lambda S: S['l'] + 1 if 'res' in S and 'l' in S else None,
                     lambda S: S['r'] - 1 if 'res' in S and 'r' in S else None),
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='stack', var='stack', h=80, fmt=lambda i: str(i)),
        dict(type='array', var='right', h=80),
        dict(type='array', var='left', h=80),
        dict(type='array', var='f', h=80),
        dict(type='array', var='g', h=80),
    ],
    skip=['now %= mod', 'mod = 10', 'stack.pop()', 'stack = [n - 1]', 'left = [-1] * n', 'g = [strength[0]]'],
    max_steps=100,
    watch=['index', 'l', 'r', ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'while stack and strength[stack[-1]] >=': lambda S, B, ret: (
            f"栈顶 `strength[{S['stack'][-1]}]` = {S['strength'][S['stack'][-1]]} `>=` {S['strength'][S['index']]}：==成立==，右边第一个不大于它的就是下标 `{S['index']}`"
            if S['stack'] and S['strength'][S['stack'][-1]] >= S['strength'][S['index']] else
            ('栈空了，不用再弹' if not S['stack'] else f"栈顶 `{S['strength'][S['stack'][-1]]}` 比 `{S['strength'][S['index']]}` 小 → 停止弹栈")),
        'while stack and strength[stack[-1]] >': lambda S, B, ret: (
            f"栈顶 `strength[{S['stack'][-1]}]` = {S['strength'][S['stack'][-1]]} `>` {S['strength'][S['index']]}：==成立==，左边第一个更小的就是下标 `{S['index']}`"
            if S['stack'] and S['strength'][S['stack'][-1]] > S['strength'][S['index']] else
            ('栈空了，不用再弹' if not S['stack'] else f"栈顶 `{S['strength'][S['stack'][-1]]}` 不大于 `{S['strength'][S['index']]}` → 停止弹栈")),
        'right[stack[-1]] = index': '`right[{stack[-1]}] = {index}`：右边界定为小于等于（带等号），==避免重复元素重复统计==',
        'left[stack[-1]] = index': '`left[{stack[-1]}] = {index}`：左边界是严格小于，不带等号',
        'stack.append(index)': '下标 `{index}` 入栈',
        'f.append': '`f` = strength 的前缀和：`f[{index}] = {f[-1]}`',
        'g.append': '`g` = f 的前缀和：`g[{index}] = {g[-1]}`',
        'l = left': '左边第一个更弱的位置 `l = {l}`（没有则为 -1）',
        'r = right': '右边第一个不大于它的位置 `r = {r}`（没有则为 n）',
        'now = g[r - 1]': '先算 `g[r-1] × (index-l)`：`{g[r-1]} × {index-l}` = =={now}==',
        'now += g[index - 1]': '再减去 `g[index-1] × (r-l)`（`l-r` 为负）：`now` → =={now}==（取模放在下一行）',
        'now += g[l - 1]': '再加 `g[l-1] × (r-index)`，补回多减的部分：`now` → =={now}==',
        'res = (res': '贡献 = `now × strength[{index}]`（最弱值 {strength[index]}），累加：`res = {res}`',
        'if index > 0': '`index = {index}`：{"index > 0，要用 g[index-1]" if index > 0 else "index = 0，g[-1] 没有意义，跳过后两项"}',
        'if l > 0': '`l = {l}`：{"l > 0，才有 g[l-1] 这一项" if l > 0 else "l 不大于 0，没有 g[l-1] 这一项"}',
    },
    cards=dict(
        one_liner='枚举每个巫师当最弱者，统计他管辖区间内的和之和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组总力量 = ==最弱值 × 元素和==，求全部子数组总力量之和，模 `10^9+7`',
                 '示例：`[1,3,1,2]` → `44`；`[5,4,6]` → `213`',
                 '视频用 `[3,1,2,1]` 演示：两个 1 正好演示重复元素'],
        quote='可以枚举每个巫师，设当前枚举到的巫师为strength[p]，那么可以先找出这个巫师左侧和右侧第一个比这个巫师力量更弱的巫师位置，分别记为l和r。',
        quote_src='—— yiduobo 题解',
        idea=['以 `p` 结尾的子串和写成 `f[p] − f[l]` 的形式，拆括号再合并',
              '合并后又是 `f` 的区间和，所以再做一层前缀和 `g`',
              '最终：`g[r-1]·(p-l) + g[p-1]·(l-r) + g[l-1]·(r-p)`，再乘 `strength[p]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`r` 取「小于等于」避免重复元素重复算；`l` 保持严格小于',
                 '用 `g[index-1]`、`g[l-1]` 前要判断 `index > 0`、`l > 0`',
                 '每一步都要取模；单调栈正反各跑一遍'],
    ),
)
