Option Compare Database
Private re As RegExp, re_alpha As RegExp, re_attn As RegExp, re_po As RegExp, re_comma As RegExp, re_dash As RegExp
Private reNum As String, reDir As String, reStreet As String
Private st As Streets

Sub initSplit()
    'set up some global variables to speed up processing
    
    Set st = New Streets
    
    '--build main regex--'
    reNum = "^(?:((?:[0-9,&/ -]|and)*(?:[a-z])?) )"
    reDir = "(?:(NORTH|SOUTH|EAST|WEST|[NSEW]\.?) )?"
    reStreet = "((?:[0-9]+(?:ST|ND|RD|TH)|(?:[a-z])).*?)"
    reAlphaStreet = "([a-z])"
    reSuffix = "(?: +" & st.StreetRegEx & "(?:\.)?(?: +(NORTH|SOUTH|EAST|WEST|NW|SW|NE|SE|[NSEW]))?(?:,? +(.*))?)?$"

    '--set up regular expressions--'
    'main regex
    Set re = New RegExp
    re.Pattern = reNum & reDir & reStreet & reSuffix 'build the main regex
    re.IgnoreCase = True 'True to ignore case
    re.Global = False 'False matches the first occurrence
    'alpha street (A Street, B Street, etc) regex\
    Set re_alpha = New RegExp
    re_alpha.Pattern = reNum & reDir & reAlphaStreet & reSuffix
    re_alpha.IgnoreCase = True 'True to ignore case
    re_alpha.Global = False 'False matches the first occurrence
    'attn regex
    Set re_attn = New RegExp
    re_attn.Pattern = "^(ATTN|C/O)"
    re_attn.Global = False
    re_attn.IgnoreCase = True
    'PO regex
    Set re_po = New RegExp
    re_po.Pattern = "^(P[. ]? ?O.? +Box +)"
    re_po.Global = False
    re_po.IgnoreCase = True
    'change & to commas
    Set re_comma = New RegExp
    re_comma.Pattern = " *([&/,]|AND) *"
    re_comma.Global = True 'True matches all occurrences
    'fix dashes
    Set re_dash = New RegExp
    re_dash.Pattern = " *- *"
    re_dash.Global = True 'True matches all occurrences
End Sub

Function isAddress(address) As Boolean
    'check if the regex has been initialized. If it hasn't, do it
    If reNum = vbNullString Then
        initSplit
    End If
    
    If Not IsNull(address) Then
        If re_alpha.Test(address) Or re.Test(address) Then
            isAddress = True
        End If
    End If
End Function

Function multipleNumbers(numbers) As Boolean
    If Not IsNull(numbers) Then
        If InStr(1, numbers, ",") > 0 Or InStr(1, numbers, "-") > 0 Then
            multipleNumbers = True
        End If
    End If
End Function

Function badAddress(address) As Boolean
    'check if the regex has been initialized. If it hasn't, do it
    If reNum = vbNullString Then
        initSplit
    End If
    
    If Not IsNull(address) Then
        If re_alpha.Test(address) Or re.Test(address) Then
            If re_alpha.Test(address) Then
                Set matches = re_alpha.Execute(address)
            ElseIf re.Test(address) Then
                Set matches = re.Execute(address)
            End If
            If re_alpha.Test(matches(0).SubMatches(5)) Or re_alpha.Test(matches(0).SubMatches(5)) Then
                badAddress = True
            End If
        End If
    End If
End Function

Function isPO(address) As Boolean
    'check if the regex has been initialized. If it hasn't, do it
    If reNum = vbNullString Then
        initSplit
    End If
    
    If Not IsNull(address) Then
        If re_po.Test(address) Then
            isPO = True
        End If
    End If
End Function

Function splitAddress(address1, address2, Optional returnPiece As String = vbNullString, Optional hasAttn As Boolean = False) As String
    'A function to return an piece of an address
    'Set-up must be done first through initSplit
    Dim matches
    Dim attn As String, number As String, direction As String, street As String, suffix As String, address As String, possible2 As String
    
    'check if the regex has been initialized. If it hasn't, do it
    If reNum = vbNullString Then
        initSplit
    End If
    
    '--turn nulls to blanks--'
    'address1
    If IsNull(address1) Then
        'nulls will cause an error otherwise
        address1 = vbNullString
    Else
        'trim leading & trailing spaces to help the regex
        address1 = Trim(address1)
    End If
    'address2
    If IsNull(address2) Then
        address2 = vbNullString
    Else
        address2 = Trim(address2)
    End If

    '--check for attn line (if requested)--'
    If hasAttn Then
        'if line 1 is an attn line
        If re_attn.Test(address1) Then
            'pull it out to the attn field
            attn = address1
            'push address2 to the first field
            address1 = address2
            address2 = vbNullString
        ElseIf re_attn.Test(address2) Then
            attn = address2
            address2 = vbNullString
        End If
    End If

    '--check for address location--'
    If re.Test(address1) Or re_alpha.Test(address1) Then
        address = address1
    ElseIf re.Test(address2) Or re_alpha.Test(address2) Then 'if the 1 is not an address, and 2 is
        'switch the addresses
        address = address2
        address2 = address1
    Else
        address = address1 'pass along the first, it won't be split
    End If

    '--check for PO boxes (to move to addr2)
    If re_po.Test(address1) Then
        If Not Len(address2) > 0 Then
            address2 = address
            address = vbNullString
            address2 = re_po.Replace(address2, "P.O. Box ")
        End If
    End If

    '--split and fix the addresses--'
    If re.Test(address) Or re_alpha.Test(address) Then
        'try to split the address
        If re_alpha.Test(address) Then
            'if the address follows matches the a street regex, use that
            Set matches = re_alpha.Execute(address)
        ElseIf re.Test(address) Then
            'Otherwise use the regular regex
            Set matches = re.Execute(address)
        End If
        number = matches(0).SubMatches(0)
        direction = matches(0).SubMatches(1)
        street = matches(0).SubMatches(2)
        suffix = matches(0).SubMatches(3)
        direction2 = matches(0).SubMatches(4)
        possible2 = matches(0).SubMatches(5)

        '-fix pieces-'
        'replace punctuation in the number
        number = re_comma.Replace(number, ", ")
        number = re_dash.Replace(number, "-")
        'upper-case the street directions
        If Len(direction) > 1 Then direction = UCase(Left(direction, 1))
        If Len(direction2) > 1 Then direction2 = UCase(Left(direction2, 1))
        'street suffix
        suffix = UCase(st.FixStreet(suffix))
        'extra info (after suffix)
        If Len(possible2) > 0 Then
            If address2 = vbNullString Then
                'if there's no addr2, put the extra stuff there
                address2 = possible2
            Else
                'if there is an addr2, keep everything in street name
                street = street & " " & suffix & " " & direction2 & " " & possible2
                'don't put these in twice
                suffix = vbNullString
                direction2 = vbNullString
            End If
        End If
    Else
        'otherwise leave as is
        street = address
    End If

    '--return the requested piece--'
    Select Case returnPiece
        Case "attn"
            splitAddress = attn
        Case "number"
            splitAddress = number
        Case "direction"
            splitAddress = direction
        Case "street"
            splitAddress = street
        Case "suffix"
            splitAddress = suffix
        Case "direction2"
            splitAddress = direction2
        Case "line2"
            splitAddress = address2
        Case Else
            splitAddress = vbNullString
    End Select

End Function
