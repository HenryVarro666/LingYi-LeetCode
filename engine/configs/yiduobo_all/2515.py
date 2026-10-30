W = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

CONFIG = dict(
    num=2515, title='到目标字符串的最短距离', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='双指针从起点向两侧同时移动',
    tags=[],
    code='''
class Solution(object):
    def closetTarget(self, words, target, startIndex):

        if words[startIndex] == target:
            return 0
        
        left = startIndex
        right = startIndex
        n = len(words)
        step = 0
        while True:
            left = (left - 1 + n) % n
            right = (right + 1) % n
            step += 1
            if words[left] == target or words[right] == target:
                return step
            
            if left == right or (left - 1 + n) % n == right:
                break
        
        return -1
''',
    call=f"Solution().closetTarget({W!r}, 'g', 1)",
    expect=3,
    views=[
        dict(type='array', var='words', label='words（环形，黄 = target）', cell=90, h=250,
             pointers={'left': 'blue', 'right': 'pink'},
             color=lambda S, i, v: 'yellow' if v == S.get('target') else None),
        dict(type='text', size=28, h=110,
             fn=lambda S: (f"`step = {S['step']}`：左指针在 `{S['left']}`，右指针在 `{S['right']}`" if 'step' in S else '')),
    ],
    watch=[('step', 'step', 'green'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('target', 'target', 'yellow')],
    captions={
        'if words[startIndex] == target': lambda S, B, r: (f'起点 `words[{S.startIndex}] = {S.words[S.startIndex]}`' + (' 就是 target → 返回 0' if S.words[S.startIndex] == S.target else f' 不是 `{S.target}` → 要往两边走')),
        'left = startIndex': '两个指针都从起点出发：`left = {left}`',
        'right = startIndex': '`right = {right}`',
        'n = len': '`n = {n}`：取模时用它让下标绕回另一端',
        'step = 0': '`step` 记录走了几步',
        'while True': '无限循环：靠 return 或 break 退出',
        'left = (left': '左指针后退一格：`(left − 1 + n) % n` → =={left}==（到头了就绕到末尾）',
        'right = (right': '右指针前进一格：`(right + 1) % n` → =={right}==（到末尾就绕到开头）',
        'step += 1': '两边各走一步，`step` → {step}',
        'if words[left] == target or': lambda S, B, r: (f'`words[{S.left}] = {S.words[S.left]}`，`words[{S.right}] = {S.words[S.right]}` → ' + ('==碰到 target=='  if (S.words[S.left] == S.target or S.words[S.right] == S.target) else f'都不是 `{S.target}`，继续走')),
        'return step': '同时出发，第一次碰到就是最短，返回 =={ret}==',
        'if left == right or': lambda S, B, r: ('两个指针汇合了（或擦肩而过），说明绕了一圈还没找到 → 退出循环' if (S.left == S.right or (S.left - 1 + S.n) % S.n == S.right) else f'`left = {S.left}`、`right = {S.right}` 还没汇合 → 继续下一轮'),
        'return -1': 'words 里没有 target，返回 -1',
    },
    cards=dict(
        one_liner='两个指针从起点同时向两侧走，先碰到目标的步数就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`words` 是环形数组，每步可以走到下一个或前一个单词',
                 '求从 `startIndex` 到 `target` 的最短步数，没有则 `-1`',
                 '示例：`["a","b","leetcode"]`，起点 0 → 1（向左一步到末尾）'],
        quote='我在这里采用的是从起始位置，使用两个指针分别向两侧同时移动，首次到达目标字符串所需的步数即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left` 往左、`right` 往右，各走 `step` 步',
              '下标用 `% n` 绕回，数组就成了环',
              '两个指针汇合还没找到，说明整圈都没有 → 返回 -1'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：先单独判断起点本身（距离 0）；左移要写 `(left - 1 + n) % n`',
                 '汇合判断有两种：`left == right`（n 为奇数）和相邻擦肩而过（n 为偶数）',
                 '原文方法名写作 `closetTarget`（原文拼写），已照搬',
                 '对比灵神：灵神枚举 k，用负下标省掉左边取模；这里手动维护两个指针'],
    ),
)
