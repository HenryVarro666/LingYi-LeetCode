CONFIG = dict(
    num=1161, title='最大层内元素和', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='层序遍历 · 数组下标 l/r 划分层',
    tags=['难度分 1250'],
    code='''
class Solution(object):
    def maxLevelSum(self, root):

        max_s = root.val
        res = 1
        q = [root]
        l = 0
        r = 1
        level = 0
        while l < r:
            s = 0
            level += 1
            for now in q[l : r]:
                s += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            if s > max_s:
                max_s = s
                res = level
            
            l, r = r, len(q)
        
        return res
''',
    call='Solution().maxLevelSum(Tr([1,7,0,7,-8,None,None]))',
    expect=2,
    views=[
        dict(type='tree', label='二叉树（蓝 = 当前累加的节点）', pointers={'now': 'blue'}, path=False, h=280),
        dict(type='text', fn=lambda S: ('队列 `q = ' + str([x.val for x in S['q']]) + '`') if 'q' in S else '', size=26, h=56),
        dict(type='text', fn=lambda S: (f"当前层下标 `[{S['l']}, {S['r']})`，层和 `s = {S.get('s')}`") if 'l' in S else '', size=26, h=56),
    ],
    watch=[('level', 'level', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('s', 's'), ('max_s', 'max_s', 'cyan'), ('res', 'res', 'green')],
    captions={
        'level = 0': '`level` 当前层号，每层开始时先 +1',
        'l = 0': '`l` 是当前层在 `q` 里的起点',
        'max_s = root.val': '`max_s` 初值取根的值 `{max_s}`（第 1 层的和）',
        'res = 1': '`res` 记最大和的层号，先假设是第 `1` 层',
        'q = [root]': '`q` 是一个只增不减的数组，按层顺序存所有节点',
        'r = 1': '`r` 是当前层的终点（不含）：第 1 层就是 `q[0:1]`',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`：这一层有节点 → 处理' if S.l < S.r else f'`l = {S.l} ≥ r = {S.r}`：没有下一层了 → 结束'),
        's = 0': '本层和清零',
        'level += 1': '现在处理第 `{level}` 层',
        's += now.val': '`s += {now.val}` → 层和 `{s}`',
        'if now.left': lambda S, B, r_: (f'`{S.now.val}` 有左儿子 `{S.now.left.val}` → 追加到 `q` 末尾' if S.now.left else f'`{S.now.val}` 没有左儿子'),
        'if now.right': lambda S, B, r_: (f'`{S.now.val}` 有右儿子 `{S.now.right.val}` → 追加到 `q` 末尾' if S.now.right else f'`{S.now.val}` 没有右儿子'),
        'if s > max_s': lambda S, B, r_: (f'第 `{S.level}` 层和 `{S.s}` > `max_s = {S.max_s}` → 更新' if S.s > S.max_s else f'第 `{S.level}` 层和 `{S.s}` ≤ `max_s = {S.max_s}` → 不更新'),
        'max_s = s': '`max_s = {max_s}`',
        'res = level': '最大和暂时在第 `{level}` 层 → `res = {res}`',
        'l, r = r, len(q)': '下一层 = 本层结束位置到 `q` 末尾：`l = {l}`, `r = {r}`',
        'return res': '最大层和 `{max_s}` 在第 `{res}` 层 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='按题意层序遍历，每层求和，取其中最大的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['根节点在第 `1` 层，返回==层内元素和最大==的层号',
                 '同分时返回最小层号',
                 '示例：`[1,7,0,7,-8,null,null]` → 各层和 `1, 7, -1` → `2`'],
        quote='直接按照题目要求对树进行层序遍历，对于每一层求出当前层所有元素的和，然后最其中的最大值即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`q` 是只增不减的数组，一层一层往后追加节点',
              '`[l, r)` 标出当前层：处理完后 `l, r = r, len(q)` 就跳到下一层',
              '`max_s` 从根的值开始，`s > max_s` 才更新，同分保留更小的层号'],
        summary=['时间 `O(n)`，空间 `O(n)`（`q` 保存所有节点）',
                 '易错：`for now in q[l : r]` 是切片的副本，循环中 `append` 不会影响本层范围',
                 '易错：`max_s` 不能初始为 0，层和可能为负；这里用根的值',
                 '对比灵神：灵神每层换一个新列表并用 `-inf`；这里用同一个数组加 `l/r` 下标'],
    ),
)
