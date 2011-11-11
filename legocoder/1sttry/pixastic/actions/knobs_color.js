/*
 * Pixastic Lib - Brightness/Contrast filter - v0.1.1
 * Copyright (c) 2008 Jacob Seidelin, jseidelin@nihilogic.dk, http://blog.nihilogic.dk/
 * License: [http://www.pixastic.com/lib/license.txt]
 */

Pixastic.Actions.knobs_color = {

	process : function(params) {

		var knobs = params.options.knobs;

		if (typeof params.options.returnValue != "object") {
			params.options.returnValue = {values:[]};
		}
		var returnValue = params.options.returnValue;
		if (typeof returnValue.values != "array") {
			returnValue.values = [];
		}

		if (Pixastic.Client.hasCanvasImageData()) {
			var data = Pixastic.prepareData(params);
			var rect = params.options.rect;
			var w = rect.width;
			var h = rect.height;

			var p = w*h;
			var pix = p*4, pix1, pix2;

			function Color(r, g, b) {
			  this.r = r;
			  this.g = g;
			  this.b = b;
			}

			var r, g, b;
			colors = Array();
			for (i = 0; i < knobs.length; i++) {
				offset = (knobs[i].y*w + knobs[i].x)*4;
				r = data[offset];
				g = data[offset+1];
				b = data[offset+2];
				if (r < 128) { r = 0; } else { r = 255; }
				if (g < 128) { g = 0; } else { g = 255; }
				if (b < 128) { b = 0; } else { b = 255; }
				c = new Color(r, g, b);
				colors.push(c);
			}
			returnValue.values = colors;
			return true;
		}
	},
	checkSupport : function() {
		return Pixastic.Client.hasCanvasImageData();
	}
}

