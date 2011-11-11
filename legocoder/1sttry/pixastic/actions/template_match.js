/*
 * Pixastic Lib - Brightness/Contrast filter - v0.1.1
 * Copyright (c) 2008 Jacob Seidelin, jseidelin@nihilogic.dk, http://blog.nihilogic.dk/
 * License: [http://www.pixastic.com/lib/license.txt]
 */

Pixastic.Actions.template_match = {

	process : function(params) {
		
		var similarity_threshold = parseFloat(params.options.similarity_threshold) || 0.9;

		if (typeof params.options.returnValue != "object") {
			params.options.returnValue = {values:[]};
		}
		var returnValue = params.options.returnValue;
		if (typeof returnValue.values != "array") {
			returnValue.values = [];
		}

		var template_width = 24;
		var template_height = 24;
		var template_sum = 9752;
		var template = new Array(
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 88, 86, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 148, 255, 255, 235, 249, 168, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 178, 207, 138, 154, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 255, 255, 255, 206, 93, 0, 0, 0, 77, 0, 74, 72, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 133, 255, 255, 174, 78, 0, 0, 0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 255, 255, 243, 65, 0, 0, 0, 0, 0, 0, 0, 0, 0, 173, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 168, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 88, 100, 0, 0, 0, 0,
		    0, 0, 0, 0, 255, 255, 187, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 139, 0, 0, 0, 0,
		    0, 0, 0, 0, 245, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 205, 177, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 149, 97, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 93, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
		);		

		var diff_threshold = template_sum - (template_sum / 10);
		var template_width_half = template_width / 2;
		var template_height_half = template_height / 2;

		if (Pixastic.Client.hasCanvasImageData()) {
			var data = Pixastic.prepareData(params);
			var dataCopy = Pixastic.prepareData(params, true)
			var rect = params.options.rect;
			var w = rect.width;
			var h = rect.height;
			var w4 = w*4;
			var w4_wo_template = w4 + (template_width)*4;

			var max_diff = template_width * template_height * 255;
			var threshold = similarity_threshold * max_diff;
			
			var map_width  = w - template_width + 1;
			var map_height = h - template_height + 1;
			var map = new Array(); //int[mapHeight + 4, mapWidth + 4];
			for (y = 0; y < 2; y++) {
				var map_row = Array();
				for (x = 0; x < map_width + 4; x++) {
					map_row.push(0);
				}
				map.push(map_row);
			}
			
			var y = map_height;
			do {
				var offsetY = (y-1)*w4;
				var map_row = new Array();
				map_row.push(0); map_row.push(0);

				var x = map_width;
				do {
					var offset = offsetY + (x-1)*4;
					var offsetLine = offset;
					var dif = 0;
					var tpl_offset = template_width*template_height-1;
					var i = template_height;
					do {
						var j = template_width;
						offsetColumn = offsetLine;
						do {
							var src = dataCopy[offsetColumn];
							var tpl = template[tpl_offset];
							var d = src-tpl;
							if (d < 0) {
								d = -d;
							}
							dif = dif + d;
							offsetColumn-=4;
							tpl_offset-=1;
						} while (--j);
						offsetLine -= w4;
					} while (--i);
					var sim = max_diff - dif;
					if ( (sim > threshold) && (dif <  diff_threshold) ) {
						map_row.push(sim);
					} else {
						map_row.push(0);
					}
				} while (--x);
				map_row.push(0); map_row.push(0);
				map_row.reverse()
				map.push(map_row);
			} while (--y);
			for (y = 0; y < 2; y++) {
				var map_row = Array();
				for (x = 0; x < map_width + 4; x++) {
					map_row.push(0);
				}
				map.push(map_row);
			}
			map.reverse()
			
			var xValues = Array();
			var yValues = Array();
			for (y = 2, maxY = map_height+2; y < maxY; y++) {
				for (x = 2, maxX = map_width+2; x < maxX; x++) {
					var current_value = map[y][x];
					OUTER: for (i = -2; i <= 2; i++) {
						for (j = -2; j <= 2; j++) {
							if (map[y+i][x+j] > current_value) {
								current_value = 0;
								break OUTER;
							}
						}
					}
					if (current_value != 0) {
						xValues.push(x-template_width_half);
						yValues.push(y-template_height_half);
					}
				}
			}
			
			var maxPoints = xValues.length;
			if (maxPoints < 1) {
				return false;
			}

			var knobs = Array();
			function Point(x, y) {
			  this.x = x;
			  this.y = y;
			}
			
			if ( ( Math.abs(xValues[1] - xValues[0]) > template_width ) ||
			    ( Math.abs(yValues[1] - yValues[0]) > template_height ) )
			{
				k = new Point(xValues[0], yValues[0])
				knobs.push(k)
			}
			for (i = 1; i < maxPoints-1; i++) {
				if (
				    ( Math.abs(xValues[i+1] - xValues[i]) > template_width ) &&
				    ( Math.abs(xValues[i] - xValues[i-1]) > template_width ) ||
				    ( Math.abs(yValues[i+1] - yValues[i]) > template_height ) &&
				    ( Math.abs(yValues[i] - yValues[i-1]) > template_height )
				   ) {
					k = new Point(xValues[i], yValues[i])
					knobs.push(k)
				}
			}

			if ( ( Math.abs(xValues[maxPoints] - xValues[maxPoints-1]) > template_width ) ||
			    ( Math.abs(yValues[maxPoints] - yValues[maxPoints-1]) > template_height ) )
			{
				k = new Point(xValues[maxPoints], yValues[maxPoints])
				knobs.push(k)
			}
			returnValue.values = knobs;
			return true;
		}
	},
	checkSupport : function() {
		return Pixastic.Client.hasCanvasImageData();
	}
}

