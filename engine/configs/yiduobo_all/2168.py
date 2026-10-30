def _kids(n):
    return [(i, c) for i, c in enumerate(n.childs) if c is not None]


def _depth(root, target, d=0):
    if root is target:
        return d
    for _, c in _kids(root):
        r = _depth(c, target, d + 1)
        if r >= 0:
            return r
    return -1


def _draw(cv, S, B, box, T):
    root = S.get('root')
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'trie 去重（每条从根出发的路径 = 一个出现过的子串；黄 = now）', 24, T['muted'], bold=True)
    if root is None:
        cv.text(((x0 + x1) / 2, (y0 + y1) / 2), '（trie 还没创建）', 28, T['muted'], anchor='mm')
        return
    pos, order, depth = {}, [], [0]

    def width(n):
        return max(1, sum(width(c) for _, c in _kids(n)))

    def place(n, d, left):
        depth[0] = max(depth[0], d)
        pos[id(n)] = (left + width(n) / 2, d)
        order.append((n, _kids(n)))
        cl = left
        for _, c in _kids(n):
            place(c, d + 1, cl)
            cl += width(c)
    total = width(root)
    place(root, 0, 0)
    top, bot = y0 + 70, y1 - 30
    gap = min((bot - top) / max(1, depth[0]), 90)
    W = x1 - x0 - 60
    unit = min(W / total, 170)
    sx = x0 + 30 + (W - unit * total) / 2

    def xy(n):
        px, d = pos[id(n)]
        return sx + px * unit, top + d * gap
    cur = S.get('now')
    for n, ks in order:
        X, Y = xy(n)
        for e, c in ks:
            X2, Y2 = xy(c)
            cv.line([(X, Y + 16), (X2, Y2 - 16)], T['muted'], 3)
            cv.text(((X + X2) / 2 - 16, (Y + Y2) / 2), str(e), 24, T['cyan'], anchor='mm', bold=True, mono=True)
    for n, ks in order:
        X, Y = xy(n)
        hot = cur is n
        cv.rect((X - 22, Y - 16, X + 22, Y + 16), fill=T['yellow'] if hot else T['panel2'], outline=T['blue'], width=3, r=16)
        if n is root:
            cv.text((X, Y), '根', 20, T['bg'] if hot else T['text'], anchor='mm', bold=True)


def _info(S):
    if 'cnt' not in S:
        return '枚举左端点，向右延伸；==新建 trie 节点 = 新子串==，才需要检查频率'
    nz = [v for v in S['cnt'] if v]
    ok = len(set(nz)) <= 1
    return f'非零频率 `{nz}` → ' + ('==都相等==' if ok else '不全相等') + f'；`res = {S.get("res", 0)}`'


