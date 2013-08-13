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

var MouseListener = function (elementId, newPosition) {
	document.getElementById(elementId).addEventListener('mouseover', function() {
		document.getElementById('sidebarText').style.visibility='hidden';
		document.getElementById('sample_container').style.backgroundPosition='0 ' + newPosition;
	}, false);
	document.getElementById(elementId).addEventListener('mouseout', function() {
		document.getElementById('sample_container').style.backgroundPosition='0 0';
		document.getElementById('sidebarText').style.visibility='visible';
	}, false);
} 

var OrderToPx  = function (picPlacement) {
	const pxMultiplier = 300;
	return picPlacement * pxMultiplier + 'px'
}

//Set up a listener for hovering over buttons
document.addEventListener('DOMContentLoaded', function () {
	MouseListener('report',OrderToPx(1));
	MouseListener('turtle',OrderToPx(2));
	MouseListener('ellis',OrderToPx(3));
	MouseListener('poster',OrderToPx(4));
	MouseListener('sitePass',OrderToPx(5));
	MouseListener('rocket',OrderToPx(6));
	MouseListener('hull',OrderToPx(7));
	MouseListener('tajik',OrderToPx(8));
	
});