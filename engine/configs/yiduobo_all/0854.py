_NAMES = [x + y for x in 'abcdef' for y in 'abcdef' if x != y]
_A, _B = 'abc', 'bca'


def _edges(S):
    cur = S.get('now')
    if cur is None:
        cur = S.get('edge_list')
    if cur is None:
        return None
    return {_NAMES[i]: c for i, c in enumerate(cur) if c > 0}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    A, Bs = S.get('A', _A), S.get('B', _B)
    cv.text((x0 + 18, y0 + 4), 'A 要变成 B：每个不同位置产生一条「字符交换」边 A[i]→B[i]', 22, T['muted'], bold=True)
    cell = 80
    sx = x0 + 120
    for r, (lab, s) in enumerate((('A', A), ('B', Bs))):
        y = y0 + 50 + r * (cell + 14)
        cv.text((sx - 20, y + cell / 2), lab, 34, T['muted'], anchor='rm', bold=True)
        for i, ch in enumerate(s):
            diff = A[i] != Bs[i]
            X = sx + i * (cell + 10)
            cv.rect((X, y, X + cell, y + cell), fill=T['pink'] if diff else T['green'], r=10)
            cv.text((X + cell / 2, y + cell / 2), ch, 40, T['bg'], anchor='mm', bold=True, mono=True)
    y = y0 + 50 + 2 * (cell + 14) + 22
    ed = _edges(S)
    if ed is None:
        cv.text((x0 + 18, y), '先预处理所有「环」，再对边的计数做记忆化搜索', 24, T['text'], bold=True)
        return
    cv.text((x0 + 18, y), '剩余的字符交换（边 × 个数）', 24, T['blue'], bold=True)
    x = x0 + 30
    if not ed:
        cv.text((x, y + 44), '（空）全部用完', 26, T['green'], bold=True)
    for k, c in ed.items():
        cv.rect((x, y + 40, x + 130, y + 96), fill=T['panel2'], outline=T['blue'], width=3, r=12)
        cv.text((x + 65, y + 68), f'{k[0]}→{k[1]} ×{c}', 28, T['text'], anchor='mm', bold=True, mono=True)
        x += 150
    y += 120
    if 'circle' in S and 'flag' in S:
        cv.text((x0 + 18, y), f"尝试取走环 `{S['circle']}`：" .replace('`', '') + ('可以（每条边都够）' if S['flag'] else '不行（缺边）'), 24, T['yellow'] if S['flag'] else T['dim'], bold=True)


