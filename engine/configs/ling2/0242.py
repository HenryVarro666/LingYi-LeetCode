def _pos_s(S):
    if 'cnt' not in S or S['_line'] not in (4, 5):
        return None
    k = sum(S['cnt']) - (1 if S['_line'] == 5 else 0)
    return k if 0 <= k < len(S['s']) else None


def _pos_t(S):
    if 'cnt' not in S or S['_line'] not in (6, 7):
        return None
    k = len(S['s']) - sum(S['cnt']) - (1 if S['_line'] == 7 else 0)
    return k if 0 <= k < len(S['t']) else None


def _done_s(S, i, v):
    if 'cnt' not in S:
        return None
    if S['_line'] in (4, 5):
        k = sum(S['cnt'])
        return 'green' if i < k else None
    return 'green' if S['_line'] > 5 else None


def _done_t(S, i, v):
    if 'cnt' not in S or S['_line'] < 6:
        return None
    if S['_line'] in (6, 7):
        k = len(S['s']) - sum(S['cnt'])
        return 'pink' if i < k else None
    return 'pink'


def _draw_cnt(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'cnt[26]：s 里出现 +1，t 里出现 −1（下标 = ord(c) − ord(\'a\')）', 22, T['muted'], bold=True)
    cnt = S.get('cnt')
    if cnt is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    bc = B.get('cnt')
    n = 26
    cell = (x1 - x0 - 40) / n
    sx = x0 + 20
    top = y0 + 56
    hot = None
    if S['_line'] in (5, 7) and isinstance(S.get('c'), str):
        hot = ord(S['c']) - ord('a')
    for i in range(n):
        v = cnt[i]
        X = sx + i * cell
        if v > 0:
            fill, tc = T['blue'], T['bg']
        elif v < 0:
            fill, tc = T['red'], T['bg']
        else:
            fill, tc = T['panel2'], T['dim']
        changed = bc is not None and bc[i] != v
        cv.rect((X + 2, top, X + cell - 2, top + cell * 1.3), fill=fill, r=6,
                outline=T['yellow'] if changed or i == hot else T['border'], width=3 if (changed or i == hot) else 1)
        cv.text((X + cell / 2, top + cell * 0.65), v, 18, tc, anchor='mm', bold=True)
        cv.text((X + cell / 2, top + cell * 1.3 + 6), chr(97 + i), 18, T['yellow'] if i == hot else T['muted'], anchor='mt', mono=True)
        if i % 5 == 0:
            cv.text((X + cell / 2, top + cell * 1.3 + 30), i, 13, T['dim'], anchor='mt', mono=True)
    nz = [chr(97 + i) + ':' + str(cnt[i]) for i in range(n) if cnt[i]]
    msg = '非 0 的格子：' + ('  '.join(nz) if nz else '无 → ==全为 0==')
    cv.rich(x0 + 22, top + cell * 1.3 + 60, msg, x1 - x0 - 44, size=24, accent=T['green'])


CONFIG = dict(
    num=242, title='有效的字母异位词', difficulty='Easy', category='哈希',
    author='灵茶山艾府', technique='一个计数数组：s 加、t 减',
    tags=['面试经典150'],
    code='''
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        cnt = [0] * 26
        for c in s:
            cnt[ord(c) - ord('a')] += 1
        for c in t:
            cnt[ord(c) - ord('a')] -= 1
        return all(c == 0 for c in cnt)
''',
    call='Solution().isAnagram("anagram", "nagaram")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（绿 = 已经 +1）', cell=72, h=170,
             pointers={_pos_s: 'yellow'}, pointer_labels={_pos_s: 'c'}, color=_done_s),
        dict(type='string', var='t', label='t（粉 = 已经 −1）', cell=72, h=170,
             pointers={_pos_t: 'yellow'}, pointer_labels={_pos_t: 'c'}, color=_done_t),
        dict(type='custom', draw=_draw_cnt, h=250),
    ],
    watch=[('c', 'c', 'yellow'), ('ord(c)-97', lambda S: ord(S['c']) - 97), ('sum(cnt)', lambda S: sum(S['cnt']), 'cyan')],
    captions={
        'cnt = [0] * 26': '只有小写字母 → 开一个长为 ==26== 的计数数组',
        'for c in s': lambda S, B, r: (f'扫 s：取出 `c = {S.c!r}`' if S._line == 4 and _pos_s(S) is not None
                                       else 's 扫完了：`cnt` 里存的是 s 中每个字母的出现次数'),
        "+= 1": lambda S, B, r: (f"`{S.c!r}` 的下标是 `ord({S.c!r}) − ord('a') = {ord(S.c) - 97}` → `cnt[{ord(S.c) - 97}]` 加一变成 `{S.cnt[ord(S.c) - 97]}`"
                                 if _pos_s(S) in (0, 1) else f"`cnt[{ord(S.c) - 97}]`（{S.c!r}）加一 → `{S.cnt[ord(S.c) - 97]}`"),
        'for c in t': lambda S, B, r: (f'扫 t：取出 `c = {S.c!r}`' if _pos_t(S) is not None
                                       else 't 也扫完了：s 加、t 减，==两边相同的字母正好抵消=='),
        "-= 1": lambda S, B, r: (f"`cnt[{ord(S.c) - 97}]`（{S.c!r}）减一 → `{S.cnt[ord(S.c) - 97]}`"
                                 + ('：t 里的这个字母比 s 多了' if S.cnt[ord(S.c) - 97] < 0 else '')),
        'return all(': lambda S, B, r: ('`cnt` ==全为 0==：每个字母在 s、t 中出现次数一样 → 返回 `True`' if r
                                         else '`cnt` 有非 0 的格子 → 次数不一样 → 返回 `False`'),
    },
    cards=dict(
        one_liner='x = y 等价于 x − y = 0：s 里加一，t 里减一，最后看是否全为 0',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`，`|Σ| = 26`',
        problem=['判断 `t` 是不是 `s` 的==字母异位词==：每个字母出现的次数都相同',
                 '示例：`s = "anagram"`，`t = "nagaram"` → `true`',
                 '`s = "rat"`，`t = "car"` → `false`；只含小写字母'],
        quote='可以只用一个 cnt 数组：把 s[i] 的出现次数加一，把 t[i] 的出现次数减一，最后判断 cnt 数组是否全为 0。从数学上来说，就是 ==x=y 等价于 x−y=0== 的意思。',
        quote_src='—— 灵茶山艾府题解',
        idea=['基础做法：分别统计 s 和 t 的字母次数，比较两个计数（`Counter(s) == Counter(t)`）',
              '优化：一个数组，s 的字母 `+1`、t 的字母 `−1`',
              '`a` 到 `z` 的 ASCII 连续 → `ord(c) − ord(\'a\')` 就是下标 0~25'],
        summary=['时间 `O(n + 26)`，空间 `O(26)`',
                 '长度不同时 `cnt` 一定不会全为 0，不用单独判断',
                 '进阶：含 unicode 字符时，==把数组换成哈希表==即可',
                 '题解另两种写法：`Counter(s) == Counter(t)`；两个 26 长数组分别计数再比较'],
    ),
)
