#!/usr/bin/env python2.7

import re

class Suffixes():
    '''Helps find and clean street suffixes'''
    
    def __init__(self):
        # hold the suffix options
        self.suffixes = [
            ["Aly", "Alley"],
            ["Ave", "Avenue"],
            ["Blvd", "Blv", "Boulevard"],
            ["Cir", "Circle"],
            ["Cres", "Crescent"],
            ["Ct", "Court"],
            ["Ctr", "Center"],
            ["Cv", "Cove"],
            ["Dr", "Drive"],
            ["Expy", "Expressway"],
            ["Fwy", "Freeway"],
            ["Hwy", "Highway"],
            ["Ln", "Lane"],
            ["Pkwy", "Parkway"],
            ["Pl", "Place"],
            ["Rd", "Road"],
            ["St", "Street"],
            ["Ter", "Terrace"],
            ["Trl", "Trail"],
            ["Way"]
        ]
    
    def suffix_regex(self):
        '''loop through self.suffixes to generate regex to find them'''
        all_streets = ''
        #loop though the suffix lists
        for suffix_list in self.suffixes:
            # loop through each suffix
            for suffix in suffix_list:
                if all_streets == '':
                    # start with a paren
                    all_streets = "(" + suffix
                else:
                    # use an or pipe to seperate options
                    all_streets += '|' + suffix
        # end with a paren
        all_streets += ')'
        
        return all_streets
    
    def fix_suffix(self,possible_suffix):
        '''check if a string is in the suffix list.
        if it is, return the shortened version.'''
        
        # return an empty string for blank input
        if not possible_suffix:
            return ''
        # if there is input, check it
        else:
            #loop though the suffix lists
            for suffix_list in self.suffixes:
                # loop through each suffix
                for suffix in suffix_list:
                    # check if the suffix is a match (including plurals)
                    if suffix == possible_suffix or suffix+'s' == possible_suffix:
                        # if found, return the first entry in that list
                        return suffix_list[0]
            # if the script gets here, it didn't find anything
            # just return the original string
            return possible_suffix
            

class Splitter_Regex():
    '''Regex to split a series of addresses'''
    
    def __init__(self):
        self.s = Suffixes()
        
        # set up the patterns for addresses
        re_num = r"^(?:((?:[0-9,&/ -]|and)*(?:[a-z])?) )"
        re_dir = r"(?:(NORTH|SOUTH|EAST|WEST|[NSEW]) )?"
        re_alphaStreet = r"(?: ([a-z])  +)"
        re_street = r"((?:[0-9]+(?:ST|ND|RD|TH)|(?:[a-z])).*?)"
        re_suffix = "(?: +{0}(?:\.)?(?: +(NORTH|SOUTH|EAST|WEST|[NSEW]))?(?:,? +(.*))?)?$".format(self.s.suffix_regex())
        
        # compile the regex
        self.re_addr = re.compile(re_num + re_dir + re_street + re_suffix + re_dir, re.I)
        self.re_alph = re.compile(re_num + re_dir + re_alphaStreet + re_suffix + re_dir, re.I)
        self.re_attn = re.compile(r"^(ATTN|C/O)", re.I)
        self.re_po = re.compile(r"^(P[. ][ ]?O.? )", re.I)
        self.re_dash = re.compile(r" *- *", re.I)
    

class Splitter():
    '''
    split a series of addresses.
    Takes an instance of the Splitter_Regex class
    '''
    
    def __init__(self, rs, address1, address2, has_attn=False):
        self.rs = rs
        self.address1 = address1
        self.address2 = address2
        self.has_attn = has_attn
        
        # set up a dictionary to hold the split address
        self.addys = {
            'attn': '',
            'number': '',
            'dir1': '',
            'street': '',
            'suffix': '',
            'dir2': '',
            'possible2':''
        }
        
        # split
        self.split()
    
    def address_prepare(self):
        # get address1 ready for regex
        if not self.address1:
            self.address1=''
        else:
            self.address1 = self.address1.strip()
        # get address2 ready for regex
        if not self.address2:
            self.address2=''
        else:
            self.address2 = self.address2.strip()
    
    def split_attn(self):
        '''check for an attn line'''
        # check the lines to see if they are attn lines
        attn_1 = self.rs.re_attn.match(address1)
        attn_2 = self.rs.re_attn.match(address2)
        # found in line 1
        if attn_1:
            # get the attention line
            self.addys['attn'] = address1
            # put line2 into line1
            self.address1 = self.address2
            self.address2 = ''
        # found in line2
        elif attn_2:
            self.addys['attn'] = self.address2
            self.address2 = ''
    
    def split_alph(self, addr_matches):
        pass
    
    def split_addr(self, addr_matches):
        # run the regex on the regular address
        self.addys['number'] = addr_matches.group(1)
        self.addys['dir1'] = addr_matches.group(2)
        self.addys['street'] = addr_matches.group(3)
        self.addys['suffix'] = addr_matches.group(4)
        self.addys['dir2'] = addr_matches.group(5)
        self.addys['line2'] = addr_matches.group(6)
    
    def corr_regex(self, regex1, regex2):
        ''' take two regex match sets, see which one fits, and return it'''
        if regex1:
            # if address is in line1
            return regex1
        elif regex2:
            # if address is in line1
            # switch line1 and line2
            address1, address2 = address2, address1
            # return the second regex match set
            return regex2
    
    def run_regex(self):
         # run main regex
        re_addr_1 = self.rs.re_addr.match(self.address1)
        re_alph_1 = self.rs.re_alph.match(self.address1)
        re_addr_2 = self.rs.re_addr.match(self.address2)
        re_alph_2 = self.rs.re_alph.match(self.address2)
        # set up holder for regex
        self.re_addr = ''
        self.re_alph = ''
        
        # determine if the address is an alpha or not, a split it out
        if re_alph_1 or re_alph_2:
            self.split_alph(self.corr_regex(re_alph_1, re_alph_2))
            return True
        elif re_addr_1 or re_addr_2:
            self.split_addr(self.corr_regex(re_addr_1, re_addr_2))
            return True
        else:
            return False
    
    def combine_street(self):
        '''combine other pieces with the street name, and clear them'''
        # set up a list of pieces to loop through
        pieces = [self.addys['suffix'],self.addys['dir2'],self.addys['line2']]
        # loop through the pieces
        for piece in pieces:
            # if there is anything in that piece
            if piece:
                # add it o the street
                self.addys['street'] = '{0} {1}'.format(self.addys['street'],piece)
                # clear it
                piece = ''
    
    def split(self):
        '''split an address'''
        
        # prepare the addresses for regex
        self.address_prepare()
        
        # check for an attn line (if requested)
        if self.has_attn:
            self.split_attn()
        
        # try to split out the addresses
        if self.run_regex():
            # set the street suffix to the abbrev.
            self.addys['suffix'] = self.rs.s.fix_suffix(self.addys['suffix'])
            
            # Clear out line2 if nessecary
            if self.address2:
                if self.addys['line2']:
                    # clear out line 2
                    self.combine_street()
                # move address2 to line2
                self.addys['line2'] = self.address2
        else:
            self.addys['street'] = self.address1


def main():
    rs = Splitter_Regex()
    sp = Splitter(rs, '123 Fake Street', '#4')
    print(sp.addys['street'])

if __name__ == '__main__':
    main()