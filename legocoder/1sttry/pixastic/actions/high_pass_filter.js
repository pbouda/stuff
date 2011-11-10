/*
 * Pixastic Lib - Brightness/Contrast filter - v0.1.1
 * Copyright (c) 2008 Jacob Seidelin, jseidelin@nihilogic.dk, http://blog.nihilogic.dk/
 * License: [http://www.pixastic.com/lib/license.txt]
 */

Pixastic.Actions.high_pass_filter = {

	process : function(params) {

		var min_value = parseInt(params.options.min_value) || 0;

		if (Pixastic.Client.hasCanvasImageData()) {
			var data = Pixastic.prepareData(params);
			var rect = params.options.rect;
			var w = rect.width;
			var h = rect.height;

			var p = w*h;
			var pix = p*4, pix1, pix2;

			var r, g, b;
			while (p--) {
				if ((r = data[pix-=4] ) > min_value )
					data[pix] = r;
				else
 					data[pix] = 0;

				if ((g = data[pix1=pix+1]) > min_value ) 
					data[pix1] = g;
				else
					data[pix1] = 0;

				if ((b = data[pix2=pix+2]) > min_value ) 
					data[pix2] = b;
				else
					data[pix2] = 0;
			}
			return true;
		}
	},
	checkSupport : function() {
		return Pixastic.Client.hasCanvasImageData();
	}
}

