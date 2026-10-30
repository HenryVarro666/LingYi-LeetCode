def _col(S, n):
    if n.val in S.get('res', []):
        return 'green'
    if any(x is n for x in S.get('mi', [])):
        return 'blue'
    if any(x is n for x in S.get('ma', [])):
        return 'pink'
    return None


def _top(S):
    mi, ma, t = S.get('mi'), S.get('ma'), S.get('target')
    if mi is None or ma is None:
        return ''
    a = f"mi 栈顶 `{mi[-1].val}`（距 {abs(mi[-1].val - t):.1f}）" if mi else 'mi 为空'
    b = f"ma 栈顶 `{ma[-1].val}`（距 {abs(ma[-1].val - t):.1f}）" if ma else 'ma 为空'
    return f'`target = {t}`：{a}　{b}'


def _choose(S, B, r):
    mi, ma, t = S.mi, S.ma, S.target
    if not mi:
        return '`mi` 空了 → 只能选 ma'
    if not ma:
        return '`ma` 空了 → 只能选 mi'
    dm, dM = abs(mi[-1].val - t), abs(ma[-1].val - t)
    if dM < dm:
        return f'`ma` 栈顶 {ma[-1].val} 距 {dM:.1f} < `mi` 栈顶 {mi[-1].val} 距 {dm:.1f} → ==选 ma=='
    return f'`ma` 栈顶 {ma[-1].val} 距 {dM:.1f} ≥ `mi` 栈顶 {mi[-1].val} 距 {dm:.1f} → ==选 mi=='


