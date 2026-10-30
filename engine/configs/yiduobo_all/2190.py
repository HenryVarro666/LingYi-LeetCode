CONFIG = dict(
    num=2190, title='数组中紧跟key之后出现最频繁的数字', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表计数',
    code='''
class Solution(object):
    def mostFrequent(self, nums, key):

        cnt_dict = {}
        for index in range(len(nums) - 1):
            if nums[index] == key:
                target = nums[index + 1]
                cnt_dict[target] = cnt_dict.get(target, 0) + 1
        
        res = None
        max_cnt = 0
        for num, cnt in cnt_dict.items():
            if cnt > max_cnt:
                max_cnt = cnt
                res = num
        
        return res
''',
    call='Solution().mostFrequent([1,100,200,1,100,3,1,200,1,100], 1)',
    expect=100,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'yellow' if 'index' in S and i == S['index'] + 1 and S['nums'][S['index']] == S['key'] else None),
        dict(type='map', var='cnt_dict', h=260),
        dict(type='text', h=60, fn=lambda S: f"当前最多：`res = {S['res']}`，出现 `{S['max_cnt']}` 次" if 'max_cnt' in S else f"key = `{S['key']}`，统计它后面紧跟的数"),
    ],
    watch=[('key', 'key', 'orange'), ('index', 'index', 'blue'), 'target', ('res', 'res', 'green'), 'max_cnt'],
    captions={
        'for index in range': '`index = {index}`，看 `nums[{index}] = {nums[index]}`（最后一个数后面没有数，所以只到 `len-1`）',
        'if nums[index] == key': '`nums[{index}] = {nums[index]}` 是否等于 key `{key}` → {nums[index] == key}',
        'target = nums': '紧跟在 key 后面的数 `target = nums[{index}+1] = {target}`',
        'cnt_dict[target] = ': '`{target}` 跟在 key 后的次数加一 → `{cnt_dict[target]}`',
        'for num, cnt in': '第二趟：遍历哈希表，找次数最多的数',
        'if cnt > max_cnt': '`{cnt} > {max_cnt}`？→ {cnt > max_cnt}（`{num}` 出现 {cnt} 次）',
        'max_cnt = cnt': '更新最多次数 `max_cnt = {max_cnt}`',
        'res = num': '答案暂定为 `{res}`',
        'return res': '出现次数最多的是 ==`{res}`==（{max_cnt} 次）',
    },
    max_steps=70,
    cards=dict(
        one_liner='一趟遍历，只统计 key 后面紧跟的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定整数数组 `nums` 和整数 `key`',
                 '统计每个紧跟在 `key` 之后出现的数 `target`（`nums[i] == key` 且 `nums[i+1] == target`）的次数',
                 '返回出现次数最多的 `target`，题目保证答案唯一',
                 '示例：`[1,100,200,1,100,3,1,200,1,100], key=1` → `100`'],
        quote='直接一趟遍历，使用哈希表统计每个key之后的下一个数字的出现次数，然后取其中出现次数最多的作为答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历下标 `0 ~ n-2`：遇到 `key` 就把后一个数计入哈希表',
              '再扫一遍哈希表，用 `max_cnt` 记录最大次数和对应的数',
              '只有严格更大才更新，答案唯一时不会出错'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '下标只到 `len(nums) - 2`，避免 `nums[index + 1]` 越界',
                 '`cnt > max_cnt` 用严格大于，题目保证答案唯一',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
