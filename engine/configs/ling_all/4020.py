def _legs(S):
    r = S['requests']
    return [0] + list(r)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    r = S['requests']
    pts = [0] + list(r)
    n = S['n']
    cv.text((x0 + 18, y0 + 4), '电梯轨迹（横轴 = 第几个请求，纵轴 = 楼层）', 24, T['muted'], bold=True)
    left, right = x0 + 70, x1 - 40
    top, base = y0 + 70, y1 - 50
    dx = (right - left) / max(1, len(pts) - 1)
    fy = lambda f: base - (base - top) * f / max(1, n - 1)
    for f in range(n):
        cv.line([(left, fy(f)), (right, fy(f))], T['border'], 1)
        cv.text((left - 12, fy(f)), f, 22, T['dim'], anchor='rm', mono=True)
    xy = [(left + i * dx, fy(p)) for i, p in enumerate(pts)]
    for i in range(1, len(pts)):
        d = abs(pts[i] - pts[i - 1])
        c = T['green'] if d else T['dim']
        cv.line([xy[i - 1], xy[i]], c, 5)
        mx, my = (xy[i - 1][0] + xy[i][0]) / 2, (xy[i - 1][1] + xy[i][1]) / 2
        cv.text((mx + 8, my - 22), f'{d}秒', 24, T['yellow'] if d else T['dim'], anchor='mm', bold=True)
    for i, (px, py) in enumerate(xy):
        cv.rect((px - 12, py - 12, px + 12, py + 12), fill=T['blue'] if i else T['orange'], r=12)
        cv.text((px, py + 24), '起点' if i == 0 else f'r{i - 1}', 20, T['muted'], anchor='mt', mono=True)


CONFIG = dict(
    num=4020, title='电梯请求 I', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='相邻差的绝对值之和',
    tags=[],
    code='''
class Solution:
    def elevatorRequests(self, n: int, requests: list[int]) -> int:
        return requests[0] + sum(abs(x - y) for x, y in pairwise(requests))
''',
    call='Solution().elevatorRequests(8, [2, 1, 4, 3, 3, 7, 0])',
    expect=2 + 1 + 3 + 1 + 0 + 4 + 7,
    views=[
        dict(type='array', var='requests', label='requests（电梯按顺序去这些楼层）', cell=84, h=150),
        dict(type='custom', draw=_draw, h=430),
        dict(type='text', size=28, h=70,
             fn=lambda S: '总时间 = `requests[0]`（从 0 层出发） + 每相邻两次请求的 `|x − y|`'),
    ],
    watch=[('requests[0]', lambda S: S['requests'][0], 'orange'), ('n', 'n')],
    captions={
        'return requests[0]': lambda S, B, ret: (
            '先加 `requests[0] = %d`：电梯从 0 层出发，去第一个请求楼层要 %d 秒；'
            '再把每对相邻请求的楼层差 `|x − y|` 全部加起来' % (S.requests[0], S.requests[0])
            if ret is None else
            '`%d` + `%s` = ==%d==' % (
                S.requests[0],
                ' + '.join(str(abs(a - b)) for a, b in zip(S.requests, S.requests[1:])), ret)),
    },
    cards=dict(
        before=[dict(heading='先手算一遍', lines=['`[2,1,4,3,3,7,0]`，起点 0 层',
                                                   '`0→2` 2 秒，`2→1` 1 秒，`1→4` 3 秒，`4→3` 1 秒',
                                                   '`3→3` 0 秒，`3→7` 4 秒，`7→0` 7 秒',
                                                   '每一段都是 ==两层楼号之差的绝对值==，全部相加 = 18'])],
        one_liner='总时间 = 第一个请求的楼层 + 相邻请求楼层差的绝对值之和',
        complexity='时间 `O(m)`，空间 `O(1)`',
        problem=['电梯从 0 层出发，每秒走一层，按顺序处理 `requests` 里的楼层',
                 '求处理完所有请求的总秒数',
                 '示例：`n = 5, requests = [2,1,4,3]` → `7`',
                 '本视频：`[2,1,4,3,3,7,0]` → `18`'],
        quote='根据题意，答案为 requests 相邻元素的绝对差之和，加上 requests[0]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两层之间走一趟的时间就是楼层差的绝对值',
              '起点在 0 层，所以第一段是 `|requests[0] - 0| = requests[0]`',
              '`pairwise` 依次给出相邻的 `(x, y)`，一行写完'],
        after=[dict(heading='为什么能一行写完', lines=['`pairwise(requests)` 依次给出 `(2,1) (1,4) (4,3) ...`',
                                                        '`abs(x - y)` 就是这一段的耗时，`sum` 把它们加起来',
                                                        '起点 0 层单独用 `requests[0]` 补上'])],
        summary=['时间 `O(m)`，`m` 是 `requests` 的长度；空间 `O(1)`',
                 '别漏掉起点：电梯初始在 0 层，要加 `requests[0]`',
                 '相邻请求同一层时 `|x - y| = 0`，自然不耗时',
                 '参数 `n`（楼层数）在解法里用不上'],
    ),
)
