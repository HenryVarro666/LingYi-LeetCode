N, P, BANNED, K = 7, 0, [3], 3


def _pt(S, name):
    v = S.get(name)
    return v if isinstance(v, int) and 0 <= v < S['n'] else None


def _pi(S):
    return _pt(S, 'i')


def _pnow(S):
    return _pt(S, 'now')


def _ml(S):
    return _pt(S, 'min_left')


def _mr(S):
    return _pt(S, 'max_right')


def _hd(S):
    return S['head'] if 'head' in S and S['head'] < len(S['q']) else None


def _ext(S):
    if 'min_left' not in S or S.get('min_left') is None:
        return ''
    pl, pr = S['pre_left'], S['pre_right']
    return (f"本轮扩展范围：`{S['min_left']}` 到 `{S['max_right']}`（同奇偶）；"
            f"上轮边界 `pre_left={pl}`、`pre_right={pr}`")


CONFIG = dict(
    num=2612, title='最少翻转操作数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='BFS + 记录已扩展的左右边界',
    tags=['图论算法', '难度分 2824'],
    code='''
class Solution(object):
    def minReverseOperations(self, n, p, banned, k):

        res = [None] * n
        res[p] = 0
        for b in banned:
            res[b] = -1
        
        ban_set = set(banned)

        step = 0
        q = [p]
        head, tail = 0, 1
        pre_left = [None, None]
        pre_right = [None, None]
        r = p % 2
        t = k % 2
        pre_left[r] = p
        pre_right[r] = p
        while head < tail:
            step += 1
            min_left = max_right = None
            for now in q[head : tail]:
                now_left = max(now - k + 1, k - now - 1)
                now_right = min(now + k - 1, (n - k) + (n - 1) - now)
                if min_left is None or min_left > now_left:
                    min_left = now_left
                if max_right is None or max_right < now_right:
                    max_right = now_right

            new_left = new_right = None
            if pre_left[1 ^ t ^ r] is None:
                for i in range(min_left, max_right + 1, 2):
                    if res[i] is None:
                        res[i] = step
                        q.append(i)
                        if new_left is None:
                            new_left = i
                        new_right = i
            else:
                for i in range(min_left, max_right + 1, 2):
                    if i >= pre_left[1 ^ t ^ r]:
                        break
                    if res[i] is None:
                        res[i] = step
                        q.append(i)
                        if new_left is None:
                            new_left = i
                
                for i in range(max_right, min_left - 1, -2):
                    if i <= pre_right[1 ^ t ^ r]:
                        break
                    if res[i] is None:
                        res[i] = step
                        q.append(i)
                        if new_right is None:
                            new_right = i
                
            pre_left[1 ^ t ^ r] = new_left
            pre_right[1 ^ t ^ r] = new_right

            r ^= (1 ^ t)
            head, tail = tail, len(q)
        
        for i in range(n):
            if res[i] is None:
                res[i] = -1
            
        return res
''',
    call=f'Solution().minReverseOperations({N}, {P}, {BANNED}, {K})',
    expect=[0, -1, 1, -1, 2, -1, 3],
    views=[
        dict(type='array', var='res', label='res（None = 还没到过，绿 = 已求出步数，红 = -1）', cell=84, h=200,
             pointers={_pi: 'pink', _pnow: 'blue'},
             pointer_labels={_pi: 'i', _pnow: 'now'},
             window=(_ml, _mr),
             color=lambda S, i, v: 'red' if v == -1 else ('green' if isinstance(v, int) else None)),
        dict(type='array', var='q', label='q（队列；第 head 到 tail-1 个是本轮要扩展的）', cell=70, h=160,
             pointers={_hd: 'blue'},
             pointer_labels={_hd: 'head'},
             color=lambda S, i, v: 'cyan' if 'head' in S and S['head'] <= i < S['tail'] else None),
        dict(type='text', h=100, size=28, fn=_ext),
    ],
    watch=['step', 'r', 't', ('pre_left', 'pre_left', 'cyan'), ('pre_right', 'pre_right', 'orange')],
    skip=['ban_set = set', 'for b in banned', 'res[b] = -1', 'res = [None]', 'q = [p]', 'if min_left is None', 'if max_right is None',
          'min_left = now_left', 'max_right = now_right', 'min_left = max_right = None', 'new_left = new_right = None',
          'if new_left is None', 'if new_right is None', 'new_left = i', 'new_right = i', 'break', 'for now in q', 'for i in range(n)', 'q.append(i)', 'head, tail = 0, 1', 'pre_left = [None', 'r = p % 2', 'pre_left[r] = p', 'pre_right[1 ^ t ^ r] = new_right', 'step += 1', 67],
    max_steps=120,
    captions={
        'res[p] = 0': '起点 `p={p}` 需要 0 步；被禁止的位置标成 `-1`；`q[head:tail]` 是本轮要扩展的位置，`pre_left/pre_right` 按奇偶记录“之前扩展到的最左/最右”',
        't = k % 2': '`t = k % 2`：k 奇偶决定每轮扩展出的位置奇偶是否翻转；`r` 是本轮起点的奇偶 = {r}',
        'while head < tail': lambda S, B, r: (f'本轮队列有 `{S.tail - S.head}` 个位置待扩展，这一轮到达的位置都要 `{S.step + 1}` 步' if S.head < S.tail
                                              else '队列扩展不出新位置 → BFS 结束'),
                'now_left = max': '`now={now}` 翻转后最左：`max(now-k+1, k-now-1) = {now_left}`（不够大时贴左边界）',
        'now_right = min': '`now={now}` 翻转后最右：`min(now+k-1, 2n-k-1-now) = {now_right}`（贴右边界）',
        'if pre_left[1 ^ t ^ r] is None': lambda S, B, r: (
            '这个奇偶之前没扩展过 → 整个范围都要扫' if S['pre_left'][1 ^ S.t ^ S.r] is None
            else f'这个奇偶之前扩展到 `[{S["pre_left"][1 ^ S.t ^ S.r]}, {S["pre_right"][1 ^ S.t ^ S.r]}]` → 只需扫两端新增的部分'),
        'for i in range(min_left, max_right + 1, 2)': '从左向右隔一个扫同奇偶位置',
        'if i >= pre_left': lambda S, B, r: (f'`i = {S.i}` >= 上轮左边界 `{S.pre_left[1 ^ S.t ^ S.r]}`：里面都扩展过了 → break' if S.i >= S.pre_left[1 ^ S.t ^ S.r]
                                             else f'`i = {S.i}` < 上轮左边界 `{S.pre_left[1 ^ S.t ^ S.r]}`：在边界外侧 → 继续检查'),
        'for i in range(max_right': '再从右向左扫，只扫到上轮右边界以外',
        'if i <= pre_right': lambda S, B, r: (f'`i = {S.i}` <= 上轮右边界 `{S.pre_right[1 ^ S.t ^ S.r]}`：里面都扩展过了 → break' if S.i <= S.pre_right[1 ^ S.t ^ S.r]
                                              else f'`i = {S.i}` > 上轮右边界 `{S.pre_right[1 ^ S.t ^ S.r]}`：在边界外侧 → 继续检查'),
        'if res[i] is None': lambda S, B, r: (
            (f'位置 `{S.i}` 还没到过 → 新位置，入队' if S.res[S.i] is None else f'位置 `{S.i}` 已有答案 `{S.res[S.i]}`（到过或被禁止）→ 跳过')
            if S['_line'] != 66 else (f'`res[{S.i}]` 仍是 None：没人能到 → 改成 `-1`' if S.res[S.i] is None else f'`res[{S.i}] = {S.res[S.i]}` 保持')),
        'res[i] = step': '位置 `{i}` 第一次到达：`res[{i}] = {step}`',
        'pre_left[1 ^ t ^ r] = new_left': '本轮新位置的最左 `{new_left}`、最右 `{new_right}` 记为这个奇偶的新边界 `pre_left/pre_right`（没有新位置就是 None）',
        'r ^= (1 ^ t)': '`k` 为偶数时起点奇偶翻转，为奇数时不变',
        'head, tail = tail': '下一轮的队列是刚加进来的 `q[{head}:{tail}]`',
        'return res': '全部位置的最少步数：`{res}`',
    },
    cards=dict(
        one_liner='每轮只扩展“上一轮边界之外”的同奇偶位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['长 `n` 的 0 数组只有 `p` 处是 1；每次翻转长 `k` 的子数组，1 不能落在 `banned` 上',
                 '求 1 到每个位置的最少操作数，到不了是 `-1`',
                 f'本视频：`n={N}, p={P}, banned={BANNED}, k={K}`'],
        quote='每次翻转可以到达的位置都将是一个由相同奇偶性的下标组成的连续子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 翻转后最左 `max(now-k+1, k-now-1)`，最右 `min(now+k-1, 2n-k-1-now)`',
              '从 L、R 又能翻回 A，所以每轮扩展的整体也是连续同奇偶序列',
              '记下 `pre_left/pre_right`，下一轮只扫它们外侧；`k` 偶数时奇偶翻转，用 `1^t^r` 算'],
        summary=['时间 `O(n)`：每个位置至多入队一次，也不会被重复扫',
                 '`k` 为奇数目标位置与起点同奇偶，偶数则相反',
                 '本题原文为 Python 2 风格，没有需要改的语法',
                 '对比灵神：灵神用并查集/有序集合直接“删点”；这里用边界数组避免重复扫描'],
    ),
)
