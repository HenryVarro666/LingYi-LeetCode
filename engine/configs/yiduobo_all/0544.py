CONFIG = dict(
    num=544, title='输出比赛匹配对', difficulty='Medium', category='位运算',
    author='yiduobo', technique='lowbit 构造',
    code='''
class Solution(object):
    def findContestMatch(self, n):
        
        mapping = {1 : 0}
        now = 1
        p = 0
        while now < n:
            now += now
            p += 1
            mapping[now] = p
        
        res = ['(' * mapping[n], '1']
        arr = [1]
        for index in range(1, n):
            res.append(',')
            lowbit = index & -index
            if lowbit == 1:
                v = n + 1 - arr[-1]
                res.append(str(v))
                arr.append(v)
                res.append(')' * mapping[(index + 1) & (-index - 1)])
            else:
                v = n // lowbit + 1 - arr[index - lowbit]
                res.append('(' * mapping[lowbit])
                res.append(str(v))
                arr.append(v)
        
        return ''.join(res)
''',
    call='Solution().findContestMatch(8)',
    expect='(((1,8),(4,5)),((2,7),(3,6)))',
    views=[
        dict(type='map', var='mapping', label='mapping：2 的幂 → 末尾 0 的个数', h=170, font=22),
        dict(type='array', var='arr', label='arr：每个位置的队伍编号', h=170, cell=70),
        dict(type='array', var='res', label='res：输出片段', h=170, cell=70),
        dict(type='text', size=30, h=110, fn=lambda S: (f"`index` = {S['index']}（二进制 {S['index']:b}），`lowbit` = =={S['lowbit']}==" if 'lowbit' in S and 'index' in S else '')),
    ],
    watch=['now', 'p', 'index', 'lowbit', 'v'],
    captions={
        'now += now': '`now` 翻倍 → {now}',
        'p += 1': '`p` = {p}：`now` 是 2 的 `{p}` 次方',
        'mapping[now] = p': '记下 `mapping[{now}] = {p}`：以后用 lowbit 反查括号数',
        "res = ['('": '开头有 `mapping[n]` = {mapping[n]} 个左括号，然后是队伍 `1`',
        'for index in range': '从下标 1 开始逐个构造，下标 0 固定是 1 号队',
        'res.append(\',\')': '每个队伍前先放一个逗号',
        'lowbit = index': '`lowbit = index & -index` = =={lowbit}==（最低位的 1）',
        'if lowbit == 1': '`lowbit` = {lowbit}：{"奇数下标，和前一个配对，要补右括号" if lowbit == 1 else "偶数下标，要开左括号"}',
        'v = n + 1 - arr[-1]': '奇数下标和前一个队伍之和为 `n+1`：`{n+1} − {arr[-1]}` = =={v}==',
        'v = n // lowbit': '配对位置 `index − lowbit` = {index - lowbit}，两者之和为 `n//lowbit + 1` = {n // lowbit + 1} → `v` = =={v}==',
        "res.append(')'": '右括号数 = `index+1` 末尾 0 的个数 = {mapping[(index + 1) & (-index - 1)]}',
        "res.append('('": '左括号数 = `lowbit` 末尾 0 的个数 = {mapping[lowbit]}',
        'res.append(str(v))': '放入队伍 `{v}`',
        'arr.append(v)': '记下 `arr[{index}]` = {v}，供后面的位置配对使用',
        'return': '拼接所有片段：`{ret}`',
    },
    max_steps=130,
    cards=dict(
        one_liner='观察规律：配对位置是 index 去掉 lowbit',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 支队伍（2 的幂）编号 1..n，每轮强队配弱队',
                 '输出用括号表示的最终对阵，如 `n=4` → `((1,4),(2,3))`',
                 '本视频：`n = 8` → `(((1,8),(4,5)),((2,7),(3,6)))`'],
        quote='由于n的规模不大，因此可以直接模拟，不过在这里也可以直接构造，时间复杂度会稍微好一点。',
        quote_src='—— yiduobo 题解原文',
        idea=['先拿 `n=16` 模拟找规律：已确定的配对之后不会再变',
              '`pair[x] = x − lowbit(x)`，且 `num[x] + num[pair[x]] = n/lowbit(x) + 1`',
              '偶数下标左边的 `(` 个数 = 末尾 0 数；奇数下标右边的 `)` 个数 = 末尾 1 数',
              '末尾 0 的个数用 2 的幂哈希表 `mapping` 反查'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：括号个数要用 `index+1` 求末尾 1，不是直接用 `index`',
                 '原文为 Python 2 写法，`n / lowbit` 已改为 `n // lowbit`，并删去了 `:type` 文档字符串',
                 '直接模拟也可以，只是每轮要重新配对'],
    ),
)
