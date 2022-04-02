/*
 * Copyright 2022 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
window.addEventListener("xlrelease.load", function() {
    window.xlrelease.queryTileData(function(response) {
		const chart = echarts.init(document.getElementById('main'), 'theme1');

		// Load data
		let businessObjects = response.data.data.businessObjects["businessObjects"];
		let startTimeField = response.data.data.startTimeField;
		let endTimeField = response.data.data.endTimeField;

		let timedeltas = businessObjects.map(businessObject => {
			// Get fields of interest (start and end datetimes)
			let startTime = ""
			let endTime = ""
			businessObject["fields"].forEach(field => {
				if (field["name"] == startTimeField) {
					startTime = Date.parse(field["value"])
				} else if (field["name"] == endTimeField) {
					endTime = Date.parse(field["value"])
				}
			});
			return times = {
				start: startTime,
				end: endTime
			}
		}).filter(times => {
			// Filter out results which do not have a start or end time
			return (times["start"] != "" && times["end"] != "")
		}).map(times => {
			// Calculate the timedelta, in milliseconds
			return (times["end"]-times["start"])
		});

		// Calculate average, in milliseconds
		let averageMs = timedeltas.reduce((total, timedelta) => total+timedelta) / timedeltas.length

		// Convert units and calculate "gauge score"
		let unit
		let pointer
		// The min and max feel reversed for the gauge, because speed is inverse of duration
		let conversions = [
			{unit: "milliseconds", range: {min: 1, max: 1000}, gauge: {min: 100, max: 100}},
			{unit: "seconds", range: {min: 1000, max: 60*1000}, gauge: {min: 100, max: 75}},
			{unit: "minutes", range: {min: 60*1000, max: 60*60*1000}, gauge: {min: 75, max: 50}},
			{unit: "hours", range: {min: 60*60*1000, max: 24*60*60*1000}, gauge: {min: 50, max: 25}},
			{unit: "days", range: {min: 24*60*60*1000, max: 30*24*60*60*1000}, gauge: {min: 25, max: 0}},
			{unit: "months", range: {min: 30*24*60*60*1000, max: Infinity}, gauge: {min: 0, max: 0}}
		]
		conversions.forEach(conversion => {
			if (conversion["range"]["min"] < averageMs && averageMs < conversion["range"]["max"]) {
				average = averageMs/conversion["range"]["min"]
				unit = conversion["unit"]
				// Linear interpolation between adjacent values
				pointer = conversion["gauge"]["min"]+(averageMs-conversion["range"]["min"])*(conversion["gauge"]["max"]-conversion["gauge"]["min"])/(conversion["range"]["max"]-conversion["range"]["min"])
			}
		});

		(function renderChart() {
			chart.setOption(getChartOptions());
		})();

		function getChartOptions() {
			return {
				tooltip: {
					formatter: `${average.toPrecision(3)} ${unit}`
				},
				series: [
					{
						type: 'gauge',
						radius: '100%',
						detail: {
							formatter: `${average.toPrecision(3)} ${unit}`,
							offsetCenter: [0, '90%']
						},
						data: [{value: pointer}],
						splitNumber: 4,
						axisLine: {
							lineStyle: {
								color: [
									[0.25, '#ae3f37'],
									[0.75, '#668199'],
									[1, '#5ea17d']
								],
								width: 24
							}
						},
						axisTick: {
							show: false
						},
						pointer: {
							width: 12,
							length: '70%'
						},
						splitLine: {
							length: 32,
							lineStyle: {
								color: 'auto',
								width: 8
							}
						},
						axisLabel: {
							fontSize: 'min(6vw, 6vh)',
							formatter: function (v){
								switch (v + '') {
									case '0' : return '1 Month';
									case '25' : return '1 Day';
									case '50' : return '1 Hour';
									case '75' : return '1 Minute';
									case '100' : return '1 Second';
								}
							}
						}
					}
				]
			}
		}

		window.addEventListener('resize', () => {
			chart.resize();
		});
	});
});
