def _cells(cv, T, x0, y, items, cell, hi=(), col=None):
    n = len(items)
    sx = x0 - n * cell / 2
    for k, ch in enumerate(items):
        X = sx + k * cell
        fill = T['blue'] if k in hi else T['panel2']
        tc = T['bg'] if k in hi else T['text']
        if col and k in col:
            fill, tc = col[k], T['bg']
        cv.rect((X + 4, y, X + cell - 4, y + cell), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, y + cell / 2), ch, 36, tc, anchor='mm', bold=True, mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    bottom, now, pos = S['bottom'], list(S['now']), S['pos']
    n = len(bottom)
    cell = min(84, (x1 - x0 - 80) / max(n, 1))
    cv.text((x0 + 18, y0 + 4), '这一层 bottom（蓝 = 正在看的两块）和正在拼的下一层 now（黄）', 22, T['muted'], bold=True)
    ytop = y0 + 60
    cv.text((x0 + 18, ytop + cell + 4), '', 20, T['dim'])
    # now 行（上）
    if n > 1:
        sx = cx - (n - 1) * cell / 2
        for k in range(n - 1):
            X = sx + k * cell
            ch = now[k] if k < len(now) else ''
            fill = T['yellow'] if ch else T['panel2']
            cv.rect((X + 4, ytop, X + cell - 4, ytop + cell), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, ytop + cell / 2), ch or '·', 36, T['bg'] if ch else T['dim'], anchor='mm', bold=True, mono=True)
    else:
        cv.text((cx, ytop + cell / 2), '只剩一块了：塔尖到手', 30, T['green'], anchor='mm', bold=True)
    yb = ytop + cell + 20
    hi = (pos, pos + 1) if pos < n - 1 else ()
    _cells(cv, T, cx, yb, list(bottom), cell, hi)
    if S['_inner'].get('a') is not None and pos < n - 1:
        a, b = S['a'], S['b']
        d = S['allowed_dict']
        cands = ''.join(d.get(a, {}).get(b, [])) or '（没有）'
        cv.text((x0 + 18, y1 - 40), f'{a}{b} 上面可放：{cands}', 28, T['yellow'], bold=True)


def _ch1(S, B, ret):
    if S.pos == 0:
        return f'`pos = 0`：第一块没有左邻，不用查左邻'
    if S.char not in S.allowed_dict[S.now[-1]]:
        return f'`char = {S.char}` 要紧挨左邻 `{S.now[-1]}`，但 `{S.now[-1]}{S.char}` 不是任何三角形的前两位 → ==剪枝 continue=='
    return f'左邻 `{S.now[-1]}` 和 `{S.char}` 能当某三角形的前两位 → 通过'


def _ch2(S, B, ret):
    if S.pos >= S.n - 2:
        return '这是下一层的最后一块，后面没有右邻 → 不用查首位'
    if S.char not in S.allowed_dict:
        return f'`{S.char}` 不是任何三角形的首位，后面接不上右邻 → ==剪枝 continue=='
    return f'`{S.char}` 能当某个三角形的首位，后面还有路 → 通过'


