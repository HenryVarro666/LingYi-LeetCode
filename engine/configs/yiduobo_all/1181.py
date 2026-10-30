PH = ["writing code", "code rocks", "rocks the house", "house of cards"]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ph = S['phrases']
    n = len(ph)
    live = 'i' in S and 'j' in S and S.get('_line', 0) >= 8
    i = S.get('i') if live else None
    j = S.get('j') if live else None
    cv.text((x0 + 18, y0 + 4), 'phrases：蓝 = i（取它的最后一个词），粉 = j（取它的第一个词）', 24, T['muted'], bold=True)
    rh = min(70, (y1 - y0 - 60) / n)
    for k, p in enumerate(ph):
        y = y0 + 52 + k * rh
        c = None
        if k == i and k == j:
            c = T['purple']
        elif k == i:
            c = T['blue']
        elif k == j:
            c = T['pink']
        cv.rect((x0 + 18, y, x1 - 18, y + rh - 8), fill=(30, 36, 46), outline=c, width=3 if c else 1, r=10)
        cv.text((x0 + 36, y + (rh - 8) / 2), k, 26, T['dim'], anchor='lm', mono=True)
        words = p.split(' ')
        x = x0 + 90
        for w_idx, w in enumerate(words):
            col = T['text']
            if w_idx == len(words) - 1 and k == i:
                col = T['blue']
            if w_idx == 0 and k == j:
                col = T['pink']
            cv.text((x, y + (rh - 8) / 2), w, 30, col, anchor='lm', bold=(col != T['text']))
            x += cv.tlen(w + ' ', 30, bold=(col != T['text']))
        tag = ''
        if k == i:
            tag += 'i '
        if k == j:
            tag += 'j'
        if tag:
            cv.text((x1 - 36, y + (rh - 8) / 2), tag, 24, c, anchor='rm', bold=True)


def _res_txt(S):
    r = S.get('res')
    if r is None:
        return '两两枚举 `(i, j)`：`i` 的最后一个词 == `j` 的第一个词，就能拼起来'
    return f'已拼出 `{len(r)}` 个不同的结果（集合自动去重）'


def _last(S, B, ret):
    a, b = S.parts_list[S.i][-1], S.parts_list[S.j][0]
    if a != b:
        return f"`i` 的末词 `'{a}'` ≠ `j` 的首词 `'{b}'` → 接不上，跳过"
    return f"`i` 的末词 `'{a}'` == `j` 的首词 `'{b}'` → ==能接起来=="


CONFIG = dict(
    num=1181, title='前后拼接', difficulty='Medium', category='字符串',
    author='yiduobo', technique='两两枚举 · 集合去重',
    code='''
class Solution(object):
    def beforeAndAfterPuzzles(self, phrases):

        n = len(phrases)
        parts_list = [s.split(' ') for s in phrases]
        res = set()
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                
                if parts_list[i][-1] != parts_list[j][0]:
                    continue
                
                res.add(' '.join(parts_list[i] + parts_list[j][1:]))
        
        return sorted(list(res))
''',
    call=f'Solution().beforeAndAfterPuzzles({PH!r})',
    expect=['code rocks the house', 'rocks the house of cards', 'writing code rocks'],
    views=[
        dict(type='text', fn=_res_txt, h=60, size=26),
        dict(type='custom', draw=_draw, h=330),
        dict(type='set', var='res', label='res（黄 = 刚加入的结果）', fmt=lambda x: x, font=26, h=230),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('n', 'n')],
    skip=['n = len', 'parts_list =', 'continue'],
    max_steps=75,
    captions={
        'res = set()': '用集合 `res` 存拼接结果，==自动去重==',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：把 `phrases[{S.i}]` 放在前面' if S.get('i') != B.get('i')
                                           else '`i` 都枚举完了，开始整理答案'),
        'for j in range': lambda S, B, r: (f'`j = {S.j}`：把 `phrases[{S.j}]` 放在后面' if B.get('j') != S.j
                                           else f'`j` 枚举完了，`i = {S.i}` 的这一轮结束'),
        'if i == j': lambda S, B, r: ('`i == j`：同一个短语不能自己接自己 → 跳过' if S.i == S.j
                                      else f'`i = {S.i} ≠ j = {S.j}`，可以考虑'),
        'if parts_list[i][-1]': _last,
        'res.add': "拼接：`i` 的全部单词 + `j` 去掉第一个词 → `'{' '.join(parts_list[i] + parts_list[j][1:])}'`",
        'return sorted': '集合里一共 `{len(res)}` 个结果，==按字典序排序==后返回',
    },
    cards=dict(
        one_liner='数据规模小，直接两两枚举，用集合去重再排序',
        complexity='时间 `O(n² · L)`，空间 `O(n · L)`，`L` 为短语长度',
        problem=['给定短语列表 `phrases`，每个短语由小写字母和空格组成',
                 '若 `A` 的==最后一个单词==等于 `B` 的==第一个单词==，可拼成 `A + B[第一个词之后]`',
                 '返回所有不同的拼接结果（字典序）',
                 '本视频：`["writing code", "code rocks", "rocks the house", "house of cards"]`'],
        quote='没有什么特别好的思路，不过好在数据规模不大，因此可以直接两两枚举字符串，使用集合储存拼接后的结果，最终集合的大小就是最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个短语按空格切成单词列表 `parts_list`',
              '枚举有序对 `(i, j)`，`i != j`，比较 `i` 的末词和 `j` 的首词',
              '相等就拼接加入 `res`，集合去掉重复结果'],
        summary=['时间 `O(n² · L)`，空间 `O(n · L)`',
                 '易错：`i == j` 要跳过，短语不能和自己拼接',
                 '拼接时 `j` 要去掉第一个词（`parts_list[j][1:]`），否则公共词重复',
                 '不同的 `(i, j)` 可能拼出同一个字符串，所以用 `set` 去重'],
    ),
)
