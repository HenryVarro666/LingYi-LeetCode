INF = 10 ** 9 + 1


def _kids(n):
    return [(k, c) for k, c in (('0', n.left), ('1', n.right)) if c is not None]


def _lay(node, depth, pos, out):
    ks = _kids(node)
    if not ks:
        x = pos[0]
        pos[0] += 1
        out.append((node, depth, x, []))
        return x
    xs = [_lay(c, depth + 1, pos, out) for k, c in ks]
    x = (xs[0] + xs[-1]) / 2
    out.append((node, depth, x, ks))
    return x


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '0-1 字典树（左边 = 位 0，右边 = 位 1；圆内 v = 这棵子树里的最小数）', 22, T['muted'], bold=True)
    root = S.get('root')
    if root is None or not hasattr(root, 'left'):
        return
    # 折叠最上面一长串只有「0」边的链（30 位里高位全是 0）
    start, skipped = root, 0
    while skipped < 27 and start.left is not None and start.right is None:
        start = start.left
        skipped += 1
    out = []
    pos = [0]
    _lay(start, 0, pos, out)
    maxd = max(o[1] for o in out)
    cols = max(pos[0], 1)
    gx = min(150, (x1 - x0 - 100) / cols)
    gy = min(95, (y1 - y0 - 190) / max(maxd, 1))
    top = y0 + (110 if skipped else 70)
    P = {id(o[0]): (x0 + 50 + (x1 - x0 - 100 - gx * (cols - 1)) / 2 + o[2] * gx, top + o[1] * gy) for o in out}
    now = S.get('now')
    sx, sy = P[id(start)]
    if skipped:
        cv.rect((x0 + 30, y0 + 40, x1 - 30, y0 + 70), fill=T['panel2'], outline=T['border'], width=2, r=10)
        cv.text(((x0 + x1) / 2, y0 + 55), f'root … 高 {skipped} 位全是 0，只有一条左链（已折叠）', 20, T['muted'], anchor='mm')
        cv.line([((x0 + x1) / 2, y0 + 70), (sx, sy - 24)], T['muted'], 2)
    for node, d, x, ks in out:
        a = P[id(node)]
        for k, c in ks:
            b = P[id(c)]
            cv.line([(a[0], a[1] + 24), (b[0], b[1] - 24)], T['muted'], 2)
            cv.text(((a[0] + b[0]) / 2 + (-14 if k == '0' else 14), (a[1] + b[1]) / 2), k, 22, T['cyan'] if k == '0' else T['pink'], anchor='mm', bold=True, mono=True)
    for node, d, x, ks in out:
        X, Y = P[id(node)]
        ring = T['yellow'] if node is now else None
        cv.rect((X - 24, Y - 24, X + 24, Y + 24), fill=T['panel2'], outline=ring or T['border'], width=5 if ring else 2, r=24)
        cv.text((X, Y), '∞' if node.v >= INF else node.v, 22, T['text'], anchor='mm', bold=True)
        if node is root:
            cv.text((X - 30, Y), 'root', 18, T['dim'], anchor='rm')


def _bits(S):
    b = S.get('binary')
    if not isinstance(b, list):
        return ''
    low = ''.join(str(v) for v in reversed(b[:3])).rjust(3, '0')
    who = S.get('num') if S['_line'] <= 46 and 'num' in S and S['_line'] < 48 else S.get('x')
    cur = S.get('p')
    mark = f'，正在看第 =={cur}== 位' if isinstance(cur, int) and 0 <= cur <= 2 else ''
    return f'`{who}` 的低 3 位（高位在前）：=={low}==（更高位全是 0）{mark}'


