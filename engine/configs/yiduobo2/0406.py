PEOPLE = [[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]
INS_LINES = (7, 9, 11)   # 三种插入写法所在的行


def _cur_idx(S):
    sp = S.get('sorted_people')
    if sp is None or 'height' not in S:
        return None
    try:
        return sp.index([S['height'], S['pos']])
    except ValueError:
        return None


def _draw_res(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'res（柱高 = 身高 h，柱下 = k；绿 = 刚插入的人，橙 = 他前面 ≥ 他的人）', 22, T['muted'], bold=True)
    res = S.get('res')
    if res is None:
        cv.text((x0 + 18, y0 + 44), '（尚未创建）', 24, T['dim'])
        return
    n = max(len(res), 1)
    cell = min(120, (x1 - x0 - 40) / max(n, 6))
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    base, top = y1 - 70, y0 + 70
    scale = (base - top) / 8
    new = None
    if S.get('_line') in INS_LINES:
        new = [S['height'], S['pos']]
    ni = res.index(new) if new in res else None
    for i, (h, k) in enumerate(res):
        X = sx + i * cell
        bw = cell * 0.62
        fill = (110, 120, 132)
        if ni is not None:
            if i == ni:
                fill = T['green']
            elif i < ni and h >= new[0]:
                fill = T['orange']
        cv.rect((X + (cell - bw) / 2, base - h * scale, X + (cell + bw) / 2, base), fill=fill, r=5)
        cv.text((X + cell / 2, base - h * scale - 6), h, 26, T['text'], anchor='mb', bold=True)
        cv.text((X + cell / 2, base + 8), f'k={k}', 22, T['muted'], anchor='mt', bold=True)
        cv.text((X + cell / 2, base + 38), i, 18, T['dim'], anchor='mt', mono=True)
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)


def _formula(S):
    if 'height' not in S:
        return '先按身高==降序==、k ==升序==排好，再逐个插入'
    h, k = S['height'], S['pos']
    ln = S.get('_line')
    if ln in INS_LINES:
        return f'`[{h},{k}]` 插在下标 `{k}`：前面恰好 `{k}` 个人，且都 ==≥ {h}=='
    return f'当前 `[{h},{k}]`：已放好的人都 ≥ {h}，他只需插到下标 `{k}`'


def _if0(S, B, ret):
    if S.pos == 0:
        return f'`k = 0`：前面不能有更高的人 → 插到==最前面=='
    return f'`k = {S.pos}` ≠ 0'


def _elif(S, B, ret):
    if S.pos == len(S.res):
        return f'`k = {S.pos}` 等于当前人数 `{len(S.res)}` → 直接排到==队尾=='
    return f'`k = {S.pos}` < 当前人数 `{len(S.res)}` → 插到中间下标 `{S.pos}`'


def _for(S, B, ret):
    if 'height' not in B or (B.get('height'), B.get('pos')) != (S.height, S.pos):
        return f'下一个：`[{S.height},{S.pos}]`（身高 {S.height}，前面要有 {S.pos} 个 ≥ 他的人）'
    return '所有人都插入完毕'


CONFIG = dict(
    num=406, title='根据身高重建队列', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='高个先排 · 按 k 插入',
    tags=['热题173'],
    code='''
class Solution(object):
    def reconstructQueue(self, people):
        sorted_people = sorted(people, key=lambda d:(-d[0], d[1]))
        res = []
        for height, pos in sorted_people:
            if pos == 0:
                res = [[height, pos]] + res
            elif pos == len(res):
                res.append([height, pos])
            else:
                res = res[:pos] + [[height, pos]] + res[pos:]

        return res
''',
    call=f'Solution().reconstructQueue({PEOPLE})',
    expect=[[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]],
    views=[
        dict(type='text', fn=_formula),
        dict(type='array', var=lambda S: [f'{h},{k}' for h, k in S['sorted_people']] if 'sorted_people' in S else None,
             label='sorted_people（h 降序、k 升序；绿 = 已插入）', cell=110, h=210,
             pointers={'sorted_people.index([height, pos])': 'blue'},
             pointer_labels={'sorted_people.index([height, pos])': '当前'},
             color=lambda S, i, v: 'green' if _cur_idx(S) is not None and (i < _cur_idx(S) or (i == _cur_idx(S) and S.get('_line') in INS_LINES)) else None),
        dict(type='custom', draw=_draw_res, h=360),
    ],
    watch=[('height', 'height', 'blue'), ('pos', 'pos', 'pink'), ('len(res)', lambda S: len(S['res']) if 'res' in S else None)],
    captions={
        'sorted_people = sorted': '矮的人不影响高的人的排位 → 按 ==h 降序==、==k 升序== 排序',
        'res = []': '`res` 是重建中的队列，高个子先入场',
        'for height, pos in': _for,
        'if pos == 0': _if0,
        'res = [[height, pos]] + res': '`[{height},{pos}]` 插到队首；后面的人都 ≥ 他，==他们的 k 不受影响==',
        'elif pos == len(res)': _elif,
        'res.append': '`[{height},{pos}]` 排到队尾：前面 {pos} 人都 ≥ {height}',
        'res = res[:pos]': '`[{height},{pos}]` 插到下标 `{pos}`：前面 {pos} 人都 ≥ {height}；他比后面的人矮，不改变他们的 k',
        'return res': '返回重建好的队列',
    },
    cards=dict(
        one_liner='高个子先排；矮个子插在第 k 位，不影响任何高个子',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`people[i] = [h, k]`：身高 `h`，前面恰好有 `k` 个身高 ==≥ h== 的人',
                 '把打乱的 `people` 重建成满足所有 `k` 的队列',
                 '示例：`[[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]`',
                 '→ `[[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]`'],
        quote='对于每个人来说，身高比这个人矮的人是不会影响到这个人的排位的，因此可以先按h降序，按k升序进行排序。排好序之后按身高逐个插入。',
        quote_src='—— yiduobo 知乎题解',
        idea=['按 h 降序处理：轮到某人时，已排好的人==都不比他矮==',
              '所以直接插到下标 `k`，前面恰好 `k` 个 ≥ 他的人',
              '他比已排好的人都矮（或同高但 k 更大）→ 插入==不会破坏==别人的 k'],
        summary=['时间 `O(n^2)`：每次插入最坏移动 `n` 个元素；原文提到可用平衡树优化',
                 '易错：同身高要按 `k` ==升序==，否则同高的人插入顺序会错',
                 '三个分支本质都是 `res.insert(pos, [h, k])`，分开写只是为了清楚',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
