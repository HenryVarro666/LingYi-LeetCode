CANDS = [2, 5, 2, 1, 2]


def _jump(cv, S, B, box, T):
    """candidates 数组 + next_pos 跳转弧线：index 回溯后直接跳到下一个不同的数"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'candidates（已排序）　弧线 = next_pos：跳到下一个不同的数', 24, T['muted'], bold=True)
    cands = S.get('candidates')
    nxt = S.get('next_pos')
    if not cands or nxt is None:
        return
    n = len(cands)
    cell = 96
    sx = x0 + (x1 - x0 - cell * (n + 1)) / 2
    top = y0 + 100
    in_dfs = 'now_pos' in S
    idx = S.get('index')
    for i, v in enumerate(cands):
        X = sx + i * cell
        fill = T['panel2']
        if in_dfs and i < S['now_pos']:
            fill = (40, 45, 53)
        if idx is not None and i == idx and idx < n:
            fill = T['pink'] if in_dfs else T['blue']
        cv.rect((X + 6, top, X + cell - 6, top + 70), fill=fill, r=10, outline=T['border'], width=1)
        tc = T['bg'] if (idx is not None and i == idx) else (T['dim'] if fill == (40, 45, 53) else T['text'])
        cv.text((X + cell / 2, top + 35), v, 34, tc, anchor='mm', bold=True)
        cv.text((X + cell / 2, top + 76), i, 18, T['dim'], anchor='mt', mono=True)
    # 末尾的 n 位置（越界哨兵）
    X = sx + n * cell
    cv.rect((X + 6, top, X + cell - 6, top + 70), outline=T['border'], width=1, r=10)
    cv.text((X + cell / 2, top + 35), '末尾', 22, T['dim'], anchor='mm')
    cv.text((X + cell / 2, top + 76), n, 18, T['dim'], anchor='mt', mono=True)
    # next_pos 弧线（只画跳过相同数的那些）
    for i, j in enumerate(nxt):
        if j > i + 1:
            p0 = (sx + i * cell + cell / 2, top - 4)
            p1 = (sx + j * cell + cell / 2, top - 4)
            hot = idx is not None and i == idx and in_dfs
            cv.arc_arrow(p0, p1, 26 + 10 * (j - i), T['yellow'] if hot else T['purple'], 4 if hot else 3, 12)
    # next_pos 数组本身
    ty = top + 140
    cv.text((x0 + 18, ty), 'next_pos[k]：下一个不等于 candidates[k] 的下标', 22, T['muted'], bold=True)
    for i, j in enumerate(nxt):
        X = sx + i * cell
        changed = B.get('next_pos') is not None and i < len(B['next_pos']) and B['next_pos'][i] != j
        hot = idx is not None and i == idx
        cv.rect((X + 12, ty + 34, X + cell - 12, ty + 84), fill=T['purple'] if j > i + 1 else T['panel2'], r=8,
                outline=T['yellow'] if (changed or hot) else T['border'], width=4 if (changed or hot) else 1)
        cv.text((X + cell / 2, ty + 59), j, 28, T['bg'] if j > i + 1 else T['text'], anchor='mm', bold=True)
    if idx is not None and idx <= n:
        X = sx + min(idx, n) * cell + cell / 2
        cv.tri_up(X, ty + 94, 10, T['pink'] if in_dfs else T['blue'])
        cv.text((X, ty + 110), 'index', 20, T['pink'] if in_dfs else T['blue'], anchor='mt', bold=True)
    if in_dfs and S['now_pos'] <= n:
        X = sx + S['now_pos'] * cell + cell / 2
        cv.tri_up(X, top + 100, 9, T['blue'])
        cv.text((X, top + 117), 'now_pos', 20, T['blue'], anchor='mt', bold=True)


def _pre_if(S, B, ret):
    i = S.index
    c = S.candidates
    if i + 1 == len(c):
        return f'==从后往前==算 next_pos：`index = {i}` 是最后一个，`next_pos[{i}] = {i + 1}`（末尾）'
    if c[i] == c[i + 1]:
        return f'`candidates[{i}] = candidates[{i + 1}] = {c[i]}`：相同 → 下一个不同的数和 `{i + 1}` 的一样'
    return f'`candidates[{i}] = {c[i]} ≠ {c[i + 1]}`：下一个不同的数就是 `{i + 1}`'


def _while_cap(S, B, ret):
    if S.index >= len(S.candidates):
        return f'`index = {S.index}` 到末尾了 → 这一层试完，回溯'
    return f'尝试 `index = {S.index}`（数字 `{S.candidates[S.index]}`）'


CONFIG = dict(
    num=40, title='组合总和 II', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯 · next_pos 跳过重复数字',
    tags=['热题173'],
    code='''
class Solution(object):
    def combinationSum2(self, candidates, target):
        next_pos = [i + 1 for i in range(len(candidates))]
        candidates = sorted(candidates)

        now = None
        for index in range(len(candidates) - 1, -1, -1):
            if index + 1 != len(candidates) and candidates[index] == candidates[index + 1]:
                next_pos[index] = next_pos[index + 1]

        res = []
        self.dfs(candidates, target, 0, next_pos, [], res)
        return res

    def dfs(self, candidates, target, now_pos, next_pos, now_choose, res):
        if target == 0:
            res.append([x for x in now_choose])
            return

        index = now_pos
        while index < len(candidates):
            if candidates[index] > target:
                break
            target -= candidates[index]
            now_choose.append(candidates[index])
            self.dfs(candidates, target, index + 1, next_pos, now_choose, res)
            now_choose.pop()
            target += candidates[index]
            index = next_pos[index]
''',
    call=f'Solution().combinationSum2({CANDS}, 5)',
    expect=[[1, 2, 2], [5]],
    skip=['now = None', 'res = []', 'for index in range(len(candidates) - 1'],
    views=[
        dict(type='custom', draw=_jump, h=372),
        dict(type='text', fn=lambda S: (f"`target` 还差 =={S['target']}==　`now_choose = {S['now_choose']}`　`res = {S['res']}`" if 'now_choose' in S else ''),
             h=46, size=25),
        dict(type='calls', h=212, hide=('candidates', 'next_pos', 'now_choose', 'res')),
    ],
    watch=[('now_pos', 'now_pos', 'blue'), ('index', 'index', 'pink'), ('target', 'target', 'yellow'), 'now_choose'],
    captions={
        'next_pos = [i + 1': '`next_pos[k]` 先设为 `k + 1`：默认下一个数就是后一位',
        'candidates = sorted': '排序 → `{candidates}`：==相同的数挨在一起==',
        'if index + 1 != len': _pre_if,
        'next_pos[index] = next_pos': '`next_pos[{index}] = next_pos[{index + 1}] = {next_pos[index]}`：直接跳过整段相同的数',
        'self.dfs(candidates, target, 0': '从位置 `0` 开始搜索，`target = {target}` 表示==还差多少==',
        'return res': '搜索结束，返回 `{ret}`',
        'if target == 0': lambda S, B, ret: (
            f'`target == 0`：正好凑够 → 得到一个解 `{S.now_choose}`' if S.target == 0 else
            f'`target = {S.target}`：还差 `{S.target}`，从 `now_pos = {S.now_pos}` 往后选'),
        'res.append': '复制一份加入 res：`{res[-1]}`',
        '            return': '记录完毕 → 回溯',
        'index = now_pos': '本层从 `now_pos = {now_pos}` 开始挑下一个数',
        'while index < len': _while_cap,
        'if candidates[index] > target': lambda S, B, ret: (
            f'`{S.candidates[S.index]} > target = {S.target}`：已排序，后面只会更大' if S.candidates[S.index] > S.target else
            f'`{S.candidates[S.index]} ≤ {S.target}`：可以加入'),
        'break': '这个数都放不下，后面更大的也不行 → ==break==，回溯',
        'target -= candidates[index]': '加入 `{candidates[index]}`：`target` → `{target}`',
        'now_choose.append': '`now_choose` → `{now_choose}`',
        'self.dfs(candidates, target, index + 1': '下一层从 ==index + 1 = {now_pos}== 开始：每个数只能用一次',
        'now_choose.pop()': '回溯：弹出 `{B.now_choose[-1]}`，`now_choose` → `{now_choose}`',
        'target += candidates[index]': '`target` 加回 `{candidates[index]}` → `{target}`',
        'index = next_pos[index]': lambda S, B, ret: (
            f'==跳==到 `next_pos[{B.index}] = {S.index}`：跳过所有和 `{S.candidates[B.index]}` 相同的数，避免重复组合'
            if S.index > B.index + 1 else f'`index` → `next_pos[{B.index}] = {S.index}`（后一个数本来就不同）'),
    },
    max_steps=58,
    cards=dict(
        one_liner='排序后预处理 next_pos，回溯时直接跳到下一个不同的数',
        complexity='指数级，剪枝后很快；预处理 `O(n log n)`，空间 `O(n)`',
        problem=['`candidates` 可能有==重复数字==，每个数字在每个组合中只能用==一次==',
                 '找出所有和为 `target` 的组合，==解集不能包含重复的组合==',
                 '示例：`[2,5,2,1,2], target = 5` → `[[1,2,2],[5]]`'],
        quote='计算出一个next_pos[k]，表示下一个不等于a[k]的数的下标是多少，然后在a[k]回溯时==直接继续尝试a[next_pos[k]]==而不是原来的a[k + 1]。',
        quote_src='—— yiduobo 题解',
        idea=['和 39 题一样往后选；但选完 `index` 后，下一层从 ==index + 1== 开始（只能用一次）',
              '同一层里，`[1,2(第1个)]` 和 `[1,2(第2个)]` 是同一个组合 → 同一层同一个数只试一次',
              '排序后==从后往前==预处理 `next_pos`，回溯时 `index = next_pos[index]` 一步跳过'],
        result='得到 `[1,2,2]` 和 `[5]` ✓：同一层的三个 2 只试了第一个',
        summary=['复杂度指数级，靠排序后 `break` 剪枝；`next_pos` 预处理 `O(n)`',
                 '去重：==同一层==跳过相同数；==不同层==可以选相同的数（`[1,2,2]` 合法）',
                 '`next_pos` 必须在==排序之后==、从后往前算',
                 '对比灵神：灵神「不选 x」时在递归里 while 跳过；yiduobo 提前算好跳转表',
                 '原文为 Python 2 风格，仅删去 docstring；`now = None` 是原文未用到的变量'],
    ),
)
