S0 = 'aabc'


def _phase(S):
    ln = S.get('_line', 0)
    if ln <= 12:
        return '一、只含一种字母：找最长的连续相同段'
    if ln <= 34:
        return f'二、只含两种字母：`{S.get("c1", "?")}` 记 +1，`{S.get("c2", "?")}` 记 −1，找差为 0 的最长段'
    return '三、含三种字母：key = (a−b, a−c) 相同 ⇒ 中间三者个数相等'


def _txt(S):
    r = S.get('res')
    return _phase(S) + (f'　当前最长 ==`{r}`==' if r is not None else '')


def _hi(S, i, v):
    ln = S.get('_line', 0)
    if ln <= 12:
        p, q = S.get('p'), S.get('q')
        return 'blue' if p is not None and q is not None and p <= i < q else None
    if ln <= 34:
        c1, c2 = S.get('c1'), S.get('c2')
        idx = S.get('index')
        if c1 is None or idx is None or i > idx:
            return None
        return 'green' if v == c1 else 'pink' if v == c2 else None
    return None


def _ptr(S):
    ln = S.get('_line', 0)
    return S.get('q') if ln <= 12 else S.get('index')


CONFIG = dict(
    num=3714, title='最长的平衡子串 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='分三种情况 + 前缀和差哈希表',
    tags=['前缀和与哈希表', '难度分 2202'],
    code='''
class Solution(object):
    def longestBalanced(self, s):

        res = 0
        p = 0
        while p < len(s):
            q = p
            while q < len(s) and s[p] == s[q]:
                q += 1

            res = max(res, q - p)
            p = q


        def check_pair(c1, c2):
            f = {0: -1}
            cnt1, cnt2 = 0, 0
            res = 0
            for index, c in enumerate(s):
                if c != c1 and c != c2:
                    f = {0: index}
                    cnt1, cnt2 = 0, 0
                else:
                    if c == c1:
                        cnt1 += 1
                    else:
                        cnt2 += 1

                    if cnt1 - cnt2 in f:
                        res = max(res, index - f[cnt1 - cnt2])
                    else:
                        f[cnt1 - cnt2] = index
            return res

        res = max(res, check_pair('a', 'b'), check_pair('a', 'c'), check_pair('b', 'c'))

        f = {(0, 0): -1}
        cnt_a, cnt_b, cnt_c = 0, 0, 0
        for index, c in enumerate(s):
            if c == 'a':
                cnt_a += 1
            elif c == 'b':
                cnt_b += 1
            else:
                cnt_c += 1

            key = (cnt_a - cnt_b, cnt_a - cnt_c)
            if key in f:
                res = max(res, index - f[key])
            else:
                f[key] = index

        return res
''',
    call=f'Solution().longestBalanced({S0!r})',
    expect=3,
    skip=['def check_pair', 'if c == c1', "if c == 'a'", "elif c == 'b'", 'cnt1, cnt2 = 0, 0', 'res = 0', 'p = q', 'q = p', 'q += 1', 'p = 0',
          'cnt_a, cnt_b, cnt_c = 0', 'else:', 'cnt1 += 1', 'cnt2 += 1', 'cnt_a += 1', 'cnt_b += 1', 'cnt_c += 1'],
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前一种字母段，绿/粉 = 两种字母的 +1/−1）', cell=110, h=220,
             pointers={'q': 'blue', 'index': 'blue'}, color=_hi),
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='map', var='f', label='f（前缀和差 → 最早下标）', fmt=lambda k, v: f'{k}: {v}', h=210, font=28),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'blue'), ('cnt1', 'cnt1', 'green'), ('cnt2', 'cnt2', 'pink'), ('res', 'res', 'orange')],
    captions={
        'while p < len(s)': lambda S, B, r: (f'`p = {S.p}`：从这里开始找一段相同字母' if S.p < len(S.s) else '一种字母的情况统计完'),
        'while q < len(s) and s[p] == s[q]': lambda S, B, r: (f'`s[{S.q}] = {S.s[S.q]!r}` 与 `s[{S.p}]` 相同吗？' + ('相同，`q` 右移' if S.s[S.q] == S.s[S.p] else '不同，这段结束')
                                                              if S.q < len(S.s) else '到末尾，这段结束'),
        'res = max(res, q - p)': '这一段长 `{q} − {p} = {q - p}` → `res = {res}`',
        'f = {0: -1}': '`f` 记每个前缀差第一次出现的下标，空前缀差 0 在 -1',
        'for index, c in enumerate(s)': lambda S, B, r: (f'看 `s[{S.index}] = {S.c!r}`' if S.get('c') is not None and ('index' not in B or S.index != B.index)
                                                         else '这一遍扫完了'),
        'if c != c1 and c != c2': lambda S, B, r: (f'`{S.c!r}` 是第三种字母：子串不能含它 → ==重置== `f` 和计数' if S.c not in (S.c1, S.c2)
                                                   else f'`{S.c!r}` 属于 `({S.c1}, {S.c2})`，继续累计'),
        'f = {0: index}': '重置：从 `index` 之后重新开始，空前缀的下标记为 `{index}`',
        'if c == c1': '`c1` 记 +1，`c2` 记 −1，差 = `cnt1 − cnt2`',
        'if cnt1 - cnt2 in f': lambda S, B, r: (f'差 `{S.cnt1 - S.cnt2}` 以前出现过（下标 {S.f[S.cnt1 - S.cnt2]}）：中间 `c1`、`c2` 个数相等 → ==更新答案=='
                                                if S.cnt1 - S.cnt2 in S.f else f'差 `{S.cnt1 - S.cnt2}` 第一次出现，登记下标'),
        'res = max(res, index - f[cnt1 - cnt2])': '长度 `{index} − {f[cnt1 - cnt2]} = {index - f[cnt1 - cnt2]}` → `res = {res}`',
        'f[cnt1 - cnt2] = index': '记下差 `{cnt1 - cnt2}` 最早出现在 `{index}`（越早越长）',
        'return res': lambda S, B, r: (f'`({S.c1}, {S.c2})` 这一对的最长段长 `{S.res}`' if 'c1' in S else f'最长平衡子串长 `{S.res}`'),
        'res = max(res, check_pair': '三对字母 `(a,b)`、`(a,c)`、`(b,c)` 各算一遍，取最大 → `res = {res}`',
        'f = {(0, 0): -1}': '三种字母：key = `(cnt_a − cnt_b, cnt_a − cnt_c)`，空前缀 `(0,0)` 在 -1',
        'key = (cnt_a': '`{c!r}` 计数后，`cnt = ({cnt_a}, {cnt_b}, {cnt_c})`，key = `{key}`',
        'if key in f': lambda S, B, r: (f'`{S.key}` 以前出现过（下标 {S.f[S.key]}）：这两次之间 a、b、c 增量相同 → ==三者相等=='
                                        if S.key in S.f else f'`{S.key}` 第一次出现，登记下标'),
        'res = max(res, index - f[key])': '长度 `{index} − {f[key]} = {index - f[key]}` → `res = {res}`',
        'f[key] = index': '记下 `{key}` 最早出现在 `{index}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='答案只有三类：一种、两种、三种字母，后两类用前缀和找最早位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串只含 `a`、`b`、`c`；子串里所有不同字符出现次数都相同，称为平衡子串',
                 '求最长平衡子串的长度',
                 '本视频：`s = "aabc"` → `3`（`"abc"`）'],
        quote='这里就可以将所有的c1都视为-1、所有的c2都视为1，问题就转化成了找出s中的一个字段，其中仅包含-1和1，且子段之和恰好为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['一种字母：一趟遍历切出相同字母段，取最长',
              '两种字母：遇到第三种字母就==重置== `f` 和计数，段内用“差”的前缀和',
              '三种字母：用二元组 `(cnt_a − cnt_b, cnt_a − cnt_c)` 当 key，相同则中间三者个数相等'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`f` 里放的是每个差第一次出现的下标，越早越长',
                 '两种字母时遇到第三种字母要重置 `f = {0: index}`，不是 `{0: -1}`',
                 '对比灵神：灵神把两种字母先分组再算；yiduobo 在一趟遍历里遇到第三种字母就重置',
                 '原文本身可直接运行，代码未改'],
    ),
)
