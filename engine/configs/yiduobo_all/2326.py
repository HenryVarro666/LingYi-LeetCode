M, N = 3, 4
VALS = [1, 2, 3, 4, 5, 6, 7]


def _bad(S):
    return S['nowx'] < 0 or S['nowx'] == S['m'] or S['nowy'] < 0 or S['nowy'] == S['n'] or S['res'][S['nowx']][S['nowy']] != -1


CONFIG = dict(
    num=2326, title='螺旋矩阵 IV', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 先走一步，不合法就退回并转向',
    code='''
class Solution(object):
    def spiralMatrix(self, m, n, head):

        res = [[-1] * n for _ in range(m)]
        now = head
        nowx, nowy = 0, 0
        nowd = 0

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        while now:
            res[nowx][nowy] = now.val
            now = now.next
            if not now:
                break
            nowx += dx[nowd]
            nowy += dy[nowd]
            while nowx < 0 or nowx == m or nowy < 0 or nowy == n or res[nowx][nowy] != -1:
                nowx -= dx[nowd]
                nowy -= dy[nowd]
                nowd = (nowd + 1) % 4
                nowx += dx[nowd]
                nowy += dy[nowd]
        
        return res
''',
    call=f'Solution().spiralMatrix({M}, {N}, L({VALS}))',
    expect=[[1, 2, 3, 4], [-1, -1, -1, 5], [-1, -1, 7, 6]],
    skip=['dx = [0', 'dy = [1', 'nowx, nowy = 0, 0', 'nowd = 0'],
    views=[
        dict(type='linked', label='链表（蓝 = 下一个要填的节点 now）', pointers={'now': 'blue'}, h=170),
        dict(type='grid', var='res', label='res（黄框 = 当前位置 (nowx, nowy)；-1 = 还没填）', cell=90, h=330,
             cursors=[('nowx', 'nowy', 'yellow', '')],
             color=lambda S, i, j, v: 'green' if v != -1 else None),
        dict(type='text', size=30, fn=lambda S: ('方向 `nowd = ' + str(S['nowd']) + '`：' + ('右', '下', '左', '上')[S['nowd']]) if 'nowd' in S and 'dx' in S else ''),
    ],
    watch=['nowx', 'nowy', ('nowd', 'nowd', 'orange')],
    captions={
        'res = [[-1]': '先造 `{m} × {n}` 的矩阵，全是 `-1`：既是空位的值，也表示「还没填过」',
        'now = head': '`now` 指向要填的当前节点，`nowx, nowy` 是填的位置，`nowd` 是方向',
        'dx = [0': '方向顺时针：右 `(0,1)` → 下 `(1,0)` → 左 `(0,-1)` → 上 `(-1,0)`，`nowd = 0` 表示向右',
        'while now:': lambda S, B, r: (f'`now` 是节点 `{S.now.val}` → 继续填' if S.now else '链表用完了'),
        'res[nowx][nowy] = now.val': '把节点值填入 `({nowx},{nowy})`：`res[{nowx}][{nowy}] = {res[nowx][nowy]}`',
        'now = now.next': '`now` 移到下一个节点',
        'if not now': lambda S, B, r: ('链表已经没有下一个节点了 → ==不用再找下一格==，直接 break' if not S.now else '还有下一个节点，继续找下一格'),
        'nowx += dx[nowd]': lambda S, B, r: (f'朝当前方向先走一步：`nowx` → {S.nowx}（还没确认合不合法）' if S._line == 17
                                             else f'按新方向再走：`nowx` → {S.nowx}'),
        'nowy += dy[nowd]': lambda S, B, r: (f'`nowy` → {S.nowy}，试探的位置是 `({S.nowx},{S.nowy})`，下面检查它合不合法' if S._line == 18
                                             else f'`nowy` → {S.nowy}，新位置 `({S.nowx},{S.nowy})`，回到 while 再检查一次'),
        'while nowx < 0': lambda S, B, r: (f'`({S.nowx},{S.nowy})` 越界' if (S.nowx < 0 or S.nowx == S.m or S.nowy < 0 or S.nowy == S.n)
                                           else (f'`({S.nowx},{S.nowy})` 已经填过 → 不合法' if S.res[S.nowx][S.nowy] != -1
                                                 else f'`({S.nowx},{S.nowy})` 在界内且是 -1 → 合法，不转向')) + ('，需要退回并转向' if _bad(S) else ''),
        'nowx -= dx[nowd]': '先==退回==刚才走的那一步，回到最后一个合法位置',
        'nowy -= dy[nowd]': '退回到 `({nowx},{nowy})`',
        'nowd = (nowd + 1) % 4': '顺时针转 90 度：`nowd = {nowd}`',
        'break': '没有下一个节点了，跳出循环',
        'return res': '链表填完，返回矩阵',
    },
    cards=dict(
        one_liner='先试着走一步，走不通就退回来、转个向再走',
        complexity='时间 `O(mn)`，空间 `O(1)`（不计返回的矩阵）',
        problem=['给 `m`、`n` 和一个链表，按==顺时针螺旋==从左上角填进 `m × n` 矩阵',
                 '多出来的格子填 `-1`',
                 '示例：`m = 3, n = 5, head = [3,0,2,6,8,1,7,9,4,2,5,5,0]`',
                 '本视频：`m = 3, n = 4, head = [1,2,3,4,5,6,7]`'],
        quote='若当前方向上的下一个单元格超出了矩阵边界，或者已经被填充过了，那么就将方向顺时针旋转90度，对应到代码上就是将当前d变为(d + 1) % 4。',
        quote_src='—— yiduobo 题解原文',
        idea=['先定义方向数组 `dx`、`dy`：右 → 下 → 左 → 上，循环',
              '填好一个格子、链表后移，然后朝当前方向先迈一步',
              '这一步越界或已填过 → 退回、`nowd` 转 90 度、再迈一步（外面是 `while`，可以连续转）'],
        summary=['时间 `O(mn)`，空间 `O(1)`（不计答案）',
                 '链表走完要立刻 `break`：否则会多迈一步，可能撞墙后误转向',
                 '「先走再检查，不行就退回转向」，所以转向那段有三行：退、转、进',
                 '对比灵神：灵神先==看==下一格行不行再动，不用退回；yiduobo 先动后退'],
    ),
)
