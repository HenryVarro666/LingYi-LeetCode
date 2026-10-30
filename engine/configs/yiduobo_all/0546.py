B0 = [1, 2, 2, 1, 2]


def _in(S):
    return S.get('_inner', {})


def _lr(S):
    I = _in(S)
    if 'l' in I and 'r' in I and 'k' in I:
        return I['l'], I['r'], I['k']
    return None


def _wl(S):
    t = _lr(S)
    return None if t is None else t[0]


def _wr(S):
    t = _lr(S)
    return None if t is None else t[1]


def _color(S, i, v):
    t = _lr(S)
    if t is None:
        return None
    l, r, k = t
    I = _in(S)
    if i == l:
        return 'yellow'
    nsp = I.get('next_same_pos')
    if I.get('_line', S.get('_line')) and nsp is not None and i == nsp and S.get('_line', 0) >= 33 and nsp <= r:
        return 'green'
    return None


def _memo(S):
    f = S.get('f')
    if f is None:
        I = _in(S)
        f = I.get('f')
    if f is None:
        return {}
    n = len(f)
    return {f'({l},{r},{k})': f[l][r][k] for l in range(n) for r in range(n) for k in range(n) if f[l][r][k] > 0}


def _txt(S):
    t = _lr(S)
    if t is None:
        return '`f[l][r][k]`：处理 `boxes[l..r]`，且前面已经累积了 `k` 个和 `boxes[l]` 相同的盒子，最多得多少分'
    l, r, k = t
    b = S['boxes']
    return f'`dfs({l}, {r}, {k})`：区间 `{b[l:r + 1]}`，`boxes[{l}]` 前带 ==`{k}`== 个同色'


def _cap_memo(S, B, ret):
    I = _in(S)
    l, r, k = I['l'], I['r'], I['k']
    v = I['f'][l][r][k]
    return f'`f[{l}][{r}][{k}] = {v}` 已算过 → ==直接返回==' if v > 0 else f'`f[{l}][{r}][{k}]` 还没算，往下算'


