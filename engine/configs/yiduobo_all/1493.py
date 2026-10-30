NUMS = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1]


def _draw(cv, S, B, box, T):
    """把 last_l、被删的 0、now_l 画成一排格子：合并后的长度 = last_l + now_l"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '两段连续 1 夹着一个 0：删掉这个 0，两段合并', 24, T['muted'], bold=True)
    if 'now_l' not in S or 'last_l' not in S:
        return
    last, now = S['last_l'], S['now_l']
    cells = [('cyan', 1)] * last + [('red', 0)] + [('orange', 1)] * now
    n = len(cells)
    cell = min(80, (x1 - x0 - 60) / max(n, 1))
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    top = y0 + 70
    for k, (c, v) in enumerate(cells):
        X = sx + k * cell
        cv.rect((X + 4, top, X + cell - 4, top + cell - 8), fill=T[c], r=8, alpha=200 if v else 110)
        cv.text((X + cell / 2, top + (cell - 8) / 2), v, 30, T['bg'] if v else T['text'], anchor='mm', bold=True)
    mid = top + cell + 30
    if last:
        cv.text((sx + last * cell / 2, mid), f'last_l = {last}', 24, T['cyan'], anchor='mt', bold=True)
    cv.text((sx + last * cell + cell / 2, mid + 34), '删掉', 22, T['red'], anchor='mt', bold=True)
    if now:
        cv.text((sx + (last + 1) * cell + now * cell / 2, mid), f'now_l = {now}', 24, T['orange'], anchor='mt', bold=True)
    cv.text(((x0 + x1) / 2, mid + 80), f'合并后 last_l + now_l = {last + now}', 28, T['text'], anchor='mt', bold=True)


CONFIG = dict(
    num=1493, title='删掉一个元素以后全为 1 的最长子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟扫描 · 合并 0 两侧的连续 1',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def longestSubarray(self, nums):

        last_l = 0
        zero_flag = False
        now_l = 0
        res = 0
        for num in nums:
            if num == 1:
                now_l += 1
            else:
                zero_flag = True
                res = max(res, now_l + last_l)
                last_l = now_l
                now_l = 0

        res = max(res, now_l + last_l)
        if not zero_flag:
            res -= 1

        return res
''',
    call=f'Solution().longestSubarray({NUMS})',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=80,
             color=lambda S, i, v: 'red' if v == 0 else None),
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('num', 'num'), ('last_l', 'last_l', 'cyan'), ('now_l', 'now_l', 'orange'),
           ('zero_flag', 'zero_flag'), ('res', 'res', 'green')],
    captions={
        'last_l = 0': '`last_l`：翻过一个 0 之前那一段连续 1 的长度',
        'zero_flag = False': '`zero_flag`：数组里有没有 0',
        6: '`now_l`：当前这一段连续 1 的长度',
        'res = 0': '`res` 记录答案',
        'for num in nums': '读入下一个数（读完就结束）',
        'if num == 1': lambda S, B, r: ('`num = 1`：当前这段连续 1 变长' if S.num == 1
                                        else '`num = 0`：当前这段连续 1 ==结束了=='),
        'now_l += 1': '`now_l` → {now_l}',
        'zero_flag = True': '记下：数组里有 0',
        13: '删掉这个 0，前后两段合并：`{B.now_l} + {last_l}` → `res = {res}`',
        'last_l = now_l': '当前段变成“上一段”：`last_l = {last_l}`',
        15: '新的一段从 0 开始：`now_l = 0`',
        17: '数组可能以 1 结尾，最后一段也要合并：`{now_l} + {last_l}` → `res = {res}`',
        'if not zero_flag': lambda S, B, r: ('数组里有 0，删的是 0，不用减' if S.zero_flag
                                             else '数组全是 1：==必须删一个 1==，答案减 1'),
        'res -= 1': '`res` → {res}',
        'return res': '答案 =={res}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='删一个 0，把它两侧的连续 1 拼起来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制数组 `nums` ==必须删掉一个元素==，求删除后最长的全 1 子数组长度',
                 '示例：`[0,1,1,1,0,1,1,0,1]` → `5`；`[1,1,1]` → `2`',
                 '本视频：`[1,1,0,1,1,1,0,0,1,1]` → `5`'],
        quote='为了使得答案尽量长，显然应该删去一个0，而删去这个0会使得0前后两段连续的1被合并为一段。',
        quote_src='—— yiduobo 题解原文',
        idea=['特殊情况：全是 1 时只能删一个 1，答案 `n − 1`',
              '遇到 1：`now_l += 1`；遇到 0：用 `now_l + last_l` 更新答案，再 `last_l = now_l, now_l = 0`',
              '扫描结束后最后一段还要再合并一次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：循环外还要用 `now_l + last_l` 更新一次（数组以 1 结尾）',
                 '易错：全 1 时要 `res -= 1`，用 `zero_flag` 区分',
                 '原文的 Python 2 风格代码可直接在 Python 3 运行，未做改动',
                 '对比灵神：灵神用“至多一个 0”的滑动窗口，答案取 `right − left`'],
    ),
)
