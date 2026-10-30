def _L(k):
    return chr(97 + k)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cnt = S.get('cnt_dict')
    conf = S.get('conflict')
    if not cnt or conf is None:
        cv.text((x0 + 18, y0 + 4), 'conflict[a][b]：首字母 a、b 里 body 相同、不能互换的名字个数', 22, T['muted'], bold=True)
        return
    ks = sorted(cnt)
    n = len(ks)
    final = S.get('_line') == 32
    cv.text((x0 + 18, y0 + 4), 'conflict[a][b]：body 相同、不能互换的名字数' + ('；右上 = 产出数' if final else ''), 22, T['muted'], bold=True)
    cw = min(200, (x1 - x0 - 150) / n)
    cell = 96
    sx, sy = x0 + 100, y0 + 70
    for j, kb in enumerate(ks):
        cv.text((sx + j * cw + cw / 2, sy - 10), f'{_L(kb)}（{cnt[kb]} 个）', 22, T['cyan'], anchor='mb', bold=True)
    for i, ka in enumerate(ks):
        cv.text((sx - 10, sy + i * cell + cell / 2), f'{_L(ka)}（{cnt[ka]} 个）', 22, T['cyan'], anchor='rm', bold=True)
        for j, kb in enumerate(ks):
            X, Y = sx + j * cw, sy + i * cell
            v = conf[ka][kb]
            if i == j:
                cv.rect((X + 3, Y + 3, X + cw - 3, Y + cell - 3), fill=T['panel2'], r=8)
                continue
            if final and j > i:
                g = (cnt[ka] - conf[ka][kb]) * (cnt[kb] - conf[kb][ka]) * 2
                cv.rect((X + 3, Y + 3, X + cw - 3, Y + cell - 3), fill=T['green'] if g else T['panel2'], alpha=90 if g else 255, outline=T['green'], r=8)
                cv.text((X + cw / 2, Y + cell / 2 - 14), f'({cnt[ka]}-{conf[ka][kb]})×({cnt[kb]}-{conf[kb][ka]})×2', 17, T['text'], anchor='mm', mono=True)
                cv.text((X + cw / 2, Y + cell / 2 + 16), f'= {g}', 26, T['text'], anchor='mm', bold=True)
            else:
                cv.rect((X + 3, Y + 3, X + cw - 3, Y + cell - 3), fill=T['yellow'] if v else T['panel2'], alpha=110 if v else 255, outline=T['border'], r=8)
                cv.text((X + cw / 2, Y + cell / 2), v, 36, T['text'] if v else T['dim'], anchor='mm', bold=True)
    cv.text((x0 + 18, sy + n * cell + 24), '其余字母没有名字：cnt = 0，不产出名字', 20, T['dim'])


def _bodyof(S, lst):
    for k, v in S['same_body'].items():
        if v == lst:
            return k
    return '?'


def _c_body(S, B, r):
    if 'same_body_ascs' in B and S.same_body_ascs == B.same_body_ascs:
        return '所有 body 都检查完了，冲突矩阵建好'
    lst = S.same_body_ascs
    return f'看 body = `{_bodyof(S, lst)}`，带它的首字母：{"".join(_L(x) for x in lst)}'


def _c_i(S, B, r):
    lst = S.same_body_ascs
    if len(lst) < 2:
        return f'只有 `{_L(lst[0])}` 一个首字母带这个 body，没有冲突，内层循环不进入'
    if 'j' in B._inner:
        return '这个 body 的所有首字母对都处理完了'
    return f'`{_bodyof(S, lst)}` 被 {len(lst)} 个首字母共用 → 两两配对，找冲突'


