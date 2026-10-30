NUMS = [4, 1, 7, 5]
K = 3
QUERIES = [[0, 2], [1, 3]]

CODE = '''
class Node:
    __slots__ = 'l', 'r', 'lo', 'ro', 'cnt', 'sum'

    def __init__(self, l: int, r: int, lo=None, ro=None, cnt=0, sum=0):
        self.l = l
        self.r = r
        self.lo = lo
        self.ro = ro
        self.cnt = cnt
        self.sum = sum

    def maintain(self):
        self.cnt = self.lo.cnt + self.ro.cnt
        self.sum = self.lo.sum + self.ro.sum

    @staticmethod
    def build(l: int, r: int) -> 'Node':
        o = Node(l, r)
        if l == r:
            return o
        mid = (l + r) // 2
        o.lo = Node.build(l, mid)
        o.ro = Node.build(mid + 1, r)
        return o

    # 在线段树的位置 i 添加 val
    def add(self, i: int, val: int) -> 'Node':
        # 复制一份当前节点
        o = Node(self.l, self.r, self.lo, self.ro, self.cnt, self.sum)
        if o.l == o.r:
            o.cnt += 1
            o.sum += val
            return o
        mid = (o.l + o.r) // 2
        if i <= mid:
            o.lo = o.lo.add(i, val)
        else:
            o.ro = o.ro.add(i, val)
        o.maintain()
        return o

    # 查询 old 和 self 对应子数组的第 k 小，有多少个数小于第 k 小，这些数的元素和是多少
    def query(self, old: 'Node', k: int) -> Tuple[int, int, int]:
        if self.l == self.r:
            return self.l, 0, 0
        cnt_l = self.lo.cnt - old.lo.cnt
        if k <= cnt_l:
            return self.lo.query(old.lo, k)
        i, c, s = self.ro.query(old.ro, k - cnt_l)
        sum_l = self.lo.sum - old.lo.sum
        return i, cnt_l + c, sum_l + s

class Solution:
    def minOperations(self, nums: List[int], k: int, queries: List[List[int]]) -> List[int]:
        n = len(nums)
        left = [0] * n
        for i in range(1, n):
            left[i] = left[i - 1] if nums[i] % k == nums[i - 1] % k else i

        # 准备离散化
        sorted_nums = sorted(set(nums))
        mp = {x: i for i, x in enumerate(sorted_nums)}

        # 构建可持久化线段树
        t = [None] * (n + 1)
        t[0] = Node.build(0, len(sorted_nums) - 1)
        for i, x in enumerate(nums):
            j = mp[x]  # 离散化
            t[i + 1] = t[i].add(j, x)

        ans = []
        for l, r in queries:
            if left[r] > l:  # 无解
                ans.append(-1)
                continue

            r += 1  # 改成左闭右开，方便计算

            # 计算区间中位数
            sz = r - l
            i, cnt_left, sum_left = t[r].query(t[l], sz // 2 + 1)
            median = sorted_nums[i]  # 离散化后的值 -> 原始值

            # 计算区间所有元素到中位数的距离和
            total = t[r].sum - t[l].sum  # 区间元素和
            s = median * cnt_left - sum_left  # 蓝色面积
            s += total - sum_left - median * (sz - cnt_left)  # 绿色面积
            ans.append(s // k)  # 操作次数 = 距离和 / k

        return ans
'''
_L = CODE.split('\n')
_q0 = next(i for i, s in enumerate(_L) if 'def query(self, old' in s) + 1      # 引擎行号 = 下标（去掉开头空行）：query 的第一行函数体
_q1 = next(i for i, s in enumerate(_L) if 'return i, cnt_l + c, sum_l + s' in s)
_sol = next(i for i, s in enumerate(_L) if s.startswith('class Solution'))
SKIP = [ln for ln in range(1, _sol) if not (_q0 <= ln <= _q1)]


