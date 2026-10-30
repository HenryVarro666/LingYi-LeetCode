AGES = [16, 16, 17, 18, 20]
LO, HI = 11, 26   # 画出的年龄范围（其余年龄的人数都是 0）


def _brute(a):
    return sum(1 for i in range(len(a)) for j in range(len(a))
               if i != j and not (a[j] <= 0.5 * a[i] + 7 or a[j] > a[i] or (a[j] > 100 and a[i] < 100)))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'cnt[age]：每个年龄的人数（只画 {LO}..{HI}，框 = 窗口 [age_y, age_x]）', 22, T['muted'], bold=True)
    if 'cnt' not in S:
        return
    cnt = S['cnt']
    n = HI - LO + 1
    cell = min(64, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    top, h = y0 + 70, 110
    live = 'age_x' in S and S.get('_line', 0) >= 13
    ax, ay = (S['age_x'], S['age_y']) if live else (None, None)
    for k in range(n):
        age = LO + k
        X = sx + k * cell
        inwin = live and ay <= age <= ax
        fill = T['panel2']
        if live and age == ax and S.get('c'):
            fill = (40, 90, 60)
        cv.rect((X + 3, top, X + cell - 3, top + h), fill=fill, outline=T['cyan'] if inwin else T['border'], width=3 if inwin else 1, r=6)
        v = cnt[age]
        cv.text((X + cell / 2, top + h / 2), v, 36, T['text'] if v else T['dim'], anchor='mm', bold=True)
        cv.text((X + cell / 2, top + h + 8), age, 20, T['muted'], anchor='mt', mono=True)
    if not live:
        return
    for name, age, c, row in (('age_y', ay, T['blue'], 0), ('age_x', ax, T['pink'], 1)):
        if LO <= age <= HI:
            X = sx + (age - LO) * cell + cell / 2
            cv.tri_up(X, top + h + 40, 10, c)
            cv.text((X, top + h + 56 + row * 26), name, 22, c, anchor='mt', bold=True)
        elif age > HI:
            cv.text((x1 - 24, top + h + 56 + row * 26), f'{name} = {age} →', 22, c, anchor='ra', bold=True)
        else:
            cv.text((x0 + 24, top + h + 56 + row * 26), f'← {name} = {age}', 22, c, anchor='la', bold=True)


def _formula(S):
    if 'age_x' not in S or S.get('_line', 0) < 13:
        return '`x` 能发给 `y` ⇔ `age_x / 2 + 7 < age_y ≤ age_x`（且 x ≠ y）'
    ax, ay = S['age_x'], S['age_y']
    return f'能收 {ax} 岁请求的年龄：`({ax}/2 + 7, {ax}]` = `[{ay}, {ax}]`，共 `cnt_window = {S["cnt_window"]}` 人'


def _iter(S, B, ret):
    ax, ay, c, w = S.age_x, S.age_y, S.c, S.cnt_window
    head = f'`age_x = {ax}`：' + (f'{c} 人进窗口；' if c else '')
    if w == 0 and ay > ax:
        return head + f'`{ax}/2 + 7 ≥ {ax}`：这个年龄==不可能==发请求（窗口为空）'
    if w == 0:
        return head + f'窗口 `[{ay}, {ax}]` 没人 → 跳过'
    if c == 0:
        return head + f'窗口有 {w} 人，但没有 {ax} 岁的人发请求'
    return head + f'窗口 `[{ay}, {ax}]` 有 =={w}== 人，可以发请求'


CONFIG = dict(
    num=825, title='适龄的朋友', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='计数 + 滑动窗口（枚举年龄）',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1697'],
    code='''
class Solution:
    def numFriendRequests(self, ages: List[int]) -> int:
        cnt = [0] * 121
        for age in ages:
            cnt[age] += 1

        ans = cnt_window = age_y = 0
        for age_x, c in enumerate(cnt):
            cnt_window += c
            if age_y * 2 <= age_x + 14:  # 不能发送好友请求
                cnt_window -= cnt[age_y]
                age_y += 1
            if cnt_window:  # 存在可以发送好友请求的用户
                ans += c * cnt_window - c
        return ans
''',
    call=f'Solution().numFriendRequests({AGES})',
    expect=_brute(AGES),
    views=[
        dict(type='text', fn=_formula, size=26, h=80),
        dict(type='custom', draw=_draw, h=300),
    ],
    watch=[('age_x', 'age_x', 'pink'), ('age_y', 'age_y', 'blue'), 'c', ('cnt_window', 'cnt_window', 'cyan'), ('ans', 'ans', 'green')],
    # 年龄要从 0 枚举到 120：每轮的 4 行合并到 if cnt_window 这一步讲，否则步数爆炸
    skip=['for age in ages', 'for age_x, c', 'cnt_window += c', 'if age_y * 2', 'cnt_window -= cnt', 'age_y += 1'],
    captions={
        'cnt = [0] * 121': '年龄只有 1..120：用长 121 的数组统计每个年龄的人数',
        'cnt[age] += 1': '`cnt[{age}]` → {cnt[age]}',
        'ans = cnt_window': '`cnt_window`：年龄在 `[age_y, age_x]` 的人数；枚举 `age_x` 从 0 到 120',
        'if cnt_window': _iter,
        'ans += c * cnt_window - c': lambda S, B, r: ('`c = 0`：这一项是 0，`ans` 不变' if S.c == 0 else
                                                      f'{S.c} 人各发给窗口里的 {S.cnt_window} 人，去掉发给自己的 {S.c} 次：`ans += {S.c}×{S.cnt_window} − {S.c}` → =={S.ans}=='),
        'return ans': '一共 =={ret}== 个好友请求',
    },
    max_steps=46,
    cards=dict(
        one_liner='年龄只有 120 种：按年龄计数，窗口 [age_y, age_x] 随 age_x 右移',
        complexity='时间 `O(n + U)`，空间 `O(U)`（U = 120）',
        problem=['`x` ==不会==给 `y` 发请求：`ages[y] ≤ 0.5·ages[x] + 7`、`ages[y] > ages[x]`、或 `ages[y] > 100 且 ages[x] < 100`',
                 '求好友请求总数（不会发给自己）',
                 '示例：`[16,17,18]` → `2`；`[20,30,100,110,120]` → `3`',
                 f'本视频：`{AGES}` → `{_brute(AGES)}`'],
        quote='当前这 cnt[ageX] 个用户可以与 cntWindow 个用户发送好友请求，根据乘法原理，这有 cnt[ageX]·cntWindow 个。其中有 cnt[ageX] 个好友请求是自己发给自己的，要减去。',
        quote_src='—— 灵茶山艾府题解',
        idea=['能发请求 ⇔ `ageX/2 + 7 < ageY ≤ ageX`；第三个条件自动为假',
              '`ageX` 越大，最小的 `ageY` 也越大 → ==滑动窗口==',
              '斜率只有 1/2：`ageX` 加 1，`ageY` 至多加 1，所以 `while` 可写成 `if`'],
        summary=['时间 `O(n + U)`：只枚举 121 个年龄，与人数无关',
                 '`ageY ≤ ageX/2 + 7` 改写成 `ageY·2 ≤ ageX + 14`，避免浮点',
                 '`c·cntWindow − c`：别忘了减去自己发给自己',
                 '本视频把每轮的窗口移动合并到 `if cnt_window` 一步讲解，后面全 0 的年龄快进'],
    ),
)
