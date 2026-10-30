def _info(S):
    I = S['_inner']
    if 'now' not in I or I.get('now') is None or 'now_l_inc' not in I:
        return ''
    nr = I.get('now_r_inc', '—')
    return (f"`{I['now'].val}`：左边 升 `{I['now_l_inc']}` 降 `{I['now_l_dec']}`；右边 升 `{nr}` 降 `{I.get('now_r_dec', '—')}`")


def _col(S, node):
    now = S['_inner'].get('now')
    return 'yellow' if (now is not None and node is now) else None


def _cmp(S, B, r):
    I = S._inner
    a, b = I['now_l_dec'] + I['now_r_inc'] - 1, I['now_l_inc'] + I['now_r_dec'] - 1
    return (f'两种拼法：左降右升 `{I["now_l_dec"]} + {I["now_r_inc"]} - 1 = {a}`，左升右降 `{I["now_l_inc"]} + {I["now_r_dec"]} - 1 = {b}`'
            f' → 取大者 ==`{max(a, b)}`== 去更新 `res`')


CONFIG = dict(
    num=549, title='二叉树中最长的连续序列', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='树形 DP · 升链 / 降链 · 子-父-子拼接',
    tags=['动态规划', '链表树与回溯'],
    code='''
class Solution(object):
    def longestConsecutive(self, root):

        global res
        res = 0

        def dfs(now):
            global res

            now_l_dec = now_l_inc = 1
            if now.left:
                son_l_inc, son_l_dec = dfs(now.left)
                if now.val == now.left.val + 1:
                    now_l_dec = son_l_dec + 1
                elif now.val == now.left.val - 1:
                    now_l_inc = son_l_inc + 1
            
            now_r_dec = now_r_inc = 1
            if now.right:
                son_r_inc, son_r_dec = dfs(now.right)
                if now.val == now.right.val + 1:
                    now_r_dec = son_r_dec + 1
                elif now.val == now.right.val - 1:
                    now_r_inc = son_r_inc + 1
            
            res = max(res, now_l_dec + now_r_inc - 1, now_l_inc + now_r_dec - 1)
            return max(now_l_inc, now_r_inc), max(now_l_dec, now_r_dec)
        
        dfs(root)
        return res
''',
    call='Solution().longestConsecutive(Tr([3,2,4,1,None,None,5]))',
    expect=5,
    skip=['global res', 'res = 0'],
    max_steps=100,
    views=[
        dict(type='tree', var='root', h=300, color=lambda S, node: _col(S, node)),
        dict(type='text', fn=_info, h=60, size=24),
        dict(type='calls', h=170, hide=('root',)),
    ],
    watch=[('l_inc', 'now_l_inc', 'blue'), ('l_dec', 'now_l_dec', 'pink'), ('r_inc', 'now_r_inc', 'cyan'), ('r_dec', 'now_r_dec', 'orange')],
    captions={
        'now_l_dec = now_l_inc = 1': '先当左边没有可接的：`now` 单独算一条长度为 1 的链，左升、左降都是 `1`',
        'if now.left': lambda S, B, r: (f'`{S.now.val}` 有左孩子 `{S.now.left.val}` → 先递归算它的升链、降链' if S.now.left else f'`{S.now.val}` 没有左孩子 → 左边保持 1'),
        'son_l_inc, son_l_dec = dfs': '左孩子返回：以它开头的最长升链 `{son_l_inc}`、降链 `{son_l_dec}`',
        'if now.val == now.left.val + 1': lambda S, B, r: (f'`{S.now.val} == {S.now.left.val} + 1` → 成立：`now` 比左孩子大 1，能接在降链的头部'
                                                           if S.now.val == S.now.left.val + 1 else f'`{S.now.val} == {S.now.left.val} + 1` → 不成立，看另一种'),
        'now_l_dec = son_l_dec + 1': '降链接上 `now`：`now_l_dec = {now_l_dec}`',
        'elif now.val == now.left.val - 1': lambda S, B, r: (f'`{S.now.val} == {S.now.left.val} - 1` → 成立：`now` 比左孩子小 1，能接在升链的头部'
                                                             if S.now.val == S.now.left.val - 1 else f'`{S.now.val}` 和左孩子 `{S.now.left.val}` 不连续 → 左边都不接'),
        'now_l_inc = son_l_inc + 1': '升链接上 `now`：`now_l_inc = {now_l_inc}`',
        'now_r_dec = now_r_inc = 1': '右边同理，先都记 `1`',
        'if now.right': lambda S, B, r: (f'`{S.now.val}` 有右孩子 `{S.now.right.val}` → 递归' if S.now.right else f'`{S.now.val}` 没有右孩子 → 右边保持 1'),
        'son_r_inc, son_r_dec = dfs': '右孩子返回：升链 `{son_r_inc}`、降链 `{son_r_dec}`',
        'if now.val == now.right.val + 1': lambda S, B, r: (f'`{S.now.val} == {S.now.right.val} + 1` → 成立：接降链'
                                                            if S.now.val == S.now.right.val + 1 else f'`{S.now.val} == {S.now.right.val} + 1` → 不成立'),
        'now_r_dec = son_r_dec + 1': '`now_r_dec = {now_r_dec}`',
        'elif now.val == now.right.val - 1': lambda S, B, r: (f'`{S.now.val} == {S.now.right.val} - 1` → 成立：接升链'
                                                              if S.now.val == S.now.right.val - 1 else f'`{S.now.val}` 和右孩子 `{S.now.right.val}` 不连续 → 右边都不接'),
        'now_r_inc = son_r_inc + 1': '`now_r_inc = {now_r_inc}`',
        'res = max': _cmp,
        'return max(now_l_inc': '向上返回：最长升链 `{max(now_l_inc, now_r_inc)}`，最长降链 `{max(now_l_dec, now_r_dec)}`',
        'dfs(root)': '从根开始递归',
        'return res': '最长连续序列长度 `{ret}`',
    },
    cards=dict(
        one_liner='把「子-父-子」拆成：左升右降 或 左降右升',
        complexity='时间 `O(n)`，空间 `O(h)`',
        problem=['二叉树里，求最长的连续序列路径长度：相邻值差 1，可以递增也可以递减',
                 '路径可以先上后下（子-父-子），不必从上往下',
                 '本视频：`[3,2,4,1,null,null,5]` → `5`（`1-2-3-4-5`）'],
        quote='可以将其拆分成父-左子以及父-右子的组合，更具体的，又可以分为左升右降和左降右升……使用这两组中较长的那一组更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dfs(now)` 返回两个数：以 now 开头往下的最长升链、最长降链',
              '孩子值恰好 ±1，就把 now 接在孩子那条链的头上，长度加 1',
              '左升 + 右降（或左降 + 右升）合起来是一条经过 now 的路径，长度要减掉重复的 now'],
        summary=['时间 `O(n)`，空间 `O(h)`',
                 '拼接长度 `a + b - 1`：`now` 被左右两边各数了一次',
                 '`if` 和 `elif` 互斥：差 +1 与差 -1 不会同时成立',
                 '先递归再用孩子的结果；没有孩子时升降都是 1',
                 '原文是 Python 2 风格的类写法，代码无需改动即可运行'],
    ),
)
