def _fml(S):
    idx = S.get('index')
    if idx is None or S.get('_line', 0) < 20:
        return '`f[i]`：前 i 个箱子的最少趟数；`cnt`：相邻目的地不同的对数；`w_s`：重量前缀和'
    st, l = S['stack'], S['l']
    if l >= len(st):
        return f'第 `{idx + 1}` 个箱子：窗口里没有可用的 j'
    j = st[l]
    return f'`f[{idx + 1}] = f[{j}] + cnt[{idx + 1}] − cnt[{j + 1}] + 2`（j = ==队首== {j}）'


def _boxcolor(S, k, v):
    idx = S.get('index')
    if idx is None:
        return None
    if k == idx:
        return 'yellow'
    st, l = S.get('stack'), S.get('l')
    if st is not None and l is not None and l < len(st) and st[l] <= k < idx:
        return 'blue'
    return None


def _cap_front(S, B, ret):
    st, l, ms = S.stack, S.l, S.w_s
    if l >= len(st):
        return '窗口里已经没有可用的 j'
    j = st[l]
    n_box = S.index + 1 - j
    wt = ms[S.index + 1] - ms[j]
    why = []
    if n_box > S.maxBoxes:
        why.append(f'箱数 `{n_box}` > `maxBoxes = {S.maxBoxes}`')
    if wt > S.maxWeight:
        why.append(f'重量 `{wt}` > `maxWeight = {S.maxWeight}`')
    if why:
        return f'队首 `j = {j}`：' + '，'.join(why) + ' → ==一车装不下，左边界右移=='
    return f'队首 `j = {j}`：箱数 `{n_box}` ≤ {S.maxBoxes}，重量 `{wt}` ≤ {S.maxWeight} → ==合法，停止移动=='


def _cap_tail(S, B, ret):
    st, l, f, cnt, index = S.stack, S.l, S.f, S.cnt, S.index
    if len(st) <= l:
        return '队列里已无元素，直接入队'
    j = st[-1]
    a, b = f[j] - cnt[j + 1], f[-1] - cnt[index + 2]
    if a >= b:
        return f'队尾 `j={j}`：`f−cnt` = `{a}` ≥ 新的 `{b}` → 更靠前又不更小，==以后不会用到它==，弹出'
    return f'队尾 `j={j}`：`f−cnt` = `{a}` < 新的 `{b}` → 保留'


