/*
 * Copyright 2020 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
window.addEventListener("xlrelease.load", function() {
    window.xlrelease.queryTileData(function(response) {
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

		// Calculate average
		let averageMs = timedeltas.reduce((total, timedelta) => total+timedelta) / timedeltas.length

		// Convert units
		let unit
		// The min and max feel reversed for the gauge, because speed is inverse of duration
		let conversions = [
			{unit: "milliseconds", range: {min: 1, max: 1000}},
			{unit: "seconds", range: {min: 1000, max: 60*1000}},
			{unit: "minutes", range: {min: 60*1000, max: 60*60*1000}},
			{unit: "hours", range: {min: 60*60*1000, max: 24*60*60*1000}},
			{unit: "days", range: {min: 24*60*60*1000, max: 30*24*60*60*1000}},
			{unit: "months", range: {min: 30*24*60*60*1000, max: Infinity}}
		]
		conversions.forEach(conversion => {
			if (conversion["range"]["min"] < averageMs && averageMs < conversion["range"]["max"]) {
				average = averageMs/conversion["range"]["min"]
				unit = conversion["unit"]
			}
		});

		// Display result (precision=3)
		document.getElementById("value").textContent = `${average.toPrecision(3)} ${unit}`
	});
});
