function appendResult(result) {
	$("ul").append(`<li class="list-group-item">${result}</li>`);
}

function appendException(exception) {
	var exceptionElement = $('<li class="list-group-item list-group-item-danger"></li>');

	exceptionElement.append(`<h4 class="list-group-item-heading">${exception.message} [${exception.type}]</h4>`);

	var tracebackElement = $('<ol></ol>');
	for(let tracebackLine of exception.traceback) {
		tracebackElement.append(`<li><strong>${tracebackLine.filename}:${tracebackLine.lineNumber}</strong><br />${tracebackLine.line}</li>`);
	}
	exceptionElement.append(tracebackElement);

	$("ul").append(exceptionElement);
}

function test_function() {
	appendResult("Test function called");
}

async function pyCall(action) {
	return new Promise((resolve, reject) => {
		var successCallback = (returnValue) => {
			resolve(returnValue);
		};
		var exceptionCallback = (exception) => {
			console.log("Exception hit")
			reject(exception);
		};
		action(successCallback, exceptionCallback);
	});
}

async function call_test_object() {
	try {
		var iterationCounts = [1, 10, 100, 1000, 1e4, 1e5, 1e6];

		for(var iterationCount of iterationCounts) {
			var start = window.performance.now();

			for(var i=0; i<iterationCount; i++) {
				var result1 = await pyCall(testObject.quickMethod);
			}
			
			var end = window.performance.now();
	
			var duration = end - start;
			var durationPerIteration = duration / iterationCount;

			appendResult(`${iterationCount} js bindings (IPC actions) took ${duration}ms (${durationPerIteration} ms per each).`);
		}
		
	}
	catch(exception) {
		appendException(exception);
	}
}