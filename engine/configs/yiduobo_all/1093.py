CONFIG = dict(
    num=1093, title='大样本统计', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='桶排 · 一趟扫描 + 前缀计数',
    code='''
class Solution(object):
    def sampleStats(self, count):

        mi = None
        ma = None
        avg = 0.0
        max_cnt = 0
        mode = None
        
        for index in range(256):
            cnt = count[index]
            if cnt > 0:
                if mi is None:
                    mi = float(index)
                ma = float(index)
                avg += index * cnt
                if cnt > max_cnt:
                    max_cnt = cnt
                    mode = float(index)
            if index > 0:
                count[index] += count[index - 1]

        avg /= count[-1]
        index = 0
        while index < 256 and count[index] < (count[-1] + 1) // 2:
            index += 1
        if count[-1] % 2 == 1 or count[index] >= (count[-1] + 1) // 2 + 1:
            median = float(index)
        else:
            median = float(index)
            while index < 256 and count[index] < (count[-1] + 1) // 2 + 1:
                index += 1
            median += float(index)
            median /= 2.0
        
        return mi, ma, avg, median, mode
''',
    setup='cnt0 = [0] * 256\ncnt0[4] = 2\ncnt0[7] = 3\ncnt0[9] = 1\ncnt0[12] = 2',
    call='Solution().sampleStats(cnt0)',
    expect=(4.0, 12.0, 7.75, 7.0, 7.0),
    skip=['cnt = count[index]', 'for index in range(256)', 'ma = float', 'if index > 0:'],
    max_steps=64,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"扫描到 `index = {S['index']}`（只画 0~15，其余都是 0 或前缀和）" if 'index' in S else '')),
        dict(type='array', var='count[:16]', label='count（只显示前 16 项）', pointers={'index': 'blue'}, h=250,
             color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='text', size=30, fn=lambda S: (f"最小 `{S['mi']}`　最大 `{S['ma']}`　众数 `{S['mode']}`（次数 {S['max_cnt']}）　总和 `{S['avg']}`" if 'mode' in S else '')),
    ],
    watch=['index', 'mi', 'ma', 'avg', 'max_cnt', 'mode', ('median', 'median', 'green')],
    captions={
        'mi = None': '`mi` 记最小值：第一个 `count > 0` 的下标',
        'ma = None': '`ma` 记最大值：最后一个 `count > 0` 的下标',
        'avg = 0.0': '`avg` 先累加 `下标 × 个数` 得总和',
        'max_cnt = 0': '`max_cnt`、`mode`：个数最多的下标就是众数',
                'if cnt > 0:': '扫描桶 `{index}`：`count[{index}] = {cnt}`：{"有这个数" if cnt > 0 else "没有这个数，跳过"}',
        'if mi is None': '`mi` 还是 None？{"是，这是第一个非零下标" if mi is None else "否，最小值已定"}',
        'mi = float': '最小值 `mi = {mi}`',
        'ma = float': '最大值随扫描不断后移：`ma = {ma}`',
        'avg += ': '总和加上 `{index} × {cnt}` → `avg = {avg}`',
        'if cnt > max_cnt': '`{cnt} > {B.max_cnt}`？比当前最多的次数大才更新众数',
        'max_cnt = cnt': '新的最多次数 `{max_cnt}`',
        'mode = float': '众数暂定 `{mode}`',
        'count[index] += ': '前缀和：`count[{index}]` 变成「小于等于 {index} 的数共有多少个」= {count[index]}',
        'avg /= ': '总数 `count[-1] = {count[-1]}`，平均数 = 总和 ÷ 总数 → `{avg}`',
        'index = 0': '再从 0 扫一遍，找排名为中间的数',
        'while index < 256': '`count[{index}] = {count[index]}` 与目标排名 `{(count[-1] + 1) // 2}`：{"还不够，继续右移" if count[index] < (count[-1] + 1) // 2 else "已达到，排名第 (tot+1)/2 的数就是它"}',
        'index += 1': '`index` → {index}',
        'if count[-1] % 2': '总数奇数，或该下标已覆盖第 (tot+1)/2+1 名 → 中位数就是它自己：`{count[-1] % 2 == 1 or count[index] >= (count[-1] + 1) // 2 + 1}`',
        'median = float': '`median = {median}`',
        'median += ': '偶数个：再找下一个排名对应的数，两数相加 `{median}`',
        'median /= ': '取平均 → 中位数 `{median}`',
        'return': '返回 `[最小, 最大, 平均, 中位, 众数]` = `{ret}`',
    },
    cards=dict(
        one_liner='值域只有 0~255：桶排一趟扫描，前缀和找中位数',
        complexity='时间 `O(256)`，空间 `O(1)`',
        problem=['`count[k]` 表示整数 `k` 在样本中出现的次数，`k` 在 `0~255`',
                 '求最小值、最大值、平均数、中位数、众数（浮点数）',
                 '本视频：`count[4]=2, count[7]=3, count[9]=1, count[12]=2`'],
        quote='利用求众数时得到的新的count数组，已知一共有count[255]个数。……直接从0开始扫描，若当前的index第一次满足count[index] >= target，那么就说明从小到大排名第target的数就是index。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描：第一个非零下标是最小值，最后一个非零下标是最大值',
              '扫描时累加 `index × count` 求和，记录最大次数得众数',
              '同时做前缀和，`count[index]` 变成「不超过 index 的个数」，中位数从 0 扫到排名处即可'],
        summary=['时间 `O(256)`，空间 `O(1)`，值域小所以不用二分',
                 '偶数个数时，中位数是中间两个排名的数取平均',
                 '平均数要先求总和，再除以总数（前缀和后的 `count[-1]`）',
                 '原文为 Python 2 写法，其中整数除法 `/` 已改为 `//`'],
    ),
)
