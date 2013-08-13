/*
	Copyright (C) 2013  Will Lee-Wagner

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

var MouseListener = function (textName) {
	document.getElementById(textName + '_link').addEventListener('mouseover', function() {
		document.getElementById('default_text').style.display='none';
		document.getElementById(textName + '_text').style.display='inline';
	}, false);
	document.getElementById(textName + '_link').addEventListener('mouseout', function() {
		document.getElementById(textName + '_text').style.display='none';
		document.getElementById('default_text').style.display='inline';
	}, false);
} 

//Set up a listener for hovering over buttons
document.addEventListener('DOMContentLoaded', function () {
	MouseListener('sitePass');
	MouseListener('sitePass_chrome');
	MouseListener('ellis');
});