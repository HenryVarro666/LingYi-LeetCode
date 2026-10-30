CONFIG = dict(
    num=3907, title='统计具有相反奇偶性的较小元素', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='归并排序 · 逆序对按奇偶计数',
    tags=[],
    code='''
class Solution(object):
    def countSmallerOppositeParity(self, nums):
        
        n = len(nums)
        res = [0] * n
        arr = [(v, index) for index, v in enumerate(nums)]

        def calc(arr, left, right, res):
            if left == right:
                return

            mid = (left + right) // 2
            calc(arr, left, mid, res)
            calc(arr, mid + 1, right, res)

            odd, even = 0, 0
            i, j = left, mid + 1
            tmp = []
            while i <= mid or j <= right:
                if i == mid + 1:
                    tmp.append(arr[j])
                    j += 1
                elif j == right + 1 or arr[i][0] <= arr[j][0]:
                    if arr[i][0] % 2 == 0:
                        res[arr[i][1]] += odd
                    else:
                        res[arr[i][1]] += even
                    tmp.append(arr[i])
                    i += 1
                else:
                    tmp.append(arr[j])
                    if arr[j][0] % 2 == 0:
                        even += 1
                    else:
                        odd += 1
                    j += 1
            
            for index in range(left, right + 1):
                arr[index] = tmp[index - left]
        
        calc(arr, 0, n - 1, res)
        return res
''',
    call='Solution().countSmallerOppositeParity([4,1,3,2])',
    expect=[2, 0, 1, 0],
    views=[
        dict(type='array', var='arr', label='arr（值，原下标）按值归并排序；框 = [left, right]', h=200, cell=110,
             window=(lambda S: S.get('left'), lambda S: S.get('right')),
             pointers={'i': 'blue', 'j': 'pink'},
             fmt=lambda v: f'{v[0]}', ),
        dict(type='array', var='res', label='res（按原下标；每个数得到的分）', h=160, cell=110),
        dict(type='array', var='tmp', label='tmp（本次归并的结果）', h=150, cell=110, fmt=lambda v: f'{v[0]}'),
        dict(type='calls', h=150),
    ],
    skip=['tmp = []', 'tmp.append', 'j += 1', 'i += 1', 'for index in range', 'arr[index] = tmp', 'i, j = left'],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('odd', 'odd', 'orange'), ('even', 'even', 'cyan')],
    captions={
        'if left == right': lambda S, B, r: f'区间 `[{S.left}, {S.right}]` 只剩 1 个元素 → 天然有序，返回' if S.left == S.right else f'区间 `[{S.left}, {S.right}]` 有多个元素 → 继续二分',
        'mid = (left + right)': '中点 `mid = {mid}`：左半 `[{left}, {mid}]`，右半 `[{mid + 1}, {right}]`',
        'calc(arr, left, mid, res)': '先递归处理左半，让它按值有序',
        'calc(arr, mid + 1, right, res)': '再递归处理右半。两半都有序后，才能合并并数逆序对',
        'odd, even = 0, 0': '`odd`/`even`：已放入 tmp 的==右半==元素里奇、偶各几个（`i`、`j` 分别扫左、右半）',
                'i == mid + 1': lambda S, B, r: '左半已用完 → 剩下的右半元素直接放入' if S.i == S.mid + 1 else '左半还有元素，继续比较',
        'elif j == right + 1 or': lambda S, B, r: (
            '右半已用完 → 剩下的左元素直接放入，已放入的右半元素都比它小' if S.j == S.right + 1 else
            f'`{S.arr[S.i][0]} <= {S.arr[S.j][0]}`：左边较小 → 先放左边，已放入的右半元素都比它小'
            if S.arr[S.i][0] <= S.arr[S.j][0] else
            f'`{S.arr[S.i][0]} > {S.arr[S.j][0]}`：右边更小 → 先放右边，并记下它的奇偶'),
        'if arr[i][0] % 2 == 0': lambda S, B, r: (
            f'左元素 `{S.arr[S.i][0]}` 是偶数 → 只与已放入右半的==奇数==（共 {S.odd} 个）构成合法逆序对'
            if S.arr[S.i][0] % 2 == 0 else
            f'左元素 `{S.arr[S.i][0]}` 是奇数 → 只与已放入右半的==偶数==（共 {S.even} 个）构成合法逆序对'),
        'res[arr[i][1]] += odd': '原下标 `{arr[i][1]}` 加 `odd = {odd}` 分 → `res[{arr[i][1]}] = {res[arr[i][1]]}`',
        'res[arr[i][1]] += even': '原下标 `{arr[i][1]}` 加 `even = {even}` 分 → `res[{arr[i][1]}] = {res[arr[i][1]]}`',
        'if arr[j][0] % 2 == 0': lambda S, B, r: f'右元素 `{S.arr[S.j][0]}` 是{"偶" if S.arr[S.j][0] % 2 == 0 else "奇"}数 → 登记到 `{"even" if S.arr[S.j][0] % 2 == 0 else "odd"}`',
        'even += 1': '`even` → {even}',
        'odd += 1': '`odd` → {odd}',
        'arr[index] = tmp': '把合并好的 `tmp` 写回 `arr[{left}..{right}]`，这一段变有序',
        'return res': '每个下标的得分：`{res}`',
    },
    cards=dict(
        one_liner='归并排序时顺手数逆序对，再按奇偶分开计数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums`，下标对 `(i, j)` 满足 `i < j`、`nums[j] < nums[i]`、且奇偶性不同',
                 '每个这样的 `(i, j)` 让下标 `i` 得 1 分',
                 '返回每个下标的得分数组',
                 '示例：`[4,1,3,2]` → `[2,0,1,0]`'],
        quote='若当前的左侧元素较小，那么就说明剩下的右侧元素都比它大，而之前已经归并进去的右侧元素都比它小，因此之前有多少个处理完的右侧元素，就可以形成多少个逆序对。',
        quote_src='—— yiduobo 题解原文',
        idea=['不看奇偶，就是「每个元素右边有几个更小」的逆序对问题，用归并排序统计',
              '本题要分奇偶：合并时分别维护已放入的右半 `odd`、`even` 个数',
              '放左元素时：偶数加 `odd`，奇数加 `even`',
              '排序会打乱位置，所以数组里存 `(值, 原下标)`，按原下标记分'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：存 `(值, 原下标)`，答案按原下标累加，不是按排序后位置',
                 '`<=`：相等时先放左边，保证相等值不算逆序对',
                 '若 n = 1，`calc` 直接返回，答案全 0'],
    ),
)
