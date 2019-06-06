'''
Fidelity Quant Assessment
Author - Amal Radhakrishnan

Instructions to run - python quant_caesar_cipher.py
'''

'''
Importing unittest for testcases.
If this could not be done, I would have gone ahead and written if-else cases for test cases.
Assuming the utiltiy functions were meant for range, length etc.
'''
import unittest

def shiftText(C, N):
    '''
    shiftText function shifts the string C to N places.
    I have used ascii characters to define the ranges for upper, lower and digit characters.
    No change on symbols and digits.
    Rotation on uppercase and lowercase characters.
    Args:
        C(string): string to be shifted
        N(int): number of places to be shifted
    '''
    #see http://ascii.cl/
    upper = {ascii:chr(ascii) for ascii in getRangeList(65,91)}
    lower = {ascii:chr(ascii) for ascii in getRangeList(97,123)}
    digit = {ascii:chr(ascii) for ascii in getRangeList(48,58)}

    for c in C:
        o = ord(c)
        # Do not change symbols and digits
        if (o not in upper and o not in lower) or o in digit:
            cipher = cipher + o
        else:
            # If it's in the upper case and
            # that the rotation is within the uppercase
            if o in upper and o + N % 26 in upper:
                cipher = cipher + str(o) + str(N % 26)
            # If it's in the lower case and
            # that the rotation is within the lowercase
            elif o in lower and o + N % 26 in lower:
                cipher = cipher + o + str(N % 26)
            # Otherwise move back 26 space
            # s after rotation.
            else: # alphabet.
                cipher = cipher + o + str(N % 26 -26)

def getListLength(myList):
  """
  getListLength function returns the length of an array
  Args:
    myList(list): array for which the length has to be calculated
  Returns:
    length(int) : length of array
  """
  length = 0

  #iterate through each element in the list
  for element in myList:
      #increment length by 1 as each element is visited
    length += 1
  return length

def getRangeList(start, end, step=1):
  """
  getARange function recreates the range functionality in python
  Args:
    start(int): starting index
    end(int): ending index
    step(int): step size of the consecutive elements in the range
  Returns:
    rangeList(list): A list of values within the range and the given step value
  """
  rangeList = []
  current = start

  while(current < end):
    #append current to rangeList
    rangeList += [current]
    #increment current by step size
    current += step
  return rangeList

def ceil(num):
  """
  ceil function recreates the math.ceil function in python
  Args:
    num(float): value to find ceil for
  Returns:
    (int): ceil value of num
  """

  inum = int(num)
  if num == float(inum):
    return inum
  return inum + 1

def listToString(myList):
  """
  listToString function converts list of string into a single string
  Args:
    myList(list): list of string
  Returns:
    (string): combined string
  """
  return ''.join(myList)


def KMPSearch(haystack, needle):
    '''
    Start KMP searching using the principle shown in the getNext function. 
    The KMP matching algorithm uses degenerating property (pattern having same sub-patterns appearing more 
    than once in the pattern) of the pattern and improves the worst case complexity to O(n).
    '''

    #needle is empty condition
    if not needle:
        return 0

    haystack = listToString(haystack)
    needle = listToString(needle)

    #length of hay and needle
    length_hay = getListLength(haystack)
    length_needle = getListLength(needle)

    #list of integers next tells us the count of characters to be skipped. 
    next = getNext(needle)
    i = 0
    j = 0

    while i < length_hay:
        if j == -1 or needle[j] == haystack[i]:
            j += 1
            i += 1
            if j == length_needle:
                return i - j
        else:
            j = next[j]
    
    return -1
  
def getNext(needle):
    '''
    Given a Pattern String "abdyab", we can get next = [-1, 0, 0, 0, 0, 1]
    For example:
    Pattern: "a b d y a b"
    First: "0 0 0 0 1 2"
    SubString that begins from the beginning to 'a' has no match of prefix and suffix, so we get 0.
    Same as 'b' , 'd', y', till 'a'. Now you can see the first 'a' (prefix) matches this 'a'(suffix), and the matched length is 1, So we get 1.
    You can go all the way to the end. Then: Right shift by one bit and put '-1' on the first element.
    Thus, you get '-1, 0, 0, 0, 0, 1'
    '''
    nextL = []
    nextL = nextL + [-1]
    length = getListLength(needle)
    j = 0
    k = -1

    # the loop calculates next[i] for i = 0 to length - 1
    while j < length - 1:
        if k == -1 or needle[j] == needle[k]:
            j += 1
            k += 1
            nextL = nextL + [k]
        else:
            k = nextL[k]
    return nextL