CONFIG = dict(
    num=546, title='移除盒子', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 三维状态 f[l][r][k]（前面带 k 个同色）',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def removeBoxes(self, boxes):

        n = len(boxes)
        
        f = [[[0] * n for _ in range(n)] for _ in range(n)]
        now = boxes[0]
        k = 0
        for index in range(1, len(boxes)):
            if boxes[index] != now:
                break
            k += 1
        
        if k == len(boxes) - 1:
            return len(boxes) ** 2

        return self.dfs(k, len(boxes) - 1, k, boxes, f)
    
    def dfs(self, l, r, k, boxes, f):
        if f[l][r][k] > 0:
            return f[l][r][k]
        if l == r:
            return (k + 1) ** 2
        
        next_k = 0
        for index in range(l + 2, r + 1):
            if boxes[index] != boxes[l + 1]:
                break
            next_k += 1
        
        if r - next_k - 1 == l:
            f[l][r][k] = (k + 1) ** 2 + (next_k + 1) ** 2
            return f[l][r][k]

        next_l = index - 1
        f[l][r][k] = (k + 1) ** 2 + self.dfs(next_l, r, next_k, boxes, f)

        next_same_pos = next_l + 1
        while True:
            while next_same_pos <= r and boxes[next_same_pos] != boxes[l]:
                next_same_pos += 1
            if next_same_pos > r:
                return f[l][r][k]
            
            part_ret = self.dfs(next_l, next_same_pos - 1, next_k, boxes, f)
            new_k = k + 1
            for index in range(next_same_pos + 1, r + 1):
                if boxes[index] != boxes[l]:
                    break
                next_same_pos = index
                new_k += 1
            
            if next_same_pos == r:
                f[l][r][k] = max(f[l][r][k], part_ret + (new_k + 1) ** 2)
                return f[l][r][k]
            
            f[l][r][k] = max(f[l][r][k], part_ret + self.dfs(next_same_pos, r, new_k, boxes, f))
            next_same_pos += 1

        return f[l][r][k]
''',
    call=f'Solution().removeBoxes({B0})',
    expect=11,
    max_steps=70,
    skip=['n = len(boxes)', 'f = [[[0]', 'now = boxes[0]', 'k = 0', 'for index in range', 'if boxes[index] !=',
          'break', 'next_k += 1', 'next_same_pos = index', 'new_k += 1', 'new_k = k + 1', 'next_k = 0'],
    views=[
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='array', var='boxes', label='boxes（框 = [l, r]，黄 = boxes[l]，绿 = 要合并的同色盒子）', cell=80, h=170,
             window=(_wl, _wr), color=_color),
        dict(type='map', var=_memo, label='备忘录 f[l][r][k]（只列出已算出的）', fmt=lambda k, v: f'{k}: {v}', h=130, font=28),
        dict(type='calls', h=300, hide=('boxes', 'f')),
    ],
    watch=[('l', lambda S: _in(S).get('l'), 'yellow'), ('r', lambda S: _in(S).get('r'), 'pink'),
           ('k', lambda S: _in(S).get('k'), 'cyan'), ('next_l', lambda S: _in(S).get('next_l'), 'blue'),
           ('new_k', lambda S: _in(S).get('new_k'), 'green')],
    captions={
        'if k == len(boxes) - 1': lambda S, B, r: (f'开头连续 `{S.k + 1}` 个相同；全部相同就直接 `n^2`' if S.k == len(S.boxes) - 1
                                                   else f'开头连续 `{S.k + 1}` 个 `{S.boxes[0]}`：先当成 `k = {S.k}` 个累积的盒子，不是全相同'),
        'return self.dfs(k, len': '从 `dfs(l = {k}, r = {len(boxes) - 1}, k = {k})` 开始：`boxes[l]` 是开头那一段的最后一个',
        'if f[l][r][k] > 0': _cap_memo,
        'if l == r': lambda S, B, r: (f'`l == r`：只剩一个，连同前面 `{S.k}` 个共 `{S.k + 1}` 个一起消 → ==`({S.k}+1)^2 = {(S.k + 1) ** 2}`=='
                                      if S.l == S.r else '区间里不止一个盒子'),
        'if r - next_k - 1 == l': lambda S, B, r: (f'`boxes[l+1..]` 连续 `{S.next_k + 1}` 个同色，刚好占满 `[l+1, r]` → 只有两段，直接算 `(k+1)^2 + (next_k+1)^2`'
                                                   if S.r - S.next_k - 1 == S.l else
                                                   f'`boxes[l+1]` 开始连续 `{S.next_k + 1}` 个同色（`next_k = {S.next_k}`），后面还有别的'),
        'f[l][r][k] = (k + 1) ** 2 + (next_k': '`f[{l}][{r}][{k}] = {(k + 1) ** 2} + {(next_k + 1) ** 2}` = =={f[l][r][k]}==，返回',
        'next_l = index - 1': '`next_l = {next_l}`：`boxes[l+1]` 这一连串的最后一个位置',
        'f[l][r][k] = (k + 1) ** 2 + self.dfs': lambda S, B, r: (f'情况 1：把累积的 `{B.k + 1}` 个 `boxes[{B.l}]` ==直接消掉==，得 `{(B.k + 1) ** 2}`，'
                                                                  f'再处理 `[{B.next_l}..{B.r}]`（带 `next_k = {B.next_k}` 个）'),
        'while True': '循环：逐个找后面和 `boxes[l]` 同色的盒子',
        'next_same_pos = next_l + 1': '情况 2：往后找和 `boxes[l]` 同色的盒子，看要不要==先消中间、再合并==',
        'while next_same_pos <= r': lambda S, B, r: (f'`boxes[{S.next_same_pos}] = {S.boxes[S.next_same_pos]}` ≠ `boxes[{S.l}] = {S.boxes[S.l]}`，往后找'
                                                     if S.next_same_pos <= S.r and S.boxes[S.next_same_pos] != S.boxes[S.l]
                                                     else '找到了同色（或越界）'),
        'if next_same_pos > r': lambda S, B, r: ('后面再没有同色盒子 → 所有合并方式都试完，返回' if S.next_same_pos > S.r
                                                 else f'在位置 `{S.next_same_pos}` 找到同色盒子'),
        'part_ret = self.dfs': lambda S, B, r: f'先把中间 `[{B.next_l}..{B.next_same_pos - 1}]` 消掉，带 `next_k = {B.next_k}` 个，得 `part_ret`',
        'if next_same_pos == r': lambda S, B, r: (f'同色盒子一路连到 `r`：新累积 `new_k + 1 = {S.new_k + 1}` 个一起消'
                                                  if S.next_same_pos == S.r else f'合并后 `{S.new_k}` 个同色盒子（含前面累积的），后面还有 `[{S.next_same_pos}..{S.r}]`'),
        'f[l][r][k] = max(f[l][r][k], part_ret + (new_k': '`f[{l}][{r}][{k}] = max(.., {part_ret} + {(new_k + 1) ** 2})` = =={f[l][r][k]}==，返回',
        'f[l][r][k] = max(f[l][r][k], part_ret + self.dfs': lambda S, B, r: (f'合并：`part_ret = {B.part_ret}` + 继续处理 `[{B.next_same_pos}..{B.r}]`'
                                                                             f'（累积 `new_k = {B.new_k}`）'),
        'next_same_pos += 1': '`next_same_pos` → {next_same_pos}：继续找下一个同色盒子',
        'return f[l][r][k]': '`f[{l}][{r}][{k}]` = =={ret}==',
    },
    cards=dict(
        one_liner='区间 DP 不够，要多记一维：前面带了几个同色盒子',
        complexity='时间 `O(n^4)`，空间 `O(n^3)`',
        problem=['一排盒子，每次选连续同色的 `k` 个盒子消掉，得 `k × k` 分',
                 '求消完所有盒子能得到的==最大分数==',
                 '示例：`[1,3,2,2,2,3,4,3,1]` → `23`；本视频：`[1,2,2,1,2]` → `11`'],
        quote='对于最中间的1，我们在一开始是无法得知其是否应该消除的。因此f[l][r]这种形式的状态是不行的……使用状态f[l][r][k]表示现在处理l到r这一段，且前面已经积累了k个连续的boxes[l]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[l][r][k]`：处理 `l..r`，前面已累积 `k` 个和 `boxes[l]` 同色的盒子',
              '要么把累积的 `k+1` 个直接消掉；要么枚举后面同色的位置，==先消中间、再把它们合并==',
              '连续相同的盒子要一次处理掉，不拆开，所以用 `next_k` / `next_l` 跳过整段'],
        summary=['状态 `O(n^3)`，每次转移扫一遍 → 时间 `O(n^4)`，空间 `O(n^3)`',
                 '易错：连续同色必须一次消，所以状态里先把整段合并（`next_k`、`new_k`）',
                 '`f` 初值 0 兼作“没算过”：得分一定为正，所以可以用 `> 0` 判断备忘',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；本题无整数除法',
                 '这份代码把“连续段”显式处理，细节多；常见写法见官方题解的 `dfs(l, r, k)`'],
    ),
)