CONFIG = dict(
    num=854, title='相似度为K的字符串', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='拆环 + 记忆化搜索',
    tags=['灵神题单', '图论算法'],
    code='''
class Solution(object):
    def kSimilarity(self, A, B):

        edge_dict = {}
        cnt = 0
        for x in ['a', 'b', 'c', 'd', 'e', 'f']:
            for y in ['a', 'b', 'c', 'd', 'e', 'f']:
                if x != y:
                    key = x + y
                    edge_dict[key] = cnt
                    cnt += 1

        q = ['a', 'b', 'c', 'd', 'e', 'f']
        l = 0
        r = 6
        circle_dict = {}
        length = 1
        while length < 6:
            length += 1
            for now in q[l:r]:
                for char in ['a', 'b', 'c', 'd', 'e', 'f']:
                    if now.find(char) == -1:
                        tmp = now + char
                        min_pos = 0
                        for index in range(1, len(tmp)):
                            if tmp[index] < tmp[min_pos]:
                                min_pos = index
                        tmp = tmp[min_pos:] + tmp[:min_pos]
                        if tmp not in circle_dict:
                            circle_dict[tmp] = [edge_dict[tmp[index] + tmp[(index + 1) % length]] for index in range(length)]
                            q.append(tmp)
            
            l, r = r, len(q)

        f = {}
        edge_list = [0] * len(edge_dict)
        f[tuple(edge_list)] = 0
        for index in range(len(A)):
            if A[index] != B[index]:
                key = A[index] + B[index]
                edge_list[edge_dict[key]] += 1

        return sum(edge_list) - self.dfs(tuple(edge_list), circle_dict, f)
    
    def dfs(self, now, circle_dict, f):
        if now not in f:
            f[now] = -1
            for circle in circle_dict:
                tmp = list(now)
                flag = True
                for edge in circle_dict[circle]:
                    if tmp[edge] > 0:
                        tmp[edge] -= 1
                    else:
                        flag = False
                        break
                if flag:
                    f[now] = max(f[now], 1 + self.dfs(tuple(tmp), circle_dict, f))
        
        return f[now]
''',
    call="Solution().kSimilarity('abc', 'bca')",
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='calls', h=130, hide=('circle_dict', 'f')),
    ],
    watch=[('len(circle_dict)', 'len(circle_dict)', 'cyan'), 'length', ('f 记忆数', 'len(f)', 'green')],
    skip=['edge_dict[key] = cnt', 'cnt += 1', 'cnt = 0', 'key = x + y', 'for x in', 'for y in', 'if x != y',
          'l = 0', 'r = 6', 'length = 1', 'length += 1', 'for now in q[l:r]', 'for char in', 'if now.find', 'tmp = now + char',
          'min_pos', 'for index in range(1, len(tmp))', 'if tmp[index] <', 'tmp = tmp[min_pos', 'if tmp not in circle_dict', 'q.append(tmp)',
          'l, r = r, len(q)', 'for circle in circle_dict', 'tmp = list(now)', 'flag = True', 'for edge in', 'if tmp[edge] > 0', 'tmp[edge] -= 1', 'flag = False', 'break', 'q = [', 'if flag', 'circle_dict[tmp] =', 'edge_dict = {}', 'circle_dict = {}'],
    max_steps=60, max_events=400000,
    captions={
        'while length < 6': lambda S, B, r: (f'枚举环长 2~6（现在已有 {len(S.circle_dict)} 种环）：把环写成「最小字符打头」去重，如 `bac` 与 `acb` 是同一个环' if S.length < 6 else f'所有环枚举完：共 =={len(S.circle_dict)}== 种，存进 `circle_dict`'),
        'circle_dict[tmp] =': '环 `{tmp}` 含的字符交换边：{[tmp[k] + tmp[(k + 1) % length] for k in range(length)]}',
        'f = {}': '`f[边的计数]` = 最多还能拆出几个环；备忘录 `f` 开始',
        'edge_list = [0]': '30 个位置：每种「字符交换」a→b 剩几条',
        'f[tuple(edge_list)] = 0': '边全用完时能再拆 0 个环（边界）',
        'for index in range(len(A))': '扫 A、B：`A[{index}]`=`{A[index]}`，`B[{index}]`=`{B[index]}`',
        'if A[index] != B[index]': lambda S, B, r: (f'`{S.A[S.index]}` ≠ `{S.B[S.index]}` → 这个位置需要交换，产生一条边' if S.A[S.index] != S.B[S.index] else '这一位已经匹配，无需交换'),
        'edge_list[edge_dict[key]] += 1': '边 `{key[0]}→{key[1]}` 计数 +1',
        'return sum(edge_list)': '答案 = 总边数 `m` − 最多环数 `n`（每个 k 字符的环要 k−1 次交换）',
        'if now not in f': lambda S, B, r: ('这个边计数没算过 → 搜索' if S.now not in S.f else '算过了 → 直接用备忘录'),
        'f[now] = -1': '先设为 -1：表示「一个环也拆不了」',
        'if flag': lambda S, B, r: (f'环 `{S.circle}` 的每条边都够 → 可以拆掉它，递归到剩下的边' if S.flag else '缺边，这个环不能拆'),
        'f[now] = max': '`f[now]` = max(旧值, 1 + 拆掉该环后剩余的最多环数) = =={f[now]}==',
        'return f[now]': '从这个状态最多能拆出 =={f[now]}== 个环',
    },
    cards=dict(
        one_liner='把交换拆成若干环：k 个字母的环只要 k−1 次，环越多越好',
        complexity='时间 `O(环种类 × 状态数)`，空间 `O(状态数)`',
        problem=['`A` 与 `B` 是由 a~f 组成的字母异位词',
                 '每次可交换 `A` 中两个字符，求使 `A` 等于 `B` 的==最少交换次数==',
                 '示例：`A="abc"`，`B="bca"` → `2`；本视频：`abc` → `bca`'],
        quote='对于一个参与字母数量为k的交换序列，需要花费k - 1次操作进行交换。',
        quote_src='—— yiduobo 题解原文',
        idea=['`A[i] != B[i]` 就产生一条边 `A[i]→B[i]`，ans = 边数 m − 环数 n',
              '字符只有 a~f，先枚举所有长度 2~6 的环并去重（最小字符打头）',
              '对「每种边剩几条」做记忆化搜索，取最多能拆出的环数'],
        summary=['最少交换 = 不匹配位数 − 最多能拆出的环数',
                 '环用「最小字符轮转到最前」去重，否则同一个环会重复计数',
                 '直接用 tuple 当 dict 键，没有显式状态压缩',
                 '本题示例边：`a→b、b→c、c→a` 恰好一个 3 环，所以 3 − 1 = 2',
                 '原文已是 Python 3 可运行写法，逐字照搬'],
    ),
)