def takeInputFromUser():
    '''
    Function to take input from the user
    Return:
        S(string): string S
        C(string): string C
        N(int): number of places to shift
    '''

    #take input from the user
    S = input("Enter string S: ") 
    C = input("Enter string C: ") 
    N = int(input("Enter number N: "))

    return(S, C, N)

def switches_occurrences_part_a(S_List, S_Len, C_List, C_Len, N):
  '''
  switches_occurrences_part_a function solves for part A.

  Args: 
    S_List(list): string S converted into list
    S_Len(int): length of string S
    C_List(list): string C converted into list
    C_Len(list): length of string C
    N(int): number of letters by which C should be shifted
  '''

  #calculate C_SHIFT using the shiftText function
  C_SHIFT = listToString(map(chr, shiftText(listToString(C_List), N)))

  if(listToString(C_List) == C_SHIFT ):
    return listToString(S_List)
  
  S_FIRST_THIRD = S_List[:int(S_Len/3)]
  S_SECOND_THIRD = S_List[int(S_Len/3):]

  while True:
      search_in_first_half = KMPSearch(S_FIRST_THIRD, C_List)
      search_in_second_half = KMPSearch(S_SECOND_THIRD, C_SHIFT)

      if search_in_first_half != -1 and search_in_second_half != 1:
          S_FIRST_THIRD = list(S_FIRST_THIRD)
          S_FIRST_THIRD[search_in_first_half:(search_in_first_half+getListLength(C_List))] = list(C_SHIFT)
          S_FIRST_THIRD = listToString(S_FIRST_THIRD)

          S_SECOND_THIRD = list(S_SECOND_THIRD)
          S_SECOND_THIRD[search_in_second_half:(search_in_second_half+getListLength(C_List))] = list(C_List)
          S_SECOND_THIRD = listToString(S_SECOND_THIRD)
      else:
        return S_FIRST_THIRD + S_SECOND_THIRD

def switches_occurrences_recursion_part_b(S_List, S_Len, C_List, C_Len, N):
  '''
  switches_occurrences_part_a function solves for part A

  Args: 
    S_List(list): string S converted into list
    S_Len(int): length of string S
    C_List(list): string C converted into list
    C_Len(list): length of string C
    N(int): number of letters by which C should be shifted
  '''

  #calculate C_SHIFT using the shiftText function
  C_SHIFT = listToString(map(chr, shiftText(listToString(C_List), N)))

  if(listToString(C_List) == C_SHIFT ):
    return listToString(S_List)

  S_FIRST_THIRD = S_List[:ceil(S_Len/3)]
  S_SECOND_THIRD = S_List[ceil(S_Len/3):]

  search_in_first_half = KMPSearch(S_FIRST_THIRD, C_List)
  search_in_second_half = KMPSearch(S_SECOND_THIRD, C_SHIFT)

  if search_in_first_half >= 0 and search_in_second_half >= 0:
    S_List[search_in_first_half:search_in_first_half+C_Len] = list(C_SHIFT)
    S_List[int(S_Len/3)+search_in_second_half:int(S_Len/3)+search_in_second_half+C_Len] = C_List
  else:
    return listToString(S_List)

  return switches_occurrences_recursion_part_b(S_List, S_Len, C_List, C_Len, N)

def disperse(S_SECOND_THIRD, C_SHIFT):
  '''

  '''

  search_in_second_half = []
  index = 0
  
  for i in getRangeList(0, getListLength(C_SHIFT)):
    for k in getRangeList(0, getListLength(S_SECOND_THIRD)):
      if C_SHIFT[i] == S_SECOND_THIRD[k] and k >= index:
        index = k
        search_in_second_half = search_in_second_half + [k]
        break

  return search_in_second_half

def disperse_occurrences_part_c(S_List, S_Len, C_List, C_Len, N):
  '''
  switches_occurrences_part_a function solves for part A

  Args: 
    S_List(list): string S converted into list
    S_Len(int): length of string S
    C_List(list): string C converted into list
    C_Len(list): length of string C
    N(int): number of letters by which C should be shifted
  '''

  #calculate C_SHIFT using the shiftText function
  C_SHIFT = list(listToString(map(chr, shiftText(listToString(C_List), N))))

  if(listToString(C_List) == C_SHIFT ):
    return listToString(S_List)
  
  S_FIRST_THIRD = S_List[:ceil(S_Len/3)]
  S_SECOND_THIRD = S_List[ceil(S_Len/3):]

  while True:
    search_in_first_half = KMPSearch(S_FIRST_THIRD, C_List)
    search_in_second_half = disperse(S_SECOND_THIRD, C_SHIFT)

    if getListLength(search_in_second_half) == 3 and (search_in_first_half != -1) == True:
      S_FIRST_THIRD = list(S_FIRST_THIRD)
      S_FIRST_THIRD[search_in_first_half:(search_in_first_half+getListLength(C_List))] = list(C_SHIFT)
      S_FIRST_THIRD = listToString(S_FIRST_THIRD)

      for k in range(len(search_in_second_half)):
        S_SECOND_THIRD[search_in_second_half[k]] = C_List[k]
    else:
      return listToString(S_FIRST_THIRD) + listToString(S_SECOND_THIRD)

