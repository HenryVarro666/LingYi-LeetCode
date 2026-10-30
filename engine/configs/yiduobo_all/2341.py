CONFIG = dict(
    num=2341, title='数组能形成多少数对', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · 次数//2 与 次数%2',
    code='''
class Solution(object):
    def numberOfPairs(self, nums):

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = [0, 0]
        for cnt in cnt_dict.values():
            res[0] += cnt // 2
            res[1] += cnt % 2
        
        return res
''',
    call='Solution().numberOfPairs([1,3,2,1,3,2,2])',
    expect=[3, 1],
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=90, pointers={}),
        dict(type='map', var='cnt_dict', label='cnt_dict（数 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='array', var='res', label='res = [数对数, 落单数]', h=150, cell=110),
    ],
    watch=['num', 'cnt', ('res', 'res', 'green')],
    captions={
        'cnt_dict = {}': '`cnt_dict` 记录每个数出现了几次',
        'cnt_dict[num] =': '数到 `{num}`：它现在出现了 `{cnt_dict[num]}` 次',
        'res = [0, 0]': '`res[0]` 是数对数，`res[1]` 是落单的数',
        'for cnt in': '取出一种数的出现次数 `cnt = {cnt}`',
        'res[0] +=': '出现 `{cnt}` 次，两个一对 → 形成 `{cnt} // 2 = {cnt // 2}` 对，数对数累计 =={res[0]}==',
        'res[1] +=': '`{cnt} % 2 = {cnt % 2}`：多出来落单的个数，累计 =={res[1]}==',
        'return res': '数对 `{res[0]}` 个，剩余 `{res[1]}` 个',
    },
    cards=dict(
        one_liner='一趟哈希表计数，每种数的次数 //2 是对数、%2 是落单',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次选两个==相等==的数删掉，形成一个数对，直到不能再操作',
                 '返回 `[数对数, 剩余数字个数]`',
                 '示例：`[1,3,2,1,3,2,2]` → `[3,1]`'],
        quote='设其出现了cnt次，由于两个形成一对，那么一共可以形成cnt / 2对，同时又cnt % 2个落单的数，使用这两个值更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一趟遍历，用哈希表统计每个数的出现次数',
              '每种数出现 `cnt` 次：配成 `cnt // 2` 对，落单 `cnt % 2` 个',
              '分别累加进 `res[0]` 和 `res[1]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，整数除法 `cnt / 2` 已改为 `cnt // 2`（Python 3 的 `/` 得到小数）',
                 '落单个数也可以直接用 `len(nums) - 2 * 对数` 得到',
                 '对比灵神：灵神用 `Counter` 一行求对数，剩余数用总数减去两倍对数；这里两个值同时统计'],
    ),
)
