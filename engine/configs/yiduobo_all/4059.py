def _fmt_group(g):
    return '{' + ','.join(str(p) if lv is None else str(p) for p, lv in g) + '}'


def _stack_txt(S):
    st = S.get('stack')
    if st is None:
        return ''
    return '栈（右端是队首）：`' + (' '.join('[' + ','.join(f'{p}@{lv}' for p, lv in g) + ']' for g in st) or '（空）') + '`'


def _tmp_txt(S):
    t = S.get('tmp')
    if t is None:
        return ''
    return '暂存 tmp：`' + (' '.join('[' + ','.join(f'{p}@{lv}' for p, lv in g) + ']' for g in t) or '（空）') + '`'


def _node_color(S, i, v):
    if 'index' in S and 'level' in S and S.get('_line') is not None:
        if i == S['index'] << 1:
            return 'yellow'
    return 'green' if v else None


CONFIG = dict(
    num=4059, title='字典序最大的答案数组', difficulty='Hard', category='位运算',
    author='yiduobo', technique='分组 + 满二叉 trie 统计',
    tags=[],
    code='''
class Solution(object):
    def largestPower(self, nums):
        
        ma = max(nums)
        m = 1
        h = 1
        while m <= ma:
            m <<= 1
            h += 1
        
        f = [0] * (m * 2)
        for v in nums:
            f[-v - 1] += 1
        
        now = m >> 1
        while now > 0:
            for index in range(now, now << 1):
                f[index] = f[index << 1] + f[index << 1 | 1]
            now >>= 1
            
        res = []
        stack = [[(1, 0)]]
        tmp = []
        for level in range(h - 1):
            res.append(0)
            while stack:
                interval = stack.pop()
                cnt = 0
                one = []
                zero = []
                for p_index, p_level in interval:
                    level_diff = level - p_level
                    start = p_index << level_diff
                    for index in range(start, start + (1 << level_diff), 1):
                        res[-1] += f[index << 1]
                        if f[index << 1] == f[index]:
                            one.append(index << 1)
                        elif f[index << 1] == 0:
                            zero.append(index << 1 | 1)
                        else:
                            one.append(index << 1)
                            zero.append(index << 1 | 1)
                
                if one:
                    tmp.append([(index, level + 1) for index in one])

                if zero:
                    tmp.append([(index, level + 1) for index in zero])
                    break
            
            while tmp:
                stack.append(tmp.pop())

        return [0] * (15 - len(res)) + res
''',
    call='Solution().largestPower([7,5,2,1])',
    expect=[0] * 12 + [2, 1, 3],
    views=[
        dict(type='array', var='f', cell=50, label='f：满二叉树的权重（叶子 8..15 对应 7..0，值越大越靠左）', h=170,
             color=_node_color),
        dict(type='text', fn=_stack_txt, size=28, h=70),
        dict(type='text', fn=_tmp_txt, size=28, h=70),
        dict(type='array', var='res', cell=64, label='res（从最高位往低位逐位追加）', h=170,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('level', 'level', 'blue'), ('index', 'index', 'yellow'), ('one', 'one', 'green'), ('zero', 'zero', 'pink')],
    captions={
        'ma = max(nums)': '先找最大值 `{ma}`，决定树要建多大',
        'while m <= ma': lambda S, B, r: (f'`m = {S.m}` ≤ `{S.ma}`，二的幂还不够大 → 继续翻倍' if S.m <= S.ma
                                          else f'`m = {S.m}` > `{S.ma}`：`m` 就是不小于最大值的二的幂，树有 `{S.m}` 个叶子'),
        'f = [0] * (m * 2)': '满二叉树用数组存：根是 `1` 号，孩子是 `index << 1` 和 `index << 1 | 1`',
        'f[-v - 1] += 1': '值 `{v}` 的次数记到叶子 `{2*m - v - 1}`：==反过来放==，这样「该位为 1」的都在左边',
        'f[index] = f[index << 1]': '`f[{index}] = f[{index*2}] + f[{index*2+1}]` = {f[index]}，自底向上求权重',
        'now >>= 1': '上移一层',
        'res = []': '`res` 一位一位往里填',
        'stack = [[(1, 0)]]': '分组只有一个：根节点 `1`（高度 0），整组无序',
        'for level in range': '处理第 `{level}` 层（对应从高位数第 {level+1} 位）',
        'res.append(0)': '这一位的答案先记 0，后面累加',
        'while stack': lambda S, B, r: ('栈里还有组 → 取队首处理' if S.stack else '栈空了，这一位处理完'),
        'interval = stack.pop()': '取出队首这一组：`{interval}`',
        'level_diff = level': '这个节点是第 `{p_level}` 层的，要往下覆盖 `{level_diff}` 层才到当前层（被截断的组留在高处）',
        'start = p_index': '当前层对应的最左节点是 `{start}`',
        'res[-1] += f[index << 1]': '左孩子 `{index*2}` 权重 `{f[index*2]}`（该位为 1 的个数）→ 全 1 前缀累计 `res[-1] = {res[-1]}`',
        'if f[index << 1] == f[index]': lambda S, B, r: (f'左孩子权重 `{S.f[S.index*2]}` == 本节点 `{S.f[S.index]}` → ==全是 1==，不用拆，进 `one`'
                                                        if S.f[S.index*2] == S.f[S.index] else f'左孩子 `{S.f[S.index*2]}` ≠ 本节点 `{S.f[S.index]}` → 不是全 1'),
        'elif f[index << 1] == 0': lambda S, B, r: ('左孩子权重为 0 → ==全是 0==，整组进 `zero`（右孩子）' if S.f[S.index*2] == 0
                                                    else '有 0 有 1 → 要拆成两半'),
        'one.append(index << 1)': '1 的一半（左孩子 `{index*2}`）放前面',
        'zero.append(index << 1 | 1)': '0 的一半（右孩子 `{index*2+1}`）放后面',
        'if one': '有 1 的节点：单独成一个新组，先暂存到 `tmp`',
        'tmp.append([(index, level + 1) for index in one])': '`tmp` 加入 1 的组：`{tmp[-1]}`',
        'if zero': lambda S, B, r: ('有 0 的节点 → ==这里出现截断==，后面的组不用在这一位处理' if S.zero
                                    else '没有 0，全是 1 → ==没有截断==，继续看栈里下一组'),
        'tmp.append([(index, level + 1) for index in zero])': '0 的组紧跟其后：`{tmp[-1]}`',
        'while tmp': '把 `tmp` 倒回 `stack`，保持原先后顺序，给下一位用',
        'stack.append(tmp.pop())': '`stack` 回填，右端是队首',
        'return [0] * (15 - len(res)) + res': '前面补 0 到 15 位：`{ret}`',
    },
    skip=['cnt = 0', 'one = []', 'zero = []', 'level_diff =', 'start =', 'break', 'now >>= 1', 'm <<= 1', 'interval = stack.pop()', 'for v in nums', 'for index in range(now', 'while now > 0', 'now = m >> 1', 'for p_index', 'for index in range(start', 'while tmp', 'stack.append(tmp.pop())', 'tmp = []', 'while stack'],
    max_steps=140,
    cards=dict(
        one_liner='把元素分组，只拆被 0 截断处，用 trie 一次数清',
        complexity='时间 `O(n + U)`，空间 `O(U)`',
        problem=['重排 `nums`，`power[i]` = 第 `14-i` 位全为 1 的最长前缀长度',
                 '要 `power` 字典序最大，高位优先',
                 '示例：`[7,5,2,1]` → 末三项 `[2,1,3]`'],
        quote='组间有序，但是组内依然保持无序。另外，这种情况同样出现了截断，因此无需考虑后续的组。',
        quote_src='—— yiduobo 题解',
        idea=['从 `[7,5,2,1]` 一个大组开始，逐位拆组：1 的在前、0 的在后',
              '某组出现 0，说明 1 的前缀在此截断，后面的组保持无序',
              '用满二叉 trie 的权重判断「全 1 / 全 0 / 有 0 有 1」，不必逐个看元素'],
        summary=['作者先讲 `O(n log U)` 的分组，再优化到哈希计数、再到 trie 的 `O(n + U)`，这里演示 trie 版',
                 '原文代码已是 Python 3 可运行，未改动',
                 '易错：被截断的组留在高层，处理低位时要用 `level_diff` 向下覆盖',
                 '用栈当队列：先放 `tmp`，再倒回 `stack` 保持顺序'],
    ),
)