CONFIG = dict(
    num=1687, title='从仓库到码头运输箱子', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前缀和 + 单调队列优化 DP', tags=['动态规划'],
    code='''
class Solution(object):
    def boxDelivering(self, boxes, portsCount, maxBoxes, maxWeight):

        cnt = [0]
        w_s = [0]
        n = len(boxes)
        for index in range(n):
            cnt.append(cnt[-1])
            if index > 0 and boxes[index][0] != boxes[index - 1][0]:
                cnt[-1] += 1
            
            w_s.append(w_s[-1] + boxes[index][1])

        cnt.append(cnt[-1])

        f = [0]
        stack = [0]
        l = 0
        for index in range(n):
            while l < len(stack) and (index + 1 - stack[l] > maxBoxes or w_s[index + 1] - w_s[stack[l]] > maxWeight):
                l += 1

            f.append(f[-1] + 2)
            if l < len(stack):
                f[-1] = min(f[-1], f[stack[l]] + cnt[index + 1] - cnt[stack[l] + 1] + 2)

            while len(stack) > l and f[stack[-1]] - cnt[stack[-1] + 1] >= f[-1] - cnt[index + 2]:
                stack.pop()
            
            stack.append(index + 1)

        return f[-1]
''',
    call='Solution().boxDelivering([[1, 2], [3, 3], [3, 1], [3, 1], [2, 4]], 3, 3, 6)',
    expect=6,
    skip=['cnt = [0]', 'w_s = [0]', 'n = len', 'cnt.append(cnt[-1])', 'cnt[-1] += 1', 'w_s.append', 'cnt.append(cnt[-1])\n', 'for index in range'],
    max_steps=90,
    views=[
        dict(type='text', fn=_fml, size=22, h=50),
        dict(type='array', var=lambda S: [b[0] for b in S['boxes']], label='port', h=110, cell=76, color=_boxcolor),
        dict(type='array', var=lambda S: [b[1] for b in S['boxes']], label='weight', h=110, cell=76, color=_boxcolor),
        dict(type='array', var='cnt', label='cnt', h=110, cell=76),
        dict(type='array', var='f', label='f', h=110, cell=76),
        dict(type='queue', var='stack', label='stack', h=110, fmt=lambda j: f'{j}'),
    ],
    watch=[('index', 'index', 'blue'), ('l', 'l', 'pink'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'cnt.append(cnt[-1])\n': '',
        'if index > 0 and': lambda S, B, r: ('第一个箱子，前面没有箱子可比' if S.index == 0 else f'箱 `{S.index}` 与箱 `{S.index - 1}` 港口 `{S.boxes[S.index][0]}` / `{S.boxes[S.index - 1][0]}` ' + ('不同 → 要多走一趟，`cnt` 加 1' if S.index > 0 and S.boxes[S.index][0] != S.boxes[S.index - 1][0] else '相同 → 不用多走')),
        'while l < len(stack)': _cap_front,
        'l += 1': '左边界 `l` → {l}（队首后移）',
        'f.append(f[-1] + 2)': '先假设第 `{index+1}` 个箱子==单独装一车==：来回 2 趟 → `f = f[-2] + 2` = =={f[-1]}==',
        'f[-1] = min': lambda S, B, r: (f'借队首 `j={S.stack[S.l]}`：箱 `{S.stack[S.l]+1}..{S.index+1}` 一车运完，`f[j] + cnt[i] − cnt[j+1] + 2` = {S.f[S.stack[S.l]]} + {S.cnt[S.index + 1] - S.cnt[S.stack[S.l] + 1]} + 2 → `f[{S.index + 1}]` = =={S.f[-1]}=='),
        'while len(stack) > l': _cap_tail,
        'stack.pop()': '弹出队尾 → `stack = {stack}`',
        'stack.append(index + 1)': '`{index+1}` 入队 → `stack = {stack}`',
        'return f[-1]': '运完全部箱子最少 `{ret}` 趟',
    },
    cards=dict(
        one_liner='f[i] = f[j] + cnt[i] − cnt[j] + 2：区间最小值用单调队列',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['卡车按顺序运箱子，一次最多 `maxBoxes` 个箱、总重 `≤ maxWeight`，`boxes[i] = [港口, 重量]`',
                 '一车送完要「去一趟、返回一趟」，相邻箱港口不同要多走 1 趟',
                 '本视频：`[[1,2],[3,3],[3,1],[3,1],[2,4]]`，`maxBoxes=3`，`maxWeight=6`'],
        quote='cost(j + 1, i) = cnt[i] - cnt[j] + 2，这里的2表示最开始出发以及最后返回这两趟。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i] = min(f[j] + cnt[i] − cnt[j] + 2)`，`j` 受「箱数、重量」限制 → 滑动窗口',
              '`cnt[i]`、`2` 固定，只要窗口里最小的 `f[j] − cnt[j]`',
              '队尾 `f−cnt` 不小于新值就弹出；队首超出箱数/重量限制就右移 `l`'],
        summary=['时间 `O(n)`，空间 `O(n)`：每个位置至多入队一次',
                 '作者用指针 `l` 当队首，队尾仍然 `pop`',
                 '`cnt` 比 `boxes` 多一个，下标有 `+1`、`+2` 的偏移，容易写错',
                 '原文为 Python 2 风格，无需改动，直接在 Python 3 运行'],
    ),
)