CONFIG = dict(
    num=756, title='金字塔转换矩阵', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='逐层 DFS + 字符串哈希去重 + 两个剪枝',
    tags=['动态规划', '链表树与回溯', '难度分 1990'],
    code='''
class Solution(object):
    def pyramidTransition(self, bottom, allowed):

        allowed_dict = {}
        for pyr in allowed:
            a = pyr[0]
            b = pyr[1]
            c = pyr[2]
            if a not in allowed_dict:
                allowed_dict[a] = {}
            if b not in allowed_dict[a]:
                allowed_dict[a][b] = []
            allowed_dict[a][b].append(c)

        checked_set = set()
        return self.dfs(0, bottom, allowed_dict, [], checked_set)

    def dfs(self, pos, bottom, allowed_dict, now, checked_set):
        n = len(bottom)
        if n == 1:
            return True

        if pos == n - 1:
            new_bottom = ''.join(now)
            if new_bottom not in checked_set:
                if self.dfs(0, new_bottom, allowed_dict, [], checked_set):
                    return True
                checked_set.add(new_bottom)
            return False

        a = bottom[pos]
        b = bottom[pos + 1]
        if a not in allowed_dict or b not in allowed_dict[a]:
            return False
        
        for char in allowed_dict[a][b]:
            if pos > 0 and char not in allowed_dict[now[-1]]:
                continue
            if pos < n - 2 and char not in allowed_dict:
                continue

            now.append(char)
            if self.dfs(pos + 1, bottom, allowed_dict, now, checked_set):
                return True
            now.pop()
        
        return False
''',
    call='Solution().pyramidTransition("BCD", ["BCB", "BCC", "CDE", "CEA"])',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='set', var='checked_set', label='checked_set（试过但失败的一层）', h=90),
        dict(type='calls', h=170, hide=('pyramidTransition', 'dfs')),
    ],
    watch=[('pos', 'pos', 'blue'), ('now', lambda S: ''.join(S['now']), 'yellow')],
    skip=['allowed_dict = {}', 'a = pyr[0]', 'b = pyr[1]', 'c = pyr[2]', 'checked_set = set()', 'n = len(bottom)', 'for pyr in allowed', 'for char in allowed_dict'],
    captions={
        'if a not in allowed_dict:': '`{pyr[0]}` 还没当过左下角 → 建一个空字典',
        'if b not in allowed_dict[a]:': '`{pyr[0]}{pyr[1]}` 第一次出现 → 建空列表',
        'allowed_dict[a][b].append(c)': '记下：`{a}{b}` 上面可以放 `{c}`',
        'return self.dfs(0, bottom': '从底层最左边（`pos = 0`）开始，逐层往上拼',
        'if n == 1': lambda S, B, r: ('只剩 1 块 → 塔尖到手，==True==' if S.n == 1 else f'这一层有 `{S.n}` 块，还没到塔尖'),
        'if pos == n - 1': lambda S, B, r: (f'`pos = {S.pos} = n - 1`：这一层的相邻对都扫完了，`now` = `{"".join(S.now)}` 就是下一层'
                                            if S.pos == S.n - 1 else f'`pos = {S.pos}`：还没扫完这一层'),
        'new_bottom = ': lambda S, B, r: f'把 `now` 拼成下一层字符串 `{S.new_bottom}`',
        'if new_bottom not in checked_set': lambda S, B, r: (f'`{S.new_bottom}` 没试过 → 递归往上' if S.new_bottom not in S.checked_set
                                                          else f'`{S.new_bottom}` 试过且失败 → 不再重复'),
        'if self.dfs(0, new_bottom': lambda S, B, r: f'以 `{B.new_bottom}` 为新的底层，递归 `dfs(0, ...)`',
        'checked_set.add': lambda S, B, r: f'上面没成功：把 `{B.new_bottom}` 记进 `checked_set`',
        'a = bottom[pos]': '左下块 `a = {a}`',
        'b = bottom[pos + 1]': '右下块 `b = {b}`',
        'if a not in allowed_dict or b': lambda S, B, r: ('`{}{}` 不是任何三角形的前两位 → 这一层拼不下去，False'.format(S.a, S.b)
                                                         if (S.a not in S.allowed_dict or S.b not in S.allowed_dict[S.a])
                                                         else f'`{S.a}{S.b}` 是合法的底边，顶上有候选 → 继续'),
        'if pos > 0 and char not': _ch1,
        'if pos < n - 2 and char not': _ch2,
        'now.append(char)': lambda S, B, r: f'顶上放 `{B.char}`：`now` = `{"".join(S.now)}`',
        'if self.dfs(pos + 1': lambda S, B, r: f'去看下一对：`dfs({B.pos + 1}, ...)`',
        'now.pop()': lambda S, B, r: f'后面走不通 → 撤销 `{B.now[-1]}`，换下一个候选',
        'return True': '一路成功 → ==True==',
        'return False': '这里没有可用的候选 → 回溯，False',
    },
    max_steps=80,
    cards=dict(
        one_liner='一层一层往上拼：枚举下一层所有可能，再递归',
        complexity='时间 约 `O(6^n)`（有去重），空间 `O(6^n)`',
        problem=['底层 `bottom`，三角形图案 “左下 右下 顶” 必须在 `allowed` 中',
                 '问能否一直拼到塔尖',
                 '本视频：`BCD`，`allowed=[BCB,BCC,CDE,CEA]` → `True`'],
        quote='从当前层的最左侧开始往右遍历，枚举所有可能形成的下一层的结果，然后递归求解下一层。',
        quote_src='—— yiduobo 题解原文',
        idea=['`allowed_dict[a][b]` 存 a、b 上面可以放的字符',
              '`dfs(pos, bottom, ..., now)`：从左到右拼下一层 `now`，拼满就递归',
              '两个小优化：新字符要能当某个三角形的首位；还要能和左邻接上',
              '原文用字符串做 key 记下失败的层，偷懒但够快'],
        result='拼到塔尖，返回 True ✓',
        summary=['时间约 `O(6^n)`，空间同量级（原文说最多 8^6 种状态）',
                 '`checked_set` 只记失败的层：成功了直接返回',
                 '回溯要 `now.pop()` 撤销，否则下一个候选会拼在旧字符后面',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神把行压成位运算，yiduobo 用字符串 + 嵌套字典'],
    ),
)
