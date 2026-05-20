# 📝 LeetCode [1]：[两数之和]

- **题目链接**: https://leetcode.cn/studyplan/top-100-liked/
- **刷题日期**: 2026-05-20
- **模块分类**: [01. 哈希 (Hash)]

**题目**：给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出和为目标值的那两个整数，并返回它们的数组下标。

---

## 方法一：暴力双循环 — 保证正确的最笨办法

### 解题思路
拿到题的第一反应就是穷举所有两数组合。思路分三步走：

1. **固定第一个数**：用外层循环遍历数组，当前元素作为第一个加数。
2. **在剩余元素中找第二个数**：内层循环从 `i+1` 开始，避免重复组合，也防止同一个元素用两次。
3. **命中即返回**：一旦两数之和等于 `target`，立刻返回它们的下标。

### 核心代码
```python
def twoSum(self, nums, target):
    n = len(nums)
    # 外层循环：固定第一个数
    for i in range(n):
        # 内层从 i+1 开始，不回头、不加自己
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
```

### 复杂度与易错点
- **时间复杂度**：\(O(n^2)\) — 最坏情况要检查约 \(n^2/2\) 对组合。
- **空间复杂度**：\(O(1)\) — 没有使用额外空间。
- **极易写错的地方**：
  - 内层循环若从 `0` 开始，可能返回 `[i,i]`，同一个元素被用了两次。
  - 返回值顺序无所谓，但必须都是原始索引。

### 为什么不满足于此？
内层循环的本质是**在一个区间里线性查找一个特定值**，复杂度是 \(O(n)\)。算法优化的第一步，往往就是“把查找变快”。

---

## 方法二：排序 + 二分查找 — 用空间换时间的第一次尝试

查找变快的最经典手段是二分查找，但它有一个铁打的前提：**数组必须有序**。原数组是乱序的，直接二分就是瞎找。所以整体思路分三步：

1. **备份索引**：在排序前，用“模板”把每个数的原始下标存下来。
2. **排序**：让数组有序，为二分创造条件。
3. **二分查找配对值**：固定第一个数，在右侧有序区间二分查找 `target - nums[i]`，找到后用模板取回原始下标。

下面把排序的两种实现拆开：**手写快速排序** 和 **调库 `.sort()`**。

---

### 方法二 A：手写快速排序 + 二分查找

#### 解题思路
面试官想看手写排序，我就用原地快排。整个流程拆成四步：

1. **备份模板**：遍历数组，把 `(值, 原始索引)` 成对存入列表。
2. **手写快速排序**：
   - 选最左元素为基准，左右指针交替扫描。
   - 右侧找比基准小的，左侧找比基准大的，找到后交换。
   - 基准归位后，递归处理左右子数组。
3. **固定一个数，二分查另一个**：排序后遍历，对每个 `nums[i]` 计算 `need = target - nums[i]`，在 `[i+1, len-1]` 区间做标准二分查找。
4. **用模板还原索引**：遍历模板，找到两个值对应的原始下标。注意加 `idx != first_idx` 保证重复值时不会拿到同一个索引。

