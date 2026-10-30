def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ds = S['details']
    inner = S.get('_inner', {})
    cur = inner.get('s')
    cv.text((x0 + 18, y0 + 4), 'details（黄 = 年龄 s[11:13]，绿 = 大于 60，橙 = 不大于）', 22, T['muted'], bold=True)
    cw, rh = 30, 78
    sx = x0 + 60
    yy = y0 + 60
    kc = len(ds)  # 单行生成器：一步里全部算完，直接展示每位乘客的判断
    for k, s in enumerate(ds):
        is_cur = k == kc
        done = k < kc
        age = int(s[11:13])
        Y = yy + k * rh
        cv.text((x0 + 24, Y + 20), k, 22, T['dim'], anchor='mm', mono=True)
        for c, ch in enumerate(s):
            X = sx + c * cw
            fill = T['panel2']
            if c in (11, 12):
                fill = T['yellow']
                if done or is_cur:
                    fill = T['green'] if age > 60 else T['orange']
            cv.rect((X + 1, Y, X + cw - 1, Y + 40), fill=fill, r=4)
            cv.text((X + cw / 2, Y + 20), ch, 22, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True, mono=True)
        if is_cur or done:
            cv.text((sx + 15 * cw + 20, Y + 20), f'{age} {">" if age > 60 else "≤"} 60', 26, T['green'] if age > 60 else T['muted'], anchor='lm', bold=True)
        if is_cur:
            cv.rect((sx - 4, Y - 4, sx + 15 * cw + 4, Y + 44), outline=T['blue'], width=3, r=6)


CONFIG = dict(
    num=2678, title='老人的数目', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='切片取年龄 · 生成器求和',
    tags=[],
    code='''
class Solution:
    def countSeniors(self, details: List[str]) -> int:
        return sum(int(s[11:13]) > 60 for s in details)
''',
    call='Solution().countSeniors(["7868190130M7522","5303914400F9211","9273338290F4010","1313579440F2036"])',
    expect=2,
    views=[dict(type='custom', draw=_draw, h=420)],
    watch=[('s', 's', 'blue')],
    captions={
        'return sum': lambda S, B, r: ('一行代码把所有乘客过一遍：年龄依次是 '
                                       + '、'.join(str(int(d[11:13])) for d in S.details)
                                       + f'，其中大于 60 的有 =={r}== 个 → 返回 {r}'),
    },
    cards=dict(
        before=[dict(heading='下标怎么数', lines=['手机号占下标 `0~9`，性别是 `s[10]`',
                                                 '年龄是 `s[11]` 和 `s[12]`，座位号是 `s[13]`、`s[14]`',
                                                 '切片 `s[11:13]` 左闭右开，刚好取到这两位'])],
        after=[dict(heading='生成器怎么数', lines=['`int(s[11:13]) > 60` 对每个乘客得到 `True` 或 `False`',
                                                 '`sum` 把 `True` 当 1、`False` 当 0 相加',
                                                 '所以不需要显式的计数变量和 if'])],
        one_liner='年龄就是 s[11] 和 s[12]，切片转整数和 60 比',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每个乘客信息是 15 位字符串：10 位手机号 + 1 位性别 + 2 位年龄 + 2 位座位号',
                 '统计年龄 ==严格大于 60== 的人数',
                 '示例：`["7868190130M7522","5303914400F9211","9273338290F4010"]` → `2`'],
        quote='遍历每个字符串 s，如果 s[11] 和 s[12] 组成的数字大于 60，则答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['手机号 10 位 + 性别 1 位，年龄从下标 `11` 开始，占两位',
              '`s[11:13]` 切出年龄，`int()` 转数字，和 60 比较',
              '布尔值 `True` 当 1 用，`sum` 直接数出个数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：切片左闭右开，年龄是 `s[11:13]` 不是 `s[11:12]`',
                 '是「严格大于」60，恰好 60 岁不算',
                 '本视频用 4 个乘客演示：75、92、40、20 岁 → 答案 2'],
    ),
)
