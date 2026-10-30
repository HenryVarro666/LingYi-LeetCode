def _line(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'right' not in S:
        return
    lo0, hi0 = S['blocks'][0], S['blocks'][0] + (len(S['blocks']) - 1) * S['split']
    cv.text((x0 + 18, y0 + 4), '答案的搜索范围（数轴）：蓝 = left，粉 = right，黄 = mid', 24, T['muted'], bold=True)
    nb = len(S['blocks'])
    ax0, ax1 = x0 + 60, x1 - 60
    y = y0 + 120

    def X(v):
        return ax0 + (v - lo0) / max(1, hi0 - lo0) * (ax1 - ax0)
    cv.line([(ax0, y), (ax1, y)], T['border'], 3)
    l, r = S['left'], S['right']
    cv.rect((X(l), y - 14, max(X(r), X(l) + 4), y + 14), fill=T['blue'], alpha=90, r=6)
    for name, v, c, dy in (('left', l, T['blue'], 1), ('right', r, T['pink'], 1)):
        cv.line([(X(v), y - 26), (X(v), y + 26)], c, 5)
        cv.text((X(v), y + 34 + (28 if (name == 'right' and l == r) else 0)), f'{name}={v}', 24, c, anchor='mt', bold=True)
    if 'mid' in S:
        m = S['mid']
        cv.line([(X(m), y - 40), (X(m), y + 26)], T['yellow'], 5)
        cv.text((X(m), y - 46), f'mid={m}', 24, T['yellow'], anchor='mb', bold=True)
    cv.text((ax0, y + 90), f'下界 = 最大的街区 {lo0}（至少要建完它）', 20, T['dim'])
    cv.text((ax1, y + 90), f'上界 = {lo0} + {nb - 1}×split = {hi0}（先全分裂再各建一块）', 20, T['dim'], anchor='rt')


CONFIG = dict(
    num=1199, title='建造街区的最短时间', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='二分答案 + 模拟分裂',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minBuildTime(self, blocks, split):

        blocks.sort(reverse=True)

        n = len(blocks)
        left = blocks[0]
        right = blocks[0] + (n - 1) * split

        while left < right:
            mid = (left + right) // 2

            idle = 1
            flag = True
            last_rnd = 0

            for index, t in enumerate(blocks):
                if idle == 0:
                    flag = False
                    break
                rest_time = mid - t
                rnd = rest_time // split

                if rnd - last_rnd >= 10:
                    break
                
                idle <<= (rnd - last_rnd)
                if idle >= n - index:
                    break
                
                last_rnd = rnd
                idle -= 1

            if flag:
                right = mid
            else:
                left = mid + 1
        
        return left
''',
    call='Solution().minBuildTime([1,2,4,7], 3)',
    expect=11,
    views=[
        dict(type='array', var='blocks', label='blocks（从大到小：耗时长的先建）', pointers={'index': 'blue'}, h=190,
             color=lambda S, i, v: 'blue' if S.get('index') == i and S.get('t') == v else None),
        dict(type='custom', draw=_line, h=300),
        dict(type='text', size=26, h=70, fn=lambda S: (f"工人数 `idle = {S['idle']}`，上一次的分裂轮次 `last_rnd = {S['last_rnd']}`" if 'idle' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('idle', 'idle', 'green'),
           ('rnd', 'rnd', 'orange'), ('flag', 'flag', 'cyan')],
    captions={
        'blocks.sort(reverse=True)': '==耗时最长的街区排在前面先建==，这样它有最多时间，后面短的可以晚点分裂再建：`{blocks}`',
        'left = blocks[0]': '答案至少是最长的街区 `{left}`',
        'right = blocks[0]': '答案至多：先分裂出 `n-1` 次，每次 `split`，再各建一块 → `{right}`',
        'while left < right': lambda S, B, r: (f'搜索范围 [`{S.left}`, `{S.right}`] 还没收缩到一个点 → 继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}` → 找到最小建造时间'),
        'mid = (left + right) // 2': '二分答案：能不能在 `mid = {mid}` 分钟内全部建完？时间越长越容易，所以==可行性单调==',
        'idle = 1': '判定：一开始只有 1 个工人',
        'flag = True': '假设可行，遇到工人不够再改成 False',
        'last_rnd = 0': '`last_rnd`：到上一个街区为止，已经用了多少轮分裂',
        'for index, t in enumerate(blocks)': lambda S, B, r: (f'给第 `{S.index}` 个街区（耗时 `{S.t}`）安排工人' if 'index' in B and S.index != B.index or 'index' not in B
                                                              else '所有街区都安排完了'),
        'if idle == 0': lambda S, B, r: ('工人用完了但街区还没建完 → 这个 `mid` ==不够=='if S.idle == 0 else f'还有 `{S.idle}` 个工人，继续'),
        'flag = False': '`flag = False`：`mid = {mid}` 太小',
        'rest_time = mid - t': '这个街区建造要 `{t}`，其余 `rest_time = {mid} - {t} = {rest_time}` 分钟可用来分裂',
        'rnd = rest_time // split': '分裂一轮要 `{split}`，最多分 `rnd = {rest_time} // {split} = {rnd}` 轮',
        'if rnd - last_rnd >= 10': lambda S, B, r: ('比上一个街区多分裂 10 轮以上 → 工人至少 1024 个，远超街区数 → ==肯定够==' if S.rnd - S.last_rnd >= 10
                                                   else f'比上一个街区多分裂 `{S.rnd - S.last_rnd}` 轮，不会爆炸，继续算'),
        'idle <<= (rnd - last_rnd)': '多出来的 `{rnd - last_rnd}` 轮分裂：工人数翻 `2^{rnd - last_rnd}` 倍 → `idle = {idle}`',
        'if idle >= n - index': lambda S, B, r: (f'工人 `{S.idle}` ≥ 剩余街区 `{S.n - S.index}` → 每块一个人，==够了=='if S.idle >= S.n - S.index
                                                 else f'工人 `{S.idle}` < 剩余街区 `{S.n - S.index}`，继续'),
        'last_rnd = rnd': '记住已用轮数：`last_rnd = {last_rnd}`',
        'idle -= 1': '一个工人去建这个街区，不再分裂：`idle = {idle}`',
        'if flag': lambda S, B, r: (f'`mid = {S.mid}` ==可行== → 答案不超过 mid，缩小上界' if S.flag else f'`mid = {S.mid}` ==不可行== → 答案大于 mid，抬高下界'),
        'right = mid': '`right = {right}`',
        'left = mid + 1': '`left = {left}`',
        'return left': '最短建造时间 =={ret}==',
    },
    skip=['flag = True', 'last_rnd = 0'],
    cards=dict(
        one_liner='二分「总用时」，再模拟分裂检查工人够不够',
        complexity='时间 `O(n log S)`，空间 `O(1)`',
        problem=['有若干街区，建一个要 `blocks[i]` 分钟；一个工人可以建街区，或花 `split` 分钟分裂成两个工人',
                 '所有工人同时工作，求建完所有街区的最短时间',
                 '示例：`blocks=[1,2,3], split=1` → `4`；本视频：`[1,2,4,7], split=3` → `11`'],
        quote='建造时间越长，可以完成建造的可能性就越大，这也就意味着本题可以通过二分这个最短的建造时间，将问题转化为判定问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['总用时越大越容易 → ==二分答案 `mid`==，范围 `[最大街区, 最大街区 + (n-1)×split]`',
              '判定：耗时长的先建；用 `mid - t` 算出还能分裂几轮，工人数 `idle` 随之翻倍',
              '工人 ≥ 剩余街区就够了；分裂轮数差 ≥ 10 说明工人早就爆多，直接判可行'],
        summary=['时间 `O(n log S)`，空间 `O(1)`',
                 '判定里先判断 `idle == 0`，最后一个街区后工人变 0 也算不够',
                 '轮数差太大时不能直接左移，否则整数会爆炸，所以用 10 轮截断',
                 '原文为 Python 2 写法，`/` 是整数除法，已改为 `//`（`mid` 与 `rnd` 两处）',
                 '题面库里没有，题意依据 yiduobo 文章与力扣原题'],
    ),
)