#### 核心代码
```python
def twoSum(self, nums, target):
    # 1. 备份模板：(值, 原始索引)
    backup = [(nums[i], i) for i in range(len(nums))]

    # 2. 手写快速排序（原地排序，直接修改 nums）
    def quicksort(arr, left, right):
        if left >= right:
            return
        pivot = arr[left]       # 选择最左元素为基准
        i, j = left, right
        while i < j:
            # 从右向左找第一个小于基准的数
            while i < j and arr[j] >= pivot:
                j -= 1
            arr[i] = arr[j]
            # 从左向右找第一个大于基准的数
            while i < j and arr[i] <= pivot:
                i += 1
            arr[j] = arr[i]
        arr[i] = pivot          # 基准归位
        quicksort(arr, left, i - 1)
        quicksort(arr, i + 1, right)

    quicksort(nums, 0, len(nums) - 1)   # nums 已有序

    # 3. 遍历排序后数组，二分查找配对值
    first_val = second_val = None
    for i in range(len(nums) - 1):
        need = target - nums[i]          # 要查找的目标值
        left, right = i + 1, len(nums) - 1
        while left <= right:             # 标准二分查找模板
            mid = (left + right) // 2
            if nums[mid] == need:
                first_val, second_val = nums[i], need
                break
            elif nums[mid] < need:
                left = mid + 1
            else:
                right = mid - 1
        if first_val is not None:
            break

    # 4. 从模板中取回原始索引，防止重复值拿到同一个索引
    first_idx = second_idx = -1
    for val, idx in backup:
        if val == first_val and first_idx == -1:
            first_idx = idx
        elif val == second_val and idx != first_idx:   # 确保两个索引不同
            second_idx = idx
        if first_idx != -1 and second_idx != -1:
            return [first_idx, second_idx]
```

#### 复杂度与易错点
- **时间**：平均 \(O(n \log n)\)，最坏 \(O(n^2)\)（若每次选到极值基准）。
- **空间**：快排递归栈 \(O(\log n)\)，模板 \(O(n)\)。
- **极易出错的地方**：
  - 手写快排时 `while i < j` 内层循环必须严格先右后左，否则基准归位逻辑会错乱。
  - 二分查找 `left <= right`，更新边界要 `mid±1`，否则死循环。
  - 找回索引时，如果两个数相同，必须用 `idx != first_idx` 避免拿到同一个位置。

---

### 方法二 B：调库 `sort()` + 二分查找

#### 解题思路
自己写排序容易出 bug，且 Python 自带的 `list.sort()` 底层是 Timsort，混合排序，稳定且高效。工程上直接用现成的。步骤与手写版一致，只是排序交给内置方法：

1. **备份模板**：同方法二 A。
2. **调用 `nums.sort()`** 原地排序，干净利落。
3. **二分查找配对值**：逻辑完全同上。
4. **用模板还原索引**：同样注意去重判断。

#### 核心代码
```python
def twoSum(self, nums, target):
    # 备份模板
    backup = [(nums[i], i) for i in range(len(nums))]
    # 直接使用 Python 内建排序，原地排序，稳定且高效
    nums.sort()

    first_val = second_val = None
    for i in range(len(nums) - 1):
        need = target - nums[i]
        left, right = i + 1, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == need:
                first_val, second_val = nums[i], need
                break
            elif nums[mid] < need:
                left = mid + 1
            else:
                right = mid - 1
        if first_val is not None:
            break

    first_idx = second_idx = -1
    for val, idx in backup:
        if val == first_val and first_idx == -1:
            first_idx = idx
        elif val == second_val and idx != first_idx:
            second_idx = idx
        if first_idx != -1 and second_idx != -1:
            return [first_idx, second_idx]
```

#### 复杂度与易错点
- **时间**：\(O(n \log n)\)，常数因子远小于手写快排。
- **空间**：模板 \(O(n)\)，排序原地。
- **易错点**：
  - 仍然要处理重复值取索引的问题。
  - `sort()` 会改变原数组，如果题目不允许修改输入，需要先拷贝一份。

#### 手写 vs 调库：面试时怎么说
- 手写版用于展示对排序算法的理解，尤其是 Partition 过程。
- 调库版表达工程素养：知道“不重复造轮子”，并能讲出 Timsort 的优势（稳定、自适应的归并排序）。
- 实际面试中，先写调库版说清思路，如果面试官要求手写排序，再补上手写实现。

### 思路过渡：还能再快吗？
排序 + 二分已经是 \(O(n \log n)\)，但每次查找都还要 \(O(\log n)\)，而且排序的 \(O(n \log n)\) 省不掉。有没有一种方法，不用排序，还能让查找变成 \(O(1)\)？  
答案就是**哈希表**。

