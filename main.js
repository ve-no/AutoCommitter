
function replaceString(originalString, searchString, replacementString) {
	return originalString.replace(searchString, replacementString);
}

// Example usage
const originalString = "Hello, world!";
const searchString = "world";
const replacementString = "hi laila!";
const modifiedString = replaceString(originalString, searchString, replacementString);
console.log(modifiedString);
