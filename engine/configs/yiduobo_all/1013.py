CONFIG = dict(
    num=1013, title='将数组分成和相等的三个部分', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='前缀和找两个切点',
    tags=[],
    code='''
class Solution(object):
    def canThreePartsEqualSum(self, arr):

        s = sum(arr)
        if s % 3 != 0:
            return False

        target = s // 3
        prefix_s = 0
        flag = False
        for index, num in enumerate(arr):
            prefix_s += num
            if not flag:
                if prefix_s == target:
                    flag = True
            elif prefix_s == target + target and index != len(arr) - 1:
                return True
        
        return False
''',
    call='Solution().canThreePartsEqualSum([0, 2, 1, -6, 6, -7, 9, 1, 2, 0, 1])',
    expect=True,
    views=[
        dict(type='array', var='arr', h=230, pointers={'index': 'blue'},
             window=(lambda S: 0, 'index'),
             color=lambda S, i, v: 'green' if 'index' in S and i <= S['index'] and S.get('prefix_s') == S.get('target') and i == S['index'] else None),
        dict(type='text', size=34, fn=lambda S: (f"目标 `target = {S['target']}`；前缀和 `{S['prefix_s']}`；"
             + ('==已找到第一个切点，继续找 2×target==' if S.get('flag') else '先找第一个 target')) if 'prefix_s' in S else ''),
    ],
    watch=['s', 'target', ('prefix_s', 'prefix_s', 'cyan'), ('flag', 'flag', 'yellow'), 'index'],
    max_steps=70,
    captions={
        's = sum': '总和 `s = {s}`',
        's % 3 != 0': '`{s} % 3 = {s % 3}` → 能被 3 整除，继续',
        'target = s': '每部分的目标和 `target = {s} // 3 = {target}`',
        'prefix_s += num': '加入 `{num}`，前缀和 `prefix_s = {prefix_s}`',
        'if not flag': lambda S, B, r: ('还没找到第一个切点，先找前缀和 = target' if not S.flag else '第一个切点已找到，现在找前缀和 = 2×target'),
        'if prefix_s == target:': '`prefix_s = {prefix_s}` 对比 `target = {target}` → ' + '{"==相等，记下第一个切点 flag=True==" if prefix_s == target else "不等，继续"}',
        'elif prefix_s == target + target': '`prefix_s = {prefix_s}` 对比 `2×target = {target + target}`，且下标 `{index}` 不是末尾 `{len(arr) - 1}` → {"==成立，第二个切点，剩下的和也是 target=="  if prefix_s == target + target and index != len(arr) - 1 else "不成立，继续"}',
        'return True': '两个切点都找到，且后面还留有数字 → 返回 `True`',
        'return False': '遍历完也没找到合法切点 → `False`',
    },
    cards=dict(
        one_liner='前缀和先到 target，再到 2×target，且后面还剩元素',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `arr`，问能否切成连续的三段（每段非空），三段和相等',
                 '示例：`[0,2,1,-6,6,-7,9,1,2,0,1]` → `true`',
                 '例如 `[0,2,1] [-6,6,-7,9,1] [2,0,1]` 每段和都是 3'],
        quote='若求解过程出现了prefix等于target以及prefix等于target * 2的情况，且后者出现的位置不是数组末尾，并且与前者出现的位置也不同，那么就说明……可以得到和相等的三个部分。',
        quote_src='—— yiduobo 题解原文',
        idea=['总和 `s` 不是 3 的倍数，直接 `False`',
              '否则每段目标 `target = s // 3`，只需看前缀和',
              '前缀和第一次到 `target` 立旗，之后再到 `2×target` 且不在末尾就成功'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：第二个切点不能在最后一个元素，否则第三段为空',
                 '用 `flag` 保证两个切点先后不同位置（用 `elif`）',
                 '原文为 Python 2 写法，`s / 3` 是整数除法，已改为 `s // 3`'],
    ),
)
