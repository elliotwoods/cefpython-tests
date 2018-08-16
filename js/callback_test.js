function test_function() {
	$("body").append("<p>Test function called</p>");
}

async function call_test_object() {
	testObject.testMethod((returnValue) => {
		console.log("Returned from Python:");
		console.log(returnValue);
	});
}