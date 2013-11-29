 /*
    Copyright (C) 2013  Will Lee-Wagner
    whentheresawill.net

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

//check if a value is in an array
function isInArray(arrayName,character) {
    return arrayName.indexOf(character) in arrayName;
}

//add a missing character
function doAddChar(newPass, hashedPass, x, charType, charDomain, hashStart, hashEnd) {
    var addChar;
    var editedNewPass = "";
    var location;
    var secretNum = parseInt(hashedPass.substring(hashStart,hashEnd),16);
    location = (secretNum*x) % (newPass.length);
    addChar = (secretNum*x) % charDomain;
    if (charType === 'upper') {
        addChar = String.fromCharCode(addChar + 65);
    }
    else if (charType === 'lower') {
        addChar = String.fromCharCode(addChar + 97);
    }
    else if (charType === 'symbol') {
        addChar = symbolsAllowed[addChar];
    }
    else if (charType === 'number') {
        addChar =  addChar + 1;
    }
    editedNewPass = newPass.substring(0,location) + addChar + newPass.substring(location+1,newPass.length);
    return editedNewPass;
}


//main function
function GenPassword() {
    var siteName = document.getElementById("txt_site").value;     //get the given site name
    var passWord = document.getElementById("txt_password").value; //get the given password
	var passLength; // the length of the final password
    var hashedPass; //will hold a hashed version of the password & site
    var iterationNum = parseInt(document.getElementById("num_iteration").value); //get the given iteration#
    var lengthNum; //a randomized number generated from the hash
    var secretNum; //a randomized number generated from the hash
    var hashChar; //use to generate the newPass, letter by letter
    var checkChar; //to check if a given char type is in the password
    var counterCap = 0; //counts to make sure there are two capital letters
    var counterLow = 0; //counts to make sure there are two lower case letters
    var x = 0; //increase the location by one to get everthing to fit
    var hasCap = false;    //true if the pass has 2 cap letters
    var hasLow = false;    //true if the pass has 2 lowercase letters
    var hasNumber = false; //true if the pass has 2 numbers
    var hasSymbol = false; //true if the pass has 2 symbols
    var newPass = ""; //add letters to make the new password
	
    //hash the sitename and password
    hashedPass = new String(CryptoJS.SHA256(siteName + passWord + iterationNum));
    
    //generate a randomized number from the hash, to use to set the lenght
    lengthNum =  parseInt(hashedPass.substring(1,4),16);
    //generate another randomized number from the hash, to use later
    secretNum =  parseInt(hashedPass.substring(6,9),16);
    
    //set the pass length to between 10 and 14 to help aid security
    passLength = (lengthNum % 6) + 9
    
    //Generate a usable pass
    for (var i=0;i<passLength;i++)
    {   
        //Convert the number with digits i to i+3 to a decimal number
        hashChar =  parseInt(hashedPass.substring(i,i+3),16) % charsUpperLevel;
        //Convert the hashChar to a number within the
        //range of characters we want to convert to
        hashChar = String.fromCharCode(conversionChart[hashChar]);

        newPass = newPass + hashChar;
    }

    //checking for missing characters, looping to make sure one does not cover another

    while (hasCap === false || hasLow === false || hasNumber === false || hasSymbol === false) {
        x++;
		hasCap = false; hasLow = false; hasNumber = false; hasSymbol = false; //reset checkers
        counterLow = 0; counterCap = 0;
        for (c=0;c<newPass.length;c++) {
            checkChar = newPass.substring(c,c+1);
            //check the character type, to put missing types in later if nessecary
            if (!isNaN(checkChar)) { //number
                hasNumber = true;
            }
            else if (isInArray(symbolsAllowed,checkChar)) { //symbol
                hasSymbol = true;
            }
            else if (checkChar.toLowerCase() === checkChar) { //lower case
                counterLow ++;
                if (counterLow >= 2) {
                    hasLow = true; //make sure there are two
                }
            }
             else if (checkChar.toUpperCase() === checkChar) { //capital
                hasCap ++;
                if (counterCap >= 2) {
                    hasCap = true; //make sure there are two
                }
            }
        }
		//add missing charaters
        if (hasNumber === false) {
            newPass = doAddChar(newPass, hashedPass, x, 'number', 10, 1, 4);
        }
        else if (hasSymbol === false) {
            newPass = doAddChar(newPass, hashedPass, x+1, 'symbol', symbolCounter, 5, 8);
        }
        else if (hasLow === false) {
            newPass = doAddChar(newPass, hashedPass, x+2, 'lower', 26, 9, 12);
        }
        else if (hasCap === false) {
            newPass = doAddChar(newPass, hashedPass, x+3, 'upper', 26, 13, 16);
        }
		
		//after 100 tries, just give up
		//this should almost never happen, but it stops long loops from ever happening
		if (x===100) {
			hasNumber = true;
			hasSymbol = true;
			hasLow = true;
			hasCap = true;
		}
    } 

    //output the password
    document.getElementById("txt_new_pass").value = newPass; //place the pass
    document.getElementById("txt_new_pass").focus(); //move the cursor to it
	document.getElementById("txt_new_pass").select(); //select it, so the user can just hit ctrl-c
}


///////////////////////////
// calling the functions //
///////////////////////////

//Set the website to the URL of the active site
try {chrome.tabs.query({ currentWindow: true, active: true }, function (tab) {
    // regular expression to get the domain
    var domain_name = tab[0].url.match(/^[\w-]+:\/*\[?([\w\.:-]+)\]?(?::\d+)?/)[1];
	//drop the www.
	domain_name = domain_name.replace("www.","");
	//set the box
	document.getElementById("txt_site").value = domain_name;
});}

catch(e){
//suppress errors, allow password to go to example.com default
}

//create an array that holds the unicode conversion chart
var uCode = parseInt('!'.charCodeAt(0)); //unicode to convert to. (the first valid char is !)
var cCode = 0; //codes the generator will convert from
var thisChar; //hold a char to its test validity
var anotherLetter = true;
var conversionChart = new Array();
var symbolsAllowed = new Array(); //generate a list of allowed symbols
var symbolCounter = 0;
var notAllowed = new Array("'",'"','(',')','<','>','`');

while (uCode <= parseInt('z'.charCodeAt(0))){ //z is the last valid character
    while (isInArray(notAllowed,String.fromCharCode(uCode))){ //go to the next uCode if this one is not allowed
        uCode++;
    }
    conversionChart[cCode] = uCode;
    cCode++;
    //this doubles the number of letters, so there should be enough of them
    thisChar = String.fromCharCode(uCode);
    if ((thisChar>='a' && thisChar<='z') || (thisChar>='A' && thisChar<='Z')) {
        if (anotherLetter === true) {
            anotherLetter = false; //the next character will be the same as the current letter
        }
        else {
            uCode++; //the next char will be different
            anotherLetter = true;
        }
    }
    else {
		//make the symbol list
        if (isNaN(thisChar)){ 
            symbolsAllowed[symbolCounter] = thisChar;
            symbolCounter++;
        }
        uCode++;
        anotherLetter = true;
    }
}
var charsUpperLevel = cCode; //set as the number of possible characters + 1 (so the remainder is correct)


//test the distribution of the characters
function charFreq() {
    var charHolder = ""; //hold the string of password chars
    var charCounter = 0; //count the instances of a char
    for (x=1; x<10000; x++) {
        document.getElementById("num_iteration").value = x;
        GenPassword();
        charHolder = charHolder + document.getElementById("txt_new_pass").value;
    }

    for (y=0; y<charsUpperLevel; y++){
        for (z=0; z<=charHolder.length; z++) {
            if (charHolder.substring(z,z+1) === String.fromCharCode(conversionChart[y])) {
                charCounter = charCounter+1;
            }
        }
    console.debug(String.fromCharCode(conversionChart[y]) + ': ' + charCounter);
    charCounter = 0;
    }
}


//Triggers the create new password function by clicking
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("btn_generate").addEventListener('click', GenPassword, false);
});
