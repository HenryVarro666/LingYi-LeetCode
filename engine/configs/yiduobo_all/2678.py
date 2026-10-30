def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ds = S['details']
    cur = S.get('s')
    cv.text((x0 + 18, y0 + 4), 'details（黄 = 倒数第 4、3 位，绿 = 年龄 > 60，橙 = 不大于）', 22, T['muted'], bold=True)
    cw, rh = 30, 78
    sx = x0 + 60
    kc = ds.index(cur) if cur in ds else len(ds)
    line = S.get('_line', 0)
    for k, s in enumerate(ds):
        # 当前这一行（if 已判断后）才算结果
        is_cur = k == kc and cur is not None
        judged = k < kc or (is_cur and line >= 8)
        age = int(s[-4]) * 10 + int(s[-3])
        Y = y0 + 60 + k * rh
        cv.text((x0 + 24, Y + 20), k, 22, T['dim'], anchor='mm', mono=True)
        for c, ch in enumerate(s):
            X = sx + c * cw
            fill = T['panel2']
            if c in (11, 12):
                fill = T['yellow'] if is_cur or k > kc else T['panel2']
                if judged:
                    fill = T['green'] if age > 60 else T['orange']
                elif k > kc:
                    fill = T['panel2']
            cv.rect((X + 1, Y, X + cw - 1, Y + 40), fill=fill, r=4)
            cv.text((X + cw / 2, Y + 20), ch, 22, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
        if is_cur or judged:
            cv.text((sx + 15 * cw + 20, Y + 20), f'{age} {">" if age > 60 else "≤"} 60', 26,
                    T['green'] if age > 60 else T['muted'], anchor='lm', bold=True)
        if is_cur:
            cv.rect((sx - 4, Y - 4, sx + 15 * cw + 4, Y + 44), outline=T['blue'], width=3, r=6)


CONFIG = dict(
    num=2678, title='老人的数目', difficulty='Easy', category='字符串',
    author='yiduobo', technique='倒数下标取年龄',
    tags=[],
    code='''
class Solution(object):
    def countSeniors(self, details):

        res = 0
        for s in details:
            if int(s[-4]) * 10 + int(s[-3]) > 60:
                res += 1
        
        return res
''',
    call='Solution().countSeniors(["7868190130M7522","5303914400F9211","9273338290F4010","1313579440F2036"])',
    expect=2,
    views=[dict(type='custom', draw=_draw, h=420)],
    watch=[('s', 's', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计年龄大于 60 的人数',
        'for s in details': lambda S, B, r: (f'看下一位乘客 `{S.s}`' if S.s != B.get('s') or 's' not in B else '所有乘客都看完了'),
        'if int(s[-4])': lambda S, B, r: (f'倒数第 4 位 `{S.s[-4]}`、倒数第 3 位 `{S.s[-3]}` → 年龄 `{int(S.s[-4])*10+int(S.s[-3])}`，'
                                           + ('大于 60 → 是老人' if int(S.s[-4])*10+int(S.s[-3]) > 60 else '不大于 60 → 跳过')),
        'res += 1': '又找到一位老人：`res` → =={res}==',
        'return res': '老人一共 =={res}== 位',
    },
    cards=dict(
        one_liner='座位号占最后两位，年龄就是倒数第 4、3 位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每个乘客信息是 15 位字符串：手机号、性别、年龄（2 位）、座位号（2 位）',
                 '统计年龄 ==严格大于 60== 的人数',
                 '示例：`["7868190130M7522","5303914400F9211","9273338290F4010"]` → `2`'],
        quote='题目只关心乘客的年龄，因此只需提取乘客信息中的倒数第四位以及倒数第三位，计算出乘客的年龄并与60对比即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['年龄在座位号前面：`s[-4]` 是十位，`s[-3]` 是个位',
              '年龄 = `十位 × 10 + 个位`，不必管手机号有几位',
              '大于 60 就让 `res` 加 1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：倒数下标从 -1 开始数，座位号占 -2、-1，年龄是 -4、-3',
                 '是「严格大于」60，恰好 60 岁不算',
                 '对比灵神：灵神用正数切片 `s[11:13]`，yiduobo 用倒数下标',
                 '本视频用 4 个乘客演示，75、92、40、20 岁 → 答案 2'],
    ),
)
