def _top(S):
    if 'f' not in S:
        return ''
    return f"`cnt = {S['cnt']}`：已扫过的小球个数；`f[p]`：左侧球移到 p 的代价"


CONFIG = dict(
    num=1769, title='移动所有球到每个盒子所需的最小操作数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='左右两遍递推 f[p]=f[p-1]+cnt',
    code='''
class Solution(object):
    def minOperations(self, boxes):

        n = len(boxes)

        f = [0]
        if boxes[0] == '1':
            cnt = 1
        else:
            cnt = 0
        for index in range(1, n):
            f.append(f[-1] + cnt)
            if boxes[index] == '1':
                cnt += 1
        
        g = [0]
        if boxes[-1] == '1':
            cnt = 1
        else:
            cnt = 0
        for index in range(n - 2, -1, -1):
            g.append(g[-1] + cnt)
            if boxes[index] == '1':
                cnt += 1
        g.reverse()
        
        return [f[index] + g[index] for index in range(n)]
''',
    call='Solution().minOperations("11010")',
    expect=[4, 3, 4, 5, 8],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='boxes', label='boxes（1 = 有球）', cell=84, pointers={'index': 'pink'},
             color=lambda S, i, v: 'yellow' if v == '1' else None),
        dict(type='array', var='f', label='f[p]：p 左侧的球移到 p 的操作数', cell=84, color=lambda S, i, v: 'blue'),
        dict(type='array', var='g', label='g[p]：p 右侧的球移到 p 的操作数（先倒序算，最后 reverse）', cell=84, color=lambda S, i, v: 'orange'),
    ],
    watch=[('index', 'index', 'pink'), ('cnt', 'cnt', 'yellow')],
    captions={
        'n = len': '`n = {n}`',
        'f = [0]': '`f[0] = 0`：第 0 个盒子左边没有球',
        "if boxes[0] == '1'": '`cnt` 记录「已扫过的盒子里球的个数」，先看第 0 个盒子',
        'cnt = 1': '第 0 个盒子有球 → `cnt = 1`',
        'cnt = 0': '这个盒子没球 → `cnt = 0`',
        'for index in range(1, n)': '算 `f[{index}]`：左侧球先到 `{index-1}`，再整体挪一步',
        'f.append': '`f[p] = f[p-1] + cnt[p-1]` = ==`{f[-2]} + {cnt}`== = {f[-1]}：每个球都多走一步',
        "boxes[index] == '1'": lambda S, B, r: ("这个盒子有球 → 之后的盒子左边多一个球" if S.boxes[S.index] == '1'
                                                else '这个盒子没球，`cnt` 不变'),
        'cnt += 1': '`cnt` → {cnt}',
        'g = [0]': '`g` 同理从右往左算（镜像），最右盒子右边没有球：`g = [0]`',
        "boxes[-1] == '1'": '最后一个盒子有球吗？先初始化 `cnt`',
        'for index in range(n - 2': '算右侧：下标 `{index}`，把右边的球往左挪一步',
        'g.append': '`g[-1] + cnt` → `{g}`（此时 g 还是倒序存放）',
        'g.reverse': '`g` 是从右往左存的，反转后 `g[p]` 就对应盒子 p：`{g}`',
        'return [': lambda S, B, ret: f'每个盒子 `f[p] + g[p]` = {ret}',
    },
    cards=dict(
        one_liner='左边的球先挪到 p-1 再整体挪一步，用上一个位置的结果',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`boxes` 的第 i 个字符为 `1` 表示盒子 i 有一个球，每次只能把球移到相邻盒子',
                 '对每个盒子 p，求把所有球移到 p 的最少操作数',
                 '示例：`"110"` → `[1,1,3]`；本视频：`"11010"`'],
        quote='将p左侧小球移动到p的过程分两步走。首先将这些小球全部移动到p - 1这个位置，然后将这些球连同原来就在p - 1这个位置上的球移动到p。……f[p] = f[p - 1] + cnt[p - 1]',
        quote_src='—— yiduobo 题解原文',
        idea=['只能走相邻格，所以 p 左边的球都要经过 p-1 才能到 p',
              '`f[p] = f[p-1] + cnt[p-1]`：先花 `f[p-1]` 挪到 p-1，再让 p-1 及之前的 `cnt` 个球各走一步',
              '右边是镜像：从右往左算出 `g`；答案 `f[p] + g[p]`'],
        summary=['时间 `O(n)`，空间 `O(n)`；数据小也可以 `O(n^2)` 暴力枚举',
                 '易错：`g` 是从右往左 append 的，要 `reverse()` 后才和下标对齐',
                 '易错：`cnt` 要在 `append` 之后才加上当前盒子，否则会多算一步',
                 '原文为 Python 2 风格，代码无需改动；题面由简报缺失，按 LeetCode 1769 题意编写'],
    ),
)
