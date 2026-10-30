def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H, s = S['width'], S['height'], S['sideLength']
    cv.text((x0 + 18, y0 + 4), f'{W}×{H} 矩阵，按 {s}×{s} 切分（蓝 = 整块正方形，橙 = 右侧条，紫 = 下方条，粉 = 角落）', 22, T['muted'], bold=True)
    cell = min(80, (x1 - x0 - 60) / W, (y1 - y0 - 110) / H)
    sx = x0 + ((x1 - x0) - cell * W) / 2
    sy = y0 + 96
    nn, mm = H // s, W // s
    for i in range(H):
        for j in range(W):
            inr, inb = j >= mm * s, i >= nn * s
            if inr and inb:
                c = T['pink']
            elif inr:
                c = T['orange']
            elif inb:
                c = T['purple']
            else:
                c = T['blue']
            cv.rect((sx + j * cell + 2, sy + i * cell + 2, sx + (j + 1) * cell - 2, sy + (i + 1) * cell - 2), fill=c, alpha=110, r=6)
    # block borders
    for bi in range(nn):
        for bj in range(mm):
            cv.rect((sx + bj * s * cell, sy + bi * s * cell, sx + (bj + 1) * s * cell, sy + (bi + 1) * s * cell), outline=T['text'], width=3)
    cv.text((x0 + 18, y0 + 40),
            f'整块 m×n = {mm}×{nn} 个；右侧宽 w = {S["w"]}；下方高 h = {S["h"]}', 22, T['text'], bold=True)


CONFIG = dict(
    num=1183, title='矩阵中1的最大数量', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='分块 · 先填重叠最多的位置',
    tags=[],
    code='''
class Solution(object):
    def maximumNumberOfOnes(self, width, height, sideLength, maxOnes):

        m = width // sideLength
        w = width % sideLength

        n = height // sideLength
        h = height % sideLength

        res = m * n * maxOnes

        if h * w >= maxOnes:
            res += (m + n + 1) * maxOnes
        else:
            res += (m + n + 1) * (w * h)
            maxOnes -= w * h
            if m < n:
                if (sideLength - h) * w >= maxOnes:
                    res += n * maxOnes
                else:
                    res += n * (sideLength - h) * w
                    maxOnes -= (sideLength - h) * w
                    if (sideLength - w) * h >= maxOnes:
                        res += m * maxOnes
                    else:
                        res += m * (sideLength - w) * h
            
            else:
                if (sideLength - w) * h >= maxOnes:
                    res += m * maxOnes
                else:
                    res += m * (sideLength - w) * h
                    maxOnes -= (sideLength - w) * h
                    if (sideLength - h) * w >= maxOnes:
                        res += n * maxOnes
                    else:
                        res += n * (sideLength - h) * w
        
        return res
''',
    call='Solution().maximumNumberOfOnes(5, 5, 3, 5)',
    expect=18,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=lambda S: (f'已累计 res = =={S["res"]}==，还剩可用的 1：`maxOnes = {S["maxOnes"]}`') if 'res' in S else '', size=26, h=70),
    ],
    watch=[('m', 'm', 'blue'), ('w', 'w', 'orange'), ('n', 'n', 'blue'), ('h', 'h', 'purple'),
           ('maxOnes', 'maxOnes', 'yellow'), ('res', 'res', 'green')],
    captions={
        'm = width': '横向能放下 `m = {m}` 个整块，剩余宽度 `w = {width} % {sideLength} = {w}`',
        'n = height': '纵向能放下 `n = {n}` 个整块，剩余高度 `h = {height} % {sideLength} = {h}`',
        'res = m * n * maxOnes': '每个整块里恰好放满 `{maxOnes}` 个 1，先累加：`{m} × {n} × {maxOnes}` = =={res}==',
        'if h * w >= maxOnes': '角落 `h×w = {h*w}` 个格子，和右侧条、下方条共享位置，最优先填。够放 `maxOnes = {maxOnes}` 吗？{"够" if h*w >= maxOnes else "不够"}',
        'res += (m + n + 1) * maxOnes': '角落位置够用：这 `m+n+1 = {m+n+1}` 个矩形各放 `maxOnes` 个 1 → res = =={res}==',
        'res += (m + n + 1) * (w * h)': '角落位置不够，全部填满：`{m+n+1} × {w*h}`，res = =={res}==',
        'maxOnes -= w * h': '角落用掉 `{w*h}` 个 1，还剩 `maxOnes = {maxOnes}`',
        'if m < n': '`m = {m}`，`n = {n}`：右侧条有 n 个、下方条有 m 个，==个数多的先填==，更赚。{"n 更多：先填右侧" if m < n else "m 不小于 n：先填下方"}',
        'if (sideLength - h) * w >= maxOnes': '右侧条（宽 w，高 s−h）共 `{(sideLength-h)*w}` 格，剩 `{maxOnes}` 个 1 → {"放得下" if (sideLength-h)*w >= maxOnes else "放不下"}',
        'if (sideLength - w) * h >= maxOnes': '下方条（宽 s−w，高 h）共 `{(sideLength-w)*h}` 格，剩 `{maxOnes}` 个 1 → {"放得下" if (sideLength-w)*h >= maxOnes else "放不下"}',
        'res += n * maxOnes': '右侧 n 个条各放 `maxOnes` 个 → res = =={res}==，1 用完',
        'res += m * maxOnes': '下方 m 个条各放 `maxOnes` 个 → res = =={res}==，1 用完',
        'res += n * (sideLength - h) * w': '右侧条全部填满：`{n} × {(sideLength-h)*w}` → res = =={res}==',
        'res += m * (sideLength - w) * h': '下方条全部填满：`{m} × {(sideLength-w)*h}` → res = =={res}==',
        'maxOnes -= (sideLength - h) * w': '右侧条用掉 `{(sideLength-h)*w}` 个，还剩 `maxOnes = {maxOnes}`',
        'maxOnes -= (sideLength - w) * h': '下方条用掉 `{(sideLength-w)*h}` 个，还剩 `maxOnes = {maxOnes}`',
        'return res': '最多放 `{res}` 个 1',
    },
    cards=dict(
        one_liner='先切出 s×s 整块，再把 1 填在被覆盖最多的位置',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`width × height` 的矩阵，每个格子填 0 或 1',
                 '任意 `sideLength × sideLength` 的正方形里至多 `maxOnes` 个 1',
                 '求整个矩阵里 1 的最大数量',
                 '本视频：`5, 5, 3, 5` → `18`'],
        quote='直接设计填充方案是比较困难的，不妨先进行一些分割。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左上角切出 `m×n` 个整块，每块恰好放 `maxOnes` 个 1',
              '剩下角落、右侧条、下方条的位置会被更多正方形覆盖，同一位置模 s 相同',
              '角落最优先；再看 n 和 m 谁大，个数多的条先填'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：m<n 时先填右侧条（有 n 个），否则先填下方条（有 m 个）',
                 '每种矩形处理时都要判断 1 够不够，不够就按 `maxOnes` 收尾返回',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
