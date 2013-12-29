 /*
  Copyright (C) 2013  Will Lee-Wagner
  whentheresawill.net
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

function isInArray(a,b){return a.indexOf(b)in a}function randRange(a,b,c){var d=c-b+1;return Math.floor(a*d)+b}function getCharByType(a,b){if("upper"===b)return String.fromCharCode(randRange(a,65,90));if("lower"===b)return String.fromCharCode(randRange(a,97,122));if("symbol"===b){var c=randRange(a,0,convTable.symCount);return convTable.symChars[c]}return"number"===b?randRange(a,0,9):void 0}function hexToASCII(a){for(var b="",c=0;c<a.length;c+=2)b+=String.fromCharCode(parseInt(a.substr(c,2),16));return b}function shuffle(a){for(var c,d,b=a.length;b;)d=Math.floor(Math.random()*b--),c=a[b],a[b]=a[d],a[d]=c;return a}function conversionTables(){for(var c,a=parseInt("!".charCodeAt(0)),b=0,d=[],e=[],f=0,h=["'",'"',"(",")","<",">","`","\\"];a<=parseInt("z".charCodeAt(0));){for(;isInArray(h,String.fromCharCode(a));)a++;d[b]=a,c=String.fromCharCode(a),("a">c||c>"z")&&("A">c||c>"Z")&&isNaN(c)&&(e[f]=c,f++),b++,a++}var i=[];return i.allChars=d,i.symChars=e,i.allCount=b-1,i.symCount=f-1,i}function GenPassword(){var d,a=document.getElementById("txt_site").value,b=document.getElementById("txt_password").value,c=document.getElementById("num_iteration").value,e=[];d=hexToASCII(CryptoJS.SHA256(a+b+c)+""),Math.seedrandom(d+"\0");for(var f=0;393>f;f++)Math.random();e.push(getCharByType(Math.random(),"lower")),e.push(getCharByType(Math.random(),"lower")),e.push(getCharByType(Math.random(),"upper")),e.push(getCharByType(Math.random(),"upper")),e.push(getCharByType(Math.random(),"number")),e.push(getCharByType(Math.random(),"symbol"));for(var g=0;g<=randRange(Math.random(),4,8);g++)e.push(String.fromCharCode(convTable.allChars[randRange(Math.random(),0,convTable.allCount)]));newPass=shuffle(e).join(""),document.getElementById("txt_new_pass").value=newPass,document.getElementById("txt_new_pass").focus(),document.getElementById("txt_new_pass").select()}try{chrome.tabs.query({currentWindow:!0,active:!0},function(a){var b=a[0].url.match(/^[\w-]+:\/*\[?([\w\.:-]+)\]?(?::\d+)?/)[1];b=b.replace("www.",""),document.getElementById("txt_site").value=b})}catch(e){}var convTable=conversionTables();document.addEventListener("DOMContentLoaded",function(){document.getElementById("btn_generate").addEventListener("click",GenPassword,!1)});