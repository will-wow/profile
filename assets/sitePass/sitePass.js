 /*
  Copyright (C) 2013  Will Lee-Wagner
  whentheresawill.net
  2913-11-29
  
  This script generates a strong password from a seed site, password,
  and number. It uses outside scripts for hashing and random number 
  generation.
  
  In short, this creates a hash from all three inputs, and uses that
  as the seed for a random number generator. The generator creates
  the characters for the password, and is used to shuffle those
  characters.
*/

/*
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

//change a random 0-1 number into an interger range
function randRange(random_num, lower_bound, upper_bound) {
  var range = upper_bound - lower_bound + 1;
  return Math.floor(random_num * range) + lower_bound;
}

//add a specific character type
function getCharByType(random_num, charType) {
  
  if (charType === 'upper') {
    return String.fromCharCode(randRange(random_num,65,90));
  }
  else if (charType === 'lower') {
    return String.fromCharCode(randRange(random_num,97,122));
  }
  else if (charType === 'symbol') {
    var addChar = randRange(random_num,0,convTable.symCount);
    return convTable.symChars[addChar];
  }
  else if (charType === 'number') {
    return randRange(random_num,0,9);
  }
}

//Fisher–Yates shuffle from:
//http://bost.ocks.org/mike/shuffle/
function shuffle(array) {
  var m = array.length, t, i;

  // While there remain elements to shuffle…
  while (m) {

    // Pick a remaining element…
    i = Math.floor(Math.random() * m--);

    // And swap it with the current element.
    t = array[m];
    array[m] = array[i];
    array[i] = t;
  }

  return array;
}

//create an array that holds the unicode conversion chart
function conversionTables() {
  var uCode = parseInt('!'.charCodeAt(0)); //unicode to convert to. (the first valid char is !)
  var cCode = 0; //codes the generator will convert from
  var thisChar; //hold a char to check its type
  var conversionChart = []; //the main conversion chart
  var symbolsAllowed = []; //generate a list of allowed symbols
  var symbolCounter = 0;
  var charsUpperLevel;
  var notAllowed = ["'",'"','(',')','<','>','`','\\'];

  //loop through each unicode char, ! to z
  while (uCode <= parseInt('z'.charCodeAt(0))){ 
    //go to the next uCode if this one is not allowed
    while (isInArray(notAllowed,String.fromCharCode(uCode))){ 
      uCode++;
    }
    //add the code to the conversion array
    conversionChart[cCode] = uCode;
    //get the actual character
    thisChar = String.fromCharCode(uCode);
    // check if it is a symbol
    if (((thisChar<'a' || thisChar>'z') && (thisChar<'A' || thisChar>'Z')) && (isNaN(thisChar))) {
      // if it is, add it to the symbol array
      symbolsAllowed[symbolCounter] = thisChar;
      // increment the symbol counter (to be used later)
      symbolCounter++;
    }
    //increment
    cCode++;
    uCode++;
  }
  
  //return the tables and counts
  var returnTable = [];
  returnTable.allChars = conversionChart;
  returnTable.symChars = symbolsAllowed;
  returnTable.allCount = cCode - 1;
  returnTable.symCount = symbolCounter - 1;
  
  return returnTable;
}

//main function
function GenPassword() {
  var siteName = document.getElementById("txt_site").value;   //get the given site name
  var passWord = document.getElementById("txt_password").value; //get the given password
  var iterationNum = parseInt(document.getElementById("num_iteration").value); //get the given iteration#
	var hashedPass; //will hold a hashed version of the password & site
	var passChars = []; //an array to hold the password chars to shuffle
	
  //hash the sitename and password
  hashedPass = new String(CryptoJS.SHA256(siteName + passWord + iterationNum)) + "";
  
  //init the random number generator with the hash 
  Math.seedrandom(hashedPass + '\0');
  
  //throw out the first 786 bytes (these are biased)
  for (var i=0;i<3072;i++){Math.random()}
  
  //Add specific char types
  //two lower, two upper, a number, and a symbol 
  //is a standard password requirement
  passChars.push(getCharByType(Math.random(),'lower'));
  passChars.push(getCharByType(Math.random(),'lower'));
  passChars.push(getCharByType(Math.random(),'upper'));
  passChars.push(getCharByType(Math.random(),'upper'));
  passChars.push(getCharByType(Math.random(),'number'));
  passChars.push(getCharByType(Math.random(),'symbol'));
  
  //add 4 to 8 more random chars (for a total size of 10-14 chars)
  for (var n=0;n<=randRange(Math.random(),4,8);n++)
  {
    passChars.push(String.fromCharCode(convTable.allChars[randRange(Math.random(),0,convTable.allCount)]));
  }
  
  //Shuffle the chars to generate the final password
  newPass = shuffle(passChars).join('');
  
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
//suppress errors, allow password to go to the example.com default
}

//generate the conversion tables
var convTable = conversionTables();

//Triggers the create new password function by clicking the Gen button
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("btn_generate").addEventListener('click', GenPassword, false);
});