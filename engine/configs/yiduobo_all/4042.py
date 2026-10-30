NUMS = [1, 2, 2, 1, 3]


def _phase(S):
    ln = S.get('_line', 0)
    if ln >= 106:
        return '第三步：查询。区间 `[left, right]` 需在 `hit_k[left]` 范围内，且前缀 id 相同'
    if ln >= 81:
        return '第二步：按出现次数奇偶性给每个前缀一个 id，id 相同 ⇒ 每个数出现次数奇偶性相同'
    return '第一步：双指针求每个 `index` 对应的右端点范围 `hit_k[index] = [p1, p2-1]`'


def _ptr_color(S, i, v):
    ln = S.get('_line', 0)
    if ln < 36 and 'index' in S and 'hit_k' in S:
        idx = S['index']
        if i == idx:
            return 'blue'
        p1, p2 = S.get('p1', 0), S.get('p2', 0)
        if idx <= i < p1 and ln <= 20:
            return 'cyan'
    if ln >= 106 and 'left' in S and S['left'] <= i <= S['right']:
        return 'cyan'
    if 81 <= ln < 106 and 'v' in S and 'prefix_id' in S and i < len(S['prefix_id']) - 1:
        return 'cyan'
    return None


def _hit(S):
    h = S.get('hit_k')
    if h is None:
        return ''
    return '`hit_k` = ' + '，'.join(f'[{a},{b}]' for a, b in h)


def _ids(S):
    pid = S.get('prefix_id')
    return None if pid is None else list(pid)


def _idcolor(S, i, v):
    if 'left' in S and 'right' in S and S.get('_line', 0) >= 106:
        if i == S['left']:
            return 'blue'
        if i == S['right'] + 1:
            return 'pink'
    return None


def _res_cap(S, B, r):
    left, right = S.left, S.right
    a, b = S.hit_k[left]
    in_range = a <= right <= b
    same = S.prefix_id[left] == S.prefix_id[right + 1]
    if not in_range:
        why = f'`right = {right}` 不在 `hit_k[{left}] = [{a}, {b}]` → 种类不是 k'
    elif same:
        why = f'`{a} ≤ {right} ≤ {b}` 且 `prefix_id[{left}] = prefix_id[{right + 1}]` → 种类是 k，且都是偶数次'
    else:
        why = f'`right` 在范围内，但 `prefix_id[{left}] ≠ prefix_id[{right + 1}]` → 有的数出现奇数次'
    return f'查询 `[{left}, {right}]`：{why} → =={S.res[-1]}=='