CONFIG = dict(
    num=272, title='最接近的二叉搜索树值 II', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='两个栈 mi / ma · 中序前驱后继',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def closestKValues(self, root, target, k):

        mi = []
        ma = []
        now = root
        res = []

        while now:
            if now.val > target:
                ma.append(now)
                now = now.left
            else:
                mi.append(now)
                now = now.right
        
        while k > 0:
            choose_mi = False

            if not mi:
                if not ma:
                    break
                else:
                    choose_mi = False
            elif not ma:
                choose_mi = True
            elif abs(ma[-1].val - target) < abs(mi[-1].val - target):
                choose_mi = False
            else:
                choose_mi = True
            
            if choose_mi:
                res.append(mi[-1].val)
                now = mi[-1].left
                mi.pop()
                while now:
                    mi.append(now)
                    now = now.right
            
            else:
                res.append(ma[-1].val)
                now = ma[-1].right
                ma.pop()
                while now:
                    ma.append(now)
                    now = now.left
            
            k -= 1
        
        return res
''',
    call='Solution().closestKValues(Tr([8,4,12,2,6,10,14,1,3,5,7]), 5.3, 3)',
    expect=[5, 6, 4],
    views=[
        dict(type='tree', var='root', pointers={'now': 'yellow'}, path=False, h=300,
             color=_col),
        dict(type='stack', var='mi', fmt=lambda n: str(n.val), label='mi（蓝：比 target 小的候选，栈顶最大）', h=120),
        dict(type='stack', var='ma', fmt=lambda n: str(n.val), label='ma（粉：比 target 大的候选，栈顶最小）', h=120),
        dict(type='array', var='res', label='res（绿）', h=150, cell=60),
        dict(type='text', h=60, fn=_top, size=26),
    ],
    watch=[('target', 'target', 'orange'), ('k', 'k', 'cyan'), ('choose_mi', 'choose_mi', 'purple'), ('res', 'res', 'green')],
    captions={
        'mi = []': '`mi` 存比 target 小的节点，`ma` 存比 target 大的节点',
        'now = root': '先像 270 题一样，从根向下找 target 的位置',
        'while now:': lambda S, B, r: (f'`now = {S.now.val}` → 继续向下' if S.now else '这一层走到头了'),
        'if now.val > target': lambda S, B, r: (f'`{S.now.val} > {S.target}`：偏大的节点，放进 ==ma==' if S.now.val > S.target
                                              else f'`{S.now.val} ≤ {S.target}`：偏小的节点，放进 ==mi=='),
        'ma.append(now)': '`ma` 压入 `{now.val}` → {[x.val for x in ma]}（越往下越小）',
        'mi.append(now)': '`mi` 压入 `{now.val}` → {[x.val for x in mi]}（越往下越大）',
        'now = now.left': '偏大 → 往左找更小的',
        'now = now.right': '偏小 → 往右找更大的',
        'while k > 0': lambda S, B, r: (f'还需要 `k = {S.k}` 个数 → 从两个栈顶里挑更近的' if S.k > 0 else '`k = 0`：已经找够了 → 退出循环'),
        18: '每轮先默认 `choose_mi = False`',
        20: lambda S, B, r: ('`mi` 为空 → 左边没有候选了' if not S.mi else '`mi` 非空 → 左边还有候选，继续看 ma'),
        22: lambda S, B, r: ('`ma` 也空了 → 没有数可选，提前结束' if not S.ma else '`ma` 非空 → 只能选 ma'),
        25: lambda S, B, r: ('`ma` 空了 → 只能选 mi' if not S.ma else '`ma` 非空，两边都有候选 → 比较距离'),
        28: '`ma` 更近 → `choose_mi` 保持 False',
        'elif abs': _choose,
        30: '`mi` 更近（或一样近）→ `choose_mi = True`',
        'res.append(mi[-1].val)': '`mi` 栈顶最接近 → 收进答案：`res = {res}`',
        'now = mi[-1].left': lambda S, B, r: (f'接着要补「比 {S.mi[-1].val} 小的最大值」→ 它在左子树的最右侧，先看左孩子 ' + (f'`{S.now.val}`' if S.now else '：没有左孩子，不用额外处理')),
        'mi.pop()': '弹出已选的 `mi` 栈顶 → {[x.val for x in mi]}',
        'res.append(ma[-1].val)': '`ma` 栈顶最接近 → 收进答案：`res = {res}`',
        'now = ma[-1].right': lambda S, B, r: (f'接着要补「比 {S.ma[-1].val} 大的最小值」→ 它在右子树的最左侧，先看右孩子 ' + (f'`{S.now.val}`' if S.now else '：没有右孩子，不用额外处理')),
        'ma.pop()': '弹出已选的 `ma` 栈顶 → {[x.val for x in ma]}',
        'k -= 1': '又找到一个，`k = {k}`',
        'return res': '`k` 个最接近的值：`{res}`',
    },
    cards=dict(
        one_liner='两个栈保存查找路径，每轮取更近的栈顶再补一个',
        complexity='时间 `O(h + k·h)`，空间 `O(h)`',
        problem=['给一棵二叉搜索树、目标值 `target` 和整数 `k`',
                 '返回 BST 中==最接近 target 的 k 个值==（顺序任意）',
                 '示例：BST `[8,4,12,2,6,10,14,1,3,5,7]`，`target = 5.3`，`k = 3` → `[5,6,4]`'],
        quote='可以使用两个栈mi和ma分别储存在查找过程中遇到的比target小以及比target大的数。接下来，最接近target数应该是mi栈顶和ma栈顶这二者中里target更近的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['先按 270 题往下查找：偏小的进 `mi`，偏大的进 `ma`',
              '两个栈顶就是 target 左右最近的两个数',
              '取走一个后，补上它的前驱 / 后继：沿子树最右（最左）一路入栈',
              '重复 `k` 轮，不用整棵树排序'],
        summary=['时间 `O(h + k·h)`（平均每个节点只入出栈一次，摊销 `O(h + k)`），空间 `O(h)`',
                 '`mi` 弹出后补左子树最右一路，`ma` 弹出后补右子树最左一路，别写反',
                 '某个栈为空时只能选另一个；两个都空就 `break`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
