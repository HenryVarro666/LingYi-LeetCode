S_TREE = [1, 1, None, 1]
T_TREE = [1, 1]


def _phase(S):
    line = S.get('_line') or 0
    if 9 <= line <= 16:
        return 1
    if line >= 18 and line <= 27:
        return 2
    return 0


def _idx(S):
    return S.get('index') if isinstance(S.get('index'), int) else None


def _p1(S):
    return _idx(S) if _phase(S) == 1 else None


def _p2(S):
    return _idx(S) if _phase(S) == 2 else None


def _s_color(S, i, v):
    if _phase(S) != 2 or _idx(S) is None:
        return None
    idx, pos = _idx(S), S['pos']
    line = S.get('_line')
    end = idx if line in (22, 23, 24, 25) else idx - 1  # 本轮 if 之后，s[index] 已经参与匹配
    if end - pos + 1 <= i <= end and pos > 0:
        return 'green'
    if i == idx:
        return 'orange'
    return None


def _t_color(S, i, v):
    ph, pos = _phase(S), S.get('pos')
    if not isinstance(pos, int):
        return None
    if ph == 2:
        return 'green' if i < pos else ('orange' if i == pos and _idx(S) is not None else None)
    if ph == 1 and _idx(S) is not None:
        if i == _idx(S):
            return 'orange'
        if i < pos:
            return 'cyan'
    return None


def _cap_while1(S, B, ret):
    pos, i, t = S.pos, S.index, S.t_list
    if pos > 0 and t[pos] != t[i]:
        return f'`t[{pos}] = {t[pos]}` ≠ `t[{i}] = {t[i]}`：失配，`pos` 退回 `f[{pos - 1}] = {S.f[pos - 1]}`'
    return f'`pos = {pos}`' + ('，不用回退' if pos == 0 else f'，`t[{pos}] = t[{i}]`，不用回退')


def _cap_if1(S, B, ret):
    pos, i, t = S.pos, S.index, S.t_list
    if t[pos] == t[i]:
        return f'`t[{pos}] = t[{i}] = {t[i]}` → 相同前后缀长度 +1：`pos` → {pos + 1}'
    return f'`t[{pos}] = {t[pos]}` ≠ `t[{i}] = {t[i]}` → 长度保持 `{pos}`'


def _cap_while2(S, B, ret):
    pos, i, t, sl = S.pos, S.index, S.t_list, S.s_list
    if pos > 0 and t[pos] != sl[i]:
        return (f'`t[{pos}] = {t[pos]}` ≠ `s[{i}] = {sl[i]}`：失配！不从头来，'
                f'`pos` 退到 `f[{pos - 1}] = {S.f[pos - 1]}`（==KMP 跳转==）')
    if pos == 0:
        return f'`pos = 0`，直接比较 `t[0]` 和 `s[{i}]`'
    return f'`t[{pos}] = s[{i}] = {sl[i]}`，不用回退'


def _cap_if2(S, B, ret):
    pos, i, t, sl = S.pos, S.index, S.t_list, S.s_list
    if t[pos] == sl[i]:
        return f'`t[{pos}] = s[{i}] = {sl[i]}` → 匹配长度 +1：`pos` → {pos + 1}'
    return f'`t[{pos}] = {t[pos]}` ≠ `s[{i}] = {sl[i]}` → 匹配长度为 0'