def _leaves(o, so):
    out = [0] * len(so)
    sm = [0] * len(so)
    st = [o]
    while st:
        x = st.pop()
        if x is None:
            continue
        if x.l == x.r:
            out[x.l] = x.cnt
            sm[x.l] = x.sum
        else:
            st.append(x.lo)
            st.append(x.ro)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    t, so = S.get('t'), S.get('sorted_nums')
    cv.text((x0 + 18, y0 + 14), 't[i]：前 i 个数的“值出现次数”（可持久化线段树的叶子）', 22, T['muted'], bold=True)
    if t is None or so is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    m = len(so)
    rows = [(i, _leaves(o, so)) for i, o in enumerate(t) if o is not None and o.l == 0]
    inn = S.get('_inner') or {}
    ql, qr = (S.get('l'), S.get('r')) if 'ans' in S and S.get('l') is not None and S.get('r') is not None and 'sz' in S else (None, None)
    show_diff = ql is not None
    nrow = len(t) + (1 if show_diff else 0)
    hx = 90
    cw = min(110, (x1 - x0 - 40 - hx) / m)
    ch = min(56, (y1 - y0 - 90) / max(1, nrow))
    sx, sy = x0 + 20 + hx, y0 + 90
    for j, v in enumerate(so):
        cv.text((sx + j * cw + cw / 2, sy - 8), str(v), 22, T['cyan'], anchor='mb', mono=True, bold=True)
    for i, cnts in rows:
        Y = sy + i * ch
        hot = show_diff and i in (ql, qr)
        cv.text((sx - 10, Y + ch / 2), f't[{i}]', 22, T['yellow'] if hot else T['muted'], anchor='rm', mono=True, bold=hot)
        for j, c in enumerate(cnts):
            X = sx + j * cw
            fill = T['panel2'] if c == 0 else (46, 74, 70)
            cv.rect((X + 2, Y + 2, X + cw - 2, Y + ch - 2), fill=fill, r=6, outline=T['yellow'] if hot else T['border'], width=3 if hot else 1)
            cv.text((X + cw / 2, Y + ch / 2), c, 24, T['dim'] if c == 0 else T['text'], anchor='mm', bold=True)
    if show_diff and ql < len(t) and qr < len(t) and t[ql] is not None and t[qr] is not None:
        a, b = _leaves(t[ql], so), _leaves(t[qr], so)
        Y = sy + len(t) * ch
        cv.text((sx - 10, Y + ch / 2), f't[{qr}]−t[{ql}]', 20, T['green'], anchor='rm', mono=True, bold=True)
        for j in range(m):
            X = sx + j * cw
            d = b[j] - a[j]
            cv.rect((X + 2, Y + 2, X + cw - 2, Y + ch - 2), fill=T['green'] if d else T['panel2'], r=6)
            cv.text((X + cw / 2, Y + ch / 2), d, 24, T['bg'] if d else T['dim'], anchor='mm', bold=True)


def _node_txt(S):
    inn = S.get('_inner') or {}
    if inn.get('self') is not None and hasattr(inn['self'], 'l') and 'k' in inn:
        o, old = inn['self'], inn.get('old')
        return f'当前节点管理值域下标 `[{o.l}, {o.r}]`：差值个数 `{o.cnt - (old.cnt if old else 0)}`，第 `{inn["k"]}` 小'
    if 'median' in S:
        return f'中位数 `{S["median"]}`；比它小的有 `{S["cnt_left"]}` 个，和为 `{S["sum_left"]}`'
    return ''


