S0, K0 = '0101', 3


def _zl(S):
    n = S.get('n')
    return list(range(n + 1)) if n is not None else []


def _ok(S, name):
    v = S.get(name)
    return v if isinstance(v, int) and 'n' in S and 0 <= v <= S['n'] else None


def _p_zero(S):
    return _ok(S, 'zero')


def _p_ml(S):
    return _ok(S, 'min_left')


def _p_mr(S):
    return _ok(S, 'max_right')


def _col(S, i, v):
    vis = S.get('vis')
    if vis is None:
        return None
    if i == 0:
        return 'green' if 0 in vis else 'yellow'
    return 'green' if i in vis else None


def _txt(S):
    if 'min_left' in S and S['min_left'] is not None and 'now_left' in S:
        return (f"0 的个数为 `now={S.get('now')}` 时，一次翻转后能变成 `[{S['min_left']}, {S['max_right']}]` 里同奇偶的数")
    return '状态 = 字符串里 0 的个数 `zero`（0 到 n），一次翻转后 0 的个数落在步长为 2 的区间里'


CONFIG = dict(
    num=3666, title='使二进制字符串全为 1 的最少操作次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按 0 的个数 BFS · 记录左右边界',
    tags=['图论算法', '难度分 2477'],
    code='''
class Solution(object):
    def minOperations(self, s, k):

        n = len(s)        
        zero = 0
        for c in s:
            if c == '0':
                zero += 1

        step = 0
        q = [zero]
        head, tail = 0, 1
        pre_left = [None, None]
        pre_right = [None, None]
        r = zero % 2
        t = k % 2
        pre_left[r] = zero
        pre_right[r] = zero
        vis = set()
        vis.add(zero)
        while head < tail and 0 not in vis:
            step += 1
            min_left = max_right = None
            for now in q[head : tail]:
                now_left = max(now - k, k - now)
                now_right = min(now + k, (n - k) + n - now)
                if min_left is None or min_left > now_left:
                    min_left = now_left
                if max_right is None or max_right < now_right:
                    max_right = now_right

            new_left = new_right = None
            if pre_left[t ^ r] is None:
                for zero in range(min_left, max_right + 1, 2):
                    if zero not in vis:
                        vis.add(zero)
                        q.append(zero)
                        if new_left is None:
                            new_left = zero
                        new_right = zero
            else:
                for zero in range(min_left, max_right + 1, 2):
                    if zero >= pre_left[t ^ r]:
                        break
                    if zero not in vis:
                        vis.add(zero)
                        q.append(zero)
                        if new_left is None:
                            new_left = zero
                
                for zero in range(max_right, min_left - 1, -2):
                    if zero <= pre_right[t ^ r]:
                        break
                    if zero not in vis:
                        vis.add(zero)
                        q.append(zero)
                        if new_right is None:
                            new_right = zero
                
            pre_left[t ^ r] = new_left
            pre_right[t ^ r] = new_right

            r ^= t
            head, tail = tail, len(q)

        if 0 in vis:
            return step
        return -1
''',
    call=f'Solution().minOperations({S0!r}, {K0})',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（红 = 0）', cell=80, h=130,
             color=lambda S, i, v: 'red' if v == '0' else 'green'),
        dict(type='array', var=_zl, label='状态：0 的个数（绿 = 已到达；目标是 0 变绿）', cell=70, h=190,
             pointers={_p_zero: 'pink'}, pointer_labels={_p_zero: 'zero'},
             window=(_p_ml, _p_mr), color=_col),
        dict(type='queue', var='q', label='BFS 队列 q（存的是 0 的个数）', h=100),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=['step', 'r', 't', ('pre_left', 'pre_left', 'cyan'), ('pre_right', 'pre_right', 'orange')],
    skip=['zero = 0', 'pre_right = [None', 'pre_right[r] = zero', 'for c in s', "if c == '0'", 'zero += 1', 'step = 0', 'q = [zero]', 'head, tail = 0, 1', 'pre_left = [None', 'r = zero % 2',
          'pre_left[r] = zero', 'vis = set()', 'min_left = max_right = None', 'if min_left is None', 'if max_right is None',
          'min_left = now_left', 'max_right = now_right', 'new_left = new_right = None', 'if new_left is None', 'if new_right is None',
          'new_left = zero', 'new_right = zero', 'break', 'q.append(zero)', 'for now in q', 'step += 1', 'pre_right[t ^ r] = new_right', 'if zero not in vis'],
    max_steps=100,
    captions={
        'n = len(s)': '`n = {n}`：0 的个数只会在 0 到 `n` 之间',
        'while head < tail': lambda S, B, r: (f'队列还有 `{S.tail - S.head}` 个状态，且 0 还没到过 → 再翻一轮'
                                              if S.head < S.tail and 0 not in S.vis else
                                              ('0 已经到达 → 结束' if 0 in S.vis else '队列空了，0 到不了 → 结束')),
        'now_left = max': '0 的个数为 `{now}`，翻 `k={k}` 个：下界 `max(now-k, k-now) = {now_left}`（0 不够 k 个时，多出来的要翻 1，会再变回 0）',
        'now_right = min': '上界 `min(now+k, 2n-k-now) = {now_right}`（1 不够 k 个时，同理）',
        'if pre_left[t ^ r] is None': lambda S, B, r: (
            '这个奇偶还没扩展过 → 整个区间都要扫' if S['pre_left'][S.t ^ S.r] is None
            else f'这个奇偶以前扩展到 `[{S["pre_left"][S.t ^ S.r]}, {S["pre_right"][S.t ^ S.r]}]` → 只扫两端没处理过的'),
        'for zero in range(min_left, max_right + 1, 2)': '本轮范围 `[{min_left}, {max_right}]`，隔一个取同奇偶的数（范围是步长为 2 的区间）',
        'if zero >= pre_left': lambda S, B, r: (f'`zero = {S.zero}` >= 以前的左边界 `{S.pre_left[S.t ^ S.r]}`：里面扩展过 → break'
                                                if S.zero >= S.pre_left[S.t ^ S.r] else f'`zero = {S.zero}` < 以前的左边界 `{S.pre_left[S.t ^ S.r]}`：在外侧，继续'),
        'for zero in range(max_right': '再从右往左，只处理比以前右边界更大的数',
        'if zero <= pre_right': lambda S, B, r: (f'`zero = {S.zero}` <= 以前的右边界 `{S.pre_right[S.t ^ S.r]}`：里面扩展过 → break'
                                                 if S.zero <= S.pre_right[S.t ^ S.r] else f'`zero = {S.zero}` > 以前的右边界 `{S.pre_right[S.t ^ S.r]}`：在外侧，继续'),
        'vis.add(zero)': lambda S, B, r: (f'数一遍得 `zero = {S.zero}` 个 0，作为 BFS 起点；`q` 是队列，`pre_left/pre_right` 按奇偶记录“以前扩展到的最左/最右”，`vis` 记录到过的状态'
                                          if S['_line'] == 20 else f'`{S.zero}` 第一次到达，标记已访问并入队（本轮 `step = {S.step}` 步）'),
        't = k % 2': '`t = k % 2`：`k` 的奇偶决定每轮扩展出的个数奇偶是否翻转；`r` 是当前状态个数的奇偶',
        'pre_left[t ^ r] = new_left': '本轮新到的最左 `{new_left}`、最右 `{new_right}` 记作这个奇偶的新边界',
        'r ^= t': '`k` 为奇数时，扩展出的 0 的个数奇偶与起点相反：`r` 翻转；`k` 为偶数则不变',
        'head, tail = tail': '下一轮的队列是刚加入的 `q[{head}:{tail}]`',
        'if 0 in vis': lambda S, B, r: ('0 到过了：能全变 1' if 0 in S.vis else '0 没到过：不可能 → 返回 -1'),
        'return step': '最少操作次数 = `step = {step}`',
    },
    cards=dict(
        one_liner='状态只看“0 的个数”，每轮扩展成步长为 2 的区间',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制串 `s`，每次恰好选 `k` 个不同下标翻转，问全变 1 的最少操作次数，不行返回 `-1`',
                 f'本视频：`s = "{S0}", k = {K0}` → `2`',
                 '示例：`s = "110", k = 1` → `1`'],
        quote='若当前有now个0，考虑一次翻转后0的数量：…… now可以扩展到步长为2的区间[now - k, now + k]。',
        quote_src='—— yiduobo 题解原文',
        idea=['翻 `x` 个 0 和 `k-x` 个 1：0 的个数变成 `now + k - 2x`，是步长为 2 的区间',
              '边界要修正：`max(now-k, k-now)` 到 `min(now+k, 2n-k-now)`',
              '照搬 2612 题：记下以前扩展到的最左/最右，每轮只扫外侧；`k` 奇偶决定奇偶是否翻转'],
        summary=['时间 `O(n)`，空间 `O(n)`；起点是 `s` 中 0 的个数，目标是 0',
                 '`k` 为奇数时，每轮扩展出的个数奇偶与起点相反，所以要分奇偶记边界',
                 '本题原文为 Python 2 风格，没有需要改的语法',
                 '对比灵神：灵神用有序集合 BFS 或直接数学公式分 m 奇偶求下界，这里是 BFS 加左右边界'],
    ),
)
