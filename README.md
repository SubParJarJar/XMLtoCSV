# XMLtoCSV
WIP recursive xml to csv function

  
1. Parent searches for data in child (child.text)
  a. If data, save to list
2. At the same time checks for grandchildren
  a. If grandchildren, add to dict {child_elem: [grandchildren]}.
  b. Tag: no_grandchildren is set to False.
3. If no grandchildren, write to file
4. If grandchildren, restart function for child
