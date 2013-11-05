Function splitAddress(address1, address2, return1 As Boolean, Optional returnPiece As String = vbNullString, Optional hasAttn As Boolean = False) As String
    'A function to return an piece of an address
    Dim re As RegExp, re_attn As RegExp, re_po As RegExp, re_comma As RegExp, re_dash As RegExp
    Dim matches
    Dim attn As String, number As String, direction As String, street As String, suffix As String, address As String, possible2 As String
    Dim reNum As String, reDir As String, reStreet As String
    Dim st As New Streets

    '--build main regex--'
    reNum = "^(?:((?:[0-9,&/ -]|and)*(?:[a-z])?) )"
    reDir = "(?:(NORTH|SOUTH|EAST|WEST|[NSEW]) )?"
    reAlphaStreet = "(?: ([a-z])  +)"   '-- wcw 2013/08/17
    '-- this last "?" looks extraneous, if not erroneous
    '-- ----------------------------------------------|
    '--                                               v
    reStreet = "((?:[0-9]+(?:ST|ND|RD|TH)|(?:[a-z])).*?)"
    reSuffix = "(?: +" & st.StreetRegEx & "(?:\.)?(?: +(NORTH|SOUTH|EAST|WEST|[NSEW]))?(?:,? +(.*))?)?$"

    '--set up regular expressions--'
    'main regex
    Set re = New RegExp
    re.Pattern = reNum & reDir & reStreet & reSuffix
    re.IgnoreCase = True 'True to ignore case
    re.Global = False 'False matches the first occurrence
    'alpha street (A Street, B Street, etc) regex -- wcw 2013/08/17
    Set re_alpha = New RegExp
    re_alpha.Pattern = reNum & reDir & reAlphaStreet & reStreet & reSuffix
    re_alpha.IgnoreCase = True 'True to ignore case
    re_alpha.Global = False 'False matches the first occurrence
    'attn regex
    Set re_attn = New RegExp
    re_attn.Pattern = "^(ATTN|C/O)"
    re_attn.Global = False
    re_attn.IgnoreCase = True
    'PO regex
    Set re_po = New RegExp
    re_po.Pattern = "^(P[. ][ ]?O.? )"
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
    If re.Test(address1) Then
        address = address1
    ElseIf re.Test(address2) Then 'if the 1 is not an address, and 2 is
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
        End If
    End If

    '--split and fix the addresses--'
    If re.Test(address) Or re_alpha.Test(address) Then
        If re_alpha.Test(address) Then
            'if possible, split the address
            Set matches = re_alpha.Execute(address)
            number = matches(0).SubMatches(0)
            direction = matches(0).SubMatches(1)
            street = matches(0).SubMatches(2) & matches(0).SubMatches(3)  '-- wcw 2013/08/17
            suffix = matches(0).SubMatches(4)  '-- wcw 2013/08/17
            direction2 = matches(0).SubMatches(5)  '-- wcw 2013/08/17
            possible2 = matches(0).SubMatches(6)  '-- wcw 2013/08/17
        Else If re.Test(address) Then
            Set matches = re.Execute(address)
            number = matches(0).SubMatches(0)
            direction = matches(0).SubMatches(1)
            street = matches(0).SubMatches(2)
            suffix = matches(0).SubMatches(3)
            direction2 = matches(0).SubMatches(4)
            possible2 = matches(0).SubMatches(5)
        End If

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

    '--return requested piece--'
    If return1 Then
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
            Case Else
                splitAddress = vbNullString
        End Select
    Else
        splitAddress = address2
    End If

End Function