---

## 方法三：哈希表一次遍历 — 时间与空间的终极平衡

### 解题思路
我搞一个字典 `seen`，存“值 → 索引”。整个过程只遍历一次，每一步分三个动作：

1. **计算需求的数**：`need = target - 当前数`。
2. **先查哈希表**：看 `need` 是否已经在 `seen` 中。如果在，直接返回 `[seen[need], 当前索引]`。
3. **后存自己**：如果没找到，把 `(当前值, 当前索引)` 存入 `seen`，供后续元素使用。

这里的关键是**必须先查后存**。如果顺序反过来，当 `target = 2 * num` 时，会刚把自己存进去就立刻查到自己，返回两个相同索引，导致错误。

### 核心代码
```python
def twoSum(self, nums, target):
    seen = {}                     # 哈希表、
    for i, num in enumerate(nums):
        need = target - num
        if need in seen:          # 先查之前是否有存储过
            return [seen[need], i]
        seen[num] = i             # 没有则进行存储
```

### 复杂度与易错点
- **时间**：\(O(n)\) — 每个元素只看一次，字典查找平均 \(O(1)\)。
- **空间**：\(O(n)\) — 最坏要存下所有元素。
- **极容易出错的顺序问题**：
  - **先查后存**是正确姿势。先存后查会在 `target = 2 * num` 时自己配对自己。
  - 如果用列表代替字典（`if need in seen` 但 `seen` 是 list），查找退化为 \(O(n)\)，整体又回到 \(O(n^2)\)。

### 为什么这是最优解？
在不修改数组且不预先知道任何顺序信息的前提下，\(O(n)\) 时间 + \(O(n)\) 空间是两数之和问题的最低复杂度下界（因为至少需要扫描一遍数组）。哈希表完美达到了这个下界。

---

## 面试时可能被追问的高阶问题

1. **如果输入数组已经有序，能进一步优化空间吗？**
   - 能。用**双指针**：头尾各一个指针，两数之和大于 `target` 就右指针左移，小于就左指针右移。时间 \(O(n)\)，空间 \(O(1)\)。

2. **如果要求返回所有和为 target 的不重复索引对？**
   - 哈希表方法可扩展。找到一个配对后不 `return`，而是把 `(seen[need], i)` 加入结果列表，并跳过重复值避免结果集重复。

3. **Python 的字典为什么能做到 O(1) 查找？**
   - 底层是哈希表。通过哈希函数把键映射到一个整数，再映射到数组下标。理想情况无冲突，一次定位；冲突时 Python 使用开放地址法解决，平均依然是 O(1)。

4. **Two Sum 的思想如何迁移到 3Sum、4Sum？**
   - 3Sum 先排序，固定第一个数，然后在剩余数组上做两数之和（双指针）。4Sum 同理，固定前两个数，再套一层双指针。核心都是在有序数组上利用双指针将多层循环降维，从 \(O(n^3)\) 降到 \(O(n^2)\)。

---

## 总结：我今天真正掌握了什么

这道题教会我的不是一种解法，而是一整套 **查找优化的思维链路**：

- **暴力枚举** → 内层循环就是“线性查找”，优化它。
- **排序 + 二分** → 用 \(O(\log n)\) 的查找替代 \(O(n)\) 的遍历，代价是排序的 \(O(n \log n)\) 和备份索引的空间。手写快排和调库 `sort` 两种实现，分别对应“展示内功”和“工程务实”。
- **哈希表** → 用 \(O(1)\) 的查找直接省掉排序，空间换时间，一针见血。
- **双指针** → 当有序条件满足时，把空间也省到 \(O(1)\)，是特定场景下的最优。

以后碰到任何“在数组里找几个数满足某种和”的问题，我脑子里第一时间跳出来的就是这条路：能不能排序？要不要空间换时间？有没有可能双指针？这道题是地基，地基扎稳了，3Sum、4Sum 不过是往上面盖楼。