CONFIG = dict(
    num=2168, title='每个数字的频率都相同的独特子字符串的数量', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举左端点 + trie 去重',
    tags=['字符串'],
    code='''
class TreeNode(object):

    def __init__(self):
        self.childs = [None] * 10

class Solution(object):
    def equalDigitFrequency(self, s):

        root = TreeNode()
        n = len(s)
        res = 0

        def check(cnt):
            target = None
            for v in cnt:
                if v != 0:
                    if target is None:
                        target = v
                    elif target != v:
                        return False

            return True

        num_list = [int(x) for x in list(s)]
        for left in range(n):
            cnt = [0] * 10
            check_flag = False
            now = root

            for digit in num_list[left:]:
                if now.childs[digit] is None:
                    now.childs[digit] = TreeNode()
                    check_flag = True
                
                now = now.childs[digit]
                cnt[digit] += 1

                if check_flag and check(cnt):
                    res += 1
        
        return res
''',
    call='Solution().equalDigitFrequency("1212")',
    expect=5,
    views=[
        dict(type='string', var='s', label='s', cell=70, h=130,
             color=lambda S, i, v: ('blue' if S.get('left') is not None and 'now' in S and S['left'] <= i < S['left'] + max(0, _depth(S['root'], S['now'])) else None)),
        dict(type='array', var='cnt', label='cnt（数字 0~9 出现次数）', cell=60, h=130,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', h=60, size=26, fn=_info),
    ],
    watch=[('left', 'left', 'blue'), ('digit', 'digit', 'pink'), ('check_flag', 'check_flag', 'orange'), ('res', 'res', 'green')],
    captions={
        'for left in range(n)': '枚举左端点 `left = {left}`：从 `s[{left}]` 往右延伸，每次得到一个子串',
        'now = root': '频率表 `cnt` 清零，`check_flag = False`，每个左端点都从 trie 根出发',
        'for digit in num_list[left:]': lambda S, B, r: ('`digit = %s`：子串再向右延伸一位' % S.digit if _depth(S.root, S.now) < len(S.s) - S.left
                                                         else '`s[%d:]` 都走完了，换下一个左端点' % S.left),
        'if now.childs[digit] is None': lambda S, B, r: ('`{}` 这条边还没有 → 这个子串==以前没出现过==' if S.now.childs[S.digit] is None
                                                       else '`{}` 这条边已有 → 这个子串以前出现过').format(S.digit),
        'now.childs[digit] = TreeNode()': '新建节点：子串是新的，`check_flag` 置为真，后面的更长子串也都是新的',
        'now = now.childs[digit]': '`now` 走进 `{digit}` 这条边',
        'cnt[digit] += 1': '数字 `{digit}` 出现次数 → `{cnt[digit]}`',
        'if check_flag and check(cnt)': lambda S, B, r: (
            '子串以前见过（`check_flag` 为假）→ 已经统计过，不再重复检查' if not S.check_flag else
            ('新子串，检查频率：非零频率 `{}` ==全相等== → `res` 加 1' if len({v for v in S.cnt if v}) <= 1
             else '新子串，检查频率：非零频率 `{}` 不全相等 → 不算').format([v for v in S.cnt if v])),
        'res += 1': '`res` → =={res}==',
        'return res': '一共 `{res}` 个不同子串满足条件',
    },
    skip=['self.childs = [None]', 'root = TreeNode()', 'n = len(s)', 'res = 0', 'num_list = ', 'def check',
          'target = None', 'check_flag = True', 'check_flag = False', 'cnt = [0] * 10', 'for v in cnt', 'if v != 0', 'if target is None', 'target = v', 'elif target != v', 'return False', 'return True'],
    max_steps=110,
    cards=dict(
        one_liner='枚举左端点往右延伸，用 trie 判断子串是不是第一次出现',
        complexity='时间 `O(n²·10)`，空间 `O(n²)`',
        problem=['数字串 `s`，统计其中「所有数字出现次数都相同」的==不同==子串个数',
                 '例如 `121` 的子串 `12` 里 1、2 各一次，满足；`121` 里 1 两次、2 一次，不满足',
                 '本视频：`s = "1212"` → 满足的不同子串是 `1, 2, 12, 21, 1212`，共 `5`'],
        quote='对于字符串的去重，可以直接使用哈希表来去重，当然也可以利用trie树来进行，我在这里采用的是trie树。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举所有左边界 `left`，向后延伸，用 `cnt` 记每种数字的次数',
              '沿 trie 往下走：==走到新节点 = 新子串==，只有新子串才需要检查频率',
              '一旦新建过节点，更长的子串必然也是新的，所以 `check_flag` 一直为真'],
        summary=['时间 `O(n²·10)`，空间 `O(n²)`',
                 '`check` 忽略频率为 0 的数字，其余必须全相等',
                 '`check_flag` 一旦为真就不再复位，直到换下一个 `left`',
                 '原文可直接在 Python 3 运行；自定义的 `TreeNode` 会覆盖预置的同名类',
                 '题面库里没有，题意按 yiduobo 文章和原题（LeetCode 会员题）整理'],
    ),
)
