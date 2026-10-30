CONFIG = dict(
    num=2442, title='反转之后不同整数的数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 逐位分离再组装',
    tags=[],
    code='''
class Solution(object):
    def countDistinctIntegers(self, nums):

        num_set = set(nums)

        for num in nums:
            now = num
            digit_list = []
            while now:
                digit_list.append(now % 10)
                now //= 10
            
            now = 0
            for digit in digit_list:
                now = now * 10 + digit
            
            num_set.add(now)

        return len(num_set)
''',
    call='Solution().countDistinctIntegers([1,13,10,12,31])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums', cell=90,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] and S['nums'].index(v) == i else None),
        dict(type='array', var='digit_list', label='digit_list（从低位到高位分离出的数位）', cell=80),
        dict(type='set', var='num_set', label='num_set', fmt=lambda x: str(x)),
    ],
    watch=['num', 'now', ('len(num_set)', 'len(num_set)', 'green')],
    captions={
        'num_set = set(nums)': '先把所有原数放进哈希集合：`{num_set}`',
        'for num in nums': '一趟遍历：处理 `num = {num}`',
        'now = num': '`now` 拷贝一份用来拆数位，不动 `num`',
        'digit_list = []': '`digit_list` 存逐位分离出的数字',
        'while now': lambda S, B, r: (f'`now = {S.now}` 还没拆完' if S.now else '`now` 变成 0，数位拆完了'),
        'digit_list.append': '取末位 `{now % 10}`，放进 `digit_list`：`{digit_list}`',
        'now //= 10': '去掉末位，`now` → {now}',
        'now = 0': '`now` 清零，准备按 `digit_list` 的顺序重新组装',
        'for digit in digit_list': '依次取数位 `{digit}`',
        'now = now * 10': '`now = {B.now} * 10 + {digit} = {now}`：先拆出来的末位变成了最高位',
        'num_set.add': '反转结果 `{now}` 加入集合（原来的 `{num}` 反转后是 `{now}`），集合大小 `{len(num_set)}`',
        'return len': '哈希表里一共 `{ret}` 个不同的数',
    },
    cards=dict(
        one_liner='先存原数，再逐位拆开反着拼，也存进哈希表',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['把 `nums` 里每个数的数位反转并追加到数组末尾，求不同整数的个数',
                 '反转 `10` 得 `01` 即 `1`',
                 '示例：`[1,13,10,12,31]` → `6`'],
        quote='首先将所有整数都加入到哈希表中，然后一趟遍历，逐位分离当前遍历到的数，反转并组装起来之后同样也加入到哈希表中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num_set = set(nums)`：原数先进表',
              '拆：`% 10` 取末位放进 `digit_list`，`//= 10` 去掉末位',
              '拼：按 `digit_list` 顺序 `now * 10 + digit`，先拆出的末位就成了最高位'],
        result='集合里是 `{1, 10, 12, 13, 21, 31}`，共 6 个 ✓',
        summary=['时间 `O(n log U)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`now /= 10` 已改为 `now //= 10`，并删去类型说明文档字符串',
                 '易错：`now` 要先 `now = 0` 再组装，否则会接在旧值后面',
                 '对比灵神：他边拆边拼，不需要 `digit_list`'],
    ),
)
