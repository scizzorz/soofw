window.onload = function() {
	var toc = document.getElementById("toc");
	var sec0 = document.getElementsByTagName("section")[0];
	var em = 11 * 4 / 3;

	var offset = function(element) {
		var ret = [0, 0, 0, 0];
		var par = element;
		while(par) {
			ret[0] += par.offsetTop;
			ret[1] += par.offsetRight;
			ret[2] += par.offsetBottom;
			ret[3] += par.offsetLeft;
			par = par.offsetParent;
		}
		return ret;
	}

	var update_pos = function(element) {
		var sec_off = offset(element);
		toc.style.position = "fixed";
		toc.style.top = Math.max(2*em, 80 - window.pageYOffset) + "px";
		toc.style.left = (sec_off[3] + element.offsetWidth + 1*em - 4) + "px";
		toc.style.right = null;
	}

	window.onscroll = function() {
		update_pos(sec0);
	}
	window.onresize = function() {
		update_pos(sec0);
	}

	update_pos(sec0);
}
