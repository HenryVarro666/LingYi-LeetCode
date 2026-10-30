def _color(S, i, j, v):
    if v is None:
        return None
    I = S['_inner']
    if 'rx' in I and 'j' in I and (i, j) == (I['rx'] + I['i'], I['ry'] - I['j']):
        return 'yellow'
    return 'green'


def _top(S):
    pl, d = S.get('part_length'), S.get('diff')
    if pl is None:
        return '右上角先放 `0`，然后一圈一圈往外「顺时针」扩成 2 倍大'
    I = S['_inner']
    if 'rx' in I:
        return f'已填好的 `{pl}×{pl}` 右上角块，整体加 `{I["diff"]}` 后抄到 `({I["rx"]}, {I["ry"]})` 为右上角的位置'
    return f'已填好的块边长 `part_length = {pl}`，每个数加的基准差 `diff = {d}`'


CONFIG = dict(
    num=3537, title='填充特殊网格', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='递推 · 右上角逐圈倍增',
    tags=['灵神题单·链表树与回溯', '难度分 1542'],
    code='''
class Solution(object):
    def specialGrid(self, n):
        
        m = 1 << n
        res = [[None] * m for _ in range(m)]
        res[0][m - 1] = 0

        def fill(rx, ry, length, diff):
            for i in range(length):
                for j in range(length):
                    res[rx + i][ry - j] = res[i][m - 1 - j] + diff

        part_length = 1
        diff = 1
        for index in range(n):
            fill(part_length, m - 1, part_length, diff)
            fill(part_length, m - 1 - part_length, part_length, diff * 2)
            fill(0, m - 1 - part_length, part_length, diff * 3)

            part_length <<= 1
            diff <<= 2
        
        return res
''',
    call='Solution().specialGrid(2)',
    expect=[[15, 12, 3, 0], [14, 13, 2, 1], [11, 8, 7, 4], [10, 9, 6, 5]],
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='grid', var='res', label='res（绿 = 已填好，黄框 = 这一步新写入，蓝框 = 被抄的源格子）', cell=100, h=440, color=_color,
             cursors=[(lambda S: S['_inner'].get('i') if 'j' in S['_inner'] else None, lambda S: S['m'] - 1 - S['_inner']['j'] if 'j' in S['_inner'] else None, 'blue')]),
        dict(type='text', fn=lambda S: '顺时针依次放：右上 `+0`、右下 `+diff`、左下 `+2·diff`、左上 `+3·diff`' if 'part_length' in S else '', size=22, h=50),
    ],
    watch=[('m', 'm'), ('part_length', 'part_length', 'cyan'), ('diff', 'diff', 'pink'),
           ('rx', lambda S: S['_inner'].get('rx'), 'blue'), ('ry', lambda S: S['_inner'].get('ry'), 'yellow')],
    skip=['for i in range(length)', 'for j in range(length)', 'def fill', '_ in range(m)'],
    max_steps=75,
    captions={
        'm = 1 <<': '边长 `m = 2^n = {m}`',
        'res = [[None]': '建一个 `{m}×{m}` 的空矩阵',
        'res[0][m - 1] = 0': '==右上角放 0==：这是最小的 1×1 块',
        'part_length = 1': '`part_length` 是已填好的右上角块的边长',
        'diff = 1': '`diff` = 已填块里的数字个数（块边长的平方），新块要整体加它的倍数',
        'for index in range(n)': lambda S, B, r: (f'已经铺满 `{S.m}×{S.m}`，循环结束' if S.part_length >= S.m else f'开始一轮：把 `{S.part_length}×{S.part_length}` 扩成 `{S.part_length * 2}×{S.part_length * 2}`'),
        'fill(part_length, m - 1, part_length, diff)': '==右下角块==：已有块整体 `+diff`，放到右上块的正下方',
        'fill(part_length, m - 1 - part_length, part_length, diff * 2)': '==左下角块==：已有块整体 `+2·diff`，放到右下块的左边',
        'fill(0, m - 1 - part_length, part_length, diff * 3)': '==左上角块==：已有块整体 `+3·diff`，放到右上块的左边（最大）',
        'res[rx + i][ry - j]': '`res[{rx + i}][{ry - j}] = res[{i}][{m - 1 - j}] + {diff}` = {res[i][m - 1 - j]} + {diff} = =={res[rx + i][ry - j]}==',
        'part_length <<= 1': '边长翻倍：`part_length` → `{part_length}`',
        'diff <<= 2': '数字个数变成 4 倍：`diff` → `{diff}`',
        'return res': '右上角的块不断倍增，直到铺满整个 `{m}×{m}`',
    },
    cards=dict(
        one_liner='从右上角的 0 出发，顺时针把已填块复制并加偏移，倍增铺满',
        complexity='时间 `O(4^n)`，空间 `O(1)`（不含返回值）',
        problem=['用 `0 ~ 2^2n - 1` 填满 `2^n × 2^n` 网格，右上 < 右下 < 左下 < 左上，且每个象限也满足同样规则',
                 '示例：`n = 1` → `[[3,0],[2,1]]`',
                 '本视频：`n = 2`，4×4 网格'],
        quote='除了递归外，本题反过来写递推也是可行的。首先在答案矩阵的右上角填充0，接下来对于当前已有的1 * 1的网格，将其加1、加2、加3的结果按照顺时针的顺序填充满答案矩阵右上角2 * 2的网格。',
        quote_src='—— yiduobo 题解原文',
        idea=['递归是「大块拆四份」，递推反过来：右上角的块「复制四份拼成更大的块」',
              '已有 `2^k × 2^k` 块，里面有 `2^2k` 个数，所以三份拷贝依次加 1、2、3 倍的 `2^2k`',
              '拷贝摆放顺时针：右下、左下、左上；每轮边长翻倍，`diff` 乘 4'],
        summary=['时间 `O(4^n)`：总共填写 `4^n` 个格子，每个只写一次',
                 '易错点：源始终是右上角那块，所以读的是 `res[i][m - 1 - j]`，写入的坐标是 `(rx + i, ry - j)`',
                 '三次 `fill` 的偏移是 `diff, 2·diff, 3·diff`，每轮结束 `diff <<= 2`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，无需其他修改',
                 '对比灵神：递归先右上再右下、左下、左上，递推则把这个顺序倒过来铺'],
    ),
)