CONFIG = dict(
    num=2306, title='公司命名', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='首字母计数 · body 冲突矩阵',
    tags=['灵神题单·数学算法', '难度分 2305'],
    code='''
class Solution(object):
    def distinctNames(self, ideas):

        cnt_dict = {}
        same_body = {}
        for idea in ideas:
            first_asc = ord(idea[0]) - 97
            cnt_dict[first_asc] = cnt_dict.get(first_asc, 0) + 1
        
            body = idea[1:]
            if body not in same_body:
                same_body[body] = []
            same_body[body].append(first_asc)

        n = len(ideas)
        res = 0

        conflict = [[0] * 26 for _ in range(26)]
        for same_body_ascs in same_body.values():
            for i in range(len(same_body_ascs) - 1):
                for j in range(i + 1, len(same_body_ascs)):
                    conflict[same_body_ascs[i]][same_body_ascs[j]] += 1
                    conflict[same_body_ascs[j]][same_body_ascs[i]] += 1

        for asc_a in range(25):
            for asc_b in range(asc_a + 1, 26):
                if asc_a == asc_b:
                    continue
                
                res += (cnt_dict.get(asc_a, 0) - conflict[asc_a][asc_b]) * (cnt_dict.get(asc_b, 0) - conflict[asc_b][asc_a]) * 2

        return res
''',
    call='Solution().distinctNames(["coffee","donuts","time","toffee"])',
    expect=6,
    skip=['for asc_a in range(25)', 'for asc_b in range', 'if asc_a == asc_b', 'continue', 'res += (cnt_dict'],
    views=[
        dict(type='map', var='cnt_dict', fmt=lambda k, v: f'{_L(k)} → {v}', label='cnt_dict：每个首字母有几个名字', h=100),
        dict(type='map', var='same_body', fmt=lambda k, v: f'{k} → {"".join(_L(x) for x in v)}', label='same_body：body → 出现过的首字母', h=120),
        dict(type='custom', draw=_draw, h=410),
    ],
    watch=['res'],
    captions={
        'cnt_dict = {}': '`cnt_dict[first]`：以 first 为首字母的名字个数',
        'same_body = {}': '`same_body[body]`：body（去掉首字母的部分）→ 带这个 body 的首字母列表',
        'first_asc = ': '`{idea}` 的首字母 `{idea[0]}` → 下标 `{first_asc}`',
        'cnt_dict[first_asc] =': '`cnt_dict[{first_asc}]` = {cnt_dict[first_asc]}：`{idea[0]}` 开头的名字多了一个',
        'body = idea': '`body = {body!r}`：去掉首字母剩下的部分',
        'if body not in': lambda S, B, r: (f'`{S.body}` 第一次出现 → 先建一个空列表' if S.body not in B.same_body else f'`{S.body}` 之前出现过（首字母 {"".join(_L(x) for x in B.same_body[S.body])}）→ 这就是一个冲突来源'),
        'same_body[body] = []': '为 `{body}` 新建空列表',
        'same_body[body].append': '`{body}` 对应的首字母：{"".join(_L(x) for x in same_body[body])}',
        'n = len(ideas)': '名字总数 `n = {n}`（这份代码后面没用到）',
        'res = 0': '`res` 累计合法公司名',
        'conflict = [[0]': '`conflict[a][b]`：首字母 a、b 之间 body 相同的名字个数，先全 0',
        'for same_body_ascs in': _c_body,
        'for i in range(len': _c_i,
        'for j in range(i + 1': lambda S, B, r: f'配对 `{_L(S.same_body_ascs[S.i])}` 和 `{_L(S.same_body_ascs[S.j])}`：它们有同一个 body' if 'j' in S and S._inner.get('j') is not None and ('j' not in B._inner or S.j != B.j or S.i != B.i) else '这一个首字母的配对找完了',
        'conflict[same_body_ascs[i]][same_body_ascs[j]] += 1': lambda S, B, r: f'题目保证名字不重复，`conflict[{_L(S.same_body_ascs[S.i])}][{_L(S.same_body_ascs[S.j])}]` 直接 +1',
        'conflict[same_body_ascs[j]][same_body_ascs[i]] += 1': lambda S, B, r: f'对称的 `conflict[{_L(S.same_body_ascs[S.j])}][{_L(S.same_body_ascs[S.i])}]` 也 +1：c 和 t 各有一个名字不能和对方互换',
        'return res': '枚举每一对首字母 a、b（右上角表格）：`(cnt[a]-冲突) × (cnt[b]-冲突) × 2`，相加得 ==`{res}`==（真实循环要走 325 对，这里只画有名字的字母）',
    },
    cards=dict(
        one_liner='先数每个首字母有几个名字，再扣掉 body 相同的冲突',
        complexity='时间 `O(n·m + 26²)`，空间 `O(n·m + 26²)`',
        problem=['选两个不同名字，互换首字母，两个新名字==都不在 ideas 里==才有效',
                 '`idea_A idea_B` 的先后算不同名字',
                 '示例：`["coffee","donuts","time","toffee"]` → `6`'],
        quote='对于first_a和first_b，也可能存在某些idea会出现body相同的情况，这些idea不能与另一方的任意idea进行交换操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['首字母不同才可能换：`cnt[a] × cnt[b] × 2` 是理论上限',
              'body（去掉首字母的部分）相同的两个名字，换首字母会撞上对方 → 记入 `conflict[a][b]`',
              '合法数 = `(cnt[a]−冲突) × (cnt[b]−冲突) × 2`，对所有首字母对求和'],
        summary=['时间 `O(n·m + 26²)`',
                 '冲突要对称地 `+= 1` 两个格子，因为名字互不相同',
                 '最后的 26×26 双重循环共 325 对，视频里不逐对播放，只展示有名字的字母对',
                 '对比灵神：灵神按首字母分组、直接算集合交集；yiduobo 按 body 分组、累计冲突矩阵'],
    ),
)