CONFIG = dict(
    num=1707, title='与数组中元素的最大异或值', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='0-1 字典树 + 节点最小值',
    tags=['字典树', '位运算'],
    code='''
class Node(object):
    def __init__(self, v):
        self.v = v
        self.left = self.right = None

class Solution(object):
    def maximizeXor(self, nums, queries):

        root = Node(10 ** 9 + 1)
        for num in nums:
            tmp = num
            binary = []
            while True:
                binary.append(tmp % 2)
                tmp //= 2
                if not tmp:
                    break
            
            now = root
            p = 29
            while p >= len(binary):
                if now.left is None:
                    node = Node(num)
                    now.left = node
                
                now.v = min(now.v, num)
                now = now.left
                p -= 1

            while p >= 0:
                if binary[p] == 0:
                    if now.left is None:
                        node = Node(num)
                        now.left = node
                    
                    now.v = min(now.v, num)
                    now = now.left
                else:
                    if now.right is None:
                        node = Node(num)
                        now.right = node
                    
                    now.v = min(now.v, num)
                    now = now.right
        
                p -= 1

        res = []
        for x, m in queries:
            if root.v > m:
                res.append(-1)
                continue

            tmp = x
            binary = []
            while True:
                binary.append(tmp % 2)
                tmp //= 2
                if not tmp:
                    break

            now = root
            res.append(0)
            p = 29
            while p >= len(binary):
                if now.right and now.right.v <= m:
                    now = now.right
                    res[-1] += res[-1] + 1
                else:
                    now = now.left
                    res[-1] += res[-1]
                
                p -= 1
            
            while p >= 0:
                if binary[p] == 0:
                    if now.right and now.right.v <= m:
                        now = now.right
                        res[-1] += res[-1] + 1
                    else:
                        now = now.left
                        res[-1] += res[-1]
                else:
                    if now.left and now.left.v <= m:
                        now = now.left
                        res[-1] += res[-1] + 1
                    else:
                        now = now.right
                        res[-1] += res[-1]
                
                p -= 1
        
        return res
''',
    call='Solution().maximizeXor([1, 2, 5], [[5, 1], [5, 5], [0, 0]])',
    expect=[4, 7, -1],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_bits, h=70),
        dict(type='array', var='res', label='res（每个询问的答案）', cell=90, h=150),
    ],
    watch=['num', 'x', 'm', 'p', ('now.v', lambda S: S['now'].v if getattr(S.get('now'), 'v', None) is not None and S['now'].v < INF else '∞', 'yellow'), ('root.v', lambda S: S['root'].v if S.get('root') is not None else '', 'cyan')],
    skip=[2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 26, 27, 28, 30, 31, 32, 33, 37, 39, 40, 44, 46, 48,
          49, 52, 54, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 73, 75, 76, 78, 81, 85, 88, 91],
    max_steps=110,
    captions={
        19: '插入 `{num}`：二进制（低位在前）`binary = {binary}`，共 30 位，高位的 0 全走左边（已折叠）',
        34: '位是 0，左孩子还没有 → 新建节点 `Node({num})`，挂在左边',
        36: '经过这个节点：`v = min(v, num)` = ==`{now.v}`==（子树里最小的数）；位 = 0 → 往左走',
        41: '位是 1，右孩子还没有 → 新建节点 `Node({num})`，挂在右边',
        43: '经过这个节点：`v = min(v, num)` = ==`{now.v}`==（子树里最小的数）；位 = 1 → 往右走',
        50: lambda S, B, r: (f'询问 `x = {S.x}, m = {S.m}`：`root.v = {S.root.v}` > m → 连最小的数都超过 m，没有可选的数，答案 -1' if S.root.v > S.m
                             else f'询问 `x = {S.x}, m = {S.m}`：`root.v = {S.root.v}` ≤ m，至少有一个数可选；从最高位开始贪心，每位尽量走和 x 相反的边'),
        51: '没有数 ≤ m → 加入 `-1`',
        64: '`x` 的二进制 `binary = {binary}`；高位的 0 想走 1（右边）但右边没有 → 走左边（已折叠）',
        77: lambda S, B, r: (lambda rt: f'`x` 这一位是 0 → 想走右边(1)：' + ('右孩子最小值 `' + str(rt.v) + '` ≤ m → 能走' if rt is not None and rt.v <= S.m
                             else '右边没有或最小值 > m → 走不了，被迫走左'))(S.now.right),
        79: '走右，这一位异或得 1：`res[-1]` = ==`{res[-1]}`==',
        82: '走左，这一位异或得 0：`res[-1]` = ==`{res[-1]}`==',
        84: lambda S, B, r: (lambda lf: f'`x` 这一位是 1 → 想走左边(0)：' + ('左孩子最小值 `' + str(lf.v) + '` ≤ m → 能走' if lf is not None and lf.v <= S.m
                             else '左边没有或最小值 > m → 走不了，被迫走右'))(S.now.left),
        86: '走左，这一位异或得 1：`res[-1]` = ==`{res[-1]}`==',
        89: '走右，这一位异或得 0：`res[-1]` = ==`{res[-1]}`==',
        93: '全部询问处理完：`{res}`',
    },
    cards=dict(
        one_liner='异或最大：每一位尽量走「和 x 相反」的那条边；节点记最小值来满足 ≤ m',
        complexity='时间 `O((n + q) · 30)`，空间 `O(n · 30)`',
        problem=['给整数数组 `nums` 和询问 `[x, m]`：在 `nums` 中选一个 `≤ m` 的数 `y`，使 `x XOR y` 最大',
                 '没有 `≤ m` 的数则答案 `-1`',
                 '本视频：`nums = [1,2,5]`，询问 `[5,1] [5,5] [0,0]` → `[4,7,-1]`'],
        quote='对于一个x，如果从高位向低位进行扫描的话，应该尽量选择nums中当前位与x不同的数。……可以使用trie树来储存nums的二进制表示。',
        quote_src='—— yiduobo 题解原文',
        idea=['异或「不同为 1」→ 从高位到低位，==尽量走和 x 当前位相反的边==',
              '0-1 字典树：每个数是一条 30 位的路径，查询走 30 步',
              '限制 `≤ m`：节点多存一个 `v` = 子树最小值；`v > m` 的子树整个不能走（对应原文的第二种做法）'],
        summary=['时间 `O((n+q)·30)`，空间 `O(30n)`；30 位足够：`2^30 > 10^9`',
                 '先判 `root.v > m` → 直接 `-1`，否则字典树里一定能走出一条合法路径',
                 '走右/走左前都要检查孩子「存在且 v ≤ m」，否则被迫走另一边',
                 '原文为 Python 2 写法，`tmp /= 2`（整数除法）已改为 `tmp //= 2`',
                 '图中高位全 0 的那条长链已折叠，实际代码里每个数都要走满 30 层'],
    ),
)
