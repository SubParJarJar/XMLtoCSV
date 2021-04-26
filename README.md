# XMLtoCSV
WIP currently working on dynamically creating new headers in streaming mode.
Recursive xml to csv function:

  
1. Parent searches for data in child (child.text)
   :: If data, save to list
   
2. At the same time checks for grandchildren
  :: If grandchildren, add to dict {child_elem: [grandchildren]}.
  :: Tag: no_grandchildren is set to False.
  
3. If no grandchildren, write to file

4. If grandchildren, restart function for child
