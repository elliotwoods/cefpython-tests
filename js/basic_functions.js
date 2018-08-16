function test_function() {
	$("body").append("<p>Test function called</p>");
}

async function call_test_object() {
	var returnValue = await testObject.testMethod();
	console.log("Returned from Python:");
	console.log(returnValue);
}