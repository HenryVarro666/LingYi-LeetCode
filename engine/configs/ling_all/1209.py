TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

# 代码行号（第 1 行是 class Solution）：7 append / 9 pop / 11 += 1，执行完这三行才算 s[k] 处理完毕
DONE_LINES = (7, 9, 11)


def _cur(S):
    s = S.get('s')
    k = getattr(s, 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _upto(S):
    """已处理完的字符个数"""
    s = S.get('s')
    k = getattr(s, 'k', -1)
    if k == -1:
        return 0
    if k is None:
        return len(s)
    return k + 1 if S['_line'] in DONE_LINES else k


def _alive(s, K, upto):
    """模拟算法，返回仍留在栈里的字符下标（只用于画图）"""
    st = [('', [])]
    for i in range(upto):
        c = s[i]
        if st[-1][0] != c:
            st.append((c, [i]))
        elif len(st[-1][1]) == K - 1:
            st.pop()
        else:
            st[-1][1].append(i)
    return {j for _, idxs in st for j in idxs}


def _dim(S, i, v):
    s = S.get('s')
    if s is None or 'k' not in S:
        return False
    u = _upto(S)
    return i < u and i not in _alive(str(s), S['k'], u)


def _top(S):
    t = S['st'][-1][0]
    return '哨兵' if t == '' else f'`"{t}"`'


def _txt(S):
    st = S.get('st')
    if st is None:
        return f"每次删掉连续 `{S['k']}` 个相同字母，删除后两边会接到一起，可能引发连锁消除"
    cur = ''.join(c * n for c, n in st)
    return f"栈还原成的字符串：`{cur}`" if cur else '栈还原成的字符串：（空，只剩哨兵）'


def _for(S, B, ret):
    if getattr(S.s, 'k', None) is None:
        return '`s` 遍历完了，开始拼接答案'
    return f'取第 `{S.s.k}` 个字符 `ch = "{S.ch}"`'


def _if1(S, B, ret):
    if S.st[-1][0] != S.ch:
        return f'`ch = "{S.ch}"` 与栈顶 {_top(S)} ==不同== → 连续段断了，要开一个新段'
    return f'`ch = "{S.ch}"` 与栈顶 {_top(S)} ==相同== → 连续段在变长，看看够不够 `k` 个'


def _if2(S, B, ret):
    t, c = S.st[-1]
    if c == S.k - 1:
        return f'栈顶 `"{t}"` 已有 `{c}` 个 = `k - 1`，再算上当前这个就是 ==k 个== → 可以消除'
    return f'栈顶 `"{t}"` 只有 `{c}` 个 < `k - 1 = {S.k - 1}`，凑不够 `k` 个 → 只能计数加一'


CONFIG = dict(
    num=1209, title='删除字符串中的所有相邻重复项 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 压缩连续字母计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1542'],
    code='''
class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        st = [['', 0]]  # 加个哨兵，无需判断栈是否为空

        for ch in s:
            if st[-1][0] != ch:  # ch 与栈顶字母不同
                st.append([ch, 1])  # 计数器从 1 开始
            elif st[-1][1] == k - 1:  # 连续 k 个相同字母
                st.pop()  # 消除
            else:  # 相同但无法消除
                st[-1][1] += 1  # 只需把计数器增加 1

        return ''.join(ch * cnt for ch, cnt in st)
''',
    setup=TRACK,
    call='Solution().removeDuplicates(Tracked("deeedbbbdaa"), 3)',
    expect='aa',
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（灰色 = 已被消除的字母）', h=260, cell=80,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'ch'}, dim=_dim),
        dict(type='stack', var='st', label='st（每段 = 字母×连续次数）', h=190, font=36,
             fmt=lambda p: '哨兵' if p[0] == '' else f'{p[0]}×{p[1]}'),
        dict(type='text', fn=_txt, size=30, h=130),
    ],
    watch=[('ch', 'ch', 'blue'), ('k', 'k', 'yellow'), ('栈顶', 'st[-1]', 'purple'), ('段数', 'len(st) - 1', 'green')],
    max_steps=75,
    captions={
        'st = [[': '栈里存 ==[字母, 连续出现次数]==；先放一个哨兵 `["", 0]`，这样 `st[-1]` 永远存在，不用判空',
        'for ch in s': _for,
        'if st[-1][0] != ch': _if1,
        'st.append([ch, 1])': '新开一段入栈，计数器从 `1` 开始：`["{ch}", 1]`',
        'elif st[-1][1] == k - 1': _if2,
        'st.pop()': '连续 `k` 个 `"{B.st[-1][0]}"`（栈里 `{B.st[-1][1]}` 个 + 当前 1 个）→ ==整段消除==，弹出栈顶',
        'st[-1][1] += 1': '相同但还凑不够 `k` 个 → 栈顶计数加一：`"{st[-1][0]}"` 现在连续 `{st[-1][1]}` 个',
        'return': '把每段还原成 `字母 × 次数` 再拼起来，返回 =={ret}==',
    },
    cards=dict(
        one_liner='栈里不存单个字母，存「字母 + 连续次数」，数到 k 就整段弹出',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次删掉 `s` 中 `k` 个相邻且相等的字母，删完左右两边会接起来；重复到不能删为止',
                 '示例：`s = "deeedbbcccbdaa"`，`k = 3` → `"aa"`',
                 '本视频用 `"deeedbbbdaa"`：删掉 `eee`、`bbb` 后 `ddd` 才靠到一起，==连锁消除== → `"aa"`'],
        quote='为快速判断能否消除，栈中不能只存字符，而是要存字符连续出现的次数（相当于==压缩==了连续出现的字符）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每次回头检查栈顶 `k - 1` 个字母，时间 `O(nk)`，太慢',
              '把连续相同的字母压成一段：栈里存二元组 `(字母, 次数)`',
              '分三种情况：字母不同 → 新段入栈；次数已是 `k - 1` → 弹出；否则次数加一'],
        result='栈里只剩 `a×2`，还原成 `"aa"` ✓',
        after=[dict(heading='相关题目', lines=[
            '`k = 2` 的特例是 1047 删除字符串中的所有相邻重复项，建议先做',
            '相似题：3703 移除 K-平衡子字符串',
            '都属于题单「§3.3 邻项消除」：消除后左右相邻，==后进先出== → 栈'])],
        summary=['时间 `O(n)`：每个字母至多入栈、出栈各一次；空间 `O(n)`',
                 '易错：判断的是 `cnt == k - 1`（再加当前这个才满 `k` 个），不是 `== k`',
                 '哨兵 `["", 0]` 省去判空；与哨兵比较时字母一定不同，会直接新开一段',
                 '最后别忘了用 `ch * cnt` 把压缩的段还原成字符串'],
    ),
)