def disperse_occurrences_recursion_part_d(S_List, S_Len, C_List, C_Len, N):
  '''
  switches_occurrences_part_a function solves for part A

  Args: 
    S_List(list): string S converted into list
    S_Len(int): length of string S
    C_List(list): string C converted into list
    C_Len(list): length of string C
    N(int): number of letters by which C should be shifted
  '''

  #calculate C_SHIFT using the shiftText function
  C_SHIFT = list(listToString(map(chr, shiftText(listToString(C_List), N))))

  if(listToString(C_List) == C_SHIFT ):
    return listToString(S_List)
  
  S_FIRST_THIRD = S_List[:ceil(S_Len/3)]
  S_SECOND_THIRD = S_List[ceil(S_Len/3):]

  search_in_first_half = KMPSearch(S_FIRST_THIRD, C_List)
  search_in_second_half = disperse(S_SECOND_THIRD, C_SHIFT)

  if getListLength(search_in_second_half) == 3 and search_in_first_half != -1:
    S_List[search_in_first_half:search_in_first_half+C_Len] = C_SHIFT
    for i in getRangeList(0,C_Len):
      S_List[ceil(S_Len/3)+search_in_second_half[i]] = C_List[i]
  else:
    return listToString(S_List)

  return disperse_occurrences_recursion_part_d(S_List, S_Len, C_List, C_Len, N)
    
def main():

  #temporary input
  S = 'AABCXABCXXBCDXXBCD'
  C = 'ABC'
  N = 1

  #S, C, N = takeInputFromUser()

  print('S = ', S)
  print('C = ', C)
  print('N = ', N)

  C_SHIFT = (listToString(map(chr, shiftText(C, N))))

  print('C_SHIFT = ' , C_SHIFT)

  S_List = list(S)
  C_List = list(C)
  S_Len = getListLength(S_List)
  C_Len = getListLength(C_List)

  S_PART_A = switches_occurrences_part_a(S_List, S_Len, C_List, C_Len, N)
  S_PART_B = switches_occurrences_recursion_part_b(S_List, S_Len, C_List, C_Len, N)
  #S_PART_C = partC(S_List, S_Len, C_List, C_Len, N)
  #S_PART_D = partD(S_List, S_Len, C_List, C_Len, N)

  print('S_PART_A = ' , S_PART_A)
  print('S_PART_B = ' , S_PART_B)
  #print('S_PART_C = ' , S_PART_C)
  #print('S_PART_D = ' , S_PART_D)

class TestMethods(unittest.TestCase):
    '''
    class for all the unit test cases.
    '''

    def test_getListLength(self):
      self.assertEqual(getListLength([10,3,2,7]), 4)

    def test_getRangeList(self):
      self.assertEqual(getRangeList(0,5), [0,1,2,3,4])

    def test_shiftText(self):
      self.assertEqual(listToString(map(chr, shiftText('ABC', 1))), 'BCD')

    def test_KMPSearch(self):
      self.assertTrue(KMPSearch(list("ABC"),list("BC")))

    def test_partA(self):
      self.assertEqual(switches_occurrences_part_a(list('ABCXXABCXXBCDXXBCD'), 18, list('ABC'), 3, 1), 'BCDXXABCXXABCXXBCD')
    
    def test_partB(self):
      self.assertEqual(switches_occurrences_recursion_part_b(list('ABCXXABCXXBCDXXBCD'), 18, list('ABC'), 3, 1), 'BCDXXABCXXABCXXBCD')
    
    def test_partC(self):
      self.assertEqual(disperse_occurrences_part_c(list('ABCXXABCXXBXXCXDXBCD'), 20, list('ABC'), 3, 1), 'BCDXXABCXXAXXBXCXBCD')

    def test_partD(self):
      self.assertEqual(disperse_occurrences_recursion_part_d(list('ABCXXABCXXBXXCXDXBCD'), 20, list('ABC'), 3, 1), 'BCDXXABCXXAXXBXCXBCD')

    def test_listToString(self):
      self.assertEqual(listToString(['A','B','C','D','E','F','G']), 'ABCDEFG')

if __name__ == "__main__":
  runner = unittest.TextTestRunner(verbosity=2)
  unittest.main(testRunner=runner, exit=False)
  main()