def _fh(x):
    return '[0]占位' if not x else f'{x[0]}×{x[1]}'


def _evt(S):
    if 'x' not in S:
        return '把每个建筑的左、右边界拆成事件：左边界记 `-高度`，右边界记 `+高度`'
    inner = S.get('_inner', {})
    h = inner.get('height')
    s = f"扫描到 x = =={S['x']}=="
    if h is not None and S.get('_line', 0) >= 17 and S.get('_line', 0) < 62:
        s += f"，当前事件 `{('左边界 加入 ' + str(-h)) if h < 0 else ('右边界 删去 ' + str(h))}`"
    return s


def _res(S):
    r = S.get('res')
    if r is None:
        return ''
    return '转折点 `res` = ==' + ('、'.join(f'({a},{b})' for a, b in r) if r else '（空）') + '=='


CONFIG = dict(
    num=218, title='天际线问题', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='扫描线 + 手写带计数的最大堆',
    tags=[],
    code='''
class Solution(object):    

    def getSkyline(self, buildings):

        height_dict = {}
        for left, right, height in buildings:
            if left not in height_dict:
                height_dict[left] = []
            if right not in height_dict:
                height_dict[right] = []

            height_dict[left].append(-height)
            height_dict[right].append(height)

        max_height = [[]]
        pos_dict = {}
        last_height = 0
        res = []

        for x in sorted(height_dict.keys()):
            for height in height_dict[x]:
                if height < 0:
                    height = -height
                    if height in pos_dict:
                        max_height[pos_dict[height]][1] += 1
                    else:
                        max_height.append([height, 1])
                        now = len(max_height) - 1
                        while now > 1 and height > max_height[now // 2][0]:
                            max_height[now] = max_height[now // 2]
                            pos_dict[max_height[now // 2][0]] = now
                            now //= 2
                        max_height[now] = [height, 1]
                        pos_dict[height] = now
                
                else:
                    pos = pos_dict[height]
                    max_height[pos][1] -= 1
                    if max_height[pos][1] == 0:
                        max_height[pos] = max_height[-1]
                        max_height.pop()
                        while True:
                            left = pos + pos
                            right = left + 1
                            left_flag = right_flag = False
                            if left < len(max_height) and max_height[pos][0] < max_height[left][0]:
                                left_flag = True
                            if right < len(max_height) and max_height[pos][0] < max_height[right][0]:
                                right_flag = True

                            if not left_flag:
                                if not right_flag:
                                    break
                                else:
                                    pos_dict[max_height[right][0]] = pos
                                    max_height[right], max_height[pos] = max_height[pos], max_height[right]
                                    pos = right
                            else:
                                if not right_flag or max_height[left][0] > max_height[right][0]:
                                    pos_dict[max_height[left][0]] = pos
                                    max_height[left], max_height[pos] = max_height[pos], max_height[left]
                                    pos = left
                                else:
                                    pos_dict[max_height[right][0]] = pos
                                    max_height[right], max_height[pos] = max_height[pos], max_height[right]
                                    pos = right

                        if pos < len(max_height):
                            pos_dict[max_height[pos][0]] = pos
                        pos_dict.pop(height)

            if len(max_height) == 1:
                now_height = 0
            else:
                now_height = max_height[1][0]

            if not res or res[-1][1] != now_height:
                res.append([x, now_height])

        return res
''',
    call='Solution().getSkyline([[2,9,10],[3,7,15]])',
    expect=[[2, 10], [3, 15], [7, 10], [9, 0]],
    views=[
        dict(type='text', fn=_evt, h=60),
        dict(type='heap', var='max_height', label='max_height（高度×个数）', fmt=_fh, top_color=None, h=150),
        dict(type='map', var='pos_dict', label='pos_dict（高度 → 在堆中的下标）', fmt=lambda k, v: f'{k} → {v}', h=100),
        dict(type='text', fn=_res, h=60),
    ],
    watch=[('x', 'x', 'blue'), ('height', 'height', 'orange'), ('now_height', 'now_height', 'green'), ('last_height', 'last_height', 'dim')],
    skip=['max_height = [[]]', 'pos_dict = {}', 'last_height = 0', 'left_flag = right_flag = False', 'pos_dict[max_height[now // 2][0]] = now', 'left_flag = True', 'if left not in height_dict', 'height_dict[left] = []', 'if right not in height_dict', 'height_dict[right] = []', 'for height in height_dict[x]', 'max_height.pop()', 'while True:', 'if not left_flag:', 'height = -height', 'now = len(max_height) - 1', 'res = []', 'right_flag = True', 'right = left + 1', 'left = pos + pos'],
    captions={
        'height_dict[left].append(-height)': '建筑的左边界 `x={left}` 记 `-{height}`（负数 = 要加入）',
        'height_dict[right].append(height)': '右边界 `x={right}` 记 `+{height}`（正数 = 要删去）',
        'res = []': '`res` 保存转折点；堆下标从 1 开始，`max_height[0]` 只是占位',
        'for x in sorted': '扫描 x = `{x}`：先把这个 x 上的==所有==边界事件处理完，再取堆顶',
        'for height in height_dict[x]': '先把 x = `{x}` 上的==所有==事件处理完，再取堆顶',
        'if height < 0': lambda S, B, r: ('负数 → 左边界：高度 `{}` 要加入堆'.format(-S.height) if S.height < 0
                                           else '正数 → 右边界：高度 `{}` 要从堆里删去一个'.format(S.height)),
        'height = -height': '还原成正数 `{height}`',
        'if height in pos_dict': lambda S, B, r: ('堆里已有高度 `{}` → 只把计数 +1'.format(S.height) if S.height in S.pos_dict
                                                   else '堆里还没有高度 `{}` → 新插入节点'.format(S.height)),
        '[pos_dict[height]][1] += 1': '这个高度的计数 +1，不重复入堆',
        'max_height.append([height, 1])': '新节点 `[{height}, 1]` 先放到堆尾',
        'now = len(max_height) - 1': '从堆尾位置 `now = {now}` 开始上浮',
        'while now > 1 and height >': lambda S, B, r: (
            f'比较 `height = {S.height}` 与父节点 `{S.max_height[S.now // 2][0]}`：更大 → 继续上浮'
            if S.now > 1 and S.height > S.max_height[S.now // 2][0] else '到堆顶或不比父节点大 → 上浮结束'),
        'max_height[now] = max_height[now // 2]': '父节点下移到位置 `{now}`',
        'now //= 2': '`now` 上移到 `{now}`',
        'max_height[now] = [height, 1]': '新节点落在位置 `{now}`',
        'pos_dict[height] = now': '`pos_dict[{height}] = {now}`：记下位置，删除时能直接找到',
        'pos = pos_dict[height]': '右边界：用 `pos_dict` 直接找到高度 `{height}` 在堆中的位置 `{pos}`',
        'max_height[pos][1] -= 1': '计数 −1 → `{max_height[pos][1]}`',
        'if max_height[pos][1] == 0': lambda S, B, r: ('计数变成 0 → 这个高度没有建筑了，要从堆里删掉' if S.max_height[S.pos][1] == 0
                                                       else '计数还 > 0 → 还有别的建筑同高，节点保留'),
        'max_height[pos] = max_height[-1]': '用堆尾元素顶替被删位置，再下沉恢复堆序',
        'max_height.pop()': '堆长度减 1',
        'while True:': '下沉：比较 `pos={pos}` 与左右孩子',
        'if left < len(max_height) and': lambda S, B, r: '左孩子存在且更大：{}'.format('是' if S.left < len(S.max_height) and S.max_height[S.pos][0] < S.max_height[S.left][0] else '否'),
        'if right < len(max_height) and': lambda S, B, r: '右孩子存在且更大：{}'.format('是' if S.right < len(S.max_height) and S.max_height[S.pos][0] < S.max_height[S.right][0] else '否'),
        'if not right_flag:': lambda S, B, r: ('两个孩子都不更大 → 下沉结束' if not S.right_flag and not S.left_flag else '只有右孩子更大 → 和右孩子交换'),
        'if not right_flag or': '左右孩子都更大时，挑较大的那个交换',
        'if pos < len(max_height):': '被换到最终位置的节点，记下它的新下标',
        'pos_dict.pop(height)': '高度 `{height}` 已不在堆里，从 `pos_dict` 删除',
        'if len(max_height) == 1': lambda S, B, r: ('堆里只剩占位元素 → 没有建筑，高度 `0`' if len(S.max_height) == 1
                                                    else '堆非空 → 当前最高高度 = 堆顶 `max_height[1][0]`'),
        'now_height = 0': '当前最高高度 `0`（地面）',
        'now_height = max_height[1][0]': '当前最高高度 = 堆顶 = =={now_height}==',
        'if not res or res[-1][1] != now_height': lambda S, B, r: (
            '`res` 还是空 → 第一个转折点' if not S.res else
            (f'`res` 最后高度 `{S.res[-1][1]}` ≠ 当前 `{S.now_height}` → ==出现转折点==' if S.res[-1][1] != S.now_height
             else f'最后高度 `{S.res[-1][1]}` = 当前 `{S.now_height}` → 高度没变，不是转折点')),
        'res.append([x, now_height])': '记录转折点 `({x}, {now_height})`',
        'return res': '天际线转折点：`{ret}`',
    },
    max_steps=140,
    cards=dict(
        one_liner='只在边界处扫描：堆顶高度一变，就是一个转折点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给出每栋建筑的 `[左, 右, 高]`，求天际线的关键点（高度变化的左端点）',
                 '示例：`[[2,9,10],[3,7,15],[5,12,12],…]` → `[[2,10],[3,15],[7,12],[12,0],…]`',
                 '本视频：`[[2,9,10],[3,7,15]]` → `[[2,10],[3,15],[7,10],[9,0]]`'],
        quote='转折点只可能出现在建筑的左边界或者右边界，那么实际上x只需要在所有建筑的左右边界中遍历即可。……若当前点是某个建筑的左边界，则将其高度加入堆中，若是某个建筑的右边界，则将其高度从堆中删去。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 x 从左到右扫：左边界高度入堆，右边界高度出堆，堆顶 = 此处最高高度',
              '堆顶和上一次不同 → 在 `(x, 堆顶)` 出现转折点；堆空则高度为 0',
              '作者手写最大堆，节点带==频率==：同高建筑只计数，计数为 0 才真正删除'],
        summary=['时间 `O(n log n)`，空间 `O(n)`：每个边界最多一次入堆、一次出堆',
                 '易错：同一 x 上若有多个边界，要==全部处理完==再取堆顶判断转折点',
                 '`pos_dict` 记录高度在堆中的位置，让删除任意高度不用扫描整个堆',
                 '原文为 Python 2 写法，已把 `now / 2`、`now /= 2` 改成 `//`，并删去未使用的 `import Queue`',
                 '题面库里缺失，题意据 yiduobo 文章与 LeetCode 原题补写'],
    ),
)
