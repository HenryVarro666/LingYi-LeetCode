def _done(S):
    if 'res' not in S:
        return 0
    cum, k = 0, 0
    pts = [0] + list(S['requests'])
    for i in range(1, len(pts)):
        cum += abs(pts[i] - pts[i - 1])
        if cum <= S['res'] and (cum < S['res'] or i == len(pts) - 1 or abs(pts[i + 1] - pts[i]) > 0 or True):
            k = i
    return k if S['res'] > 0 else 0


def _cur(S):
    return _done(S) - 1 if _done(S) > 0 else None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    r = S['requests']
    n = S['n']
    pts = [0] + list(r)
    cv.text((x0 + 18, y0 + 4), '电梯轨迹（绿 = 已走完，黄 = 这一步刚走的）', 24, T['muted'], bold=True)
    left, right = x0 + 70, x1 - 40
    top, base = y0 + 70, y1 - 50
    dx = (right - left) / max(1, len(pts) - 1)
    fy = lambda f: base - (base - top) * f / max(1, n - 1)
    for f in range(n):
        cv.line([(left, fy(f)), (right, fy(f))], T['border'], 1)
        cv.text((left - 12, fy(f)), f, 22, T['dim'], anchor='rm', mono=True)
    xy = [(left + i * dx, fy(p)) for i, p in enumerate(pts)]
    done = _done(S)
    for i in range(1, len(pts)):
        d = abs(pts[i] - pts[i - 1])
        c = T['border']
        if i <= done:
            c = T['yellow'] if i == done else T['green']
        cv.line([xy[i - 1], xy[i]], c, 5)
        mx, my = (xy[i - 1][0] + xy[i][0]) / 2, (xy[i - 1][1] + xy[i][1]) / 2
        if i <= done:
            cv.text((mx + 8, my - 22), f'{d}秒', 24, T['yellow'] if i == done else T['green'], anchor='mm', bold=True)
    for i, (px, py) in enumerate(xy):
        cv.rect((px - 12, py - 12, px + 12, py + 12), fill=T['orange'] if i == 0 else (T['blue'] if i <= done + 1 else T['dim']), r=12)
        cv.text((px, py + 24), '起点' if i == 0 else f'r{i - 1}', 20, T['muted'], anchor='mt', mono=True)


CONFIG = dict(
    num=4020, title='电梯请求 I', difficulty='Easy', category='模拟',
    author='yiduobo', technique='pre 记录上一层，累加差值',
    tags=[],
    code='''
class Solution(object):
    def elevatorRequests(self, n, requests):
        
        pre = 0
        res = 0
        for v in requests:
            res += abs(v - pre)
            pre = v
        
        return res
''',
    call='Solution().elevatorRequests(8, [2, 1, 4, 3, 3, 7, 0])',
    expect=18,
    views=[
        dict(type='array', var='requests', label='requests（箭头 = 刚处理完的请求）', cell=84, h=150,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'v'}),
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', size=28, h=70,
             fn=lambda S: f"`res += |v − pre|`：当前 `res = {S['res']}`" if 'res' in S else '电梯初始在 0 层，`pre = 0`'),
    ],
    watch=[('pre', 'pre', 'orange'), ('v', 'v', 'blue'), ('res', 'res', 'green')],
    captions={
        'pre = 0': '`pre` 记录电梯当前所在楼层，初始在 ==0 层==',
        'res = 0': '`res` 累计总秒数',
        'for v in requests': lambda S, B, ret: (f'下一个请求 `v = {S.v}`' if 'v' in S and ('v' not in B or True) else '请求处理完了'),
        'res += abs': '从 `{pre}` 层走到 `{v}` 层：`|{v} − {pre}| = {abs(v - pre)}` 秒 → `res = {res}`',
        'pre = v': '电梯停在 `{v}` 层，`pre = {pre}`；下一段从这里出发',
        'return res': '总时间 `{res}` 秒',
    },
    cards=dict(
        one_liner='用 pre 记住上一层，每个请求累加 |v − pre|',
        complexity='时间 `O(m)`，空间 `O(1)`',
        problem=['电梯在第 0 层，每秒移动一层，按顺序处理 `requests`',
                 '求处理完全部请求的总秒数',
                 '示例：`n = 5, requests = [2,1,4,3]` → `7`',
                 '本视频：`[2,1,4,3,3,7,0]` → `18`'],
        quote='需要计算的实际上就是request中相邻元素之差的和，于是可以使用pre记录上一个元素，初始值为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个请求的耗时 = 当前楼层与上一个楼层的差的绝对值',
              '`pre` 初始是 0（电梯在 0 层），这样第一个请求也不用特殊处理',
              '先累加 `abs(v - pre)`，再把 `pre` 更新成 `v`'],
        summary=['时间 `O(m)`，空间 `O(1)`',
                 '==先累加再更新 pre==，顺序反了差值恒为 0',
                 '相邻请求同一层时差为 0，不耗时',
                 '对比灵神：灵神用 `pairwise` 一行写完，再加 `requests[0]`；这里 `pre = 0` 自然包含起点',
                 '原文为 Python 2 风格（`class Solution(object)`），无需改动即可运行'],
    ),
)
