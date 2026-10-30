def _s(t):
    return ''.join(str(x) for x in t)


def _ops(S):
    if 'now' not in S:
        return ''
    t = f"当前 `now = {_s(S['now'])}`"
    if 'left' in S and 'right' in S and 'mid' in S:
        t += f"，取出 `now[{S['left']}:{S['right'] + 1}]` = `{_s(S['mid'])}`"
        if 'rest' in S:
            t += f"，剩下 `rest = {_s(S['rest'])}`"
        if 'nxt' in S and S['_line'] >= 21:
            t += f"，插到 `index = {S['index']}` → `{_s(S['nxt'])}`"
    return t


def _cell_color(S, i, v):
    if 'head' not in S:
        return None
    if S['head'] <= i < S['tail']:
        return 'blue'
    return None


CONFIG = dict(
    num=3690, title='拆分合并数组', difficulty='Medium', category='位运算',
    author='yiduobo', technique='暴力 BFS · 枚举 left、right、插入位置',
    tags=['灵神题单', '位运算', '难度分 1982'],
    code='''
class Solution(object):
    def minSplitMerge(self, nums1, nums2):
        
        if nums1 == nums2:
            return 0
        
        q = [tuple(nums1)]
        head, tail = 0, 1
        res = 0
        n = len(nums1)
        vis = set(tuple(nums1))
        target = tuple(nums2)
        while head < tail:
            res += 1
            for now in q[head : tail]:
                for left in range(n):
                    for right in range(left, n):
                        if left == 0 and right == n - 1:
                            continue
                        
                        mid = now[left : right + 1]
                        rest = now[:left] + now[right + 1:]
                        for index in range(len(rest)):
                            nxt = rest[:index] + mid + rest[index:]
                            key = tuple(nxt)
                            if key not in vis:
                                vis.add(key)
                                q.append(key)
                                if target in vis:
                                    return res
            
            head, tail = tail, len(q)
        
        return 0
''',
    call='Solution().minSplitMerge([3, 1, 2], [1, 2, 3])',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: (f"目标 `target = {_s(S['target'])}`；每次操作后得到的仍是 `nums1` 的某个排列" if 'target' in S else ''), size=22, h=70),
        dict(type='text', fn=_ops, size=22, h=90),
        dict(type='queue', var='q', fmt=_s, label='q：下标 head 到 tail 之前是当前这一层，之后是下一层', h=210),
        dict(type='set', var='vis', fmt=lambda x: _s(x) if isinstance(x, tuple) else str(x), label='vis', h=200),
    ],
    watch=[('res', lambda S: S.get('res'), 'green'), ('head', lambda S: S.get('head'), 'blue'), ('tail', lambda S: S.get('tail'), 'pink'),
           ('left', lambda S: S.get('left'), 'cyan'), ('right', lambda S: S.get('right'), 'yellow'), ('index', lambda S: S.get('index'), 'orange')],
    max_steps=60,
    captions={
        'if nums1 == nums2': '起点就是终点，不需要操作 → 返回 `0`',
        'q = [tuple': '队列从起点开始；数组改成 `tuple`，才能放进集合判重',
        'head, tail = 0, 1': '`q[head:tail]` 就是当前这一层的所有排列',
        'res = 0': '`res` 记录层数，也就是操作次数',
        'vis = set': '`vis` 记录出现过的排列',
        'target = tuple': '终点 `target`，也要变成 `tuple`',
        'while head < tail': lambda S, B, r: (f'当前层 `q[{S.head}:{S.tail}]` 有 {S.tail - S.head} 个排列' if S.head < S.tail else '这一层没有排列了'),
        'res += 1': '再多做一次操作：`res` → `{res}`',
        'for now in': lambda S, B, r: f'取出当前层的一个排列 `now = {_s(S.now)}`',
        'for left in range': '枚举子数组的左端点 `left`',
        'for right in range': '枚举右端点 `right`，子数组是 `now[left : right + 1]`',
        'if left == 0 and right == n - 1': lambda S, B, r: ('取走整个数组，剩下空数组，插回来还是原样 → 无意义，跳过' if S.left == 0 and S.right == S.n - 1 else f'`[{S.left}, {S.right}]` 不是整个数组，继续'),
        'mid = now': '被移出的子数组 `mid = {mid}`',
        'rest = now': '剩下的元素拼起来：`rest = now[:left] + now[right + 1:] = {rest}`',
        'for index in range': '枚举把 `mid` 插进 `rest` 的位置 `index`',
        'nxt = rest': '`mid` 插到 `rest` 的位置 `{index}` → `nxt = {nxt}`',
        'key = tuple': '转成 `tuple` 好判重',
        'if key not in vis': lambda S, B, r: ('`key` 没见过 → 是一个新排列，加入队列' if S.key not in S.vis else '`key` 见过了（更少的操作次数就能到），忽略'),
        'vis.add': '标记已见过',
        'q.append': '`key` 入队，等下一层再扩展',
        'if target in vis': lambda S, B, r: ('`target` 已经出现在 `vis` 里 → ==找到终点==，当前层数就是答案' if S.target in S.vis else '`target` 还没出现，继续找'),
        'return res': '最少操作次数 `{res}`',
        'head, tail =': '这一层处理完：下一层是 `q[{tail}:]`，更新 `head, tail`',
    },
    cards=dict(
        one_liner='排列最多 720 个，直接 BFS 找最少操作次数',
        complexity='时间约 `O(n!·n^4)`，空间 `O(n!·n)`',
        problem=['拆出 `nums1` 的一个子数组，插回剩余数组的任意位置，算一次操作',
                 '求 `nums1` 变成 `nums2` 的最少操作次数，`n ≤ 6`',
                 '示例：`[3,1,2] → [1,2,3]`，把 `[3]` 放到末尾，答案 `1`'],
        quote='每次操作后nums1中的元素没有凭空消失，也没有多出其他元素，得到的依然是nums1的某个排列。……最多只有6! = 720中不同排列，在这里完全可以直接暴力bfs。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 6` → 排列最多 720 个，每个排列是图的一个点',
              '对队列里的 `now`：枚举 `left、right` 取出 `mid`，拼出 `rest`',
              '再枚举插入位置 `index`，新数组没见过就入队；一旦出现 `target` 就返回层数'],
        result='第 1 层里就出现了 `(1,2,3)`，返回 `1` ✓',
        summary=['层数 = 操作次数；用 `head、tail` 切出当前层，不用开新列表',
                 '易错：整个数组取出再插回是原样，必须 `continue`（不然白做）',
                 '易错：用 `tuple` 才能放进 `set` 判重',
                 '原文本来就能在 Python 3 运行，代码未改动（`set(tuple(nums1))` 会把元素拆开放进 `vis`，不影响结果）',
                 '对比灵神：灵神把数组压成整数并先枚举 `r` 再枚举 `l`，这里直接切片拼接 `tuple`，写法更直观'],
    ),
)
