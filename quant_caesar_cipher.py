def shiftText(C, N):
    '''
    shiftText function shifts the string C to N places
    Args:
        C(string): string to be shifted
        N(int): number of places to be shifted
    '''
    # See http://ascii.cl/
    upper = {ascii:chr(ascii) for ascii in getRangeList(65,91)}
    lower = {ascii:chr(ascii) for ascii in getRangeList(97,123)}
    digit = {ascii:chr(ascii) for ascii in getRangeList(48,58)}

    for c in C:
        o = ord(c)
        # Do not change symbols and digits
        if (o not in upper and o not in lower) or o in digit:
            yield o
        else:
            # If it's in the upper case and
            # that the rotation is within the uppercase
            if o in upper and o + N % 26 in upper:
                yield o + N % 26
            # If it's in the lower case and
            # that the rotation is within the lowercase
            elif o in lower and o + N % 26 in lower:
                yield o + N % 26
            # Otherwise move back 26 spaces after rotation.
            else: # alphabet.
                yield o + N % 26 -26

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
    rangeList += [current]
    current += step
  return rangeList

def KMPSearch(haystack, needle):
    '''
    Start KMP searching using the principle shown in the getNext function. 
    The KMP matching algorithm uses degenerating property (pattern having same sub-patterns appearing more 
    than once in the pattern) of the pattern and improves the worst case complexity to O(n).
    '''
    if not needle:
        return 0

    haystack = ''.join(haystack)
    needle = ''.join(needle)

    length_hay = getListLength(haystack)
    length_needle = getListLength(needle)
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

    S = input("Enter string S: ") 
    C = input("Enter string C: ") 
    N = int(input("Enter number N: "))

    return(S, C, N)

def partA(S_List, S_Len, C_List, C_Len, N):

    C_SHIFT = ''.join(map(chr, shiftText(''.join(C_List), N)))
    
    S_FIRST_THIRD = S_List[:int(S_Len/3)]
    S_SECOND_THIRD = S_List[int(S_Len/3):]

    i = 0

    while(i < getListLength(S_FIRST_THIRD)):
        search_in_first_half = KMPSearch(S_FIRST_THIRD, C_List)
        search_in_second_half = KMPSearch(S_SECOND_THIRD, C_SHIFT)

        if search_in_first_half != -1 and search_in_second_half != 1:
            S_FIRST_THIRD = list(S_FIRST_THIRD)
            S_FIRST_THIRD[search_in_first_half:(search_in_first_half+getListLength(C_List))] = list(C_SHIFT)
            S_FIRST_THIRD = ''.join(S_FIRST_THIRD)

            S_SECOND_THIRD = list(S_SECOND_THIRD)
            S_SECOND_THIRD[search_in_second_half:(search_in_second_half+getListLength(C_List))] = list(C_List)
            S_SECOND_THIRD = ''.join(S_SECOND_THIRD)
        else:
            i = i + 1

    return S_FIRST_THIRD + S_SECOND_THIRD

def partB(S_List, S_Len, C_List, C_Len, N):

  C_SHIFT = ''.join(map(chr, shiftText(''.join(C_List), N)))

  if(''.join(C_List) == C_SHIFT ):
    return ''.join(S_List)

  S_FIRST_THIRD = S_List[:int(S_Len/3)]
  S_SECOND_THIRD = S_List[int(S_Len/3):]

  search_in_first_half = KMPSearch(S_FIRST_THIRD, C_List)
  search_in_second_half = KMPSearch(S_SECOND_THIRD, C_SHIFT)

  if search_in_first_half >= 0 and search_in_second_half >= 0:
    S_List[search_in_first_half:search_in_first_half+C_Len] = list(C_SHIFT)
    S_List[int(S_Len/3)+search_in_second_half:int(S_Len/3)+search_in_second_half+C_Len] = C_List
  else:
    return ''.join(S_List)

  return partB(S_List, S_Len, C_List, C_Len, N)
    
def main():

    #temporary input
    S = 'ABCXXABCXXBCDXXBCD'
    C = 'ABC'
    N = 1

    #S, C, N = takeInputFromUser()

    print('S = ', S)
    print('C = ', C)
    print('N = ', N)

    C_SHIFT = (''.join(map(chr, shiftText(C, N))))

    print('C_SHIFT = ' , C_SHIFT)

    S_List = list(S)
    C_List = list(C)
    S_Len = getListLength(S_List)
    C_Len = getListLength(C_List)

    S_PART_A = partA(S_List, S_Len, C_List, C_Len, N)
    S_PART_B = partB(S_List, S_Len, C_List, C_Len, N)

    print('S_PART_A = ' , S_PART_A)
    print('S_PART_B = ' , S_PART_B)

def unittest():
  """
  This function runs all the unit test cases for all utility functions.
  """

  print("Running all unit test cases...")

  print("TEST 1: getListLength(...): ")
  if( getListLength([10,3,2,7]) == 4 ):
    print("TEST 1 passed")
  else:
    print("TEST 1 failed")

  print("TEST 2: getRangeList(...): ")
  if( getRangeList(0,5) == [0,1,2,3,4] ):
    print("TEST 2 passed")
  else:
    print("TEST 2 failed")

  print("TEST 3: shiftText(...): ")
  if( (''.join(map(chr, shiftText('ABC', 1)))) == 'BCD' ):
    print("TEST 3 passed")
  else:
    print("TEST 3 failed")

  print("TEST 4: KMPSearch(...): ")
  if(KMPSearch(list("ABC"),list("BC"))==1):
    print("TEST 4 passed")
  else:
    print("TEST 4 failed")

  print("TEST 5: partA(...): ")
  if(partA(list('ABCXXABCXXBCDXXBCD'), 18, list('ABC'), 3, 1)=='BCDXXABCXXABCXXBCD'):
    print("TEST 5 passed")
  else:
    print("TEST 5 failed")

  print('all tests have been finished...\n')

if __name__ == "__main__":
  unittest()
  main()
  