CONFIG = dict(
    num=4042, title='有效 K 个不同元素子数组 II', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='双指针定范围 + 奇偶性哈希（八叉树）',
    code='''
class Solution(object):
    def validSubarrays(self, nums, k, l0, r0, q):
        
        n = len(nums)

        freq1 = {}
        freq2 = {}
        hit_k = []
        p1 = 0
        p2 = 0
        for index, v in enumerate(nums):
            if p1 < index:
                p1 = index
            while p1 < len(nums) and len(freq1) < k:
                freq1[nums[p1]] = freq1.get(nums[p1], 0) + 1
                p1 += 1
            
            if len(freq1) < k:
                hit_k.append([-1, -1])
                continue

            if p2 < index:
                p2 = index
            while p2 < len(nums) and len(freq2) < k + 1:
                freq2[nums[p2]] = freq2.get(nums[p2], 0) + 1
                p2 += 1

            hit_k.append([p1, p2 - 1])

            freq1[v] -= 1
            if freq1[v] == 0:
                freq1.pop(v)
            freq2[v] -= 1
            if freq2[v] == 0:
                freq2.pop(v)

        vid = {}
        m = 0
        for v in nums:
            if v not in vid:
                vid[v] = m
                m += 1

        p = 1
        while p < m:
            p <<= 1

        f = [0] * (p << 1)
        length = p
        nxt_id = p << 1
        node_dict = {}
        root_flag = False
        pre_length = None
        while length:
            for index in range(length, length << 1):
                if length >= p:
                    f[index] = (index - length) << 1
                elif index == 1 and pre_length < 8:
                    if pre_length == 2:
                        key = (f[2], f[3])
                    elif pre_length == 4:
                        key = (f[4], f[5], f[6], f[7])
                    node_dict[key] = nxt_id
                    f[index] = nxt_id
                    nxt_id += 1
                else:
                    key = tuple([f[index << 3 | offset] for offset in range(8)])
                    node_dict[key] = nxt_id
                    f[index] = nxt_id
                    nxt_id += 1
            
            if length == 1:
                break

            pre_length = length
            if length >= 8:
                length >>= 3
            else:
                length = 1

        prefix_id = [f[1]]
        cnt = 0
        for v in nums:
            index = vid[v] + p
            f[index] ^= 1
            while index > 1:
                if index >= 8:
                    target = index >> 3
                    key = tuple(sorted([f[target << 3 | offset] for offset in range(8)]))
                else:
                    target = 1
                    if index >= 4:
                        key = tuple(sorted([f[4], f[5], f[6], f[7]]))
                    else:
                        key = tuple(sorted([f[2], f[3]]))
                
                if key not in node_dict:
                    node_dict[key] = nxt_id
                    nxt_id += 1
                
                f[target] = node_dict[key]
                index = target
            
            prefix_id.append(f[1])

        left, right = l0, r0
        res = []
        for _ in range(q):
            res.append(hit_k[left][0] <= right <= hit_k[left][1] and prefix_id[left] == prefix_id[right + 1])
            if res[-1]:
                g = left + right
            else:
                g = right - left
            
            left, right = (left ^ g) % n, (right ^ g) % n
            if left > right:
                left, right = right, left
        
        return res
''',
    call=f'Solution().validSubarrays({NUMS}, 2, 1, 2, 3)',
    expect=[False, True, True],
    skip=['n = len(nums)', 'freq1 = {}', 'freq2 = {}', 'hit_k = []', 'p1 = 0', 'p2 = 0', 'for index, v in enumerate', 'if p1 < index', 'p1 = index',
          'freq1[nums[p1]]', 'p1 += 1', 'if p2 < index', 'p2 = index', 'freq2[nums[p2]]', 'p2 += 1', 'continue',
          'if freq1[v] == 0', 'freq2[v] -= 1', 'freq1.pop', 'if freq2[v] == 0', 'freq2.pop',
          'vid = {}', 'm = 0', 'for v in nums', 'if v not in vid', 'vid[v] = m', 'm += 1',
          'p = 1', 'while p < m', 'p <<= 1', 'f = [0]', 'length = p', 'nxt_id =', 'node_dict = {}', 'root_flag', 'pre_length = None',
          'while length', 'for index in range(length', 'if length >= p', 'f[index] = (index', 'elif index == 1', 'if pre_length', 'elif pre_length', 'key = ', 'node_dict[key]', 'f[index] = nxt_id',
          'nxt_id += 1', 'if length == 1', 'break', 'pre_length = length', 'if length >= 8', 'length >>= 3', 'else:', 'length = 1',
          'cnt = 0', 'index = vid', 'while index > 1', 'if index >= 8', 'target', 'if index >= 4', 'if key not in', 'f[target]', 'index = target',
          'res = []', 'left, right = l0', 'for _ in range', 'if res[-1]', 'if left > right', 'left, right = right, left'],
    views=[
        dict(type='text', fn=_phase, size=22, h=64),
        dict(type='array', var='nums', label='nums（指针：index / p1 / p2 或 left / right；青 = 当前区间）', h=215, cell=84,
             pointers={'index if _line < 36 else None': 'blue', 'p1 if _line < 36 else None': 'pink', 'p2 if _line < 36 else None': 'orange',
                       'left if _line >= 106 else None': 'blue', 'right if _line >= 106 else None': 'pink'},
             pointer_labels={'index if _line < 36 else None': 'index', 'p1 if _line < 36 else None': 'p1', 'p2 if _line < 36 else None': 'p2',
                             'left if _line >= 106 else None': 'left', 'right if _line >= 106 else None': 'right'},
             color=_ptr_color),
        dict(type='text', fn=_hit, size=24, h=60),
        dict(type='array', var=_ids, label='prefix_id：前 i 个数的“奇偶性指纹”（i = 0..n）', h=190, cell=84, color=_idcolor, min_slots=6),
    ],
    watch=['k', 'index', 'p1', 'p2', 'left', 'right', ('res', 'res', 'green')],
    max_steps=80,
    captions={
        'while p1 < len(nums)': lambda S, B, r: (f'`p1` 右扩直到窗口有 `{S.k}` 种：现在有 `{len(S.freq1)}` 种' + ('，够了' if len(S.freq1) >= S.k else '，还不够，继续扩')),
        'if len(freq1) < k': lambda S, B, r: (f'`index = {S.index}`：后面凑不够 {S.k} 种了 → `hit_k` 记 `[-1, -1]`' if len(S.freq1) < S.k
                                              else f'`index = {S.index}`：从它开始能凑出 {S.k} 种（`p1 = {S.p1}`）'),
        'while p2 < len(nums)': lambda S, B, r: (f'`p2` 右扩到窗口有 `{S.k + 1}` 种：现在 `{len(S.freq2)}` 种' + ('，到了' if len(S.freq2) >= S.k + 1 else '，继续')),
        'hit_k.append([p1': '`hit_k[{index}] = [{p1}, {p2 - 1}]`：右端点 `right` 落在这个范围里，种类才可能恰好是 {k}（端点处新数只出现一次，会被奇偶性排除）',
        'freq1[v] -= 1': '`index` 右移：把 `{v}` 从 `freq1`、`freq2` 两个窗口里各减一次，种类跟着更新',
        'prefix_id = [f[1]]': '建一棵“奇偶性”树：叶子是每种值出现次数的奇偶（0/1），每个结点用 `tuple(sorted(孩子))` 哈希成 id，`f[1]` 是根 id',
        'f[index] ^= 1': '`{v}` 的奇偶翻转一次，沿路径往上重算 id，根 id = 当前前缀的指纹',
        'prefix_id.append': '`prefix_id` 追加 `{prefix_id[-1]}`：前 {len(prefix_id) - 1} 个数的指纹',
        'res.append(': _res_cap,
        'g = left + right': '上一个答案为真：`g = left + right = {g}`',
        'g = right - left': '上一个答案为假：`g = right - left = {g}`',
        'left, right = (left ^ g)': '强制在线：`left = (left ^ g) % n`，`right = (right ^ g) % n` → `[{left}, {right}]`（若 left > right 则交换）',
        'return res': '全部查询答案：`{res}`',
    },
    cards=dict(
        one_liner='用双指针定“恰好 k 种”的范围，再用奇偶性指纹判断都是偶数次',
        complexity='时间 `O((n+q)·log n)`，空间 `O(n)`',
        problem=['子数组有效：==恰好 k 种不同的数，且每种都出现偶数次==',
                 '`q` 个查询强制在线：下一个 `(l, r)` 由上一个答案算出',
                 '本视频：`nums=[1,2,2,1,3], k=2, (l0,r0)=(1,2), q=3` → `[False, True, True]`'],
        quote='将原来的二叉树压缩成八叉树，即每个节点记录一个长度为8的tuple并进行哈希就是一种可行的平衡方案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`p1`、`p2` 单调右移：`hit_k[index]` 给出 `right` 的范围，保证种类约等于 k',
              '每加入一个数就翻转它的奇偶，用树结点哈希出前缀“奇偶性指纹” `prefix_id`',
              '两个前缀 id 相同 ⇔ 区间内每个数出现偶数次；原文为省内存把二叉树压成八叉树'],
        summary=['时间 `O((n+q)·log n)`，查询 `O(1)`；强制在线也能做',
                 '`hit_k` 的 `[p1, p2-1]` 端点处新数只出现一次，被奇偶性自动排除',
                 '视频里只演示了 `hit_k`、`prefix_id` 和查询；建树（`f` 与 `node_dict`）的循环被折叠',
                 '原文为 Python 2 风格，本题无需改动即可在 Python 3 运行',
                 '对比灵神：他用随机数异或哈希 + 两次滑窗；yiduobo 用确定性的树哈希'],
    ),
)
