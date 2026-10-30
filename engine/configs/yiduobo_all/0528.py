W = [1, 3, 2]


def _draw(cv, S, B, box, T):
    """把权重画成一排小球：第 j 个小球的标记 = 它落在哪个前缀和区间"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '小球（编号 0..sum−1，球上写的是它的标记 = 返回的下标；黄框 = 随机到的 pos）', 22, T['muted'], bold=True)
    pre = S.get('self.sum_list') or []
    if not pre or len(pre) < len(W):
        # 前缀和还没算完：按已算出的部分画
        pass
    total = sum(W)
    marks = []
    for k, w in enumerate(W):
        marks += [k] * w
    cols = [T['blue'], T['pink'], T['green'], T['purple']]
    cell = min(110, (x1 - x0 - 60) / total)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * total) / 2
    cy = y0 + 128
    rad = cell * 0.36
    known = pre[-1] if pre else 0
    pos = S.get('pos')
    for j, m in enumerate(marks):
        X = sx + j * cell + cell / 2
        on = j < known
        c = cols[m % len(cols)] if on else T['panel2']
        cv.d.ellipse((X - rad, cy - rad, X + rad, cy + rad), fill=c, outline=T['border'])
        cv.text((X, cy), m if on else '?', 30, T['bg'] if on else T['dim'], anchor='mm', bold=True)
        cv.text((X, cy + rad + 8), j, 18, T['dim'], anchor='mt', mono=True)
        if pos is not None and j == pos:
            cv.rect((X - rad - 8, cy - rad - 8, X + rad + 8, cy + rad + 8), outline=T['yellow'], width=4, r=10)
            cv.text((X, cy - rad - 14), 'pos', 22, T['yellow'], anchor='mb', bold=True)
    # 区间分隔线：前缀和就是每种标记的右边界（开）
    for k, v in enumerate(pre):
        X = sx + v * cell
        cv.line([(X, cy - rad - 4), (X, cy + rad + 36)], T['orange'], 3)
        cv.text((X, cy + rad + 40), f'sum_list[{k}]={v}', 18, T['orange'], anchor='mt', bold=True)


def _cap_if(S, B, ret):
    p, m, v = S.pos, S.mid, S.self.sum_list[S.mid]
    if p >= v:
        return f'`pos = {p} >= sum_list[{m}] = {v}`：标记 0..{m} 的小球只有编号 `< {v}` 的 → pos 在 mid ==右边=='
    return f'`pos = {p} < sum_list[{m}] = {v}`：pos 落在标记 `<= {m}` 的小球里 → 答案可能就是 mid，==保留 mid=='


CONFIG = dict(
    num=528, title='按权重随机选择', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='前缀和 + 二分查找',
    tags=['labuladong', '灵神题单·数学算法'],
    code='''
class Solution(object):

    def __init__(self, w):
        self.sum_list = [w[0]]
        for index in range(1, len(w)):
            self.sum_list.append(self.sum_list[-1] + w[index])

    def pickIndex(self):
        pos = random.randint(0, self.sum_list[-1] - 1)
        l = 0
        r = len(self.sum_list) - 1
        while l < r:
            mid = (l + r) >> 1
            if pos >= self.sum_list[mid]:
                l = mid + 1
            else:
                r = mid
        return l
''',
    setup='import random\nrandom.seed(6)',
    call=f'''s = Solution({W})
[s.pickIndex(), s.pickIndex(), s.pickIndex()]''',
    expect=[2, 0, 1],
    views=[
        dict(type='text', size=24, h=70,
             fn=lambda S: f'`w = {W}`：看成 1 个标 0 的球、3 个标 1 的球、2 个标 2 的球，==等概率摸一个=='),
        dict(type='custom', draw=_draw, h=270),
        dict(type='array', var='self.sum_list', cell=110, h=230, label='sum_list（前缀和，单调递增 → 可以二分）',
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'},
             color=lambda S, i, v: 'green' if S.get('_line') == 18 and i == S.get('l') else None,
             dim=lambda S, i, v: 'l' in S and 'r' in S and not (S['l'] <= i <= S['r'])),
    ],
    watch=[('pos', 'pos', 'yellow'), ('l', 'l', 'blue'), ('mid', 'mid', 'cyan'), ('r', 'r', 'pink')],
    captions={
        'self.sum_list = [w[0]]': '前缀和从 `w[0] = {self.sum_list[0]}` 开始',
        'for index in range(1': lambda S, B, r: ('前缀和算完：`sum_list = {}`'.format(S.self.sum_list) if 'index' in B and B['index'] == S.index
                                                     else f'处理 `w[{S.index}] = {W[S.index]}`'),
        'self.sum_list.append': '`sum_list` 追加 `{self.sum_list[-2]} + {w[index]} = {self.sum_list[-1]}`：标记 {index} 的小球编号到 `{self.sum_list[-1]} − 1` 为止',
        'pos = random.randint': '从 `0..{self.sum_list[-1] - 1}` 里等概率选一个小球编号：`pos = {pos}`',
        'l = 0': '二分：找第一个 `sum_list[i] > pos` 的下标',
        'r = len(self.sum_list) - 1': '`r = {r}`：答案一定在 `[l, r]` 里',
        'while l < r': lambda S, B, r: ('区间里不止一个候选，继续二分' if S.l < S.r else f'`l = r = {S.l}`：只剩一个候选，就是答案'),
        'mid = (l + r) >> 1': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'if pos >= self.sum_list[mid]': _cap_if,
        'l = mid + 1': '`l = mid + 1 = {l}`',
        'r = mid': '`r = mid = {r}`',
        'return l': '编号 `{pos}` 的小球标记是 =={ret}== → 返回下标 {ret}',
    },
    cards=dict(
        one_liner='权重 = 小球个数；随机摸一个球，用前缀和 + 二分找出它的标记',
        complexity='初始化 `O(n)`；每次 `pickIndex` `O(log n)`；空间 `O(n)`',
        problem=['给正整数数组 `w`，`pickIndex()` 随机返回下标 `i`，选中概率为 `w[i] / sum(w)`',
                 '示例：`w = [1,3]` → 返回 0 的概率 25%，返回 1 的概率 75%',
                 '本视频：`w = [1,3,2]`，固定随机种子，连续调用 3 次'],
        quote='对于w中的权重，我们可以==看成有数字标记的小球==。例如样例中的W=[1,3]，可以看成一个标记了数字0的小球，以及3个标记了数字1的小球。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 `0..sum−1` 里随机一个编号 `pos`，再找它对应哪种标记',
              '小球按顺序编号，前缀和 `sum_list[k]` 就是标记 `k` 的==右边界（开）==',
              '前缀和单调递增 → 二分找第一个 `sum_list[i] > pos`'],
        summary=['初始化 `O(n)`，每次选取 `O(log n)`',
                 '易错：比较用 `pos >= sum_list[mid]`（等于时 pos 属于下一种标记），随机范围是 `0..sum−1`',
                 '等价写法：`bisect_right(sum_list, pos)`',
                 '原文为 Python 2 写法，代码可直接在 Python 3 运行；演示中补上 `import random` 并固定随机种子'],
    ),
)
