def target_hit(S):
    return S.words[S.startIndex - S.k] == S.target or S.words[(S.startIndex + S.k) % S.n] == S.target


W = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

CONFIG = dict(
    num=2515, title='到目标字符串的最短距离', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='从起点向两侧枚举距离 k',
    tags=[],
    code='''
class Solution:
    def closestTarget(self, words: list[str], target: str, startIndex: int) -> int:
        n = len(words)
        for k in range(n // 2 + 1):
            if words[startIndex - k] == target or words[(startIndex + k) % n] == target:
                return k
        return -1
''',
    call=f"Solution().closestTarget({W!r}, 'g', 1)",
    expect=3,
    views=[
        dict(type='array', var='words', label='words（黄 = target，蓝 = 向左探，粉 = 向右探）', cell=90, h=250,
             pointers={'startIndex': 'green'},
             color=lambda S, i, v: ('blue' if 'k' in S and i == (S['startIndex'] - S['k']) % S['n'] else 'pink' if 'k' in S and i == (S['startIndex'] + S['k']) % S['n'] else 'yellow' if v == S.get('target') else None)),
        dict(type='text', size=28, h=110,
             fn=lambda S: (f"向左 `words[{S['startIndex']} − {S['k']}]` = `{S['words'][S['startIndex'] - S['k']]}`（下标 {(S['startIndex'] - S['k']) % S['n']}），"
                           f"向右 `words[({S['startIndex']} + {S['k']}) % {S['n']}]` = `{S['words'][(S['startIndex'] + S['k']) % S['n']]}`（下标 {(S['startIndex'] + S['k']) % S['n']}）") if 'k' in S else ''),
    ],
    watch=[('k', 'k', 'blue'), ('target', 'target', 'yellow'), ('startIndex', 'startIndex', 'green')],
    captions={
        'n = len': '`n = {n}`：环形数组的长度，向右取模要用它',
        'for k in range': '枚举距离 `k = {k}`（最多 `n // 2 = {n // 2}`，再远就该反向走了）',
        'if words[startIndex - k]': lambda S, B, r: (
            f"左边 `words[{S.startIndex - S.k}]`（负下标等价于 {(S.startIndex - S.k) % S.n}）= `{S.words[S.startIndex - S.k]}`，"
            f"右边 `words[{(S.startIndex + S.k) % S.n}]` = `{S.words[(S.startIndex + S.k) % S.n]}` → "
            + ('==有一边是 target==' if target_hit(S) else '都不是 `' + S.target + '`，k 加大')),
        'return k': '距离 `{k}` 就能到 target，==第一次命中即最短==，返回 {ret}',
        'return -1': 'words 里没有 target，返回 -1',
    },
    cards=dict(
        one_liner='从起点向左右同时走 k 步，第一次碰到目标就是最短',
        complexity='时间 `O(nm)`，空间 `O(1)`',
        problem=['`words` 是环形数组，首尾相连；从 `startIndex` 出发每步左移或右移一格',
                 '返回到达 `target` 的最短步数，没有则 `-1`',
                 '示例：`["hello","i","am","leetcode","hello"]`，目标 hello，起点 1 → 1'],
        quote='枚举答案 k=0,1,2,…,⌊n/2⌋，判断 nums[startIndex−k]=target 或者 nums[startIndex+k]=target 是否成立，如果成立，直接返回 k。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['答案最多是 `n // 2`：超过一半，反方向走更近',
              'Python 的负下标天然是环形的：`words[startIndex - k]` 不用取模',
              '向右的 `startIndex + k` 可能越界，用 `% n` 绕回开头'],
        summary=['时间 `O(nm)`，`m` 是 `target` 长度（字符串比较的代价），空间 `O(1)`',
                 '易错点：向右要 `% n`；向左靠 Python 负下标，其他语言要写 `(i - k + n) % n`',
                 '方法一：遍历所有等于 target 的下标 i，取 `min(d, n - d)` 更新答案',
                 '相似题：1848. 到目标元素的最小距离'],
    ),
)
