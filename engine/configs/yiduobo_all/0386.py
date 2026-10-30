def _txt(S):
    if 'tmp' not in S or S.get('_line', 0) < 14:
        return f"n = {S.get('n', '')}：先枚举首位 1–9，再往后接一位 0–9"
    return f"`now × 10 + num = {S['now']} × 10 + {S['num']}` = ==`{S['tmp']}`==　（n = {S['n']}）"


CONFIG = dict(
    num=386, title='字典序排数', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='DFS · 前序遍历 trie',
    tags=[],
    code='''
class Solution(object):
    def lexicalOrder(self, n):

        res = []
        for now in range(1, 10):
            if now <= n:
                res.append(now)
                self.dfs(now, n, res)

        return res

    def dfs(self, now, n, res):
        for num in range(10):
            tmp = now * 10 + num
            if tmp <= n:
                res.append(tmp)
                self.dfs(tmp, n, res)
''',
    call='Solution().lexicalOrder(12)',
    expect=[1, 10, 11, 12, 2, 3, 4, 5, 6, 7, 8, 9],
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='res', h=200, label='res（按字典序加入的数）', cell=70,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
        dict(type='calls', h=330, hide=('lexicalOrder',)),
    ],
    watch=[('now', 'now', 'blue'), ('num', 'num', 'cyan'), ('tmp', 'tmp', 'yellow'), ('res', 'res', 'green')],
    skip=['for num in range(10)'],
    max_steps=60,
    captions={
        'res = []': '`res` 按字典序收集结果',
        'for now in range(1, 10)': '先枚举首位 `1 … 9`：每个首位是 trie 的一棵子树，按 1、2、…、9 的顺序走',
        'if now <= n': lambda S, B, r: (f'`{S.now} <= n = {S.n}` → 这棵子树存在' if S.now <= S.n else f'`{S.now} > n = {S.n}` → 太大，不要'),
        'res.append(now)': '先把 `{now}` 加入结果：==父节点排在孩子前面==（前序）→ `{res}`',
        'self.dfs(now, n, res)': '再往下钻：接着看 `{now}0 … {now}9`',
        'tmp = now * 10 + num': '`{now}` 后接 `{num}`：`{now} × 10 + {num}` = =={tmp}==',
        'if tmp <= n': lambda S, B, r: (f'`{S.tmp} <= n = {S.n}` → 合法，是 trie 里的孩子' if S.tmp <= S.n
                                       else f'`{S.tmp} > n = {S.n}` → 越界，孩子不存在，跳过'),
        'res.append(tmp)': '先记下 `{tmp}`，再去找它的孩子 → `{res}`',
        'self.dfs(tmp, n, res)': '递归：下一层处理 `{tmp}` 的孩子 `{tmp}0 … {tmp}9`',
        'return res': '前序遍历完成：`{res}`',
    },
    cards=dict(
        one_liner='把 1 到 n 放进 trie，字典序就是前序遍历',
        complexity='时间 `O(n)` 个有效节点（每个节点多循环 10 次），空间 `O(log n)` 递归栈',
        problem=['给定整数 `n`，把 `1 … n` 按==字典序==排序后返回',
                 '字典序：像字符串一样比，`10` 排在 `2` 前面',
                 '示例：`n = 13` → `[1,10,11,12,13,2,3,4,5,6,7,8,9]`',
                 '本视频：`n = 12`'],
        quote='相邻的项要么具有相同的前缀，要么全然无关从头开始，那么如果将这些数按位放到trie树中，就可以发现题目实际上是要在trie中做一个类似前序遍历的遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['数字按位放进 trie：`1` 的孩子是 `10 … 19`，`10` 的孩子是 `100 … 109`',
              '字典序 = 先父后子、孩子按 `0 … 9` 的顺序 = ==前序遍历==',
              '不用真的建树：搜索时边走边算孩子 `now × 10 + num`，不超过 `n` 才进入'],
        summary=['时间 `O(n)`，空间 `O(log n)`（递归深度 = n 的位数）',
                 '先 `append` 再递归，才是前序；顺序反了就变成后序',
                 '`tmp > n` 时不必递归，直接跳过',
                 '原文代码未改动'],
    ),
)