CONFIG = dict(
    num=572, title='另一棵树的子树', difficulty='Easy', category='二叉树',
    author='yiduobo', technique='带空节点的前序序列 + KMP 子串匹配',
    tags=['热题173'],
    code='''
class Solution(object):
    def isSubtree(self, s, t):
        s_list = self.dfs(s)
        t_list = self.dfs(t)

        m = len(s_list)
        n = len(t_list)

        pos = 0
        f = [0]
        for index in range(1, n):
            while pos > 0 and t_list[pos] != t_list[index]:
                pos = f[pos - 1]
            if t_list[pos] == t_list[index]:
                pos += 1
            f.append(pos)

        pos = 0
        for index in range(m):
            while pos > 0 and t_list[pos] != s_list[index]:
                pos = f[pos - 1]
            if t_list[pos] == s_list[index]:
                pos += 1
            if pos == n:
                return True

        return False

    def dfs(self, now):
        ret = [str(now.val)]
        if now.left:
            ret.extend(self.dfs(now.left))
        else:
            ret.append('#')
        if now.right:
            ret.extend(self.dfs(now.right))
        else:
            ret.append('$')

        return ret
''',
    call=f'Solution().isSubtree(Tr({S_TREE}), Tr({T_TREE}))',
    expect=True,
    views=[
        dict(type='tree', label='左：s　右：t（序列化：根、左子树、右子树，空左 #、空右 $）', h=185, path=False),
        dict(type='array', var='s_list', label='s_list（绿 = 已经和 t 匹配上的一段）', cell=72, h=165,
             pointers={_p2: 'orange'}, pointer_labels={_p2: 'index'}, color=_s_color),
        dict(type='array', var='t_list', label='t_list（pos = 已匹配长度 / 当前前后缀长度）', cell=72, h=180,
             pointers={'pos': 'pink', _p1: 'orange'}, pointer_labels={_p1: 'index'}, color=_t_color),
        dict(type='array', var='f', label='f（前缀函数：失配时 pos 退回 f[pos-1]）', cell=72, h=96),
    ],
    watch=[('index', 'index', 'orange'), ('pos', 'pos', 'pink'), ('n', 'n')],
    skip=list(range(30, 41)) + ['m = len(s_list)', 15, 23],
    captions={
        's_list = self.dfs(s)': '把 s 前序序列化，空的左儿子记 `#`、空的右儿子记 `$`（dfs 内部步骤略）',
        't_list = self.dfs(t)': lambda S, B, ret: f's 序列化完成：`s_list = {S.s_list}`；同样序列化 t',
        'n = len(t_list)': lambda S, B, ret: f'`t_list = {S.t_list}`，长度 `n = {S.n}`',
        9: 'KMP 第一步：求 `t_list` 的前缀函数 `f`，`f[0] = 0`',
        'f = [0]': '`f = [0]`',
        'for index in range(1, n)': lambda S, B, ret: (f'计算 `f[{S.index}]`' if S.get('index') != B.get('index') or 'index' not in B
                                                       else f'前缀函数求好了：`f = {S.f}`'),
        'while pos > 0 and t_list[pos] != t_list[index]': _cap_while1,
        13: '`pos` 退回 `{pos}`',
        'if t_list[pos] == t_list[index]': _cap_if1,
        'f.append(pos)': '`f[{index}] = {pos}`',
        18: 'KMP 第二步：在 `s_list` 上匹配，`pos` 从 0 开始',
        'for index in range(m)': lambda S, B, ret: (f'读入 `s_list[{S.index}] = {S.s_list[S.index]}`' if S.get('index') != B.get('index') or B.get('_line') != 19
                                                    else '扫完了'),
        'while pos > 0 and t_list[pos] != s_list[index]': _cap_while2,
        21: '`pos` 退回 `{pos}`：`t_list` 的前 `{pos}` 个仍然和 s 的末尾对得上',
        'if t_list[pos] == s_list[index]': _cap_if2,
        'if pos == n': lambda S, B, ret: (f'`pos == n = {S.n}`：整个 `t_list` 都匹配上了！' if S.pos == S.n
                                          else f'`pos = {S.pos} < {S.n}`，继续'),
        'return True': 't 的序列是 s 序列的连续一段 → ==t 是 s 的子树==，返回 True',
        'return False': '没找到，返回 False',
    },
    max_steps=60,
    cards=dict(
        one_liner='把两棵树都序列化成带空节点的前序序列，再用 KMP 判断是不是连续子串',
        complexity='时间 `O(|s| + |t|)`，空间 `O(|s| + |t|)`',
        problem=['给你两棵二叉树 `s` 和 `t`，判断 `s` 中是否有一棵子树与 `t` ==结构和节点值都相同==',
                 '子树 = 某个节点和它的==所有后代==',
                 '示例：`s = [3,4,5,1,2]`，`t = [4,1,2]` → `true`',
                 f'本视频：`s = [1,1,null,1]`（一条左链），`t = {T_TREE}` → `true`'],
        quote='由于==一棵树的子树其dfs序在整棵树的dfs序中是连续的==，因此在这里可以按前序遍历的顺序对s和t分别求出其包含空节点的dfs序，然后若t的dfs序是s的dfs序的子序列，那么就说明t是s的子树。',
        quote_src='—— yiduobo 题解（文中“子序列”指连续的一段）',
        idea=['只有前序序列确定不了树形；==把空节点也写进去==就能确定',
              '空节点还要区分左右：左空记 `#`、右空记 `$`',
              '例：`s` 的前两个节点也是 `1,1`，但下面还有节点 → 序列里 `#` 对不上，不会误判',
              '判断连续子串用 KMP：失配时 `pos = f[pos-1]`，不用回头'],
        result='在 s 的第二个 1 处匹配成功：中间那棵子树就是 t ✓',
        summary=['时间 `O(|s| + |t|)`：序列化线性，KMP 线性',
                 '必须记录空节点，且左右要区分，否则不同的树序列可能相同',
                 'KMP 前缀函数：`f[i]` 是 `t[0..i]` 最长相同真前后缀的长度',
                 '原文为 Python 2 风格，仅删去文档字符串和 LeetCode 模板注释，代码未改',
                 '对比灵神：灵神按高度剪枝后逐个比较，这里转成字符串匹配'],
    ),
)
