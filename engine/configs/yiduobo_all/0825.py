AGES = [16, 16, 17, 18, 20]


def _brute(a):
    return sum(1 for i in range(len(a)) for j in range(len(a))
               if i != j and not (a[j] <= 0.5 * a[i] + 7 or a[j] > a[i] or (a[j] > 100 and a[i] < 100)))


def _info(S):
    ai = S.get('age_info')
    return [f'{a}岁×{c}' for a, c in ai] if ai else None


def _win(S):
    # 合法区间 [min_pos, index]
    if 'now' not in S or S.get('_line', 0) < 17:
        return None
    return S['min_pos']


def _color(S, i, v):
    if 'now' in S and S.get('_line') in (20, 21, 22, 23) and S['min_pos'] <= i <= S['index']:
        return 'green'
    return None


def _top(S):
    if 'age_info' not in S:
        return '`A` 能发给 `B` ⇔ `age[A]·0.5 + 7 < age[B] ≤ age[A]`'
    if 'now' not in S:
        return '按年龄排序 + 前缀和 `s`：区间人数 = `s[index] − s[min_pos − 1]`'
    now = S['now']
    lo = now * 0.5 + 7
    return f'年龄 `{now}` 能发给 `({lo:g}, {now}]` 内的人'


def _wh(S, B, ret):
    mp, idx, now = S.min_pos, S.index, S.now
    if mp <= idx and (S.age_info[mp][0] - 7) * 2 <= now:
        a = S.age_info[mp][0]
        return f'`{a} ≤ {now}·0.5 + 7`：{a} 岁太小，收不到 → 左边界右移'
    if mp > idx:
        return '左边界已经越过自己：没有人能收'
    a = S.age_info[mp][0]
    return f'`{a} > {now}·0.5 + 7`：{a} 岁可以收 → 左边界停在 `min_pos = {mp}`'


CONFIG = dict(
    num=825, title='适龄的朋友', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按年龄计数排序 · 双指针 + 前缀和',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1697'],
    code='''
class Solution(object):
    def numFriendRequests(self, ages):

        age_dict = {}
        for age in ages:
            age_dict[age] = age_dict.get(age, 0) + 1

        age_info = sorted(age_dict.items(), key=lambda d:d[0])
        s = [age_info[0][1]]
        for index in range(1, len(age_info)):
            s.append(s[-1] + age_info[index][1])

        min_pos = 0
        res = 0
        for index in range(len(age_info)):
            now, cnt = age_info[index]
            while min_pos <= index and (age_info[min_pos][0] - 7) * 2 <= now:
                min_pos += 1
            
            if min_pos == 0:
                res += cnt * (s[index] - 1)
            elif min_pos <= index:
                res += cnt * (s[index] - s[min_pos - 1] - 1)

        return res
''',
    call=f'Solution().numFriendRequests({AGES})',
    expect=_brute(AGES),
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='map', var='age_dict', label='age_dict（年龄 → 人数）', fmt=lambda k, v: f'{k}岁: {v}', h=130, font=32),
        dict(type='array', var=_info, label='age_info（按年龄排序；框 = 能收请求的 [min_pos, index]）',
             pointers={'min_pos': 'blue', 'index': 'pink'}, window=(_win, 'index'), color=_color, cell=150, h=230),
        dict(type='array', var='s', label='s（人数前缀和）', cell=150, h=170),
    ],
    watch=[('index', 'index', 'pink'), ('min_pos', 'min_pos', 'blue'), 'now', 'cnt', ('res', 'res', 'green')],
    skip=['for age in ages'],
    captions={
        'age_dict = {}': '先按年龄统计人数：同龄的人可以==一起算==',
        'age_dict[age] = age_dict.get': '`age_dict[{age}]` → {age_dict[age]}',
        'age_info = sorted': '按年龄从小到大排序：`{age_info}`',
        's = [age_info[0][1]]': '前缀和 `s[0] = {s[0]}`',
        'for index in range(1': lambda S, B, r: ('前缀和算完' if len(S.s) == len(S.age_info) else f'`index = {S.index}`'),
        's.append(': '`s[{len(s) - 1}] = {s[-2]} + {age_info[len(s) - 1][1]} = {s[-1]}`',
        'min_pos = 0': '`min_pos`：合法区间的左边界（只会右移）',
        'res = 0': '`res = 0`',
        'for index in range(len(age_info))': lambda S, B, r: (f'枚举发送者的年龄：`index = {S.index}`' if 'now' not in B or B.index != S.index or B._line == 16 else '枚举结束'),
        'now, cnt = age_info[index]': '`{now}` 岁有 `{cnt}` 人；区间右边界就是自己',
        'while min_pos <= index': _wh,
        'min_pos += 1': '`min_pos` → {min_pos}',
        'if min_pos == 0': lambda S, B, r: ('`min_pos == 0`：从最小年龄起都能收，人数直接是 `s[index]`' if S.min_pos == 0
                                            else f'`min_pos = {S.min_pos}`，用前缀和相减'),
        'res += cnt * (s[index] - 1)': '`{cnt}` 人 × (区间 `{s[index]}` 人 − 自己) → `res` = =={res}==',
        'elif min_pos <= index': lambda S, B, r: (f'区间 `[{S.min_pos}, {S.index}]` 非空' if S.min_pos <= S.index else '区间为空：这个年龄发不出请求'),
        'res += cnt * (s[index] - s[min_pos - 1] - 1)': '区间人数 `{s[index]} − {s[min_pos - 1]} = {s[index] - s[min_pos - 1]}`，每人发 `{s[index] - s[min_pos - 1] - 1}` 份：`res += {cnt} × {s[index] - s[min_pos - 1] - 1}` → =={res}==',
        'return res': '一共 =={ret}== 个好友请求',
    },
    max_steps=70,
    cards=dict(
        one_liner='排序后区间 (age/2+7, age] 只会右移：双指针 + 前缀和',
        complexity='时间 `O(n + m log m)`（m = 不同年龄数），空间 `O(m)`',
        problem=['`x` ==不会==给 `y` 发请求：`ages[y] ≤ 0.5·ages[x] + 7`、`ages[y] > ages[x]`、或 `ages[y] > 100 且 ages[x] < 100`',
                 '求好友请求总数（不会发给自己）',
                 '示例：`[16,17,18]` → `2`；`[20,30,100,110,120]` → `3`',
                 f'本视频：`{AGES}` → `{_brute(AGES)}`'],
        quote='随着age[A]的增大，这个区间也是在逐渐往坐标轴右侧移动的……假设这个区间内一共有k人，那么除开此人本身之外，一共可以发出k - 1份好友请求。',
        quote_src='—— yiduobo 题解原文',
        idea=['条件三多余：`age[B] > 100 > age[A]` 时必有 `age[B] > age[A]`',
              '合法区间 `(age[A]·0.5 + 7, age[A]]` 随年龄右移 → 只维护左边界',
              '同龄 cnt 人一起算：`cnt × (k − 1)`，k 用==前缀和==求'],
        summary=['只维护左边界 `min_pos`，右边界就是当前年龄自己',
                 '`(a − 7)·2 ≤ now` 即 `a ≤ now/2 + 7`：用整数比较避免浮点',
                 '区间人数要减 1：不能给自己发',
                 '对比灵神：灵神直接开长 121 的数组枚举所有年龄；这里只枚举出现过的年龄',
                 '代码本身可在 Python 3 运行，未做改动'],
    ),
)
