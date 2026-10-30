CONFIG = dict(
    num=2951, title='找出峰值', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='枚举中间下标',
    code='''
class Solution:
    def findPeaks(self, mountain: List[int]) -> List[int]:
        return [i for i in range(1, len(mountain) - 1)
                if mountain[i - 1] < mountain[i] > mountain[i + 1]]
''',
    call='Solution().findPeaks([1,4,3,8,5,2,6,3])',
    expect=[1, 3, 6],
    views=[
        dict(type='array', var='mountain', pointers={'i': 'blue'}, h=300,
             color=lambda S, k, v: ('green' if S['mountain'][S['i']-1] < S['mountain'][S['i']] > S['mountain'][S['i']+1] else 'orange') if 'i' in S and k == S['i'] else None),
        dict(type='text', fn=lambda S: (f"下标 `{S['i']}`：`{S['mountain'][S['i']-1]} < {S['mountain'][S['i']]} > {S['mountain'][S['i']+1]}` → "
                                         + ('==是峰值==' if S['mountain'][S['i']-1] < S['mountain'][S['i']] > S['mountain'][S['i']+1] else '不是峰值')) if 'i' in S else '首尾不可能是峰值，只枚举 `[1, n-2]`'),
    ],
    watch=['i'],
    captions={
        'for i in range': lambda S, B, ret: ('遍历结束，所有峰值下标都收进了结果' if ret is not None else '枚举 `i` 从 1 到 `n-2`：首尾没有两侧邻居，直接排除，只看中间元素'),
        'if mountain': '`{mountain[i-1]} < {mountain[i]} > {mountain[i+1]}`？比左右都大才是峰值 → =={"是，下标 " + str(i) + " 入答案" if mountain[i-1] < mountain[i] > mountain[i+1] else "不是，跳过"}==',
    },
    cards=dict(
        one_liner='枚举 1 到 n-2，比左右邻居都大就是峰值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['峰值 = ==严格大于==左右相邻元素的数，首尾元素不算',
                 '返回所有峰值的下标',
                 '示例：`[1,4,3,8,5]` → `[1,3]`'],
        quote='遍历下标在 [1,n-2] 内的所有数，如果其大于左右两侧相邻数字，则把 i 加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['首尾缺一侧邻居，题目直接排除，循环范围就是 `range(1, n-1)`',
              '链式比较 `a < b > c` 一行判断两侧'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '必须==严格==大于：`[2,4,4]` 中 4 不是峰值',
                 '范围别写成 `range(len)`，否则 `i+1` 越界'],
    ),
)
