WORDS = ['hey', 'aeo', 'mu', 'ooo', 'artro']
LEFT, RIGHT = 1, 4


def _cur(S):
    w = S.get('w')
    if w is None or w not in WORDS:
        return None
    return WORDS.index(w)                                 # 示例里的单词互不相同


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '当前单词 w：首、尾字符是否都在 vowel_set 中', 24, T['muted'], bold=True)
    w = S.get('w')
    vs = S.get('vowel_set')
    if w is None or vs is None:
        if vs is not None:
            cv.rich(x0 + 40, y0 + 60, f'`vowel_set = {{{", ".join(sorted(vs))}}}`', x1 - x0 - 80, size=28)
        return
    L = len(w)
    cw = 76
    sx = x0 + 40
    y = y0 + 54
    for k, ch in enumerate(w):
        edge = k == 0 or k == L - 1
        fill = (T['green'] if ch in vs else T['red']) if edge else T['panel2']
        cv.rect((sx + k * cw, y, sx + k * cw + cw - 8, y + 70), fill=fill, r=10)
        cv.text((sx + k * cw + (cw - 8) / 2, y + 35), ch, 34, T['bg'] if edge else T['text'], anchor='mm', bold=True, mono=True)
    cv.text((sx, y + 82), 'w[0]', 20, T['muted'], mono=True)
    cv.text((sx + (L - 1) * cw + (cw - 8), y + 82), 'w[-1]', 20, T['muted'], anchor='ra', mono=True)
    a, b = w[0] in vs, w[-1] in vs
    rx = sx + max(L, 3) * cw + 50
    cv.rich(rx, y + 2, f"`'{w[0]}' in vowel_set` → " + ('==True==' if a else 'False'), x1 - rx - 10, size=26)
    cv.rich(rx, y + 46, f"`'{w[-1]}' in vowel_set` → " + ('==True==' if b else 'False'), x1 - rx - 10, size=26)
    cv.rich(x0 + 40, y + 130, '两个都是元音 → `res += 1`' if a and b else '有一个不是元音 → 不计数', x1 - x0 - 80, size=26,
            color=T['text'] if a and b else T['muted'])


CONFIG = dict(
    num=2586, title='统计范围内的元音字符串数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='枚举区间 · 元音集合判首尾',
    tags=['List.md'],
    code='''
class Solution(object):
    def vowelStrings(self, words, left, right):
        vowel_set = set(['a', 'e', 'i', 'o', 'u'])
        res = 0
        for w in words[left : right + 1]:
            if w[0] in vowel_set and w[-1] in vowel_set:
                res += 1

        return res
''',
    call=f'Solution().vowelStrings({WORDS}, {LEFT}, {RIGHT})',
    expect=3,
    views=[
        dict(type='array', var='words', label='words（青框 = 区间 [left, right]，蓝 = 当前 w）', cell=150, h=270,
             window=('left', 'right'), pointers={_cur: 'blue'}, pointer_labels={_cur: 'w'},
             color=lambda S, i, v: 'blue' if i == _cur(S) else None,
             dim=lambda S, i, v: not (S['left'] <= i <= S['right'])),
        dict(type='custom', draw=_draw, h=260),
    ],
    watch=[('left', 'left'), ('right', 'right'), ('w', 'w', 'blue'), ('res', 'res', 'green')],
    captions={
        'vowel_set = set': '把 5 个元音放进集合 `vowel_set`，判断 `in` 只要 `O(1)`',
        'res = 0': '`res` 统计元音字符串个数',
        'for w in words[left : right + 1]': lambda S, B, ret: (
            f'枚举 `words[{S.left} : {S.right + 1}]` 中的 `w = "{S.w}"`' if S.get('w') != B.get('w') or 'w' not in B
            else '区间内的字符串枚举完了'),
        'if w[0] in vowel_set and w[-1] in vowel_set': lambda S, B, ret: (
            f'`"{S.w}"`：首字符 `{S.w[0]}`、尾字符 `{S.w[-1]}` ==都是元音==' if S.w[0] in S.vowel_set and S.w[-1] in S.vowel_set
            else (f'`"{S.w}"`：首字符 `{S.w[0]}` 不是元音（`and` 短路，尾字符不用看）' if S.w[0] not in S.vowel_set
                  else f'`"{S.w}"`：尾字符 `{S.w[-1]}` 不是元音')),
        'res += 1': '`res` → {res}',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='直接枚举 [l, r] 内的字符串，首尾字符都是元音就计数',
        complexity='时间 `O(r − l)`，空间 `O(1)`',
        problem=['==以元音开头并以元音结尾==的字符串叫元音字符串（元音：`a e i o u`）',
                 '统计 `words` 中下标在 `[left, right]` 内的元音字符串个数',
                 '示例：`words = ["are","amy","u"]`，`left = 0`，`right = 2` → `2`',
                 '本视频：`["hey","aeo","mu","ooo","artro"]`，`[1, 4]` → `3`'],
        quote='直接枚举范围[l, r]内的所有字符串，==检测当前字符串的首位字符是否都是元音字符==，若是，则更新答案。',
        quote_src='—— yiduobo 题解',
        idea=['元音放进集合 `vowel_set`，判断字符是否为元音只要 `O(1)`',
              '切片 `words[left : right + 1]` 正好是闭区间 `[left, right]`',
              '`w[0]` 是首字符，`w[-1]` 是尾字符'],
        result='`aeo`、`ooo`、`artro` 三个是元音字符串 → `3` ✓',
        summary=['时间 `O(r − l)`，每个字符串只看两个字符；空间 `O(1)`',
                 '易错：闭区间要写 `right + 1`；长度为 1 的串首尾是同一个字符',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：同样的思路，灵神用 `sum(...)` 一行写完'],
    ),
)
