CONFIG = dict(
    num=888, title='公平的糖果棒交换', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希集合 + 差值',
    tags=[],
    code='''
class Solution(object):
    def fairCandySwap(self, A, B):

        sumA = sumB = 0
        setA = set()
        for num in A:
            setA.add(num)
            sumA += num
        
        for num in B:
            sumB += num
        
        diff = (sumA - sumB) // 2
        for num in B:
            if num + diff in setA:
                return [num + diff, num]
''',
    call='Solution().fairCandySwap([1, 2, 5], [2, 4])',
    expect=[5, 4],
    views=[
        dict(type='array', var='A', label='A（Alice 的糖果棒）', h=130),
        dict(type='array', var='B', label='B（Bob 的糖果棒）', pointers={}, h=130,
             color=lambda S, i, v: 'yellow' if S.get('_line') and 'diff' in S and S.get('num') == v else None),
        dict(type='set', var='setA', label='setA', h=140),
        dict(type='text', fn=lambda S: f"`sumA = {S['sumA']}`，`sumB = {S['sumB']}`" + (f"，`diff = {S['diff']}`" if 'diff' in S else '') if 'sumB' in S else '', h=60),
    ],
    watch=['sumA', 'sumB', 'diff', 'num'],
    captions={
        'sumA = sumB = 0': '`sumA`、`sumB` 分别累计两人糖果总数',
        'setA = set()': '`setA` 存 A 中出现过的数，方便 `O(1)` 查找',
        'setA.add': '`{num}` 放进 `setA`',
        'sumA += num': '`sumA` 累加 `{num}` → {sumA}',
        'sumB += num': '`sumB` 累加 `{num}` → {sumB}',
        'diff = ': '换完要相等：`diff = (sumA − sumB) // 2 = ({sumA} − {sumB}) // 2 = =={diff}==`，即 A 要换出的数比 B 的大 `diff`',
        'for num in B': '枚举 Bob 要换出的 `num = {num}`',
        'if num + diff in setA': '需要 A 中有 `{num} + {diff} = {num + diff}` → {"==有=="  if num + diff in setA else "没有，换下一个"}',
        'return [num + diff': '找到了：Alice 给 `{num + diff}`，Bob 给 `{num}` → `{ret}`',
    },
    cards=dict(
        one_liner='交换后总和要相等，所以 A 换出的数 = B 换出的数 + 差值的一半',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['Alice 和 Bob 各有若干糖果棒，`A[i]`、`B[j]` 是每根的糖果数',
                 '各交换一根，使两人总糖果数相等，返回 `[A 换出, B 换出]`',
                 '本视频：`A=[1,2,5]`，`B=[2,4]` → `[5,4]`'],
        quote='由于题目要求只能交换一次，那么就需要靠这一次交换抹平A和B的差值……找出来一组数，使其满足numA = numB + diff / 2即可。这个查找的过程则可以利用哈希表来做。',
        quote_src='—— yiduobo 题解原文',
        idea=['设 `diff = (sumA − sumB) / 2`，交换 `numA`、`numB` 后：`sumA − numA + numB = sumB + numA − numB`',
              '化简得 `numA = numB + diff`',
              '把 A 放进集合，枚举 B 的每个数，查 `num + diff` 在不在集合里'],
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '`sumA − sumB` 题目保证为偶数，所以 `//` 不丢信息',
                 '易错：`numA = numB + diff`，不是减号；`diff` 可能为负',
                 '原文为 Python 2 写法，其中整数除法 `/` 已改为 `//`'],
    ),
)
