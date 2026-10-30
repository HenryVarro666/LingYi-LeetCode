CONFIG = dict(
    num=3842, title='切换打开灯泡', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='布尔数组 · 取反',
    tags=[],
    code='''
class Solution(object):
    def toggleLightBulbs(self, bulbs):
        
        flag = [False] * 101
        for b in bulbs:
            flag[b] = not flag[b]
        
        res = []
        for index in range(1, 101):
            if flag[index]:
                res.append(index)
        
        return res
''',
    call='Solution().toggleLightBulbs([3,5,3,7,5,5])',
    expect=[5, 7],
    views=[
        dict(type='array', var='bulbs', label='bulbs', cell=90, h=170),
        dict(type='array', var=lambda S: S['flag'][:9], label='flag[0..8]（True = 亮；原数组共 101 格，只画前 9 格）', cell=90, h=240,
             pointers={'b': 'blue'},
             color=lambda S, i, v: 'yellow' if v else None),
        dict(type='text', h=90, size=30, fn=lambda S: f"已亮的灯：`{S['res']}`" if 'res' in S else '先对每个 b 取反 flag[b]，最后从 1 到 100 收集 True'),
    ],
    watch=['b', 'index', ('res', 'res', 'green')],
    captions={
        'flag = [False]': '`flag[i]` 表示第 i 个灯泡是否亮着，全部初始为 ==False==（多开一格，下标 1 到 100 直接用）',
        'flag[b] = not flag[b]': '对灯泡 `{b}` 取反：`{B.flag[b]}` → ==`{flag[b]}`==',
        'for b in bulbs': '操作灯泡 `b = {b}`',
        'res = []': '操作都完成了，开始收集亮着的灯',
        'if flag[index]': '灯泡 `{index}` 是 {"==亮的== → 加入答案" if flag[index] else "灭的，跳过"}',
        'res.append': '`res = {res}`',
        'return res': '升序遍历得到的 `res` 天然有序：==`{ret}`==',
    },
    skip=['for index in range'],
    max_steps=60,
    cards=dict(
        one_liner='一个布尔数组记开关状态，按一次就取反',
        complexity='时间 `O(n + 100)`，空间 `O(1)`（数组固定 101 格）',
        problem=['100 个灯泡编号 1 到 100，一开始全灭',
                 '`bulbs` 中每个数表示：若该灯灭就打开，若亮就关闭',
                 '按升序返回最终亮着的灯；示例 `[10,30,20,10]` → `[20,30]`'],
        quote='接下来遍历bulbs，对于当前遍历到的bulbs[index]，将flag[bulbs[index]]取反，表示对bulbs[index]这个灯泡进行操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['`flag` 初始全 False，对每个操作直接取反',
              '遍历完再从 1 到 100 扫一遍，True 的就收进答案',
              '因为是从小到大扫，答案天然升序，不用排序'],
        summary=['时间 `O(n + 100)`，空间 `O(1)`',
                 '`flag` 开 101 格，让编号直接当下标',
                 '对比灵神：灵神数出现次数的奇偶，yiduobo 直接维护开关状态',
                 '同类题：统计奇偶次数（异或、状态翻转）'],
    ),
)