CONFIG = dict(
    num=3762, title='使数组元素相等的最小操作次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='同余判无解 + 中位数贪心 + 可持久化线段树',
    tags=['灵神题单·常用数据结构', '灵神题单·贪心与思维', '难度分 2497'],
    code=CODE,
    call=f'Solution().minOperations({NUMS}, {K}, {QUERIES})',
    expect=[2, -1],
    max_steps=64,
    skip=SKIP + ['n = len(nums)', 'left = [0] * n', 'mp = {x', 'j = mp[x]'],
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前查询区间 [l, r)）', cell=70, h=170,
             window=('l', 'r - 1') if False else None,
             color=lambda S, i, v: 'blue' if 'sz' in S and S['l'] <= i < S['r'] else None),
        dict(type='array', var='left', label='left[i]：以 i 结尾、模 k 同余的最左起点', cell=70, h=170,
             pointers={"r - 1 if 'sz' in S else None": 'pink'}),
        dict(type='custom', draw=_draw, h=320),
        dict(type='text', fn=_node_txt, size=22, h=50),
        dict(type='calls', h=90, hide=('old',)),
    ],
    watch=[('l', "S.get('l')", 'blue'), ('r', "S.get('r')", 'pink'), ('median', "S.get('median')", 'yellow'), ('s', "S.get('s')"), ('ans', "S.get('ans')", 'green')],
    captions={
        'left = [0] * n': '`left[i]`：区间 `[left[i], i]` 的数模 `k` 全部同余',
        'for i in range(1, n)': '预处理 `left`：模 `k` 同余才能互相变成相等',
        'left[i] = left[i - 1]': lambda S, B, r: (f'`nums[{S.i}] % k = {S.nums[S.i] % S.k}`，`nums[{S.i-1}] % k = {S.nums[S.i-1] % S.k}`：'
                                                  + ('==同余== → 沿用 `left[i-1]`' if S.nums[S.i] % S.k == S.nums[S.i-1] % S.k else '不同余 → 从 `i` 重新开始') + f'，`left[{S.i}] = {S.left[S.i]}`'),
        'sorted_nums = sorted': '离散化：排序去重 `{sorted_nums}`，线段树按值域下标 0..{len(sorted_nums)-1} 建',
        't = [None]': '`t[i]` 是“前 i 个数”的线段树版本，`t[0]` 是空树',
        't[0] = Node.build': '建空树：每个叶子的出现次数 = 0',
        't[i + 1] = t[i].add': lambda S, B, r: f'在 `t[{B.i}]` 基础上加入 `{B.x}`（值域下标 `{B.j}`）：只复制路径上 `O(log n)` 个节点 → 新版本 `t[{B.i + 1}]`，其余节点共用',
        'for l, r in queries': lambda S, B, r: (f'处理查询 `[{S.l}, {S.r}]`' if not ('ans' in B and B.l == S.l and B.r == S.r) else '所有查询处理完了'),
        'if left[r] > l': lambda S, B, r: (f'`left[{S.r}] = {S.left[S.r]} > l = {S.l}`：区间里有模 k 不同余的数 → ==无解==' if S.left[S.r] > S.l
                                           else f'`left[{S.r}] = {S.left[S.r]} ≤ l = {S.l}`：区间内全部同余 → 有解，继续'),
        'ans.append(-1)': '无解，这个查询答案 `-1`',
        'r += 1': '改成左闭右开：区间 `[l, r)`，子数组 = `t[r] − t[l]`（前缀相减）',
        'sz = r - l': '区间长度 `sz = {sz}`，中位数是第 `{sz // 2 + 1}` 小',
        'i, cnt_left, sum_left = t[r].query': '同时在 `t[r]` 和 `t[l]` 上二分找第 `{sz // 2 + 1}` 小，顺便累计比它小的个数和元素和',
        'if self.l == self.r': lambda S, B, r: ('到叶子：值域下标 `{}` 就是第 k 小'.format(S.l) if S.l == S.r else '还没到叶子，继续往下二分'),
        'cnt_l = self.lo.cnt': '左子树里区间元素个数 `cnt_l = {cnt_l}`（两个版本的 cnt 相减）',
        'if k <= cnt_l': lambda S, B, r: (f'`k = {S.k} ≤ {S.cnt_l}`：第 k 小在左子树' if S.k <= S.cnt_l else f'`k = {S.k} > {S.cnt_l}`：第 k 小在右子树，要找右边第 `{S.k - S.cnt_l}` 小'),
        'return self.lo.query': '往左子树走',
        'i, c, s = self.ro.query': '往右子树走，`k` 减去左边已有的 `{cnt_l}` 个',
        'sum_l = self.lo.sum': '把左子树的个数 `{cnt_l}`、元素和 `{sum_l}` 也累计进“比它小”的统计',
        'return i, cnt_l + c': '回溯返回：第 k 小的下标 `{i}`，比它小的个数 `{cnt_l + c}`，元素和 `{sum_l + s}`',
        'return self.l, 0, 0': '叶子：返回值域下标 `{self.l}`，从叶子开始累计',
        'median = sorted_nums[i]': '离散化的下标 `{i}` → 原始值，中位数 `median = {median}`',
        'total = t[r].sum': '区间元素和 `total = {total}`',
        's = median * cnt_left': '比中位数小的数到中位数的距离和：`{median} × {cnt_left} − {sum_left}` = `{s}`（蓝色面积）',
        's += total': '其余数到中位数的距离和：`({total} − {sum_left}) − {median} × {sz - cnt_left}`，加上后 `s = {s}`（绿色面积）',
        'ans.append(s // k)': '每次操作改变 `k`，所以操作次数 = 距离和 `{s}` ÷ `k` = =={s // k}==',
        'return ans': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='同余才能相等；变成中位数最省；可持久化线段树查区间中位数',
        complexity='时间 `O((n+q) log n)`，空间 `O(n log n)`',
        problem=['每次可把一个数 `±k`；每个查询问 `nums[l..r]` 全部变成相等的最少操作次数',
                 '不可能就返回 `-1`',
                 '示例：`nums=[1,4,7], k=3, queries=[[0,1],[0,2]]` → `[1,2]`',
                 '本视频：`[4,1,7,5]`，`k=3`，查询 `[[0,2],[1,3]]` → `[2,-1]`'],
        quote='如果有解，那么把区间内的数都变成区间的中位数是最优的。……子数组是两个前缀的差值，用计数排序，对每个前缀统计元素出现次数，不就可以做减法了吗！',
        quote_src='—— 灵茶山艾府题解',
        idea=['无解：区间内所有数关于模 `k` 必须同余，用 `left[i]` 一次判断',
              '有解：全变成中位数最优，操作次数 = 距离和 ÷ `k`',
              '可持久化线段树：每加一个数只新建一条链，`t[r] − t[l]` 就是子数组的值域计数',
              '在两棵树上同时二分求第 k 小，并累计“比它小”的个数和元素和，用两块面积算距离和'],
        after=[dict(heading='另一种写法', lines=['写法一把 `kth` 和 `query` 分成两个函数，各做一次递归',
                                                  '写法二合并成一个 `query`，统计“小于中位数”的个数和，边界返回 0，更简洁'])],
        summary=['时间 `O((n+q) log n)`，空间 `O(n log n)`',
                 '易错：`left[r] > l` 才无解；`r += 1` 之后要用左闭右开的 `t[r] − t[l]`',
                 '易错：距离和要除以 `k`，且中位数取 `sz // 2 + 1` 小',
                 '前置：同余、中位数贪心（462 题）、距离和（2602 题）'],
    ),
)
